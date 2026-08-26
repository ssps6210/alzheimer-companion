<h1 align="center">阿茲海默陪伴者<br>Alzheimer's Voice Companion</h1>

<p align="center">
  <b>用最親的人的聲音，陪伴記憶正在遠去的長輩。</b><br>
  <i>Companionship for elders with dementia — in the voice of someone they love.</i>
</p>

> **這個專案的起點很私人。**
> 我阿公（閩南／台灣話的「爺爺」）住院兩年了，有時候還會卡痰，很辛苦；我住得很遠，每次回去看他都忍不住哭。
> 我沒辦法時時刻刻陪著他——**但我可以把「家人的聲音」留在他身邊。** 所以有了這個。
> 願它在你不在的時候，替你陪著那個正在慢慢忘記的人。
>
> _My grandfather has been in hospital for two years. I live far away, and every visit, I cry. I can't always be there — but I can leave the voice of family by his side._

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
- 🔒 **隱私優先**：對話留在**你自己的機器**，不上雲端資料庫
- 🧓 **為長者設計**：大按鈕、暖色、日夜自動；可選「按住說話」或「自動連續對話」

## 🎙️ 自帶你的聲音 · Bring your own voice

**這個 repo 不含任何人的聲音。** clone 後開 `/setup`「設定陪伴聲音」，上傳一段**清楚、安靜、10–30 秒**的家人錄音（wav / mp3 / m4a）→ 即時套用。設定前用通用聲頂著，不會壞。

> _No voice ships with the repo. Open `/setup`, upload a 10–30s clip, and it becomes the companion voice — instantly._

## 🖥️ 配置需求 · Requirements

跑這套的是**架設的電腦**（長輩只要一台有 Chrome 的平板）。**顯卡 VRAM 是關鍵。**

| | 最低（能跑） | 建議（穩） |
|---|---|---|
| **顯卡** | NVIDIA **8GB VRAM**（3060 / 4060 / 2080…） | NVIDIA **12GB+**（3060 12G / 4070 / 2080 Ti） |
| **RAM** | 8 GB | 16 GB+ |
| **硬碟** | 30 GB 可用 | 50 GB+ SSD |
| **系統** | Windows 10 (2004+) / 11 ＋ WSL2 | Windows 11 ＋ WSL2 |

> **沒有 NVIDIA 顯卡目前跑不動。** 8GB 實測可跑（作者用 RTX 4060 8GB）但偶爾會卡；12GB+ 明顯更穩。

## 🚀 安裝 · Install

**👉 第一次裝？看 [手把手安裝指南](docs/安裝指南.md)**（給非工程師，含前置準備 + FAQ）。架設需要一點技術；裝好後長輩端只有一顆大按鈕。

```powershell
wsl --install -d Ubuntu-22.04                          # 沒裝過 WSL：系統管理員跑一次、重開機
powershell -ExecutionPolicy Bypass -File install.ps1   # 一鍵裝好所有依賴（會下載數 GB）
# 打開 .env 填 NVIDIA_API_KEY（build.nvidia.com 免費）→ 雙擊「一鍵啟動.bat」
```

長輩畫面 `http://localhost:8080/`｜設定台 `/setup`。技術細節見 **[`PROJECT.md`](PROJECT.md)**。

> 📱 想把長輩畫面做成**平板 App**（一點就開、全螢幕、麥克風原生授權）？見 [`android/`](android/)。

**技術棧：** STT `faster-whisper`（本地）· LLM 任何 OpenAI 相容端點（預設 NVIDIA Nemotron）· TTS `Qwen3-TTS` 零樣本克隆。

## 🔒 隱私 · Privacy

所有聲音、照片、錄音、對話記憶、金鑰都被 `.gitignore` 擋掉——**repo 不含任何個人資料**。對話存本機 `memory.json`，只有 LLM 呼叫會離開本機。

> _Every voice / photo / recording / conversation / key is gitignored — no personal data in this repo._

## ☕ 支持 · Support

如果它對你或你家人有幫助：⭐ **給個 Star**，讓更多正在照顧失智長輩的家庭看到它，就是最好的支持。

<p><a href="https://buymeacoffee.com/ssps6210noa"><img src="https://img.shields.io/badge/Buy_me_a_coffee-ffdd00?style=for-the-badge&logo=buymeacoffee&logoColor=black" alt="Buy me a coffee"></a></p>

## ⚠️ 免責 · Disclaimer

**陪伴**工具，**不是醫療器材**，不能取代醫療照護或緊急服務。請由家人監督使用。

## 📄 授權 · License

[MIT](LICENSE) — 自由使用、修改、散布，尤其歡迎用於長者照護等公益用途。
