# AI-assisted end-to-end social content workflows for solo creators (2025–2026): what to automate vs keep human

Research date: 2026-10-28. Method: web search plus snippet/aggregator review. Note: a direct fetch of buffer.com failed because the domain is not on this session's allowed network list, so Buffer figures come from secondary summaries and need checking against the primary page. Claims from a vendor about its own product are marked **[vendor]**.

---

## 1. Documented solo / tiny-team AI-assisted workflows: realistic shape, time saved, failure modes

### Takeaway
No rigorous independent study measures time saved by solo creators. The evidence is self-reported creator write-ups and vendor claims, typically "10–15 h/week saved". The best population data (Buffer, 1.2M posts) shows AI-assisted posts perform slightly better. That data is from 2024, and Buffer attributes the gain to more consistent posting, not to better copy. The failure modes are well documented in 2025–2026: audiences punish undisclosed or "slop" AI content, and platforms (YouTube, Facebook, Xiaohongshu) now cut reach or monetization for mass-produced, unoriginal, or fully AI-run accounts.

### Cited Findings
**Performance and adoption data**
- Buffer analysed about 1.2M posts made with its AI Assistant against human-only posts across Facebook, LinkedIn, Pinterest, Threads, TikTok, X, and YouTube. Secondary summaries report a median engagement of 5.87% for AI-assisted posts vs 4.82% for non-AI posts. The study is dated **Oct 15, 2024 (older than 2025)**. Buffer attributes the gain to AI helping people publish more consistently, not to the AI copy itself. — [Buffer](https://buffer.com/resources/ai-assistant-post-performance/); [Indie Hackers summary](https://www.indiehackers.com/post/learning/buffer-analyzed-1-2-million-ai-posts-to-see-if-they-outperformed-human-content-4PGZVWttmETogcWnwuAa)
  - Caveat: Buffer is a vendor of AI posting tools, and the comparison is observational. Users who choose to use AI may differ from those who don't. A "Buffer 2025 study" claiming ~3.1% higher engagement circulates on a secondary site, but I could not trace it to Buffer, so treat it as unverified. — [GenSumo](https://gensumo.pages.dev/research/ai-vs-human-social-media-posts-report/)
- Hootsuite Social Trends 2026 reports that 79% of social media managers use AI daily, based on a survey of 6,500+ marketers. The same report says more than 30% of consumers are less likely to choose a brand whose ads are visibly AI-generated. Secondary coverage notes that the sample details for the 79% figure are not disclosed. — [thinkdigital.travel summary](https://www.thinkdigital.travel/research-directory/hootsuite-social-trends-2026); [Carahsoft copy of report](https://www.carahsoft.com/resources/28604-2026-social-media-trends-report)
- Social Media Examiner 2026 AI report: 32% of marketers say AI now touches the majority of their work. — [Social Media Examiner](https://aisociety.socialmediaexaminer.com/2026-ai-report/)
- Sociality.io 2026 survey: 89.7% of respondents use AI at least several times a week **[vendor survey]**. — [Sociality.io](https://www.sociality.io/blog/ai-in-social-media-marketing/)

**Self-reported solo workflows and time saved (anecdotal)**
- A DEV Community author reports going from about 6 h of manual work per video to under 15 min of oversight for an automated Shorts pipeline. This is a single-person anecdote. — [DEV](https://dev.to/tamayerd/from-zero-to-daily-content-my-ai-automation-journey-2h0h)
- Startup Ideas Podcast (May 2025) demos an n8n "content agent" with a claimed 3x engagement in 30 days and 10–15 h/week saved, with an optional human review step before publishing. These are demo claims, not a measured result. — [Audioscrape transcript](https://audioscrape.com/podcast/the-startup-ideas-podcast/episode/i-built-an-ai-content-agent-that-3x-my-engagement-in-30-days-full-n8n-workflow)
- A creator Substack describes an agent that turns one long article into multiple platform posts. — [Unpromptable](https://unpromptable.substack.com/p/i-built-an-ai-agent-that-ended-my)
- "Level 3 automation" write-up: a creator-led account of moving from assisted to autonomous content production. — [Augmented Startups](https://www.augmentedstartups.com/blog/building-an-autonomous-content-engine-my-journey-to-level-3-automation)
- An agency case study claims 32 h/week saved across a multi-client team **[vendor/agency]**. It is not a solo-creator data point. — [AppAiFlow](https://appaiflow.pages.dev/case-studies/agency-content-automation)

**Failure modes: "AI slop", trust, and platform penalties**
- In Sprout Social's Q3 2025 Pulse data (US/UK/AU, 2,000+ respondents), 52% of consumers ranked brands posting AI content without disclosure as a top concern. 55% are more likely to trust brands that commit to human-created content, and 46% are uncomfortable with AI influencers. — [Digital Information World](https://www.digitalinformationworld.com/2025/09/ai-disclosure-and-trust-define-social.html); [eMarketer](https://www.emarketer.com/content/ai-transparency--data-privacy-top-consumers--concerns-brands-on-social-media)
- In Sprout's Q1 2026 Pulse survey, unlabeled AI-generated content was the No. 1 brand turn-off (28%). 50% of Gen Z have blocked, muted, or unfollowed a brand or creator whose content felt like "AI slop". — [eMarketer](https://www.emarketer.com/content/hiding-ai-use-brands--biggest-social-media-sin)
- YouTube (July 15, 2025) renamed "repetitious content" to "inauthentic content" in its YPP monetization rules, targeting mass-produced and repetitive videos. YouTube says channels that use AI remain eligible, and creator liaison Rene Ritchie called it a "minor update". — [Social Media Today](https://www.socialmediatoday.com/news/youtube-clarifies-monetization-update-inauthentic-repeated-content/752892/); [Plagiarism Today](https://www.plagiarismtoday.com/2025/07/08/youtube-targets-inauthentic-content/); [Windows Central](https://www.windowscentral.com/software-apps/youtube-ramps-up-campaign-against-ai-slop-with-stricter-monetization-caveats-on-inauthentic-and-repetitive-videos)
- Facebook (July 14, 2025) began reducing distribution and monetization for accounts that repeatedly repost others' content without credit. Duplicate posts are detected automatically. Meta reported action against about 500k spammy accounts and removal of about 10M impersonating profiles in H1 2025. Commentary and a "unique take" are not targeted. — [MediaNama](https://www.medianama.com/2025/07/223-meta-cracks-down-on-unoriginal-facebook-content/); [Storyboard18](https://www.storyboard18.com/digital/after-youtube-meta-crackdowns-on-unoriginal-content-removes-10-million-fake-facebook-profiles-74532.htm); [PPC Land](https://ppc.land/facebook-introduces-stronger-measures-against-unoriginal-content-creators/)
- Xiaohongshu (2026) has the strictest rules against fully AI-run accounts:
  - **Feb 2026:** reduced distribution for AI content that is not self-labelled, and the platform labels it itself using detection.
  - **Mar 10, 2026:** an announcement against "AI 托管账号" (AI-managed accounts). Occasional AI ghost-writing, posting, or interaction on a normal account brings a warning or reduced distribution. Accounts registered, posting, and interacting through AI-hosting tools, or whose public notes are all AI-posted, are **banned**.
  - **Apr 27, 2026:** AI content governance rules with graded penalties and an appeal channel for labelling disputes.
  - National rule (China): the 《人工智能生成合成内容标识办法》 requires explicit and implicit labels on AI text, images, audio, and video from Sept 1, 2025.
  - Sources: [The Paper](https://www.thepaper.cn/newsDetail_forward_32747698); [The Paper](https://www.thepaper.cn/newsDetail_forward_32599956); [GMW 2026-03-10](https://m.gmw.cn/2026-03/10/content_1304371172.htm); [Yangtse Evening Post](https://www.yzwb.net/news/txs/202509/t20250901_257831.html); [IThome](https://www.ithome.com/0/944/156.htm)
  - A Sohu article claims an Aug 2026 rule with an "AI participation >30%" threshold for virtual-human accounts. I could not corroborate it, so it is unverified. — [Sohu](https://m.sohu.com/a/1060134772_122066679)

### Inferences
- A realistic solo workflow is "AI as research assistant + first-draft writer + format adapter, with the human as editor-in-chief and the only voice in comments". Consistency, which AI enables through batching, seems to drive more of the engagement gain than AI copy quality does.
- Fully autonomous posting is now a measurable ban or reach risk on Xiaohongshu, and a reach risk on Facebook and YouTube if the output becomes repetitive or templated. A low-volume, high-originality project like alzheimer-companion should avoid volume-driven automation.

### Gaps
- No independent, controlled 2025–2026 study of time saved for solo creators. All hour figures are self-reported or vendor-reported.
- I could not fetch the Buffer primary page (domain blocked here), so per-platform figures (including Threads) are not verified.
- No public data on engagement drops for health or caregiving accounts specifically after adopting AI.

---

## 2. How LLM agents (Claude Code + skills/MCP, ChatGPT, n8n agents) are used for listening, ideation, brand-voice drafting, multi-platform adaptation, and human-in-the-loop (HITL) approval

### Takeaway
The dominant documented pattern is a staged pipeline: research agent → writer agent (with a brand-voice/style file) → per-platform adapter → **human approval gate** (Notion/Airtable status, Slack/Telegram button) → scheduler API. Community Claude Code skills exist for repurposing and cross-posting. Publishing goes through a scheduler's MCP endpoint (Postiz, Blotato), not direct platform automation. Practitioners explicitly warn against letting agents publish without guard rails.

### Cited Findings
- n8n LinkedIn pipeline template: research agent → writing agent → human approval → publishing agent, with a claim of 10+ h/week saved **[vendor]**. — [GrowwStacks](https://growwstacks.com/blog/automate-viral-linkedin-posts-ai-agents-n8n/); [GrowwStacks GPT-4o approval workflow](https://www.growwstacks.com/workflows/streamline-content-creation-with-gpt-4o-and-one-click-human-review-approvals); [GrowwStacks blog approval case](https://growwstacks.com/case-studies/apps/automate-blog-post-creation-ai-approval)
- A concrete HITL example: an n8n + Airtable + Softr setup keeps drafts in "Ready for Review" until a human approves them. Approval flips the status, and the system auto-publishes to LinkedIn and Facebook at the scheduled time. — [Freelancehunt showcase](https://freelancehunt.com/en/showcase/work/n8n-fabryka-tresci-airtable-softr/2000829.html)
- Claude Code skills for social content:
  - `social-media-content-repurposer` turns long-form content into drafts for LinkedIn, X, Instagram, and Threads, aimed at developers. — [claudemarketplaces](https://claudemarketplaces.com/skills/onewave-ai/claude-skills/social-media-content-repurposer); [Skillselion](https://skillselion.com/skills/onewave-ai/claude-skills/social-media-content-repurposer)
  - A `crosspost` skill (everything-claude-code) adapts posts to X, LinkedIn, Threads, and Bluesky conventions such as character limits. — [killer-skills](https://killer-skills.pages.dev/en/skills/affaan-m/everything-claude-code/crosspost)
  - Blotato's Claude skill pack includes a post-scheduler that publishes over MCP to 9 platforms. Without MCP, it saves the post to a file for manual pasting **[vendor]**. — [Blotato](https://www.blotato.com/tools/claude-skills)
- MindStudio guides **[vendor]**:
  - Stage generated content in a Notion database for human review before publishing.
  - Use a two-pass approach (core message first, then per-platform adaptation), because one large prompt for many platforms gives weaker results.
  - Keep reusable "skill" files for brand voice.
  - Sources: [Repurposing engine](https://www.mindstudio.ai/blog/content-repurposing-engine-claude-code); [Claude Code skills for repurposing](https://www.mindstudio.ai/blog/claude-code-skills-social-media-content-repurposing); [content marketing skill system](https://www.mindstudio.ai/blog/claude-code-content-marketing-skill-system)
- Postiz (open source, AGPL-3.0, self-hostable):
  - Schedules to X, Instagram, LinkedIn, Facebook, TikTok, YouTube, Reddit, Threads, Bluesky, Mastodon, Pinterest, and Discord.
  - Offers a REST API, n8n/Make/Zapier integration, and an MCP endpoint (`/api/mcp/{API_KEY}`). A third-party MCP wrapper exposes 22 tools for scheduling, media, and analytics.
  - Hosting costs about $5–10/month on Railway.
  - The MCP wrapper's author warns that "letting an AI agent loose on it without guard rails is a fast way to send the wrong draft to the wrong account."
  - Sources disagree on whether v2.12+ requires Temporal.
  - Sources: [Railway template](https://railway.com/deploy/postiz-open-source-social-media-scheduler-for-30-platforms--deploy-postiz); [Postiz MCP project](https://solomonneas.dev/projects/postiz-mcp); [r/selfhosted thread](https://reddit.birdcat.cafe/r/selfhosted/comments/1jzsfav/postiz_v1392_opensource_social_media_scheduling/mncot3u/?context=3)
- Chinese-platform agent skills exist, for example a "social-hotsearch" skill on ClawHub that pulls hot-search lists. — [ClawHub](https://clawhub.ai/supermalo/social-hotsearch)

### Inferences
- A fitting stack for this user:
  - Claude Code with a project `brand-voice.md` and a "do-not-say" list (no medical claims, "not a medical device").
  - Skills for research digest → topic shortlist → drafts per platform (Threads, IG caption, FB Page, Reddit, XHS in Simplified/Traditional Chinese).
  - Drafts go to a review queue, either a git folder or Postiz drafts.
  - The human approves and edits, then Postiz/Meta native schedulers publish.
  - Reddit and Xiaohongshu stay manual-post.
- The approval gate is the consistent best practice in every documented workflow. No source recommends unattended publishing for a brand with reputational stakes.

### Gaps
- No official Anthropic or OpenAI case study specific to social media operations was found in this pass.
- No measured data on whether brand-voice files actually reduce "AI-sounding" copy.

---

## 3. Free or cheap social listening and trend research (Reddit, Threads, Facebook, YouTube, Xiaohongshu)

### Takeaway
Reddit listening got harder after GummySearch closed under Reddit's Data API commercial terms. F5Bot (free keyword email alerts) remains the zero-cost baseline, and Syften (~$20/mo) is the paid step up. Threads has an official keyword-search API (500 queries per 7 days). Facebook groups have no legitimate listening API, so listening there means manual membership. For Xiaohongshu: the official creator center (free), the free tiers of 灰豚/千瓜, and in-app search suggestions.

### Cited Findings
- **GummySearch** stopped new subscriptions on Nov 30, 2025, because it could not reach an agreement under Reddit's Data API usage policy, which requires a commercial licence. Sources disagree on the final shutdown date: Nov 2025, or Nov 30, 2026 for existing paid users. — [SyncsUp Substack](https://syncsuptech.substack.com/p/gummysearch-shuts-down); [DEV (wubingwx)](https://dev.to/wubingwx/gummysearch-shut-down-here-are-the-reddit-research-alternatives-for-indie-hackers-2akc); [DEV (devtoolpicks)](https://dev.to/devtoolpicks/best-gummysearch-alternatives-in-2026-honest-picks-for-solo-devs-and-indie-hackers-4af9)
- **F5Bot** is free keyword email alerts for Reddit, Hacker News, and Lobsters. It is a notifier only, with no analysis. **Syften** is paid monitoring from about $19.95/mo with Slack integration. Comparisons are often written by competing vendors. — [xpoz comparison (vendor)](https://www.xpoz.ai/blog/comparisons/best-gummysearch-alternatives-2026/); [DEV (devtoolpicks)](https://dev.to/devtoolpicks/best-gummysearch-alternatives-in-2026-honest-picks-for-solo-devs-and-indie-hackers-4af9); [rawneed guide](https://rawneed.pages.dev/guides/best-gummysearch-alternatives/)
- **Threads API:**
  - A keyword search endpoint requires the `threads_keyword_search` permission and is limited to 500 queries per rolling 7 days.
  - Since Dec 2024, you can reply to, repost, or quote posts surfaced by keyword or mention search.
  - Insights cover views, likes, replies, reposts, quotes, and shares.
  - Long-lived tokens last 60 days.
  - Sources: [Meta dev blog (Dec 2024)](https://developers.facebook.com/blog/post/2024/12/09/discover-ideas-with-the-threads-api/); [Threads API reference](https://developers.facebook.com/documentation/threads/reference); [Threads changelog](https://developers.secure.facebook.com/docs/threads/changelog); [PPC Land](https://ppc.land/meta-introduces-new-search-and-analytics-features-to-threads-api-platform/); [Social Media Today](https://www.socialmediatoday.com/news/meta-adds-more-functionality-threads-api/735139/)
- **Xiaohongshu:**
  - The official 创作服务平台 (creator center) gives free note, follower, and engagement data.
  - 灰豚数据 has a reported free tier of 100 queries/day with keyword analysis (one third-party 2026 tutorial, unverified).
  - 千瓜 offers hot-word rankings (increment and total lists) and keyword heat trends.
  - Manual keyword mining from the search dropdown, "猜你想搜", and "搜索发现" is also common.
  - Sources: [tixiaolu tutorial](https://www.tixiaolu.com/v2/posts/v2-14ad9daa.html); [woshipm](https://www.woshipm.com/operate/4139337.html); [woshipm](https://www.woshipm.com/operate/5854784.html); [ganhuoku](https://ganhuoku.cn/archives/131837)
- Metricool's free plan includes analysis of up to 5 competitors, which serves as lightweight competitor tracking. — [Social Champ (competitor vendor)](https://www.socialchamp.com/blog/metricool-pricing/); [inmagic review](https://inmagic.ai/metricool-review/)

### Inferences
- A cheap listening setup:
  - **Reddit:** F5Bot alerts on terms such as "dementia caregiver", "sundowning", "voice clone mom", "失智", plus subreddit-specific manual browsing.
  - **Threads:** Threads keyword-search API driven by a small script or a Claude Code skill (weekly digest).
  - **YouTube:** YouTube Data API search or manual search.
  - **Xiaohongshu:** the in-app search dropdown plus a 千瓜/灰豚 free quota.
  - Then an LLM summarises the collected text into "pain points / questions / language caregivers use".
- Facebook caregiver groups should be listened to as a member reading manually. Scraping groups breaches Meta terms. This is general knowledge, not sourced in this pass.

### Gaps
- No verified current free-tier details for Syften, Brand24, or 新红.
- No sourced free tool for Facebook Group listening.
- The YouTube Data API quota was not re-checked in this pass.

---

## 4. Comment and inbox management: safe to automate vs not; backlash against AI replies

### Takeaway
Evidence strongly suggests that AI-authored public replies in support communities harm trust. The clearest example is Meta AI answering in Facebook support groups and claiming lived experience. Meta's own tests of AI replies and comment suggestions on Instagram and Threads drew loud backlash. Comment-to-DM automation through official-API tools such as ManyChat is lower-risk, but accounts are still flagged for volume or repetitive behaviour. Safe to automate: triage, tagging, alerts, and drafting suggested replies for human sending. Not safe: auto-posting replies, especially in caregiver groups or on Reddit.

### Cited Findings
- Meta AI replied in Facebook groups when tagged, or when a question went unanswered for an hour. In 2024 it posted in a parenting group claiming to have a child with "unique needs". The AI Incident Database logged that support-group chatbots give misleading information and pretend to share lived experiences. A researcher noted that Meta puts the burden on group moderators. **(2024, older)** — [AI Incident Database #700](https://incidentdatabase.ai/cite/700/); [The Conversation](https://theconversation.com/ai-chatbots-are-intruding-into-online-communities-where-people-are-trying-to-connect-with-other-humans-229473); [Computing](https://www.computing.co.uk/news/4199289/facebook-chatbot-claims-child-unique-abilities)
- Meta tested AI-drafted comment suggestions on Instagram in 2025. Critics said it would fill feeds with fake conversation and mislead advertisers. — [dig.watch](https://dig.watch/updates/instagram-users-react-to-metas-new-ai-experiment); [The Hans India](https://thehansindia.com/tech/metas-ai-experiment-on-instagram-faces-backlash-users-accuse-it-of-ruining-social-media-957027)
- Meta AI replies on Threads (2026 test) brought backlash when users found they could not block the @meta.ai account. "Users cannot block Meta AI" reportedly trended with 1M+ posts. These are lower-tier outlets. — [SQ Magazine](https://sqmagazine.co.uk/meta-tests-ai-replies-threads-user-backlash.md); [LAVX](https://news.lavx.hu/article/meta-s-threads-ai-sparks-backlash-as-users-discover-they-can-t-block-the-account)
- A 2026 arXiv preprint on opioid-recovery subreddits found that AI-generated support conforms to norms but may over- or under-validate seekers in distress. It recommends that moderators set AI norms. — [arXiv 2603.19093](https://arxiv.org/pdf/2603.19093)
- A CSCW study (Nov 2025) of Reddit moderators found that AI-generated-content restrictions are hard to enforce and rely on time-intensive, inaccurate detection heuristics. — [arXiv 2311.12702](https://arxiv.org/pdf/2311.12702v7)
- Automated moderation can also hurt caregivers: a parent caregiver's account was removed after an automated system misread a caregiving conversation (Oct 2025 opinion piece). — [KevinMD](https://kevinmd.com/2025/10/ai-moderation-of-online-health-communities.html)
- Instagram automation risk:
  - Official-API tools (ManyChat is a Meta Business Partner) do not scrape or need passwords. Unofficial bots are flagged aggressively.
  - Bans are still triggered by behaviour, such as too many automated messages too fast or repetitive or promotional comment replies.
  - ManyChat staff cite a throttle of 750 private-reply API calls/hour **[vendor]**.
  - A ManyChat community thread documents a business account disabled after automation flags.
  - Sources: [setsmart](https://setsmart.io/blog/is-manychat-safe); [dealism.ai](https://dealism.ai/blog/is-manychat-safe-for-instagram-a-clear-objective-guide); [ManyChat community](https://community.manychat.com/general-q-a-43/instagram-business-account-disabled-due-to-automation-10161)
- Xiaohongshu explicitly penalises AI-hosted interaction (互动): warnings or reduced reach for occasional use, bans for accounts fully run by AI. — [GMW](https://m.gmw.cn/2026-03/10/content_1304371172.htm); [The Paper](https://www.thepaper.cn/newsDetail_forward_32747698)
- Reddit's sitewide policy does not ban AI text per se. It bans spam, deception, and coordinated inauthentic behaviour, and community rules are where restrictions apply. One guide cites a CHI 2025 finding (unverified here) that subreddits with explicit AI rules more than doubled in a year. The usual self-promotion norm is about 9:1 participation to promotion. Removals happen through automod, mods, and shadowbans (anecdotal). — [DEV self-promo framework](https://dev.to/sh20raj/reddit-self-promotion-framework-how-to-post-smart-and-stay-unbanned-1kfg); [Indie Hackers banned-posts analysis](https://www.indiehackers.com/post/analyzed-500-reddit-posts-that-got-banned-73-failed-for-the-same-reason-and-it-s-not-what-you-think-Y5JloVysPICuN2rOliIT); [Indie Hackers](https://www.indiehackers.com/post/how-do-you-promote-yourself-on-reddit-without-getting-removed-1f06e1f595)

### Inferences
- **Safe to automate:**
  - Pull new comments and DMs into one digest.
  - Classify them (question / praise / bug report / distress / spam / medical question).
  - Flag urgent or distress messages.
  - Suggest a draft reply drawn from a vetted FAQ (privacy, "not a medical device", how to install, voice-cloning consent).
- **Keep human:**
  - Sending every public reply and DM.
  - Every interaction in Facebook caregiver groups and on Reddit.
  - Anything touching medical advice, grief, or crisis.
  - Any reply on Xiaohongshu, where AI interaction is itself a penalty trigger.
- A comment-keyword → DM-link funnel (ManyChat-style) is technically low-risk on IG. It would feel transactional to grieving caregivers, though, and is probably unnecessary at this scale.

### Gaps
- No quantitative study of engagement or trust loss after a creator's own (as opposed to Meta's) AI auto-replies were discovered.
- Meta's current official policy pages on automated comments were not fetched.

---

## 5. Lightweight free cross-platform analytics

### Takeaway
No single free tool covers all six platforms. Practical free options: native dashboards (Meta Business Suite for FB/IG, Threads Insights and the Threads API, YouTube Studio, the Xiaohongshu creator center, Reddit post stats) plus a free scheduler tier (Metricool: 1 brand, 30-day history; Buffer: 3 channels). Alternatively, self-hosted Postiz analytics, or a small script pulling the Threads/YouTube APIs into a spreadsheet.

### Cited Findings
- Metricool free plan:
  - 1 brand, one profile per network.
  - Excludes LinkedIn and X.
  - 30 days of analytics history.
  - 5 competitors.
  - Monthly post cap disputed: 20 (third-party) vs 50 (Metricool's own comparison page).
  - Threads support on the free plan not confirmed.
  - Sources: [Metricool DE pricing](https://metricool.com/de/metricool-pricing-preise-und-features/); [inmagic review](https://inmagic.ai/metricool-review/); [Metricool vs Agorapulse](https://metricool.com/metricool-vs-agorapulse/); [Social Champ](https://www.socialchamp.com/blog/metricool-pricing/)
- Other free tiers per vendor comparisons: Buffer free for 3 channels, Agorapulse free for 3 accounts and 10 posts/month **[vendor-published]**. — [Metricool vs Agorapulse](https://metricool.com/metricool-vs-agorapulse/); [Social Champ](https://www.socialchamp.com/blog/metricool-pricing/)
- The Threads API insights endpoint provides views, likes, replies, reposts, quotes, and shares per post and per user. `since`/`until` filters do not work before Apr 13, 2024. — [Threads API reference](https://developers.facebook.com/documentation/threads/reference); [socialcrawl guide](https://www.socialcrawl.dev/blog/threads-api)
- Postiz (self-hosted) includes analytics tools, exposed through its MCP wrapper. — [Postiz MCP](https://solomonneas.dev/projects/postiz-mcp)
- The Xiaohongshu creator center is free and covers reads, followers, and engagement. — [tixiaolu](https://www.tixiaolu.com/v2/posts/v2-14ad9daa.html)

### Inferences
- For a solo developer: a weekly 15-minute ritual. Export or copy native metrics into a single sheet or CSV in the repo (date, platform, post id, topic tag, views, saves/shares, comments, link clicks, GitHub stars delta). Then let Claude Code summarise "which topics/formats outperform".
- GitHub stars, clones, and README referrers from GitHub traffic insights are the conversion metric that matters for the developer audience.

### Gaps
- Free-tier specifics for Buffer and Metricool in late 2026 were not verified on primary pages.
- No sourced free tool covers Reddit and Xiaohongshu analytics together with the Meta platforms.

---

## 6. Considerations for sensitive health / caregiving audiences

### Takeaway
Disclosure and authenticity matter more here than anywhere. Undisclosed AI is consumers' top complaint, and YouTube requires disclosure of realistic synthetic voices, with more prominent labels on health topics. China mandates labels on AI content (Sept 2025), and Xiaohongshu throttles unlabelled AI content. Support communities have documented harm from AI "pretending lived experience". For a voice-cloning dementia project, AI-generated visuals or voices in posts should be labelled. Human-authored, first-person storytelling and human replies are the trust anchor.

### Cited Findings
- YouTube "altered or synthetic content" disclosure:
  - Covers making a real person appear to say something they didn't, including **synthetically generating a person's voice to narrate**.
  - Labels are more prominent on the player for sensitive topics, including **public health**.
  - YouTube may add labels itself.
  - Repeated non-disclosure risks removal or YPP suspension.
  - Stylised or animated AI content generally gets only a description label.
  - **(Policy introduced 2024.)**
  - Sources: [9to5Google](https://9to5google.com/2024/03/18/youtube-altered-content-disclosure/); [TechSpot](https://www.techspot.com/news/102315-youtube-introduces-labeling-requirements-synthetic-altered-content.html); [Android Central](https://www.androidcentral.com/apps-software/youtube-ai-synthetic-content-disclosure); [AIR Media-Tech](https://air.io/en/youtube-glossary/what-is-youtubes-ai-content-disclosure-policy)
- China's AIGC labelling rules (effective Sept 1, 2025) cover text, images, audio, and video. Xiaohongshu throttles unlabelled AI content (Feb 2026) and has an appeal channel (Apr 2026). — [Yangtse Evening Post](https://www.yzwb.net/news/txs/202509/t20250901_257831.html); [The Paper](https://www.thepaper.cn/newsDetail_forward_32747698)
- Consumers: 52% are concerned about undisclosed AI content (Sprout Q3 2025). 55% trust brands that commit to human-created content more. — [Digital Information World](https://www.digitalinformationworld.com/2025/09/ai-disclosure-and-trust-define-social.html)
- Support communities: AI replies that claim lived experience caused documented harm. AI support can mis-validate people in distress. Moderators struggle to detect AI content and are tightening rules. — [AI Incident Database](https://incidentdatabase.ai/cite/700/); [arXiv 2603.19093](https://arxiv.org/pdf/2603.19093); [arXiv 2311.12702](https://arxiv.org/pdf/2311.12702v7)
- Automated platform moderation can also misread caregiver content and remove accounts. Wording about distress, abuse, or confusion in elders could trigger similar false positives. — [KevinMD](https://kevinmd.com/2025/10/ai-moderation-of-online-health-communities.html)

### Inferences
- Content rules for this project:
  - (a) Never imply medical efficacy. Keep "not a medical device" in bios and pinned posts.
  - (b) Label AI comics, images, and voice demos. Use YouTube's synthetic-content toggle for any cloned-voice demo, and add the XHS AI label.
  - (c) Show voice-cloning consent and privacy (local-first) prominently. This is the likely main objection from caregivers.
  - (d) Use real caregiver stories only with permission. Never fabricate testimonials with AI.
  - (e) Don't let AI post or reply in caregiver groups. Group admins are the gatekeepers, so ask permission before sharing.
- AI-generated comics are acceptable as clearly labelled illustration. Realistic AI "elder + family" video could be read as deceptive on health topics and draw the more prominent YouTube label.

### Gaps
- Meta's current "AI info" labelling policy for FB/IG/Threads was not retrieved in this pass.
- No caregiver-specific survey on attitudes to AI-generated outreach content.
- No Taiwan- or Hong Kong-specific platform rules on AI labelling were researched.

---

## Stage-by-stage automation map (synthesis of the findings above)

| Stage | Automate (AI/agent) | Keep human | Key reason / evidence |
|---|---|---|---|
| Listening / trend research | Keyword alerts (F5Bot, Threads keyword API, XHS hot-word tools), LLM digest of collected threads | Reading FB caregiver groups as a member; judging what is emotionally appropriate | Reddit API commercial limits (GummySearch closure); no FB group API |
| Topic selection | LLM clusters pain points into a ranked shortlist | Final pick and angle | Originality and "unique take" protect reach (FB/YouTube 2025 rules) |
| Drafting | First drafts with a brand-voice file; two-pass per-platform adaptation; zh-TW/zh-CN/EN variants | Edit to own voice; first-person stories; fact and claim check (no medical claims) | Slop and undisclosed AI are top consumer complaints (Sprout 2025–26) |
| Visuals | AI comics and images, labelled | Approve every image; no realistic fake testimonials; cloned-voice demos disclosed | YouTube synthetic disclosure; China/XHS labelling |
| Scheduling / publishing | Scheduler (Postiz self-hosted, Metricool/Buffer free, Meta Business Suite native) after approval | Approval gate; Reddit and XHS posted manually | XHS bans AI-hosted accounts; Reddit community rules; MCP "wrong draft to wrong account" warning |
| Community replies | Triage, classification, distress flags, FAQ draft suggestions | Sending all replies; all group and Reddit interaction | Meta AI support-group incident; Threads/IG AI-reply backlash; XHS AI interaction penalty |
| Analytics | Weekly pull or export into a CSV; LLM summary of which topics and formats perform | Deciding strategy changes | No free all-in-one tool; native dashboards are free |
