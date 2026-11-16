#!/usr/bin/env bash
# Per-game screenshots for the game pages, in every site language, from the App Store raw captures
# (../zirve/docs/store/screenshots/raw/<lang>/iphone-6.9/game-<kind>.jpg, 1320×2868, clean UI, 9:41 status bar).
# Writes assets/shots/games/<lang>/<kind>.webp at 603×1311 (the size the site already uses). Run when captures change:
#   ./scripts/game-shots.sh            # every language and game
#   ./scripts/game-shots.sh en arrows  # one language, one game
set -euo pipefail
cd "$(dirname "$0")/.."
raw="${ZIRVE_APP_REPO:-../zirve}/docs/store/screenshots/raw"
langs="${1:-$(ls "$raw")}"
kinds="${2:-colorMatch pathDraw blockFit memory flow pipes colorSort arrows gates flags lights}"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
for lang in $langs; do
  site_lang="$(echo "$lang" | tr '[:upper:]' '[:lower:]')"
  mkdir -p "assets/shots/games/$site_lang"
  for kind in $kinds; do
    src="$raw/$lang/iphone-6.9/game-$kind.jpg"
    [[ -f "$src" ]] || { echo "missing $src" >&2; exit 1; }
    sips --resampleWidth 603 "$src" --out "$tmp/s.png" -s format png >/dev/null
    cwebp -quiet -q 78 -metadata none "$tmp/s.png" -o "assets/shots/games/$site_lang/$kind.webp"
  done
done
du -sh assets/shots/games
