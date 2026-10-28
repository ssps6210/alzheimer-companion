# AI visuals, comics and short video for a solo creator who needs a recurring character (2026)

> Method note (read first): researched 2026-10-28. WebFetch was blocked in this session for every primary source tried (ai.google.dev, platform.openai.com, docs.midjourney.com, docs.comfy.org, invideo.io, renderreport.com). Those hosts must be allowed in the session's network settings before the official pages can be fetched. As a result, **every finding below comes from web-search result snippets**, most of them third-party blogs or vendor content. Prices and limits change monthly, so check them on the official pricing pages before using them in a final recommendation. Where sources conflict, this is noted.

## Q1. Character-consistency methods in 2026: which are most reliable and cheapest?

### Takeaway
For a solo creator, the most practical option is reference-image editing in a hosted multimodal model, specifically Google's Nano Banana family (Gemini image models), with a single clean "character reference sheet" reused for every panel. GPT Image 2 is a close second and is better on text. Midjourney gives the best look but holds a character less well. Local LoRA training for Flux on an 8GB RTX 4060 is marginal (slow, and many guides say there isn't enough VRAM). A local reference-editing model (Qwen-Image-Edit-2511 as a GGUF quant) is the more realistic free local route, but no source confirmed it runs on 8GB.

### Cited Findings
**Hosted reference-image models**
- 2026 comparison blogs most often name Nano Banana (Gemini image) as the top pick for character consistency. Google says it can keep the resemblance of up to 5 characters in one workflow. — [rupertchesman.com](https://rupertchesman.com/blog-midjourney-vs-nano-banana-vs-chatgpt-images-2026.html); [renderreport.com](https://renderreport.com/blog/best-ai-image-generators-character-consistency)
- Sources conflict on reference limits: one says Nano Banana Pro takes 5 character images and the base model takes 4. — [queststudio.io](https://queststudio.io/blog/best-ai-models-for-character-consistency); [pxz.ai](https://pxz.ai/blog/nano-banana-vs-top-ai-image-generators-complete-2026)
- One review says Nano Banana holds a character well within a single editing session but drifts faster across separate generations. The widely quoted "95%+ consistency" figure refers to the older Gemini 2.5 Flash Image, so it is stale. — [pixmind.io](https://www.pixmind.io/posts/midjourney-v7-vs-gpt-image-2-vs-nano-banana-2); [pxz.ai](https://pxz.ai/blog/nano-banana-vs-top-ai-image-generators-complete-2026)
- GPT Image: OpenAI's own docs reportedly say GPT Image models can struggle to keep recurring characters consistent. A "Thinking" mode reportedly produces up to 8 frames with character continuity from one prompt. — [floatboat.ai](https://floatboat.ai/blog/gpt-image-2-vs-midjourney-nano-banana-2); [pixmax.ai](https://www.pixmax.ai/blog/midjourney-ai-image-model-review.html)
- GPT Image 2 editing accepts up to 16 reference images. — [aireiter.com](https://aireiter.com/blog/gpt-image-2-api-pricing); [blog.segmind.com](https://blog.segmind.com/ai-image-gen-pricing-compared-nano-banana-2-vs-seedream-5-0-vs-gpt-image-2-2026/)
- Midjourney is rated the most artistic (V8.2), but one review says it is weaker at consistency than Nano Banana or ChatGPT. The V8.2 Edit model takes up to 4 references. — [pixmax.ai](https://www.pixmax.ai/blog/midjourney-ai-image-model-review.html); [christytuckerlearning.com](https://christytuckerlearning.com/comparing-ai-image-generation-tools/)
- Midjourney's official Character Reference doc tells V7 users to switch to Omni Reference (`--oref`, weight `--ow`) and links a separate V8.1 article. — [docs.midjourney.com](https://docs.midjourney.com/docs/character-reference); [aiarty.com](https://www.aiarty.com/midjourney-guide/midjourney-omni-reference.htm)
- Community reaction to Omni Reference is mixed ("still rough"). — [producthunt.com](https://www.producthunt.com/p/midjourney/midjourney-omni-reference)
- All three tools drift, especially across repeated edits. — [rupertchesman.com](https://rupertchesman.com/blog-midjourney-vs-nano-banana-vs-chatgpt-images-2026.html)

**Cost of hosted options (API)**
- Nano Banana Pro (Gemini 3 Pro Image) costs about $0.134 per image at 1K/2K and $0.24 at 4K ($120 per 1M image-output tokens). The free tier is not available for the Pro image models. — [benchlm.ai](https://benchlm.ai/media-pricing/nano-banana); [docs.ai.it.ufl.edu](https://docs.ai.it.ufl.edu/docs/navigator_models/models/google-gemini-3.0-pro-image); [myarchitectai.com](https://www.myarchitectai.com/blog/nano-banana-api-pricing)
- Nano Banana 2 (Gemini 3.1 Flash Image) costs $0.045 at 0.5K, $0.067 at 1K, $0.101 at 2K and $0.151 at 4K. "Nano Banana 2.1" (listed as released 2026-10-06) costs $30 per 1M image-output tokens, or $15 on Batch. — [myarchitectai.com](https://www.myarchitectai.com/blog/nano-banana-api-pricing); [evolink.ai](https://evolink.ai/es/collections/nano-banana)
- Reference images uploaded to Pro are reportedly charged about $0.067 each. This is unconfirmed against Google's page. — [myarchitectai.com](https://www.myarchitectai.com/blog/nano-banana-api-pricing)
- GPT Image 2 output at 1024×1024 costs about $0.006 (low), $0.053 (medium) and $0.211 (high). Image tokens cost $8 per 1M input and $30 per 1M output, so reference-heavy edits cost more. — [blog.segmind.com](https://blog.segmind.com/ai-image-gen-pricing-compared-nano-banana-2-vs-seedream-5-0-vs-gpt-image-2-2026/); [aireiter.com](https://aireiter.com/blog/gpt-image-2-api-pricing)
- Third-party resellers' prices vary widely, from a flat $0.008 per image (Atlas Cloud) to $0.422 for high quality (EmpirioLabs). — [atlascloud.ai](https://www.atlascloud.ai/blog/gpt-image-2-api-guide); [catalog.empiriolabs.ai](https://catalog.empiriolabs.ai/models/gpt-image-2)

**Local (RTX 4060 8GB)**
- Flux LoRA training on 8GB is reported as possible but slow (6+ hours) at 768×768 with an FP8-quantized Flux. — [promptus.ai](https://www.promptus.ai/workflow/how-to-train-lora-models-with-flux-in-comfyui)
- FluxGym defaults (gradient checkpointing plus 8-bit Adam) fit in 12GB. The Kohya ecosystem recommends 16GB as the floor for Flux training. — [dev.to](https://dev.to/thurmon_demich/best-gpu-for-fluxgym-in-2026-5-picks-for-flux-lora-training-pp6)
- A 2026 hardware guide says Flux and SD3.5 LoRAs need 24GB minimum. The Flux 2 Klein 4B base (meant for fine-tuning) lists 13GB minimum. — [vrlatech.com](https://vrlatech.com/?p=81866); [insiderllm.com](https://insiderllm.com/guides/flux-locally-complete-guide/)
- Qwen-Image-Edit-2511 improves character consistency and multi-person group shots over 2509. ComfyUI supports it natively, with LoRA capabilities built in. GGUF quants are on Hugging Face (Unsloth and others). — [docs.comfy.org](https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit-2511); [huggingface.co/unsloth](https://huggingface.co/unsloth/Qwen-Image-Edit-2511-GGUF)
- A community OpenArt workflow uses the 2511 Q8_0 GGUF with reference control to keep facial identity, in about 4 steps. — [openart.ai](https://openart.ai/workflows/lordtzeentch/convertomatic---qwen-edit-image-2511/VJtUpdvckSQ2aKWWBxnQ)
- RunComfy has ready-made 2511 workflows for consistent characters and multi-image merge. — [runcomfy.com](https://www.runcomfy.com/comfyui-workflows/models/qwen-image-edit)

### Inferences
- For a stylised, illustrated grandpa and grandson, a reference sheet plus Nano Banana 2 (about $0.07 per 1K image) or the ChatGPT/Gemini consumer apps costs only a few dollars a month at 30–60 panels. That is far cheaper in time than training a LoRA.
- Flat or simple illustration styles (thick outlines, limited palette, distinctive props such as grandpa's cardigan and glasses) make drift less visible than semi-realistic styles. This is a general practice inference and not sourced.
- Because the user must not depict their real grandfather, the reference sheet should be designed from a text description, not from family photos. Hosted models also keep any uploaded photos, which is a privacy issue.
- The 8GB GPU is better used for local inference (Qwen-Image-Edit GGUF at a lower quant, or SDXL with IP-Adapter) than for Flux LoRA training. Training could be rented on a cloud GPU for a few dollars if a LoRA is ever needed (no source on rental pricing was gathered).

### Gaps
- No primary-source confirmation of current Gemini or OpenAI prices or free-tier quotas in the consumer apps (ChatGPT free image limits, Gemini app daily limits), because the official pages could not be fetched.
- No independent benchmark of consistency across separate sessions. All rankings are blog opinions.
- No VRAM figures verified for Qwen-Image-Edit-2511 GGUF quants on 8GB. Flux Kontext and Ideogram Character were not covered in the results retrieved.
- Midjourney Omni Reference GPU-time cost (it is believed to cost more GPU time than a normal job) was not confirmed. The docs page was blocked.

## Q2. Which tools render Traditional Chinese text correctly? Workarounds

### Takeaway
GPT Image 2 (April 2026) and Qwen-Image are the strongest for Chinese text in general, but no source benchmarks Traditional Chinese specifically, and published Chinese-text benchmarks use the mainland standard character set. The safe production pattern is to generate the art with no text, then add Traditional Chinese text in Canva, Figma or code.

### Cited Findings
- GPT-Image-2 launched 2026-04-21. The vendor claims 99% typography accuracy (up from 90–95%). It is not broken out by Traditional characters. — [medium.com/@tentenco](https://medium.com/@tentenco/insane-gpt-image-2-nails-chinese-text-90-of-the-time-523122742660); [finance.biggo.com](https://finance.biggo.com/news/202604240451_GPT-Image-2-text-rendering-analysis)
- Hands-on tests of GPT-Image-2 with calligraphy and an exam-paper mockup were good, but did not test Traditional characters. — [finance.biggo.com](https://finance.biggo.com/news/202604240451_GPT-Image-2-text-rendering-analysis)
- Qwen-Image is described as "the model to beat" for text, and Seedream 5.0 is also strong. Neither is split by Traditional vs Simplified. — [secondtalent.com](https://www.secondtalent.com/resources/chinese-llms-for-ai-image-generation/); [find-aiverse.com](https://find-aiverse.com/en/posts/2026-03-30-ai-54628f/)
- LongCat-Image (Meituan, 6B) claims 95%+ on complex Traditional Chinese. This comes from an unverified third-party page. — [longcat-video.org](https://longcat-video.org/blog/longcat-image-generation-tutorial); [longcatai.org](https://www.longcatai.org/models/image)
- GLM-Image claims 90% Chinese accuracy, citing an unnamed "Zhipu AI Evaluation". This is unreliable. — [glmimage.app](https://glmimage.app/blog/best-ai-text-rendering)
- Methodology caveat: the ChineseWord benchmark draws characters from the mainland Ministry of Education standard set, and VLM judges fail on rare characters (LongCat switched to PP-OCRv5). Published scores may therefore overstate Traditional-character accuracy. — [arXiv 2604.28185](https://arxiv.org/pdf/2604.28185)
- Recommended comic workflow: a layout app (Canva or Krita) handles pages and lettering, separately from panel generation. — [creativeainews.com](https://www.creativeainews.com/articles/how-to-make-a-comic-with-ai-2026/)

### Inferences
- For speech bubbles and carousel copy in Traditional Chinese, generate text-free panels with blank bubble areas, then letter them in Canva or Figma with a Traditional Chinese font (for example Noto Sans TC or jf open 粉圓, which are free). This avoids glyph errors such as Simplified forms slipping in (说/說) and lets the same art be reused for Xiaohongshu with Simplified text.
- If text is generated in-image, an OCR check (such as PP-OCRv5) can automatically flag wrong characters before posting.

### Gaps
- No source tested Traditional Chinese accuracy for Nano Banana 2 or Pro, Midjourney or Ideogram.

## Q3. Comic and multi-panel workflows, Canva templates, batch generation

### Takeaway
The documented 2026 workflow is: script in an LLM, then a reusable "character block + shot type + action + fixed style line" prompt, then one reference sheet reused for every panel, then layout and lettering in Canva. A 6–12-panel story takes "a few hours" by hand. Batching in Canva needs either the in-app Bulk Create feature or the Connect API, and the API's autofill requires Canva Enterprise.

### Cited Findings
- Pipeline: a chat model for the script, an image model with character reference for the panels, then Canva or Krita for layout and lettering. A 6–12-panel story takes a few hours. — [creativeainews.com](https://www.creativeainews.com/articles/how-to-make-a-comic-with-ai-2026/)
- Prompt structure: a saved character block, the shot type, the action from the script, and a fixed style line repeated in every panel. — [creativeainews.com](https://www.creativeainews.com/articles/how-to-make-a-comic-with-ai-2026/)
- Build a clean reference lineup first, then use that single image as the only reference for a 6-panel storyboard. Asking a character to "transform" can produce duplicates. The vendor admits consistency is "not always perfect". — [weshop.ai](https://www.weshop.ai/solutions/models/nano-banana-2-1-consistent-character-storyboard)
- Nano Banana plus Canva is positioned as a fast route for generation, brand consistency and editing. Manga-specific tools give finer panel control. — [timewell.jp](https://timewell.jp/en/columns/nanobanana-canva)
- Canva Connect API autofill works in three steps: get the brand-template dataset, create an autofill job (asynchronous), then poll the job. — [canva.dev autofill guide](https://www.canva.dev/docs/connect/autofill-guide/); [canva.dev brand templates](https://canva.dev/docs/connect/api-reference/brand-templates/)
- The Brand Template and Autofill APIs require the user to be in a Canva Enterprise org. Developers without Enterprise can request access in the Developer Portal for genuine development use. — [canva.dev autofill guide](https://www.canva.dev/docs/connect/autofill-guide/)
- There is no dedicated bulk endpoint. The pattern is one autofill job per row, and a third-party skill implements bulk create this way. — [tessl.io](https://tessl.io/registry/skills/github/openai/plugins/canva-bulk-create)
- The Apps SDK, Connect APIs and MCP are unified in the Canva Developers SDK. — [canva.dev](https://www.canva.dev/docs/connect/reference-apps/nourish/)
- An example AI comic-strip generator uses Flux plus Veo 3. — [mindstudio.ai](https://mindstudio.ai/blog/build-ai-comic-strip-generator-flux-veo-3)

### Inferences
- For a solo creator without Enterprise, the cheapest batch route is a script that calls the image API to make panels, then composes panels, bubbles and Traditional Chinese text with Python (Pillow) or HTML-to-PNG (Playwright) templates. This replaces Canva for repetitive 4-panel and carousel layouts, leaving Canva for one-off designs. Canva's in-editor "Bulk Create" (CSV into a template) is a manual but quick option on Canva Pro. It was not verified in this research.

### Gaps
- Canva Pro pricing and the current Bulk Create limits in Taiwan were not retrieved. No source on dedicated comic tools (for example Dashtoon or LlamaGen) with pricing.

## Q4. Short vertical video: image-to-video, captions, TTS, free tiers, cost per clip

### Takeaway
Animate the existing consistent character stills with image-to-video, rather than text-to-video, to keep the character on-model. Kling is the cheapest and has the most generous free usage, but free output is watermarked and non-commercial, so Standard (about $10 a month) is the minimum for clean output. Veo is available through Google AI Pro ($19.99 a month, about 50 Veo 3 Fast videos). **Sora is gone**: the app closed on 2026-04-26 and the API on 2026-09-24. CapCut auto-captions have reportedly moved behind Pro in many regions. Free Taiwan-Mandarin TTS is available through Edge/Azure neural voices.

### Cited Findings
**Image-to-video**
- Kling's free tier is about 66 credits a day (about 2 videos at 720p). Free output is watermarked and non-commercial. Paid plans are about $10 (Standard), $37 (Pro), $92 (Premier) and $180 (Ultra) a month. — [whichoneisreal.com](https://whichoneisreal.com/compare/best-free-ai-video/); [layer3labs.io](https://www.layer3labs.io/guides/best-ai-video-generators)
- Sources conflict on the Kling free refill: "66 free credits per day" vs "no fixed monthly credits, event-based promos". — [crepal.ai](https://crepal.ai/blog/aivideo/is-kling-ai-free-pricing/); [eesel.ai](https://eesel.ai/blog/kling-ai-pricing)
- A 5-second Kling clip costs roughly 20–35 credits. One source says 30 credits for 720p and 60 credits for 1080p with native audio. Standard is the cheapest plan with commercial use and no watermark: about $10 a month (about $6.60 a month billed yearly) for 660 credits a month. — [photonpay.com](https://www.photonpay.com/hk/blog/article/kling-ai-pricing?lang=en); [atlascloud.ai](https://www.atlascloud.ai/blog/guides/kling-ai-pricing)
- Kling's API costs about $0.10/s, or about $0.032/s on Replicate. — [devtk.ai](https://devtk.ai/en/blog/ai-video-generation-pricing-2026/); [aifreeapi.com](https://www.aifreeapi.com/en/posts/seedance-2-vs-kling-3-vs-sora-2-vs-veo-3)
- Hailuo offers about 150 signup credits, with paid plans from about $10 to $200 a month. — [getaiperks.com](https://www.getaiperks.com/en/blogs/70-free-ai-video-credits-2026)
- Veo 3 comes with Google AI Pro at $19.99 a month, which includes about 50 Veo 3 Fast videos. API prices conflict: $0.75/s (older Veo 3) vs from $0.15/s (Veo 3.1 Fast). — [getaiperks.com](https://www.getaiperks.com/en/blogs/44-best-ai-video-generators-2026); [digitalmaker.ai](https://digitalmaker.ai/blog/veo-3-vs-sora-2-vs-kling-ai-video-model-comparison-2026)
- Sora: the app shut down on 2026-04-26 and the Videos API plus all sora-2 aliases on 2026-09-24, with no successor listed. Pre-September pricing articles are stale. — [techjacksolutions.com](https://techjacksolutions.com/ai-brief/openai-videos-api-sora-2-deprecated-september-2026/); [kaopiz.com](https://kaopiz.com/en/articles/sora-shutdown-guide/); [Wikipedia](https://en.wikipedia.org/wiki/Sora_(text-to-video_model))
- The reasons given for the Sora shutdown (GPU cost, $2.1M lifetime revenue) are unconfirmed, and OpenAI's notice gives no reason. — [arboraistudio.com](https://arboraistudio.com/blog/why-is-openai-shutting-down-sora-the-shift-to-ai-agents/); [futurumgroup.com](https://futurumgroup.com/insights/openai-sora-discontinuation-what-the-end-of-a-platform-means-for-enterprise-ai-strategy/)
- Runway and Pika are covered only in aggregate free-limit lists. No current figures were confirmed. — [whichoneisreal.com](https://whichoneisreal.com/compare/best-free-ai-video/)

**Captions**
- CapCut auto-captions reportedly moved behind Pro (in a 2025 restructure, or Feb 2026 per another source). One source says annual Pro went from $77 to $179.99. — [descript.com](https://descript.com/blog/article/capcut-captions-arent-free-anymore-heres-a-better-option); [fluxnote.io](https://fluxnote.io/guides/capcut-ai-features-free-vs-paid-2026)
- This is contradicted: other sources say basic auto-captions are still free, and an Aug 2026 forum post says it depends on platform, region and app version. Several of these sources are competitors' blogs. — [zsky.ai](https://zsky.ai/blog/is-capcut-ai-free); [forum.aejuice.com](https://forum.aejuice.com/t/aejuice-auto-captions-vs-capcut-auto-captions-2026/2173)

**TTS (Taiwan Mandarin)**
- Azure zh-TW neural voices are HsiaoChen (female), YunJhe (male) and HsiaoYu. — [json2video.com](https://json2video.com/ai-voices/azure/voices/zh-tw-hsiaochenneural/); [json2video.com](https://json2video.com/ai-voices/languages/chinese/taiwan/)
- The open-source `edge-tts` tool uses these voices for free with no API key (voices are listed with `--list-voices`). The terms of the free endpoint are unverified and could change. — [clawhub.ai](https://clawhub.ai/hamlet0168/edge-tts-zh); [zenn.dev](https://zenn.dev/kun432/scraps/5c0d5d08857375)
- ElevenLabs Taiwan-accent voices are described as more expressive. This is a vendor claim. — [json2video.com](https://json2video.com/ai-voices/languages/chinese/taiwan/)

### Inferences
- The cheapest explainer-Reel pipeline: still panels, then a Ken Burns or pan effect plus edge-tts narration plus subtitles generated from the script itself (the script text is known, so no speech-to-text is needed). This can be assembled with FFmpeg or MoviePy at $0. Spend Kling or Veo credits only on 1–2 "hero" motion shots per Reel.
- Since the project is a voice companion, its own TTS output could narrate the Reels. That would double as a product demo.
- Text-to-video without a reference image is likely to drift the character. Image-to-video from the reference panels is the consistency-safe path. This is consistent with Q1 findings but not tested directly.

### Gaps
- No verified Hailuo, Runway or Pika current per-clip prices. No source on 剪映 (the China version of CapCut) caption terms. Edge-TTS terms for commercial use are unverified. No verified Taiwan-specific CapCut pricing.

## Q5. Automation via API and orchestration

### Takeaway
Everything except CapCut can be scripted. Image generation is available through the Gemini API (Nano Banana 2 or 2.1, with a Batch discount) or the OpenAI image API (GPT Image 2, up to 16 references). Video is available through Kling or Veo APIs, and Sora is no longer an option. Canva autofill needs Enterprise. An LLM such as Claude can write scripts, captions and prompts, and orchestrate the calls.

### Cited Findings
- Nano Banana 2.1 Batch pricing is $15 per 1M image-output tokens, half the standard $30. — [evolink.ai](https://evolink.ai/es/collections/nano-banana)
- The GPT Image 2 API supports editing with up to 16 reference images, billed per token. — [aireiter.com](https://aireiter.com/blog/gpt-image-2-api-pricing)
- Kling and Veo per-second API prices are listed above. Sora API removed 2026-09-24. — [devtk.ai](https://devtk.ai/en/blog/ai-video-generation-pricing-2026/); [techjacksolutions.com](https://techjacksolutions.com/ai-brief/openai-videos-api-sora-2-deprecated-september-2026/)
- The Canva autofill API is asynchronous and gated by Enterprise. — [canva.dev](https://www.canva.dev/docs/connect/autofill-guide/)
- JSON-to-video services (for example JSON2Video) bundle TTS voices and video assembly by API. Free voiceovers are limited to 60s. — [json2video.com](https://json2video.com/ai-voices/languages/chinese/taiwan/)

### Inferences
- A suggested weekly batch run: an LLM drafts 7 scripts (4-panel comic text, carousel copy and Reel narration), then a script calls Nano Banana 2 with the reference sheet for each panel, then a Pillow or HTML template letters the Traditional Chinese text, then edge-tts and FFmpeg build the Reel. A human reviews before posting. At about $0.07 per image, a week of about 40 images costs about $3. This is an estimate from the cited prices.

### Gaps
- Rate limits and free-tier API quotas for Gemini and OpenAI could not be verified (official pages were blocked). The Instagram and Threads publishing APIs were out of scope here.

## Q6. Licensing, commercial-use terms, watermarks and disclosure (C2PA/SynthID)

### Takeaway
OpenAI assigns output rights to the user. Midjourney's paid plans allow commercial use, but free or trial output is CC BY-NC and images are public unless on Pro or Mega. Kling's free output is watermarked and non-commercial. Gemini's free-tier commercial status is disputed. Purely AI images may not be copyrightable in the US. Gemini output carries SynthID, and ChatGPT output carries C2PA metadata, with OpenAI announcing it will add SynthID. Platforms can strip metadata, so manual "AI-generated" disclosure is the reliable route.

### Cited Findings
- OpenAI: "OpenAI hereby assigns to you all its right, title and interest in and to Output". OpenAI may use outputs to improve services unless the user opts out. — [terms.law](https://terms.law/ai-output-rights/comparison); [terms.law FAQ](https://terms.law/FAQ/ai-tools/ai-commercial-use-faq.html)
- Midjourney: companies with more than $1M in revenue need Pro ($60/mo) or Mega ($120/mo). Free or trial images are CC BY-NC 4.0. There is no indemnity. Only Pro and Mega include private (Stealth) mode. — [terms.law Midjourney 2026](https://terms.law/2026/01/15/midjourney-commercial-use-rights-complete-2026-guide/)
- Gemini free-tier commercial use: one comparison says "No" and another says outputs are owned on all tiers. This is unresolved. — [terms.law](https://terms.law/Demand-Letters/Guides/ai-tools-commercial-rights-comparison.html); [licenseorg.com](https://licenseorg.com/blog/ai-commercial-use-guide-2026)
- Kling: free output carries a visible logo, and commercial rights come only with paid membership. — [eesel.ai](https://eesel.ai/blog/kling-ai-pricing); [atlascloud.ai](https://www.atlascloud.ai/blog/guides/kling-ai-pricing)
- US Copyright Office: AI output without sufficient human authorship is not copyrightable. — [terms.law](https://terms.law/FAQ/ip-copyright/ai-content-ownership-faq.html)
- Google says more than 20B pieces of content have been watermarked with SynthID. The Gemini app can check SynthID and C2PA, and SynthID verification is live in Google Search (I/O 2026). — [techspot.com](https://www.techspot.com/news/112462-google-making-ai-images-easier-create-deepfakes-easier.html); [petapixel.com](https://petapixel.com/2025/11/21/you-can-now-ask-google-gemini-whether-an-image-is-ai-generated-or-not)
- ChatGPT images carry C2PA metadata, which is often stripped when shared. OpenAI announced it will embed SynthID in ChatGPT, Codex and API images. — [trustinsights.ai](https://www.trustinsights.ai/blog/2026/04/ai-watermarks/); [bensbites](https://bensbites.beehiiv.com/p/daily-digest-detecting-ai-images)
- Instagram scans for C2PA. Its earlier labelling attempts caused controversy. — [aichief.com](https://aichief.com/news/crunch-time-for-ai-labelling-systems/)

### Inferences
- For a nonprofit open-source project, commercial-use restrictions matter less, but free Kling or Midjourney trial output is still technically non-commercial and Kling's carries a watermark. Paid tiers or the OpenAI and Gemini APIs avoid the issue.
- Disclosing "AI 生成插畫，角色為虛構" (AI-generated illustration, fictional characters) in captions builds trust in the dementia-care context and avoids any appearance of depicting a real patient, which matches the user's own constraint.

### Gaps
- No 2026 source confirmed how Meta's "AI info" label currently behaves on Instagram and Threads, or whether Meta reads SynthID. Xiaohongshu AI-labelling rules were not researched. Official Google and Kling terms were not fetched.
