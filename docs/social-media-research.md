# 社群媒體推廣研究與策略 · alzheimer-companion

> 研究日期：2026-10-27。平台數據與規則變動很快，**發文前請再到各平台／社團確認當下的版規**。
> 本文標註「（待查證）」的地方，代表這次研究沒有找到一手來源，只能當作方向參考。

---

## 0. 一頁摘要（TL;DR）

| 結論 | 說明 |
|---|---|
| **真正會「裝起來」的人，不是長輩、也不是一般照顧者** | 目前需要一台 Windows 電腦（最好有 NVIDIA 顯卡）＋跑 PowerShell 安裝。實際採用者是「**會一點電腦的孫子女／子女**」，以及願意幫別人架設的工程師。 |
| **所以要跑雙軌** | **軌道 A：情感故事 → 照顧者與家屬**（Threads、Facebook、Instagram、小紅書、YouTube、LINE），目標是共鳴、分享、讓家裡「會電腦的那個人」看到。**軌道 B：技術 → 開發者／自架玩家**（Reddit 技術版、Hacker News、X、GitHub），目標是 Star、貢獻者、志工。 |
| **最強資產是起源故事** | 「阿公認不得我，直到我叼著麥香奶茶走進病房」——具體、有畫面、無法複製。所有平台的第一篇都該是它。 |
| **最強差異化是「免費＋開源＋本機＋家人的聲音」** | 同類產品 KindredMind 每月 179 加幣、走雲端電話；Elsy 不是家人的聲音。本專案資料不出門、要本人口說同意、有 AI 浮水印。 |
| **最大風險是說錯話** | 不能宣稱「治療／改善／延緩失智」（台灣非醫材宣稱療效可罰 60 萬–2,500 萬元）；不能露出阿公的臉和聲音；聲音克隆容易被聯想到詐騙，要主動講防護。 |
| **優先順序** | ① Threads（台灣）② Facebook 社團（台港）③ YouTube 示範影片（全部平台的「證據」）④ Reddit（英語，技術版優先）⑤ Instagram ⑥ 小紅書（中國大陸）⑦ X / Hacker News（一次性發表） |

---

## 1. 產品理解（讀 repo 後的整理）

**一句話**：失智長輩在平板上按一顆大按鈕說話，系統用「家人的聲音」溫柔回應；問一百次答一百次，不會說「你剛剛問過了」。

| 面向 | 內容 |
|---|---|
| 直接使用者 | 中重度失智長輩（只需會按一顆按鈕） |
| 購買／決策者 | 家屬（子女、孫子女），尤其是**住得遠、無法天天陪伴**的人 |
| 安裝者 | 家裡會用電腦的人；或幫忙架設的工程師／志工 |
| 潛在推薦者 | 失智照護社工、日照中心、居服員、長照機構（**注意：免責聲明寫明本專案不適合直接拿去做機構收費服務，且 CPU 版 XTTS 權重限非商業**） |
| 主打功能 | 家人聲音克隆（10–30 秒錄音）、失智照護護欄（不糾正、不催促、找已故親人時溫柔安撫、提到跌倒／胸痛通報家人）、閒置播放老照片、日夜模式、家人看得到「最近常說什麼」 |
| 信任設計 | 預設本機模型（Ollama），**對話文字也不出門**；無伺服器、無帳號；克隆前需本人口說同意；每句合成語音有聽不見的 AI 浮水印；CI 隱私掃描；九個高風險情境的安全測試 |
| 語言 | 繁中（預設）、簡中、英文三套 README 與語言包 |
| 門檻 | Windows 10/11、建議 NVIDIA 顯卡（作者用 RTX 4060 8GB）、下載數 GB；無顯卡有 CPU 版 |
| 支持方式 | GitHub Star、Buy Me a Coffee |

**推廣上的含義**

1. 內容不能只打動照顧者，還要給他們「下一步」：轉給家裡會電腦的人、或在留言找志工幫忙裝。
2. 「本機、資料不出門」對照顧者是**安心**，對工程師是**技術亮點**（local-first、Ollama、零樣本 TTS）——同一個事實要寫成兩種語言。
3. 需要一支**真實運作的示範影片**，否則所有貼文都只是概念。影片中**不要出現真實長輩**（見第 5 節）。

