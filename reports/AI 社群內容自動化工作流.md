# 讓 Claude 打草稿，發文鍵留給自己

**結論先講：每週 4 小時做得完，前提是自動化只用在「研究 → 草稿 → 素材 → 檢查」這幾段，「選題、定稿、按發布、回留言」都留給你本人。** 2025–2026 年有記錄的獨立創作者工作流，幾乎都長同一個樣子：AI 做聆聽摘要、初稿和各平台改寫，人在中間設一道核准關卡，最後才交給排程器。沒有任何一份資料建議有名聲風險的品牌讓 AI 無人看管地發文。對 alzheimer-companion 來說，這不只是品味問題，也是硬性限制。小紅書在 2026 年 3 月起會封禁「AI 託管帳號」；Facebook 社團自 2024 年起已沒有發文 API；Reddit 的 r/opensource 在 2026 年 10 月直接禁止 AI 相關專案。照顧者社群也有 Meta AI 冒充「過來人」回覆而出事的紀錄。$0 方案確實可行：Claude Code 加上一份品牌語氣檔、各平台原生排程器（Meta Business Suite、Threads 內建排程、YouTube Studio），再加上用腳本批次生成、後製上字的插畫。低成本方案每月約 US$15–45，多出來的只是圖像 API、少量影片額度和一個跨平台排程器。揭露方面的紅線很清楚：**寫實影片、寫實聲音（包括聲音克隆示範）在 Meta 和 YouTube 都必須主動揭露**，YouTube 對健康主題還會把標籤放在播放器上；小紅書依中國法規，任何 AI 內容都要自主聲明。插畫式漫畫在 Meta 不強制揭露，但建議一律自願標示。本報告以 2026-10-27 的平台研究報告（`docs/social-media-research.md`）為基礎，那份已經寫過的平台定位、內容支柱和貼文點子不再重複，這裡只處理「怎麼用最少時間穩定產出」。

> **可信度說明**：這次研究時，buffer.com、developers.facebook.com、YouTube 說明中心、Meta 透明度中心、CAC 官網等一手頁面都無法直接讀取。很多數字因此來自搜尋摘要或第三方部落格。本文以 **［待查證］** 標示需要回官方頁面確認的項目，以 **［二手］** 標示只有第三方或廠商來源的項目。價格與額度每月都在變，付費前請再確認。

---

## 一、可以交給 AI 的只有前半段，發文與回覆都要你親手做

