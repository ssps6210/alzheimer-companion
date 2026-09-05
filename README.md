<p align="center">
  <b>繁體中文</b> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.en.md">English</a>
</p>

<h1 align="center">阿茲海默陪伴者<br>Alzheimer's Voice Companion</h1>

<p align="center">
  <b>用最親的人的聲音，陪伴記憶正在遠去的長輩。</b><br>
  <i>Companionship for elders with dementia — in the voice of someone they love.</i>
</p>

<p align="center">
  <a href="https://github.com/ssps6210/alzheimer-companion/releases"><img alt="下載 APK" src="https://img.shields.io/badge/📱_平板_App-下載_APK-2ea44f?style=for-the-badge"></a>
  &nbsp;
  <a href="#security"><img alt="資料不離開你的電腦" src="https://img.shields.io/badge/🔒_資料-不離開你的電腦-2b7bba?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
  <img alt="for dementia care" src="https://img.shields.io/badge/for-dementia%20care-ff8c69">
  <a href="../../actions/workflows/privacy.yml"><img alt="privacy scan" src="https://github.com/ssps6210/alzheimer-companion/actions/workflows/privacy.yml/badge.svg"></a>
</p>

> **這個專案的起點很私人。**
>
> 我阿公（閩南／台灣話的「爺爺」）有嚴重的阿茲海默，快三年了，常常認錯人。把我看成我爸、我叔叔，有時候是叔公，有一次是姨丈。我說過很多次「我是你孫子」，說一百次也沒用。
>
> 有一天，我在樓下買了一盒**麥香奶茶**，把吸管叼在嘴裡、一邊喝一邊走進病房，像我小時候那樣。他愣了一下，然後笑了：「你怎麼在這裡？有沒有用功讀書？有沒有吃飽？」他認出我了。
>
> 原來他要的不是解釋。是那個他還認得的畫面：一個孫子，叼著吸管喝奶茶。
>
> 我住得很遠，沒辦法天天陪他。所以我想：如果一盒奶茶可以是熟悉的線索，那**熟悉的聲音**是不是也可以？
>
> 他可能不記得我是誰。但他記得那個叼著奶茶的孩子。
>
> _My grandfather has had Alzheimer's for almost three years. He mistakes me for my dad, my uncle, once for my great-uncle. Saying "I'm your grandson" never worked — not once in a hundred times. Then one day I walked into his room sipping a carton of the milk tea I drank as a kid, straw still in my mouth. He paused, then smiled: "Are you studying hard? Have you eaten?" He knew me. What he needed wasn't an explanation. It was something he still recognised. I live far away and can't be there every day — but I can leave a familiar voice by his side._

---

長輩在平板上**按一顆大按鈕說話**，系統就用**你設定的家人聲音**回他。他問一百次，它就答一百次，不會說「你剛剛問過了」。

> _An elder presses one big button and speaks; it answers in a family member's voice. Ask the same question a hundred times and it answers a hundred times, never "you just asked me that."_

## 🚀 三步驟開始 · Quick start

**長輩端只要一台平板。** 架設在你自己的電腦上，不需要註冊帳號、不需要伺服器。

