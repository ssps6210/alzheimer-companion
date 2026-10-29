# API-first / AI-agent-native social posting tools as Buffer alternatives (as of Oct 2026)

> Method note: In this cloud session, WebFetch to vendor domains (postiz.com, docs.postiz.com, typefully.com, blotato.com, getlate.dev, ayrshare.com) failed DNS resolution because they are not in the allowed network domains. GitHub access to gitroomhq/postiz-app was also denied (repo not attached). All findings therefore come from WebSearch result summaries (Oct 2026), which cite official docs pages in some cases but are mostly third-party or competitor content. **Every price below needs a check on the vendor's own pricing page before purchase.** Many comparison pages are written by competitors (Blotato, Upload-Post, Postiz rivals, social-api.ai, PlanVortex) and are flagged as such.
>
> GBP figures are approximate at ~£0.75–0.80 per USD (my conversion, not sourced).

## Q1. Postiz (Cloud and self-hosted): pricing, networks, API/MCP, human-in-the-loop

### Takeaway
Postiz is the strongest overall fit for the networks he needs: Threads, Instagram, YouTube, Bluesky and Facebook Pages are all supported, plus a public API with a `draft` post type, an official MCP server (OAuth or API key), and public preview links with comments for approval. Cloud starts at $29/mo (about £22–23), inside the budget. Self-hosting is free (AGPL-3.0) but needs your own Meta and Google developer apps and a Temporal-based Docker stack.

