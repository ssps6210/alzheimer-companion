# Budget/SMB social media schedulers as Buffer competitors (2026): Metricool, Publer, SocialBee, SocialPilot, Vista Social

> **Method caveat (read first):** In this cloud session, direct page fetches were blocked for every vendor domain tried (metricool.com, publer.com, socialbee.com, socialpilot.co, vistasocial.com) and for aggregators (postplanify.com). The network allowlist caused this. So the findings below come from web-search result summaries of official help pages and third-party pricing or review sites. Many of those sites are **affiliate or competitor-authored** (for example SocialPilot writing about Metricool pricing, Blotato writing about Vista Social, PostPlanify, SocialRails, Costbench). Prices conflict across sources, so treat every price as "reported, verify on the vendor page." To re-verify, allow those domains in the session network settings.
>
> User context: solo user, 4–6 channels, budget £0–30/mo. A Claude cloud agent writes posts and pushes them via API/MCP; the user only approves. Core networks: Threads, Instagram Professional, YouTube Shorts. Facebook personal profile and Xiaohongshu (RED) are manual.

---

## Q1. Metricool

### Takeaway
Metricool has the best free plan of the five: 1 brand, all main networks except LinkedIn and X, with Threads, Instagram, YouTube and Bluesky included. It also has an **official MCP server** built for Claude. But the official README says the MCP needs **API access, which is on the Advanced tier (~$53/mo annual)**, well above £30. Sources conflict on whether a limited MCP now works on Free or Starter, and this conflict decides whether Metricool fits the budget.

