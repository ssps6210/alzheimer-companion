# Phase 0 啟動清單 — 最小可用迴圈（只用 edge-tts，不碰 CosyVoice）

目標：先證明「平板說話 → 聽到回應」整條迴圈會動。
這一步**不啟動 WSL2 的 CosyVoice**，語音由 edge-tts 提供（通用男聲）。
跑通它 = 你已經有一個能用的陪伴系統，只是還沒換成家人的克隆聲音。

---

## 0. 前置確認（一次性）

PC（Windows）需要這些 Python 套件：
```powershell
pip install faster-whisper fastapi uvicorn requests numpy edge-tts
```
- Whisper 用 GPU，需要 CUDA 環境（你 RTX 4060 已具備）。
- edge-tts 需要**能連外網**（它打 Microsoft 的服務）。

---

## 1. 設 MiMo API Key（用 rotate 過的新 key）

```powershell
$env:MIMO_API_KEY = "你rotate後的新key"
```
> ⚠️ 舊 key 已在對話中外洩，記得先去小米後台換一條。
> 想長期生效：`setx MIMO_API_KEY "新key"`（設完要重開終端機）。

---

## 2. 啟動 server

```powershell
python D:\elder-companion\companion_web.py
```
啟動成功應看到：
- `固定句快取：載入 N 條`（沒錄音檔就是 0 或略過，正常）
- `載入 Whisper...` → `Whisper 就緒`
- **沒有**出現 `⚠ 未設定 MIMO_API_KEY`（出現代表 key 沒吃到）
- 最後印出 `平板 Chrome 打開：http://<你的IP>:8080`

---

## 3. 在 PC 上先驗 /health（關鍵診斷）

瀏覽器開 `http://localhost:8080/health`，預期：
```json
{
  "status": "degraded",                      // Phase 0 預期：degraded
  "whisper": {"loaded": true, "size": "medium"},
  "mimo": {"ok": true, "latency_ms": 800},   // 必須 ok
  "cosyvoice": {"ok": false, "error": "...未啟動..."},  // Phase 0 正常，因為沒開
  "edge_tts": {"available": true},
  "phrases": 0
}
```
- `mimo.ok = true` → key + 端點都通 ✅
- `cosyvoice.ok = false` → **這步是正常的**（我們還沒啟動它）
- 若 `whisper.loaded=false` 或 `mimo.ok=false` → 先解決這個，別往下走

---

## 4. 開 HTTPS tunnel（平板麥克風必須 HTTPS）

手機/平板瀏覽器**只在 HTTPS 或 localhost 下才給麥克風權限**，
所以區網 http://<IP>:8080 在平板上錄不了音 → 需要 tunnel。

擇一：
```powershell
# cloudflared（免費、不用註冊）
cloudflared tunnel --url http://localhost:8080

# 或 ngrok
ngrok http 8080
```
記下它給的 `https://xxxx.trycloudflare.com`（或 ngrok 網址）。

---

## 5. 平板實測

1. 平板 Chrome 開那個 **https** 網址。
2. 第一次會問**麥克風權限 → 允許**。
3. 按住「🎤 按住說話」，講一句（例如「早安」），放開。
4. 預期流程：`識別中...` → `回應中...` → **聽到 edge-tts 男聲回覆**，畫面顯示你說的話 + 回覆文字。

---

## 6. 出問題對照表

| 症狀 | 可能原因 / 處理 |
|---|---|
| 平板按了沒反應、沒問權限 | 不是 HTTPS（用 tunnel 網址，不是 http://IP） |
| 顯示「請允許麥克風，再按一次」 | 權限被拒，到瀏覽器網站設定重新允許 |
| 有字幕但沒聲音（iOS） | 調高音量；已加 ctx.resume，仍無聲就回報我 |
| 「連線錯誤，請重試」 | server 沒開 / tunnel 斷 / 網址打錯 |
| 「回應太慢，請重試」 | MiMo 太慢或斷網；先看 /health 的 mimo |
| 一直「我現在有點問題」 | MiMo 錯誤，看終端機 `MiMo 錯誤：` 那行 |
| /health 的 mimo.ok=false | key 沒設對 / 端點連不到 / 無外網 |

---

## ✅ 成功標準
平板按住說話 → 放開 → **幾秒內聽到一句溫暖的男聲回應**。
做到這步就回報我，我們再上 **Phase 1：接上 CosyVoice 克隆聲音**。

回報時方便的話貼給我：
- `/health` 的 JSON
- 終端機那幾行 log（阿公：… / 回應：…）
- 平板上實際的體感（延遲、有沒有聲音）
