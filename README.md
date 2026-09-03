<h1 align="center">阿茲海默陪伴者<br>Alzheimer's Voice Companion</h1>

<p align="center">
  <b>用最親的人的聲音，陪伴記憶正在遠去的長輩。</b><br>
  <i>Companionship for elders with dementia — in the voice of someone they love.</i>
</p>

<p align="center">
  <a href="https://github.com/ssps6210/alzheimer-companion/releases"><img alt="下載 APK" src="https://img.shields.io/badge/📱_平板_App-下載_APK-2ea44f?style=for-the-badge"></a>
  &nbsp;
  <a href="#-資訊安全--security"><img alt="資料不離開你的電腦" src="https://img.shields.io/badge/🔒_資料-不離開你的電腦-2b7bba?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
  <img alt="for dementia care" src="https://img.shields.io/badge/for-dementia%20care-ff8c69">
  <a href="../../actions/workflows/privacy.yml"><img alt="privacy scan" src="https://github.com/ssps6210/alzheimer-companion/actions/workflows/privacy.yml/badge.svg"></a>
</p>

> **這個專案的起點很私人。**
>
> 我阿公（閩南／台灣話的「爺爺」）失智快三年了，常常認錯人。把我看成我爸、我叔叔，有時候是叔公，有一次是姨丈。我說過很多次「我是你孫子」，說一百次也沒用。
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

**第一次裝？** 看 [手把手安裝指南](docs/安裝指南.md)，寫給非工程師，含前置準備與常見問題。

## 📱 畫面 · Screenshots

<p align="center">
  <img src="docs/screenshots/companion-day.png" width="30%" alt="長輩畫面（日）">
  &nbsp;&nbsp;
  <img src="docs/screenshots/companion-night.png" width="30%" alt="長輩畫面（夜）">
</p>
<p align="center"><img src="docs/screenshots/setup.png" width="66%" alt="家人設定台 /setup"></p>
<p align="center"><sub>長輩畫面：一顆大按鈕、日／夜自動、閒置放老照片　｜　家人設定台 <code>/setup</code>：上傳你要的聲音<br><i>Elder's screen (day/night, idle photos) · Family console (/setup) to set the voice</i></sub></p>

## 🔒 資訊安全 · Security

失智長輩的聲音和對話，是最不該外流的那種資料。這個專案的處理方式：

**留在你自己的電腦，一步都不出去**
家人的聲音、長輩的老照片、每一句對話記錄、上傳的錄音——全部只存在架設的那台電腦上。沒有我們的伺服器，也沒有任何第三方會拿到。

**唯一離開本機的，是對話的文字**
它會送到你自己設定的 LLM API（預設 NVIDIA，用你自己申請的免費金鑰）。想連這一步都留在本機，把 `conf.yaml` 的 `llm.base_url` 指向 [Ollama](https://ollama.com) 之類的本地模型，就是**完全離線**。

**repo 裡沒有任何個人資料，而且是自動把關的**
`.gitignore` 擋掉聲音／照片／記憶／金鑰，另外每次 push 都會跑 [`tools/privacy_scan.py`](tools/privacy_scan.py) 掃一次已追蹤的檔案，發現音檔或金鑰樣式就讓 CI 紅燈。防的是「規則寫錯」和「手滑 `git add -f`」這兩種真的會發生的事。

**克隆聲音要本人同意，而且生成的語音帶浮水印**
設定音色前，本人要在**同一段錄音的開頭**唸一句「我同意用我的聲音陪伴家人」，系統聽到才會設定；同意紀錄只留在你的機器。每段生成的語音都打上聽不見的 [AudioSeal](https://github.com/facebookresearch/audioseal) 浮水印，`python tools/detect_watermark.py <音檔>` 可以驗出它是合成的。即使音訊外流，也能被辨識為 AI 合成。

> _Voices, photos and conversations never leave the machine you run it on. Only the LLM call goes out — conversation text to an API key you own — and pointing `llm.base_url` at a local model makes it fully offline. The repo ships no personal data, enforced on every push by a privacy scan in CI. Cloning a voice requires spoken consent recorded in the same clip, and every generated clip is watermarked with AudioSeal._

## ✨ 特色 · Highlights

- 🎙️ **用家人的聲音**：上傳一段 10–30 秒的錄音就換好音色，repo 不含任何人的聲音
- 🛡️ **失智照護護欄**：不糾正、不催促；找已故親人時溫柔安撫，不揭穿；說到跌倒或胸口痛會**通報家人**
- 📷 **待機放長輩的老照片**（懷舊療法）——用照片，不用會動的合成臉
- 📈 **家人看得到近況**：最近常說什麼、哪個時段最需要陪伴（是陪伴觀察，不是醫療診斷）
- 🧓 **為長者設計**：大按鈕、暖色、日夜自動；可選「按住說話」或「自動連續對話」

護欄不只是寫在提示詞裡：`tests/test_safety.py` 用九個高風險情境（問已故親人、重複發問、要求獨自外出…）實測回覆有沒有踩線，改人設必跑。

## 🖥️ 配置需求 · Requirements

在一台**架設的電腦**上跑，長輩只要一台有 Chrome 的平板。**推薦一張 NVIDIA 顯卡**，語音又快又穩（作者用 RTX 4060 8GB）。沒有顯卡就用 CPU 版，一樣是家人的聲音、一樣完全本機，速度慢一些。系統 Windows 10 / 11。

技術棧：STT `faster-whisper`（本地）· LLM 任何 OpenAI 相容端點 · TTS `Qwen3-TTS` 零樣本克隆。細節見 [`PROJECT.md`](PROJECT.md)，想一起做見 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## ☕ 支持 · Support

如果它對你或你家人有幫助：⭐ **給個 Star**，讓更多正在照顧失智長輩的家庭看到它。

<p><a href="https://buymeacoffee.com/ssps6210noa"><img src="https://img.shields.io/badge/Buy_me_a_coffee-ffdd00?style=for-the-badge&logo=buymeacoffee&logoColor=black" alt="Buy me a coffee"></a></p>

## ⚠️ 免責 · Disclaimer

**陪伴**工具，**不是醫療器材**，不能取代醫療照護或緊急服務。請由家人監督使用。

## 📄 授權 · License

[MIT](LICENSE) — 自由使用、修改、散布，尤其歡迎用於長者照護等公益用途。