有記錄的工作流都是分段管線：研究代理 → 寫作代理（搭配品牌語氣檔）→ 各平台改寫 → **人工核准關卡** → 排程器。n8n 官方範本庫裡的「AI 草稿 → Telegram 問『可以發嗎？』→ 核准才發」就是典型（[n8n #5625](https://n8n.io/workflows/5625-create-x-posts-with-gemini-and-gpt-41-ai-and-telegram-human-in-the-loop-approval)、[n8n #5397](https://n8n.io/workflows/5397)）。MindStudio 的 Claude Code 指南建議**分兩階段**：先寫核心訊息，再逐平台改寫，因為一個大 prompt 同時寫多個平台效果較差。指南也建議把品牌語氣寫成可重複使用的 skill 檔（[MindStudio](https://www.mindstudio.ai/blog/claude-code-skills-social-media-content-repurposing)）［廠商］。社群上已經有現成的 Claude Code skill，例如 `social-media-content-repurposer`、`crosspost`，可以參考它們的結構（[claudemarketplaces](https://claudemarketplaces.com/skills/onewave-ai/claude-skills/social-media-content-repurposer)、[killer-skills](https://killer-skills.pages.dev/en/skills/affaan-m/everything-claude-code/crosspost)）。

「AI 能省多少時間」沒有獨立研究可以回答。網路上「每週省 10–15 小時」的說法，都是創作者自述或廠商宣稱（[Startup Ideas Podcast](https://audioscrape.com/podcast/the-startup-ideas-podcast/episode/i-built-an-ai-content-agent-that-3x-my-engagement-in-30-days-full-n8n-workflow)）。最大的樣本是 Buffer 分析約 120 萬則貼文，AI 輔助貼文的中位互動率是 5.87%，非 AI 是 4.82%。但 Buffer 自己把差異歸因於 **AI 讓人更規律地發文**，不是 AI 文案比較好，而且這份資料是 2024 年的（[Buffer](https://buffer.com/resources/ai-assistant-post-performance/)）［二手，原頁未能讀取］。這點很重要：**AI 的價值在於讓你不斷更**，不在於幫你寫出爆文。

反過來說，自動化做過頭的代價已經可以量化。Sprout Social 2026 年第一季調查顯示，**未標示的 AI 內容是消費者最反感的品牌行為**（28%），50% 的 Z 世代曾因內容像「AI slop」而封鎖或退追（[eMarketer](https://www.emarketer.com/content/hiding-ai-use-brands--biggest-social-media-sin)）。平台也在收緊：

- **YouTube**：2025 年 7 月把營利規則裡的「重複內容」改名為「**不真實內容**」，針對大量生產、模板化的影片（[Social Media Today](https://www.socialmediatoday.com/news/youtube-clarifies-monetization-update-inauthentic-repeated-content/752892/)）。
- **Facebook**：同月開始降低搬運內容的觸及（[MediaNama](https://www.medianama.com/2025/07/223-meta-cracks-down-on-unoriginal-facebook-content/)）。
- **Instagram**：2026 年 4 月把原創性政策從 Reels 擴大到全平台（[PetaPixel](https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/)）。
- **小紅書最嚴格**：2026 年 3 月 10 日起，一般帳號偶爾讓 AI 代寫、代發、代互動，會被警告或限流；透過 AI 託管工具註冊、發文、互動，或公開筆記全由 AI 發布的帳號，會被**封禁**（[光明網](https://m.gmw.cn/2026-03/10/content_1304371172.htm)、[澎湃](https://www.thepaper.cn/newsDetail_forward_32747698)）。

跨平台改寫因此不能只是複製貼上，每個版本都要有新開頭、原生格式，也不能帶其他平台的浮水印。

回覆留言是最不能交給 AI 的環節。2024 年 Meta AI 在 Facebook 家長社團裡自稱「有個特殊需求的孩子」，被 AI 事件資料庫收錄為支持型社群的傷害案例（[AIID #700](https://incidentdatabase.ai/cite/700/)）。Meta 在 Instagram 和 Threads 測試 AI 代擬留言、AI 回覆，也都引發強烈反彈（[dig.watch](https://dig.watch/updates/instagram-users-react-to-metas-new-ai-experiment)）。可以安全自動化的是**分流**：把各平台新留言收進一份摘要，分類成提問、讚美、bug 回報、情緒求助、醫療問題，標出需要優先處理的，再從審過的 FAQ 擬回覆草稿。**送出那一下一定是你。** 下表把各環節整理在一起：

| 環節 | 交給 AI／自動化 | 必須本人做 | 理由 |
|---|---|---|---|
| 聆聽／趨勢研究 | 關鍵字提醒（F5Bot、Threads 關鍵字搜尋 API）、把收集到的討論整理成「痛點／常見問題／照顧者用語」摘要 | 以成員身分親自讀 FB 照顧者社團；判斷什麼話題在情緒上適合碰 | FB 社團沒有合法的聆聽 API；GummySearch 因 Reddit API 商業條款收攤 |
| 選題 | 把痛點分群、排出候選清單 | 決定主題與角度 | 原創觀點是 Meta 與 YouTube 規則保護的對象 |
| 文案 | 照品牌語氣檔寫初稿，兩階段改寫成繁中／英文／簡中版本 | 改成自己的口吻；第一人稱故事由你寫；檢查有沒有醫療宣稱 | 未標示的 AI 和「slop」是消費者頭號反感 |
| 視覺 | 分鏡、prompt、批次生圖、上字腳本 | 每張圖都要親眼過目；不做寫實假長輩；不做假見證 | YouTube、Meta 對寫實合成內容有強制揭露 |
| 排程／發布 | 核准後進原生排程器或 Postiz／Buffer | 核准關卡；Reddit、小紅書、FB 社團一律手動發 | 小紅書封禁 AI 託管帳號；FB 社團沒有 API |
| 社群互動 | 分流、情緒危機標記、FAQ 回覆草稿 | 每一則公開回覆和私訊 | Meta AI 支持社團事件；小紅書處罰 AI 互動 |
| 數據 | 每週把各平台數字整理成 CSV，摘要哪些主題和格式表現好 | 決定策略要不要調整 | 沒有免費的全平台工具 |

---

## 二、$0 工具鏈做得到，關鍵是先別急著架自動化平台

**沒有任何一個免費工具能涵蓋六個平台**，但各平台的原生排程器加起來，已經能免費處理最需要定時的部分。Meta Business Suite 可以免費排程 FB 粉專和 IG（[SocialChamp](https://www.socialchamp.com/blog/schedule-facebook-posts/)）［二手］。Threads 在 2025 年 1 月對所有人開放內建排程（[Techsoma](https://techsoma.africa/?p=3112)）。YouTube Studio 一向可以「先私人上傳、再設定公開時間」。至於 Business Suite 能不能排 Threads，兩份第三方指南說法相反，**［待查證］**（[DEV](https://dev.to/ppcvote/how-to-schedule-threads-posts-set-up-daily-auto-posting-in-5-minutes-1h0f) 說不行、[ShortSync](https://shortsync.app/guides/schedule-threads-posts) 說可以）。

想讓 Claude 直接把草稿送進排程器，有幾個官方 MCP 可以用。**Buffer** 有官方 MCP（[buffer.com/mcp](https://buffer.com/mcp)），Free 方案是 3 個頻道、每頻道最多排隊 10 則（[boomp.net](https://boomp.net/blog/buffer-pricing-free-plan-limits-2026)）［二手；MCP 是否支援 Free 方案 **［待查證］**］。**Postiz** 是 AGPL 開源，雲端版 Standard 每月 US$29、5 個頻道、不限貼文數（[Postiz 官方方案](https://docs.postiz.com/cloud/plans)），官方 MCP 可以一行指令加進 Claude Code（[postiz.com/claude-code](https://postiz.com/claude-code)）。Postiz 自架版授權免費，代價不小：v2.12 之後必須跑 Temporal，最低 2 vCPU/2 GB（[Postiz 系統需求](https://docs.postiz.com/installation/system-requirements)），Railway 上約每月 US$15–25（[Railway 範本](https://railway.com/deploy/postiz-self-hosted-buffer-alternative-for-30-platforms--postiz-social-scheduler)）［二手估價］。另外還要自己向 Meta、Google 申請開發者 App。Postiz MCP 第三方包裝的作者也提醒：「讓 AI 代理在沒有護欄的情況下操作，是把錯的草稿發到錯的帳號的最快方法」（[solomonneas](https://solomonneas.dev/projects/postiz-mcp)）。

自動化膠水方面：

- **n8n 自架社群版**：唯一不限執行次數又免費的選擇，只需付主機費。
- **n8n Cloud**：沒有永久免費方案，Starter 約 €20/月（[sliplane](https://sliplane.io/blog/n8n-pricing)）［二手］。
- **Make Free**：1,000 credits、最多 2 個啟用中的情境（[jetadmin](https://www.jetadmin.io/blog/make-pricing/amp/)）［二手］。
- **Zapier Free**：每月 100 tasks、只能兩步驟，對這個用途太小（[DEV](https://dev.to/trackstack/zapier-free-plan-in-2026-what-100-tasks-actually-buy-you-3h8k)）。

**我的建議是第一階段完全不架 n8n 或 Postiz。** 每週發文量大約十幾則，在原生排程器手動貼上的時間，比維護一套自架系統、通過 Meta App Review、處理 OAuth 驗證都少。核准關卡也自然存在：草稿在 repo 的資料夾裡，你看過、改過、貼進排程器，就等於核准了。等到「複製貼上」真的成為瓶頸（例如超過一個月都穩定每週發文），再加 Buffer Free + Buffer MCP，或 Postiz Cloud，而且設定成**只建草稿、不直接發布**。

各平台官方 API 的限制，決定了哪些平台根本不可能自動發：

| 平台 | 官方 API 現況 | 對你的意義 | 可信度 |
|---|---|---|---|
| Threads | 每帳號每 24 小時 250 則 API 發文；自己的帳號或測試者在開發模式下不需 App Review；關鍵字搜尋 API 每 7 天 500 次 | 可自動化，但量遠用不到上限；關鍵字 API 適合做聆聽 | 官方摘要（[Meta](https://developers.facebook.com/docs/threads/overview)、[Meta dev blog](https://developers.facebook.com/blog/post/2024/12/09/discover-ideas-with-the-threads-api/)） |
| Instagram | 需商業或創作者帳號；常見說法是每 24 小時約 100 則 API 發文 | 可經 Business Suite 或排程器發 | **［待查證］**，本次未能讀到官方頁 |
| FB 粉專 | 可經 Business Suite 或 Graph API 發文 | 可排程 | 權限細節 **［待查證］** |
| **FB 社團** | **Groups API 已在 2024 年 4 月移除，沒有替代方案**（[Meta 開發者論壇](https://developers.facebook.com/community/threads/2076398286093257/)） | **只能手動**；排程器最多只能提醒你 | 多方一致 |
| YouTube | 每專案每日 10,000 units；據報 2025 年 12 月上傳成本降到約 100 units，2026 年 6 月起上傳另有每日 100 次的獨立額度（[bundle.social](https://bundle.social/blog/youtube-api-quota-exceeded-limits-fixes)） | 額度不是問題；未驗證的 API 專案上傳可能被鎖在私人 | 額度變動 ［二手］；私人鎖定 **［待查證］** |
| Reddit | 2025 年 11 月起關閉自助申請，一律要人工審核（[r/redditdev 公告鏡像](https://r.datuan.dev/r/redditdev/s/gquSJqMgrM)）；第三方說 2026-10-31 停止受理新申請 | **只能手動**；推廣用的機器人也不符合「負責任開發者」的精神 | 停收日期 **［待查證］**（[keyapi.ai](https://www.keyapi.ai/blog/reddit-data-api-overhaul-major-changes-and-migration-guide/)） |
| 小紅書 | **沒有公開發文 API**；市面工具都靠 cookie 操控瀏覽器，cookie 檔等同帳號憑證（[ClawHub 安全稽核](https://clawhub.ai/jmin1113/skills/xiaohongshu-auto-poster/security-audit)） | **只能手動**；自動化等於直接踩 AI 託管封禁條款 | 多方一致 |

小紅書在台灣還有一層：內政部 2025 年 12 月依《詐欺犯罪危害防制條例》第 42 條，對小紅書下了暫定一年的停止解析令（[NOWnews](https://www.nownews.com/news/6761411)），到期大約是 2026 年 12 月。**目前有沒有延長或解除，［待查證］**。

聆聽工具用免費的就夠：

- **Reddit**：F5Bot 免費關鍵字 email 提醒，付費升級可用 Syften，約 US$19.95/月（[DEV](https://dev.to/devtoolpicks/best-gummysearch-alternatives-in-2026-honest-picks-for-solo-devs-and-indie-hackers-4af9)）［二手］。
- **Threads**：可以寫一個小 Claude Code skill 呼叫 Threads 關鍵字搜尋 API，每週產生摘要。
- **小紅書**：用 App 內的搜尋下拉選單和創作服務平台。

數據方面，Metricool Free 是 1 個品牌、每月 20 則排程、30 天歷史（[Metricool 官方說明](https://help.metricool.com/es/main-differences-between-free-and-paid-plans-bl0v9)），但對你來說，原生後台加上一份 repo 內的 CSV 就夠了。真正該看的轉換指標，是 GitHub Star 和 README 的流量來源。

---

## 三、角色一致靠「一張設定圖＋無字面板＋後製上字」

2026 年的比較文章大多推薦 Google 的 **Nano Banana 系列（Gemini 圖像模型）**，認為它最能維持角色一致；GPT Image 2 是接近的第二名，文字渲染較強；Midjourney 美感最好但最難維持同一角色（[rupertchesman](https://rupertchesman.com/blog-midjourney-vs-nano-banana-vs-chatgpt-images-2026.html)、[pixmind](https://www.pixmind.io/posts/midjourney-v7-vs-gpt-image-2-vs-nano-banana-2)）［二手，都是部落格評比，沒有獨立基準測試］。

可重複的做法有三步：

1. 先做一張乾淨的「角色設定圖」，例如一位穿毛背心、戴眼鏡的虛構阿公，加上孫子。**要從文字描述生成，不要上傳真實家人照片。**
2. 之後每一格都只用這張圖當參考。
3. prompt 固定由四塊組成：「角色描述＋鏡位＋動作＋固定畫風句」（[creativeainews](https://www.creativeainews.com/articles/how-to-make-a-comic-with-ai-2026/)、[weshop.ai](https://www.weshop.ai/solutions/models/nano-banana-2-1-consistent-character-storyboard)）。

粗線條、少色、有標誌性道具的扁平畫風，最能掩蓋角色漂移，這是實務推論。成本上，Nano Banana 2 在 1K 解析度約 **US$0.067/張**（[myarchitectai](https://www.myarchitectai.com/blog/nano-banana-api-pricing)）［二手］，每週 40 張約 US$3。你的 RTX 4060 8GB 不適合訓練 Flux LoRA，多份指南說至少要 12–24 GB（[dev.to](https://dev.to/thurmon_demich/best-gpu-for-fluxgym-in-2026-5-picks-for-flux-lora-training-pp6)）。本機替代方案是 Qwen-Image-Edit-2511 的 GGUF 量化版，ComfyUI 原生支援（[ComfyUI 文件](https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit-2511)），但**能不能在 8 GB 上順利跑，沒有來源證實**。

**繁體中文字不要讓模型畫。** GPT Image 2 號稱文字正確率 99%，但沒有任何來源專測繁體（[biggo](https://finance.biggo.com/news/202604240451_GPT-Image-2-text-rendering-analysis)），而中文字基準測試用的是大陸標準字集（[arXiv 2604.28185](https://arxiv.org/pdf/2604.28185)）。穩定做法是生成**留白對話框的無字面板**，再用 Pillow 或 HTML→PNG 模板套上 Noto Sans TC 等免費字型。同一組畫面換一份簡體文字，就能直接給小紅書用。Canva 的 Autofill API 要 Enterprise 才能用（[Canva 開發文件](https://www.canva.dev/docs/connect/autofill-guide/)），對你來說，自己寫一支模板腳本比較實際。

影片的原則是「**用圖生影片，不用文生影片**」。最省的 Reel／Short 做法是：靜態面板加平移或縮放（Ken Burns 效果）、配上旁白、字幕直接從腳本產生（腳本是已知的，不需要語音辨識），用 FFmpeg 組裝，成本 $0。旁白有兩個選擇。一是開源的 `edge-tts`，可免費使用台灣口音的 HsiaoChen、YunJhe 語音（[ClawHub](https://clawhub.ai/hamlet0168/edge-tts-zh)），但免費端點的使用條款 **［待查證］**。二是直接用**本專案自己的 TTS** 來念旁白，同時也是產品示範，不過要用你本人或已授權者的聲音，並且揭露（見下一節）。

只有在需要一兩個「主角動起來」的鏡頭時才花影片額度：

- **Kling**：免費版有浮水印、不可商用；Standard 約 US$10/月是乾淨輸出的最低門檻（[atlascloud](https://www.atlascloud.ai/blog/guides/kling-ai-pricing)）［二手］。
- **Google AI Pro**：US$19.99/月，含約 50 支 Veo 3 Fast（[getaiperks](https://www.getaiperks.com/en/blogs/44-best-ai-video-generators-2026)）［二手］。
- **Sora 已經不能用了**：App 在 2026-04-26 關閉，API 在 2026-09-24 停止（[techjacksolutions](https://techjacksolutions.com/ai-brief/openai-videos-api-sora-2-deprecated-september-2026/)），9 月以前的教學都已過時。
- **CapCut 自動字幕**是否已移到付費版，各來源說法矛盾，**［待查證］**（[Descript](https://descript.com/blog/article/capcut-captions-arent-free-anymore-heres-a-better-option) vs. [aejuice 論壇](https://forum.aejuice.com/t/aejuice-auto-captions-vs-capcut-auto-captions-2026/2173)）。

---

## 四、揭露紅線：寫實影音與聲音克隆一律要標

各平台對「必須揭露」的界線不同，但對你最重要的交集很清楚：**聲音克隆示範屬於「寫實合成聲音」，在 Meta 和 YouTube 都是強制揭露範圍。** 插畫漫畫在多數平台不強制，但照護題材的受眾對未標示的 AI 特別敏感，平台的偵測器也會讀取 C2PA 中繼資料自動貼標（[ClipSpeed](https://www.clipspeed.ai/blog/ai-generated-video-disclosure-rules.html)）［二手］。主動標示，總比被平台貼標後再解釋好。

| 地區／平台 | 強制揭露範圍 | 健康題材的特別規定 | 違規後果 | 可信度 |
|---|---|---|---|---|
| **Meta（FB／IG／Threads）** | 數位製作或修改的**寫實影片、寫實音訊**，須用 AI 揭露工具；靜態圖不強制，但可能被自動標「AI 資訊」 | 「在重要事項上有高度欺騙風險」的內容可能加上更醒目的標籤 | 可能處罰；Meta 拒絕公開處罰標準 | 依搜尋摘要（[Meta 透明度中心](https://transparency.meta.com/oversight/oversight-board-cases/ai-generated-video-in-iran-israel-conflict/)、[TechCrunch](https://techcrunch.com/2024/02/06/meta-ai-generated-image-labelling/)）；2026 年確切措辭 **［待查證］** |
| **YouTube** | 寫實的人說了沒說過的話、寫實事件、**合成某人聲音來旁白**；只用 AI 寫腳本、想點子不需揭露 | **健康主題的標籤顯示在播放器上**，不只在說明欄 | 屢次不揭露可能被移除內容或停止營利；YouTube 可能自行加標 | 2024 年政策（[Business Today](https://www.businesstoday.in/amp/technology/news/story/youtubes-new-rule-to-tackle-deepfakes-misinformation-creators-must-flag-altered-or-ai-generated-content-405728-2023-11-15)、[9to5Google](https://9to5google.com/2024/03/18/youtube-altered-content-disclosure/)）；動畫豁免細節與 2026 年變更 **［待查證］**；網傳的「三振制度」**未證實** |
| **Reddit** | 全站沒有 AI 內容禁令，只禁欺騙與操弄；是否要求全站揭露，來源互相矛盾 | 各版自訂；**r/opensource 於 2026 年 10 月禁止使用 AI 或為 AI 打造的專案**（[The Register](https://www.theregister.com/software/2026/10/26/reddits-r/opensource-bans-ai-slop-and-quite-a-few-humans-for-good-measure/5305392)） | 被版主刪文、封禁 | 全站揭露義務 **［待查證］**（[Versely](https://www.versely.studio/blog/reddit-has-no-site-wide-ai-ban)）［二手］ |
| **小紅書／中國大陸** | 《人工智能生成合成内容标识办法》2025-09-01 施行，第 10 條：使用者發布 AI 內容**應主動聲明**並使用平台的標識功能，不得刪除標識（[新華網全文](https://www.news.cn/politics/20250314/75107e1e6566404f8471559a8fb34158/c.html)） | 2025 年 8 月四部委通知：健康內容創作者須驗證資質，**新帳號未認證前不得發健康內容**，健康科普須註明來源並揭露 AI（[人民網英文](https://en.people.cn/n3/2025/0804/c90000-20348885.html)） | 2026-02 起未自主聲明的 AI 內容會被平台貼標並**限流**（[163.com](https://www.163.com/dy/article/KLLNQUFT053469M5.html)）；AI 託管帳號封禁 | 法規條文可信；平台公告原文未取得 ［二手報導］；這些規定是否適用台灣個人帳號 **［待查證］** |
| **台灣** | 《人工智慧基本法》2025-12-23 三讀，是框架法，**沒有一般性的 AI 內容標示義務**，只針對被認定為高風險的 AI 產品（[TechNews](https://technews.tw/2025/12/23/artificial-intelligence-basic-law/)、[天下](https://www.cw.com.tw/article/5139204)） | 《醫療器材管理法》第 6 條：**暗示或影射醫療效能**的報導、宣傳都視為廣告（[高雄高等行政法院判決](https://judgment.judicial.gov.tw/FILES/KSTA/113%2c%e5%9c%b0%e8%a8%b4%2c107%2c20260629%2c2.pdf)）；非醫材宣稱療效可罰 60 萬–2,500 萬元（[TVBS 引臺北市衛生局](https://news.tvbs.com.tw/life/2970257)） | 付費推廣貼文屬廣告，數發部草案要求揭露是否使用深偽或 AI 生成肖像（[數發部草案](https://www-api.moda.gov.tw/File/Get/adi/zh-tw/rcorti3mjvbcFtO)） | 數發部定案版本 **［待查證］** |
| **香港** | 沒有法定 AI 內容標示義務 | 私隱公署 2025 年 12 月發布深偽指引；**家人的聲音屬於個人資料**，受《個人資料（私隱）條例》規範（[unwire.hk](https://unwire.hk/2025/12/18/ai-deepfake-privacy-pcpd-guidance-hong-kong/ai/)、[私隱公署](https://www.pcpd.org.hk/tc_chi/resources_centre/publications/files/ai_deepfake.pdf)） | 惡意深偽可能違法 | 《不良醫藥廣告條例》本次未研究 **［待查證］** |

這張表帶出兩個新判斷，會修正前一份報告。

第一，**r/opensource 應從 Reddit 目標清單移除**。前一份報告把它列為技術版之一，但它 10 月的新規很可能直接擋掉一個用聲音克隆的開源專案。r/selfhosted、r/LocalLLaMA 發文前也要重讀側欄規則。

第二，**小紅書的風險比前一份報告估得更高**。現在疊了好幾層：台灣封鎖、沒有 API、AI 託管會被封禁、新帳號不能發健康內容、AI 內容必須自主聲明。所以小紅書應該維持「暫停或每週最多一則手動」，題材限定在「開發日誌」和「隱私設計」這兩個最不像健康內容的支柱。

倫理上，失智症組織的共同原則是**不污名化的文字與影像、呈現多元、尊重當事人偏好**。Alzheimer Europe 指出，「文字與影像」中的失智呈現方式，會影響失智者被對待的方式（[Alzheimer Europe 指引](https://www.alzheimer-europe.org/resources/publications/guidelines-ethical-and-inclusive-communication-about/portrayal-dementia-and)）。英國阿茲海默症協會 2025 年 10 月也推出了失智友善媒體指南（[Alzheimer's Society](https://www.alzheimers.org.uk/news/2025-10-08/julian-fellowes-helps-launch-dementia-friendly-media-arts-and-drama-guide)）。對 AI 素材來說，這代表：

- 選**插畫風、明確虛構的角色**，不用寫實的「AI 假長輩」。這既避開 Meta 和 YouTube 的強制寫實標籤，也避免在健康脈絡中被看成「假病人」。
- 不用 AI 圖庫常見的污名化意象：只拍手、沒有臉、霧濛濛的「記憶消逝」、拼圖腦袋。

聲音克隆本身也帶有詐騙聯想（[TechNews](https://technews.tw/2024/08/20/deepfake-fraud-statute/)），所以每次露出都要同時說明三件事：本人同意、聲音不出門、這是合成。

---

## 五、可執行工作流：每週 4 小時、一個核心內容、三個手動平台

### 管線圖

```
 ┌──────────── 週五晚（自動，0 分鐘）──────────────┐
 │ F5Bot email ─┐                                 │
 │ Threads 關鍵字 API ─┼→ Claude: digest.md          │
 │ 上週 metrics.csv ─┘  (痛點／問題／照顧者用語／表現最好的貼文)   │
 └──────────────────────────────────────────────┘
                     ↓
 ┌──────────── 週六批次（約 2 小時 45 分）──────────┐
 │ [你] 選 1 個核心主題＋角度                            │
 │   ↓                                              │
 │ [你] 口述或條列 → [Claude] 寫成核心長文 → [你] 改成自己的話   │
 │   ↓                                              │
 │ [Claude] 第二階段：各平台草稿（繁中／英文／簡中）           │
 │   ↓                                              │
 │ [Claude] 分鏡＋prompt → 批次生圖 → 模板上字 → FFmpeg 組片 │
 │   ↓                                              │
 │ [Claude] 合規檢查（禁用詞／簡繁混用／揭露句／連結位置）      │
 │   ↓                                              │
 │ ★ 核准關卡 [你]：逐篇看、改、勾 AI 揭露開關                │
 │   ↓                                              │
 │ 原生排程器：Threads 內建｜Business Suite(FB 粉專+IG)｜YT Studio │
 └──────────────────────────────────────────────┘
                     ↓
 ┌──────────── 週一到週五（每天 15 分鐘，全手動）───────┐
 │ 回留言 → 參與別人的討論 → 手動發 FB 社團／Reddit／小紅書   │
 │ 好問題存進點子庫（點子庫是下週選題的來源）                   │
 └──────────────────────────────────────────────┘
```

建議在 repo 裡建一個 `marketing/` 資料夾，放 `brand-voice.md`（語氣、身分是家屬兼開發者、固定免責句）、`do-not-say.md`（禁用詞清單，直接沿用前一份報告第 4 節的用語表）、`character-sheet.png`、`templates/`（上字與輪播模板）、`queue/2026-W44/`（每週草稿）、`library.csv`（內容庫）、`metrics.csv`。再寫一個自訂 Claude Code skill，例如 `/weekly-content`，把上面的步驟串起來。**這個 skill 不要接任何發布用的 MCP**，讀留言和發文的權限要分開，也避免留言內容透過提示注入操控代理（[ClawHub 稽核](https://clawhub.ai/mrmao007/skills/rednote-skills/security-audit) 也提出同樣警告）。

### 每週節奏（總計約 4 小時，硬上限 5 小時）

| 時段 | 步驟 | 誰做 | 時間 |
|---|---|---|---|
| 週五晚 | 產生聆聽摘要：整理 F5Bot 信件、Threads 關鍵字搜尋、上週數據 | Claude（排程或手動下一個指令） | 0（你不用在場） |
| 週六 0:00 | 讀摘要，選 1 個核心主題（輪流用 5 根內容支柱），決定角度 | **你** | 15 分 |
| 週六 0:15 | 口述或條列 10 分鐘 → Claude 寫成 600–1,000 字核心長文（開發日誌或照護故事）→ 你改成自己的話 | 你＋Claude | 35 分 |
| 週六 0:50 | Claude 產出各平台草稿：Threads 繁中 3 則（英文選配）、IG 輪播 6–8 張文案、FB 粉專長文、Short 腳本 30–45 秒、Reddit 草稿（若本週有）、小紅書簡中改寫（若本週有） | Claude | 5 分（等待） |
| 週六 0:55 | 逐篇修改草稿：開頭、口吻、事實、提問句 | **你** | 30 分 |
| 週六 1:25 | 視覺：Claude 寫分鏡和 prompt，批次跑參考圖生圖，你挑圖（不合格就重跑），腳本套上繁中字 | Claude 生、**你挑** | 25 分 |
| 週六 1:50 | Short／Reel：腳本組裝靜圖平移＋旁白（本專案 TTS 或 edge-tts）＋字幕；有預算時加 1 個 Kling 鏡頭 | Claude 組、你看一遍 | 15 分 |
| 週六 2:05 | 合規檢查：Claude 掃禁用詞、簡繁混用、揭露句、連結位置，輸出清單；你逐項確認 | Claude＋**你** | 10 分 |
| 週六 2:15 | 排程：貼進 Threads 內建排程、Business Suite（FB 粉專＋IG）、YouTube Studio，**每個平台都勾 AI 揭露** | **你** | 20 分 |
| 週六 2:35 | 更新 `library.csv`：常青標記、預計 6 或 12 個月後重用的日期 | Claude 寫、你確認 | 5 分 |
| 週一～五 | 每天 15 分鐘：5 分鐘回自己貼文的留言（Threads、IG 優先）；5 分鐘在別人的照護或開發討論真誠回覆；5 分鐘存點子，或手動發 FB 社團、Reddit、小紅書其中一則 | **你** | 75 分 |
| 每月最後一個週六 | 加 30 分鐘：Claude 彙整 `metrics.csv`，看哪些主題和格式表現好；你決定下個月的主題，並從內容庫挑 1 篇舊的高表現貼文改寫重發 | Claude＋**你** | 約 8 分／週（攤提） |
| **合計** | | | **約 4 小時／週** |

這個節奏的時間估算，是把廠商公布的步驟時間（規劃 45–60 分、集中寫作 1–2 小時，[SocialKit](https://socialk.it/en/blog/batch-content-creation-workflow)）［廠商］扣掉 AI 初稿省下的部分後推算的，**不是實測數字**，前兩週請自己計時校正。有兩條保護機制：

- **至少維持 2–3 週的常青內容庫存**，正職忙的那週就直接排庫存。Buffer 的 26 週研究顯示，26 週中有 20 週以上有發文的人，每則互動比只發 4 週以下的人高約 450%（[Buffer](https://buffer.com/resources/creator-growth-playbook)）［二手］。
- **要減量時，先砍投報最低的平台，不要全部停一週。** 依目前證據，先砍小紅書，其次是 FB 粉專。

### 各平台節奏（穩定期；冷啟動期請沿用前一份報告的 30 天計畫）

| 平台 | 頻率 | 格式 | 發布方式 | 依據 |
|---|---|---|---|---|
| Threads | 每週 3 則繁中（英文選配） | 純文字＋提問結尾，連結放留言 | 內建排程；發文後 1–3 小時內要能回留言 | Meta 建議每週 2–5 則；回覆佔近半數瀏覽（[Social Media Today](https://www.socialmediatoday.com/news/meta-shares-tips-on-how-to-grow-your-threads-presence/730488/)） |
| Instagram | 每週 2 則（1 Reel＋1 輪播） | 輪播重收藏和分享；1,000 追蹤以下 Reel 觸及較高 | Business Suite | 每週 3–5 則是甜蜜點，但 Mosseri 更看重能持續（[Buffer](https://buffer.com/resources/how-often-to-post-on-instagram/)［二手］、[Contentdrips](https://contentdrips.com/blog/2026/06/instagram-reels-vs-carousels-2026-guide/)） |
| FB 粉專 | 每週 1–2 則 | 核心長文的故事版 | Business Suite | 沒有官方頻率指引 |
| FB 社團 | 管理員同意後，每個社團最多 1 次主動分享；平時只參與 | 經驗分享、徵求意見 | **手動** | 沒有 API；社團通常禁止廣告 |
| YouTube | Shorts 每週 1 支（與 Reel 同一個原始檔，不帶浮水印）；長片每月最多 1 支 | 示範、FAQ、開發日誌 | YouTube Studio 排程 | 沒有官方頻率指引 |
| Reddit | 主貼每月 1 支以下；平時留言參與 | 純文字、提供價值、誠實列限制 | **手動** | 9:1 是社群慣例而非官方規則；各版規則優先（[Redship](https://redship.io/blog/reddit-self-promotion-rules)） |
| 小紅書 | 暫停，或每週最多 1 則（等封鎖狀態確認後再說） | 3:4 封面、標題 20 字內、簡體並在地化用詞、不放外連 | **手動**（需要時開 VPN） | AI 託管封禁、健康內容資質規定 |

### 工具鏈：$0 方案 vs. 低成本方案

| 用途 | $0 方案 | 低成本方案 | 備註 |
|---|---|---|---|
| 草稿與編排 | Claude Code＋自訂 skill（假設你已有 Claude 訂閱） | 同左 | 不另外計價 |
| 聆聽 | F5Bot、Threads 關鍵字 API（自己的 Meta App 開發模式）、小紅書 App 內搜尋 | ＋Syften 約 US$20/月 ［二手］ | FB 社團只能親自讀 |
| 圖像 | Gemini／ChatGPT App 免費額度 **［額度待查證］**，或本機 Qwen-Image-Edit GGUF **［8GB 是否可行待查證］** | Nano Banana 2 API 約 US$0.067/張，每週約 US$3 | 一律用角色設定圖；不上傳家人照片 |
| 上字與排版 | Pillow 或 Playwright 模板＋Noto Sans TC；Canva 免費版做一次性設計 | 同左 | 不讓模型渲染中文 |
| 影片 | 靜圖平移＋edge-tts 或專案 TTS＋FFmpeg | ＋Kling Standard 約 US$10/月，或 Google AI Pro US$19.99/月 | Kling 免費版有浮水印、不可商用；Sora 已停 |
| 排程 | Threads 內建、Meta Business Suite、YouTube Studio | Buffer Free＋MCP（3 頻道），或 Postiz Cloud US$29/月 | MCP 一律設成只建草稿 |
| 膠水 | 不需要（先別架） | n8n 自架或 Make Free | 等複製貼上真的成為瓶頸再說 |
| 數據 | 原生後台＋`metrics.csv`＋Claude 摘要；GitHub Traffic | Metricool Free | — |
| **每月合計** | **約 US$0** | **約 US$15–45** | 不含 Claude 訂閱 |

### 交給 Claude vs. 必須本人做

| 交給 Claude | 必須本人做 |
|---|---|
| 聆聽摘要、痛點分群、候選題目清單 | 選題、決定角度、判斷話題在情緒上是否適合碰 |
| 把你的條列或口述寫成核心長文；兩階段改寫成各平台、各語言版本 | 第一人稱故事的事實與感受；最後定稿的語氣 |
| 分鏡、prompt、批次生圖、上字、組片 | 每張圖和每支影片的最終核准；聲音克隆示範的錄音與同意書 |
| 禁用詞、簡繁、揭露句、連結位置的檢查 | 在各平台勾選 AI 揭露開關、按發布 |
| 留言分流、標出情緒危機或醫療問題、FAQ 回覆草稿 | **所有公開回覆、私訊，以及 FB 社團、Reddit、小紅書的每一次互動** |
| 數據彙整、內容庫維護 | 策略調整、聯絡協會或社團管理員 |

### 揭露與合規清單（每篇發文前逐項勾選）

**所有平台通用**
- [ ] 沒有「治療、改善失智、延緩退化、預防、醫療級、臨床證實」等暗示醫療效能的字；簡介和置頂寫明「非醫療器材」
- [ ] 提到「通知家人」功能時，附上「不是緊急救援系統，緊急請撥 119／999／911」
- [ ] 沒有出現真實失智長輩的臉、聲音、病房或真實對話；角色是虛構插畫
- [ ] AI 插畫或漫畫的說明文字寫明「AI 生成插畫，角色為虛構」，不刻意清除生成工具的中繼資料
- [ ] 聲音克隆示範：取得聲音提供者的書面或錄音同意；影片中標示「AI 合成語音示範」；附防詐提醒（家人驗證暗號、本程式不會打電話）
- [ ] 沒有用 AI 捏造照顧者見證；引用真實故事都已取得當事人同意
- [ ] 用語用「失智者／失智長輩」（台）、「認知障礙症」（港），不用「老人痴呆」；畫面不用污名化意象
- [ ] 表明「這是我做的」，不偽裝成使用者推薦

**各平台**

| 平台 | 發文前檢查 |
|---|---|
| Threads／IG／FB 粉專 | 寫實影片或聲音克隆 → **必須開啟 AI 揭露（AI 資訊）**；插畫 → 建議開啟，並寫在說明文字裡；連結放留言或個人簡介 |
| FB 社團 | 已取得管理員同意；不是 AI 代發、代回；同一社團這段期間沒有主動分享過 |
| YouTube | 聲音克隆或寫實合成 → 上傳時勾選「經過修改或合成的內容」（健康主題標籤會顯示在播放器上）；說明欄寫明 AI 使用方式；避免大量模板化的投影片影片 |
| Reddit | 已重讀該版側欄和置頂規則（確認沒有禁 AI 或禁自我推廣，**不發 r/opensource**）；照顧者版已先參與 2–4 週並私訊版主；內文主動揭露 AI 圖像和聲音克隆 |
| 小紅書 | 發布頁 → 高級選項 → **自主聲明「內容由 AI 生成」**；不放外連、不放 QR code；題材是開發日誌或隱私設計，不寫照護建議；確認台灣封鎖的現況 |
| 付費推廣（任何平台） | 依平台的廣告流程完成身分驗證和 AI／深偽揭露；再次確認沒有醫療效能暗示 |

---

## 結論

這次研究最重要的發現是：限制自動化程度的不是工具，而是平台規則和受眾信任。2026 年的工具已經能讓 Claude 從聆聽一路做到排程，但會讓帳號受罰或失去信任的，正好是最後兩步：無人看管的發布，和 AI 代為互動。對 alzheimer-companion 這種「靠信任吃飯」的照護專案，最好的槓桿是**把一個真實的核心內容做透，再用 AI 便宜地改寫成多個版本**，而不是用 AI 衝發文量。Buffer 的資料也指向同一件事：AI 帶來的成效提升主要來自規律發文，所以這套流程設計的重點是「你不會中斷」，不是「你發得多」。

這次研究也修正了先前的平台判斷：Reddit 的 r/opensource 已不再是可用的發表場所；小紅書在台灣面對封鎖、沒有 API、AI 託管封禁、健康內容資質等多重門檻，實際上應該降為選配。後續最值得做的三件事是：

1. 先用兩週實測這個 4 小時節奏，校正時間估算。
2. 到 Meta 說明中心、YouTube 說明中心、Reddit 各目標版的官方頁面，逐一確認本文標為 ［待查證］ 的揭露條款。
3. 2026 年 12 月確認小紅書封鎖令有沒有延長，再決定那個平台要不要繼續經營。
