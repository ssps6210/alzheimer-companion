#!/usr/bin/env python3
"""提交前的安全閘門：改到護欄或人設，就得先過測試才能 commit。

為什麼要擋在 commit 前：CONTRIBUTING 寫了「改 persona 要重跑 test_safety.py」，
但規定靠人記得，遲早會忘一次——而忘的那一次，代價由長輩承擔。

兩道檢查：
  1. 改到 companion_web.py、lang/、tests/ 的護欄檔 → 跑離線的 tests/test_guards.py
     （一秒左右，不需要模型）。紅燈就擋。
  2. 改到人設或情境（conf.example.yaml、lang/*.yaml、tests/safety_cases.yaml）→
     要求 tests/test_safety.py 對「現在這份內容」全綠過。test_safety.py 全過時
     會寫下 tests/.safety_stamp（內容指紋），這裡比對指紋；對不上就擋。
     真的沒辦法跑模型（例如雲端環境沒有 Ollama）時，設 SKIP_LIVE_SAFETY=1 放行，
     並在 PR 裡寫明「真模型測試還沒跑」。

兩種掛法：
  · Claude Code：.claude/settings.json 的 PreToolUse 鉤子（--claude，從 stdin 讀指令）
  · 一般 git：  git config core.hooksPath .githooks  （.githooks/pre-commit 呼叫 --git）
"""
import glob
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAMP = os.path.join(ROOT, "tests", ".safety_stamp")

GUARD_FILES = ("companion_web.py", "tests/test_guards.py", "tests/test_care.py",
               "family.example.yaml")
PERSONA_FILES = ("conf.example.yaml", "tests/safety_cases.yaml")


def persona_fingerprint():
    """人設與危險情境的內容指紋。test_safety.py 全過時寫入，這裡用來比對。"""
    h = hashlib.sha256()
    paths = [os.path.join(ROOT, p) for p in PERSONA_FILES]
    paths += sorted(glob.glob(os.path.join(ROOT, "lang", "*.yaml")))
    for p in paths:
        if os.path.exists(p):
            h.update(os.path.relpath(p, ROOT).replace("\\", "/").encode())
            with open(p, "rb") as f:
                h.update(f.read())
    return h.hexdigest()


def changed_files():
    """這次 commit 會帶進去的檔案：已 stage 的，加上工作目錄裡改過的
    （Claude 常用 `git add -A && git commit`，鉤子跑的時候還沒 add）。"""
    out = set()
    for args in (["git", "diff", "--cached", "--name-only"], ["git", "diff", "--name-only"]):
        try:
            r = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=20)
            out.update(l.strip() for l in r.stdout.splitlines() if l.strip())
        except Exception:
            pass
    return out


def _python():
    for p in (os.path.join(ROOT, "venv", "Scripts", "python.exe"),
              os.path.join(ROOT, "venv", "bin", "python"),
              os.path.join(ROOT, ".venv", "Scripts", "python.exe"),
              os.path.join(ROOT, ".venv", "bin", "python")):
        if os.path.exists(p):
            return p
    return sys.executable


def run_offline_tests():
    """回 None（通過或沒裝 pytest）或錯誤訊息。"""
    py = _python()
    probe = subprocess.run([py, "-c", "import pytest"], capture_output=True)
    if probe.returncode != 0:
        print("（沒裝 pytest，略過離線護欄測試：venv\\Scripts\\pip install pytest）",
              file=sys.stderr)
        return None
    r = subprocess.run([py, "-m", "pytest", "-q", "tests/test_guards.py", "tests/test_care.py"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        tail = "\n".join((r.stdout + r.stderr).strip().splitlines()[-25:])
        return "離線護欄測試沒過（tests/test_guards.py）：\n" + tail
    return None


def check(files):
    problems = []
    lang = any(f.startswith("lang/") and f.endswith(".yaml") for f in files)
    if lang or any(f in GUARD_FILES or f in PERSONA_FILES for f in files):
        err = run_offline_tests()
        if err:
            problems.append(err)
    if (lang or any(f in PERSONA_FILES for f in files)) and \
            os.environ.get("SKIP_LIVE_SAFETY") != "1":
        stamp = ""
        if os.path.exists(STAMP):
            with open(STAMP, encoding="utf-8") as f:
                stamp = f.read().strip()
        if stamp != persona_fingerprint():
            problems.append(
                "人設、語言包或危險情境改過了，但 tests/test_safety.py 還沒對這份內容全綠跑過。\n"
                "  先跑：venv\\Scripts\\python.exe tests\\test_safety.py\n"
                "  真的沒有模型可跑（例如雲端環境）：設 SKIP_LIVE_SAFETY=1 再 commit，"
                "並在 PR 寫明「真模型測試還沒跑」。")
    return problems


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--git"
    if mode == "--claude":
        try:
            cmd = (json.load(sys.stdin).get("tool_input") or {}).get("command", "")
        except Exception:
            return 0
        if "git commit" not in cmd:
            return 0
        # 鉤子跑在 Claude Code 的程序裡，讀不到單一指令前綴的環境變數，
        # 所以 `SKIP_LIVE_SAFETY=1 git commit ...` 要從指令字串本身認
        if "SKIP_LIVE_SAFETY=1" in cmd:
            os.environ["SKIP_LIVE_SAFETY"] = "1"
    problems = check(changed_files())
    if not problems:
        return 0
    print("⛔ 安全閘門擋下這次 commit：\n\n" + "\n\n".join(problems), file=sys.stderr)
    # Claude Code 的 PreToolUse：exit 2 = 擋下並把 stderr 交給 Claude；git 鉤子：非 0 即擋
    return 2


if __name__ == "__main__":
    sys.exit(main())
