# Free native scheduling tools and direct official APIs (Threads / Instagram / YouTube / Facebook / Xiaohongshu) as a baseline against Buffer, as of Oct 2026

> Method note: this session could not reach developers.facebook.com, developers.google.com, skedsocial.com or ultralab.tw (DNS blocked by the session's network allowlist). Official Meta and Google documentation was therefore seen only through search-engine snippets and third-party quotations, not fetched directly. Every item marked "(official, via snippet)" should be re-checked against the live page. Most other sources are vendor or developer blogs (often vendors selling a competing tool), so treat their numbers with caution.

## 1. Meta Business Suite / Planner: platforms, limits, Facebook Page requirement, Threads support in 2026

### Takeaway
Business Suite is built around a Facebook Page. Several sources say an Instagram account must be linked to a Page to schedule there, so with only a personal Facebook profile the user cannot use it unless he creates a free Page. Threads support in Business Suite is contested: the only "yes, since late April 2026, desktop only" evidence is a Meta AI chatbot reply. Several 2026 guides say no, and one says it is rolling out unevenly.

### Cited Findings
- Business Suite requires the Instagram account to be linked to a Facebook Page, and the Page is the object Business Suite is built around. This holds even for Instagram-only businesses. — [PostOtter](https://postotter.app/blog/meta-business-suite-instagram-scheduling); [Planable](https://planable.io/blog/schedule-instagram-posts/); [Stackmatix](https://www.stackmatix.com/blog/instagram-without-facebook)
- The Business Suite scheduling window is given as "20 minutes to 29 days ahead" by Post Planner, but as "up to 75 days" by another 2026 guide. This conflicts; 75 days may be confused with the Instagram in-app limit. — [Post Planner](https://www.postplanner.com/blog/how-to-schedule-and-publish-instagram-reels); contradicted by [PostOtter](https://postotter.app/blog/meta-business-suite-instagram-scheduling)
- Business Suite can schedule Instagram Stories, which the Instagram in-app scheduler cannot. It does not cover TikTok, X, LinkedIn, YouTube or Pinterest. — [PostOtter](https://postotter.app/blog/meta-business-suite-instagram-scheduling)
- Threads support, "No" side: as of March 2026 Business Suite schedules only Facebook and Instagram, and Threads is not supported. — [DEV Community](https://dev.to/ppcvote/how-to-schedule-threads-posts-set-up-daily-auto-posting-in-5-minutes-1h0f); [postey.ai (citing Sprout Social, Mar 2026)](https://postey.ai/blog/how-to-schedule-threads-posts); [pcmonks.net](https://www.pcmonks.net/social-media/where-is-threads-post-scheduler/)
- Threads support, "Yes" side: a reply from the Meta AI account on Threads says Threads was added to Business Suite scheduling at the end of April 2026, including Taiwan, via desktop "Share to → Threads", and that the mobile app does not have it yet. This is an AI chatbot answer, not an official announcement. — [threads.com @meta.ai](https://www.threads.com/@meta.ai/post/DY46kNqkZD2); also listed as an option by [ShortSync](https://www.shortsync.app/guides/schedule-threads-posts)
- Post-mate says Threads in Business Suite is rolling out unevenly across accounts. — [post-mate](https://post-mate.com/blog/schedule-threads-posts)
- Back in 2025, MediaPost predicted (it was not confirmed) that Business Suite would add Threads after the native scheduler launched. — [MediaPost](https://www.mediapost.com/publications/article/402001/threads-targets-social-media-managers-with-post-sc.html)
- Business Suite can cross-post Instagram content to Facebook Groups, but only to groups linked to a Page in the same business portfolio. — [groupposting.com](https://groupposting.com/group-posting/facebook-groups-api/)

### Inferences
- For this user, Business Suite is useful only if he creates a free Facebook Page and links Instagram to it. It has no API and cannot be driven by an agent, so it is a manual-approval UI and not an automation target.
- The Threads-in-Business-Suite status should be checked by hand in his own account. Do not rely on it in the design.

### Gaps
- No official Meta Business Help Center page was retrieved (network block) to confirm the Page requirement, the scheduling window, the drafts limit or Threads support.
- Whether "Meta Planner" is a distinct product name or just the Business Suite Planner view was not established.

## 2. Threads native (in-app) scheduling

### Takeaway
Threads announced drafts and scheduling in August 2024, and most sources say scheduling rolled out to all users around January 2025, via the composer's three-dot menu → Schedule. Reported limits (a 75-day window, up to 100 drafts, replies cannot be scheduled) come from press coverage, not a Meta help article. A minority of 2026 sources claim the feature is absent, so availability may vary by account or region.

### Cited Findings
- Meta announced Threads analytics, post drafts and scheduling in August 2024, with scheduling on web first. Users can save up to 100 drafts. — [Social Media Today](https://www.socialmediatoday.com/news/threads-announces-analytics-adds-draft-scheduling/724428/); [Social Media Today (scheduling test)](https://www.socialmediatoday.com/news/threads-tests-native-post-scheduling/735857/)
- Native scheduling has been available to all users since January 2025. Steps: three-dot menu → Schedule → set date and time. Scheduled posts sit in the Drafts folder. Meta has not published a maximum scheduling window, so the 75-day claim is unconfirmed. — [Sked Social (updated Oct 2026; snippet only)](https://skedsocial.com/blog/schedule-threads-posts); [Sprout Social](https://sproutsocial.com/insights/schedule-threads-posts/)
- Press coverage citing Adam Mosseri describes a 75-day window, multiple posts per day, and no scheduling of replies. — [gagadget](https://gagadget.com/en/570590-threads-now-allows-you-to-schedule-posts/)
- Conflicting 2026 reports: one guide says Meta's support assistant answered "there is currently no option to schedule Threads posts", and another says no native scheduling button exists. — [postey.ai](https://postey.ai/blog/how-to-schedule-threads-posts); [pcmonks.net](https://www.pcmonks.net/social-media/where-is-threads-post-scheduler/)

### Inferences
- The native scheduler is fine for manual "approve and schedule" on a phone or the web, but it has no API hook. An agent would still have to use the Threads API (section 6) to push automatically.

### Gaps
- No official Threads Help Center article on scheduling limits was found.

## 3. Instagram native (in-app) scheduling

### Takeaway
Since November 2022, Instagram's in-app scheduler lets accounts schedule feed posts, carousels and Reels up to 75 days ahead. Third-party guides cite a cap of 25 scheduled posts per day. Stories cannot be scheduled in-app. One March 2026 claim says scheduling is now open to all public accounts, not just Professional ones; this is unverified.

### Cited Findings
- Instagram launched in-app scheduling for Professional accounts in 2022, covering a picture, carousel or Reel up to 75 days in advance. Upgrading to a Professional account is free. — [Business Standard](https://business-standard.com/amp/article/technology/instagram-brings-native-scheduling-tool-achievements-feature-for-creators-122110900678_1.html); [Social Media Today](https://www.socialmediatoday.com/news/Instagram-Rolls-Out-In-App-Post-Scheduling-Tools/635987/); [Search Engine Journal](https://www.searchenginejournal.com/instagram-lets-users-schedule-posts-reels-in-the-app)
- Third-party guides give a limit of 25 scheduled posts per day (posts, Reels and carousels) up to 75 days ahead. No official Instagram source for this was found. — [SocialPilot](https://www.socialpilot.co/blog/schedule-instagram-reels); [Post Planner](https://www.postplanner.com/blog/how-to-schedule-and-publish-instagram-reels)
- One source says that as of March 2026, native scheduling opened to all public accounts, so Business or Creator status is no longer needed. It supports posts, carousels and Reels only (not Stories). Unverified. — [PostOtter](https://postotter.app/blog/meta-business-suite-instagram-scheduling)

### Inferences
- In-app scheduling has no API, so it is a manual fallback only.

### Gaps
- No official Instagram Help Center confirmation of the 25/day cap or the March 2026 expansion to all accounts.

## 4. YouTube Studio scheduling (including Shorts)

### Takeaway
YouTube Studio on desktop and the YouTube mobile app both let you schedule Shorts with the same Visibility → Schedule option used for regular videos. This is free and has no special limits in the sources found, but the step-by-step evidence is third-party.

### Cited Findings
- Desktop: studio.youtube.com → Create → Upload, add details, then Visibility → Schedule (date and time). A video counts as a Short when it is vertical or square. — [SocialBee](https://socialbee.com/blog/how-to-schedule-youtube-shorts/); [Outfy](https://www.outfy.com/blog/how-to-schedule-youtube-short/)
- Mobile: the YouTube app's "+" → upload or create a Short → Visibility → Schedule, then set date, time and time zone. — [SocialBu](https://socialbu.com/blog/schedule-youtube-videos-and-shorts); [CapCut](https://www.capcut.com/resource/how-to-schedule-shorts-on-youtube)
- Some guides still say a Short must be under 60 seconds. YouTube extended Shorts to 3 minutes in Oct 2024, so this may be stale (that date is from model knowledge, not a fetched source). — [SocialBee](https://socialbee.com/blog/how-to-schedule-youtube-shorts/)

### Inferences
- Through the API, scheduling uses `status.privacyStatus=private` plus `status.publishAt`. That only works if the project is not private-locked (see section 6), so for an unaudited personal project the practical path is: upload via API as private, then the human sets the schedule in Studio. That manual step also serves as the approval step.

### Gaps
- The official YouTube Help page on scheduling was not fetched. The publishAt behaviour above is from model knowledge, not a fetched source.

## 5. Facebook personal profiles and Groups: can anything schedule posts in 2026?

### Takeaway
No official tool or API can post or schedule to a personal Facebook profile. The Groups API (`publish_to_groups`) was removed on 22 April 2024 and has not returned. Only Pages can be posted to via API (with `pages_manage_posts`). Browser-automation tools exist but sit outside the official API and carry ToS risk.

### Cited Findings
- Groups API deprecation was announced with Graph API v19.0 on 23 Jan 2024. It was removed from all versions on 22 Apr 2024, including `publish_to_groups`. — [groupposting.com](https://groupposting.com/group-posting/facebook-groups-api/); [Sprinklr help](https://www.sprinklr.com/help/articles/getting-started-facebook/meta-deprecates-facebook-groups-api/66229eb25f9dd9599d632712); [Zoho community](https://help.zoho.com/portal/de/community/topic/discontinuing-facebook-groups-due-to-api-deprecation?page=1)
- "You cannot post to personal profiles or Groups." Page posting needs a Page access token with `pages_manage_posts`, via POST /PAGE_ID/feed. — [upload-post Facebook Graph API guide](https://www.upload-post.com/facebook-graph-api/)
- Sprinklr dropped Groups publishing and reporting, and Zoho Social moved scheduled Groups posts to Drafts. — [Sprinklr](https://www.sprinklr.com/help/articles/getting-started-facebook/meta-deprecates-facebook-groups-api/66229eb25f9dd9599d632712); [Zoho](https://help.zoho.com/portal/de/community/topic/discontinuing-facebook-groups-due-to-api-deprecation?page=1)
- Some vendors post to Groups through a logged-in browser session instead of the API. Compliance with Meta's terms was not verified. — [multiplegroupposter](https://multiplegroupposter.com/blog/facebook-groups-integration/); [socialrails](https://socialrails.com/blog/how-to-post-to-multiple-facebook-groups)

### Inferences
- Buffer and every other scheduler are in the same position: no personal-profile posting (Meta removed `publish_actions` in 2018, from model knowledge). If he wants Facebook, the only automatable option is to create a free Page.

### Gaps
- None material.

## 6. Direct official APIs: requirements, limits, effort and risk

### Takeaway
All three APIs are free to use, and own-account use is feasible without a public App Review. Threads and Instagram allow it via app roles or testers in development mode. YouTube is the trickiest: uploads from an unaudited project are forced to private, which actually suits a "human approves in Studio" flow. The main ongoing burden is refreshing 60-day Meta tokens. Instagram also requires media at a public URL, which means hosting is needed.

### Threads API — Cited Findings
- Publishing cap: 250 API-published posts per profile per rolling 24 hours. A carousel counts as one post, and replies reportedly do not count toward it (third-party). A `threads_publishing_limit` endpoint returns remaining quota. — [Emplifi docs](https://docs.emplifi.io/platform/latest/home/threads-publishing); [social-api.ai](https://social-api.ai/blog/threads-api-publishing-posts-developer-guide); [bulkpublish](https://www.bulkpublish.com/blog/threads-limits/)
- Publishing needs scopes `threads_basic` and `threads_content_publish`. The flow is two steps: create a container, then publish. — [postproxy](https://postproxy.dev/blog/how-to-post-to-threads-via-api/); [chirio](https://blog.chirio.dev/blog/threads-api-tutorial)
- App Review: one guide says review is needed for `threads_content_publish` "in production". Others say your own account works through the Threads Tester flow without App Review, and that testers get the configured permissions immediately after accepting. — [posteverywhere](https://posteverywhere.ai/blog/post-to-threads-api) vs [netrows](https://www.netrows.com/blog/how-to-auto-post-threads-api-2026); [replia](https://replia.net/blog/threads-api-guide)
- The tester invite must be accepted inside Threads under Settings → Account → Website permissions. Adding a tester and accepting are separate steps. The User Token Generator on the use-case Settings page mints a long-lived token for testers without OAuth. Exchanging an already long-lived token can cause error 452. — [DEV Community: 7 errors](https://dev.to/hyojunlim/the-7-errors-everyone-hits-setting-up-the-threads-api-and-the-exact-fixes-2bl1); [pete-builds/mcp-threads](https://github.com/pete-builds/mcp-threads); [note.com shogo](https://note.com/shogo_works/n/na47d5d8f202a?hl=en)
- Tokens: short-lived about 1 hour, long-lived 60 days. There is no separate refresh token: you refresh the access token itself (after it is at least 24 hours old, before it expires), and once expired it is dead. — [pete-builds/mcp-threads](https://github.com/pete-builds/mcp-threads); [socialcrawl](https://www.socialcrawl.dev/blog/threads-api)
- Permissions from private-profile users reportedly expire after 90 days regardless of the token (third-party, single source). — [socialcrawl](https://www.socialcrawl.dev/blog/threads-api)
- The API supports publishing, replies and insights. — [thraads.com](https://thraads.com/api/); [social-api.ai](https://social-api.ai/blog/threads-api-publishing-posts-developer-guide)
- The API has no native "schedule for later" parameter. Third-party tutorials run their own scheduler (cron) that calls publish at the target time. — [ultralab tutorial (snippet)](https://ultralab.tw/en/blog/threads-api-auto-post-tutorial-2026); [DEV Community](https://dev.to/ppcvote/how-to-schedule-threads-posts-set-up-daily-auto-posting-in-5-minutes-1h0f)

### Instagram Graph API (Instagram Platform) — Cited Findings
- Requires a Professional account (Business or Creator). Sources conflict on Creator support: one says Creator accounts are not supported for publishing, others say both are. — [Meta content-publishing doc (official, via snippet)](https://developers.facebook.com/docs/instagram-platform/content-publishing/); [Blotato](https://www.blotato.com/blog/instagram-posting-api); [upload-post](https://www.upload-post.com/instagram-api/)
- There are two login paths. "Instagram API with Instagram Login" needs no Facebook Page; its publish permission was renamed `instagram_business_content_publish` on 27 Jan 2025. The Facebook Login path needs a linked Page. — [postzen](https://www.postzen.dev/blog/instagram-api-integration-guide); [PostOtter](https://postotter.app/blog/meta-business-suite-instagram-scheduling)
- Publishing limit: 100 API-published posts per rolling 24 hours (a carousel counts as one), enforced at `media_publish`. The `content_publishing_limit` reference still says 50, and one source reports accounts showing a quota of 100 in Oct 2026. Query `GET /{ig-user-id}/content_publishing_limit` rather than hardcoding. Hitting the limit returns error code 9, subcode 2207042. — [Meta content-publishing doc (official, via snippet)](https://developers.facebook.com/docs/instagram-platform/content-publishing/); [reeluploader](https://reeluploader.com/blog/instagram-api-publishing-limits); [contentiq](https://contentiq.media/rules/instagram/posting-limits)
- Reels publish through the same container flow. Only 5–90 second, 9:16 videos are eligible for the Reels tab. — [postproxy Reels guide](https://postproxy.dev/blog/instagram-reels-api-publishing-guide/)

### YouTube Data API v3 — Cited Findings
- Private lock: "All videos uploaded via the videos.insert endpoint from unverified API projects created after 28 July 2020 will be restricted to private viewing mode." Lifting it requires an audit for ToS compliance. Creators get an email saying the video is locked private. — [videos.insert (official, via snippet)](https://developers.google.com/youtube/v3/docs/videos/insert); [Revision history (official, via snippet)](https://developers.google.com/youtube/data/revision_history); [Quota and compliance audits](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits?hl=de)
- Conflict: one search summary quoted the official page as saying videos from unverified projects are "not restricted" to private. That reading was not corroborated; the second, more specific search and multiple third parties confirm the restriction. Treat the lock as current, but verify on the live page. — [outstand](https://www.outstand.so/blog/youtube-api-pricing-quota); [clipember](https://clipember.com/guides/youtube-upload-comes-out-private); [upload-post](https://www.upload-post.com/youtube-api/)
- Locked videos reportedly cannot be appealed and must be re-uploaded (third-party; unverified). — [clipember](https://clipember.com/guides/youtube-upload-comes-out-private)
- Quota (conflicting): one official snippet says videos.insert costs 1 unit in a separate "Video Uploads" bucket of 100 calls per day, after a 1 June 2026 change. A different snippet of the same page says 100 units. Older guides say about 1,600 units out of the default 10,000 per day (roughly 6 uploads per day). Under any of these figures, 1–3 Shorts per day fits within the free quota. — [videos.insert (official, via snippet)](https://developers.google.com/youtube/v3/docs/videos/insert); [outlierkit](https://outlierkit.com/resources/youtube-api-quota/); [socialcrawl](https://www.socialcrawl.dev/blog/youtube-data-api-2026); [Blotato](https://www.blotato.com/blog/youtube-api-pricing)
- The Data API has no monetary price; the constraint is quota. — [outlierkit pricing](https://outlierkit.com/resources/youtube-api-pricing/)

### Inferences (effort and risk of a small DIY script)
- **Effort**: about 1–3 evenings per platform for an engineer. Meta work: a developer app, use-case setup, tester invite and acceptance, token generation, a 60-day refresh cron, and the container → publish flow. Instagram also needs public hosting for media URLs (for example, S3 or R2 free tier). YouTube: a Google Cloud project, an OAuth consent screen with yourself as test user, and a resumable upload.
- **OAuth testing-mode caveat (model knowledge, not fetched):** Google OAuth apps in "Testing" status issue refresh tokens that expire after 7 days. To avoid weekly re-auth, publish the consent screen to "In production"; for your own use you can ignore the "unverified app" warning.
- **Approval flow**: the cleanest free design is that the Claude agent drafts content into a queue (for example, a GitHub repo or sheet) and the human approves. A small scheduled job, such as a GitHub Actions cron, then publishes at the target time. For YouTube, upload private and let the human set the schedule or public status in Studio, which turns the private lock into the approval gate.
- **Risks**: silent token expiry (Meta 60-day); Meta API or permission renames (as in Jan 2025); account-type requirements; Instagram media-URL hosting; the YouTube private lock or audit; no official "schedule" field on Threads or Instagram, so your own scheduler must be reliable. Buffer's value over DIY is mainly that it handles these, but Buffer itself is subject to the same platform limits, including no Facebook personal profiles.

### Gaps
- Official Threads and Instagram docs pages could not be fetched (developers.facebook.com blocked), so exact App Review wording, the tester cap and the Instagram token lifetime (believed to be 60 days long-lived, from model knowledge) are unverified.
- The 2026 YouTube quota-bucket change rests on snippets that contradict each other.

## 7. Xiaohongshu: is there a public posting API?

### Takeaway
No verifiable official public posting API for individual creators was found. The official route is the web Creator Service Platform (创作服务平台), which supports manual publishing and scheduled publishing. Manual posting is the right plan.

### Cited Findings
- Third-party, unofficial API docs list "publish note" endpoints marked "in development". Their origin is unclear and they are not official. — [Apifox shared doc](https://apifox.com/apidoc/shared/c41cf343-9eca-4060-868e-76b159406a8b/api-143214461)
- Aliyun developer articles on Xiaohongshu "APIs" cover reading note details and engagement data, not publishing. — [Aliyun 1651527](https://developer.aliyun.com/article/1651527); [Aliyun 1683375](https://developer.aliyun.com/article/1683375)
- The Xiaohongshu Creator Service Platform supports image, text and video publishing, including scheduled publishing, via the web. — [ai-bot.cn](https://ai-bot.cn/sites/77134.html)

### Inferences
- An agent could prepare the copy and media for Xiaohongshu, but posting or scheduling must be manual on the Creator Platform. Unofficial automation risks account penalties.

### Gaps
- The official open platform (open.xiaohongshu.com) was not fetched. Enterprise or partner-only publishing capability, if any, is unconfirmed.
