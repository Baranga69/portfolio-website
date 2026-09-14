import { defineConfig, fontProviders } from 'astro/config';

export default defineConfig({
  /* Served from the project path https://baranga69.github.io/portfolio-website/,
     so `base` MUST match the repo name — without it every asset resolves against
     the domain root and 404s, and the page silently drops to Georgia and Arial.
     Remove `base` (and point `site` at the domain) only if a custom domain is
     put in front, since that serves from a root instead. */
  site: 'https://baranga69.github.io',
  base: '/portfolio-website',
  compressHTML: true,
  build: {
    inlineStylesheets: 'always',
  },

  /* Self-hosted, and deliberately NOT `fontProviders.google()`.

     Astro's Google provider resolves only the `wght` axis, so Newsreader comes
     back pinned at 16pt with no `opsz` and `font-optical-sizing: auto` silently
     stops doing anything. These files come from `scripts/build-fonts.py`, which
     requests the axis explicitly, subsets to the codepoints this page renders,
     narrows `wght` to the weights the CSS asks for, and pins `opsz` on the
     italic — which never renders large enough to earn a second axis.

     Newsreader has no IPA coverage beyond ŋ, so the masthead pronunciation
     /bɑːˈrɑːŋɡɑ/ renders from a system fallback by design — shipping the
     latin-ext slice bought one glyph and split the string across two faces.

     Every face here is preloaded because every face is used above the fold.
     Regenerate with:  .venv/bin/python scripts/build-fonts.py
     Do not hand-edit src/assets/fonts/. */
  fonts: [
    {
      name: 'Newsreader',
      cssVariable: '--font-newsreader',
      provider: fontProviders.local(),
      fallbacks: ['Georgia', 'Times New Roman', 'serif'],
      options: {
        variants: [
        {
          src: ['./src/assets/fonts/Newsreader-normal-latin.woff2'],
          weight: '300 600',
          style: 'normal',
          unicodeRange: ['U+0020-007E', 'U+00A0-00FF', 'U+2013-2014', 'U+2018-201A', 'U+201C-201E', 'U+2026', 'U+2032-2033', 'U+20AC'],
        },
        {
          src: ['./src/assets/fonts/Newsreader-italic-latin.woff2'],
          weight: '300 500',
          style: 'italic',
          unicodeRange: ['U+0020-007E', 'U+00A0-00FF', 'U+2013-2014', 'U+2018-201A', 'U+201C-201E', 'U+2026', 'U+2032-2033', 'U+20AC'],
        },
        ],
      },
    },
    {
      name: 'Archivo',
      cssVariable: '--font-archivo',
      provider: fontProviders.local(),
      fallbacks: ['system-ui', 'sans-serif'],
      options: {
        variants: [
        {
          src: ['./src/assets/fonts/Archivo-normal-latin.woff2'],
          weight: '400 600',
          style: 'normal',
          unicodeRange: ['U+0020-007E', 'U+00A0-00FF', 'U+2013-2014', 'U+2018-201A', 'U+201C-201E', 'U+2026', 'U+2032-2033', 'U+20AC'],
        },
        ],
      },
    },
  ],
});
