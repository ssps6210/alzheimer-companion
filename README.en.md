<p align="center">
  <a href="README.md">繁體中文</a> · <a href="README.zh-CN.md">简体中文</a> · <b>English</b>
</p>

<h1 align="center">Alzheimer's Voice Companion</h1>

<p align="center">
  <b>Keep an elder company in the voice of someone they love.</b>
</p>

<p align="center">
  <a href="https://github.com/ssps6210/alzheimer-companion/releases"><img alt="Download APK" src="https://img.shields.io/badge/📱_Tablet_App-Download_APK-2ea44f?style=for-the-badge"></a>
  &nbsp;
  <a href="#security"><img alt="Data stays on your computer" src="https://img.shields.io/badge/🔒_Your_data-stays_on_your_computer-2b7bba?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
  <img alt="for dementia care" src="https://img.shields.io/badge/for-dementia%20care-ff8c69">
  <a href="../../actions/workflows/privacy.yml"><img alt="privacy scan" src="https://github.com/ssps6210/alzheimer-companion/actions/workflows/privacy.yml/badge.svg"></a>
</p>

> **This started somewhere personal.**
>
> My grandfather has had severe Alzheimer's for almost three years. He mistakes me for my dad, for my uncle, once for my great-uncle. I told him "I'm your grandson" more times than I can count. It never worked.
>
> Then one afternoon I bought a carton of the milk tea I drank as a kid, put the straw in my mouth, and walked into his room sipping it — the way I did when I was small. He paused. Then he smiled: "When did you get here? Are you studying hard? Have you eaten?"
>
> He knew me.
>
> What he needed wasn't an explanation. It was something he still recognised: a grandson with a straw in his mouth.
>
> I live far away and can't be there every day. So I wondered — if a carton of milk tea can be something familiar, could a familiar **voice** be too?
>
> He may not remember who I am. But he remembers the kid with the milk tea.

---

An elder presses **one big button** and speaks. It answers in **a voice you chose** — someone in the family. Ask it the same question a hundred times and it answers a hundred times, never "you just asked me that."

## 🚀 Three steps

**The elder only needs a tablet.** Everything runs on your own computer. No account to create, no server to rent.