### 競品與參考（同類怎麼說故事）

| 產品 | 模式 | 對我們的意義 |
|---|---|---|
| **KindredMind**（加拿大） | 長輩打電話時用照顧者克隆聲音接聽，依加拿大阿茲海默協會溝通指引設計，月費約 179 加幣起，創辦人本身是照顧者 | 證明「家人聲音 + 失智照護」有市場；我們的對比點是**免費、開源、本機** |
| **Elsy** | 給早期失智者的語音陪伴，家人看到「趨勢而非逐字稿」，iOS/Android | 「趨勢不是逐字稿」是很好的隱私說法，可借鏡 |
| **模擬陪伴療法（Simulated Presence Therapy）** | 用家人預錄的影音安撫焦躁的失智者，是學術上已有的概念 | 可以說「這個想法在照護領域有前例」；**但 Cochrane 回顧指出證據品質低、無法下結論**，所以**不能說有療效** |

---

## 2. 各平台研究

### 2.1 Threads（脆）— 台灣第一優先

- **受眾在不在**：在。Threads 全球月活躍用戶於 2026 年 6 月宣布突破 5 億；台灣是官方點名的爆紅市場之一。2025 年一份 1,300 人問卷顯示已有過半台灣民眾使用 Threads，**其中包括不少中年與老年人**——正好是「父母開始失智的那一代子女」。
- **文化**：純文字、口語、「接地氣」，真實故事和求助文容易被轉發；演算法會把陌生人的好文推到推薦欄，冷啟動比 FB 容易。
- **相關話題**：長照、失智、照顧者、阿公阿嬤、「孫子」視角的故事。Threads 的話題標籤（topic tag）一篇只能放一個，選最精準的（例如「失智症」或「長照」）。（具體標籤熱度待查證）
- **表現好的格式**：第一人稱短故事（分成 3–5 則串文）、一張截圖＋一句話、提問帖（「你家長輩重複問最多次的是什麼？」）。
- **規則**：跟 Instagram 同屬 Meta 社群守則；外連不會被禁止，但**把 GitHub 連結放在串文最後一則或留言**，主文先講故事，比較不像廣告。
- **定位**：**故事的首發地**、與家屬對話的地方。

### 2.2 Facebook — 台港家屬社團與機構

- **受眾在不在**：在，而且是年紀最大的照顧者族群。DataReportal 指出台灣 2025 年 10 月有 1,810 萬社群媒體身分（約人口 78%）；Statista 把 Facebook 列為台灣最主要平台之一。
- **相關社群／帳號**（請自行在 FB 搜尋確認官方帳號）：
  - 台灣失智症協會（全國失智症關懷專線 0800-474-580；另有 YouTube 頻道）
  - 中華民國家庭照顧者關懷總會（家總）
  - 各縣市失智共同照護中心、失智社區服務據點（提供家屬支持團體）
  - 「失智症 家屬」「長照 照顧者」等私密社團（名稱與人數待查證）
  - 香港：香港認知障礙症協會、賽馬會耆智園、社聯（樂齡科技）——香港常用「認知障礙症」而非「失智症」，**文案要換詞**
- **表現好的格式**：長文（真實故事）、照片、短影片；社團內「經驗分享」比「產品介紹」受歡迎。
- **規則**：大多數照顧者社團**禁止廣告**。正確做法：**先私訊管理員**，說明是免費開源、無營利、問能否分享；被拒絕就只參與、不貼連結。
- **定位**：觸及年長照顧者、與協會／機構建立關係（之後可能合辦說明會或找試用家庭）。

### 2.3 YouTube（含 Shorts）— 所有平台的「證據」

- **受眾在不在**：在。YouTube 是台灣最常用平台之一；台灣失智症協會有官方頻道（醫師叮嚀、運動、手作影片）。
- **為什麼必要**：這是一個「聽了才懂」的產品——家人的聲音回答長輩，需要**聲音**才有說服力。其他平台都應該能連回一支示範影片。
- **建議內容**：
  1. 60 秒示範（Shorts／Reels 共用）：按鈕 → 問「我兒子什麼時候來？」→ 用（演出者授權的）家人聲音回答 → 再問一次 → 同樣溫柔地再答一次。
  2. 10–15 分鐘安裝教學（給「家裡會電腦的那個人」）。
  3. 「為什麼不放 AI 人臉」「聲音會不會被拿去詐騙」等 FAQ 短片。
