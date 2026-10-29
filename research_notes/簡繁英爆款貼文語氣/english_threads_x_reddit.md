# Viral English posting voice for indie devs and personal stories (Threads, X, Reddit, HN, LinkedIn), 2025–2026

Research note on access: this session could not fetch en.wikipedia.org, news.ycombinator.com, hn.svelte.dev, dev.to, pangram.com or trevorlasn.com (DNS blocked by network policy). Claims about those pages come from search-engine summaries or mirrors and are marked as such. The blader/humanizer README on github.com was fetched directly. Items marked [background] come from the researcher's prior knowledge and need checking against the live source before anyone quotes them.

## 1. Hooks and openings on Threads and X; build-in-public examples

### Takeaway
Well-known indie hackers write plain, first-person, lowercase-friendly updates. They lead with one hard number or one concrete thing they shipped, then add a messy, honest aside. They do not use "hook formulas". Specificity (a dollar figure, day count or object name) beats drama. On Threads, comments and replies drive distribution, and the platform is demoting engagement bait.

### Cited Findings
- levelsio milestone format: "✅ Reached $15,000/mo MRR with [link]!! I'm not doing anything for it to grow rn but @MysteryGuitarM told me all over TikTok 🤯 Never really had recurring revenue before so it's very interesting to experience". The post has a number first, an abbreviation ("rn"), an admission that he did nothing, and a small reflection. — [X, levelsio, Jan 2023](https://twitter.com/levelsio/status/1610127445092634624)
- levelsio, fly.pieter.com (Mar 2025): "💸 Revenue update for [link] after 13 days: Hit $67,000 MRR (+$10K from yday) (hopefully we can pass $70K tomorrow, a man can dream!)". It gives the number, the day count and a self-deprecating bracket. — [X, levelsio](https://x.com/levelsio/status/1897784027186446820)
- A longer levelsio update mixes stats ("320,000 people have now flown in the game") with honest doubt ("Whether the MRR is truly sustainable for a year we can only guess"), personal life ("I was ski'ing today so was AFK mostly", "on travel with gf") and an admission about AI code ("AI doesn't really care about [XSS]… it can be full of security holes"). It has run-on sentences and few commas, and nobody would mistake it for polished prose. — [X, levelsio, Mar 2025](https://x.com/levelsio/status/1899596115210891751?lang=en)
- levelsio on credibility (Oct 2025): "There's so many fake MRR screenshots on here… It took me years to get to $10K/mo revenue!" The grammar is casual ("There's so many"), which suggests native-feeling looseness reads as human. — [X, levelsio](https://x.com/levelsio/status/1983110741033996484)
- levelsio curates a "Build in Public" list of makers who post "no politics, no LinkedIn bs threads, no content marketing, just public updates". This is an explicit statement that the genre's top voice dislikes thread-bro and content-marketing style. — [X, levelsio](https://x.com/levelsio/status/1405118725796159496?lang=en)
- Marc Lou's TrustMRR launch: "Bye Bye fake MRR screenshots 👋 I built [link], the database of verified startup revenues. 1. Upload a read-only Stripe API key 2. Get a free page showing your verified revenue 3. And a nice dofollow backlink as a bonus. There's no way to game the system." The post opens on the problem everyone recognises, then "I built X, the [one-line definition]", then numbered steps. — [X, marclou, Oct 2025](https://x.com/marclou/status/1983985733095325873)
- Secondary sources say the TrustMRR launch tweet got over 2M impressions and $20,378 in ad slots within 3 days. These are unverified secondary figures and they conflict across sources. — [DEV via search](https://dev.to/promptway/he-built-an-app-in-24-hours-and-made-20378-the-next-day-heres-the-part-nobody-screenshots-5gep); [Scale Nuggets](https://scalenuggets.beehiiv.com/p/made-528k-4-months-shipping-saas-projects-like-madman)
- Nicolas Cole (Ship 30 for 30) on headlines: a headline gets stronger when you add detail to one of four parts, the WHAT, the WHO, the FEELING or the PROMISE. — [Nicolas Cole thread via Threadreader](https://threadreaderapp.com/thread/1441450057119592456.html)
- Cole and Dickie Bush (Write With AI) on Carlton-style story hooks: research for "eccentric details" that make the reader say "Wait, back up." In other words, a strange concrete detail in line one. — [Write With AI / Carlton story hooks summary](https://hq-raydata-co.pages.dev/vault/06-reference/2026-01-21-write-with-ai-story-hooks-carlton/)
- Cole's hook thread borrows Ogilvy's concrete "At 60 mph…" Rolls-Royce line and says to address readers directly. — [Threadreader](https://threadreaderapp.com/thread/1442626559660072965.html)
- Threads ranking (blog consensus, not Meta primary): comments weigh more than likes, and engagement velocity matters. Mosseri has acknowledged the engagement-bait problem, so "comment YES" hooks are risky. Buffer data relayed second-hand says image posts get about 60% more engagement than text-only (unverified). — [Outfy](https://www.outfy.com/blog/how-threads-algorithm-works/); [PostEverywhere](https://posteverywhere.ai/blog/how-the-threads-algorithm-works); [ContentStudio](https://contentstudio.io/blog/how-to-go-viral-on-threads)
- A 2026 profile says levelsio's build in public works as "continuous user research, lightweight marketing, trust creation through transparency". — [IndieAI blog](https://indieai.pages.dev/blog/pieter-levels-real-indie-developer-playbook-2026)
- A third-party imitation tool (vendor, not affiliated) calls levelsio's style "extremely casual, almost stream-of-consciousness… liberal emoji use". — [OpenTweet (vendor)](https://opentweet.io/generate-like/levelsio)
- A linguist quoted in Mint says lowercase-by-default on Twitter signals familiarity or an anti-establishment stance. — [Mint via PressReader](https://www.pressreader.com/india/mint-mumbai/20240401/281990382534271)

### Inferences
- Line one of a top indie-hacker post usually contains a number, a named product or a named object. It is almost never an abstract claim like "A silly childhood habit did what medicine could not do." Abstract or aphoristic openers read as copywriting, and since 2024 they also read as AI.
- Imperfection (abbreviations, run-ons, brackets, "lol", self-doubt) is part of the voice. For a C1 writer, light non-native looseness fits this register better than polished, Claude-perfect prose.
- Story posts on Threads probably benefit from one photo of the real object or person (where privacy allows), given the reported text-only penalty.
- The 382-view result fits the pattern of an abstract hook with no concrete noun, plus a mistranslated object ("juice box") that confuses rather than evokes.

### Gaps
- Could not retrieve verbatim recent posts from Tony Dinh, Danny Postma or Arvid Kahl. Search returned nothing for their handles.
- No independent dataset ranks text hook styles on Threads. All Threads advice is anecdotal or from vendor blogs.

## 2. Reddit "I built X" posts, caregiving story posts, and Show HN conventions

### Takeaway
Reddit and HN punish marketing voice hardest. Good posts say plainly what the thing is, why you built it (a personal reason), what it does not do yet, and ask for feedback. Show HN titles are neutral and descriptive, the backstory goes in the text or first comment, and the thing must be usable now.

### Cited Findings
- r/SideProject: a bare link without context is treated as spam. Posts should say what you made, why, and the tech, and be candid about whether it is a prototype or finished. — [RedditMaster rules guide](https://www.redditmaster.com/subreddit-rules/sideproject)
- Title convention depends on the subreddit. "I built…" is traditional on r/SideProject, and other subs expect different phrasing. It also helps to reply to your own post with context. — [Medium, Tereza Tizkova](https://tereza-tizkova.medium.com/best-subreddits-for-sharing-your-project-517c433442f9)
- r/selfhosted (Mar 2026 rules update): the "Vibe Code Friday" experiment became "New Project Friday". Projects younger than 3 months may only be posted on Fridays, and mods stopped policing AI involvement and removed AI flairs. — [r/selfhosted rules thread via redlib mirror](https://redlib.groet-infra.nl/r/selfhosted/comments/1rmt39o/rules_update_new_project_friday_here_to_stay/o91wk8x)
- On the Lemmy selfhosted community, rules require [AIP] tags plus disclosure of which parts used AI. A commenter notes vibe-coded spam is "deliberately engineered to look 'high effort'". Because readers are primed for this, an honest AI disclosure builds trust. — [Lemmy rules post](https://deddit.petersanchez.com/g/selfhosted@lemmy.world/p/8zmvWp42vmcdKvw18x-AI--Promotional-Post-Expanded-Rules); [discussion](https://discuss.mschae23.de/comment/17808)
- One developer who posted across Reddit, LinkedIn and X found "Reddit sent nearly everything. LinkedIn and X barely registered." — [DEV, Damon Thomas (via search snippet)](https://dev.to/damon-thomas/how-i-missed-out-on-thousands-of-views-launching-my-side-project-3d8d)
- Show HN (secondary summary of the official guidelines): the title format is "Show HN: [what it is] – [differentiator]", kept neutral. Guidelines reportedly prohibit uppercase, exclamation points, praise, site names, gratuitous numbers and editorialised titles. — [Causo Show HN playbook 2026](https://hub.causo.ai/guides/show-hn-launch-playbook-technical-founders-2026); [MentionMe HN guide](https://mentionme.appspot.com/blog/hacker-news-marketing/)
- HN moderator dang: the project must actually exist and people must be able to try it. Landing pages, waitlists, blog posts and reading lists don't qualify. Text goes at the top of the submission, or failing that in a first comment with the backstory, what's different, and what it does. — [dang comment mirror](https://hn.svelte.dev/item/22336638) (summarised via search; page not fetched)
- HN tone: drop "any language that sounds like marketing or sales". Technical details and personal stories are well received. Stay in the thread answering questions, and never ask for upvotes. — [Stackmatix](https://www.stackmatix.com/blog/launching-on-hacker-news); [IndieHackers thread](https://www.indiehackers.com/post/any-tips-for-doing-a-show-hn-post-ff7e6f688b)
- [background] The official showhn.html says Show HN is "for something you've made that other people can play with" and asks makers to be available to answer questions. It discourages sign-up walls. Check against https://news.ycombinator.com/showhn.html.
- Grandparent-dementia projects are a recurring media story shape: a grandchild sees the grandparent stop recognising them, then builds a tool (photos, voice recordings, prompts). Examples are Alzimate (Dubai student, 400+ users), Recollect (Detroit teen) and MemoLens (DubHacks '24). This shows the "I built X for my grandad" frame is familiar, so the specific details have to carry the post. — [Khaleej Times](https://www.khaleejtimes.com/alzimate-app-alzheimers-dubai-student-develops-help-patients-caregivers); [Fox 2 Detroit](https://www.fox2detroit.com/news/metro-detroit-teen-creates-app-those-alzheimers-inspired-late-grandfather); [Georgia Tech](https://sci.cc.gatech.edu/external-news/cs-majors-win-hackathon-ai-powered-app-alzheimers-patients)

### Inferences
- Title templates that fit each venue:
  - r/selfhosted: "I made a self-hosted voice companion for my grandad (Alzheimer's). Runs on [hardware], [model], no cloud". Post on a Friday if the project is under 3 months old.
  - r/LocalLLaMA: lead with model, hardware and latency numbers ("Local voice companion on a [GPU]: [model] + [TTS], ~[x]s round trip").
  - Show HN: "Show HN: [Name] – a voice companion for people with dementia, runs locally".
- Caregiving subs (e.g., r/dementia, r/Alzheimers, r/AgingParents) are support spaces. A product link there will likely be read as self-promotion. Lead with the experience, put the tool second, ask whether it is OK to share, and follow each sub's rules. This is inferred; the rules were not verified.
- A "what doesn't work yet" paragraph is a trust signal on every technical venue.

### Gaps
- Could not read r/LocalLLaMA or caregiving-sub rules directly (Reddit not fetched). Found no data on which r/LocalLLaMA title shapes get the most upvotes.
- Could not fetch the official Show HN page or a quantitative Show HN title study.

## 3. LinkedIn personal-story structure and what is now cringe

### Takeaway
"Broetry" has been parodied since 2017. By 2025–26 the same format reads as AI slop: a dramatic story cut into one-sentence lines, a moral, and "Agree?" or "Let that sink in." LinkedIn added an "AI slop" flag. Formulaic posts can still win reach, but they cost credibility with technical readers.

### Cited Findings
- "Broetry" is credited to journalist Lorcan Roche Kelly (2017). The format is a dramatic story split into single-sentence lines and closed with a prompt for agreement. — [Live in the Future](https://liveinthefuture.org/stories/linkedin-thought-leadership-ai-authenticity-crisis)
- An Originality.AI study reported 54% of long-form LinkedIn posts since mid-2023 are likely AI-generated or heavily AI-edited. This is a vendor study relayed second-hand. — [Live in the Future](https://liveinthefuture.org/stories/linkedin-thought-leadership-ai-authenticity-crisis); [Trevor Lasn (not fetched)](https://www.trevorlasn.com/blog/linkedin-is-drowning-in-ai-generated-content-slop)
- Cringebot 3000: a deliberately over-the-top post generator. A journalist's test post outperformed their normal posts, and "96% of viewers were outside my network". The format still games reach. — [The Cool Down](https://www.thecooldown.com/green-tech/test-cringebot-3000-linkedin-ai-slop/); [Gizmodo AU](https://gizmodo.com.au/?p=1813428)
- LinkedIn added a way to flag posts as "AI slop" (per Business Insider, relayed). — [search summary of Live in the Future / BI](https://liveinthefuture.org/stories/linkedin-thought-leadership-ai-authenticity-crisis)
- Reported tells (anecdotal roundup): stock phrases like "Let that sink in" and one sentence per line as the default output of AI LinkedIn tools. — [LinkedIQ](https://linkediq.pages.dev/blog/ai-vs-human-linkedin-posts)

### Inferences
- For LinkedIn, use short paragraphs (2–4 sentences), not one-line verses. End with a plain fact or a specific question, not "Agree?", "Thoughts?" or "Let that sink in." No "I'm humbled" or "Here's what it taught me about leadership."
- Tie the story to a concrete work detail (the stack, what broke) so it reads as an engineer's post, not a coach's.

### Gaps
- No primary LinkedIn data on dwell time or format performance in 2025–26 was retrieved.

## 4. British English tone

### Takeaway
UK readers distrust hype and superlatives. Understatement, dry self-deprecation and evidence work better. For a London-based author writing to UK parents (11+ tool), use British spelling and turn the volume down.

### Cited Findings
- British audiences "prefer understatement" and are "wary of anything overly promotional". Loud US brand voice "can feel off-putting" in the UK, and Brits are "far more questioning of new brands, particularly those arriving with significant hype". — [Decision Marketing](https://www.decisionmarketing.co.uk/views/why-expanding-from-us-to-the-uk-is-not-all-plain-sailing)
- 2025 comparative study: British ads "rely on subtlety, irony, and understatement", while American ads are "more direct, emotionally driven". — [inlibrary.uz study](https://inlibrary.uz/index.php/tinnint/article/view/119499)
- UK readers respond to evidence and social proof. Their emails are longer and more reserved. — [Bird](https://bird.com/nl/blog/differences-us-uk-marketing-emails)
- Stats on profiletree.com (34% lower conversion etc.) have no cited origin, so treat them as unreliable. — [ProfileTree](https://profiletree.com/uk-vs-us-copywriting/)

### Inferences
- Swap "game-changer", "insanely", "super excited", "awesome" and "crushing it" for "quite useful", "it mostly works", "I'm pleased with", "not bad for a weekend". Use British spelling (colour, organise, mum, grandad, maths, Year 5, 11+ "exam" not "test prep"), and "rubbish" or "a bit" rather than "terrible".
- UK parents audience: be calm and factual, and name the actual paper format (GL or CEM style). Avoid fear-based urgency.

### Gaps
- No source lists specific "banned" words for UK audiences. The word list above is inference.

## 5. AI-writing tells and keeping a non-native voice authentic

### Takeaway
The current detector folklore (Wikipedia's guide, humanizer) targets structure more than single words. The structural tells are contrast reversals ("not X, it's Y"), triads, dramatic one-line closers, inflated significance, "-ing" riders, sales adjectives and decorative formatting. Single words like "delve" or "testament" also count. Machine translation and LLM polishing also push non-native writers toward Standard American English, which erases the voice that makes their posts credible.

### Cited Findings
- blader/humanizer pattern list (fetched):
  - "Not X but Y" ("It's not just X, it's Y")
  - one-line closers and dramatic fragments ("That is the real win.")
  - sayings that sound deep ("At its core…")
  - staged run-ups ("Let's dive in.")
  - arguing with no one
  - forced triads
  - repeated sentence openings
  - dashes as the universal connector
  - stacked qualifiers
  - over-hyphenation
  - missing subjects
  - overused AI words ("delve… testament… landscape… showcasing")
  - inflated significance ("marking a pivotal moment")
  - vague association
  - shallow -ing riders ("symbolizing… reflecting… showcasing")
  - sales language ("nestled within the breathtaking region")
  - borrowed authority ("Experts believe…")
  - avoiding is, are and has ("serves as… features… boasts")
  - bold as decoration
  - decorative headings ("🚀 Launch Phase:")
  - curly quotes
  - chatbot residue ("Great question!… I hope this helps!")
  - knowledge-limit disclaimers
  - a heading repeated in the first sentence
  - writing about the document
  - re-explaining what the reader knows

  — [github.com/blader/humanizer](https://github.com/blader/humanizer)
- Wikipedia "Signs of AI writing" (via mirrors and summaries):
  - Em dashes are a sign only when they are more frequent than typical human text and stand where commas or parentheses would go.
  - Rule-of-three triplets count as a pattern only when repeated.
  - Vocabulary includes "delve", "intricate", "tapestry" and "underscore".
  - The page says the list is not a ban, and some formatting signs may not apply outside Wikipedia.

  — [FlowingData](https://flowingdata.com/2025/10/20/signs-of-ai-writing-on-wikipedia/); [Beutler Ink](https://www.beutlerink.com/blog/how-to-spot-ai-writing); [mirror](https://cavac.at/cavacopedia/Wikipedia%3ASigns_of_AI_writing)
- [background] The Wikipedia page also lists promotional "puffery" ("rich cultural heritage", "stands as a testament", "plays a vital role"), "Not only… but also", title-case headings, emoji-led bullets, excessive bold, and closing summaries ("In summary", "Overall"). Verify on the live page.
- Pangram (an AI-detector vendor) publishes "9 Signs of AI Writing, Backed by Data". Not fetched, so its stats are unverified. — [Pangram (vendor)](https://www.pangram.com/signs-of-ai-writing)
- UC Berkeley researchers found ChatGPT prefers Standard American English and produces "exaggerated caricature-like outputs" for other dialects. A Cornell study suggests AI nudges Indian English writers toward American patterns. — [Fortune, Jun 2025](https://fortune.com/2025/06/30/linguists-chatgpt-influencing-how-humans-write-speak/)
- A non-native poster on HN reports readers calling their polished comments AI-written. — [HN Ask thread mirror](https://ask.live.com.de/46398608)
- Essays argue that AI-polishing strips a non-native writer's culture and "spiciness" and the "ghost" of native syntax. These are opinion pieces. — [Bear Wiseman Substack](https://bearwiseman.substack.com/p/when-you-edit-your-truth-with-ai); [imperfect.bearblog](https://imperfect.bearblog.dev/evolve-your-voice/)
- Advice (Ritesh Chugh, via TechRadar): swap buzzwords for simpler words, read more human writing, value the quirks in your own style. — [TechRadar](https://www.techradar.com/ai-platforms-assistants/chatgpt/chatgpt-is-changing-the-way-we-communicate-heres-how-you-can-avoid-speaking-like-ai-in-public)

### Inferences (translated-English tells relevant to a Taiwanese author)
- Object mistranslation is the "juice box" problem. Don't replace a cultural object with the nearest US object. Name it, then gloss it once: "a carton of Taiwanese milk tea (the 300ml kind with a straw, every Taiwanese kid had one)". The foreign object is the hook, so keep it.
- Chinese four-character idioms and moral endings translate into proverb-like English ("did what medicine could not do"). This collides with the AI "sayings that sound deep" tell, so cut them.
- Common Mandarin-to-English transfer that is fine to keep: slightly direct phrasing, "my grandpa/grandad" naming, small article slips. Fix only errors that change meaning.
- Kinship terms: use "grandad" (UK) or "grandpa", and add the Taiwanese term once if it adds texture ("阿公, my grandad"). Use family-specific detail rather than "my beloved grandfather".

### Gaps
- No study found that measures how readers rate non-native writers who keep minor errors versus fully polished text.

---

## Draft: English style rules (for an AI drafting posts in this author's voice)

### Do
1. Open with a concrete noun, number or scene in line one: an object, a day count, a model name, a price, an age. ("My grandad is 87. He forgets my name about twice a week.")
2. Write in first person, past tense for stories and present tense for updates. Use short paragraphs of 1–3 sentences, not one sentence per line.
3. Name the real thing: Taiwanese milk tea, not juice box; "Whisper + a £30 mic", not "cutting-edge AI".
4. Give real numbers with units, including small or unflattering ones ("9 users, 2 are my mum").
5. Include one thing that doesn't work, and one thing you're unsure about.
6. Keep the author's slight non-native edge. Fix only errors that change meaning or are confusing.
7. On X and Threads, casual is fine: contractions, "tbh", brackets, lowercase where natural. Use at most one emoji, or none.
8. For Reddit and HN, write a plain descriptive title, then context, what it is, why, how it works (stack), limits, link, and a specific question.
9. Use British spelling and understatement for UK audiences: "quite", "a bit", "seems to work", "pleased with how it turned out".
10. Use one image of the real thing on Threads and X where privacy allows.

### Don't
1. No em dashes (use full stops, commas or brackets), no semicolons in social posts, and few colons.
2. No "It's not X, it's Y" or "This isn't about X. It's about Y."
3. No triads for rhythm ("faster, smarter, kinder").
4. No aphorism openers or closers: "did what medicine could not do", "Sometimes the smallest things…", "That's the real lesson."
5. Banned words: delve, testament, tapestry, landscape, game-changer, revolutionary, seamless, leverage, unlock, empower, journey, pivotal, crucial, vibrant, robust, "in today's fast-paced world", "let's dive in", "here's the thing", "let that sink in", "Agree?", "Thoughts?".
6. No inflated significance ("a pivotal moment for our family") and no -ing riders ("…, reminding us of what truly matters").
7. No emoji bullets, no Title Case Headings, no bold decoration, no hashtag stacks (one tag max on Threads), and no "🧵 1/".
8. No marketing claims on Reddit or HN ("the best", "the ultimate"), no asking for upvotes, no waitlist-only Show HN.
9. No LinkedIn broetry (one-line-per-paragraph drama ending in a moral).
10. Don't substitute a culturally specific object with an American equivalent.

### Hook formulas (fill with real facts only)
- [Person] + [concrete fact] + [unexpected detail]: "My grandad has Alzheimer's and forgets most things now. He has never once forgotten the milk tea."
- [Number] + [time] + [what]: "Day 14 of building a voice companion for my grandad. He talked to it for 11 minutes today."
- "I built [thing] for [specific person/problem]. Here's what [it does / went wrong]." (Reddit and Threads)
- Problem everyone recognises, then "so I built X, the [plain one-line definition]" (Marc Lou pattern).
- Revenue or usage update: "[Product] update: [number] [unit] after [n] days" plus an honest aside (levelsio pattern).
- Show HN: "Show HN: [Name] – [what it is in plain words], [one key constraint, e.g. runs locally]"

### Closing formulas
- A plain next step: "Next I want to try [specific thing]."
- A specific question the reader can answer: "Has anyone got a TTS voice that elderly listeners find easier to follow?"
- The link plus a limit: "It's free and open source: [link]. It only works in Mandarin and English for now."
- A quiet human beat with no moral: "He asked it to play Teresa Teng again. So it did."

### Before/after rewrites (illustrations, not real posts. Bracketed items must be replaced with the author's true facts.)

**1. The story opener**
- Before: "A silly childhood habit did what medicine could not do."
- After (Threads/X): "My grandad has Alzheimer's. Most days he isn't sure who I am.
  When I was little he bought me a carton of milk tea from the 7-Eleven every day after school (the small Taiwanese kind with a straw).
  Last month I put one in his hand over a video call and he said, 'You still drink this?'
  So I'm building him a voice companion that talks about [the things he still remembers]."
- Why: a concrete object, a real line of dialogue, no aphorism, and no claim about medicine (which also avoids a misleading health claim).

**2. Build-in-public update**
- Before: "🚀 Excited to share that I've been on an incredible journey building an AI-powered companion that's not just a tool, it's a lifeline — empowering families, bridging generations, and redefining care."
- After: "Week 3 of the voice companion for my grandad. It runs on a [Raspberry Pi 5 / old laptop], [model] for speech. Round trip is about [2.5]s, which is too slow for him. He talks over it. Trying a smaller model this weekend."

**3. Reddit / Show HN launch**
- Before (title): "Introducing MemoryMate: The Ultimate AI Companion Revolutionizing Dementia Care!"
- After (r/selfhosted title): "I made a local voice companion for my grandad (Alzheimer's). No cloud, runs on [hardware]"
- After (Show HN title): "Show HN: [Name] – a local voice companion for people with dementia"
- First comment: "My grandad has Alzheimer's and lives in Taiwan, I'm in London. I wanted something he could talk to in Mandarin between our calls. It's [stack]. It doesn't handle [X] well yet, and I've only tested it with one person, so I'd really like feedback from anyone who cares for someone with dementia."

**4. UK parents (11+) tone**
- Before: "Supercharge your child's 11+ success with our game-changing AI platform!"
- After: "I made a free 11+ practice site for my [niece / friend's son]. It's [verbal reasoning] questions in the [GL] style, timed, no sign-up. It's a side project, so some questions will be wrong. Tell me and I'll fix them."
