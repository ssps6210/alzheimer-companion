# 讓 Claude 把草稿送進 Buffer 免費版

**結論：首選 Buffer Free（£0），備選 Postiz Cloud Standard（約 £22–23／月）。** 2026 年 5 月 27 日起，Buffer 的公開 GraphQL API 和官方 MCP 對**所有方案開放，包括免費版**（[Buffer 官方公告](https://buffer.com/resources/buffer-api-is-here/)）。API 的 `createPost` 可以帶 `saveToDraft: true`，這樣送進去的貼文「在明確排程前不會發布」（[Buffer API 範例](https://developers.buffer.com/examples/)）。Buffer Free 剛好給 3 個頻道，正好放下你的 Threads、Instagram 專業帳號、YouTube Shorts，所以「Claude 雲端排程寫稿、送進排程器、你在手機上審核」這套流程可以 £0 起步。Buffer Free 的硬限制有四個：每頻道同時只能排 10 則、只有 1 個使用者、正式審核流程要 Team 方案、使用介面只有英文（Android App 例外）。備選 Postiz 的優勢有三個：API 有 `draft` 類型、每則貼文有可留言的公開預覽連結、可以自架。二十個候選裡，Hootsuite、Sprout Social、Agorapulse、Vista Social、Ayrshare 的 API／MCP 方案都要每月 £60 以上，超出預算三倍。Later、SocialBee、SocialPilot 價格合適，卻沒有 Claude 能寫入的 API。Typefully 不支援 IG 和 YouTube。Zernio、Upload-Post 便宜，但查不到草稿狀態，審核關卡要自己做。Metricool 的 MCP 需要哪個方案，各來源互相矛盾。**FB 個人帳號、FB 社團、小紅書在所有工具裡都沒辦法自動發文**，你原本規劃手動處理是對的。本報告延續先前〈AI 社群內容自動化工作流〉的研究，並依 10 月的新資料修正其中幾個判斷，修正處都會註明。

> **可信度說明（付費前必讀）**：這次研究時，**所有廠商官網都無法直接讀取**，包括 buffer.com、developers.buffer.com、postiz.com、metricool.com、publer.com、hootsuite.com、later.com、developers.facebook.com、developers.google.com 等，連線都被網路白名單擋下。所有數字因此來自**搜尋引擎摘要**和**第三方文章**，而很多第三方文章是**競品寫的**，例如 Blotato 寫 Vista Social 和 Later、SocialPilot 寫 Metricool、Upload-Post 寫 Buffer、Socialync 寫 Hootsuite。各來源的價格常互相矛盾，本文會並列不同說法。**所有價格都是美元報價，沒有任何來源給出官方英鎊價或英國 VAT 處理方式。** 換算一律用 1 美元約 £0.75–0.80，這個匯率是估計值，沒有來源。若對個人消費者加收 20% VAT，實付金額要再乘 1.2，這點也**［待查證］**。第五節最後列有一張「付費前必查清單」。

---

## 一、Buffer 補上最後一塊：免費版也能讓 Claude 寫入草稿

先前那份報告說「Buffer MCP 是否支援 Free **［待查證］**」，現在已經有答案。Buffer 在 2026 年 2 月 24 日開放公開測試，5 月 27 日正式推出公開 API、官方 MCP 和 CLI（`@bufferapp/cli`），並明說**每個方案都能用，包括 Free**（[Buffer 官方公告](https://buffer.com/resources/buffer-api-is-here/)、[Buffer 工程師 Diego Castillo](https://x.com/diegocasmo/status/2028553459901861990)）。API 是 `https://api.buffer.com` 的 GraphQL，用個人 API key 當 Bearer token。Free 方案的額度是 **1 把 key、每 15 分鐘 100 次、每 24 小時 250 次、每 30 天 3,000 次**（[Buffer API 限額頁](https://developers.buffer.com/guides/api-limits.html)）。每週送幾十則草稿，連額度的零頭都用不到。要注意，GraphQL 被限流時可能回 HTTP 200，錯誤藏在 `errors` 陣列的 `RATE_LIMIT_EXCEEDED` 裡，腳本要檢查這個欄位，不能只看狀態碼（[professionalstoolkit](https://professionalstoolkit.com/articles/buffer-api)）。

官方 MCP 的端點是 `https://mcp.buffer.com/mcp`。在 claude.ai 用「自訂連接器」加入、OAuth 登入；在 Claude Code 用 `claude mcp add --transport http buffer https://mcp.buffer.com/mcp`（[Buffer MCP 文件](https://developers.buffer.com/guides/integrations/mcp.html)、[usecarly](https://www.usecarly.com/blog/claude-buffer-integration/)）。它**不是唯讀**：工具有 `create_post`、`edit_post`、`delete_post`、`create_idea`，還有可以執行任意 mutation 的 `execute_mutation`。據第三方說法，MCP **沒有留言／收件匣工具**，媒體也只能用網址附加，不能從本機上傳。至於能不能讀數據，Buffer 自己在 Threads 上說可以透過 API／MCP 拉分析（[Buffer Threads 貼文](https://www.threads.com/@buffer/post/DbnpZiKiFsQ/getting-it-out-is-quick-in-buffer-open-insights-hit-export-in-the-top-right/)），usecarly 則說不行，兩邊矛盾。這個設計對你的意義是：**MCP 能做的比「建草稿」多**，所以在無人看管的雲端排程裡，比較安全的做法是不掛 MCP，改用一支寫死 `saveToDraft: true` 的小腳本呼叫 API（見第三節）。

草稿的規則最關鍵。Buffer 說明中心寫明「**草稿所有方案都有，核准草稿只在 Team 方案**」（[Buffer Help: drafts](https://support.buffer.com/article/665-managing-and-approving-draft-posts)）。API 文件寫「存成草稿時**不檢查發文上限**，在明確排程前不會發布」（[Buffer API reference](https://developers.buffer.com/reference.html)）。由此推論，Claude 可以一次堆超過 10 則草稿，只有真正排進佇列的貼文才算進每頻道 10 則的上限。這是推論，第一週要實測。對單人使用來說，Team 的「申請核准 → Approvals 分頁」流程根本用不到：Claude 建草稿，你在網頁或手機 App 打開、修改、按排程，效果一樣。

| Buffer 方案（USD） | 價格 | 3 頻道月費 | 約合 £／月（未含 VAT） | 重點 |
|---|---|---|---|---|
| **Free** | $0 | $0 | **£0** | 3 頻道；每頻道同時 10 則排程（共 30 則）；1 使用者；AI 助理不限次；Community 收件匣（只看連線後的新貼文）；Insights 30 天、無報表；**API 1 把 key**（[Buffer Help](https://support.buffer.com/article/643-how-many-posts-can-i-schedule-in-advance)、[use-apify](https://use-apify.com/blog/buffer-free-plan-guide)、[boomp.net](https://boomp.net/blog/buffer-pricing-free-plan-limits-2026)） |
| Essentials | 每頻道 $6 月繳／$5 年繳 | $18／$15 | £13.5–14.4／£11–12 | 不限歷史數據、報表、匯出；1 使用者（[napoleoncat 2026-10](https://napoleoncat.com/blog/buffer-pricing/)） |
| Team | 每頻道 $12 月繳／$10 年繳 | $36／$30 | £27–29／£22.5–24 | 唯一有審核流程的方案；不限使用者；加 VAT 後月繳會超過 £30（[socialbu](https://socialbu.com/blog/buffer-pricing)） |

頻道支援方面，Buffer 支援 Threads（含串文和長文自動拆段）、Bluesky、Mastodon、X、LinkedIn、TikTok、Pinterest、FB 粉專、Google 商家，**FB 社團只能用「通知」模式**，頻道表裡**沒有 FB 個人帳號**（[Buffer Help: 連接頻道](https://support.buffer.com/en-us/articles/connecting-your-channels-to-buffer-HvWLgAJvL9)、[Buffer Help: 排程貼文](https://support.buffer.com/en-us/articles/scheduling-posts-4Qdld7giAZ)）。Instagram 只能自動發到**專業帳號**，個人帳號「因 API 限制」無法自動發。有音樂、貼圖等 API 不支援的元素時，貼文會改成「Notify Me」，要你在手機上手動點一下（[Buffer Help: Instagram](https://support.buffer.com/en-us/articles/scheduling-instagram-posts-reels-stories-and-notifications-3XA98S9Q5p)）。YouTube Shorts 可以立即發、排進佇列或指定時間（[Buffer: 排程 YouTube Shorts](https://buffer.com/resources/how-to-schedule-youtube-shorts/)）。資料裡找不到 Reddit 和小紅書。另外，Buffer 走的是自己通過審核的 Google App，所以理論上**不會碰到自建 YouTube API 專案的「上傳強制私人」問題**（見第三節）。這是推論。

---

## 二、二十個選項，只有四個同時符合「三平台＋API＋£30」

下面四張表依序是總表、平台支援、價格。圖例：✅ 有來源支持；⚠️ 支援但有條件；❓ 未查到或來源矛盾；❌ 不支援。

### 表 1：總表（以你的情境評分）

| 工具 | 定位 | Threads／IG／YT Shorts | 免費方案 | 能讓 Claude 寫入的最低月費 | 草稿 API | 收件匣 | 數據 | 內建 AI | 中文介面 | 適合你？ |
|---|---|---|---|---|---|---|---|---|---|---|
| **Buffer** | 小型排程器 | ✅／✅（專業帳號）／✅ | ✅ 3 頻道 | **£0** | ✅ `saveToDraft` | ✅ 免費版含 | Free 30 天 | AI 助理 | ⚠️ 僅 Android | **首選** |
| **Postiz Cloud** | 開源排程器（代管） | ✅／✅／✅ | ❌（7 天試用） | 約 £22–23 | ✅ `type: draft` | ❓ | 較不成熟 | ❓ | ❓ | **備選** |
| Postiz 自架 | 開源（AGPL-3.0） | ✅／✅／✅（要自己申請 App） | 授權免費 | VPS 約 £4–20 | ✅ | ❓ | 同上 | ❓ | ❓ | 時間成本高 |
| Metricool | 排程＋數據 | ✅／✅／✅ | ✅ 1 品牌 20 則／月 | £0 或約 £40（矛盾） | ❓ | ❓ | Free 30 天 | 5 點／月 | ❓ | 待查清 MCP 方案 |
| Publer | 小型排程器 | ✅／✅／⚠️ 推測有 | ✅ 3 帳號 | 約 £16–24（Business） | ❓ | ❓ | Business 才完整 | Business 不限 | ❓ | 預算上緣 |
| Zernio（原 Late） | 發文 API | ✅／✅／✅ | 前 2 帳號免費 | 約 £5 | ❓ | 有訊息類工具 | 有 | ❌ | 無介面 | 審核要自建 |
| Upload-Post | 發文 API | ✅／✅／✅ | ✅ 10 則／月 | 約 £12–19 | ❓ | ❓ | ❓ | ❓ | ❓ | 原型可用 |
| bundle.social | 發文 API | ❓ | ✅ 約 20 則／月 | 免費版或 £75+ | ❓ | ❓ | ❓ | ❌ | ❓ | 只能用免費版 |
| Blotato | AI 內容＋發文 | ✅／✅／✅ | ❌ | 約 £22–23 | ❓ | ❓ | 不含 LinkedIn | 1,250 點 | ❓ | AI 功能多餘 |
| Typefully | 文字串文 | ✅／❌／❌ | ✅ 10 則／月 | £0 | ✅ | ❌ | 有 | 有 | ❓ | 平台不足 |
| Later | 視覺排程 | ✅／✅／✅（僅 Shorts） | ❓ 有隱藏免費版的說法 | 無 API | ❌ | ❓ | 約 3 個月 | 5 點／月 | ❓ | 無法自動化 |
| SocialBee | 常青內容循環 | ⚠️ 矛盾／❓／✅ | ❌ | 無 API | ❌ | ✅ | 3 個月 | ❓ | ❓ | 無法自動化 |
| SocialPilot | 小型排程器 | ✅／❓／❓ | ❌ | 只有 Zapier | ❌ | ❓ | 基本 | ✅ | ❓ | 無法自動化 |
| Hootsuite | 企業套件 | ✅／✅／⚠️ Shorts 未確認 | ❌ | 約 £74–89 | ✅（Perch MCP） | ✅ Nest | ✅ | Wisdom | ❓ | 超預算 |
| Sprout Social | 企業套件 | ✅／✅／✅ | ❌ | 約 £300（Advanced） | ✅（API） | ✅ Smart Inbox | 進階分析要加購 | ✅ | ❓ | 超預算 |
| Agorapulse | 企業套件 | ❓／✅／✅ | ❌ 2026-07 取消 | 約 £59–79 | ✅（MCP 只建草稿） | ✅ | ✅ | Archie | ❓ | 超預算 |
| Vista Social | 中階套件 | ✅／✅／❓ | ❓ 矛盾 | 約 £59–79 | ❓ | ❓ | ✅ | ✅ | ❓ | 超預算 |
| Ayrshare | 發文 API | ❓ | ❌ | 約 £112–119 | ❓ | ❓ | ❓ | ❌ | 無介面 | 超預算 |
| Meta Business Suite | 官方免費 | ❓ 矛盾／✅（需粉專）／❌ | ✅ | 無 API | ❌ | ✅（FB／IG） | ✅ | ✅ | ✅ | 只能手動用 |
| 原生排程＋官方 API | 各平台 | ✅／✅／✅ | ✅ | £0＋自己寫程式 | 自建 | 各 App 內 | 各 App 內 | ❌ | ✅ | 最後手段 |

### 表 2：平台支援

| 工具 | Threads | IG 專業帳號 | FB 粉專 | FB 個人 | FB 社團 | YT Shorts | Bluesky | LinkedIn | X | Reddit | 小紅書 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Buffer | ✅ 含串文 | ⚠️ 有音樂或貼圖時改 Notify Me | ✅ | ❌ | ⚠️ 僅通知 | ✅ | ✅（App 密碼） | ✅ | ✅ | ❌ | ❌ |
| Postiz | ✅（自架要自建 Meta App） | ✅（不需 FB 粉專） | ✅ | ❌ | ❌ | ✅ | ✅ | ❓ 宣稱 30+ 平台 | ❓ | ❓ | ❌ |
| Metricool | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ Starter 起 | ⚠️ Free 無 | ❓ | ❌ |
| Publer | ✅ 最多 25 則串文 | ✅ Reels／Stories | ✅ | ❌ | ❌ | ⚠️ 文件路徑有 Shorts | ✅ | ❓ | ⚠️ Free 無 | ❓ | ❌ |
| SocialBee | ⚠️ 官方頁面互相矛盾 | ❓ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❓ | ❌ |
| SocialPilot | ✅ | ❓ | ❓ | ❌ | ❌ | ❓ | ✅（300 字） | ❓ | ❓ | ❓ | ❌ |
| Vista Social | ✅ | ✅ | ✅ | ❌ | ❌ | ❓ | ✅ | ✅ | ⚠️ 每月加 $29 | ✅ | ❌ |
| Later | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ 只有 Shorts | ❌ | ✅ | ❓ 未列 | ❓ | ❌ |
| Hootsuite | ✅ | ✅ | ✅ | ❌ | ❌ | ⚠️ YouTube 有，Shorts 未確認 | ❓ 矛盾 | ✅ | ✅ | ❓ | ❌ |
| Sprout Social | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ⚠️ 僅桌面版 | ❌ |
| Agorapulse | ❓ API 有列出 | ✅ Reels 限原聲 | ✅ | ❌ | ❌ | ✅ 自動判定 | ✅ | ✅ | ✅ | ❓ | ❌ |
| Typefully | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Blotato | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Zernio | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ❓ | ✅ | ✅ 費用轉嫁 | ❓ | ❌ |
| Upload-Post | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Meta Business Suite | ❓ 2026-04 起可能有 | ✅（需連結粉專） | ✅ | ❌ | ⚠️ 限同一商家組合 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 官方 API 自寫 | ✅ 每 24 小時 250 則 | ✅ 每 24 小時 100 則 | ✅ | ❌ | ❌ 2024 年移除 | ⚠️ 未驗證專案會被鎖私人 | ✅ | ✅ | 付費 | 需人工核准 | ❌ 無公開 API |

來源：Buffer 見第一節；Postiz（[Mintlify 文件鏡像](https://www.mintlify.com/gitroomhq/postiz-app)、[r/selfhosted 2025-01](https://redlib.hackliberty.org/r/selfhosted/comments/1i5qnzq/postiz_v1281_opensource_social_media_scheduling/m874qc6/?context=3)）；Metricool（[hyperplanners](https://hyperplanners.com/metricool-review/)、[PostPlanify](https://postplanify.com/metricool-pricing)）；Publer（[Publer 串文說明](https://help.publer.io/en/article/how-to-schedule-poststhreads-to-the-threads-app-4yjmqd)、[Publer Reels 文件](https://publer.com/docs/create-posts/content-types/platform-specific-formats/reels-shorts-and-stories)）；SocialBee（[SocialBee 說明中心](https://help.socialbee.com/article/110-how-can-i-add-an-account)）；Vista Social（[Fastlancer](https://www.fastlancer.org/en/fastlancer-blog/vistasocial-review/)）；Later（[Later 說明中心](https://help.later.com/hc/en-us/articles/360060842914-Supported-Social-Platforms-Post-Types)）；Hootsuite（[Hootsuite FAQ](https://www.hootsuite.com/faq)、[modelranked](https://modelranked.com/social-media-management/hootsuite-review/)）；Sprout（[Sprout 說明中心](https://support.sproutsocial.com/hc/en-us/articles/115005707863-What-social-profiles-can-I-connect-to-Sprout)）；Agorapulse（[Agorapulse API 限制](https://support.agorapulse.com/en/articles/8712660-api-limitations-per-network)）；Typefully（[Typefully v2 遷移指南](https://support.typefully.com/en/articles/13133296-typefully-api-v1-v2-migration-guide)）；Blotato（[Blotato API](https://www.blotato.com/social-media-api)）；Zernio（[dupple](https://dupple.com/tools/zernio)）；Upload-Post（[Upload-Post FAQ（廠商）](https://www.upload-post.com/postiz-alternative/)）。

有三列在所有工具裡都一樣，原因出在平台，不在工具。**FB 社團**：Meta 在 2024 年 4 月 22 日移除了 Groups API，包括 `publish_to_groups` 權限，排程器最多只能做提醒（[Sprinklr](https://www.sprinklr.com/help/articles/getting-started-facebook/meta-deprecates-facebook-groups-api/66229eb25f9dd9599d632712)、[groupposting](https://groupposting.com/group-posting/facebook-groups-api/)）。**FB 個人帳號**：Graph API 只能發到粉專（`pages_manage_posts`），「不能發到個人檔案或社團」（[Upload-Post Graph API 指南](https://www.upload-post.com/facebook-graph-api/)）。**小紅書**：沒有可驗證的官方公開發文 API，只有網頁版「創作服務平台」可以手動發布和定時發布（[ai-bot.cn](https://ai-bot.cn/sites/77134.html)、[Phyllo](https://www.getphyllo.com/rednote-api)）。市面上的 `xiaohongshu-mcp` 一類工具都靠 cookie 操控瀏覽器，而小紅書 2026 年 3 月 10 日起會**封禁**透過 AI 託管工具發文的帳號（[光明網](https://m.gmw.cn/2026-03/10/content_1304371172.htm)）。所以 FB 個人帳號和小紅書手動處理是唯一安全的選項。Claude 可以照樣幫你寫好文案和圖，放在 repo 的手動佇列資料夾裡。

Meta 自家工具也幫不上忙。Business Suite 以 FB 粉專為核心，IG 必須連到粉專才能在那裡排程（[PostOtter](https://postotter.app/blog/meta-business-suite-instagram-scheduling)）。你只有個人帳號，要先另開一個粉專才用得到。Business Suite 能不能排 Threads，目前唯一說「2026 年 4 月底起桌面版可以」的來源，是 Meta AI 帳號在 Threads 上的聊天回覆，不是官方公告（[threads.com @meta.ai](https://www.threads.com/@meta.ai/post/DY46kNqkZD2)），其他 2026 年的指南都說不行（[DEV](https://dev.to/ppcvote/how-to-schedule-threads-posts-set-up-daily-auto-posting-in-5-minutes-1h0f)）。Threads 自 2025 年 1 月起有內建排程，可存 100 則草稿（[Social Media Today](https://www.socialmediatoday.com/news/threads-announces-analytics-adds-draft-scheduling/724428/)、[Sprout Social](https://sproutsocial.com/insights/schedule-threads-posts/)）。IG 內建排程可以排到 75 天後（[Social Media Today](https://www.socialmediatoday.com/news/Instagram-Rolls-Out-In-App-Post-Scheduling-Tools/635987/)）。YouTube Studio 可以排 Shorts（[SocialBu](https://socialbu.com/blog/schedule-youtube-videos-and-shorts)）。這些原生排程**都沒有 API**，Claude 碰不到，只能當人工備援。

### 表 3：價格（USD 報價；英鎊以 0.75–0.80 換算，未含 VAT）

| 工具 | 免費方案內容 | 最便宜付費方案 | 你的 3 頻道月費 | 約合 £／月 | 有 API／MCP 的方案 | ≤ £30？ |
|---|---|---|---|---|---|---|
| **Buffer** | 3 頻道、每頻道 10 則排程、API 1 把 key | Essentials 每頻道 $5–6 | **$0**（Free） | **£0** | 全方案 | ✅ |
| **Postiz Cloud** | 無（7 天試用） | Standard $29（5 頻道）；年繳 $278 | $29（年繳約 $23.2） | £22–23（年繳 £17–19） | 全方案（[Postiz 方案](https://docs.postiz.com/cloud/plans)） | ✅ |
| Postiz 自架 | 授權免費 | VPS 建議 4 GB | VPS 約 $5–25 | 約 £4–20 | 內建 | ✅ |
| Metricool | 1 品牌、每月 20 則、30 天數據（[Metricool 官方說明](https://help.metricool.com/es/main-differences-between-free-and-paid-plans-bl0v9)） | Starter $20 年繳／$25 月繳（5 品牌） | $0–25 | £0–20 | API 要 Advanced $53；MCP 方案說法矛盾 | ⚠️ |
| Publer | 3 帳號、每帳號 10 則、無 X | Business：每帳號 $8–10，或 3 帳號 $21 | $21–30 | £16–24 | Business 有 API；MCP 測試中，不對一般用戶開放 | ⚠️ 上緣 |
| SocialBee | 無（14 天試用） | Bootstrap $29／年繳 $24.20（5 帳號） | $24–29 | £18–23 | 未找到 | ❌ 無 API |
| SocialPilot | 無（14 天試用） | Essentials $20–30（矛盾） | $20–30 | £15–24 | 只有 Zapier | ❌ 無 API |
| Later | 有隱藏免費版的說法（Blotato） | Starter $18.75 年繳／$25 月繳 | $19–25 | £14–20 | 無 | ❌ 無 API |
| Typefully | 每月 10 則，含 API／MCP | Creator $99／年 | $0 | £0 | 免費版即有（[Postel](https://www.postel.app/typefully-pricing)） | ❌ 無 IG／YT |
| Blotato | 無（試用不含 API） | Starter $29 | $29 | £22–23 | 付費才有（[PlugKit](https://www.plugkit.co/blog/blotato-pricing-api-alternatives/)） | ✅ 價格可，不推薦 |
| Zernio | 前 2 帳號免費 | 第 3–10 帳號每個 $6 | $6 | 約 £5 | 有（[hypertools](https://hypertools.so/tool/zernio)） | ✅ 價格可 |
| Upload-Post | 2 profiles、每月 10 則 | Basic $16 年繳／$24 月繳 | $0–24 | £0–19 | 全方案（廠商說法） | ✅ |
| bundle.social | 每月約 20 則，含 API | Pro $100 | $0 或 $100 | £0 或 £75–80 | 全方案（[bundle.social](https://bundle.social/)） | ⚠️ 只有免費版 |
| Hootsuite | 無（14 天試用） | Standard $99／人（英國評測稱 £89） | $99 | £74–89 | MCP 適用方案未公布 | ❌ |
| Sprout Social | 無 | Essentials $79 年繳／$99 月繳 | $79–99 | £59–79 | API 要 Advanced $399 | ❌ |
| Agorapulse | 2026-07-06 取消（30 天試用） | Standard $79 年繳／$99 月繳 | $79–99 | £59–79 | MCP 測試版限付費方案 | ❌ |
| Vista Social | 說法矛盾 | Professional $79–99；X 另加 $29 | $79–99 | £59–79 | MCP 方案說法矛盾 | ❌ |
| Ayrshare | 無 | Premium $149 | $149 | £112–119 | 付費 | ❌ |
| Meta 原生／官方 API | 全免費 | — | $0 | £0 | 官方 API 免費、自己寫 | ✅ 但要自建 |

價格來源：Hootsuite（[lilachbullock](https://www.lilachbullock.com/hootsuite-pricing/)、[ukbusinesssoftware](https://ukbusinesssoftware.co.uk/hootsuite-review-uk-2026-2/)）；Sprout（[eesel.ai](https://www.eesel.ai/blog/sprout-social-pricing)、[socialcrawl](https://www.socialcrawl.dev/blog/sprout-social-pricing)）；Agorapulse（[napoleoncat](https://napoleoncat.com/blog/agorapulse-pricing/)）；Later（[socialpilot（競品）](https://www.socialpilot.co/insights/later-pricing)、[blotato（競品）](https://www.blotato.com/blog/later-pricing)）；Metricool（[SocialPilot（競品）](https://www.socialpilot.co/insights/metricool-pricing)）；Publer（[SocialK.it](https://socialk.it/en/pricing/publer)、[G2](https://www.g2.com/products/publer/pricing)）；SocialBee（[PostPlanify](https://postplanify.com/socialbee-pricing)）；SocialPilot（[PostPlanify](https://postplanify.com/socialpilot-pricing)）；Vista（[Costbench](https://costbench.com/software/social-media-management/vista-social/free-plan/)、[Socialync（競品）](https://www.socialync.io/compare/vista-social)）；Upload-Post（[Blotato（競品）](https://www.blotato.com/blog/upload-post-pricing)）；Ayrshare（[social-api.ai（競品）](https://social-api.ai/blog/ayrshare-pricing-social-media-api-2026)）；Postiz 自架 VPS（[OSSAlt](https://ossalt.com/guides/self-host-postiz-2026)、[Railway 範本](https://railway.com/deploy/postiz-self-hosted-buffer-alternative-for-30-platforms--postiz-social-scheduler)）。

這張表的結論很直接：**同時符合 £30 預算、能讓 Claude 寫入、涵蓋 Threads／IG／YT 三個平台的，只有 Buffer、Postiz（雲端或自架）、Zernio、Upload-Post 四個**。Publer Business 和 Metricool 在邊緣，要看英鎊實價和 MCP 開放範圍。

---

## 三、能讓 Claude 寫入的工具很多，能保證「只建草稿」的很少

你的要求是「人只做審核」。所以要問的不只是「Claude 能不能寫進去」，還有「Claude **只能**建草稿嗎」。有些 MCP 在設計上就只能建草稿：Hootsuite Perch、Agorapulse、Sprout API 都是，但都超預算。預算內的工具，草稿限制都要靠你自己加：同一把 key 或同一個 MCP 也能直接排程，甚至立刻發布。

### 表 4：API／MCP 與 Claude 整合

| 工具 | 公開 API（所需方案） | 官方 MCP（端點／驗證） | API 能建草稿？ | Claude 雲端排程可行性 | 備註 |
|---|---|---|---|---|---|
| **Buffer** | GraphQL，**全方案含 Free**；Free 每 30 天 3,000 次 | `mcp.buffer.com/mcp`，OAuth；另有 CLI | ✅ `saveToDraft: true` | ✅ 用環境密鑰存 API key 直接呼叫最穩 | MCP 有 `delete_post`、`execute_mutation`；沒有收件匣工具；媒體只能給網址（[Buffer MCP 文件](https://developers.buffer.com/guides/integrations/mcp.html)） |
| **Postiz** | REST，全雲端方案；每小時 90–100 次（另有 30 次的舊說法） | 雲端 `mcp.postiz.com/mcp-oauth-dynamic`；自架有 `/mcp`、`/mcp/:apiKey`、`/mcp-oauth` | ✅ `type: draft` | ✅ | 重新產生 API key 會讓所有 MCP 連線失效（[Postiz API](https://docs.postiz.com/public-api/introduction)、[postiz.com/claude-code](https://postiz.com/claude-code)、[lobehub](https://lobehub.com/mcp/antoniolg-postiz-mcp)） |
| Metricool | 要 Advanced（約 $53） | `mcp-metricool`（PyPI）；官方 README 寫要 Advanced，其他來源說 Free 也能用 | ❓（有 `post_schedule_post`） | ⚠️ 看方案 | [Glama README 鏡像](https://glama.ai/mcp/servers/@metricool/mcp-metricool/blob/0d2346e07f6b7555e0a2ebc7698898583c37e27f/README.md) vs [PricingSaaS](https://pricingsaas.com/companies/metricool) |
| Publer | Business | 測試中，只開放 Top Ambassadors 和企業客戶；API key 可設權限範圍 | ❓ | ⚠️ 用 REST | [Publer MCP 說明](https://publer.com/help/en/article/how-to-set-up-and-use-publers-mcp-server-14orlq0/)；另有社群版 MCP |
| Typefully | v2，免費版即有 | `mcp.typefully.com/mcp`（OAuth 或 key，說法矛盾） | ✅ 以草稿為核心 | ✅ 但只有文字平台 | [Pallyy](https://pallyy.com/blog/social-media-mcp-servers) |
| Blotato | 付費 | `mcp.blotato.com/mcp`；工具數 35 或 13，官方頁面矛盾 | ❓ | ✅ | 自訂每日上限比平台嚴（IG 50 則）（[Blotato MCP](https://www.blotato.com/mcp)） |
| Zernio | 依帳號數計費 | `mcp.zernio.com`，OAuth／Bearer；號稱 496 個工具 | ❓ | ✅ 但工具太多會塞滿 context | [Socialync](https://www.socialync.io/mcp-server/zernio) |
| Upload-Post | 全方案 | 約 40 個工具，全方案 | ❓ | ✅ | 資料多來自廠商（[Upload-Post MCP](https://www.upload-post.com/mcp)） |
| bundle.social | 免費版即有 | 本機執行＋API key；代管版在規劃中 | ❓ | ⚠️ | [That Marketing Buddy](https://thatmarketingbuddy.com/software/bundle-social) |
| Ayrshare | $149 起 | 唯讀文件 MCP 免費；Action MCP 付費 | ❓ | ✅ 但超預算 | [PlanVortex](https://planvortex.com/en/resources/ayrshare-mcp-server) |
| Hootsuite | 有開發者 API | Perch：`mcp.hootsuite.com/perch`，OAuth，以草稿為主 | ✅ | ✅ 但約 £75+ | 適用方案未公布（[Hootsuite 部落格](https://blog.hootsuite.com/post-on-social-media-from-claude/)） |
| Agorapulse | 分析 API 唯讀，限企業方案 | `api.openmcp.agorapulse.com/mcp`，測試版，**只建草稿** | ✅ | ✅ 但約 £60+ | [Agorapulse MCP](https://support.agorapulse.com/en/articles/12960496-model-context-protocool-mcp-integration-explained) |
| Sprout Social | Advanced（$399／人）才有，可建草稿 | 只支援 ChatGPT，範圍限 TikTok 數據 | ✅ | ❌ | [Sprout ChatGPT 整合](https://support.sproutsocial.com/hc/en-us/articles/41085761844365-ChatGPT-Integration-Overview-and-Setup) |
| Vista Social | 要洽業務 | `mcp.vistasocial.com/mcp`，方案說法矛盾 | ❓ | ⚠️ | [Blotato（競品）](https://www.blotato.com/blog/blotato-vs-vista-social) |
| Later／SocialBee | ❌ | ❌ | — | ❌ | [dev.to MCP 比較](https://dev.to/olver_thorarinsson_bcf885/which-social-media-schedulers-support-mcp-every-tool-compared-2026-e87) |
| SocialPilot | 只有客製方案 | 透過 Zapier（有「Approve Post」動作） | — | ⚠️ 要另付 Zapier | [Zapier SocialPilot](https://zapier.com/help/socialpilot/) |
| Threads 官方 API | 免費；自己的帳號用測試者身分即可，不需 App Review | 無官方 MCP | 沒有排程參數，要自己跑 cron | ⚠️ 長效 token 60 天要續期 | [Meta Threads 發文](https://developers.facebook.com/docs/threads/create-posts)、[pete-builds/mcp-threads](https://github.com/pete-builds/mcp-threads) |
| IG 官方 API | 免費；需專業帳號；媒體要放在公開網址 | 無 | 沒有排程參數 | ⚠️ | [Meta 內容發布文件](https://developers.facebook.com/docs/instagram-platform/content-publishing/) |
| YouTube Data API | 免費，靠配額限制 | 無 | 未驗證專案上傳後**強制私人** | ⚠️ 私人鎖反而可以當審核關卡 | [videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert) |

### 表 5：草稿與審核流程

| 工具 | 草稿 | 正式審核流程 | 手機上審核 | 怎麼確保 Claude「只建草稿」 |
|---|---|---|---|---|
| **Buffer** | 全方案 | 只有 Team（約 $30–36／月） | App 有草稿分頁；Team 方案顯示「Approve and Schedule」（[Buffer 手機草稿](https://support.buffer.com/articles/creating-managing-and-approving-draft-posts-on-the-buffer-mobile-app-XSRim1JeUl)） | 寫一支只會送 `saveToDraft: true` 的腳本；雲端排程不掛官方 MCP |
| **Postiz** | `type: draft` | 沒有會擋住發布的「已核准」旗標；預覽連結可以留言 | 網頁 UI | 腳本寫死 `type: "draft"`；**預覽連結沒有密碼**，等同「不公開但可分享」（[Postiz Approvals](https://docs.postiz.com/general/approvals)） |
| Hootsuite | 有 | Advanced 才有 | App | Perch MCP 以草稿為主 |
| Agorapulse | 有 | 有 | App | **MCP 本身只能建草稿**，結構上最安全 |
| Sprout Social | API 建草稿 | 有 | App | API 本身不能代發 |
| SocialPilot | 有 | Premium $85 起 | App | Zapier 的「Approve Post」動作 |
| Publer | Free 可存 25 則草稿 | ❓ | App | API key 可設權限範圍，能不能只給建草稿權限 **［待查證］** |
| Typefully | 以草稿為核心 | — | App | MCP 能建草稿，也能排程 |
| Zernio／Upload-Post／bundle.social／Blotato | 未確認有 API 層級的草稿 | ❌ | ❌ 無介面或介面有限 | 只能自建：Claude 把候選稿寫進 repo，你核准後再由第二次執行發布 |
| 原生排程 | Threads 可存 100 則草稿 | — | ✅ | YouTube 私人上傳後，由你在 Studio 設定公開時間 |

安全設計要分兩層。第一層是**工具權限**：官方 MCP 對寫入工具通常會跳出確認（[Buffer MCP 文件](https://developers.buffer.com/guides/integrations/mcp.html)），但 Claude 雲端排程是無人值守的，沒人按確認，所以應該只給代理一支寫死草稿參數的腳本。Buffer 的 API key 能不能限縮權限，本次沒有查到，所以要假設 key 本身有完整權限，**要靠「代理只知道這支腳本」和 repo 規則來約束**，不能只靠 key 本身。第二層是**輸入隔離**：先前報告建議過，讀留言和發文的工具不要放在同一個代理裡，避免留言內容透過提示注入操控代理。Buffer MCP 本來就沒有收件匣工具，對這一點反而有利。

直接打官方 API 能省訂閱費，但成本會轉到維運上。Threads API 沒有「排程」參數，要自己跑 cron 準時呼叫發布（[ultralab 教學](https://ultralab.tw/en/blog/threads-api-auto-post-tutorial-2026)）。長效 token 60 天到期，過期就失效，只能在到期前續期（[pete-builds/mcp-threads](https://github.com/pete-builds/mcp-threads)）。IG 媒體必須先放到公開網址。YouTube 方面，2020 年 7 月 28 日之後建立、未經稽核的 API 專案，上傳的影片一律鎖成私人（[videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert)、[clipember](https://clipember.com/guides/youtube-upload-comes-out-private)）。先前報告把這點列為 ［待查證］，這次有多個第三方來源佐證，但仍要上官方頁確認。上傳配額有好幾種互相矛盾的說法，但不管哪一種，每天 1–3 支 Shorts 都夠用（[outlierkit](https://outlierkit.com/resources/youtube-api-quota/)）。這條路最適合拿來補 Buffer 不足的地方，例如之後想把 YouTube 拿出 Buffer、改成「私人上傳＝待審」，不適合當主幹。

---

## 四、收件匣、數據、AI、中文介面與可靠性：差異沒有價格大

**留言收件匣**方面，Buffer 在你的預算內最完整。Buffer Community 免費版就有，可以回覆 Threads、IG 專業帳號、YouTube、Bluesky、X、FB 粉專、LinkedIn、TikTok 等平台的留言，手機 App 也能用（[Buffer Help: Community](https://support.buffer.com/article/977-how-comments-work-across-each-social-network-in-buffer-community)、[Buffer 手機 Community](https://support.buffer.com/en-us/articles/using-community-on-the-buffer-mobile-app-mCNla9C1We)）。限制是免費版**只看得到連線之後新貼文的留言**（[boomp.net](https://boomp.net/blog/buffer-pricing-free-plan-limits-2026)）。SocialBee 的收件匣涵蓋 FB、X、IG、Threads、LinkedIn、YouTube（[SocialBee 功能頁](https://socialbee.com/social-media-management-tool/)），但它沒有 API。Hootsuite 的 Nest 和 Sprout 的 Smart Inbox 都在 £60 以上的方案。Postiz、Zernio、Upload-Post 的收件匣能力沒查到。照先前報告的原則，**回留言一律你本人來**，所以收件匣的價值在於「一個 App 看三個平台」，不在自動化。

**數據**方面，Buffer Free 只有最近 7 天、30 天、本月三種範圍，沒有報表。CSV／PDF 匯出是付費功能（[Buffer Help: Insights](https://support.buffer.com/article/950-using-insights-in-buffer)），但 Buffer 自己的 Threads 貼文又說 CSV 匯出全方案免費，兩邊矛盾（[Buffer Threads](https://www.threads.com/@buffer/post/DbnpZiKiFsQ/getting-it-out-is-quick-in-buffer-open-insights-hit-export-in-the-top-right/)）。Metricool Free 同樣是 30 天，Metricool 本來就以數據見長。對三個個人專案來說，真正的轉換指標是 GitHub Star、遊戲遊玩次數、11+ 產品的註冊數，這些都不在排程器裡，所以數據功能不該是選工具的理由。**AI 功能**也一樣：Buffer AI 助理免費不限次、Blotato 有 1,250 點、Later 每月 5 點、Hootsuite 有 Wisdom、Agorapulse 有 Archie，但你的文案由 Claude 寫，這些功能大多用不到。Blotato 尤其如此，它的價值主要在 AI 生成，對你等於是花 $29 買一個發文 API。

**中文介面與英國使用**：Buffer 網頁版和 iOS **只有英文**，Android App 9.4.0 以上有中文（[Buffer Help: 介面語言](https://support.buffer.com/en-us/articles/can-i-use-buffer-in-another-language-wetiyDOiI4)、[Buffer Help: 手機 App 語言](https://support.buffer.com/article/638-using-the-buffer-mobile-app-in-another-language)）。其他工具都沒有找到繁中介面的證據。你是工程師，英文介面不是障礙；貼文內容用中文只是 Unicode，理論上沒問題，但 X 和 Threads 的 CJK 字數計算要實測。英國使用方面，沒有任何工具有地區限制，但**全部以美元報價**。目前只有一篇英國評測給過 Hootsuite 的英鎊價（£89／人／月）（[ukbusinesssoftware](https://ukbusinesssoftware.co.uk/hootsuite-review-uk-2026-2/)），可見部分廠商對英國顯示英鎊，換算和 VAT 要以結帳頁為準。

**可靠性**沒有好的量化資料：沒找到 2026 年的停機紀錄，也沒找到可信的評分平均。Buffer 的評價一致稱讚「簡單、便宜、多數格式可靠」（[goodfirms](https://www.goodfirms.co/software/buffer?page=2)）。抱怨集中在 IG 和 LinkedIn 要反覆重新授權、偶爾無聲失敗或重複發文、客服慢（[softwareadvice](https://www.softwareadvice.com/marketing/buffer-profile/reviews/)、[Capterra](https://www.capterra.com/p/143492/Buffer/)），問題多半出在 Meta API。Metricool 的 Trustpilot 評分有 3.9／5（615 則）和 4.2／5（519 則）兩種說法，抱怨集中在帳單、發文卡住和客服（[PostPlanify](https://postplanify.com/metricool-reviews)）。SocialPilot 被指批次排程偶爾無聲失敗（[PostPlanify](https://postplanify.com/socialpilot-reviews)）。G2 使用者認為 Publer 客服比 Metricool 可靠（[G2](https://www.g2.com/compare/publer-vs-metricool)）。Postiz 自架有人用了一年很滿意（[Product Hunt](https://www.producthunt.com/p/postiz/postiz-2?page=2)），但官方 Threads 文件自己寫「Threads API 似乎有問題」，並把使用者導向 Discord（[Postiz Threads 文件](https://docs.postiz.com/providers/threads)）。v2.12 起還必須跑 Temporal，維運複雜度明顯上升（[DEV 除錯手冊](https://dev.to/klytron/debugging-postiz-temporal-a-production-runbook-for-self-hosted-social-media-orchestration-560f)）。

### 各工具的限制與陷阱

| 工具 | 主要陷阱 |
|---|---|
| Buffer | 每頻道同時只能排 10 則；有音樂的 Reels 會改成 Notify Me；媒體要放公開網址；審核流程要 Team；有一篇部落格說 Free 終身只能連 8 個不同頻道（單一來源，[Marc Andrews](https://marcandrews.com/?p=2565)），**別隨便斷開重連** |
| Postiz | 沒有會擋住發布的核准旗標；預覽連結不需登入；自架要自建 Meta、Google App，記憶體建議 4 GB（[Postiz 系統需求](https://docs.postiz.com/self-host/installation/system-requirements)）；Standard 是否有每月 400 則上限有爭議 |
| Metricool | MCP 到底要 Free 還是 Advanced（$53）各說各話；Free 每月 20 則對 3 專案 × 3 平台太少 |
| Publer | 兩種計價模式並存；官方 MCP 不對一般用戶開放；有 API 的方案要 Business |
| Later | 沒有 API；多一個使用者就要升級；額外 social set 另計 |
| Hootsuite | 2026-06-24 改版為「Social OS」多 App 架構，部分功能上線時還寫著「即將推出」（[smartkeys](https://smartkeys.org/hootsuite-review/)） |
| Agorapulse | 免費版 2026-07-06 取消；每加一個使用者就是全價 |
| Vista Social | X 每月另加 $29；MCP 適用方案連官方頁面都互相矛盾 |
| Zernio | 號稱 496 個工具的 MCP 會塞滿 context；沒有日曆 UI |
| 官方 API | Threads、IG 沒有排程參數；Meta token 60 天到期；YouTube 私人鎖；Meta 會改權限名稱（IG 發文權限 2025-01-27 改名，[postzen](https://www.postzen.dev/blog/instagram-api-integration-guide)） |
| 小紅書 | 沒有 API；AI 託管會被封號；台灣 2025 年 12 月起封鎖約一年（[NOWnews](https://www.nownews.com/news/6761411)）。你在倫敦不受影響，但台灣受眾可能看不到 |

---

## 五、推薦：Buffer Free 首選、Postiz Cloud 備選，其餘為何排除

**首選：Buffer Free＋GraphQL API（只建草稿）＋Claude 雲端排程。** 理由有四個：唯一 £0 又官方支援 API 寫入的工具；剛好 3 個頻道放 Threads、IG、YouTube；Buffer 的 YouTube 和 Meta 整合省掉你自己申請開發者 App、處理私人鎖和 60 天 token；免費版附帶三平台合一的留言收件匣。前提是你用**一組個人帳號經營三個專案**，以「做三個專案的工程師」身分發文。這是本報告的判斷，沒有來源。用這種方式，有正職的人只要經營一組帳號，三個專案可以互相導流。英國 11+ 家長和台灣開源社群的受眾差異很大，你可以靠語言和主題分流，不必拆帳號。超過 10 則排程上限時，Essentials 3 頻道月繳 $18，約 £14。

**備選：Postiz Cloud Standard（$29，約 £22–23；年繳約 £17–19）。** 適用三種情況：Buffer 的 API 實測下來做不到 IG Reels、輪播或 Threads 串文；你想要可以留言的預覽連結；或你想之後改成自架。如果你**堅持每個專案各開一組帳號**（3 專案 × 3 平台 = 9 個頻道），預算內的排序會變：Buffer Essentials 9 頻道月繳約 $54（£40+），超出預算；Zernio 約 $42，也超出；**Postiz Team 年繳 $374（約 $31／月，£23–25）有 10 個頻道**，是唯一放得下的選項，但加上 VAT 會逼近 £30。

**DIY 備援：官方 API 只用在單一平台。** 例如 Buffer 的 YouTube 不穩時，改成 Claude 用 YouTube Data API 私人上傳、你在 Studio 設定公開，把私人鎖當成審核關卡。

### 表 6：排除理由

| 工具 | 排除理由 |
|---|---|
| Hootsuite、Sprout Social、Agorapulse、Vista Social、Ayrshare | 有 API／MCP 的方案每月約 £59–119（Sprout API 約 £300），是預算的 2–10 倍；Agorapulse 的草稿專用 MCP 設計最好，但價格不合 |
| Later、SocialBee、SocialPilot | 價格合適，但沒有可以讓 Claude 寫入的公開 API（SocialPilot 只能透過 Zapier，還要另付錢） |
| Metricool | 官方 README 寫 MCP 要 Advanced（約 £40+）；就算 Free 真的開放，每月 20 則也不夠。適合當觀察名單：若官方頁確認 Free／Starter 可用 MCP，它會是有力的第三選擇 |
| Publer | Business 落在預算上緣，官方 MCP 不對一般用戶開放，計價模式還不清楚；功能和 Buffer 重疊但更貴 |
| Typefully | 不支援 IG 和 YouTube；只適合當 Threads／X 純文字的免費補充 |
| Blotato | $29 的價值主要在 AI 生成，Claude 已經在寫稿；查不到 API 層級的草稿狀態 |
| Zernio、Upload-Post、bundle.social | 便宜或免費，但查不到草稿狀態，也沒有完整的審核 UI，審核關卡要自建；Upload-Post 免費版每月 10 則可以拿來做原型 |
| Postiz 自架 | 要自建 Meta、Google App，跑 Temporal、4 GB VPS，還要讓 Claude 雲端能透過公開 HTTPS 連到；有正職的人花在這上面的時間，比每月 £23 貴 |
| Meta Business Suite、原生排程 | 沒有 API，Claude 送不進去；只當手動備援 |

### 表 7：一次性設定步驟（Buffer 首選方案）

| 步驟 | 做什麼 | 注意 |
|---|---|---|
| 1 | IG 切換成創作者或商業帳號（免費）；確認 Threads 連的是同一個 IG；確認 YouTube 頻道可以上傳 Shorts | IG API 是否支援創作者帳號，來源有矛盾，若發文失敗就改成商業帳號 |
| 2 | 註冊 Buffer Free，連接 Threads、Instagram、YouTube 三個頻道 | 連好就別斷開重連（可能有 8 次終身上限，未證實） |
| 3 | 在 Buffer 設定的 Integrations 頁（publish.buffer.com/settings/integrations）建立 API key | Free 只有 1 把，不要外流；存成 Claude 雲端環境的密鑰，例如 `BUFFER_API_KEY` |
| 4 | Claude 雲端環境的網路白名單加入 `api.buffer.com` 和你的媒體主機 | 這次研究時 buffer.com 就是被白名單擋下的，沒加白名單排程會靜默失敗 |
| 5 | 準備公開媒體主機，例如 Cloudflare R2 或公開 bucket，放圖片和 Shorts 影片 | Buffer API 和 MCP 都只接受網址，不能上傳檔案 |
| 6 | 在 repo 寫一支 `buffer_draft` 腳本：先查頻道 ID，再呼叫 `createPost`，**寫死 `saveToDraft: true`**，並檢查 GraphQL `errors` | 欄位名稱以 developers.buffer.com 的 schema 為準（本次未讀到），先用 introspection 確認 |
| 7 | 在 CLAUDE.md 或自訂 skill 寫明：只能用這支腳本送稿，雲端環境不掛 Buffer MCP，FB 個人帳號和小紅書的稿子寫進 `queue/manual/` | 互動時要用 MCP，可以在 claude.ai 個人連接器裡另外加，不要放進無人值守的排程 |
| 8 | 建立 Claude 雲端排程，例如每週五晚：讀品牌語氣檔 → 為三個專案寫稿 → 生成並上傳素材 → 呼叫腳本 → 把清單寫進 repo 並通知你 | 先手動跑一次 dry-run |
| 9 | 第一週驗收：每個頻道送一則測試草稿，在手機 App 從草稿排程 | 實測四件事：草稿是否不算進 10 則上限、Threads 串文、IG 輪播和 Reels、YouTube 標題欄位 |
| 10 | 之後的日常：手機 Buffer App → 草稿 → 修改 → 排程；Notify Me 貼文到時候手動點；留言在 Community 回 | 排程佇列超過 10 則就升級 Essentials（約 £11–14），或改用 Postiz |

### 表 8：付費或上線前，必須到官方頁面確認的項目

| 項目 | 去哪裡查 | 為什麼重要 |
|---|---|---|
| Buffer 英鎊價格、VAT、Free 的 10 則上限是否不算草稿 | buffer.com/pricing、Buffer 說明中心 | 決定 Free 夠不夠用 |
| Buffer `createPost` 能否發 IG Reels／輪播、Threads 串文、YouTube 標題與隱私設定 | developers.buffer.com/reference.html | 決定首選能不能撐起完整流程 |
| Buffer API key 能否限縮權限、MCP 能否不用 OAuth 改用 key | developers.buffer.com | 只建草稿的安全邊界 |
| Buffer Free 是否有終身頻道連線次數上限 | Buffer 說明中心 | 避免頻道名額被鎖死 |
| Postiz Standard 是否有每月 400 則上限、MCP 是否有建草稿工具、API 實際限額 | docs.postiz.com、postiz.com/pricing | 備選方案是否成立 |
| Metricool MCP 在 Free／Starter 能不能用 | metricool.com/pricing、Metricool MCP 頁 | 可能讓它升為第三選擇 |
| Publer 現行計價（每帳號或基本費）與 MCP 是否開放 | publer.com/plans | 預算邊緣的判斷 |
| Zernio、Upload-Post 的 API 是否有草稿狀態 | zernio.com、upload-post.com 文件 | 能不能當便宜的發文層 |
| YouTube 未驗證專案的私人鎖、上傳配額 | developers.google.com/youtube/v3 | 只有走 DIY 時才需要 |
| Meta Business Suite 能否排 Threads | 自己的帳號實測 | 手動備援的範圍 |
| 小紅書台灣封鎖令是否延長（約 2026 年 12 月到期） | 內政部或新聞 | 台灣受眾看不看得到 |

---

## 結論

2026 年對你的情境最大的變化不在功能，而在**誰對免費用戶開放寫入**。Buffer 把 API 開放到 Free 方案，讓原本最平價的排程器也能讓 AI 寫入。企業級工具則反方向走：Agorapulse 取消免費版、Hootsuite 改版成多 App 架構、Sprout 把 API 鎖在每人 $399 的方案。同時，設計上最安全的「MCP 只能建草稿」只出現在昂貴的工具裡，預算內的工具都要你自己用一支腳本把寫入權限收窄成「只建草稿」。這也修正了先前報告「第一階段先別接排程器」的建議：當時 Buffer API 是否開放給 Free 還不確定；現在確認可以 £0 接上，而且「Claude 建草稿、你在手機按排程」的審核成本，比「從 repo 複製貼上到三個原生排程器」還低。

接下來兩週，最值得驗證的是 Buffer API 能不能處理 IG Reels、輪播和 Threads 串文。這一點決定首選能不能撐住全部流程。如果不行，就把那一類貼文改成 Notify Me 或原生排程手動處理，而不是馬上換工具。真正要換工具的時機有兩個：每頻道 10 則的排程上限或 3 個頻道成為瓶頸。那時候先比較 Buffer Essentials（約 £11–14）和 Postiz Cloud（約 £17–23），兩者都還在預算內。