- **中國大陸**：YouTube 不可用，同樣影片上 **Bilibili**（技術教學在 B 站接受度高）。

### 2.4 Instagram — 視覺化的照護知識與故事

- **受眾在不在**：在，偏 25–45 歲的子女／孫子女，以及英語圈的照顧者創作者生態。
- **英語圈同類帳號怎麼做**：
  - Dementia Darling（前失智照護工作者，IG 3.7 萬+ 追蹤）：輕鬆、有點可愛的圖文，談節日壓力、送長輩進機構等。
  - Be Light Care Consulting（語言治療師，跨平台 35 萬+）：溝通技巧教學。
  - MomOfMyMom、Diane Chew（照顧丈夫的日常，跨平台 16.5 萬+，分享「fiddle box」等實用小技巧）。
  - 共同點：**實用技巧 > 情緒宣洩 > 產品**；人設是「照顧者」，不是「公司」。
- **表現好的格式**：輪播圖（carousel，5–8 張的知識卡）、Reels、限時動態問答。
- **相關標籤**：#失智症 #失智照護 #長照 #阿茲海默 #照顧者 #dementia #dementiacare #alzheimers #dementiacaregiver #caregiving（熱度待查證；一篇 3–5 個精準標籤即可）。
- **規則**：個人簡介只能放連結，貼文內連結不可點 → 用「連結在個人頁」；可與 Threads 同步。
- **定位**：「不糾正、不催促」等照護溝通原則的知識卡，順帶介紹產品怎麼把這些原則做成護欄。

### 2.5 小紅書 — 中國大陸（簡體）

- **受眾在不在**：在大陸有大量家庭照護、老人照顧筆記；但這次搜尋工具**沒有收錄小紅書站內內容**，具體話題熱度與帳號需在 App 內自行搜尋（例如「阿尔茨海默 照顾」「老年痴呆 陪伴」「认知症 家属」）。（待查證）
- **⚠️ 台灣使用限制**：內政部於 2025 年 12 月 4 日依《詐欺犯罪危害防制條例》對小紅書發布**為期一年**的停止解析及限制接取命令。若你人在台灣，帳號經營會受影響；且以台灣身分在該平台推廣，可能招致政治性爭議。**建議把小紅書列為「大陸市場」專用、時間上延後**，視封鎖到期後的處置再決定。
- **平台規則**：小紅書對醫療健康（特別是醫美）內容有專項治理；**導流**（貼手機、微信、網址、QR code、他平台浮水印）是重點打擊項目，也會監測虛構體驗、誇大其詞。→ 筆記內**不要放 GitHub 網址**，改用「主頁簡介」或回覆私訊引導搜尋 repo 名稱。
- **大陸使用者的實際障礙**：GitHub、Hugging Face、Ollama 模型下載在大陸可能很慢或不穩，需要提供鏡像或替代下載說明，否則轉換率會很低。
- **法規**：中國對 AI 深度合成／生成內容有標識要求（《互聯網信息服務深度合成管理規定》、2025 年起施行的 AI 生成合成內容標識辦法；詳細條文請自行查證）。本專案的 AI 浮水印與口說同意是加分點，可以明講。
- **表現好的格式**：圖文筆記（3:4 直式封面 + 大字標題）、「真實經歷」口吻、清單型乾貨。
- **定位**：簡體版故事＋照護溝通乾貨；技術教學導到 B 站。

### 2.6 Reddit — 英語圈，技術版先行

- **受眾在不在**：兩種都在。
  - 照顧者：r/dementia、r/Alzheimers、r/AgingParents、r/CaregiverSupport、r/eldercare
  - 技術／自架：r/selfhosted、r/LocalLLaMA、r/opensource、r/SideProject
- **規則**：
  - Reddit 長期的 Reddiquette 經驗法則是 **9:1**——你的投稿中自家內容最多約十分之一，只發自家東西的帳號會被當成 spam。
  - **每個 subreddit 自訂規則，以側欄與置頂為準**。第三方 2026 年的統計顯示，抽樣的 64 個版裡約 34% 完全禁止自我推廣。照顧者版成員對露骨推銷特別反感。（r/dementia 的實際版規本次無法直接讀取，**發文前必看並先發 modmail 詢問**）
  - 有些社群把「自己做的免費 App」也算作推廣（例如 r/AutisticWithADHD 的公告）。