| | 做什麼 | 花多久 |
|---|---|---|
| **1** | 電腦跑一行安裝：`powershell -ExecutionPolicy Bypass -File install.ps1` | 依網速，會下載數 GB |
| **2** | 到 [**Releases**](https://github.com/ssps6210/alzheimer-companion/releases) 下載 `elder-companion.apk` 裝進平板 | 1 分鐘 |
| **3** | 打開 App，掃一下電腦畫面上的 QR（或按「自動尋找」） | 10 秒 |

沒有 NVIDIA 顯卡就改跑 `install_cpu.ps1`（純 Windows、免 WSL，家人的聲音一樣克隆，只是慢一點）。

**不需要申請任何 API 金鑰。** 預設用跑在你自己電腦上的模型（Ollama），對話文字一個字都不出門。想換成更聰明的雲端模型也可以，見下方〈語言與大腦〉。

**第一次裝？** 看 [手把手安裝指南](docs/安裝指南.md)，寫給非工程師，含前置準備與常見問題。

## 📱 畫面 · Screenshots

<p align="center">
  <img src="docs/screenshots/companion-day.png" width="30%" alt="長輩畫面（日）">
  &nbsp;&nbsp;
  <img src="docs/screenshots/companion-night.png" width="30%" alt="長輩畫面（夜）">
</p>
<p align="center"><img src="docs/screenshots/setup.png" width="66%" alt="家人設定台 /setup"></p>
<p align="center"><sub>長輩畫面：一顆大按鈕、日／夜自動、閒置放老照片　｜　家人設定台 <code>/setup</code>：上傳你要的聲音<br><i>Elder's screen (day/night, idle photos) · Family console (/setup) to set the voice</i></sub></p>

<a id="security"></a>

## 🔒 你家人的聲音，會怎麼被保管 · Security

**你錄的聲音、長輩的照片、他們說過的話，都只留在你自己家裡的那台電腦。**

我們沒有伺服器，也沒有帳號可以註冊。就算我們想拿，也拿不到。

三個最常被問到的問題：

**「我爸的聲音會被拿去詐騙嗎？」**
聲音檔案從頭到尾沒有離開過你的電腦。而且系統要設定某個人的聲音之前，會要求**本人親口說一句同意**；聽不到那句話就不會設定。另外，它講出來的每一句話都藏了一個聽不見的記號，可以驗出「這是 AI 合成的，不是本人說的」。

**「會有人偷聽我們的對話嗎？」**
對話記錄存在你的電腦裡，不會上傳。而且**預設連「文字」都不出門**——回話的 AI 就跑在你自己那台電腦上。

如果你選擇改用雲端的 AI（回話更聰明一點），那麼只有**對話的文字**（不是聲音）會送出去，就像你在 Google 打字搜尋那樣。要不要這樣換，決定權在你。

**「我不懂電腦，會不會設定錯就外洩了？」**
不會有那個機會——把個人資料傳出去的功能，這個專案根本沒有寫。要外洩得有人故意去改程式。

<details>
<summary><b>技術細節（給工程師）</b></summary>

- 聲音、照片、`memory.json`、`patterns.json`、同意紀錄，全部只在本機檔案系統，沒有任何 outbound 傳輸路徑。
- 唯一的對外呼叫是 `POST {llm.base_url}/chat/completions`，帶對話文字，用使用者自己的 API 金鑰。把 `conf.yaml` 的 `llm.base_url` 指向 [Ollama](https://ollama.com) 等本地 OpenAI 相容端點即可完全離線。
- repo 不含任何個人資料，且每次 push 由 [`tools/privacy_scan.py`](tools/privacy_scan.py) 在 CI 掃描已追蹤檔案，命中音檔／記憶檔／金鑰樣式就讓 build 失敗。防的是規則寫錯與 `git add -f` 這兩種實際會發生的狀況。
- **家人管理台 `/setup` 有密碼**：它能讀長輩的完整對話記錄，所以一定有鎖。首次啟動會自動產生一組密碼寫進 `.env`（`SETUP_PASSWORD`）並印在啟動視窗，帳號是 `family`。長輩畫面 `/` 刻意不設密碼——長輩不可能輸入密碼，那個畫面也沒有私密內容。
- 同意閘門：同意句必須出現在**成為音色的那一段錄音**裡，說話者即同意者。可用 `CONSENT_REQUIRED=0` 關閉。
- 浮水印：[AudioSeal](https://github.com/facebookresearch/audioseal)，跑在 CPU 不佔顯存，`python tools/detect_watermark.py <音檔>` 驗證。可用 `WATERMARK=0` 關閉。
  這是**事後可驗證性**，不是防護——重新編碼有機會把標記洗掉。它的用處是「證明某段音訊是合成的」，不是「阻止有心人」。

</details>

> _Your recordings, photos and everything your elder says stay on your own computer. There is no server to sign up for. The only thing that goes online is the conversation **text** sent to an AI service using your own API key — like typing into a search box — and you can point it at a local model to stay fully offline. Cloning a voice requires the owner's spoken consent in the same clip, and every generated clip carries an inaudible watermark identifying it as AI-synthesised._

## ✨ 特色 · Highlights

- 🎙️ **用家人的聲音**：上傳一段 10–30 秒的錄音就換好音色，repo 不含任何人的聲音
- 🛡️ **失智照護護欄**：不糾正、不催促；找已故親人時溫柔安撫，不揭穿；說到跌倒或胸口痛會**通報家人**
- 📷 **待機放長輩的老照片**（懷舊療法）——用照片，不用會動的合成臉
- 📈 **家人看得到近況**：最近常說什麼、哪個時段最需要陪伴（是陪伴觀察，不是醫療診斷）
- 🧓 **為長者設計**：大按鈕、暖色、日夜自動；可選「按住說話」或「自動連續對話」

護欄不只是寫在提示詞裡：`tests/test_safety.py` 用九個高風險情境（問已故親人、重複發問、要求獨自外出…）實測回覆有沒有踩線，改人設必跑。

## 🧠 大腦 · The AI

**預設跑在你自己的電腦上，不需要任何金鑰。** 裝 [Ollama](https://ollama.com)（免費）之後
`ollama pull qwen2.5:3b`，這樣連對話的文字都不會離開這台機器。

| | 本機模型（預設） | 雲端模型 |
|---|---|---|
| 金鑰 | 不用 | 要自己申請（免費） |
| 對話文字 | **完全不出門** | 送到你選的服務商 |
| 回話品質 | 夠用，句子簡單 | 較細膩 |
| 速度 | 看你的電腦 | 通常較快 |

兩個都不想裝也沒關係：本機模型沒在跑、又填了雲端金鑰時，它會**自動改用雲端並在啟動視窗說明**。
想「只用本機、絕不連雲端」，把 `conf.yaml` 的 `fallback_api_key_env` 留空即可。

> ⚠️ 顯卡只有 8GB 的話要留意：語音辨識和聲音克隆已經吃掉大部分顯存，
> 本機大腦建議用小模型（3B）或讓 Ollama 跑 CPU，不然三邊搶顯存會當掉。

## 🌏 語言 · Language

介面、語音辨識與合成、照護護欄、人設，可整套切換：在 `conf.yaml` 設
`language: zh-TW`（預設）／ `zh-CN` ／ `en`。語言包在 [`lang/`](lang/)，
想加語言就複製一份改；沒翻到的項目會留著中文，不會變空白。

> 換語言不只是換介面文字——緊急詞、禁語這些**護欄關鍵詞也會跟著換**。
> 中文的關鍵詞在英文部署裡是無效的，護欄會靜默失效，所以它們寫在語言包裡。

## 🖥️ 配置需求 · Requirements

在一台**架設的電腦**上跑，長輩只要一台有 Chrome 的平板。**推薦一張 NVIDIA 顯卡**，語音又快又穩（作者用 RTX 4060 8GB）。沒有顯卡就用 CPU 版，一樣是家人的聲音、一樣完全本機，速度慢一些。系統 Windows 10 / 11。

技術棧：STT `faster-whisper`（本地）· LLM 任何 OpenAI 相容端點 · TTS `Qwen3-TTS` 零樣本克隆。細節見 [`PROJECT.md`](PROJECT.md)，想一起做見 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## ☕ 支持 · Support

如果它對你或你家人有幫助：⭐ **給個 Star**，讓更多正在照顧失智長輩的家庭看到它。

<p><a href="https://buymeacoffee.com/ssps6210noa"><img src="https://img.shields.io/badge/Buy_me_a_coffee-ffdd00?style=for-the-badge&logo=buymeacoffee&logoColor=black" alt="Buy me a coffee"></a></p>

## ⚠️ 免責 · Disclaimer

**這是陪伴工具，不是醫療器材，也不是緊急救援系統。**

「說到不適就通知家人」是盡力而為的提醒，斷網、關機、沒說話、聽錯都會失效。
**緊急狀況請打 119**，不要因為裝了這套就減少原本的照護安排。

克隆聲音前必須取得本人同意；嚴禁用於詐欺、冒充或任何違法用途。

完整條款見 **[免責聲明與使用規範](DISCLAIMER.md)**——安裝或使用即表示你已閱讀並同意。

## 📄 授權 · License

[MIT](LICENSE) — 自由使用、修改、散布，尤其歡迎用於長者照護等公益用途。