| | What you do | How long |
|---|---|---|
| **1** | Run one line on your PC: `powershell -ExecutionPolicy Bypass -File install.ps1` | Depends on bandwidth (several GB) |
| **2** | Grab `elder-companion.apk` from [**Releases**](https://github.com/ssps6210/alzheimer-companion/releases) and install it on the tablet | 1 minute |
| **3** | Open the app, scan the QR on your computer screen (or tap "find automatically") | 10 seconds |

No NVIDIA GPU? Run `install_cpu.ps1` instead — plain Windows, no WSL, same cloned family voice, just slower.

**First time?** The [step-by-step install guide](docs/install-guide.en.md) is written for non-engineers.

## 📱 Screenshots

<p align="center">
  <img src="docs/screenshots/companion-day.png" width="30%" alt="Elder's screen (day)">
  &nbsp;&nbsp;
  <img src="docs/screenshots/companion-night.png" width="30%" alt="Elder's screen (night)">
</p>
<p align="center"><img src="docs/screenshots/setup.png" width="66%" alt="Family console"></p>
<p align="center"><sub>Elder's screen: one big button, day/night automatic, old photos while idle　｜　Family console <code>/setup</code>: set the voice</sub></p>

<a id="security"></a>

## 🔒 Your family's voice stays with you

**The recordings you make, your elder's photos, everything they say — all of it stays on the computer you run this on.**

There is no server to sign up for. Even if we wanted your data, we have no way to receive it.

The three questions people actually ask:

**"Could my dad's voice be used in a scam?"**
The audio files never leave your machine. Before the system will use someone's voice, it requires **that person to say a consent sentence out loud** in the same recording — no consent sentence, no voice. And every clip it speaks carries an inaudible marker, so anyone can verify it was AI-generated rather than really said by them.

**"Can anyone listen in on our conversations?"**
Conversation history is a file on your computer; it is never uploaded. One thing does go online: after your elder speaks, the **text** (not the audio) goes to an AI service to compose a reply, the same way typing into a search box does. If you'd rather that stayed local too, you can run fully offline — see the technical notes below.

**"I'm not good with computers. Could I leak something by mistake?"**
There's nothing to misconfigure. The ability to send personal data anywhere was never written into this project. Leaking it would take someone deliberately modifying the code.

<details>
<summary><b>Technical notes</b></summary>

- Voices, photos, `memory.json`, `patterns.json` and consent records live on the local filesystem only. There is no outbound path for any of them.
- The single outbound call is `POST {llm.base_url}/chat/completions` carrying conversation text, authenticated with the user's own API key. Point `llm.base_url` at a local OpenAI-compatible endpoint such as [Ollama](https://ollama.com) for a fully offline setup.
- No personal data ships in the repo, enforced on every push: [`tools/privacy_scan.py`](tools/privacy_scan.py) scans tracked files in CI and fails the build on audio, memory files or key patterns. It exists to catch the two things that actually happen — a malformed ignore rule, and `git add -f`.
- **The family console `/setup` is password-protected.** It can read the elder's full conversation history, so it is never left open. A password is generated on first start, written to `.env` as `SETUP_PASSWORD` and printed in the launcher window; the username is `family`. The elder's screen `/` is deliberately not protected — an elder cannot type a password, and that screen holds nothing private.
- Consent gate: the consent sentence must appear in **the same clip that becomes the voice**, so the speaker is the consenter. Disable with `CONSENT_REQUIRED=0`.
- Watermark: [AudioSeal](https://github.com/facebookresearch/audioseal), running on CPU so it costs no VRAM. Verify with `python tools/detect_watermark.py <file>`. Disable with `WATERMARK=0`.
  This is **after-the-fact verifiability, not protection** — re-encoding can strip the marker. It proves a clip was synthesised; it does not stop a determined person.

</details>

## ✨ What it does

- 🎙️ **Uses a family member's voice** — upload a clear 10–30 second recording and the voice is set. No voice ships with this repo.
- 🛡️ **Dementia-care guardrails** — never corrects, never rushes. When they ask for someone who has died, it comforts them instead of breaking the news. Words like a fall or chest pain **alert the family**.
- 📷 **Old photos while idle** (reminiscence therapy) — photographs, not an animated synthetic face.
- 📈 **Family can see how they're doing** — what they've been talking about lately, which hours they most want company. Companionship observation, not a medical assessment.
- 🧓 **Built for old eyes and hands** — big button, warm colours, automatic day/night; press-and-hold or continuous conversation.

The guardrails aren't only prompt text: [`tests/test_safety.py`](tests/test_safety.py) runs nine high-risk scenarios (asking for a dead relative, repeating a question, asking to go outside alone) against the live model and checks the reply crossed no lines. Required before any persona change.

## 🌏 Language

Interface, speech recognition and synthesis, care guardrails and personas all
switch together: set `language: zh-TW` (default), `zh-CN` or `en` in `conf.yaml`.
Packs live in [`lang/`](lang/) — copy one to add a language. Anything you leave
untranslated falls back to Chinese rather than rendering blank.

> Switching language is not only interface text. The **guardrail keywords move
> too** — urgent phrases, never-say terms, the consent sentence. A Chinese
> keyword list matches nothing in an English deployment, so the guardrails would
> fail silently; that is why they live in the language pack.

## 🖥️ Requirements

Runs on **a computer you set up**; the elder just needs a tablet with Chrome. **An NVIDIA GPU is recommended** — speech is fast and steady (the author uses an RTX 4060 8GB). Without one, the CPU build gives you the same cloned family voice, fully local, a bit slower. Windows 10 / 11.

Stack: STT `faster-whisper` (local) · LLM any OpenAI-compatible endpoint · TTS `Qwen3-TTS` zero-shot cloning. Details in [`PROJECT.md`](PROJECT.md); to help out, see [`CONTRIBUTING.en.md`](CONTRIBUTING.en.md).

## ☕ Support

If this helps you or your family: ⭐ **star it**, so more families caring for someone with dementia can find it.

<p><a href="https://buymeacoffee.com/ssps6210noa"><img src="https://img.shields.io/badge/Buy_me_a_coffee-ffdd00?style=for-the-badge&logo=buymeacoffee&logoColor=black" alt="Buy me a coffee"></a></p>

## ⚠️ Disclaimer

A **companionship** tool, **not a medical device**. It cannot replace medical care or emergency services. Use with family supervision.

## 📄 License

[MIT](LICENSE) — use, modify and distribute freely. Elder-care and other non-profit use especially welcome.