- **建議**：
  - **先發技術版**：r/selfhosted、r/LocalLLaMA 很吃「完全本機、資料不出門、Ollama + 零樣本 TTS、8GB 顯卡也能跑」這種敘事；標題寫明「I built…」、內文誠實列限制。
  - **照顧者版**：先用帳號真誠參與 2–4 週（回答別人的問題、分享自己照顧阿公的經驗），再**先問 mod**，以「我做了這個給我阿公，想聽照顧者的意見，有哪裡會讓你不舒服？」的徵求回饋形式發文。
- **定位**：英語圈開發者與早期採用者；照顧者版主要拿「回饋」而不是「流量」。

### 2.7 LINE — 台灣家族的傳播管道

- **受眾在不在**：在台灣幾乎每個家族都有 LINE 群組，長輩與照顧者都在（具體滲透率本次未查到最新一手數據，待查證）。
- **用法**：不是拿來「推廣」，而是讓內容**好轉傳**——做一張懶人包長圖＋一句話＋示範影片連結，讓看到 Threads／FB 的人轉進家族群組「這個好像可以給阿嬤用」。
- 可考慮建立 **LINE 社群（OpenChat）**作為安裝互助群，但要有人回覆，否則寧可不開。

### 2.8 Dcard / PTT — 年輕子女的真心話

- **Dcard**：有家屬在 Dcard 發失智長輩照顧困境的求助文被媒體轉載，說明年輕照顧者在這裡講真心話。**適合參與討論，不適合貼產品**；具體看板名稱與版規請自行確認。（待查證）
- **PTT**：可考慮技術向看板分享開發過程（看板與版規待查證）。

### 2.9 X（Twitter）、Hacker News、Product Hunt — 一次性發表

- **Hacker News「Show HN」**：專門給「自己做的東西」，官方規則要求東西要能讓人實際試用；禁止拉票、禁止刪文重發。本專案「完全本機的 AI 聲音陪伴＋安全測試＋同意閘門＋浮水印」很符合 HN 口味，但要準備好面對倫理質疑（見第 5 節）。
- **X**：英語 AI／開源開發者聚集；適合 build-in-public 的開發日誌與 Show HN 當天同步。
- **Product Hunt**：競品 KindredMind、Elsy 都在上面；本專案是開源工具，效果可能有限，列為選配。

---

## 3. 推廣策略

### 3.1 各平台定位與優先順序

| 優先 | 平台 | 語言 | 軌道 | 定位 | 成功指標 |
|---|---|---|---|---|---|
| 1 | Threads | 繁中 | A | 故事首發、與家屬對話 | 轉發、留言「想給家人用」 |
| 2 | Facebook（社團＋協會） | 繁中／港式中文 | A | 觸及年長照顧者、機構合作 | 管理員同意分享、協會回應 |
| 3 | YouTube／Bilibili | 繁中＋英字幕／簡中 | A+B | 示範與安裝教學（證據） | 觀看完成率、從影片到 Releases 的下載 |
| 4 | Reddit | 英文 | B→A | 技術版發表、照顧者版徵求回饋 | Star、Issue、有建設性的批評 |
| 5 | Instagram | 繁中／英文 | A | 照護溝通知識卡 | 收藏、分享 |
| 6 | 小紅書 | 簡中 | A | 大陸市場故事＋乾貨（延後） | 收藏、私訊詢問 |
| 7 | X＋Hacker News | 英文 | B | 一次性發表＋開發日誌 | Star、貢獻者 |
| 配合 | LINE | 繁中 | A | 讓內容好轉傳進家族群組 | 轉傳 |

### 3.2 內容支柱（5 根）

