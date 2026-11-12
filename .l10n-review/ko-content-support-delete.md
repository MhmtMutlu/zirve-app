# ko review: content/i18n/ko.json, support.ko.html, delete.ko.html (2026-11-12)

Checked: all en.json keys present in ko.json, state translated, placeholders/markup/{href:...}/numbers match
(extra digits only from Korean date/counter forms: 1월..12월, 2026년 11월 6일, 1분/5초, 3층, 10층, 3장, 2개).
Game, tier, gem, life, floor, daily tower, calm mode, Top climbers, Time assist, share-card strings match the app
String Catalog and docs/l10n/ko/glossary.md. HTML: '<', href=, {{ }}, { } counts and href values identical to .en.html
(delete.ko has +1 <p> = translation note, present; support pages carry no note in any language).

Fixes:
1. delete.ko.html: "추가 확인을 요청할 수 있어요" was ambiguous (reads as "you can request further verification");
   now "저희가 추가 확인을 요청드릴 수 있어요" = "we may ask you to verify further" (EN meaning).
2. delete.ko.html: "서버에" -> "저희 서버에" ("our servers", as in EN).
3. delete.ko.html: "12개월 동안 사용하지 않았을 때" -> "12개월 동안 사용하지 않으면" (condition "after 12 months without use", clearer).
4. support.ko.html: "알려 주면" -> "알려 주시면" (natural polite 해요체 toward the reader).
ko.json: no changes needed.
