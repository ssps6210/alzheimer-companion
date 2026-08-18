# 阿公語音陪伴系統 · Elder Voice Companion

> 用**家人的聲音**，陪伴失智長者。
> A voice companion for elders with dementia — it answers in a **family member's cloned voice**.

長輩在平板上「**按住按鈕說話**」，系統就用你設定的**親人聲音**溫柔回應他。
目標不是做一個聰明的 AI，而是做一個「**永遠耐心、永遠都在、聽起來像親人**」的陪伴者。

---

## 為什麼是這樣設計

- 🚫 **不要虛擬人臉 / Avatar** —— 會動的合成臉對失智長者是驚嚇來源（尤其半夜意識混亂時）。閒置畫面改用**長輩自己的舊照片**慢速輪播（有實證的「懷舊療法」）。
- 🎙️ **家人的聲音才是核心** —— 一顆大按鈕、家人克隆聲、安全護欄，才是價值所在。
- 🔒 **隱私優先** —— 長輩的對話**留在你自己的機器**，不上任何雲端資料庫（只有 LLM 那一次呼叫走 API）。
- 🧓 **為長者設計的極簡介面** —— 一顆大到手抖也好按的按鈕；日系暖色、日夜自動切換；可選「按住說話」或「自動連續對話」。

## 安全護欄（給失智照護）

不糾正、不催促、永遠耐心重複回答；找已故親人時溫柔安撫不揭穿；偵測到不適/求助句可**通報家人**（Telegram）。人設只放「行為傾向」，不塞私人資料庫。

---

## 🎙️ 自帶你的聲音（重要）

**這個 repo 不含任何人的聲音**（家人錄音、照片、對話記錄都被 `.gitignore` 擋掉了）。
所以 clone 下來後，**你要放進自己想要的音色**：

1. 啟動後開 **`http://<你的電腦>:8080/setup`**（家人設定台）
2. 找「**🎙 設定陪伴聲音（音色）**」
3. 上傳一段**清楚、安靜、連續 10–30 秒**的人聲（wav / mp3 / m4a），逐字稿可留空（會自動辨識）
4. 按「設為陪伴聲音」→ 即時套用，長輩馬上聽到這個聲音

> 還沒設定音色前，系統會用通用聲（edge-tts）頂著，不會壞。

---

## 架構

```
 平板(長輩) ──HTTPS──▶ PC (Windows + NVIDIA GPU)
                         ├─ companion_web.py  :8080   前端 + /setup + 大腦串接
                         │    ├─ STT：faster-whisper（本地）
                         │    ├─ LLM：OpenAI 相容 API（預設 NVIDIA Nemotron，可換）
                         │    ├─ 固定句快取（家人真聲，秒回）
                         │    └─ 記憶 / 家人通報
                         └─ WSL2 Ubuntu：qwen_tts_api.py :50000
                              └─ Qwen3-TTS 零樣本聲音克隆
```

- **STT**：`faster-whisper`（本地，免 API）
- **LLM**：任何 OpenAI 相容端點（`conf.yaml` 的 `llm` 段可換 base_url / model）
- **TTS**：`Qwen/Qwen3-TTS-12Hz-1.7B-Base` 零樣本克隆（Apache-2.0）

## 需求

- Windows 11 + **NVIDIA GPU**（8GB 可跑；whisper + Qwen 同卡）
- **WSL2**（Ubuntu）跑語音克隆
- 一組 OpenAI 相容的 LLM 金鑰（預設 [build.nvidia.com](https://build.nvidia.com) 免費 Nemotron）

## 快速開始

```bash
# 1) 金鑰
cp .env.example .env          # 填入 NVIDIA_API_KEY（或改 conf.yaml 換別家 LLM）

# 2) Windows 端（companion）
python -m venv venv
venv\Scripts\pip install -r requirements.txt

# 3) WSL2 端（Qwen 語音克隆）：在 Ubuntu 裝好 qwen-tts（見 PROJECT.md）
#    python -m venv /root/rvc_env && /root/rvc_env/bin/pip install qwen-tts soundfile ...

# 4) 啟動（Windows 雙擊）：一鍵啟動.bat
#    會先起 companion、等語音辨識載完、再起 Qwen（錯開 GPU）
```

啟動後：長輩畫面 `http://localhost:8080/`、家人設定台 `http://localhost:8080/setup`。
**設定音色**見上面「自帶你的聲音」。完整安裝/排錯細節見 [`PROJECT.md`](PROJECT.md)。

> 平板要用麥克風需 **HTTPS 或 localhost**（瀏覽器規定）。同一 WiFi 可在平板 Chrome 的
> `chrome://flags` →「Insecure origins treated as secure」加入 `http://<電腦IP>:8080`；
> 或用 cloudflared / ngrok 開一個 https 通道。

## 設定（`conf.yaml`）

改這裡就能換模組，不用動程式：`asr`（whisper 大小）、`llm`（base_url / model / 金鑰變數名）、
`tts`、`memory`、`notify`（Telegram）、`characters`（人設 + 對應音色）。金鑰一律走環境變數，不入庫。

---

## 隱私與安全

- `.gitignore` 已排除**所有聲音、照片、原始錄音、對話記憶、金鑰**——這個 repo 不含任何個人資料。
- 長輩的對話存在本機 `memory.json`（不入庫）；只有 LLM 呼叫會離開本機。
- 你上傳的音色存在本機 `voices/`（不入庫）。

## ⚠️ 免責

這是一個**陪伴**工具，**不是醫療器材**，不能取代醫療照護或緊急服務。請由家人監督使用。

## 授權

[MIT](LICENSE)。歡迎自由使用、修改、散布 —— 尤其歡迎用於長者照護等公益用途。