1. **起源故事與「為什麼」**——麥香奶茶、住得遠、問一百次。這是情感核心，也是可信度來源（作者本人是家屬）。
2. **照護溝通原則**——不糾正、不催促、不揭穿、重複發問就重複回答。把產品的「護欄」翻譯成任何照顧者明天就能用的說話技巧（**即使不裝軟體也有價值**），並註明參考來源、不冒充專業。
3. **隱私與安全透明**——資料不出門、口說同意、AI 浮水印、為什麼不放 AI 人臉、聲音會不會被拿去詐騙。這一根支柱同時回應「AI 好可怕」的疑慮。
4. **開發日誌（build in public）**——安全測試抓到什麼錯、8GB 顯卡怎麼塞下三個模型、為什麼預設本機模型。給技術受眾，也給家屬看見「有人在認真做」。
5. **社群共創**——招募志工幫忙架設、翻譯語言包、錄音腳本範本、照顧者回饋。讓「無法自己安裝的家庭」也有下一步。

建議比例：故事／原則 50%、隱私安全 20%、開發日誌 20%、共創號召 10%。

### 3.3 具體貼文點子（10 個）

| # | 標題／開頭 | 平台 | 格式 | 重點 |
|---|---|---|---|---|
| 1 | 「阿公認不得我快三年了。直到有一天，我叼著一盒麥香奶茶走進病房。」 | Threads（首發）→ FB → IG → 小紅書（簡體改寫） | 4–5 則串文／長文 | 起源故事；最後一則才放 repo 連結與「我做了什麼」。**不放阿公照片**，可用麥香奶茶盒、空病房走廊或插畫 |
| 2 | 「他問了第 37 次『你爸什麼時候來？』，它第 37 次溫柔地回答。」 | YouTube Shorts／Reels／Threads | 60 秒示範影片 | 演員或作者自己扮演長輩，聲音用**已授權**家人或作者本人；字幕標明「AI 合成語音示範」 |
| 3 | 「照顧失智長輩，我學到最難的一句話是『不要糾正他』」 | IG 輪播／FB／小紅書 | 6–8 張知識卡 | 不糾正、不催促、順著回答的實際例句；最後一張：「我把這些原則寫成了 AI 的護欄」 |
| 4 | 「我爸的聲音會被拿去詐騙嗎？——我做這個專案時最常被問的三個問題」 | Threads／FB／YouTube | 問答串文／3 分鐘影片 | 資料不離開電腦、本人口說同意、聽不見的浮水印＋誠實講限制（浮水印可能被洗掉） |
| 5 | 「為什麼我堅持不給它一張 AI 人臉」 | IG／Threads／小紅書 | 圖文 | 半夜醒來看到會動的臉會被嚇到；改用長輩自己的老照片輪播 |
| 6 | 「I built a fully local voice companion for my grandfather with Alzheimer's — no cloud, no account, runs on an 8GB GPU」 | r/selfhosted、r/LocalLLaMA、X | 技術貼文＋架構圖 | Ollama + faster-whisper + Qwen3-TTS；隱私架構；誠實列已知限制；徵求回饋 |
| 7 | 「Show HN: A voice companion for people with dementia, in a family member's voice (local-first, open source)」 | Hacker News | 一次性發表 | 直接連 repo；作者第一則留言說明動機、倫理設計（同意閘門、浮水印、不冒充醫療）與限制 |
| 8 | 「我用九個高風險情境測試 AI 會不會說錯話」 | Threads／X／Reddit | 開發日誌 | 問已故親人、重複發問、要求獨自外出……AI 原本怎麼答、改成怎麼答（**情境用虛構對話，不用阿公的真實紀錄**） |
| 9 | 「你家長輩最常重複問的一句話是什麼？」 | Threads／FB 社團／IG 限動 | 互動提問 | 蒐集常見問句 → 之後整理成「固定句錄音腳本範本」回饋社群（產品的「固定句」功能正好用得上） |
| 10 | 「徵：願意幫忙架設的工程師志工／想試用的家庭」 | Threads／FB／PTT／LINE 社群 | 招募帖 | 降低門檻的關鍵；說清楚是免費、開源、不收集資料，以及家屬需要準備什麼 |

### 3.4 發文頻率

