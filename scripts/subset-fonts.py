#!/usr/bin/env python3
"""Cuts the self-hosted web fonts into per-script subsets (plan §7.3) and prints the fallback metrics for site.css.

Needs fontTools + brotli (not a dependency of build.py; run only when the source fonts change):
    python3 -m venv .venv && .venv/bin/pip install fonttools brotli
    .venv/bin/python scripts/subset-fonts.py

Sources: assets-src/fonts/{Fredoka,Nunito}.woff2 (variable, SIL OFL; the same faces as the app).
Output:  assets/fonts/<family>-<subset>.woff2. A subset is skipped when the source font has no glyph in its range
         (Fredoka and Nunito ship here without Cyrillic and Vietnamese; those languages fall back to system fonts
         until the full families are added to assets-src/fonts/).
The `wdth` axis of Fredoka is pinned to 100 (the site never uses it); the `wght` range is kept.
The unicode ranges must match the @font-face blocks in assets/site.css (build.py checks the file names).
"""
import pathlib, sys
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets-src" / "fonts"
OUT = ROOT / "assets" / "fonts"

# Google Fonts' ranges (same split the CSS uses).
RANGES = {
    "latin": "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,"
             "U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD",
    "latinext": "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,"
                "U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF",
    "cyrillic": "U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116",
    "vietnamese": "U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,"
                  "U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB",
}
FAMILIES = {"Fredoka": "fredoka", "Nunito": "nunito"}
MIN_GLYPHS = 40


def codepoints(spec):
    out = set()
    for part in spec.split(","):
        a, _, b = part.strip()[2:].partition("-")
        out.update(range(int(a, 16), int(b or a, 16) + 1))
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for family, slug in FAMILIES.items():
        font = TTFont(SRC / f"{family}.woff2")
        if "fvar" in font and any(a.axisTag == "wdth" for a in font["fvar"].axes):
            font = instancer.instantiateVariableFont(font, {"wdth": 100})
        cmap = set(font.getBestCmap())
        for name, spec in RANGES.items():
            # A subset with only a handful of glyphs would not cover its script (Fredoka has 11 Latin Extended
            # glyphs and no ş/ğ); the browser then uses the next font in the stack for those characters.
            wanted = codepoints(spec)
            if len(wanted & cmap) < MIN_GLYPHS:
                print(f"skip {slug}-{name}: {len(wanted & cmap)} glyphs in range")
                continue
            target = OUT / f"{slug}-{name}.woff2"
            options = subset.Options()
            options.flavor = "woff2"
            options.layout_features = ["*"]
            options.name_IDs = ["*"]
            options.notdef_outline = True
            sub = subset.Subsetter(options)
            sub.populate(unicodes=wanted & cmap)
            work = copy_font(font)
            sub.subset(work)
            work.flavor = "woff2"
            work.save(target)
            print(f"{target.relative_to(ROOT)}  {target.stat().st_size // 1024} KB  {len(wanted & cmap)} code points")
    print_fallback_metrics()


def copy_font(font):
    import io
    buf = io.BytesIO()
    font.save(buf)
    buf.seek(0)
    return TTFont(buf)


def print_fallback_metrics():
    """size-adjust / ascent-override for a local Arial fallback so the swap to the web font barely moves text."""
    arial = pathlib.Path("/System/Library/Fonts/Supplemental/Arial.ttf")
    if not arial.exists():
        print("Arial not found; fallback metrics not printed")
        return
    sample = "the quick brown fox jumps over a lazy dog zirve kule bulmaca etage puzzle"

    def avg_width(font):
        cmap, hmtx, upm = font.getBestCmap(), font["hmtx"], font["head"].unitsPerEm
        return sum(hmtx[cmap[ord(c)]][0] for c in sample) / len(sample) / upm

    ref = TTFont(arial)
    for family in FAMILIES:
        font = TTFont(SRC / f"{family}.woff2")
        if "fvar" in font:
            font = instancer.instantiateVariableFont(font, {a.axisTag: a.defaultValue for a in font["fvar"].axes})
        ratio = avg_width(font) / avg_width(ref)
        hhea, upm = font["hhea"], font["head"].unitsPerEm
        print(f"{family} fallback: size-adjust {ratio * 100:.1f}%; ascent-override {hhea.ascent / upm / ratio * 100:.1f}%; "
              f"descent-override {abs(hhea.descent) / upm / ratio * 100:.1f}%; line-gap-override {hhea.lineGap / upm / ratio * 100:.1f}%")


if __name__ == "__main__":
    sys.exit(main())
