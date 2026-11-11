#!/usr/bin/env bash
# Re-downloads Apple's official "Download on the App Store" badges (black, SVG) from Apple Marketing Tools into
# assets/badges/app-store-<locale>.svg. Apple serves the US English badge for locales without their own artwork
# (on 12 Nov 2026: uk-ua and hi-in); build.py maps those languages to en-us (LANGS → badge).
# Guidelines: https://developer.apple.com/app-store/marketing/guidelines/ (do not modify, min. 40 px high, clear space).
set -euo pipefail
cd "$(dirname "$0")/.."
for l in en-us tr-tr de-de fr-fr it-it es-es ja-jp ko-kr zh-tw zh-cn nl-nl pl-pl sv-se th-th id-id ru-ru pt-br vi-vn; do
  curl -fsS -o "assets/badges/app-store-$l.svg" \
    "https://toolbox.marketingtools.apple.com/api/badges/download-on-the-app-store/black/$l?size=250x83"
  printf '%s %s\n' "$l" "$(grep -o '<title>[^<]*' "assets/badges/app-store-$l.svg" | head -1 | cut -c8-)"
done
