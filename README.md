<h1 align="center">阿茲海默陪伴者<br>Alzheimer's Voice Companion</h1>

<p align="center">
  <b>用最親的人的聲音，陪伴記憶正在遠去的長輩。</b><br>
  <i>Companionship for elders with dementia — in the voice of someone they love.</i>
</p>

> **這個專案的起點很私人。**
> 我阿公（閩南／台灣話的「爺爺」）失智快三年了，常常認不出我——把我認成叔叔，或以為我還是讀國小的孫子，問我「這次考試考得怎麼樣」。他還住院兩年了，有時候會卡痰，很辛苦。
>
> 有一天，我在樓下買了一盒**麥香奶茶**，叼在嘴裡、咬著吸管走進病房，像我小時候那樣。他愣了一下，突然笑了：「你怎麼在這裡？有沒有用功讀書？有沒有吃飽？」——他認出我了。那一刻我又開心，又難過。
>
> 原來讓他找回我的，不是我說了幾次「我是你孫子」，而是一個他熟悉的、屬於過去的線索。我住得很遠，沒辦法時時刻刻陪著他——**但我可以把「熟悉的聲音」留在他身邊。** 所以有了這個。
>
> 記憶會消失，但愛可以換一種方式留下來。
>
> _My grandfather has had Alzheimer's for almost three years. He often doesn't recognize me — until, one day, I walked in sipping a childhood milk tea, the straw still in my mouth like when I was small. He paused, then smiled: "Hey — are you studying hard? Have you eaten?" He knew me again. What brought him back wasn't me saying "I'm your grandson" — it was something familiar. I live far away and can't always be there. But I can leave a familiar voice by his side. Memory fades. Love can stay, in another form._

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
  <img alt="for dementia care" src="https://img.shields.io/badge/for-dementia%20care-ff8c69">
  <img alt="privacy: local-first" src="https://img.shields.io/badge/privacy-local--first-2b7bba">
</p>

---

長輩在平板上**按住一顆大按鈕說話**，系統就用**你設定的家人聲音**溫柔回他——永遠耐心、永遠都在、聽起來像親人。不是做一個聰明的 AI，是做一個**不會離開的陪伴**。

> _An elder presses one big button and speaks; it answers in a family member's cloned voice — patient, always there. Not a clever AI; a presence that doesn't leave._

## 📱 畫面 · Screenshots

<p align="center">
  <img src="docs/screenshots/companion-day.png" width="30%" alt="長輩畫面（日）">
  &nbsp;&nbsp;
  <img src="docs/screenshots/companion-night.png" width="30%" alt="長輩畫面（夜）">
</p>
<p align="center"><img src="docs/screenshots/setup.png" width="66%" alt="家人設定台 /setup"></p>
<p align="center"><sub>長輩畫面：一顆大按鈕、日／夜自動、閒置放老照片　｜　家人設定台 <code>/setup</code>：上傳你要的聲音<br><i>Elder's screen (day/night, idle photos) · Family console (/setup) to set the voice</i></sub></p>

## ✨ 特色 · Highlights

- 📷 **待機放長輩的老照片**（懷舊療法，安撫情緒）——用照片，不用會動的合成臉
- 🎙️ **家人的聲音是核心**：一顆大按鈕 + 家人克隆聲 + 安全護欄
- 🛡️ **失智照護護欄**：不糾正、不催促；找已故親人時溫柔安撫、不揭穿；偵測不適可**通報家人**
- 🔒 **隱私優先**：家人的聲音、照片、對話都**留在你自己的電腦**，永不上傳（只有 LLM 文字會呼叫雲端，可換成本地全離線）
- 🧓 **為長者設計**：大按鈕、暖色、日夜自動；可選「按住說話」或「自動連續對話」

## 🔒 隱私 · Privacy

**你的聲音、照片、錄音、對話記錄，都留在你自己的電腦。** 它們永遠不會上傳到我們或任何人的伺服器（repo 也被 `.gitignore` 擋掉，不含任何個人資料）。

