<h1 align="center">阿茲海默陪伴者<br>Alzheimer's Voice Companion</h1>

<p align="center">
  <b>用最親的人的聲音，陪伴記憶正在遠去的長輩。</b><br>
  <b>Companionship for elders with dementia — in the voice of someone they love.</b>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
  <img alt="for dementia care" src="https://img.shields.io/badge/for-dementia%20care-ff8c69">
  <img alt="privacy: local-first" src="https://img.shields.io/badge/privacy-local--first-2b7bba">
</p>

---

長輩在平板上**按住按鈕說話**，系統就用**你設定的家人聲音**溫柔回應他——
永遠耐心、永遠都在、聽起來像親人。
這個項目不是要做一個聰明的 AI，而是做一個**不會離開的陪伴**。

> An elder holds one big button and speaks; the companion answers in **a family
> member's cloned voice** — endlessly patient, always there, sounding like
> someone who loves them. Not a clever AI. A presence that doesn't leave.

失智長輩最深的痛苦之一是**孤單、混亂、與反覆的不安**。家人無法 24 小時在身邊；
市面產品要嘛冷冰冰、要嘛不是家人的聲音、要嘛把長輩的私密對話送上雲端。
這個項目選擇**開源**，因為照顧脆弱者的技術，本就該**透明、可被檢視、屬於每個家庭**。

---

## 📱 畫面 · Screenshots

<p align="center">
  <img src="docs/screenshots/companion-day.png" width="31%" alt="長輩畫面（日）">
  &nbsp;&nbsp;
  <img src="docs/screenshots/companion-night.png" width="31%" alt="長輩畫面（夜）">
</p>
<p align="center"><sub>長輩的畫面：一顆大按鈕，日／夜自動切換，閒置時放老照片。<br><i>The elder's screen — one big button, auto day/night, idle shows old photos.</i></sub></p>

<p align="center"><img src="docs/screenshots/setup.png" width="72%" alt="家人設定台 /setup"></p>
<p align="center"><sub>家人設定台 <code>/setup</code>：第一步就是「上傳你要的聲音」，設定簡潔、家人自己就能弄。<br><i>The family console — step one is uploading the voice you want. Simple enough for any family member.</i></sub></p>

---

## ✨ 為什麼這樣設計 · Design principles

| | |
|---|---|
| 📷 **待機放長輩的老照片** | 沒事時螢幕慢慢輪播**長輩自己的舊照片**——熟悉、溫柔，有實證的「懷舊療法」，讓他安心。<br>_When idle, the screen slowly cycles the elder's own old photos — familiar and calming (reminiscence therapy)._ |
| 🎙️ **家人的聲音是核心** | 一顆大按鈕 + 家人克隆聲 + 安全護欄，才是價值。<br>_The family's voice is the point — one big button, a cloned familiar voice, safety guardrails._ |
| 🔒 **隱私優先** | 長輩的對話**留在你自己的機器**，不上任何雲端資料庫。<br>_Local-first. Conversations stay on your machine; nothing is uploaded to a cloud database._ |
| 🧓 **為長者而生的介面** | 一顆手抖也好按的大按鈕；日系暖色、日夜自動切換；可選「按住說話」或「自動連續對話」。<br>_Built for elders: one huge button, warm palette, auto day/night, hold-to-talk or hands-free continuous mode._ |

## 🛡️ 安全護欄 · Safety guardrails (for dementia care)

不糾正、不催促、永遠耐心重複回答；長輩尋找已故親人時，**溫柔安撫、不揭穿真相**；
偵測到不適或求助時可**通報家人**（Telegram）。人設只放「行為傾向」，不塞私人資料庫。

> Never corrects or rushes; when the elder asks for someone who has passed away,
> it gently reassures rather than telling the painful truth; can alert family on
> distress. The persona holds *behaviour*, never a database of private facts.

## 🎙️ 自帶你的聲音 · Bring your own voice

**這個 repo 不含任何人的聲音**——家人錄音、照片、對話全被 `.gitignore` 擋掉。
所以 clone 下來後，**放進你自己想要的音色**：