| 平台 | 冷啟動期（前 4 週） | 穩定期 |
|---|---|---|
| Threads | 每週 3–5 則（含回覆別人的照護文） | 每週 2–3 則 |
| Facebook | 每週 1–2 則（專頁）；社團依管理員許可，**一個社團最多一次主動分享** | 每週 1 則 |
| Instagram | 每週 2 則（1 輪播 + 1 Reels） | 每週 1–2 則 |
| YouTube | 冷啟動期內完成 3 支：示範、安裝、FAQ | 每月 1 支 |
| Reddit | 每個版**只發一次主貼**；平時以留言參與為主 | 有重大版本更新再發 |
| 小紅書 | （延後）啟動後每週 2 篇 | 每週 1–2 篇 |
| X | 每週 2–3 則開發日誌 | 隨開發節奏 |
| HN | 只發一次 Show HN（重大版本可再考慮） | — |

一個人做，寧可少平台、穩定更新，也不要七個平台各發一篇就停。

### 3.5 冷啟動做法（30 天）

**第 0 週：準備（發文前一定要先完成）**
- [ ] 錄好 60 秒示範影片與安裝教學（不出現真實長輩，見第 5 節）
- [ ] README 頂端放示範影片連結；確認 Releases 的 APK 可下載
- [ ] 準備一個「給家屬看的一頁說明」（非技術語言），和一個「給工程師的一頁說明」
- [ ] 統一各平台帳號名稱與簡介，簡介寫明「非醫療器材、免費開源、資料不出門」
- [ ] 在 GitHub 開啟 Discussions 或一個 Issue 模板「我想試用但不會裝」，讓需求有地方落地
- [ ] 準備好常見疑問的回覆稿（詐騙、欺騙長輩、醫療效果、為什麼要 Windows/顯卡）

**第 1 週：故事首發**
- Threads 發點子 #1（起源故事）；同日上傳 YouTube 示範影片
- 私訊 3–5 個 FB 照顧者社團管理員，詢問能否分享
- 每天花 15 分鐘在 Threads 回覆別人的照護、長照文（真誠回覆，不貼連結）

**第 2 週：技術發表**
- r/selfhosted 或 r/LocalLLaMA 發點子 #6；X 同步
- 視反應準備 Show HN（點子 #7），選平日美西上午發；整天守著回答留言

**第 3 週：知識與信任**
- IG／FB 發點子 #3、#4、#5
- 主動聯絡台灣失智症協會、家總、各地失智共照中心，**請教**而不是請求推廣：「這樣的工具對家屬是否有幫助、有沒有應避免的地方？」

**第 4 週：共創**
- 發點子 #9、#10；把收到的回饋整理成一篇「照顧者告訴我的 5 件事」
- 照顧者 subreddit（已參與 2–4 週後、mod 同意的前提下）徵求回饋

**可借力的時間點**：每年 **9 月是世界阿茲海默症月（World Alzheimer's Month）、9 月 21 日是世界阿茲海默症日**——適合安排重大版本發表或回顧文。

**衡量指標**（只看少數幾個）：GitHub Star 數、Releases APK 下載次數、「非工程師」開的 Issue／留言數、志工報名數、協會或機構的回應。

---

## 4. 文案用語指引

| ✅ 可以說 | ❌ 不要說 |
|---|---|
| 陪伴、安心、讓長輩聽到熟悉的聲音 | 治療、改善、延緩、預防失智；「有療效」「臨床證實」 |
| 「照護上有『模擬陪伴』這種做法，我想試試用科技做到」 | 「模擬陪伴療法已被證實有效」（Cochrane 回顧：證據品質低，無法下結論） |
| 懷舊、用老照片陪伴 | 「懷舊療法有實證，能安撫情緒」（作者自己的介紹文件有這句，對外文案建議軟化） |
| 「說到跌倒或胸痛會試著通知家人，但不保證，緊急請打 119」 | 「緊急通報系統」「24 小時守護」「取代看護」 |
| 「最近常說的話、哪個時段比較需要陪伴」（陪伴觀察） | 「偵測病程」「失智程度評估」 |
| 「家人的聲音」「AI 合成，會標記」 | 「就像他本人」「分辨不出來」（會被理解為冒充、詐騙） |
| 失智症（台）／認知障礙症（港）／阿尔茨海默、认知症（陸） | 「老人痴呆」（帶貶義；但大陸搜尋仍常用，可作為搜尋詞而非內文用語） |

依台北市衛生局說明，**非醫療器材宣稱醫療效能，依《醫療器材管理法》可處新台幣 60 萬至 2,500 萬元罰鍰**，且這是違規廣告中最常見的樣態。軟體是否屬於醫療器材（SaMD）的認定，若之後有機構合作或收費需求，請諮詢專業法律意見。

