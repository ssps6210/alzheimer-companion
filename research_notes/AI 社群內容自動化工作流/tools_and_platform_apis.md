# Social Media Scheduling/Automation Tools and Official Platform API Limits (as of Oct 2026, solo creator, near-zero budget)

Research note: written 2026-10-28. Access limits for this session: `buffer.com` and `developers.facebook.com` could not be fetched directly (host blocked in this sandbox). Facts about those sites come from search-engine snippets of the official pages or from third-party pages, and are labeled. Many pricing claims come from third-party blogs and some come from vendors. Each claim is marked as official, vendor or third-party.

---

## Q1. Scheduling tool comparison (Buffer, Postiz, Meta Business Suite, Threads native, YouTube Studio, Metricool, Later, Typefully)

### Takeaway
No free tool covers all of this creator's platforms. For $0, the realistic mix is native schedulers: Meta Business Suite for FB Page and IG, Threads' in-app scheduler, and YouTube Studio. Buffer's free plan (3 channels, 10 queued posts per channel) or self-hosted Postiz can add one API-driven layer. Facebook Groups, Xiaohongshu and (for most tools) Reddit stay manual.

### Cited Findings
**Buffer**
- Free plan (mid-2026): 3 connected channels and 10 scheduled posts per channel at a time. This is a queue cap, not a monthly cap. Instagram and TikTok each count as separate channels. — [Marc Andrews blog (third-party)](https://marcandrews.com/?p=2565); [boomp.net (third-party)](https://boomp.net/blog/buffer-pricing-free-plan-limits-2026)
- Supported networks that can fill those 3 slots: Instagram, Facebook, X, LinkedIn, Mastodon, TikTok, Pinterest, YouTube, Threads, Bluesky. — [SocialBu blog (competitor, third-party)](https://socialbu.com/blog/buffer-pricing)
- Some YouTube and TikTok flows may use mobile-notification ("remind me") publishing instead of full auto-publish. — [sonary.com review (third-party)](https://sonary.com/b/buffer-inc/buffer+social-media-management)
- One blog reports a lifetime limit of 8 unique channel connections on Free, even if you disconnect and reconnect. Single source, unverified. — [Marc Andrews blog](https://marcandrews.com/?p=2565)
- Sources disagree on free analytics. One says basic analytics with 30-day history; another says none. — [socialk.it pricing guide](https://socialk.it/en/pricing/buffer); [SocialBu](https://socialbu.com/blog/buffer-pricing)
- Essentials costs about $5 per channel per month billed yearly, or $6 monthly. — [SocialBu (third-party)](https://socialbu.com/blog/buffer-pricing)
- Buffer runs an official MCP server ("draft, schedule, and manage your posts" from Claude or ChatGPT). — [buffer.com/mcp (vendor)](https://buffer.com/mcp)

**Postiz** (open source, gitroomhq/postiz-app, AGPL-3.0)
- Self-host requirements (official docs): Temporal is required since v2.12.0 and is bundled in the official docker-compose with Postgres and Redis. External services can be used via `DATABASE_URL`, `REDIS_URL` and `TEMPORAL_ADDRESS`. — [docs.postiz.com system requirements (official)](https://docs.postiz.com/installation/system-requirements)
- Hardware: supported floor is 2 vCPU / 2 GB RAM, and the stack has been tested on a 2 GB / 2 vCPU Ubuntu VM. 4 vCPU / 8 GB is recommended for up to 20 users. An older Mintlify mirror of the docs says 4 GB minimum, which is stale. — [docs.postiz.com (official)](https://docs.postiz.com/installation/system-requirements); [Mintlify mirror (older)](https://www.mintlify.com/gitroomhq/postiz-app/self-hosting/overview)
- Hosted on Railway, the Temporal stack costs roughly $15–25/month. A pre-Temporal v2.11.3 template is listed at roughly $5–10/month. These are third-party template estimates. — [Railway template](https://railway.com/deploy/postiz-self-hosted-buffer-alternative-for-30-platforms--postiz-social-scheduler); [Railway template (updated Oct 26)](https://railway.com/deploy/postiz-updated-oct26--postiz-scheduler.md)
- Self-hosting means you register your own developer apps and API keys with each platform (Meta, Google and so on). Postiz does not supply them. This is inferred from the self-host model and fits the env-var-driven setup in the [docs](https://docs.postiz.com/installation/system-requirements). It is not explicitly confirmed in what I could fetch.
- Official cloud plans: Standard $29/mo (5 channels, $278/yr), Team $39/mo (10 channels), Pro $49/mo (30 channels), Ultimate $99/mo (100 channels). All list unlimited posts. Some third-party sites still list "400 posts/month" on Standard, which conflicts with the official table. — [docs.postiz.com/cloud/plans (official)](https://docs.postiz.com/cloud/plans); [socialrails (third-party)](https://socialrails.com/blog/postiz-pricing)
- Postiz claims 30+ platforms. — [Railway template](https://railway.com/deploy/postiz-self-hosted-buffer-alternative-for-30-platforms--postiz-social-scheduler); [postiz.com/claude (vendor)](https://postiz.com/claude)

**Meta Business Suite and Threads native**
- Sources conflict on whether Business Suite schedules Threads. A DEV Community guide says Threads was not supported in Business Suite as of March 2026. A ShortSync guide says you can pick Threads as a channel in Business Suite. Neither is official. — [DEV Community](https://dev.to/ppcvote/how-to-schedule-threads-posts-set-up-daily-auto-posting-in-5-minutes-1h0f); [ShortSync](https://shortsync.app/guides/schedule-threads-posts)
- Threads rolled out native in-app post scheduling to all users in January 2025. — [Techsoma](https://techsoma.africa/?p=3112); see also [MediaPost on the earlier test](https://www.mediapost.com/publications/article/402001/threads-targets-social-media-managers-with-post-sc.html)
- Native Threads scheduling reportedly reaches up to 75 days ahead. Single vendor blog. — [PostPlanify](https://postplanify.com/blog/how-to-schedule-threads-posts)
- Business Suite scheduling of FB Pages and IG is free. Widely documented, e.g. [SocialChamp (third-party)](https://www.socialchamp.com/blog/schedule-facebook-posts/).

**Metricool**
- Free plan (official help article, Spanish): 1 brand, up to 20 scheduled posts per month, 30 days of analytics history, 5 fixed competitors, 5 AI text-generation credits per month. It never expires and has no Make or Zapier integration. A third-party site claims 50 posts per month, which conflicts with the official article. — [help.metricool.com (official)](https://help.metricool.com/es/main-differences-between-free-and-paid-plans-bl0v9); [costbench (third-party)](https://www.costbench.com/software/social-media-management/metricool/free-plan/)
- Metricool documents daily posting limits per network, including Threads at 250 posts and 1,000 replies. — [help.metricool.com](https://help.metricool.com/daily-posting-limits-on-social-media-sh58j)

**Typefully**
- Official remote MCP server at `https://mcp.typefully.com/mcp` with OAuth. Typefully is strongest for X and threads-style drafting. — [support.typefully.com (vendor)](https://support.typefully.com/en/articles/13128440-typefully-mcp-server)

**YouTube Studio / Later**
- YouTube Studio's native scheduling (upload as private, then set a publish time) is free. I did not fetch a 2026 source; this is long-standing product behavior.
- Later's free plan: I found no 2026 data.

### Inferences
- Cheapest low-maintenance stack: Threads native scheduler + Meta Business Suite (FB Page, IG) + YouTube Studio, all $0. Add Buffer Free only if a single cross-post queue is worth it. Buffer's 3-channel cap means picking, for example, Threads + IG + FB Page.
- Self-hosted Postiz is free in license terms but not in effort. It needs a 2 GB+ VPS (about US$5–25/month), Docker, Temporal, and your own approved developer apps on each platform. The approval workload (Meta App Review, Google OAuth verification) is likely the bigger cost for a solo developer.
- Metricool Free (20 posts/month) and Buffer Free (10 queued per channel) both suit a cadence of a few posts per week, not daily multi-platform posting.

### Gaps
- Could not fetch buffer.com/pricing to confirm free-plan limits, whether the AI Assistant and Community/comment inbox are on Free, or whether YouTube auto-publishes. All Buffer limits above are third-party.
- Later's 2026 free plan status is unknown.
- No official Meta statement found on Threads in Business Suite.
- Typefully pricing and free tier were not checked.

---

## Q2. Automation glue: n8n, Make, Zapier, and human-approved AI posting templates

### Takeaway
Self-hosted n8n is the only option with unlimited runs at $0 apart from the server, and it has ready-made "AI draft → Telegram approve → publish" templates. Zapier Free (100 tasks/month, 2-step Zaps) is too small for this. Make Free (1,000 credits, 2 active scenarios) is workable for one light pipeline.

### Cited Findings
- **n8n Cloud** (prices in EUR): Starter about €20/month annual (€24 monthly) for 2,500 executions and 5 concurrent. Pro about €50/month annual (€60 monthly) for 10,000 executions. No permanent free Cloud tier, only a 14-day trial. — [sliplane (third-party)](https://sliplane.io/blog/n8n-pricing); [jetadmin (third-party)](https://www.jetadmin.io/blog/n8n-pricing/amp/); [activepieces (competitor)](https://www.activepieces.com/blog/n8n-pricing-2026-plans-free-tier-costs-explained.md)
- **n8n self-hosted Community Edition**: free, unlimited executions, you pay only for the server. An execution is one full workflow run regardless of step count. Polling triggers can burn Cloud quotas fast; one example is a Gmail poller exhausting 2,500 executions in under 11 days. — [sliplane](https://sliplane.io/blog/n8n-pricing); [cloudzero](https://www.cloudzero.com/blog/n8n-pricing/)
- n8n reportedly kept Cloud prices flat in 2026 while adding AI builder credits. — [collab365](https://spaces.collab365.com/posts/n8n-keeps-cloud-prices-flat-and-adds-more-ai-build-Xuioxz)
- **Zapier Free**: $0, 100 tasks/month, 2-step Zaps only (trigger + action), 15-minute polling, no premium apps or webhooks. — [DEV Community](https://dev.to/trackstack/zapier-free-plan-in-2026-what-100-tasks-actually-buy-you-3h8k); [lindy.ai](https://www.lindy.ai/blog/zapier-pricing)
- **Make Free**: 1,000 credits/month, 2 active scenarios max, 15-minute minimum interval, 5-minute max execution time. Core costs about $9/month annual for 10,000 credits; Zapier's blog cites $12. Every filter and router step consumes credits. — [jetadmin, Sept 2026 (third-party)](https://www.jetadmin.io/blog/make-pricing/amp/); [zapier.com blog (competitor)](https://zapier.com/blog/make-com-pricing/)
- **Human-in-the-loop templates (n8n.io official template gallery):**
  - #5625: drafts X posts with Gemini or GPT-4.1, sends a "Good to go?" message in Telegram, and publishes on approval or regenerates on a revision request. — [n8n.io/workflows/5625](https://n8n.io/workflows/5625-create-x-posts-with-gemini-and-gpt-41-ai-and-telegram-human-in-the-loop-approval)
  - #9472: LinkedIn drafts with Telegram approval. Rejection feedback goes to a reviser agent, and approved posts are logged to Google Sheets. — [n8n.io/workflows/9472](https://n8n.io/workflows/9472)
  - #5397: Telegram Approve/Decline buttons, then posts to Facebook, LinkedIn and optionally X, with records in NocoDB. — [n8n.io/workflows/5397](https://n8n.io/workflows/5397)
  - #13471: AI visuals → Telegram sign-off → multi-platform publish via Blotato. Needs a Blotato account. — [n8n.io/workflows/13471](https://n8n.io/workflows/13471)
  - Upload-Post Telegram bot: voice, photo or text input → per-platform copy → confirm in Telegram → upload. — [upload-post.com](https://www.upload-post.com/n8n/ai-social-media-manager-bot-with-telegram-and-gemini)
- One blog recommends a webhook-resumed Wait node for Telegram approvals over the default approval nodes. Its "83% more reliable" figure is unsourced. — [growwstacks](https://growwstacks.com/blog/n8n-human-approval-loops-for-ai-automations)

### Inferences
- A Taiwan-based developer already using LINE could swap Telegram for a LINE bot as the approval channel. Replies in a 1:1 chat probably don't count against LINE's paid push quota (see Q4). The same n8n Wait/Webhook pattern applies.
- Most "publish" nodes in these templates call either official platform APIs (needing your own Meta and Google apps) or a paid aggregator (Blotato, Upload-Post). The aggregator removes app-review work but adds a monthly fee.

### Gaps
- Did not verify Zapier and Make prices on their own pricing pages.
- Did not find a ready template targeting Threads + IG + YouTube together with LINE approval specifically.

---

## Q3. Claude-based options: MCP servers and skills for posting and scheduling

### Takeaway
Official, vendor-hosted OAuth MCP servers exist for Buffer, Postiz, Typefully and Blotato, so Claude can draft and schedule directly. Third-party "Xiaohongshu MCP" and skills work by automating a logged-in browser session (cookies). They carry real credential and account risk.

### Cited Findings
- **Buffer MCP (official)**: Buffer's page says its MCP server lets Claude, ChatGPT and other AI tools "draft, schedule, and manage your posts". A Blotato blog cites an endpoint `mcp.buffer.com/mcp`, which I could not confirm on Buffer's site. Community servers (e.g. damusix/buffer-mcp) use a personal `BUFFER_ACCESS_TOKEN`. One competitor page claims Buffer has no native MCP, which contradicts Buffer's own page. — [buffer.com/mcp](https://buffer.com/mcp); [Blotato list](https://www.blotato.com/blog/best-social-media-mcp-servers); [github.com/damusix/buffer-mcp](https://github.com/damusix/buffer-mcp); [socialync (contradicting)](https://www.socialync.io/mcp-server/buffer)
- **Postiz MCP (official)**: listed in the Claude connector directory, with an OAuth endpoint `https://mcp.postiz.com/mcp-oauth-dynamic`. Claude Code setup: `claude mcp add --transport http postiz https://mcp.postiz.com/mcp-oauth-dynamic`. A community server (cristdulcey/postiz-mcp) uses an API key and can target self-hosted instances. — [postiz.com/claude](https://postiz.com/claude); [postiz.com/claude-code](https://postiz.com/claude-code); [github.com/cristdulcey/postiz-mcp](https://github.com/cristdulcey/postiz-mcp)
- **Typefully MCP (official)**: `https://mcp.typefully.com/mcp` with OAuth and no API key. The Claude setup guide lists Claude Pro or Max as a requirement. — [support.typefully.com](https://support.typefully.com/en/articles/13128440-typefully-mcp-server)
- **Blotato MCP (official, paid)**: `https://mcp.blotato.com/mcp`, works with Claude.ai, Desktop, Code and Cowork via OAuth. Pricing starts at $29/month. Its own pages disagree on whether it covers 8 or 9 platforms. Blotato also publishes "best MCP" lists, so treat its comparisons as vendor marketing. — [help.blotato.com MCP FAQ](https://help.blotato.com/api/mcp/faqs); [blotato.com/claude](https://www.blotato.com/claude); [Blotato blog](https://www.blotato.com/blog/best-social-media-mcp-servers)
- **Aggregator toolkits**: Composio wraps Typefully and Postiz MCP for Claude Code. — [composio Typefully](https://composio.dev/toolkits/typefully/framework/claude-code); [composio Postiz](https://composio.dev/toolkits/postiz_mcp)
- **Xiaohongshu MCP and skills (unofficial)**: the xiaohongshu-mcp README, via a mirror, claims more than a year of use with no bans, only occasional cookie expiry. It warns that the same account cannot be logged into multiple web clients at once (logging in elsewhere kicks out the MCP session) and estimates about 50 posts/day allowed. That figure is the author's guess, not a platform rule. — [cnb.cool mirror](https://cnb.cool/root/mirror/xiaohongshu-mcp)
- ClawHub security audits of Xiaohongshu auto-poster skills note two things. First, a stored cookie file works as a live credential: "anyone or any process with access to that file may be able to impersonate" the account. Second, some skills include anti-detection and login-gate bypass behavior, which raises platform-terms and enforcement risk. The audits recommend a low-risk account, draft-first flows, manual confirmation and protecting the cookie file. — [ClawHub audit: xiaohongshu-auto-poster](https://clawhub.ai/jmin1113/skills/xiaohongshu-auto-poster/security-audit); [ClawHub audit: rednote-skills](https://clawhub.ai/mrmao007/skills/rednote-skills/security-audit)

### Inferences
- Security points for any posting MCP:
  - OAuth-hosted official servers (Buffer, Postiz, Typefully, Blotato) avoid storing raw tokens locally, but they grant the model write access to public accounts. Prefer servers or tools that create drafts and keep a human publish step.
  - Community MCP servers need personal API tokens in env vars. Audit the code and pin versions.
  - Watch for prompt injection. Comments or DMs read through an inbox tool could steer an agent that also has publish rights, so keep read and publish tools separate or approval-gated.
- For this project, Postiz MCP (cloud, or the community server pointed at a self-host) or Buffer MCP plus Buffer Free is the lowest-cost path from Claude Code to Threads, IG, FB Page and YouTube.

### Gaps
- Did not find an official Meta- or Threads-provided MCP server. Community Threads-API skills likely exist but were not verified.
- Did not confirm whether Buffer's MCP works on the Free plan.
- Could not access the original xiaohongshu-mcp GitHub repo; I only saw the mirror.

---

## Q4. Official API constraints per platform

### Takeaway
Threads, IG (Business or Creator account) and FB Pages can all be published via Meta APIs. Your own account works in development or tester mode without App Review, but serving other users requires App Review. Facebook Groups posting via API has been gone since April 2024 with no replacement. YouTube upload quota became much cheaper in Dec 2025 and June 2026. Reddit API access needs manual approval, and third-party reports describe a shutdown timeline into 2027. Xiaohongshu has no public posting API and is DNS-blocked in Taiwan. LINE OA free-message quota is uncertain.

### Cited Findings
**Threads API (Meta)**
- 250 API-published posts per profile per rolling 24 hours. Carousels count as 1. The limit is enforced at container publish, and Meta recommends apps enforce it themselves, especially for scheduling. Check usage at `GET /{threads-user-id}/threads_publishing_limit`, which needs `threads_basic` and `threads_content_publish`. — [developers.facebook.com Threads overview (official, via search snippet)](https://developers.facebook.com/docs/threads/overview)
- Reply, delete and location quotas: 1,000 replies, 100 deletions and 500 location searches per 24 hours. The same endpoint returns `reply_quota_usage` and other fields. These figures come from third parties and were not confirmed in the official text I retrieved. — [Blotato Threads API guide](https://www.blotato.com/blog/threads-api-pricing); [Metricool](https://help.metricool.com/daily-posting-limits-on-social-media-sh58j)
- Reply management: `threads_manage_replies` is the permission for POST calls to reply endpoints. A Meta responder on the developer forum confirmed it requires App Review for non-role users. — [developers.facebook.com retrieve-and-manage-replies (official)](https://developers.facebook.com/documentation/threads/retrieve-and-manage-replies); [Meta dev forum](https://developers.secure.facebook.com/community/threads/402735785468514)
- App review: "Threads testers can grant your app these permissions at any time." Users without an app role need each permission approved through App Review, and the app must be published. Testers are invited via App Dashboard > App roles and accept from Threads account settings. — [developers.facebook.com Threads use case (official)](https://developers.facebook.com/docs/development/create-an-app/threads-use-case); [Threads get started (official)](https://developers.facebook.com/documentation/threads/get-started)
- One vendor guide says each permission needs a screencast, review takes about 2–4 weeks, and you can publish to your own and tester accounts while pending. Third-party claim. — [website-apn developer guide](https://website-apn.pages.dev/blog/how-to-post-to-threads-via-api/)

**Facebook Groups API**
- Deprecated in Graph API v19.0 (January 2024) and removed from all versions within 90 days. This included `publish_to_groups`, `groups_access_member_info` and the Groups API reviewable feature. The removal date is usually cited as April 22, 2024; one vendor says April 15, 2024. — [Meta dev forum v19 thread](https://developers.facebook.com/community/threads/2076398286093257/); [techpoint.africa](https://techpoint.africa/2024/02/06/meta-facebook-disrupts-scheduling); [SocialSuite help](https://socialsuite.zendesk.com/hc/en-us/articles/43588755374355)
- No replacement posting API has been announced. A developer forum answer says "there has not been any new Groups API announced yet". Vendors say Meta's suggestion is to migrate the Group to a Page. Schedulers now offer only reminder notifications for manual posting. — [Meta dev forum](https://developers.facebook.com/community/threads/584177870580474/); [Make community](https://community.make.com/t/facebook-group-posting-solutions/34808); [SocialSuite](https://socialsuite.zendesk.com/hc/en-us/articles/43588755374355)

**YouTube Data API v3**
- Default allocation is 10,000 units/day per Google Cloud project, resetting at midnight Pacific Time. Invalid requests still cost at least 1 unit. — [developers.google.com determine_quota_cost (official, non-English versions)](https://developers.google.com/youtube/v3/determine_quota_cost?hl=ja); [ChannelCrawler](https://channelcrawler.com/insights/youtube-api-daily-limit-quotas-costs-and-how-to-scale-beyond-10000-units-channelcrawler)
- Upload cost changes reported by third parties:
  - Dec 4, 2025: `videos.insert` dropped from about 1,600 to about 100 units.
  - From June 1, 2026: a "granular quota system" gives `videos.insert` and `search.list` their own buckets, by default 100 `videos.insert` calls/day and 100 `search.list` calls/day, plus 10,000 units for other endpoints.
  - Conflicts: some localized official pages (e.g. Turkish) and a 2026-09 summary still show 1,600. Treat older blogs saying "6 uploads/day" as stale. — [bundle.social](https://bundle.social/blog/youtube-api-quota-exceeded-limits-fixes); [Blotato YouTube API pricing](https://www.blotato.com/blog/youtube-api-pricing); [outstand.so](https://www.outstand.so/blog/youtube-api-pricing-quota); [developers.google.com (tr)](https://developers.google.com/youtube/v3/determine_quota_cost?hl=tr)

**Reddit API**
- On Nov 11, 2025, Reddit's "Responsible Builder Policy" announcement closed self-service access to the public Data API. Anyone (developers, researchers, moderators) must request approval. Existing access was kept. Developers are pointed to Devvit. — [r/redditdev announcement (mirror)](https://r.datuan.dev/r/redditdev/s/gquSJqMgrM)
- Third-party timeline, unverified against Reddit:
  - Oct 31, 2026: new public-API access requests stop.
  - Jan 12, 2027: access starts closing for unregistered apps.
  - March 2027: public access closes for remaining apps, except partners with written agreements. — [keyapi.ai](https://www.keyapi.ai/blog/reddit-data-api-overhaul-major-changes-and-migration-guide/); see also [redditapis.com](https://www.redditapis.com/blogs/reddit-data-api-2026)
- Anecdote: a moderator was denied API access twice with a generic "not in compliance with the Responsible Builder Policy" reply. — [subreddit snapshot, May 2026](https://reddit.sentinel-team.org/posts/1svpsrw/snapshots/2026-05-02T00%3A17%3A58.705193Z)

**Xiaohongshu (小紅書)**
- No public content-posting API was found. All automation tools found are cookie or browser based (see Q3). — [cnb.cool xiaohongshu-mcp mirror](https://cnb.cool/root/mirror/xiaohongshu-mcp); [ClawHub audits](https://clawhub.ai/jmin1113/skills/xiaohongshu-auto-poster/security-audit)
- Taiwan block, Dec 2025: the Ministry of the Interior (內政部) ordered 停止解析及限制接取 (DNS resolution stop and access restriction) under 詐欺犯罪危害防制條例 Art. 42 (the Fraud Crime Hazard Prevention Act), tentatively for 1 year. TWNIC implemented it via DNS. Officials cited 950 fraud cases (NT$132.9M losses) the previous year and 756 cases in Jan–Nov 2025. 數發部 (Ministry of Digital Affairs) cited security-test violations. — [NOWnews](https://www.nownews.com/news/6761411); [World Journal](https://www.worldjournal.com/wj/amp/story/121220/9183758); [INSIDE/TWNIC](https://www.inside.com.tw/tag/11615-TWNIC)
- Early reports said the desktop web was blocked while the mobile app still worked. — [technews.tw](https://technews.tw/?p=1479277)
- A legal scholar argues the Art. 42 use is legally flawed. — [風傳媒 葉慶元](https://www.storm.mg/article/11087300)
- Current status (Oct 2026) was not verified. The 1-year term would run to about Dec 2026.

**LINE Official Account (Taiwan)**
- Conflicting free-quota figures:
  - An unofficial 2026 note lists 輕用量 (free tier) at NT$0 with 200 free messages/month, 中用量 NT$800 with 3,000 messages, and 高用量 NT$1,200 with 6,000 messages.
  - Older OA 2.0 coverage cites 500 free messages/month.
  - Neither figure is from LINE's official page. — [hackmd (unofficial)](https://hackmd.io/@assistive-devices/rJEQJX95be); [techbang (older)](https://www.techbang.com/posts/69610)
- Billable: broadcast and push messages. Generally not billed: welcome, 1:1 chat, auto-reply and keyword replies (2022 source, may have changed). — [ithelp.ithome (2022)](https://ithelp.ithome.com.tw/articles/10292653)
- 2026: OA chat history retention was cut from 1 year to 6 months, with NT$100/month for an advanced chat plan to keep full history. — [ctee 2026-04](https://www.ctee.com.tw/news/20260415701121-430502)

### Inferences
- FB Groups (likely key for Taiwanese caregiver communities) and Xiaohongshu must stay manual. Reddit should be treated as manual too, given the approval process and the reported Oct 31, 2026 cutoff on new requests. A promotional bot for an indie project is also unlikely to fit "responsible builder" criteria.
- For single-user use on their own accounts, the developer can run Threads, IG and FB Page publishing in Meta development mode with themselves as admin or tester, avoiding App Review. App Review only matters if the tool is offered to others.
- YouTube: at 100 uploads/day the quota is no longer a constraint for a solo creator. The binding constraint is likely Google OAuth app verification and audit (see Gaps).
- Xiaohongshu automation from Taiwan would stack three risks: a DNS block (needing a VPN), cookie automation against platform terms, and the cookie file as a credential. For a dementia-care project whose credibility matters, manual posting or skipping the platform is the prudent choice.

### Gaps
- **Instagram Graph API publishing limit**: could not fetch developers.facebook.com. From prior knowledge (unverified in this session), Meta's docs say about 100 API-published posts per 24h for IG Business or Creator accounts, checked via `content_publishing_limit`, and personal accounts are not supported. Verify on the [content publishing doc](https://developers.facebook.com/docs/instagram-platform/content-publishing).
- **Facebook Pages API** publishing limits and permissions (`pages_manage_posts`) were not verified.
- **YouTube**: unverified API projects historically had uploads locked to private until a compliance audit. Not re-verified for 2026.
- The official Reddit policy page and the Oct 2026 / 2027 dates were not verified from reddit.com.
- LINE's official Taiwan OA plan page (free message count) was not reached. Both the 200 and 500 figures are unconfirmed.
- Whether the Xiaohongshu block was lifted or extended as of late 2026 is unknown.
