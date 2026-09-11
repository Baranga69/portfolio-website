# Project context

Personal portfolio site for Keith Baranga (GitHub: @Baranga69), Senior Mobile
Engineer in Nairobi, Kenya. The site supports applications for **global remote
Android engineering roles**. Its audience is a hiring manager in another
timezone who has sixty seconds and no chance to talk to Keith first.

Installed and building as of 2026-09-10 (Astro 7.3.2, Node 24, 0 npm
advisories). Output is one page, 17KB raw / 5.4KB gzipped, zero client-side
JavaScript, plus 212KB of self-hosted fonts and no third-party requests at all.

## Design direction — do not quietly redesign this

The site is structured as a **lexicon**: each project is a dictionary entry with
a headword, an italic classifier, and numbered senses in a hanging indent. This
is deliberate, and Keith reconfirmed it on 2026-09-10 against two alternatives
(an exploded-assembly/workbench frame, and dropping the device entirely).
Kamusi 2.0 earns it, and so does a long fantasy-reading habit — the appendix at
the back of the book is the same object. The layout encodes the content rather
than decorating it.

The through-line the site argues, in Keith's own framing: he works a layer below
where most people stop. Sensors rather than a vendor SDK, the lexicon data
rather than the app over it, the board rather than the replacement unit, the
printed part rather than the bought one.

Constraints agreed with Keith:

- **One bold idea only.** The masthead entry is it. Everything else stays quiet.
  Keith asked on 2026-09-10 whether the wide side margins wanted doodles; the
  answer was no, and the reasoning is worth keeping: doodles would be a second
  bold idea, they encode nothing (the lexicon works because the form *is* the
  content), they read as creative-portfolio against copy doing technical work,
  and they would be invisible at 320px where the mobile-first pitch actually
  lives. The margin instead carries a **marginal gloss** — the section label,
  relocated there above 72rem. That is reference-book typography, costs no
  bytes, and takes the one element closest to an eyebrow label out of the
  reading column.
- **No cream-and-terracotta.** Palette is cool grey-green paper (`--paper #DDE1DA`),
  pine ink (`--ink #14201C`), one deep teal accent (`--accent #1F5F73`).
- **Type:** Newsreader (variable serif, entries and body) and Archivo (sans, nav
  and metadata). Two families, clearly distinct.
- **Avoid the generated-page tells:** all-caps eyebrow labels, middle-dot meta
  strings (`A · B · C`), monospace for small labels, `→` appended to links,
  identical rounded cards with soft grey shadows, fade-and-slide-up on every
  section.
- **Motion:** exactly one orchestrated moment (the masthead settling in on load).
  No scroll-triggered reveals. `prefers-reduced-motion` is respected.
- **Numbered senses are justified** because dictionary senses genuinely are
  enumerated. Do not add `01 / 02 / 03` markers anywhere the content is not a
  real sequence.
- **Performance is part of the brief.** Keith's expertise is offline-first
  mobile; a heavy portfolio would contradict the pitch. Ship no client-side JS
  unless there is a real reason. Target sub-second on a mid-range Android over a
  congested mobile network.

## Architecture

```
src/layouts/Base.astro       shell, Google Fonts, meta tags
src/components/Entry.astro   one lexicon entry (headword, classifier, href, senses, note, stack)
src/pages/index.astro        all content as arrays in frontmatter
src/styles/global.css        tokens first, then layout
```

Content is data at the top of `index.astro`. Adding a project means adding an
object to an array, not editing markup. Keep it that way.

## Facts — get these right

- Current role: Senior Mobile Engineer at Tappi (tappi.app). Previously GT Bank
  Kenya, then Enigma Consultancy.
- **Target roles: Android Engineer.** The site leads with Android and Kotlin;
  "mobile generalist" is not the pitch.
- At Tappi he built **Tappi: Caller ID & Expenses** (exact store title) —
  `app.tappi.aicontactmanager`, 4.4 stars. Built from the ground up. MVVM with
  Hilt, Compose, local SQLite as the system of record with versioned migrations.
  Transaction parsing/classification by regex, heuristics and rules; payment
  reconciliation across multiple sources. He owned the UI/UX. Lead entry.
- **Local-first here is a privacy decision, not just a network one** — user
  transactions are processed and held on the handset deliberately. Say it that
  way round; it is the stronger and truer claim.
- He also built the app's **chat assistant** solo: an orchestration layer over
  DeepSeek with tool calls, answering questions about the user's own finances
  with charts rendered inside the conversation. Production LLM tool-calling on a
  mobile client, and the most current thing on the page.
- **Scale: ~10,000 installs, ~1,000 DAU** (from Keith, 2026-09-11). The CV's
  "~15,000 active users" is NOT supportable — it exceeds the install base, and
  the page now links the store listing where a reader can see the badge. Use the
  install/DAU figures. **The CV needs correcting to match.**
- Tappi tenure: Junior (Sep 2022) → Mid-level (Sep 2023) → Senior (Oct 2025).
  Shipped four Play Store apps: Tappi, MTN Thryve, MTN GoDigital, PBP Agent.
  Also built Tappi Link. Career start was Enigma, July 2021 — five years total.
- Telemetri and Kamusi 2.0 are **personal** projects, not employer work.
- Core stack: Kotlin, Java, Dart, Jetpack Compose, Flutter, Firebase, CI/CD.
  Also Swift/Objective-C on the iOS side. Depth in fintech, payments
  integrations, offline-first architecture.
