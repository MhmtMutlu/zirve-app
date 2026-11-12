# id review: content + support + delete (2026-11-12)

Checked: every key of en.json present in id.json, all `.state` = translated; `{placeholders}`, `{href:...}`, markup and numbers identical to en.json. support/delete: tag, href, class, hreflang, `{{...}}` and number counts identical to .en.html (delete.id.html has 2 extra `<` = the required translation-note paragraph; support pages carry none in any language). Game terms, tier and game names checked against the app String Catalog (id) and docs/l10n/id/glossary.md. No meaning, number, duration, retention period or legal statement changed. `build.check_strings`: id ready.

## Fixes (7)
content/i18n/id.json
1. home.lead: "lewati teman-temanmu" -> "salip teman-temanmu" ("pass" = overtake in the league; app uses "menyalip", push.passed / friends.passed).
2. home.features[2] friends text: "saat kamu melewati mereka" -> "saat kamu menyalip mereka" (same app term).
src/support.id.html
3. Notifications answer: "mencolekmu atau melewatimu" -> "mencolekmu atau menyalipmu" (app push "%@ baru saja menyalipmu!").
src/delete.id.html
4. RevenueCat: "menghapus catatan pelanggannya" -> "menghapus catatan pelangganmu di sistemnya" (old wording could read as RevenueCat deleting its customer records in general; source = the player's own customer record). Most serious.
5. "(tidak dapat dikembalikan)" -> "(dananya tidak dapat dikembalikan)" (source "not refundable"; old text read as "cannot be returned/restored").
6. Retention note: "dengan tautan ke akunmu dihapus" -> "dengan tautannya ke akunmu diputus" (clearer: link removed, not data deleted at that point; avoids clash with the following "lalu dihapus").
7. "Tanda terima tokomu" -> "Tanda terima pembelianmu dari toko" ("tokomu" read as "your store").

Not changed (noted): the translation note in delete.id.html is identical to one other id legal page; the third uses slightly different wording ("yang kami sediakan ... yang berlaku adalah"), same meaning; left as is (other files are out of scope).
