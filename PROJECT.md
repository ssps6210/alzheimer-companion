# 爺爺語音陪伴系統 — 專案總文檔（Single Source of Truth）

> 給患有阿茲海默症的爺爺用的語音 AI 陪伴系統。這份是「先讀這個」的總覽 + Runbook，
> 目的：**任何一次接手都不用重新推導**。改了架構請同步更新這裡。
> 最後更新：2026-07-02

---

## 0. 一句話
爺爺按住平板按鈕說話 → 用**家人（爸爸）克隆的聲音**溫暖回他。極簡、離線優先、安全護欄、將**開源**。

## 1. 設計哲學（不可違背的鐵則）
- **閒置畫面用爺爺本人舊照片慢速輪播（懷舊療法）** —— 熟悉的畫面讓失智長者安心。用照片，不做會動的合成臉（設計取向，別加 avatar）。
- **前端越乾淨越好**：一個大「按住說話」按鈕，如此而已。需夜間模式（暗、暖色）。
- **人設只放「行為傾向」，不塞事實資料庫**。把家人細節硬塞進 prompt 會讓 AI 變笨、變複讀機；家人知識走內容通道（固定句/記憶），不進系統提示。看護病院不是私人空間 → persona 不主動講爺爺私事。
- **自稱一律「我」**（不自稱孫子或任何特定身分）。**台灣國語 / 台灣用語**（說「國語」不說「普通話」）。
- 護城河 = **家人克隆聲 + 安全護欄（固定句 / 家人通報）**，不能換成黑盒。端側小模型只是反射層。

## 2. 系統架構
```
 爺爺的平板(台灣, Android/Chrome)
        │ HTTPS（按住說話，錄音上傳）
        ▼
 ┌─────────────────────────────────────────────┐
 │  你的 PC (Windows 11 + RTX 4060 Laptop 8GB)   │
 │                                               │
 │  companion_web.py  ── FastAPI :8080 ──────┐   │
 │   ├─ STT: faster-whisper (medium, CUDA)   │   │
 │   ├─ 固定句快取(爸爸真聲, 命中就秒回)         │   │
 │   ├─ LLM: NVIDIA Nemotron(雲端, 見 §5)     │   │
 │   ├─ 記憶 memory.json / 家人通報 Telegram   │   │
 │   └─ /setup 家人管理台                      │   │
 │                     │ POST :50000/tts       │   │
 │        WSL2 Ubuntu-22.04 (root, /root/rvc_env)│
 │        qwen_tts_api.py ── :50000 ─────────────┤
 │         └─ Qwen3-TTS 1.7B 克隆爸爸的聲音       │
 └───────────────────────────────────────────────┘
        ▲ 對外：ngrok 通道（見 §9）
```
**同一張 4060 三邊搶 8GB VRAM**（Whisper + Qwen + 系統），這是很多當機的根因 → 需看門狗。

## 3. 三個要跑的東西（Runbook）

### 3.0 ⭐ 一鍵開關（日常用這個）
- **`一鍵啟動.bat`**（雙擊）→ 起 companion + 爸爸的聲音(Qwen)，就緒後自動開兩個分頁：前端 `http://localhost:8080/`、家人台 `http://localhost:8080/setup`。關掉黑視窗服務仍在背景跑。
- **`一鍵停止.bat`**（雙擊）→ 停 companion + Qwen + ngrok。
- 實作：`scripts\launch.ps1` / `stop.ps1`（UTF-8 BOM，PS5.1 才不亂碼）+ `scripts\_stop_qwen.sh`（pkill 放獨立檔避免自殺）。下面 3.1-3.3 是手動/排錯用。
- ⚠️ **VRAM 錯開（2026-07-10）**：launch.ps1 改成**先等 whisper 載完、再起 Qwen** —— 兩個模型同時載會搶爆 8GB 撞掛一個（父親聲音一直掉的根因）。**手動重啟 companion 也要照這順序**（companion→等 whisper→Qwen），否則 whisper 重載會把 Qwen 擠死。
- ⚠️ **判存活看行程不看 port**：launch/stop/watchdog 已改用行程命令列比對 `companion_web.py`（不只看 :8080）—— 否則 whisper 載入中的 30-60 秒窗口會被誤判成「沒在跑」→ 重複雙擊起兩份撞爆 VRAM。