- **GT Bank Kenya** (Mar–Sep 2022): banking systems with a team in Nigeria,
  paperless automated account creation, and he led the regional money transfer
  service across GTBank's African subsidiaries.
- **Enigma Consultancy** (Jul–Dec 2021): led a custom Java CRM, 5x increase in
  customer interaction, deployed to 30+ handheld field devices on Firestore.
- Education: Applied Computer Technology, USIU-Africa. Concentration in
  distributed systems; **minor in Japanese**; coursework included embedded
  real-time systems. Speaks English, **Swahili** and Japanese — the Swahili is
  what makes Kamusi his to build rather than a project about someone else's
  language.
- **Telemetri** — Keith's own driver-behaviour/trip telematics build. His
  independent run at what Damoov does commercially.
- **TelematicsApp-Android** — a fork of Damoov's open-source Zenroad app, NOT
  Keith's own work. Never present it as his.
- **Kamusi 2.0** — digitising Swahili definitions into a structured lexicon.
  Motivation: English speakers have a good dictionary in every app store;
  Swahili has no genuinely ubiquitous one.
- **Longtail** — boat simulator built on one mechanic: thrust and steering are
  the same input, so you cannot turn without accelerating. Three prototypes:
  2D top-down, Three.js 3D, multi-engine variant.
- **Reddit fine-tuning** — QLoRA on open-weight models. r/changemyview is the
  useful corpus because the delta system labels which arguments actually moved
  someone.
- Bench work: Fusion 360 and a Bambu Lab A1. Builds robots, and has a soldering
  rework station — so IoT and board-level electronics, not just print-and-
  assemble. Reading about drone and ground-sensor rigs for soil-quality
  surveying.
- The column is 46rem with a 64ch measure, giving 65–71 characters per line.
  That is deliberate and near-optimal; the wide side margins are a *consequence*
  of a correct measure, not a mistake. Do not widen the column to fill them.
- Reads a lot of fantasy. This is why the colophon mentions appendices; it is
  the honest second justification for the lexicon device.

## Open tasks

Source of record for employment history and the Tappi app is
`../baranga_resume_3.07.2026.pdf` (dated 3 July 2026). The same directory holds
Keith's passport, ID and a bank card — **never read or reference those.**

Blocked on Keith — do not invent any of these:

1. Telemetri's `stack` array is inferred. Confirm against the actual repo.
2. The `Rework station` bench entry is paraphrased from chat. Confirm, and get a
   specific robot or IoT build worth naming.
3. **Kamusi case study page.** Highest-value remaining work. Should cover noun
   classes and Bantu morphology in the schema, where the source definitions came
   from, and whether forms are derived or stored. Ask before writing — the
   technical detail must come from Keith.

Unblocked:

7. Deploy is wired: `.github/workflows/deploy.yml` builds on push to `main`,
   Pages source is "GitHub Actions". Live at **https://baranga.works** via a
   custom domain, which is a domain root — so `astro.config.mjs` sets **no**
   `base`. Setting one 404s every asset and drops the page to Georgia/Arial.
8. **Decide whether `opsz` stays.** It is 66KB — 58% of the 112KB roman file —
   and narrowing its range saves almost nothing, so the choice is binary. It is
   the difference between a masthead that looks typeset at 96px and one that
   looks scaled up from body copy. Currently kept. See the note below.

Done 2026-09-10:

- **Astro 5.18.2 → 7.3.2.** No code changes were needed; 0 advisories.
- **Fonts self-hosted**, built by `scripts/build-fonts.py`. Astro's
  `fontProviders.google()` was tried first and rejected: unifont resolves only
  the `wght` axis, which killed `opsz` and silently disabled optical sizing. The
  local provider with explicitly-requested axes is the workaround, and it also
  buys metric-matched fallbacks that cut swap-time layout shift.
- All three latin-ext slices dropped (~84KB that never painted). The italic one
  looked necessary but was not: **Newsreader has no IPA coverage beyond ŋ** —
  ɑ, ː, ˈ and ɡ are not drawn in the typeface at any weight or style. That slice
  bought one glyph and split the pronunciation across two faces. Without it the
  whole IPA string renders coherently from a single system fallback.
- Masthead pronunciation confirmed by Keith on 2026-09-10: **/bɑːˈrɑːŋɡɑ/**.
  Note it deliberately carries no syllable dots; the headword keeps its own.

- Files moved out of the flat `files/` directory into the `src/` tree the docs
  describe; imports resolve; `npm install`, `dev` and `build` all clean.
- Verified Newsreader carries the `opsz` axis (6–72) and that
  `font-optical-sizing: auto` is measurably active — normalized glyph width
  moves from 5.59 at 12px to 5.41 at 96px, and pins flat at 4.86 under `none`.
- 320px: no horizontal overflow, headword clamps to 44px. `--fs-lg` was made
  fluid because the masthead senses at 20.8px pushed sense 3 to eight lines
  before any work was visible.
- Keyboard focus order: 9 stops, DOM order matches visual order, no `tabindex`
  overrides. Skip-link copy changed to match the renamed section.

## Working style

Keith is a senior engineer — skip the explanations of what Astro is. Ask before
inventing biographical or technical detail; several facts above exist because an
earlier draft got them wrong and had to be corrected.
