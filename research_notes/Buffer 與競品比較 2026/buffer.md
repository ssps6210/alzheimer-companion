# Buffer (buffer.com): full profile for an "agent writes, human approves" posting workflow (as of Oct 2026)

> **Method caveat (read first):** This session's network blocked direct fetches of buffer.com, support.buffer.com, developers.buffer.com and most third-party sites (every WebFetch failed with DNS errors). Every finding below comes from **web-search result snippets and summaries** of the cited pages, not from reading the full pages. The cited URLs are the pages those snippets came from. Before committing money or engineering time, someone should open buffer.com/pricing and developers.buffer.com directly. Where sources conflict, both sides are noted.

## 1. Plans, prices, and Free plan limits

### Takeaway
Buffer prices each connected channel separately, in USD. Free costs $0 and covers 3 channels, 10 queued posts per channel at a time, and 1 user. Essentials is about $6 per channel per month billed monthly, or $5 billed annually. Team is about $12 per channel per month, or $10 billed annually, and is the only plan with approval workflows. Three channels (Threads, Instagram, YouTube) cost $0 on Free, about $15–18 a month on Essentials, or about $30–36 a month on Team. Team at monthly billing goes over the £30 budget.

### Cited Findings
- Free plan: up to 3 connected channels and 10 scheduled posts per channel at a time. This caps posts in the queue at one time, not posts per month. The plan has no time limit. — [Blotato](https://www.blotato.com/blog/buffer-pricing); [upload-post](https://www.upload-post.com/buffer-pricing/); [boomp.net](https://boomp.net/blog/buffer-pricing-free-plan-limits-2026)
- Buffer's help center: "Free plan · 10 per channel, up to 30 total if you have 3 channels connected." — [Buffer Help: How many posts can I schedule in advance](https://support.buffer.com/article/643-how-many-posts-can-i-schedule-in-advance)
- Free plan as described by a third-party guide: 3 channels, 10 scheduled posts per channel, unlimited AI Assistant, the Community inbox, 30 days of analytics history, 100 saved Ideas, and 1 API key. — [use-apify Buffer free plan guide](https://use-apify.com/blog/buffer-free-plan-guide); also [checkthat.ai](https://checkthat.ai/brands/buffer/pricing), [socialk.it](https://socialk.it/en/pricing/buffer)
- Free plan has 1 user. Team members, access levels and approval workflows require Team. — [howsociable](https://howsociable.com/reviews/buffer); [use-apify](https://use-apify.com/blog/buffer-free-plan-guide)
- Essentials: $6 per channel per month billed monthly, or $5 per channel per month billed annually ($60 per channel per year). 1 user. — [napoleoncat (Oct 2026)](https://napoleoncat.com/blog/buffer-pricing/); [postiv.ai](https://postiv.ai/blog/buffer-pricing); [upload-post](https://www.upload-post.com/buffer-pricing/). **Conflict:** upload-post's headline gives $5 without saying it is the annual rate.
- Team: $12 per channel per month billed monthly, or $10 billed annually. Unlimited users. — [napoleoncat](https://napoleoncat.com/blog/buffer-pricing/); [socialbu](https://socialbu.com/blog/buffer-pricing)
- Volume discounts at higher channel counts. Sources give different bands. Blotato: Essentials $6 for channels 1–10, $4 for 11–25, $3 for 26–50, $1 for 51+. Turrboo: about $5 for 1–10 and about $3.33 for 11–25. SocialRails says the rate is reduced but does not publish it. These bands are **unverified**, and none matter for 3–5 channels. — [Blotato](https://www.blotato.com/blog/buffer-pricing); [Turrboo](https://turrboo.com/blog/buffer-pricing); [SocialRails](https://socialrails.com/blog/buffer-pricing)
- Prices are in US dollars, and one source says Buffer's pricing page shows a last price update of **November 2025**. — [napoleoncat](https://napoleoncat.com/blog/buffer-pricing/)
- No search result gave **GBP prices or UK VAT treatment**. Every source quotes USD. — (search of napoleoncat, socialbu, poster.ly, postotter and others; none mention £ or VAT)
- Insights history: 30 days on Free and unlimited on Essentials (per Buffer's pricing page, as summarised in search). Reports are "Not included" on Free. — [buffer.com/pricing (via search summary)](https://buffer.com/pricing)

### Inferences
- **Budget fit:** 3 channels on Free cost £0. On Essentials they cost $18 a month billed monthly or $15 a month billed annually, which is about £14 or £12 before VAT, and roughly £17 or £14 if 20% UK VAT is added. Team for 3 channels costs $36 or $30 a month, about £27–34 including VAT, which sits at or above the £30 ceiling. Exchange rates are approximate and the VAT treatment is assumed, not sourced.
- The free cap of 10 queued posts per channel is the main practical limit. At 1–2 posts per day per channel, an agent can stay only 5–10 days ahead.
- Formal approvals need Team, but they are unnecessary here. With one person, "agent creates drafts, human schedules them" works on any plan (see section 3).

### Gaps
- **"Agency" plan:** no 2026 source in the results describes a current Agency tier. The 2026 sources list only Free, Essentials and Team. The Buffer help article "Using Buffer as an agency" exists, but its content was not retrieved. Treat Agency as probably discontinued or legacy, unconfirmed.
- Whether Free has a **lifetime cap on connecting or disconnecting channels**: not found. One Trustpilot complaint cited by an aggregator mentions difficulty removing a channel on Free (see section 7).
- GBP pricing, VAT invoicing and the AI Assistant credit limits on Free: not confirmed from primary sources.
- Whether Free includes the Instagram "first comment" feature: not found.

## 2. Supported channels and per-network specifics

### Takeaway
Buffer supports Threads, Instagram, YouTube Shorts, Bluesky, Mastodon, LinkedIn, X, TikTok, Pinterest, Facebook Pages, Facebook Groups (notification only) and Google Business Profile. There is no sign of Xiaohongshu or Reddit support. Instagram can auto-publish only to Professional (Business or Creator) accounts. Buffer falls back to "Notify Me" for features the API can't publish, such as music and stickers. Threads supports threaded (multi-post) posts.

### Cited Findings
- Buffer's help center capability table lists:
  - Facebook Pages: publishing, analytics and engagement.
  - Facebook Groups: publishing only, by notification.
  - LinkedIn Pages: publishing, analytics and engagement. LinkedIn profiles: publishing and engagement, no analytics.
  - X/Twitter: publishing, analytics and engagement.
  - Pinterest (business and personal), TikTok and Google Business Profile: publishing. No analytics or engagement listed in that table, though Community covers TikTok and GBP comments (see section 4).

  — [Buffer Help: Connecting your channels](https://support.buffer.com/en-us/articles/connecting-your-channels-to-buffer-HvWLgAJvL9)
- Buffer's homepage lists Facebook, Instagram, TikTok, LinkedIn, Threads, Bluesky and YouTube Shorts among supported platforms. — [buffer.com](https://buffer.com/)
- No network-specific surcharge was found, including for X. Cost is the same per-channel price for every network. — [Zapier: how to use Buffer](https://zapier.com/blog/how-to-use-buffer/); pricing sources above
- **Instagram:**
  - Auto-publishing to Instagram **personal** profiles is impossible "due to API limitations", so a Professional account is needed. — [Buffer Help: Scheduling Instagram posts, reels, stories, notifications](https://support.buffer.com/en-us/articles/scheduling-instagram-posts-reels-stories-and-notifications-3XA98S9Q5p); [aigrow review](https://aigrow.me/buffer-review/)
  - Feed posts, carousels (up to 10 images), Reels and Stories are supported. — [buffer.com/instagram](https://buffer.com/instagram)
  - Reels and Stories can use automatic or notification publishing. If a feature isn't supported for auto-publishing (for example music or stickers), Buffer switches the post to "Notify Me". Multi-image Stories must be scheduled as separate stories. — [Buffer Help (Instagram)](https://support.buffer.com/en-us/articles/scheduling-instagram-posts-reels-stories-and-notifications-3XA98S9Q5p)
- **Stories and short-form video:** Buffer announced Facebook Stories scheduling, adding to Instagram Stories and Reels, YouTube Shorts and TikTok. — [Buffer on X (May 2024)](https://x.com/buffer/status/1792951236758540584)
- **YouTube Shorts:** you can publish immediately, add to the start or end of the queue, or set a custom time. Buffer's guide is titled "2 Ways to Schedule YouTube Shorts in 2026 — For Free". — [Buffer: How to schedule YouTube Shorts](https://buffer.com/resources/how-to-schedule-youtube-shorts/)
- **Threads, Bluesky, Mastodon, X:** threaded posts and auto-split of long text are available on X/Twitter, Threads, Mastodon and Bluesky. — [Buffer Help: Scheduling posts](https://support.buffer.com/en-us/articles/scheduling-posts-4Qdld7giAZ)
- Bluesky threads: on Free, one thread at a time per queue. Thread creation is web-only. — [Buffer: schedule to Bluesky](https://buffer.com/resources/schedule-to-bluesky/) (Free-plan limit as relayed in search; partly from a third-party review)
- Bluesky connects with an app password, not OAuth. — [theblue.social](https://theblue.social/articles/does-buffer-support-bluesky)
- Buffer positions itself around decentralised networks (Bluesky, Mastodon, Threads). — [Buffer on X](https://x.com/buffer/status/1819387020361261113?lang=en)
- One reviewer claims Instagram analytics need a linked Facebook Page that "counts as an additional billable channel". This is **unverified and possibly stale**, since the Instagram API with Instagram Login no longer needs a Page. — aggregated in [softwareadvice](https://www.softwareadvice.com/marketing/buffer-profile/reviews/) / review summaries

### Inferences
- **Facebook personal profiles** are not in Buffer's channel table (only Pages and Groups), which matches Meta's API ban on profile publishing. The user's plan to post to the FB personal profile manually is correct.
- Xiaohongshu and Reddit do not appear in any Buffer channel list found, so both are manual or unsupported.
- For Instagram, switch to a Creator or Business account (free) to get auto-publishing. Reels using trending audio will become "Notify Me" posts that need a manual tap on the phone.

### Gaps
- Threads specifics: image or carousel count limits, video, link previews, and whether threaded posts can mix media. No search result gave Buffer-specific Threads media limits.
- YouTube Shorts: whether Buffer posts only Shorts or also regular videos, and handling of title, description, privacy and thumbnail. Not retrieved.
- Facebook Groups auto-publishing was confirmed only as notification publishing. Not verified as current.

## 3. Drafts, approval workflow, mobile review and calendar

### Takeaway
Drafts are available on every plan, including Free. The formal "Request approval → Approvals tab" workflow is Team-only. For a solo user, the practical pattern on Free or Essentials is: the agent creates drafts (the API's `saveToDraft: true`), and the user reviews and schedules them in the web or mobile app.

### Cited Findings
- "While drafts are available on all plans, approving drafts is only available on our Team plan." — [Buffer Help: Managing and approving draft posts](https://support.buffer.com/article/665-managing-and-approving-draft-posts)
- Users with the "Requires Approval" role can only edit, delete and request approval on their own drafts. Clicking Request Approval moves the draft to the "Approvals" tab. The owner and Full Posting Access users approve there and don't see the request option. — [Buffer Help](https://support.buffer.com/article/665-managing-and-approving-draft-posts)
- Mobile: drafts land in a "Pending Approval" tab. Approve options are "Approve and Schedule Post" if a time was set, or "Approve and Add to Queue" if not. — [Buffer Help: drafts on mobile](https://support.buffer.com/articles/creating-managing-and-approving-draft-posts-on-the-buffer-mobile-app-XSRim1JeUl)
- Adding users requires the Team plan and the web app. — [Buffer Help: Adding users](https://support.buffer.com/article/670-adding-users-and-setting-up-permissions-in-your-organization)
- API: "Draft posts can be created using the createPost mutation with the saveToDraft argument set to true." "When saving as draft, posting limits are not checked and the post will not be published until explicitly scheduled." — [Buffer API examples](https://developers.buffer.com/examples/); [Buffer API reference](https://developers.buffer.com/reference.html)
- A suggested pattern: create a draft, check it in the Buffer app, then add it to the queue. — [professionalstoolkit Buffer API guide](https://professionalstoolkit.com/articles/buffer-api)

### Inferences
- **Key point for this use case:** drafts skip posting-limit checks, so the agent can likely stage more than 10 drafts per channel on Free. Only scheduled or queued posts count toward the 10-post cap. This is inferred from the reference text and should be tested.
- The workflow "Claude agent → `createPost(saveToDraft)` → user reviews on the phone app → taps schedule or add to queue" fits the requirements without Team.

### Gaps
- Calendar view features and limits per plan were not retrieved.
- Whether a draft can be moved to the queue from mobile on non-Team plans (likely yes, via edit and schedule) was not confirmed.

## 4. Community (comment inbox)

### Takeaway
Buffer Community is included on Free. It handles comment replies on Threads, Instagram Professional accounts, Bluesky, X, Facebook Pages, LinkedIn, TikTok, Mastodon, Google Business Profile and YouTube. Free shows comments only on new posts from the time you connect. The official MCP server reportedly has no inbox or comment tools.

### Cited Findings
- You can reply to comments on Threads, Instagram professional accounts, Bluesky, X/Twitter, Facebook pages, LinkedIn profiles and pages, TikTok, Mastodon, Google Business Profiles and YouTube through Community. The article was about 98 days old at search time. — [Buffer Help: How comments work in Community](https://support.buffer.com/article/977-how-comments-work-across-each-social-network-in-buffer-community)
- Community launched originally on 6 platforms. — [Buffer: Introducing Community](https://buffer.com/resources/introducing-community/)
- The inbox is included on Free, but "Free plan users will only see comments from new posts going forward." — [boomp.net](https://boomp.net/blog/buffer-pricing-free-plan-limits-2026); [use-apify](https://use-apify.com/blog/buffer-free-plan-guide)
- Community is available on the mobile app. — [Buffer Help: Community on mobile](https://support.buffer.com/en-us/articles/using-community-on-the-buffer-mobile-app-mCNla9C1We)
- The official MCP server is said to have no comment or inbox tools. — [usecarly (third-party)](https://www.usecarly.com/blog/claude-buffer-integration/)

### Gaps
- Exact Free vs paid differences in Community beyond comment history, such as AI reply suggestions, were not confirmed.
- Whether the API exposes comments: not found. Treat it as no.

## 5. Analytics

### Takeaway
Free gives basic Insights for the last 7 days, last 30 days or month to date, with 30 days of history and no Reports. Essentials adds unlimited history, custom ranges, Reports and (per the Help Center) CSV, Markdown and PDF export. Buffer itself says conflicting things about whether export is free.

### Cited Findings
- Free Insights ranges: "Last 7 days, Last 30 days, and Month to date". Custom and last-month ranges are paid. — [Buffer Help: Using Insights](https://support.buffer.com/article/950-using-insights-in-buffer)
- Exporting Insights as CSV, Markdown or PDF is a paid-plan feature. "Downloading snapshots" is available on all plans. CSV export is a zip of summary, posts and timeseries files. — [Buffer Help: Using Insights](https://support.buffer.com/article/950-using-insights-in-buffer)
- **Conflict:** a Buffer Threads post says CSV export "is free on every plan", and adds that you can ask an AI tool through the API or MCP to pull posts plus analytics. — [Buffer on Threads](https://www.threads.com/@buffer/post/DbnpZiKiFsQ/getting-it-out-is-quick-in-buffer-open-insights-hit-export-in-the-top-right/)
- Pricing page: 30-day history on Free, unlimited on Essentials. Reports not included on Free. Some third-party guides say 12 months on Essentials, which is less reliable. — [buffer.com/pricing (via search)](https://buffer.com/pricing); [postiv.ai](https://postiv.ai/blog/buffer-pricing)
- Analytics are not available for every network (for example LinkedIn profiles, TikTok, Pinterest and GBP per the channel table). — [Buffer Help: Connecting channels](https://support.buffer.com/en-us/articles/connecting-your-channels-to-buffer-HvWLgAJvL9)

### Gaps
- Whether Threads, YouTube Shorts and Instagram Reels metrics (views, likes, replies) appear in Free Insights. Not confirmed per network.

## 6. Public API, official MCP server and CLI

### Takeaway
Buffer reopened a public **GraphQL API** at api.buffer.com. It was in public beta from 24 Feb 2026 and generally launched around 27 May 2026, **on every plan including Free**. Alongside it came an **official remote MCP server** at `https://mcp.buffer.com/mcp` with OAuth sign-in, and a CLI (`@bufferapp/cli`). The MCP server **can write**: create, edit and delete posts, and create ideas. It can create drafts or schedule posts. Free gets 1 API key and about 3,000 requests per 30 days. The official MCP server reportedly has no comment or inbox tools, and accounts of its media and analytics support conflict.

### Cited Findings
- **Launch:**
  - Buffer's own post (dated 27 May 2026) says the API is available on every Buffer plan including Free. It describes the MCP server as letting AI tools draft, schedule and manage posts, and says a CLI was released alongside the API. — [Buffer: Buffer's API is Open for Building](https://buffer.com/resources/buffer-api-is-here/)
  - **Date conflict:** some third parties say 26 May. — [socialync](https://www.socialync.io/blog/best-social-media-mcp-servers-2026)
- **Beta:**
  - A Buffer engineer: "The @buffer Public API and MCP server are now in public beta… Schedule posts, browse your queue, check channels, and capture ideas. It works with Claude Desktop, N8N, Zapier, Claude Code, Raycast…" — [Diego Castillo on X](https://x.com/diegocasmo/status/2028553459901861990)
  - Buffer launched an MCP integrations page at publish.buffer.com/settings/integrations. — [Buffer on Threads](https://www.threads.com/@buffer/post/DVJcjUDkWwN/want-to-connect-buffer-to-your-favorite-ll-ms-or-workflow-tools-weve-launched-a)
  - Public beta opened 24 Feb 2026, with full launch planned for the end of April; the actual launch slipped to May. — (as summarised from Buffer Threads posts in search)
- Buffer's developer page says Buffer ships an MCP server with native support for Claude, ChatGPT, Cursor, Raycast and Perplexity. — [buffer.com/made-for/developers](https://buffer.com/made-for/developers)
- **MCP endpoint and setup:**
  - Endpoint `https://mcp.buffer.com/mcp`. In Claude.ai it is added as a **custom connector** with OAuth sign-in, not an API key paste.
  - Claude Code setup: `claude mcp add --transport http buffer https://mcp.buffer.com/mcp`.

  — [usecarly](https://www.usecarly.com/blog/claude-buffer-integration/); [Buffer docs: MCP server](https://developers.buffer.com/guides/integrations/mcp.html)
  - One article says the remote server has run at mcp.buffer.com/mcp since 10 June 2026. This conflicts with the May date and may refer to a remote or OAuth version. — (secondary article in search; [Buffer docs: MCP](https://developers.buffer.com/guides/integrations/mcp.html))
- **MCP tools (official docs, via search):**
  - Write tools: `create_post`, `edit_post`, `delete_post`, `create_idea`, template write tools and `execute_mutation`, which "change your data". Most MCP clients ask for approval before these run.
  - Read tools: `get_account` (organisation plan limits and member count), `list_channels` / `get_channel`, `list_posts`.

  — [Buffer docs: MCP server](https://developers.buffer.com/guides/integrations/mcp.html)
  - So the MCP is **not read-only**.
  - **Tool count conflict:** one review says 20 tools and notes that Buffer doesn't publish a full list. — [thatmarketingbuddy](https://thatmarketingbuddy.com/mcp/buffer)
- **MCP limitations (third-party):**
  - No comment or inbox tools. Media attaches as an asset (a URL), not as a file uploaded from your machine.
  - Claude "can't report on engagement or reach" because of no analytics endpoints. **Conflicts with** Buffer's Threads post suggesting you can pull analytics through the API or MCP, and with a listing that names `get_aggregated_post_metrics`.

  — [usecarly](https://www.usecarly.com/blog/claude-buffer-integration/); [Buffer Threads post](https://www.threads.com/@buffer/post/DbnpZiKiFsQ/getting-it-out-is-quick-in-buffer-open-insights-hit-export-in-the-top-right/); [glama thenavidm listing](https://glama.ai/mcp/servers/thenavidm/buffer-mcp-cli/tools/get_channels)
- **API basics:**
  - GraphQL at `https://api.buffer.com`, with a personal API key sent as a Bearer token. — [professionalstoolkit](https://professionalstoolkit.com/articles/buffer-api); [zernio](https://zernio.com/blog/buffer-api)
  - Docs: [developers.buffer.com/reference.html](https://developers.buffer.com/reference.html), [examples](https://developers.buffer.com/examples/), [rate limits](https://developers.buffer.com/guides/api-limits.html)
  - Drafts use `createPost` with `saveToDraft: true` (see section 3). — [Buffer API examples](https://developers.buffer.com/examples/)
- **Rate limits (official page):**
  - Free: 1 API key, 1 app client, 100 requests per rolling 15 minutes, 250 per 24 hours, 3,000 per 30 days.
  - Limits apply per client, and responses include RateLimit headers.

  — [Buffer API: Rate Limits](https://developers.buffer.com/guides/api-limits.html)
  - Third party: monthly caps of 3,000 / 7,500 / 15,000 for Free / Essentials / Team, shared with the MCP server. Team gets 5 keys. — [postzen](https://www.postzen.dev/blog/buffer-api); [use-apify](https://use-apify.com/blog/buffer-free-plan-guide)
  - Zernio claims a per-account cap of 2,000 requests per 15 minutes plus GraphQL complexity limits (175k points, depth 25). This is **not in the official table, so unverified**. — [zernio](https://zernio.com/blog/buffer-api)
  - Rate-limit errors can come back as HTTP 200 with `RATE_LIMIT_EXCEEDED` in the GraphQL `errors` array. — [professionalstoolkit](https://professionalstoolkit.com/articles/buffer-api)
- **CLI:** npm package `@bufferapp/cli`, needs Node 18 or later, with commands generated from the GraphQL schema. — [professionalstoolkit](https://professionalstoolkit.com/articles/buffer-api)
- **Earlier history:** Buffer closed third-party API access in 2019. — [What happened to the Buffer API](https://website-apn.pages.dev/blog/what-happened-to-buffer-api-alternatives-for-developers) (stale context. Superseded by the 2026 launch)
- **Community MCP servers (all need an API token):**
  - [ahernan2/buffer-mcp](https://github.com/ahernan2/buffer-mcp) (GraphQL API, personal access token)
  - [@damusix/buffer-mcp](https://www.pkgstats.com/pkg:@damusix/buffer-mcp) (posts, channels, orgs, ideas)
  - [jakemeany523/buffer-mcp](https://github.com/jakemeany523/buffer-mcp) (batch posts)
  - [thenavidm/buffer-mcp-cli](https://github.com/thenavidm/buffer-mcp-cli) (41 tools: 24 read, 17 confirmation-gated writes, Cloudinary media upload)
  - [glama wjjnew123](https://glama.ai/mcp/servers/wjjnew123/buffer-mcp) (upload to catbox.moe public hosting)
  - Hosted: [activepieces](https://www.activepieces.com/mcp/buffer)
- **Unreliable source:** Socialync (a competitor) says "Buffer has no native MCP server" and then contradicts itself on the same page. — [socialync](https://www.socialync.io/mcp-server/buffer)

### Inferences
- **For a Claude cloud agent (Claude Code on the web or a scheduled task):**
  - The simplest route is the official remote MCP server, added through `claude mcp add --transport http …`. But OAuth in a headless cloud container may be awkward.
  - An alternative is calling the GraphQL API directly with a personal API key stored as an environment secret. 3,000 requests a month is plenty for a few dozen posts a week.
- **Media:** images and video must be at a public URL (for example a GitHub raw or object-storage URL) before `createPost`, because the official tools take URLs and do not upload files.
- **Safety:** create posts with `saveToDraft: true` so nothing publishes without a human tapping schedule. This keeps the "human only approves" requirement on the Free plan.

### Gaps
- Exact `createPost` input schema: per-network fields (Instagram post type such as reel or story, YouTube title or privacy, Threads thread array), `scheduledAt` and queue modes. Not retrieved because developers.buffer.com was blocked.
- Whether the API or MCP can create **threaded** Threads posts, Instagram carousels or Reels. Not confirmed.
- Whether the analytics endpoints exist. Sources conflict.
- How OAuth to mcp.buffer.com works from a headless agent, and whether the MCP can use an API key instead.

## 7. Reliability, user reviews and language support

### Takeaway
Reviewers consistently praise how easy Buffer is to use and how cheap it is for a few channels. Recurring complaints: Instagram limits (no personal accounts, Notify Me fallbacks), occasional failed, duplicated or silently failing posts, channel reconnections (Instagram and LinkedIn), and slow support. The web and iOS UI are **English-only**. The Android app (v9.4.0+) lists Chinese. Posting Chinese text was not documented as a problem, but no source confirms it either way.

### Cited Findings
- Scheduled posts "sometimes fail silently or don't sync". Instagram direct publishing and Stories are flagged as unreliable (citing Trustpilot). — [softwareadvice](https://www.softwareadvice.com/marketing/buffer-profile/reviews/); [multilogin review](https://multilogin.com/blog/buffer-review/)
- Some users report posts that fail or duplicate, and accounts that don't sync. — [usefastlane review](https://www.usefastlane.ai/review/buffer)
- Instagram and LinkedIn connection problems, authentication failures, repeated reconnections and re-auth issues (Capterra). — [Capterra](https://www.capterra.com/p/143492/Buffer/); [trustradius](https://www.trustradius.com/products/buffer/reviews)
- Slow support. Difficulty removing a channel on Free (Trustpilot, as cited by an aggregator). — [aigrow](https://aigrow.me/buffer-review/); [filmora review](https://filmora.wondershare.com/video-editor-review/buffer-scheduler.html)
- Instagram Reels and some carousel limits. Tagging challenges on LinkedIn. — [aigrow](https://aigrow.me/buffer-review/)
- Positives: "simple, reliable for most formats and cheap for a few channels"; ease of use and an intuitive interface. — [goodfirms](https://www.goodfirms.co/software/buffer?page=2); [usefastlane](https://www.usefastlane.ai/review/buffer)
- Some review pages mix in very old reviews; for example, some Capterra pages go back to 2018. — [Capterra p.48](https://www.capterra.com/p/143492/Buffer/reviews/?page=48)
- **Languages:**
  - The web app and the iOS app are English-only. — [Buffer Help: another language](https://support.buffer.com/en-us/articles/can-i-use-buffer-in-another-language-wetiyDOiI4)
  - The Android app (9.4.0+) lists Chinese (中文), Japanese, Korean and others. — [Buffer Help: mobile app languages](https://support.buffer.com/article/638-using-the-buffer-mobile-app-in-another-language)
  - **Conflict:** an older article says Chinese is not supported on any platform. It predates the Android update. — [Buffer Help article 929](https://support.buffer.com/article/929-can-i-use-buffer-in-another-language)

### Inferences
- Reliability complaints mostly concern Instagram and the Meta APIs. Expect occasional "Notify Me" fallbacks and reconnects for Instagram Reels. The agent should treat Instagram Reels with music as manual.
- Chinese text in posts is just Unicode and should work. Watch character counting on X and Threads with CJK text.

### Gaps
- No G2 star rating, Trustpilot score or Reddit threads were retrieved, so star averages are not cited.
- No 2026-specific outage or incident data (no status-page history).
- No Buffer documentation found on CJK character handling.
