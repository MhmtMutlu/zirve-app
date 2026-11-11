#!/usr/bin/env bash
# Hero image variants for <picture> (plan §7.3): AVIF and WebP at 320 and 603 px wide from assets/shots/<name>.webp.
# macOS only (sips writes AVIF; dwebp/cwebp from Homebrew `webp`). Run when a hero screenshot changes:
#   ./scripts/images.sh tower-forest
set -euo pipefail
cd "$(dirname "$0")/.."
name="${1:-tower-forest}"
src="assets/shots/$name.webp"
[[ -f "$src" ]] || { echo "missing $src" >&2; exit 1; }
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
dwebp -quiet "$src" -o "$tmp/full.png"
width="$(sips -g pixelWidth "$tmp/full.png" | awk '/pixelWidth/ {print $2}')"
cp "$tmp/full.png" "$tmp/320.png"
sips --resampleWidth 320 "$tmp/320.png" >/dev/null
cwebp -quiet -q 82 "$tmp/320.png" -o "assets/shots/$name-320.webp"
sips -s format avif -s formatOptions 45 "$tmp/full.png" --out "assets/shots/$name.avif" >/dev/null
sips -s format avif -s formatOptions 45 "$tmp/320.png" --out "assets/shots/$name-320.avif" >/dev/null
ls -l "assets/shots/$name"* | awk '{print $5, $9}'
echo "source width: $width"