### Cited Findings
**Pricing (Cloud)**
- Standard $29/mo, Team $39, Pro $49, Ultimate $99. Annual is $278 / $374 / $470 / $950 per year. Channels are 5 / 10 / 30 / 100. Every tier has a 7-day free trial — [Postiz docs: Plans and limits](https://docs.postiz.com/cloud/plans); [Postiz pricing](https://postiz.com/pricing)
- Public API, CLI and MCP are included on all four tiers, including the $29 Standard plan — [Postiz docs: Plans and limits](https://docs.postiz.com/cloud/plans)
- Post limits conflict. The official pricing page shows unlimited posts. ColdIQ reports "400 to unlimited", and Blotato (a competitor) says an FAQ mentions a 400-post cap on Standard — [ColdIQ](https://coldiq.com/tools/postiz); [Blotato: Postiz vs Publer](https://www.blotato.com/blog/postiz-vs-publer). **Flag: conflicting.** 400/month would still be plenty for one person.
- There is no free Cloud tier. The free option is self-hosting the AGPL-3.0 code on your own infrastructure — [bestsocialmediascheduler.com](https://bestsocialmediascheduler.com/reviews/postiz)

**Networks**
- Supports Facebook, Instagram, Threads, Bluesky and YouTube, among "30+" platforms — [Mintlify mirror of postiz-app docs](https://www.mintlify.com/gitroomhq/postiz-app); [Railway template](https://railway.com/deploy/postiz-open-source-social-media-scheduler-for-30-platforms--deploy-postiz). One listing says 19 platforms, which looks stale — [AlternativeTo](https://alternativeto.net/software/postiz/about)
- A stand-alone Instagram provider (no Facebook Business Page needed) was added in Jan 2025 — [r/selfhosted release thread (Jan 2025)](https://redlib.hackliberty.org/r/selfhosted/comments/1i5qnzq/postiz_v1281_opensource_social_media_scheduling/m874qc6/?context=3)

**API**
- `POST /posts` accepts `type` = `now` | `schedule` | `draft` — [third-party MCP write-up of the Postiz Public API](https://glama.ai/mcp/servers/@manbodyslam/mcp-postiz/blob/9bb58633f68606d49925b82e915c59429ba16519/POSTIZ_API_INFO.md)
- Rate limits conflict. The official docs say 90 requests/hour (100 on Cloud), counted only on the create-post endpoint, and batching several posts into one call helps — [Postiz Public API intro](https://docs.postiz.com/public-api/introduction). A Mintlify mirror and a third-party README say 30 requests/hour across all endpoints — [Mintlify rate limits](https://www.mintlify.com/gitroomhq/postiz-app/api/rate-limits). Self-hosters can change it with the `API_LIMIT` env var — [Postiz Public API intro](https://docs.postiz.com/public-api/introduction). **Flag: conflicting.** The 30/h figure is probably older.
- API and CLI use an API key and suit scripts and CI pipelines — [Postiz docs: Plans and limits](https://docs.postiz.com/cloud/plans)
- A CLI for managing posts exists — [Postiz CLI docs](https://docs.postiz.com/cli/managing-posts)

**MCP**
- Official MCP server, hosted for Cloud. It exposes Postiz actions as tools and supports OAuth login — [Postiz MCP page](https://postiz.com/mcp); [Postiz docs: Plans and limits](https://docs.postiz.com/cloud/plans)
- Typical agent flow: list connected accounts, fetch each platform's rules, then schedule the post. On self-host, the MCP server starts with the backend and is reachable at `/mcp` (Bearer), `/mcp/:apiKey` (key in URL) and `/mcp-oauth` (OAuth) — [search summary of Postiz MCP docs, via aitoolsatlas/lobehub listings](https://aitoolsatlas.ai/tools/postiz/review)
- Regenerating the Public API key in Settings → Developers breaks every MCP client still using the old key — [lobehub: postiz-mcp](https://lobehub.com/mcp/antoniolg-postiz-mcp)
- Community MCP servers also exist (e.g. antoniolg/postiz-mcp) — [lobehub](https://lobehub.com/mcp/antoniolg-postiz-mcp); [mcpservers.org](https://mcpservers.org/vi/servers/postiz-mcp)

**Human-in-the-loop**
- Every post has a public preview page. The link shows the rendered post, its scheduled date and a comment box, and comments come back attached to that post. The docs recommend "Save as Draft so nothing can publish while it is under review" — [Postiz docs: Approvals](https://docs.postiz.com/general/approvals)
- No "approved" flag blocks publishing. You move a post from draft to scheduled yourself. Preview links are not password-protected, so treat them as unlisted, not private — [Postiz docs: Approvals](https://docs.postiz.com/general/approvals)
- Team features include comments on drafts and post approvals — [Mintlify mirror](https://www.mintlify.com/gitroomhq/postiz-app)

**Reviews**
- A review site says MCP setup "requires technical setup — not plug-and-play for non-developers" and analytics are less mature than established paid schedulers — [aitoolsatlas](https://aitoolsatlas.ai/tools/postiz/review)
- Positive self-host feedback on Product Hunt: "self hosting it … for about a year … really impressed" — [Product Hunt](https://www.producthunt.com/p/postiz/postiz-2?page=2)

### Inferences
- Workflow fit: a scheduled Claude session writes posts and calls MCP or the API with `type: draft`. He opens the preview link or the Postiz UI on his phone, edits, then schedules. This covers Threads, IG and YT Shorts in one tool for £22–23/mo on Cloud.
- Because approval is not enforced, the agent's MCP or API credentials can also publish (`type: now`). The guardrail has to live in the prompt or a wrapper, or come from giving the agent only a draft-only path (see Q8).

### Gaps
- I couldn't verify the exact MCP tool names, whether the MCP can create drafts as opposed to only scheduling, or whether Postiz is listed as a Claude.ai connector. The official pages were unreachable.
- IG carousel/Reels and YouTube Shorts specifics in Postiz were not confirmed by any source.
- No Postiz UK-specific issues were found. As a SaaS, it should be usable from the UK (unverified).

## Q2. Postiz self-hosting: requirements, developer apps, maintenance, license

### Takeaway
Self-hosting is free in licence terms but not in effort. Since v2.12 it needs a Temporal stack, which the official compose file bundles. Plan on a 4 GB VPS (roughly $5–10/mo). You must register your own Meta app (Threads, Instagram) and Google/YouTube app. For posting only to your own accounts, Meta development mode with yourself as tester avoids App Review.

### Cited Findings
- Since v2.12.0, Postiz uses Temporal for scheduled posts and background workflows. The official docker-compose ships Postgres, Redis and Temporal pre-wired — [Postiz docs: System requirements](https://docs.postiz.com/self-host/installation/system-requirements); [Postiz docs: Migration to Temporal](https://docs.postiz.com/installation/migration)
- The compose stack was tested on a 2 GB / 2 vCPU Ubuntu VM with "no headroom". Docs recommend 4 GB or more, and source builds can run out of memory at 2 GB — [Postiz docs: System requirements](https://docs.postiz.com/self-host/installation/system-requirements); [OSSAlt guide](https://ossalt.com/guides/self-host-postiz-2026)
- Ports: host 4007 maps to container 5000. Temporal uses 7233 (frontend) and 8080 (UI) — [Postiz docs: System requirements](https://docs.postiz.com/self-host/installation/system-requirements)
- Temporal adds "a significant leap in operational complexity". There is a production debugging runbook — [DEV: Debugging Postiz + Temporal](https://dev.to/klytron/debugging-postiz-temporal-a-production-runbook-for-self-hosted-social-media-orchestration-560f)
- Some env vars are undocumented. One self-hoster writes about "the env vars the docs don't tell you about" — [DEV: Self-hosted Postiz with Tailscale](https://dev.to/aryaniyaps/how-i-self-hosted-postiz-with-tailscale-and-the-env-vars-the-docs-dont-tell-you-about-4i8g)
- Threads setup: create a Meta app, choose the Threads API, add the `threads_basic` and `threads_content_publish` permissions, set `THREADS_APP_ID` and `THREADS_APP_SECRET`, and set the redirect URI to `<frontend>/integrations/social/threads`. If the env vars are missing, Threads does not appear in the channel list. Docs call it "complex", say "the Threads API seems like it's having issues", and point users to Discord — [Postiz docs: Threads provider](https://docs.postiz.com/providers/threads)
- Instagram and Facebook require Meta app approvals and "can be complicated to set up" — [search summary of a third-party listing](https://www.bestaitools.com/tool/postiz)
- Meta's docs: without Advanced Access for `threads_content_publish`, you can post only for your own account and your app's tester accounts. Advanced Access needs App Review plus Tech Provider verification (about a week, per one guide) — [Meta: Threads Create Posts](https://developers.facebook.com/docs/threads/create-posts); [Meta: Threads get started](https://developers.facebook.com/documentation/threads/get-started); [Nango guide](https://nango.dev/docs/api-integrations/threads/how-to-register-your-own-threads-api-oauth-app)
- In Development mode, only Admin, Developer or Tester roles can authorize, and a pending tester invite blocks auth — [Nango guide](https://nango.dev/docs/api-integrations/threads/how-to-register-your-own-threads-api-oauth-app)
- Threads long-lived tokens last 60 days, so refresh logic matters — [bundle.social blog: Threads posting API](https://bundle.social/blog/threads-posting-api)
- The Postiz maintainer said on Reddit that approval is needed for public use but not for internal use. A private app lets the creator automate their own account and add test users — [r/selfhosted 2024 thread](https://redlib.hackliberty.org/r/selfhosted/comments/1fl8n2b/postiz_v130_opensource_social_media_scheduling/m7gl5lj/?context=3)
- License: AGPL-3.0 — [bestsocialmediascheduler.com](https://bestsocialmediascheduler.com/reviews/postiz)

### Inferences
- For one user posting to his own accounts, self-host works without Meta App Review by keeping the apps in dev mode with himself as admin or tester. YouTube likely needs a Google Cloud OAuth app. Unverified apps in "testing" status have short-lived refresh tokens (my general knowledge, not sourced here), which would mean re-auth.
- Maintenance burden is about 5 containers (app, Postgres, Redis, Temporal, Temporal UI), with upgrades, backups, token expiry and Meta API changes to handle. For someone with a full-time job, Cloud at $29 probably beats the time cost. Self-host makes sense mainly to get to £0 or to get full control and no post caps.
- The Claude cloud agent needs network reach to the self-hosted `/mcp` endpoint, so it must be publicly reachable over HTTPS. That increases the attack surface; a Tailscale-only setup would not be reachable from Anthropic's cloud.
- AGPL only matters if he modifies the code and offers it as a network service to others. Personal use has no practical impact.

### Gaps
- I couldn't confirm the current latest Postiz version or the exact Temporal resource needs. GitHub access was denied.
- Not confirmed: whether Instagram via "Instagram Login" needs App Review for your own professional account (likely dev-mode OK, unverified).

## Q3. Typefully

### Takeaway
Typefully has a good API v2 and a hosted MCP, with free-tier API access, but it does **not** support Instagram or YouTube. It covers only his Threads needs (plus X, LinkedIn, Bluesky, Mastodon), so it cannot be the main tool for this workflow.

### Cited Findings
- API v2 supports Threads, Bluesky, LinkedIn and Mastodon (v1 was X-only). v1 keys do not work with v2 — [Typefully support: v1→v2 migration guide](https://support.typefully.com/en/articles/13133296-typefully-api-v1-v2-migration-guide)
- The MCP covers X, LinkedIn, Threads, Bluesky and Mastodon. It can create drafts, schedule, upload media and view the queue. Sources disagree on auth: one says OAuth at `mcp.typefully.com/mcp` with no API key, another says API key — [Pallyy: 12 social media MCP servers](https://pallyy.com/blog/social-media-mcp-servers); [Eden blog](https://eden.so/blog/best-social-media-mcp-servers/); [Composio toolkit](https://composio.dev/toolkits/typefully)
- Pricing conflicts. One guide (checked 2 Oct 2026) lists Free at 10 posts/mo, Creator at $99/yr, and Business at $20/social set/mo ($18 yearly). Older sources say Creator $19/mo and Business $39/mo — [Postel: Typefully pricing](https://www.postel.app/typefully-pricing); [voicemoat](https://voicemoat.com/blog/typefully-pricing-2026-breakdown); [Capterra](https://www.capterra.com/p/10015231/Typefully/). **Flag: conflicting / likely changed in 2026.**
- Recent guides say API, MCP and agent access are on the free plan — [Postel](https://www.postel.app/typefully-pricing)
- No Instagram, TikTok, YouTube or Substack. Instagram reportedly appears only in homepage marketing copy — [socialk.it](https://socialk.it/en/alternatives/typefully); [Blotato: Typefully alternatives (competitor)](https://www.blotato.com/blog/typefully-alternatives); [SocialRails review](https://socialrails.com/blog/typefully-review)

### Inferences
- Typefully is drafts-first, which suits approval flows, but missing IG and YT rules it out as the primary tool. It could be a free add-on for Threads or X text posts only.

### Gaps
- Official pricing in GBP and whether Instagram was added in late 2026 could not be verified directly.

## Q4. Blotato

### Takeaway
At $29/mo (about £23) for 9 platforms (including Threads, IG, YouTube, Bluesky, Facebook, TikTok), Blotato has an API and a hosted MCP. API and MCP need a paid plan; they are not available in the trial. There is no evidence of a built-in approval queue. Much of the online coverage is Blotato's own marketing.

### Cited Findings
- Plans: Starter $29/mo (20 social accounts, 1,250 AI credits), Creator $97, Agency $499. 7-day trial — [Blotato research page](https://www.blotato.com/research/social-media-agent-pricing); [scheduler.social review](https://scheduler.social/schedulers/blotato); [PlugKit](https://www.plugkit.co/blog/blotato-pricing-api-alternatives/)
- API and MCP are not in the 7-day trial, and generating an API key activates paid Starter. No separate MCP fee — [PlugKit](https://www.plugkit.co/blog/blotato-pricing-api-alternatives/); [Blotato MCP page](https://www.blotato.com/mcp)
- MCP hosted at `mcp.blotato.com/mcp`. The tool count conflicts across Blotato's own pages (35 vs 13) — [Blotato MCP page](https://www.blotato.com/mcp); [Blotato blog: best MCP servers](https://www.blotato.com/blog/best-social-media-mcp-servers)
- Platforms (9): Instagram, TikTok, LinkedIn, Facebook, X, Threads, Bluesky, Pinterest, YouTube — [Blotato social media API](https://www.blotato.com/social-media-api)
- Blotato's own daily caps are stricter than the platforms' on some networks, e.g. Instagram 50/account/24h and Facebook 25/Page/24h. Threads and Bluesky defer to platform limits — [Blotato social media API](https://www.blotato.com/social-media-api)
- The "drafts" in the UI are AI-generated per-platform drafts from a source that you then edit — [Blotato help: first 5 posts](https://help.blotato.com/start/posts)
- Analytics skip LinkedIn. AI image and video run on monthly credits — [scheduler.social](https://scheduler.social/schedulers/blotato)
- Has an n8n node — [npm/yarn n8n-nodes-blotato](https://classic.yarnpkg.com/en/package/n8n-nodes-blotato)

### Inferences
- Since Claude writes the content, Blotato's AI credits add little value for him. He would pay $29 mostly for the posting API. Postiz Cloud costs the same and has preview links for approval.

### Gaps
- No confirmed API-level draft or approval state. Trustpilot reviews exist but weren't read in detail.

## Q5. Late → Zernio (getlate.dev)

### Takeaway
Late has rebranded to Zernio (getlate.dev redirects to zernio.com). It is a unified posting API with per-account pricing where the **first 2 accounts are free**, plus a hosted MCP at mcp.zernio.com. With 3 accounts (Threads, IG, YT) it would cost about $6/mo. It is infrastructure, not an app: it has no calendar UI and no confirmed approval UI.

### Cited Findings
- getlate.dev now redirects to zernio.com, and the old SDKs work for a grace period (vendor claim) — [Zernio blog](https://zernio.com/blog/unified-social-media-api)
- Per-account pricing: first 2 accounts free, $6 each for accounts 3–10, $3 for 11–100, $1 above that. X API costs are passed through at cost — [Blotato: Zernio alternatives (competitor)](https://www.blotato.com/blog/zernio-alternatives); [hypertools review](https://hypertools.so/tool/zernio); [Mintavocado 10-day test](https://mintavocado.com/en/zernio-api-reseaux-sociaux-solopreneur-en/)
- Older tier model: Build $19/mo (120 posts, 10 profiles), Accelerate $49/mo. Likely stale — [DEV Community roundup](https://dev.to/jesse_eisenbart/the-7-best-social-media-apis-for-developers-ai-agents-in-2026-3e15). **Flag: conflicting/stale.**
- 16 platforms, including Instagram, TikTok, YouTube, X, LinkedIn, Facebook and Threads — [OpenTweet vs Zernio](https://opentweet.io/vs/zernio); [dupple review (Sep 2026)](https://dupple.com/tools/zernio)
- Hosted MCP at mcp.zernio.com with OAuth or Bearer API key. Works with Claude, ChatGPT, Cursor, Codex and VS Code. Exposes publishing, messaging and analytics. The vendor claims 496 tools — [Socialync: does Zernio have an MCP?](https://www.socialync.io/mcp-server/zernio); [Zernio blog](https://zernio.com/blog/unified-social-media-api). One comparison wrongly says it has no MCP — [schedulenchill](https://schedulenchill.com/postiz-vs-schedule-and-chill)
- "Infrastructure rather than an end-user app", with no drag-and-drop scheduler or editorial calendar — [dupple](https://dupple.com/tools/zernio)
- Reviews exist on Trustpilot and Capterra under both "Late" and "Zernio" — [Trustpilot](https://es.trustpilot.com/review/zernio.com); [Capterra](https://www.capterra.ae/software/1085150/Late)

### Inferences
- Cheapest hosted option for exactly 3 platforms. Approval would have to be DIY, e.g. Claude writes drafts to a GitHub file, Notion or an artifact, and a second step posts after approval.
- A 496-tool MCP is very large. Loading it into a Claude context may be costly and noisy.

### Gaps
- No source confirms a draft state in the Zernio API. IG carousel/Reels and YT Shorts detail unconfirmed.

## Q6. Ayrshare

### Takeaway
Ayrshare is mature and reliable but far over budget. Premium is about $149/mo for one profile, with no permanent free plan. It has two MCP servers: a free read-only docs MCP, and an "Action" MCP that needs a paid API plan. Not suitable at £0–30.

### Cited Findings
- Premium $149/mo (1 profile), Launch $299 (up to 10), Business $599 (30), Enterprise custom. No permanent free plan; 28-day trial (others say 14-day) — [social-api.ai (competitor)](https://social-api.ai/blog/ayrshare-pricing-social-media-api-2026); [G2](https://www.g2.com/products/ayrshare-api/pricing); [That Marketing Buddy](https://thatmarketingbuddy.com/software/ayrshare). Annual $129/mo is unverified. **Flag: competitor sources.**
- Two MCPs: the docs MCP is free and read-only, and the Action MCP can publish and needs an API plan (from $149). One review claims profile management via MCP needs the $599 Business plan (conflicting) — [PlanVortex: Ayrshare MCP](https://planvortex.com/en/resources/ayrshare-mcp-server)

### Inferences
- Exclude on budget.

### Gaps
- Official ayrshare.com/pricing could not be fetched.

## Q7. Upload-Post, bundle.social, and other notable options

### Takeaway
**Upload-Post** has a permanent free plan (2 profiles, 10 uploads/mo, full API, MCP), and Basic costs $24/mo or $16/mo annual with unlimited uploads. It is the cheapest paid flat plan that covers Threads, IG and YouTube. **bundle.social** has a free API tier (about 20 posts/mo) and an official MCP, but its next plan is $100/mo. Others worth noting: Post for Me (MCP, bring-your-own developer credentials), Outstand (hosted MCP, $19/mo), and Schedule & Chill (free, has MCP, fewer networks).

### Cited Findings
**Upload-Post**
- Free: 2 profiles, 10 uploads/mo, full REST API, no card. Basic $24/mo ($16 annual), 5 profiles, unlimited uploads. Professional $50 ($33 annual), 25 profiles — [Upload-Post: Postiz alternative (vendor)](https://www.upload-post.com/postiz-alternative/); [Blotato: Upload-Post pricing (competitor)](https://www.blotato.com/blog/upload-post-pricing); [LinkStartAI review](https://www.linkstartai.com/en/agents/upload-post)
- MCP on every plan including Free. Described as an open-source MCP with about 40 tools — [Upload-Post: Blotato alternative (vendor)](https://www.upload-post.com/blotato-alternative/); [LinkStartAI](https://www.linkstartai.com/en/agents/upload-post)
- Platforms: TikTok, Instagram, YouTube, LinkedIn, X, Facebook, Threads, Pinterest, Reddit, Bluesky. Other vendor pages claim "20+" or 22 — [Upload-Post FAQ](https://www.upload-post.com/postiz-alternative/); [Upload-Post Buffer alternative](https://www.upload-post.com/buffer-alternative/); [Upload-Post llms-full.txt](https://www.upload-post.com/llms-full.txt)
- Mostly vendor-sourced; numbers unverified.

**bundle.social**
- Free $0, Pro $100/mo (10,000 posts), Business $400/mo (100,000), Enterprise custom. Paid plans have unlimited accounts — [bundle.social](https://bundle.social/)
- Free tier includes API access and 20 posts/mo — [That Marketing Buddy review](https://thatmarketingbuddy.com/software/bundle-social)
- Official MCP server, CLI and typed SDK, with tools like `create_post` and `schedule_post` — [bundle.social: MCP server](https://bundle.social/social-media-mcp-server); [bundle.social: Cursor](https://bundle.social/cursor-social-media)
- Per a review dated Oct 2026, the MCP runs locally with an API key and a hosted version is on the roadmap. DMs are allowlist-only — [That Marketing Buddy](https://thatmarketingbuddy.com/software/bundle-social)
- 15 platforms per the vendor; one review says 14+ — [bundle.social AI agents page](https://bundle.social/social-media-api-for-ai-agents)

**Others**
- Post for Me ships an MCP plus bring-your-own developer credentials. Outstand has a hosted MCP with 28 tools at $19/mo — [Blotato pricing study (competitor)](https://www.blotato.com/research/social-media-agent-pricing)
- Schedule & Chill is a free alternative with an MCP but fewer networks — [schedulenchill](https://schedulenchill.com/bundle-social-vs-schedule-and-chill)
- MCP roundups for wider scanning — [Pallyy: 12 MCP servers](https://pallyy.com/blog/social-media-mcp-servers); [Socialync: best MCP servers 2026](https://www.socialync.io/blog/best-social-media-mcp-servers-2026); [Breakreach](https://www.breakreach.com/best/mcp-servers-for-social-media)

### Inferences
- Upload-Post's free tier (10 uploads/mo across 2 profiles) could prototype the pipeline at £0. Basic at about £13–19/mo is the cheapest flat paid plan covering all three of his main networks. It is upload-focused (video-first heritage), so check Threads text-only and IG carousel support.
- bundle.social's free tier (20 posts/mo) also works for a £0 prototype, but the jump to $100 is steep.

### Gaps
- Draft or approval support in Upload-Post and bundle.social was not confirmed. bundle.social's tier names and limits differ between vendor and review.

## Q8. Connecting to Claude (cloud scheduled sessions), security, human-in-the-loop design, Chinese platforms

### Takeaway
Hosted MCPs (Postiz, Typefully, Blotato, Zernio) can be added as remote MCP servers. A Claude Code cloud session can also just call the REST API with a key stored as an environment secret, which is often simpler and allows draft-only enforcement. None of these tools posts to a Facebook *personal profile* or Xiaohongshu; both stay manual, as he planned.

### Cited Findings
- Postiz MCP endpoints: `/mcp` (Bearer), `/mcp/:apiKey` (key in URL) and `/mcp-oauth` — [search summary of Postiz MCP docs](https://aitoolsatlas.ai/tools/postiz/review)
- Zernio MCP auth via OAuth or Bearer key; works with Claude — [Socialync](https://www.socialync.io/mcp-server/zernio)
- Postiz has no publish-blocking approval flag, and preview links are unauthenticated — [Postiz docs: Approvals](https://docs.postiz.com/general/approvals)
- Xiaohongshu has no open self-serve posting API (vendor claim). Only scrapers and an unofficial `xiaohongshu-mcp` Claude skill exist (7 installs), and automation may break ToS — [Phyllo](https://www.getphyllo.com/rednote-api); [skillselion: xiaohongshu-workflow](https://skillselion.com/skills/aaaaqwq/agi-super-skills/xiaohongshu-workflow)

### Inferences
- **Security:** an API key or MCP token that can publish lets a prompt-injected or buggy agent post publicly. Mitigations:
  1. Have the agent call the REST API through a small wrapper or prompt rule that only ever sends `type: "draft"`.
  2. Avoid the `/mcp/:apiKey` URL form, because it leaks the key into logs and config.
  3. Store keys as cloud environment secrets.
  4. Rotate keys, remembering that rotation breaks existing MCP configs.
- **Recommended human-in-the-loop design:** Claude creates drafts, then sends him a notification with the preview link. He approves and schedules from the phone UI. Postiz's draft and preview-link flow fits this natively. With API-only tools (Zernio, Upload-Post), approval has to be built separately, e.g. Claude writes candidates to a repo or doc and a second run publishes the ones he approved.
- **Facebook:** all of these tools post to Facebook *Pages* only. Meta's API has not allowed personal-profile publishing since 2018 (general knowledge, not re-sourced here).
- **Budget ranking for his needs (Threads + IG + YT Shorts, approval step):**
  1. Postiz Cloud Standard at $29 (about £23): best HITL support and full coverage.
  2. Zernio at about $6/mo for 3 accounts: cheapest, but you build approval yourself.
  3. Upload-Post Basic at $16–24.
  4. Postiz self-host at £0 plus a VPS and your own Meta and Google apps: most work.
  - Blotato is redundant with Claude doing the writing. Typefully lacks IG and YT. Ayrshare and bundle.social Pro are over budget.

### Gaps
- No tool was verified as an official Anthropic Claude.ai Connector directory entry.
- Exact `claude mcp add` commands per vendor were not confirmed from official docs, because the domains were blocked. To re-verify, allow postiz.com, docs.postiz.com, typefully.com, blotato.com, zernio.com, upload-post.com and ayrshare.com in the session network settings.
- UK availability: no tool showed UK restrictions in the results, but this was not explicitly checked. GBP pricing was not found for any tool; all list USD.