1. 開 **`http://<你的電腦>:8080/setup`**（家人設定台）
2. 「🎙 設定陪伴聲音」→ 上傳一段**清楚、安靜、10–30 秒**的人聲（wav / mp3 / m4a）
3. 逐字稿可留空（自動辨識），按「設為陪伴聲音」→ **即時套用**

> Clone it, open `/setup`, upload a clean 10–30s clip of the voice you want, and
> it becomes your elder's companion voice — instantly, no restart. Until you set
> one, a neutral fallback voice keeps it working.

## 🏗️ 架構 · Architecture

```
 平板(長輩) ──HTTPS──▶ PC (Windows + NVIDIA GPU)
                         ├─ companion_web.py  :8080   前端 + /setup + 串接
                         │    ├─ STT  faster-whisper（本地）
                         │    ├─ LLM  OpenAI 相容 API（預設 NVIDIA Nemotron，可換）
                         │    ├─ 固定句快取（家人真聲，秒回）
                         │    └─ 記憶 / 家人通報
                         └─ WSL2 Ubuntu：qwen_tts_api.py :50000
                              └─ Qwen3-TTS 零樣本聲音克隆
```

- **STT** — `faster-whisper`（本地，免 API / local）
- **LLM** — 任何 OpenAI 相容端點（`conf.yaml` 可換 base_url / model）
- **TTS** — `Qwen/Qwen3-TTS-12Hz-1.7B-Base` 零樣本克隆（Apache-2.0）

## 🚀 快速開始 · Quick start

```bash
cp .env.example .env          # 填 NVIDIA_API_KEY（或改 conf.yaml 換別家 LLM）

# Windows 端（companion）
python -m venv venv
venv\Scripts\pip install -r requirements.txt

# WSL2 端（Qwen 語音克隆）：在 Ubuntu 裝好 qwen-tts（見 PROJECT.md）

# 啟動（Windows 雙擊）：一鍵啟動.bat  → 先起 companion、等辨識載完、再起 Qwen
```

長輩畫面 `http://localhost:8080/`｜家人設定台 `http://localhost:8080/setup`。
完整安裝 / 排錯見 **[`PROJECT.md`](PROJECT.md)**。

> 平板用麥克風需 **HTTPS 或 localhost**（瀏覽器規定）：同一 WiFi 可在平板 Chrome 的
> `chrome://flags` →「Insecure origins treated as secure」加入 `http://<電腦IP>:8080`；
> 或用 cloudflared / ngrok 開 https 通道。

## 🔒 隱私 · Privacy

`.gitignore` 已排除**所有聲音、照片、原始錄音、對話記憶、金鑰**——這個 repo 不含任何個人資料。
長輩的對話存在本機 `memory.json`（不入庫）；只有一次 LLM 呼叫會離開本機。
每次 push 前的自檢清單見 [`docs/上傳前隱私檢查清單.txt`](docs/上傳前隱私檢查清單.txt)。

> Every voice / photo / recording / conversation / key is gitignored — this repo
> contains **no personal data**. See the pre-push privacy checklist before you push.

## ☕ 支持這個項目 · Support

免費、開源、為長者照護而做。如果它對你或你家人有一點幫助：

- ⭐ **給這個 repo 一個 Star** —— 讓更多正在照顧失智長輩的家庭看到它，就是最好的支持。
- ☕ **請我喝杯咖啡** —— 支持持續開發與維護。

<p><a href="https://buymeacoffee.com/ssps6210noa"><img src="https://img.shields.io/badge/Buy_me_a_coffee-ffdd00?style=for-the-badge&logo=buymeacoffee&logoColor=black" alt="Buy me a coffee"></a></p>

<sub><i>If it helps your family, a ⭐ Star helps other caregivers find it — and a ☕ keeps it maintained.</i></sub>

## ⚠️ 免責 · Disclaimer

這是一個**陪伴**工具，**不是醫療器材**，不能取代醫療照護或緊急服務。請由家人監督使用。
_A companionship tool, **not a medical device**; it does not replace care or emergency services._

## 📄 授權 · License

[MIT](LICENSE) — 歡迎自由使用、修改、散布，尤其歡迎用於長者照護等公益用途。
_Free to use, modify, and share — especially for elder-care and public good._
