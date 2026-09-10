#!/usr/bin/env python3
"""
Regenerate the self-hosted font subsets in src/assets/fonts/.

    python3 -m venv .venv && .venv/bin/pip install fonttools brotli
    .venv/bin/python scripts/build-fonts.py

Why this exists rather than `fontProviders.google()`:
Astro's Google provider resolves only the `wght` axis (unifont resolves
`font.axes.find(e => e.property === "wght")`), so Newsreader comes back pinned
at 16pt with no `opsz`. `font-optical-sizing: auto` then silently does nothing.
Requesting the axis explicitly from the css2 API is the only way to keep it.

Three reductions, in order of payoff:
  1. subset  — only the codepoints the site can actually render
  2. wght    — narrowed to the weights the CSS asks for
  3. opsz    — kept variable on the roman (13px body to 96px masthead),
               pinned on the italic, which never renders above ~17px and so
               gains nothing from a second axis it pays full designspace for
"""
import json, pathlib, re, sys, urllib.request
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.subset import Subsetter, Options

OUT = pathlib.Path(__file__).parent.parent / 'src/assets/fonts'
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0 Safari/537.36')
CSS = ('https://fonts.googleapis.com/css2'
       '?family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500'
       '&family=Archivo:wght@400..600&display=swap')

# ASCII, Latin-1, and the punctuation the copy uses (en/em dash, curly quotes, ellipsis)
LATIN = ('0020-007E,00A0-00FF,2013-2014,2018-201A,201C-201E,2026,2032-2033,20AC')
LATIN_CSS = ('U+0020-007E, U+00A0-00FF, U+2013-2014, U+2018-201A, U+201C-201E, '
             'U+2026, U+2032-2033, U+20AC')
# Latin Ext-A for diacritics; IPA Extensions for ɡ (U+0261); spacing modifiers for ˈ (U+02C8)
LATIN_EXT = ('0100-017F,0250-02AF,02B0-02FF')
LATIN_EXT_CSS = 'U+0100-017F, U+0250-02AF, U+02B0-02FF'

def expand(spec):
    out = set()
    for part in spec.split(','):
        if '-' in part:
            a, b = part.split('-'); out.update(range(int(a, 16), int(b, 16) + 1))
        else:
            out.add(int(part, 16))
    return out

# Faces this page can actually render. Every string on the site is ASCII except
# the masthead pronunciation /bɑːˈrɑːŋɡɑ/, so all three latin-ext slices are
# dropped — together they shipped ~84KB that essentially never paints.
#
# The italic latin-ext slice looks like it should stay, but it must not:
# Newsreader has NO IPA coverage beyond ŋ (U+014B) — ɑ, ː, ˈ and ɡ are simply
# not drawn in the typeface, at any weight or style. Shipping that 21.6KB slice
# bought exactly one glyph and forced the other four to a system fallback,
# leaving the pronunciation visibly set in two faces. Dropping it costs the ŋ
# and buys a pronunciation rendered coherently in a single fallback face.
#
# If copy ever needs latin-ext in ordinary text, add the face back here and
# re-run; until then the browser falls back gracefully rather than showing tofu.
SHIP = {
    ('Newsreader', 'normal', 'latin'),
    ('Newsreader', 'italic', 'latin'),
    ('Archivo', 'normal', 'latin'),
}

def fetch_faces():
    req = urllib.request.Request(CSS, headers={'User-Agent': UA})
    css = urllib.request.urlopen(req).read().decode()
    faces = []
    for subset, body in re.findall(r'/\*\s*([\w-]+)\s*\*/\s*@font-face\s*\{(.*?)\}', css, re.S):
        if subset not in ('latin', 'latin-ext'):
            continue
        get = lambda k: (re.search(rf'{k}:\s*([^;]+);', body) or [None, None])[1]
        faces.append(dict(
            family=get('font-family').strip().strip("'\""),
            style=get('font-style').strip(),
            weight=get('font-weight').strip(),
            unicode_range=get('unicode-range').strip(),
            subset=subset,
            url=re.search(r'url\((https://[^)]+\.woff2)\)', body).group(1),
        ))
    return faces

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest, total = [], 0
    for f in fetch_faces():
        if (f['family'], f['style'], f['subset']) not in SHIP:
            print(f"  (skipped {f['family']}-{f['style']}-{f['subset']} — nothing on the page renders it)")
            continue
        name = f"{f['family']}-{f['style']}-{f['subset']}.woff2".replace(' ', '')
        dest = OUT / name
        raw = urllib.request.urlopen(urllib.request.Request(f['url'], headers={'User-Agent': UA})).read()
        tmp = dest.with_suffix('.orig'); tmp.write_bytes(raw)

        font = TTFont(tmp)
        opts = Options(); opts.layout_features = ['*']; opts.drop_tables += ['DSIG']
        sub = Subsetter(options=opts)
        sub.populate(unicodes=expand(LATIN_EXT if f['subset'] == 'latin-ext' else LATIN))
        sub.subset(font)

        # Narrow wght to what the CSS asks for. Pin opsz on the italic; it never
        # renders large enough for the axis to be worth its designspace.
        limits = {'wght': (300, 400, 500)} if f['family'] == 'Newsreader' else {'wght': (400, 500, 600)}
        if f['family'] == 'Newsreader' and f['style'] == 'italic':
            limits['opsz'] = 16
        instancer.instantiateVariableFont(font, limits, inplace=True, updateFontNames=False)

        font.flavor = 'woff2'
        font.save(dest)
        tmp.unlink()

        axes = {a.axisTag: f"{a.minValue:g}..{a.maxValue:g}" for a in TTFont(dest)['fvar'].axes}
        size = dest.stat().st_size; total += size
        manifest.append(dict(file=name, family=f['family'], style=f['style'],
                             weight=f['weight'],
                             unicodeRange=LATIN_EXT_CSS if f['subset'] == 'latin-ext' else LATIN_CSS,
                             subset=f['subset'], bytes=size, axes=axes))
        print(f"  {name:<34} {size:>7}  {axes}")

    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f"\n  total {total} bytes across {len(manifest)} files")
    print(f"  manifest -> {OUT / 'manifest.json'}")

if __name__ == '__main__':
    sys.exit(main())