### 3.1 大腦 + 網頁：companion（Windows）
```powershell
venv\Scripts\python.exe companion_web.py
```
- 監聽 `:8080`，自動讀 `.env`。
- 健康檢查：`Invoke-RestMethod http://localhost:8080/health`
  → 回 `whisper.loaded / mimo.ok(大腦) / cosyvoice.ok(TTS) / phrases`。
- log：`server.out.log` / `server.err.log`。

### 3.2 爸爸的聲音：Qwen TTS（WSL2）
```bash
bash scripts/_start_qwen.sh   # 用 /root/rvc_env 跑 qwen_tts_api.py，:50000
```
- 不起則開放對話自動退回 edge-tts（`zh-TW-YunJheNeural`，非爸爸聲）。
- 健康：`curl http://localhost:50000/health` → `{status, ref_loaded, model}`。
- ⚠️ **WSL 啟動鐵律**（踩過的坑）：
  - 常駐服務要用 `Start-Process wsl ...` 保持 wsl.exe 存活；純 `wsl -c "cmd &"` 回傳即被回收。
  - PowerShell 內聯會把 `>` `|` 中文、`$n:` 搞爛 → **一律寫成 `scripts/_*.sh` 再 `wsl bash`**。
  - `pkill -f qwen_tts_api.py` 會殺到自己那條 bash → pkill 放**獨立**腳本檔。

### 3.3 對外連線：ngrok（見 §9，目前未收尾）

---

## 4. 設定檔 `conf.yaml`（改這裡就能換模組，不動程式）
| 區段 | 關鍵 |
|---|---|
| `asr` | faster-whisper `medium` / `cuda` / `float16` / `zh` |
| `llm` | 見 §5。key 只讀環境變數名，值不入庫 |
| `tts` | `cosyvoice_url: http://localhost:50000/tts`（介面沿用舊名）、`timeout 40`、`edge_voice` fallback |
| `memory` | `max_history 10`、`persist true`(memory.json)、`summary_trigger 24` |
| `notify` | Telegram token/chat 讀環境變數、`daily_summary_hour 20`（-1=關） |
| `active_character` | `grandson`；多人陪伴：`characters` 下加人 + 錄聲音，改這個切換 |

程式常數對應（`companion_web.py`）：`MIMO_*`=LLM、`COSY_*`=TTS、`CLIENT_TIMEOUT_MS=(LLM_TIMEOUT+COSY_TIMEOUT+15)*1000`（現 =85s，平板前端等待上限）。

---

## 5. 大腦 LLM = NVIDIA Nemotron 3 Super 120B ⭐（2026-07 換，MiMo 掛了）
| | |
|---|---|
| model | `nvidia/nemotron-3-super-120b-a12b`（120B MoE, 12B active）|
| 端點 | `https://integrate.api.nvidia.com/v1`（OpenAI 相容 `/chat/completions`）|
| key | 環境變數 `NVIDIA_API_KEY`（`nvapi-…`；到 build.nvidia.com 免費申請，填進 `.env`）|
| conf | `api_key_env: NVIDIA_API_KEY`、`disable_thinking: true`、`max_tokens 80`、`timeout 30` |
| 速度 | health ~0.6s；一般回覆 ~1s（比 MiMo 的 0.8–21s 快又穩）|

