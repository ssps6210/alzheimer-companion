#!/usr/bin/env python3
"""隱私掃描：擋住任何個人資料被 commit 進版本庫。

這個專案處理的是家人的聲音、長輩的照片與私人對話——外流一次就收不回來。
`.gitignore` 是第一道防線，但它擋不住 `git add -f`、擋不住規則寫錯（歷史上真的
發生過：行尾註解讓整條規則失效，害 father_reference.txt 差點外流）。
這支是第二道防線：檢查「**已被 git 追蹤**」的檔案，發現個資就讓 CI 紅燈。

用法：
    python tools/privacy_scan.py          # 掃描已追蹤檔案
    python tools/privacy_scan.py --staged # 只掃暫存區（可當 pre-commit hook）

規則對齊 .gitignore 與 docs/上傳前隱私檢查清單.txt。
"""
import re
import subprocess
import sys

# ── 一、依檔名/路徑判定：這些東西本來就不該進版本庫 ──────────────────
FORBIDDEN_PATTERNS = [
    (r"\.(wav|mp3|m4a|aac|flac|ogg)$", "音檔（家人聲音／長輩錄音）"),
    (r"^(recordings|voices|photos|samples|legacy)/", "個人媒體資料夾"),
    (r"father_reference\.", "父親參考音／逐字稿"),
    (r"^reference_.*\.(wav|txt)$", "參考音／逐字稿"),
    (r"memory\.json$", "對話記憶（長輩的私人對話）"),
    (r"\.consent\.json$", "同意證明（含音檔雜湊）"),
    (r"^conf\.yaml$", "本地設定（可能含個人化 persona）"),
    (r"^ui_state\.json$", "本機執行期狀態"),
    (r"^\.env$", "環境變數（含 API 金鑰）"),
    (r"^\.env\.", "環境變數變體"),
]
# 明確放行：這些是刻意提供的範本
ALLOWLIST = {".env.example", "conf.example.yaml", "conf.cpu.example.yaml"}

# ── 二、依內容判定：金鑰樣式 ─────────────────────────────────────
SECRET_PATTERNS = [
    (r"nvapi-[A-Za-z0-9_\-]{20,}", "NVIDIA API 金鑰"),
    (r"\bsk-[A-Za-z0-9]{20,}", "OpenAI 型式金鑰"),
    (r"\b\d{8,10}:[A-Za-z0-9_\-]{35}\b", "Telegram bot token"),
]
# 只掃文字檔，且跳過這支自己（不然規則字串會誤判）
TEXT_EXTS = (".py", ".ps1", ".sh", ".bat", ".md", ".txt", ".yaml", ".yml",
             ".json", ".xml", ".java", ".gradle", ".properties", ".html")
SELF = "tools/privacy_scan.py"


def tracked_files(staged=False):
    cmd = (["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"]
           if staged else ["git", "ls-files"])
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                         errors="replace")
    if out.returncode != 0:
        print("✗ 無法執行 git（不在 git repo？）", file=sys.stderr)
        sys.exit(2)
    return [f for f in out.stdout.splitlines() if f.strip()]


def scan():
    staged = "--staged" in sys.argv
    files = tracked_files(staged)
    violations = []

    for f in files:
        if f in ALLOWLIST:
            continue
        for pat, why in FORBIDDEN_PATTERNS:
            if re.search(pat, f, re.IGNORECASE):
                violations.append((f, f"檔名符合禁止規則：{why}"))
                break

        if f != SELF and f.lower().endswith(TEXT_EXTS):
            try:
                with open(f, encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
            except OSError:
                continue
            for pat, why in SECRET_PATTERNS:
                m = re.search(pat, content)
                if m:
                    violations.append((f, f"內容疑似含{why}：{m.group()[:12]}…"))

    scope = "暫存區" if staged else "已追蹤檔案"
    if violations:
        print(f"\n✗ 隱私掃描失敗——{scope}中發現 {len(violations)} 個問題：\n")
        for path, why in violations:
            print(f"  • {path}\n      {why}")
        print("\n這些檔案不該進版本庫。處理方式：")
        print("  git rm --cached <檔案>    # 從版本庫移除，本機保留")
        print("  然後確認 .gitignore 有擋住它（注意：規則後面不能接行尾註解）\n")
        return 1

    print(f"✓ 隱私掃描通過（{scope} {len(files)} 個檔案，未發現個資或金鑰）")
    return 0


if __name__ == "__main__":
    sys.exit(scan())
