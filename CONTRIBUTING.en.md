<p align="center">
  <a href="CONTRIBUTING.md">繁體中文</a> · <b>English</b>
</p>

# Contributing

Thank you for wanting to help. The people who use this are **elders with
dementia**: they cannot report a bug, cannot complain, and will not know when
something has broken. The rules here are stricter than a typical project — please
read this page first.

---

## Three things that are not negotiable

**1. Never commit personal data**

Voices, photos, recordings, conversation history, keys — none of it belongs in
the repository. `.gitignore` blocks them and a privacy scan in CI is the second
line of defence. Run it yourself before opening a PR:

```bash
python tools/privacy_scan.py
```

**2. The care guardrails do not get weakened**

Never correcting, never rushing, comforting rather than breaking the news when
they ask for someone who has died, never inventing facts, never claiming a
specific identity — these are care ethics, not product features. **Any PR that
touches a persona must run the safety suite and include the result:**

```bash
venv\Scripts\python.exe tests\test_safety.py
```

It runs nine high-risk scenarios against a real model (needs your own API key;
it costs a little). The suite once caught the model inventing an entire visit —
"A-ming came to see you yesterday, he brought…" — exactly the fabrication rule 11
forbids, and the kind of thing an elder will try to reconcile with reality.
**Red means do not merge.**

Guardrails are also probabilistic. Even the best-written persona fabricates
roughly 2 times in 5 at temperature 0.7, which is why the never-say category has
a deterministic backstop in `guard_reply()`. Use `--repeat 5` when judging
whether a persona change actually holds.

**3. Consent and watermarking stay on by default**

Voice cloning is dual-use. Setting up a voice requires the owner's spoken
consent, and generated speech carries an AudioSeal watermark. Both **default to
on**. Offering `CONSENT_REQUIRED=0` / `WATERMARK=0` for advanced users is fine;
changing the defaults is not.

---

## Development setup

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1      # with an NVIDIA GPU
powershell -ExecutionPolicy Bypass -File install_cpu.ps1  # without one
```

Architecture, what each service does, and the potholes already hit are in
[`PROJECT.md`](PROJECT.md) (Traditional Chinese).

## Before opening a PR

- [ ] `python tools/privacy_scan.py` passes
- [ ] Touched a persona, fixed phrases or LLM settings → `tests\test_safety.py` green
- [ ] Touched `companion_web.py` → `python -m py_compile companion_web.py` passes
- [ ] Touched Android → the CI build passes (check Actions after pushing)
- [ ] Explain **why**, not only what changed

## Especially welcome

- **Localisation** — Taiwanese Hokkien and Hakka recognition and speech. This
  matters enormously for dementia care in Taiwan, where many elders' first
  language is not Mandarin. Currently blocked on model availability; if you know
  this area, you are badly needed. See [`lang/`](lang/) for how a language pack
  works.
- **Guardrails** — more high-risk scenarios in [`tests/safety_cases.yaml`](tests/safety_cases.yaml)
- **Personas** — tones for different stages and different relationships
  (see [`docs/人設範例.md`](docs/人設範例.md))
- **Accessibility** — larger type, higher contrast, simpler interactions

## Language and documentation

Code comments and docs are written in Traditional Chinese, explaining **why**
rather than only what. English is welcome in new files; the language packs and
this file show the pattern.

Text an elder or family member will read should say what to do, not what to avoid
("we'll walk slowly" rather than "don't run") — it is easier to follow.

**Do not mix 失智 and 阿茲海默 / dementia and Alzheimer's:**

| Talking about | Use |
|---|---|
| The story this project came from (the author's grandfather's diagnosis) | Alzheimer's / 阿茲海默 |
| The product, the guardrails, the audience | dementia / 失智 |

Alzheimer's is one cause of dementia (a bit over half of cases in Taiwan). The
guardrails work regardless of cause, so narrowing that language would be
inaccurate and would read as excluding families dealing with vascular or Lewy
body dementia. Simplified Chinese copy uses 阿尔茨海默 and 认知障碍.

## Licence

Opening a PR means you agree to release your contribution under the [MIT](LICENSE)
licence.