---

## 5. 倫理與隱私注意事項

1. **阿公無法同意被公開。** 他是中重度失智者，無法對「被拍、被錄、被放上網」給出有效同意。KFF Health News 報導 #dementia TikTok 時就點出：創作者拍下家人最脆弱的一面，引發隱私、尊嚴與同意的爭議。→ **不放阿公的臉、聲音、病房、真實對話紀錄**；用插畫、物件（奶茶盒）、演員或作者自己的聲音示範。故事用文字講就夠了。
2. **聲音克隆＝詐騙聯想。** 美國 FTC、FBI 都警告過詐騙集團用聲音克隆增加可信度。每次露出「克隆聲音」都要同時講清楚：本人口說同意、聲音不離開電腦、浮水印可驗證，**也誠實講限制**（浮水印可能被重新編碼洗掉、功能可被關閉）。示範影片中使用的聲音要取得當事人書面或錄音同意。
3. **「不揭穿」的倫理爭議。** 產品在長輩找已故親人時「溫柔安撫，不揭穿」，這在照護界有「善意謊言／治療性順應」的討論，也會有人質疑「用家人聲音哄騙長輩」。發文時主動說明設計理由（避免反覆重新經歷喪親之痛）、這是家屬可以調整的設定，並**歡迎不同意見**，不要和質疑者吵架。
4. **不要讓留言區變成病歷區。** 照顧者會在留言分享長輩病況、住址、機構名稱。準備好回覆模板，提醒「不需要透露個資」；必要時隱藏過度詳細的留言。
5. **不冒充專業。** 作者是家屬與開發者，不是醫師或照護專業人員。分享照護溝通技巧時註明來源（例如失智症協會的資料），並提醒「每位長輩狀況不同，請與照護團隊討論」。
6. **揭露身分。** 在任何社群推薦時都說明「這是我做的」。偽裝成使用者推薦、用小帳拉票，在 Reddit／HN 會被封，在照顧者社群會失去信任。
7. **跨境與平台政治。** 小紅書在台灣受封鎖；在大陸平台需遵守 AI 生成內容標識規定。兩岸用語、地區名稱在不同平台可能引戰，內容盡量聚焦照護本身。
8. **授權與商業。** CPU 版的 XTTS-v2 權重限非商業使用；若之後有機構詢問「可以拿去收費服務嗎」，回覆要依 README 的授權說明，不要口頭承諾。
9. **緊急免責要每次都在。** 凡是提到「通報家人」功能的內容，都附一句「不是緊急救援系統，緊急請打 119／999／911」。

---

## 6. 下一步建議

1. 先完成示範影片（第 0 週清單）——沒有它，其他貼文的轉換率都會打折。
2. 在 Threads 發起源故事，觀察留言是「想用」還是「不會裝」，用來決定接下來偏重軌道 A 還是招募志工。
3. 中期考慮降低安裝門檻（例如一鍵安裝包、或由志工代為架設的流程），這比任何推廣技巧都更能擴大實際使用者。

---

## 參考來源

**平台與使用者數據**
- DataReportal — Digital 2026: Taiwan：https://datareportal.com/reports/digital-2026-taiwan
- Statista — Taiwan social media users：https://statista.com/statistics/1296612/taiwan-social-media-users
- 自由時報 — Threads 用戶破 5 億、台灣爆紅原因：https://ec.ltn.com.tw/article/breakingnews/5476049
- 聯合新聞網 — 台灣人有多愛「脆」：https://udn.com/news/story/6811/9572928
- 數位時代 — Threads 為何在台灣這麼紅：https://www.bnext.com.tw/story/16/why-threads-so-popular-taiwan
- Ketagalan Media — Why Threads is so popular in Taiwan：https://ketagalanmedia.com/2026/03/11/the-digital-night-market-why-threads-is-so-popular-in-taiwan
- Gigazine — Threads 500 million MAU：https://gigazine.net/gsc_news/en/20260617-threads-500-million-mau/