**⭐關鍵坑（2026-07-10 實測修正，推翻先前判斷）：**
- Nemotron 是推理模型，但 `reasoning_content` 分離**不穩定** —— 思考常直接吐進 `content`；`max_tokens=80` 又放不下 200–1000 字思考 → **被截斷的思考洩漏成 content**，爺爺會聽到中/英文內心獨白、甚至自稱 granddaughter（實測 bug）。
- **正解＝關思考**：`conf.yaml` 設 `disable_thinking: true` → 程式送 `chat_template_kwargs:{"enable_thinking":false}`。**Nemotron 也吃這個**（跟 MiMo 一樣，先前「NVIDIA 不吃」判斷是錯的）。實測 reasoning 歸零、`content` 全乾淨、又快。
- ⚠️「detailed thinking off」系統提示**無效**（reasoning 仍 >0，別用）。
- companion `_sanitize_reply()`：回覆再去 emoji / markdown，免被 TTS 念出（模型偶爾加 🌞）。

（舊·退役）MiMo V2.5：`token-plan-ams.xiaomimimo.com/v1` / `mimo-v2.5` / `MIMO_API_KEY`；2026-05 從本地 Ollama 換來、2026-07 端點掛掉。其坑：關思考只有 `chat_template_kwargs:{enable_thinking:false}` 有效。⚠️ 此 key 曾在對話外洩，**開源前務必輪替 / 刪除**。

---