唯一離開本機的是**大腦 LLM**：對話的**文字**會送到你設定的雲端 API（預設 NVIDIA）。想連大腦也留在本機、做到**完全離線**，把 `conf.yaml` 的 `llm.base_url` 指向本地 LLM（如 [Ollama](https://ollama.com) 的 OpenAI 相容端點）即可——聲音與資料本來就已在本機。

> _Your voices, photos, recordings and conversation history stay on your own computer — they never leave it. The only thing that leaves is the LLM call: conversation **text** goes to the cloud API you configure (NVIDIA by default). Point `llm.base_url` at a local LLM (e.g. [Ollama](https://ollama.com)) for a fully offline setup._

## 🎙️ 自帶你的聲音 · Bring your own voice

**這個 repo 不含任何人的聲音。** clone 後開 `/setup`「設定陪伴聲音」，上傳一段**清楚、安靜、10–30 秒**的家人錄音（wav / mp3 / m4a）→ 即時套用。設定前用通用聲頂著，不會壞。

> _No voice ships with the repo. Open `/setup`, upload a 10–30s clip, and it becomes the companion voice — instantly._

## 🖥️ 配置需求 · Requirements

在一台**架設的電腦**上跑（長輩只要一台有 Chrome 的平板）。**推薦一張 NVIDIA 顯卡**——語音又快又穩（作者用 RTX 4060 8GB）。**沒有顯卡也能用 CPU 版**：純 Windows、免 WSL，家人的聲音一樣克隆、完全本機，只是慢一點。系統 Windows 10 / 11。

> _Recommended: an NVIDIA GPU for fast, smooth speech. No GPU? The CPU build works too — same cloned family voice, fully local, just slower._

## 🛡️ 同意與浮水印 · Consent & watermark

聲音克隆是好工具，界線要先畫好。這個專案**預設**就守住兩件事：

- **口說同意閘門**：設定某個聲音前，本人要在錄音的**最開頭**先唸一句同意聲明（「我同意用我的聲音陪伴家人」）＋勾選確認。同意句就在**同一段錄音**裡，代表「這把聲音的本人」確實同意；系統聽到才會設定。同意紀錄只留在**你自己的機器**。
- **AI 浮水印**：每段克隆語音都打上聽不見的 [AudioSeal](https://github.com/facebookresearch/audioseal) 浮水印，可被偵測為合成聲——`python tools/detect_watermark.py <音檔>` 即可驗。即使音訊外流，也能被辨識為 AI 合成，降低被拿去詐騙的價值。
- 只使用**你有權使用**的聲音：本人，或已取得本人同意的家人。

> _Voice cloning is dual-use. By default this project requires **spoken consent** — recorded in the same clip that becomes the voice — and **watermarks every generated clip** with AudioSeal so output is detectable as AI-synthesized. Use only voices you're entitled to use._

## 🚀 安裝 · Install

**👉 第一次裝？看 [手把手安裝指南](docs/安裝指南.md)**（給非工程師，含前置準備 + FAQ）。架設需要一點技術；裝好後長輩端只有一顆大按鈕。

```powershell
wsl --install -d Ubuntu-22.04                          # 沒裝過 WSL：系統管理員跑一次、重開機
powershell -ExecutionPolicy Bypass -File install.ps1   # 一鍵裝好所有依賴（會下載數 GB）
# 打開 .env 填 NVIDIA_API_KEY（build.nvidia.com 免費）→ 雙擊「一鍵啟動.bat」
```

長輩畫面 `http://localhost:8080/`｜設定台 `/setup`。技術細節見 **[`PROJECT.md`](PROJECT.md)**。

> 🖥️ **無顯卡 CPU 版**（純 Windows，不用 WSL、不用 CUDA）——家人的聲音一樣克隆、**完全本機**，只是慢一點：
> ```powershell
> powershell -ExecutionPolicy Bypass -File install_cpu.ps1   # 裝好 → 雙擊「一鍵啟動_CPU版.bat」
> ```

> 📱 **平板 App**（一點就開、全螢幕、麥克風原生授權）：到 [**Releases**](https://github.com/ssps6210/alzheimer-companion/releases) 下載 `elder-companion.apk` 側載安裝，**首次開啟輸入你電腦的網址**即可。自行 build / 原始碼見 [`android/`](android/)。

**技術棧：** STT `faster-whisper`（本地）· LLM 任何 OpenAI 相容端點（預設 NVIDIA Nemotron）· TTS `Qwen3-TTS` 零樣本克隆。

## ☕ 支持 · Support

如果它對你或你家人有幫助：⭐ **給個 Star**，讓更多正在照顧失智長輩的家庭看到它，就是最好的支持。

<p><a href="https://buymeacoffee.com/ssps6210noa"><img src="https://img.shields.io/badge/Buy_me_a_coffee-ffdd00?style=for-the-badge&logo=buymeacoffee&logoColor=black" alt="Buy me a coffee"></a></p>

## ⚠️ 免責 · Disclaimer

**陪伴**工具，**不是醫療器材**，不能取代醫療照護或緊急服務。請由家人監督使用。

## 📄 授權 · License

[MIT](LICENSE) — 自由使用、修改、散布，尤其歡迎用於長者照護等公益用途。