### Cited Findings
- **Free plan:** no time limit. 1 brand, 20 scheduled posts/month, 30 days of analytics. LinkedIn and X/Twitter are not available on Free. — [hyperplanners Metricool review](https://hyperplanners.com/metricool-review/); [PostPlanify (aggregator)](https://postplanify.com/metricool-pricing); [Outmano](https://outmano.com/tools/metricool/pricing)
- **Starter:** priced by number of brands. Reported as $20/mo billed annually for 5 brands (rising to $159 for 50); another source gives $25 billed monthly. Starter adds LinkedIn and PDF/PowerPoint reports. — [SocialPilot on Metricool pricing (competitor-authored)](https://www.socialpilot.co/insights/metricool-pricing); [PricingSaaS](https://pricingsaas.com/companies/metricool); [PostPlanify](https://postplanify.com/metricool-pricing)
- **Note on "brand":** in Metricool, one brand is a bundle of one account per network (one IG, one Threads, one YT and so on). So a solo user with one project per brand fits Free with 1 brand, or Starter for all 3 projects. This reflects how Metricool's brand model is generally described by the sources above. The exact per-brand network rules were not verified on the official page.
- **Hidden add-ons:** at least one source frames the real cost as including hidden add-ons, mainly X/Twitter. — [Schedpilot (competitor)](https://schedpilot.com/metricool-pricing-how-much-does-it-really-cost/)
- **API / Zapier / Make:** Advanced tier only. Advanced is reported at "$53 a month billed annually for up to 15 brands." Free and Starter have "no API access at any price," with no add-on. — [SocialPilot (competitor-authored)](https://www.socialpilot.co/insights/metricool-pricing); [brandID](https://brandid.app/blog/metricool-review/)
- **MCP — official:** Metricool documents an official MCP server. It connects a Metricool account to Claude Code, Claude Desktop, Cursor, ChatGPT, Mistral Le Chat, Make and n8n. — [Metricool: Using Metricool within Claude Code](https://metricool.com/metricool-mcp-claude/); [Metricool MCP page](https://metricool.com/metricool-mcp/)
- **MCP tools:** the tools include `post_schedule_post` ("schedule a post (or multipost) to your brands"), `get_scheduled_posts` and `update_schedule_post`, plus metric readers such as `get_thread_posts` and `get_bluesky_posts`. The open-source package is `mcp-metricool` on PyPI. — [Glama mirror of README](https://glama.ai/mcp/servers/@metricool/mcp-metricool/blob/0d2346e07f6b7555e0a2ebc7698898583c37e27f/README.md); [PyPI mcp-metricool](https://pypi.org/project/mcp-metricool)
- **MCP plan requirement (CONFLICT):**
  - The official README says it requires "A Metricool account with API access (Advanced Tier)." — [Glama README mirror](https://glama.ai/mcp/servers/@metricool/mcp-metricool/blob/0d2346e07f6b7555e0a2ebc7698898583c37e27f/README.md)
  - brandID says the MCP works "on any plan, including Free, within each plan's limits." — [brandID](https://brandid.app/blog/metricool-review/)
  - PricingSaaS says the Free plan "now includes 'Metricool MCP'" and that MCP is available in Starter and Advanced "with limits." — [PricingSaaS](https://pricingsaas.com/companies/metricool)
  - Outmano lists MCP on Free but the API under Advanced. — [Outmano](https://outmano.com/tools/metricool/pricing)
  - Likely explanation: the self-hosted PyPI server still needs an Advanced API token, while a newer hosted connector may be open on all plans. **Unverified.**
- **Reviews:** Trustpilot is reported at 3.9/5 from 615 reviews; another aggregator reports 4.2/5 from 519. Complaints cluster on billing, posting reliability and support. Metricool's Trustpilot replies blame some "stuck"/late posts on temporary network API interruptions. On Reddit, the free plan earns loyalty, while annual renewal and refunds are friction points. — [PostPlanify Metricool reviews](https://postplanify.com/metricool-reviews); [Trustpilot UK Metricool](https://uk.trustpilot.com/review/metricool.com?page=2); [CheckThat.ai](https://checkthat.ai/brands/metricool/reviews)
- G2 users rate Publer's customer service as more reliable and responsive than Metricool's. — [G2 Publer vs Metricool](https://www.g2.com/compare/publer-vs-metricool)

### Inferences
- Metricool is Spanish (Castellón) and its UI is multilingual. No source in this search confirmed a Chinese UI, so it is probably absent. Verify.
- If the hosted MCP really works on Free or Starter, Metricool is the cheapest "Claude → scheduler" path that already exists: Free costs £0, and Starter is roughly £16–20/mo for 5 brands. If it needs Advanced, it breaks the £30 budget.
- 20 posts/month on Free is roughly 5 per week across all networks, which is too few for 3 projects × 3 networks.

### Gaps
- I could not confirm from an official page (fetch blocked): exact current prices in GBP, which Instagram formats auto-publish (carousel/Reels/Stories), the YouTube Shorts flow, Facebook groups, TikTok/Pinterest/GBP/Reddit, inbox networks, AI features, approval workflow, or analytics history on Starter.
- No data found on Xiaohongshu or Weibo support (presumably none).

---

## Q2. Publer

### Takeaway
Publer is the cheapest paid option with a real API, which is on Business. Business is about $8–10/account/mo, so 4–6 accounts cost roughly $32–60, which goes over £30. It has strong Threads support (threads up to 25 posts) and Instagram/Facebook Reels and Stories via API. An **official MCP + Claude connector exists but is in beta** for "Top Ambassadors and Enterprise clients" only. A community MCP is also available.

### Cited Findings
- **Pricing (CONFLICT between models):**
  - Per-account reading: Professional costs about $5/mo per account (about $4 annual), with additional accounts +$4/mo. Business costs about $10/mo per account ($8 annual). Annual billing saves 20%. — [SocialK.it](https://socialk.it/en/pricing/publer); [PostPlanify](https://postplanify.com/publer-pricing); [Turrboo](https://turrboo.com/blog/publer-pricing)
  - Flat-base reading: Professional $12 and Business $21 covering 3 accounts. One example puts 7 accounts at $28/mo (Professional) and $37/mo (Business). — [G2 Publer pricing](https://www.g2.com/products/publer/pricing); [Costbench](https://costbench.com/software/social-media-management/publer/); [SocialRails](https://socialrails.com/blog/publer-pricing)
  - Extra team seats: about $2/mo (Professional) or $3/mo (Business). — [SocialK.it](https://socialk.it/en/pricing/publer)
- **Free plan:** 3 social accounts, X not available on Free, 10 scheduled posts per account, 25 saved drafts. The limits users hit first are the 24-hour post history and the X exclusion. — [PostPlanify](https://postplanify.com/publer-pricing); [SocialRails](https://socialrails.com/blog/publer-pricing)
- **API:** Business tier. Business includes unlimited AI prompts, analytics and reports, best time to post, competitor and hashtag analytics, and API access. One source says "API and MCP access." — [CreatorStackClub](https://www.creatorstackclub.com/software/publer); [AIGrow](https://aigrow.me/publer-review/)
- **API capabilities:** one JSON request can schedule or publish Instagram and Facebook Reels and Stories. Reels run 3–90s at 9:16; Stories max 15s. Media is uploaded through the Media API and referenced by ID. There are separate endpoints for scheduling and for publishing immediately. — [Publer docs: Reels, Shorts & Stories](https://publer.com/docs/create-posts/content-types/platform-specific-formats/reels-shorts-and-stories)
- **Threads:** a main post can carry a link, a video up to 5 min, or up to 10 photos. GIFs are not supported. A thread can have up to 25 posts of 500 characters each. — [Publer help: schedule Threads](https://help.publer.io/en/article/how-to-schedule-poststhreads-to-the-threads-app-4yjmqd)
- Publer can auto-share a published Threads post to an Instagram Story. — [Publer help (IT)](https://publer.com/help/it/article/come-condividere-i-post-di-threads-nelle-storie-di-instagram-1a386s7.md)
- **Networks:** 12+, including Bluesky, Mastodon, Threads and Telegram. — [Postfa.st (competitor)](https://postfa.st/publer-alternatives); [AIGrow](https://aigrow.me/publer-review/)
- **Official MCP:** "currently in Beta with Top Ambassadors and Enterprise clients." Setup path: Settings → AI & Automations → Claude, create an API key with scoped permissions. Claude web/desktop then adds it via Customize → Connectors → Add custom connector, and Claude Code via a terminal command. — [Publer help: set up MCP server](https://publer.com/help/en/article/how-to-set-up-and-use-publers-mcp-server-14orlq0/); [Publer help: connect Claude](https://publer.com/help/en/article/how-to-connect-claude-with-publers-mcp-1s22vvm/)
- **Community MCP:** github.com/alexkess/publer-mcp-server. It is not official and may drift. — [Glama listing](https://glama.ai/mcp/servers/alexkess/publer-mcp-server); [ThatMarketingBuddy](https://thatmarketingbuddy.com/mcp/publer)
- **Reliability:** G2 reviewers praise Publer's support responsiveness and reliability compared with Metricool. — [G2 Publer vs Metricool](https://www.g2.com/compare/publer-vs-metricool)

### Inferences
- For the user, Publer Business with 4–6 accounts costs about $32–48/mo annual (per-account model). That is roughly £25–38, around the top of the £30 budget. Professional (about $16–24 for 4–6 accounts) has no API.
- Even without official MCP access, a Claude cloud agent could call the REST API directly from Business, or use the community MCP.
- Publer's docs page path mentions "Shorts," which suggests YouTube Shorts is supported via API. Not explicitly confirmed.

### Gaps
- Not confirmed: a definitive current price (the two pricing models conflict), carousel auto-publish, Facebook groups/profile support (Meta removed groups API publishing in 2024, so probably not), TikTok/Pinterest/GBP/LinkedIn/Reddit specifics, inbox, RSS/recycling/CSV limits, analytics history on Professional, Chinese UI, webhooks.

---

## Q3. SocialBee

### Takeaway
SocialBee has no free plan. Bootstrap costs $29/mo (about $24 annual) for 5 profiles. It has strong evergreen category recycling and covers Threads, Bluesky and YouTube (Video + Shorts). It has an inbox for FB/X/IG/Threads/LinkedIn/YouTube. **No public API or MCP was found**, which makes it a poor fit for an agent-push workflow.

### Cited Findings
- **Pricing:** Bootstrap $29/mo, or about $24.20/mo annual, with 1 user, 5 profiles, 1 workspace and 3 months of analytics. Accelerate costs $49/mo and Pro $99/mo. Agency tiers Pro50/100/150 cost $179/$329/$449. There is a 14-day trial and no free plan. Sources are dated June–September 2026. — [PostPlanify](https://postplanify.com/socialbee-pricing); [FrontDeskReview (checked 2026-09-27)](https://frontdeskreview.com/software/social-media-management/socialbee/); [SocialChamp (competitor)](https://www.socialchamp.com/blog/socialbee-pricing/); [Hackceleration](https://hackceleration.com/labs/socialbee-pricing)
- **Networks:** the help center lists YouTube (Channels, content types Video and Shorts, comments engageable), Bluesky (Profiles: URLs and images; no analytics) and Threads (Profiles). — [SocialBee help: what accounts can I connect](https://help.socialbee.com/article/110-how-can-i-add-an-account); [SocialBee help center](https://help.socialbee.com/hc/en-us/articles/29979208733207)
- **CONFLICT on Threads:** one pricing page's list of direct-posting networks omits Threads, while the help center lists it as a direct-posting profile. — [SocialBee features](https://socialbee.com/social-media-management-tool/); [SocialBee agency](https://socialbee.com/agency)
- **Threads analytics and comment replies:** added in 2024. **Inbox:** Facebook, X, Instagram, Threads, LinkedIn and YouTube. — [SocialBee 2024 year in review](https://socialbee.com/?p=54169); [SocialBee features](https://socialbee.com/social-media-management-tool/)
- **Integrations:** a general claim of integrations with "link shorteners, design tools, task automation platforms, content curators." Zapier is not named in the results. — [SocialBee integrations](https://socialbee.com/integrations/)

### Inferences
- Bootstrap ($29, about £23) fits the budget and covers 5 profiles, but without an API Claude cannot push drafts. A Zapier "task automation" route may exist, which would add Zapier cost. Unverified.
- SocialBee's category queues suit evergreen recycling of project promos.

### Gaps
- Not confirmed: public API, webhooks, MCP, Zapier/Make actions, IG Stories/carousels, X extra cost, TikTok/Pinterest/GBP, AI copilot details, Chinese UI, reviews and reliability.

---

## Q4. SocialPilot

### Takeaway
SocialPilot has no free plan. Essentials is reported at $20–30/mo (about $17–25.50 annual) for 5–7 accounts with 1 user; the sources conflict. It supports Threads and Bluesky and has a well-established **Zapier** integration. **No public API or MCP was confirmed.** Reviews cite occasional silent failures in bulk scheduling and basic analytics.

### Cited Findings
- **Pricing (CONFLICT):** one review verified prices on 2026-06-10 at $20/mo for 5 accounts. Others list $30/mo for 7 accounts. The range runs up to Ultimate at $200/mo for 50 accounts. Essentials has 1 user; the annual discount is about 15%. Approval workflows and white-label start at Premium ($85/mo annual, $100 monthly). There is a 14-day trial with no card and no free plan. — [PostPlanify](https://postplanify.com/socialpilot-pricing); [SocialK.it](https://socialk.it/en/pricing/socialpilot); [SocialChamp (competitor)](https://www.socialchamp.com/blog/socialpilot-pricing/); [Adapter.to](https://adapter.to/blog/socialpilot-review)
- **Networks:** Threads and Bluesky are supported. Bluesky posts are limited to 300 characters, with image and video. There is an AI suggested time for Threads. — [SocialPilot Bluesky scheduler](https://www.socialpilot.co/fr/bluesky-scheduler?format=md); [SocialPilot Threads](https://www.socialpilot.co/?p=708959); [SocialPilot integrations](https://www.socialpilot.co/fr/integrations?format=md)
- **Zapier:** official app with actions such as "Add Comment" and "Approve Post." It can be invoked from AI assistants via Zapier's MCP/SDK. — [Zapier SocialPilot help](https://zapier.com/help/socialpilot/); [Zapier zapbook](https://zapier.com/zapbook/socialpilot/); [SocialPilot product update](https://www.socialpilot.co/product-update/socialpilot-integrates-zapier?format=md)
- **API:** one search source said API access sits on a "cus[tom]" (probably custom/enterprise) plan, but the snippet was truncated. Ayrshare positions itself as a "SocialPilot API alternative," which implies SocialPilot lacks a self-serve developer API. — [PostPlanify](https://postplanify.com/socialpilot-pricing); [Ayrshare compare (competitor)](https://www.ayrshare.com/compare/socialpilot-api-alternative.md)
- **Reviews:** the main criticism is reliability ("occasional silent failures in bulk scheduling, inconsistent post notifications"). Analytics are described as basic on G2, Capterra and Reddit. Pricing is seen as a strength. — [PostPlanify SocialPilot reviews](https://postplanify.com/socialpilot-reviews)

### Inferences
- Essentials fits the budget at about £16–24, but agent integration would depend on Zapier. Zapier's paid tier adds cost, and the actions may not include "create post with media." Weak fit.

### Gaps
- Not confirmed: API tier, IG Stories/carousel/Reels auto-publish, YouTube Shorts, X extra cost, inbox networks, AI details, Chinese UI, UK pricing in GBP.

---

## Q5. Vista Social

### Takeaway
Vista Social has the widest network list of the five (13, including Threads, Bluesky, Reddit, Snapchat, Tumblr and GBP) and an **official hosted MCP server**. But paid plans start around **$79–99/mo** (Professional), several times over the £30 budget. Sources conflict on whether a free plan exists, and X costs about $29/mo extra. Not a budget fit.

### Cited Findings
- **Free plan (CONFLICT):** most sources say there is no permanent free plan, only a 14-day trial with no card. SocialRails and WePickBest list a free tier with 3 profiles and 1 user, which is likely stale. — [Costbench](https://costbench.com/software/social-media-management/vista-social/free-plan/); [SocialRails](https://socialrails.com/blog/vista-social-pricing); [WePickBest](https://wepickbest.com/pricing/vistasocial)
- **Prices (CONFLICT):** Professional $79, Advanced $149, Scale $349 (Costbench); Professional $99, Advanced $199, Scale $449 (Socialync, October 2026). A $39 "Standard" tier appears only on CheckThat.ai and is unconfirmed. Another review gives Scale as $379. — [Costbench](https://costbench.com/software/social-media-management/vista-social/free-plan/); [Socialync (competitor)](https://www.socialync.io/compare/vista-social); [CheckThat.ai](https://checkthat.ai/brands/vista-social/pricing); [PostPlanify](https://postplanify.com/vista-social-pricing)
- **X add-on:** X (Twitter) costs $29/mo extra on every plan. Mastodon is missing (as of June 2026). — [Fastlancer review](https://www.fastlancer.org/en/fastlancer-blog/vistasocial-review/); [SocialRails review](https://socialrails.com/blog/vista-social-review)
- **Networks:** 13 in total: Facebook, Instagram, LinkedIn, X, Google Business Profile, YouTube, TikTok, Reddit, Pinterest, Snapchat, Tumblr, Threads and Bluesky. One affiliate review lists Instagram posts, Stories and Reels. Every plan includes unlimited post scheduling. — [Fastlancer](https://www.fastlancer.org/en/fastlancer-blog/vistasocial-review/); [Ecommerce Fastlane (affiliate)](https://ecommercefastlane.com/vista-social-review/); [Vista Social integrations](https://vistasocial.com/integrations/)
- **MCP (CONFLICT on plan):** Noobclaw and Socialync say MCP is on Advanced and higher. Blotato (a competitor) reports that Vista's own pages disagree: the pricing card lists it on Professional, the MCP hub says Advanced+, and the setup guide says any paid plan. A hosted endpoint at `mcp.vistasocial.com/mcp` returns an auth challenge. — [Blotato vs Vista Social (competitor)](https://www.blotato.com/blog/blotato-vs-vista-social); [Noobclaw](https://noobclaw.com/blog/vista-social-alternatives-2026/); [Socialync](https://www.socialync.io/compare/vista-social)
- **API:** the only mention says it "requires a sales conversation." — [Blotato (competitor)](https://www.blotato.com/blog/blotato-vs-vista-social)

### Inferences
- Even the cheapest confirmed path to MCP ($79+) is about 2.5× the budget.

### Gaps
- Not confirmed: YouTube Shorts specifically, IG Stories auto-publish (versus notification), Chinese UI, inbox networks, analytics history, Trustpilot/G2 scores.

---

## Q6. Cross-tool fit for "Claude agent drafts → scheduler → human approves" on £0–30/mo

### Takeaway
None of the five clearly delivers an affordable, verified "API/MCP + Threads + IG + YT Shorts" under £30. **Publer Business** (about $32–48 for 4–6 accounts, REST API with Reels/Stories, official MCP still in beta) and **Metricool** (an official Claude MCP, but its plan gating is disputed: Free/Starter vs Advanced at $53) are the two contenders. SocialBee and SocialPilot fit the budget but lack a confirmed public API. Vista Social has MCP but costs $79+. **No source mentions Xiaohongshu or Weibo support for any of the five**, which matches the user's plan to post to Xiaohongshu manually.

### Cited Findings
- Metricool's official Claude MCP includes scheduling tools; the README requires the Advanced API. — [Metricool MCP Claude](https://metricool.com/metricool-mcp-claude/); [Glama README](https://glama.ai/mcp/servers/@metricool/mcp-metricool/blob/0d2346e07f6b7555e0a2ebc7698898583c37e27f/README.md)
- Publer API on Business; official MCP in beta for ambassadors and enterprise. — [Publer MCP help](https://publer.com/help/en/article/how-to-set-up-and-use-publers-mcp-server-14orlq0/)
- Third-party API-first or MCP-first schedulers exist and could be alternatives outside this scope: Upload-Post (an MCP with 40 tools covering Threads and Bluesky), Publora (IG Reels/Stories/carousel, Threads, YouTube, Bluesky; Claude Desktop config), BulkPublish (11 platforms incl. Reels/Stories/Shorts). — [Upload-Post MCP](https://www.upload-post.com/mcp); [knowledge-space MCP tools list](https://knowledge-space.pages.dev/llm-agents/social-media-mcp-tools/); [mcpservers.org BulkPublish](https://mcpservers.org/id/servers/azeemkafridi/bulkpublish-api)
- Meta's April 2026 Threads API update added cross-sharing to Instagram Stories. — [Meta dev blog 2026-04-14](https://developers.facebook.com/blog/post/2026/04/14/whats-new-in-the-threads-api/)

### Inferences
- **Facebook personal profiles and groups:** Meta's API does not allow publishing to personal profiles, and groups publishing was deprecated in 2024. All five tools are therefore expected to support Pages only. This is general platform knowledge, not sourced here, so verify.
- **Approval workflow:** the cheapest tiers often gate multi-user approvals (SocialPilot from Premium at $85). For a solo user, a "draft" state plus self-review in the calendar may be enough, provided the API can create drafts rather than scheduled posts. That capability was not verified for any tool.
- **GBP conversions:** sources quote USD; vendors may show GBP or EUR to UK visitors with different rounding. All five are generally sold internationally; no UK restriction was found.

### Gaps
- Chinese (繁中) UI availability for all five: not found in any source.
- Whether each API can create drafts or pending-approval posts (versus scheduled posts) and attach video for YouTube Shorts: unverified for all.
- Primary Reddit r/socialmedia threads from 2025–2026: not surfaced; review data is mostly via aggregators.
- Official pricing pages could not be fetched. Re-check metricool.com/pricing, publer.com/plans, socialbee.com/pricing, socialpilot.co/plans and vistasocial.com/pricing once those domains are allowed.