## 6. 聲音 TTS = Qwen3-TTS 1.7B ⭐（2026-07 最終定案）
- model `Qwen/Qwen3-TTS-12Hz-1.7B-Base`，零樣本克隆，Apache-2.0。走過 CosyVoice3（長句飄/念instruct，棄）→ seed-vc（穩但不夠像，棄）→ Qwen（最像、免訓練）。
- 呼叫：`model.generate_voice_clone(text, language="Chinese", ref_audio=father_reference.wav, ref_text=<father_reference.txt 逐字稿>)`。
- **甜蜜區 10–16 秒**：太短(<8s)音色沒鎖定不像、>18s 後半會飄。`qwen_tts_api.py` 的 `_split` 把回覆貪婪合併成 ~58 字（≈16s）的塊逐塊合成。
- **flash-attn 2.6.3** 已裝（prebuilt wheel `cu123torch2.3 abiFALSE cp310`，免編譯）→ ~1.4× 提速 + 省顯存；服務 attn 自動退回 `sdpa`/`eager`（開源友善）。
- **速度**：暖機後 ~11–12s/塊（RTF~0.8，1.7B 在 4060 的地板，**已決定維持 1.7B**）。所以常見話走**固定句秒回**，只有開放對話才吃這 ~11s。
- 參考音：`father_reference.wav`（30s，爸爸多段語句去噪+響度正規化接成）+ `father_reference.txt`（逐字稿）。
- 依賴都在 WSL `/root/rvc_env`：`qwen-tts` / `flash-attn` / `soundfile` 等。
- **AI 浮水印（防冒用，預設開）**：`qwen_tts_api.py` 合成後過 [AudioSeal](https://github.com/facebookresearch/audioseal)（`audioseal_wm_16bits`，放 **CPU** 不佔顯存），輸出 16k 已標記 wav。`WATERMARK=0` 可關；audioseal 沒裝 → 大聲提醒並**原樣輸出**（陪伴不會壞）。`/health` 回 `watermark` 布林、Setup 台顯示徽章。驗證：`python tools/detect_watermark.py <音檔>`。

## 6.5 聲音同意閘門（防冒用，2026-08）
- `/setup/set-voice` 設定音色前：錄音本人須在**錄音最開頭唸同意聲明**「我同意用我的聲音陪伴家人」＋前端勾選確認。companion 用自己的 whisper 轉稿後，比對關鍵詞 `("同意","陪伴")` 皆present 才放行；否則**刪掉剛寫的 active_reference** 並回 400 引導。
- 同意句在**同一段錄音**裡 → 說話者＝同意者，把同意綁死在該聲音。證明存 `voices/active_reference.consent.json`（phrase / transcript / ref 的 sha256 / ts；`voices/` 已 gitignore）。
- `CONSENT_REQUIRED=0` 可關（進階／本機；本機父親音走 `QWEN_REF` 不經此路，不受影響）。常數在 `companion_web.py`（`CONSENT_PHRASE` / `CONSENT_KEYS`）。

## 6.6 無顯卡 CPU 版（XTTS-CPU，2026-08）
- 目的：降門檻——沒 NVIDIA 顯卡的家庭也能用，且**保住家人聲**（一樣克隆）、**完全本機**（連 WSL 都不用）。取捨：慢（CPU 一句話數秒~十幾秒，固定句秒回墊著）。
- `xtts_cpu_api.py`：Coqui **XTTS-v2**（`coqui-tts` 分支，CPML **非商業**授權，家庭用 OK；`COQUI_TOS_AGREED=1` 免互動下載）跑 CPU，講**與 `qwen_tts_api.py` 同一套 HTTP 介面**（`/tts`,`/health`,`/reload-ref`），**同 port 50000 → companion 免改**。是 Qwen 的 drop-in 替代（跑其一即可）。
- 音色同一套：`voices/active_reference.wav`（`/setup/set-voice` 同一道同意閘門）。浮水印共用 `wm.py`（AudioSeal，CPU）——Qwen 與 XTTS 都經同一模組（`wm.load/ok/apply`）。
- 安裝/啟動（純 Windows，不碰 WSL/CUDA）：`install_cpu.ps1`（venv + `requirements-cpu.txt`：faster-whisper + `coqui-tts` + torch(CPU) + audioseal）→ 複製 `conf.cpu.example.yaml`(whisper `device:cpu`/`compute_type:int8`/`model:small`、`cosyvoice_timeout:90`)→ `scripts/launch_cpu.ps1`（起 companion + `xtts_cpu_api.py` 兩支 Windows 行程）／`一鍵啟動_CPU版.bat`。`stop.ps1` 已一併收 `xtts_cpu_api.py`。
- 隱私定位：聲音/照片/記錄全本機；**唯一離開本機的是 LLM 文字**（雲端 Nemotron）。要 100% 離線可把 `llm.base_url` 指向本地 LLM（Ollama 等 OpenAI 相容端點）——見 README「隱私」。

---

## 7. 語音辨識 STT = faster-whisper（本地）
- `medium` / CUDA / float16 / 中文。首次自動下載模型。
- **台語 STT（待接，未解）**：爺爺母語台語、常混台語+國語。
  - NUTN-KWS/Whisper-Taiwanese-v0.5 → **會把國語轉爛**（幻覺/亂碼），不能用。
  - formoai/brecioso-e-model-taigi-20250901（台+國）→ **gated，等作者審核**；本機**沒設 HF token**。
  - 現況：先用 faster-whisper 撐（國語 OK、台語詞會漏）。

## 8. 固定句 / 記憶 / 通報
- **固定句快取**：`phrases/*.wav` = 爸爸真人錄音 17 條，命中（子字串比對 + 否定詞 不/沒/別/未/甭 防呆）就**繞過 LLM+TTS 秒回**。像導航語音包。
- **記憶**：近期對話 + 滾動摘要存 `memory.json`（重啟不忘，已 gitignore）。超過 24 則把舊的濃縮進長期摘要。
- **家人通報 Telegram**：`TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`。出現不適/求助句（帶 `alert:true`）即推播；每天 20:00 寄當日對話摘要。
- **/setup 家人管理台**：系統狀態、**爺爺說話方式(預設 hold/auto)**、試聽現在的聲音、上傳家人聲音、固定句(播放+上傳)、爺爺近況(對話記錄)。⚠️ **目前無密碼保護**（TODO）。

## 8.5 爺爺前端（2026-07 日系改造 + 說話模式）
`companion_web.py` 內嵌 HTML（`/`）已改成**日系優雅簡約溫暖**（原研哉／無印：和紙暖白 day + 墨色暖夜 night，**18:00–06:00 自動切換**；柿色強調；明體）。DOM 契約不變（`#clock #date #wave/.bar #status #user-box #reply-box #btn`），另加 `#greet`（早午晚安）、`#modeSw`（模式切換）、`#idle`（懷舊層）。設計原型：`design/爺爺前端_日系版.html`（可雙擊，右上有預覽鈕）。
- **兩種說話模式**（給腿腳/手不方便的長輩）：
  - `hold` 按住說話（原行為：按著錄、放開送）。
  - `auto` 自動連續對話：點一下開始 → **VAD 靜音偵測**（`SILENCE_MS=1400` 停頓自動送出、`NOSPEECH_MS=8000` 無語自動結束）→ 回覆播完**自動再聽** → 再點一下結束。VAD 重用 onaudioprocess 已算的 RMS（`VAD_ON=0.02`）。
  - 預設由**家人在 /setup 設**（存 `ui_state.json` 的 `talk_mode`，開機注入 HTML 的 `__DEFAULT_MODE__`）；爺爺畫面 `#modeSw` 可本機切換（存 localStorage，覆蓋預設）。端點 `GET/POST /setup/talk-mode`。
- **懷舊老照片**：閒置 `IDLE_MS=75s` → 全螢幕老照片慢速輪播 + Ken Burns + 暈影，碰一下回來。照片放 `photos/`（jpg/png/webp），端點 `GET /photos`（列表）+ `/photos/{f}`；**沒放照片就顯示暖色占位**（目前狀態）。

## 9. 對外連線 ngrok（本次進度，**未收尾**）
狀態（2026-07-02）：
- ✅ CLI 已裝（winget，路徑 `...\WinGet\Packages\Ngrok.Ngrok...\ngrok.exe`），已 `ngrok update` 升到 **3.39.9**（帳號要求 ≥3.20.0）。
- ✅ authtoken 已接：`ngrok config add-authtoken …` → 存於 `%LOCALAPPDATA%\ngrok\ngrok.yml`。
- ✅ 帳號**免費固定域名 = `coexist-sherry-parish.ngrok-free.dev`**（重開不變，可當家人固定網址）。
- ❌ **卡住**：該域名目前被**另一個 ngrok agent 佔用**（`ERR_NGROK_334 already online`；直接打回 404，不是本專案服務，也不在本機 Windows/排程 → 疑似在 WSL / 別台的通道）。要嘛找出來停掉、要嘛 `--pooling-enabled`（不建議，會分流）。
- ⚠️ **免費版坑**：開網址會先跳英文警告頁「You are about to visit…」要按 Visit Site → **對失智爺爺很糟**。正式給爺爺要嘛 ngrok 付費($10/月，去警告頁)、要嘛改 **Tailscale Funnel / cloudflared 具名通道**（免費、無警告頁）。
- 開通道指令（域名釋放後）：
  ```powershell
  <ngrok.exe> http 8080 --url=coexist-sherry-parish.ngrok-free.dev --log=stdout
  ```
  本地狀態 API：`http://127.0.0.1:4040/api/tunnels`。

（測試期舊法：cloudflared 免註冊快速通道 `C:\Users\admin\cloudflared.exe tunnel --url http://localhost:8080`，**網址每次會變**。）

## 10. 「給家人一鍵用」的方案（設計結論，尚未實作）
家人**不能自己跑伺服器**（要 GPU + 全套 WSL/模型）。正解：**伺服器留你 PC 24h 開**，家人只在爺爺平板用固定網址。待做：
1. 固定網址（§9）+ PC 24h + 看門狗（§11）。
2. Companion 做成 **PWA**（manifest+圖示）→ 平板「加到主畫面」變 App 圖示，一點全螢幕進。
3. 給家人：**QR code + 連結 + 一頁圖文指南**（怎麼設定、爺爺怎麼用、沒反應怎麼辦、怎麼找你）。

## 11. 已知問題 / TODO
- [ ] **看門狗**：`watchdog.ps1` 目前只顧 companion :8080，**沒顧 Qwen :50000** → 要合併（服務常因 VRAM 當機）。
- [ ] ngrok 域名被佔（§9）+ 免費警告頁；或改 Funnel/cloudflared。
- [ ] `/setup` 加密碼。
- [ ] PWA + QR + 家人指南（§10）。
- [ ] 台語 STT（formoai gated 待審 / 設 HF token）。
- [ ] 多人陪伴：媽媽錄音（`recordings/Mom_Voice/` 18 句）已存，等爸爸管線穩再做。
- [ ] 懷舊舊照片閒置畫面（§1）。
- [x] ~~開源前必辦~~（2026-08-19 大致完成，見 §11.6）；**剩**：`.env` 裡的舊 `MIMO_API_KEY` 建議刪、首次 `git commit` + tag。

## 11.6 開源就緒（2026-08-19）
- **`.gitignore` 加固**：修了「行尾註解讓規則失效」的坑；現在 `recordings/`（爸媽原始錄音）、`samples/`、`voices/`、`photos/`、`memory.json`、所有 `*.wav/mp3/m4a/aac/flac/ogg`、`father_reference.*`、`legacy/` 全排除。`git add -A -n` 稽核 = 0 敏感檔。
- **docs 去識別**：`爸爸_2分鐘錄音稿.txt`→`錄音稿範例.txt`（標題改「家人」）；`項目介紹` 移除 EduGen 提及（不連到私有商業項目）。
- **🎙 自帶音色（bring-your-own-voice）**：repo 不含任何人聲，使用者在 `/setup`「設定陪伴聲音」上傳 10-30s 參考音 →`/setup/set-voice`（decode_audio 解碼→whisper 轉逐字稿→存 `voices/active_reference.wav`+`.txt`）→ Qwen `POST /reload-ref` **熱重載不用重啟**。音色優先序：`voices/active_reference.wav` > `QWEN_REF`(father，本地) > 無→edge 通用聲。已端到端測通。
- **補齊**：`README.md`（含自帶音色/隱私/免責）、`LICENSE`（MIT，署名用 contributors 不放真名）、`.env.example`（改成 Nemotron，去 MiMo/CosyVoice）。
- [x] ~~launch/stop/watchdog 只看 :8080 → whisper 載入窗口重複起兩份撞 VRAM~~（2026-07-10 已改行程比對，見 §3.0）。

## 11.5 近期修復（2026-07-10）
使用者實測 3 bug + Fable 5 全盤掃 10 bug，皆已修並驗證上線：
- **大腦講內心獨白**：Nemotron reasoning 分離不穩、`max_tokens=80` 截斷思考漏進 content → `disable_thinking:true`（送 `enable_thinking:false`，實測 reasoning=0）。見 §5。
- **非父親聲音**：Qwen 沒起退 edge → 起 Qwen + launch 錯開 VRAM（§3.0）。
- **自稱孫女**：多為洩漏思考所致 → 關思考 + persona 強化「絕不自稱孫子/孫女/性別/身分」+ `_sanitize_reply()` 去 emoji/markdown。
- **auto 模式嚴重卡死 ×2**：① 雜訊觸發送出後沒清 `processing` class → 按鈕死鎖（修：續聽前清狀態 + `NOSPEECH_MAX=4` 連續沒聽到就休息）；② getUserMedia await 競態 → 放開手仍無限錄音／proc 未建就用（修：`pressed`+`micBusy` 旗標 + `ctx.close()`）。
- **其他**：半夜 0-4 點講「下午」→ 加凌晨/中午+12h制；滑鼠移出/touchcancel 收不掉錄音；auto 播放時按鈕標籤誤導；`endTurn` 蓋掉錄音中 UI；奇數位元組 `frombuffer` 500；/setup 試聽 blob URL 不 revoke；watchdog.ps1 補 BOM。

## 12. 檔案結構（皆在專案資料夾內）
```
根/         companion_web.py(主) qwen_tts_api.py(WSL TTS · 現役僅此二支)
           conf.yaml .env .env.example .gitignore requirements.txt watchdog.ps1
           一鍵啟動.bat 一鍵停止.bat  ui_state.json(說話模式預設)
           father_reference.wav/.txt  memory.json  server.*.log  PROJECT.md(本檔)
photos/     爺爺老照片（懷舊輪播，放 jpg/png 就播；空=暖色占位）
design/     爺爺前端_日系版.html（設計原型）
phrases/    固定句 17 條爸爸真聲 wav
voices/     克隆素材
recordings/ 原始錄音：Father_Voice/  Mom_Voice/(媽媽18句)  爺爺我在_父親版.aac
scripts/    現役腳本：_start_qwen.sh / _stop_qwen.sh（launch/stop.ps1 呼叫）、
           launch.ps1 / stop.ps1 / setup_env.ps1、父親參考音 _build/_rebuild/_denoise、_flash_setup.sh、_test_qwen*
           ⚠️ 部分父親參考音 .sh 內部路徑仍指舊 D:\Downloads\Father_Voice，重跑要改成 recordings/
docs/       RUN_PHASE0.md、錄音稿/講稿/項目介紹
legacy/     舊實驗檔 + 2026-07 清理移入：cosyvoice_api.py / stt_api.py / 兩個舊啟動器 / CosyVoice·seed-vc·RVC·STT 實驗 _*.sh
```

## 13. 環境 / 金鑰位置（值不寫這裡，開源安全）
| 用途 | 環境變數 | 值在哪 |
|---|---|---|
| 大腦 Nemotron | `NVIDIA_API_KEY` | `.env`|
| 舊 MiMo（退役）| `MIMO_API_KEY` | `.env`（**待輪替/刪**）|
| 家人通報 | `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | 環境變數（未設則通報關）|
| Qwen 參考音/模型 | `QWEN_REF` / `QWEN_MODEL` / `QWEN_PORT` | 預設在 `qwen_tts_api.py`，可環境覆蓋 |
| AI 浮水印開關 | `WATERMARK`（預設 1；0=關）| WSL 端 `qwen_tts_api.py`（§6）|
| 同意閘門開關 | `CONSENT_REQUIRED`（預設 1；0=關）| Windows 端 `companion_web.py`（§6.5）|
- Windows venv：`venv`；WSL venv：`/root/rvc_env`（Ubuntu-22.04，**唯一現役 WSL 環境**）。
- **磁碟清理（2026-07-10）**：WSL 內刪了 `cosyvoice_env`/`seed-vc`/`CosyVoice`/`RVC` 廢棄環境 + pip 快取；HF 快取只留 Qwen 1.7B（`~/.cache/huggingface` 14G→4.3G，刪了 NUTN台語/hubert/Qwen0.6B/bigvgan/whisper-small）。ext4 用量降到 ~14G。⚠️ **但 C 碟的 `ext4.vhdx`（~37G）原地壓縮無效** —— WSL2 sparse vhdx 已知坑，diskpart / Optimize-VHD / 填零全 ≈0（填零還危險：ext4 掛 1TB 虛擬盤會失控）。要真正還 C 碟空間，須 `wsl --export`→`--unregister`→`--import` **搬到 D 碟**（順帶重建成 ~14G 的乾淨 vhdx）。
- **Docker Desktop**：本機有裝（`docker-desktop` WSL 發行版 + `docker_data.vhdx`，約佔 C 碟 8G），**爺爺專案完全沒用到**；有自動啟動的 `com.docker.service` watchdog，要清得先停服務+關自動啟動才不會補回。
- **CPU 防當**：本機 min processor state 釘 100% 避 AMD Kernel-Power 41（正解在 BIOS Global C-state Control）。

## 14. 三步驟快速排錯
1. `GET :8080/health` → 哪個 false 修哪個。`mimo.ok=false` 查 §5 的 key/端點；`cosyvoice.ok=false` 去 WSL 起 Qwen(§3.2)。
2. 平板沒聲音 → 先確認 HTTPS 通道在（§9）、麥克風權限、Android 播 `new Audio()` 沒問題（只有 iOS 有 autoplay 坑）。
3. 服務自己掛 → VRAM 搶爆，重起對應服務；長期靠看門狗（§11）。