**小紅書**
- 世界新聞網 — 台政府封鎖小紅書 1 年：https://www.worldjournal.com/wj/amp/story/121220/9183758
- 公視新聞網：https://news.pts.org.tw/article/784595
- 關鍵評論網：https://www.thenewslens.com/article/262173
- 界面新聞 — 小紅書醫美專項治理：https://m.jiemian.com/article/12394359.html
- 數英網 — 小紅書社區規範相關：https://www.digitaling.com/articles/1388960.html

**Reddit／Hacker News**
- Hacker News Guidelines：https://news.ycombinator.com/newsguidelines.html
- Hacker News FAQ：https://news.ycombinator.com/newsfaq.html
- Y Combinator — Make Things and Show Them：https://www.ycombinator.com/blog/make-things-and-show-them
- tech.co（引述 Reddiquette 9:1）：https://tech.co/?p=151355
- r/minipainting 推廣規則（引述 9:1）：https://lr.sudovanilla.org/r/minipainting/wiki/promotion_and_participation
- Redship — Reddit self-promotion rules 2026：https://redship.io/blog/reddit-self-promotion-rules
- RedPulse — r/dementia 社群概況：https://redpulse.io/subreddit-search/r/dementia/
- Reddit 官方（請直接查看）：https://www.reddit.com/wiki/selfpromotion 、https://www.reddit.com/r/dementia/about/rules

**照顧者創作者與倫理**
- KFF Health News — Family caregivers find support on #dementia TikTok：https://kffhealthnews.org/aging/dementia-tiktok-caregivers-support/
- AgeTech Collaborative — Caregiving in the digital age：https://home.agetechcollaborative.org/blogs/mark-ogilbee/2024/11/20/caregiving-in-the-digital-age-meet-the-social-medi
- PicnicHealth — Alzheimer's content creators：https://picnichealth.com/patients/resources/blog/alz-content-creator
- 6abc — Diane Chew：https://6abc.com/amp/post/diane-chew-creating-community-hope-humor-hacks-caregivers-loves-ones-dementia/16846855/
- Being Patient — MomOfMyMom：https://beingpatient.com/jacquelyn-revere-mom-of-my-mom/
- DemetrIA：AI and ethics for the voice cloning of grandfather Demetrio：https://dau.url.edu/handle/20.500.14342/6071
- Funeral.com — AI voice synthesis after death: consent & ethics：https://funeral.com/blogs/the-journal/ai-voice-synthesis-after-death-consent-ethics-and-safer-ways-to-preserve-a-voice

**模擬陪伴療法證據**
- Cochrane — Simulated presence therapy for dementia：https://cochranelibrary.com/cdsr/doi/10.1002/14651858.CD011882.pub3
- ARIIA — Simulated presence therapy evidence theme：https://ariia.org.au/knowledge-implementation-hub/dementia-care/dementia-care-evidence-themes/simulated-presence-therapy
- Baycrest — Simulated presence therapy review：https://baycrest.echoontario.ca/long-term-care-resources/simulated-presence-therapy-for-dementia-review/

**競品**
- KindredMind（BetaList）：https://betalist.com/startups/kindredmind
- Elsy（Product Hunt）：https://www.producthunt.com/posts/elsy

**台灣法規與照護資源**
- TVBS — 非醫材宣稱療效罰則（臺北市衛生局）：https://news.tvbs.com.tw/life/2970257
- 衛福部食藥署：https://www.fda.gov.tw/TC//csmnewsContent.aspx?id=t623739&mid=267
- 臺南市衛生局 — 失智症的服務與資源（含關懷專線）：https://health.tainan.gov.tw/lasthealthweb/warehouse/%7B75ACEBBE-480E-4523-83C7-2E13A4A877E4%7Dfile/108train/%E9%99%84%E4%BB%B611_%E5%A4%B1%E6%99%BA%E7%97%87%E7%9A%84%E6%9C%8D%E5%8B%99%E8%88%87%E8%B3%87%E6%BA%90.pdf
- 自由時報 — Dcard 失智長輩照顧求助文：https://news.ltn.com.tw/news/life/breakingnews/5512849
- 元氣網 — 台灣失智症協會 YouTube 等資源：https://health.udn.com/health/story/120952/5494694
- 香港社聯 — 樂齡科技與認知障礙症行動計劃：https://n.yam.com/Article/20250711599705
- 香港認知障礙症協會照顧者支援：https://www.hkcss.org.hk/upload/cc/issue80/issue80_ebook-focus6.pdf
