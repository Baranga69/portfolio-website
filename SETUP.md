# Setup

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # outputs to ./dist
```

## Deploying to GitHub Pages

1. Create a repo (e.g. `Baranga69/baranga69.github.io`).
2. Confirm `site` in `astro.config.mjs` matches the final URL. If you deploy to a
   project repo rather than a user page, also set `base: '/repo-name'`.
3. Add `.github/workflows/deploy.yml` using Astro's official Pages action
   (`withastro/action`), then set Pages source to "GitHub Actions".

## Fonts

Self-hosted, not fetched from Google at runtime. The files in
`src/assets/fonts/` are generated — do not hand-edit them:

```bash
python3 -m venv .venv && .venv/bin/pip install fonttools brotli
.venv/bin/python scripts/build-fonts.py
```

Astro's `fontProviders.google()` cannot be used here: it resolves only the
`wght` axis, so Newsreader arrives pinned at 16pt with no `opsz` and
`font-optical-sizing: auto` silently stops working. The script requests the axis
explicitly, subsets to the codepoints the page renders, narrows `wght`, and pins
`opsz` on the italic. Adding copy that needs a glyph outside the shipped subsets
means editing `SHIP` / the unicode ranges in that script and re-running it.

## Structure

```
src/
  layouts/Base.astro       shell, fonts, meta
  components/Entry.astro   one lexicon entry
  pages/index.astro        all content lives here, as data at the top
  styles/global.css        tokens, then layout
```

Content is arrays at the top of `index.astro` — `work` and `bench`. Adding a
project means adding an object, not touching markup.

## Entry fields

- `headword` — the name
- `classifier` — italic gloss in dictionary voice (`n., Android`)
- `href` — optional link on the headword
- `senses` — array of strings, rendered as numbered senses
- `note` — optional italic aside
- `stack` — optional array of technologies
