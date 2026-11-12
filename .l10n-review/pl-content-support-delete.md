# pl review: content + support + delete

Reviewer pass (independent). Checked every key of `content/i18n/pl.json` against `en.json` (no missing/extra keys; `{…}`, `{{…}}`, tags and `href=` identical per key), and `src/support.pl.html`, `src/delete.pl.html` against their `.en.html` (tag sequence identical except the translation note; `<` / `href=` / `{{` / `{` counts match). `python3 build.py`: all checks passed (2 pre-existing first-view budget warnings for tr/en index).

## Fixes (7)

1. `delete.pl.html` – retention note: "przechowywane maksymalnie 12 miesięcy … po usunięciu powiązania z twoim kontem" could read as "kept for 12/24 months after the link is removed" (retention clock tied to unlinking) and only clearly attached to purchase events. Now "przechowywane bez powiązania z twoim kontem maksymalnie 12 miesięcy, a zdarzenia zakupu maksymalnie 24 miesiące" – matches EN: both kept with the link removed, max 12 / 24 months.
2. `delete.pl.html` – translation note moved from `<article>` into `<header class="doc-head">`, as in pl privacy/terms and most other languages' delete pages (text unchanged).
3. `delete.pl.html` – "To have it deleted sooner": "Aby usunąć je wcześniej" (you delete it) → "Jeśli chcesz, aby zostało usunięte wcześniej" (we delete it on request).
4. `delete.pl.html` – "friendships": "znajomości" → "relacje ze znajomymi" (clearer data category).
5. `delete.pl.html` – "Game Center records stay with Apple": "pozostają w Apple" → "pozostają u Apple".
6. `support.pl.html` – heading "Odblokowano premium sezonu…" (impersonal "was unlocked", not the user's voice) → "Mam premium sezonu, ale nagrody są zablokowane" (gender-neutral first person); "numer zamówienia" → "identyfikator zamówienia (Order ID)" as on Apple receipts.
7. `pl.json` `home.features[3][4]` – "10 czystych pięter" → "10 bezbłędnych pięter", matching the app term (`chest.subtitle`: "Nagroda za 10 bezbłędnych pięter").

## Checked, no change
- Game names, tier names, Wieża dnia, Pomoc z czasem, Przywróć zakupy, Zaloguj się przez Apple, Kod wsparcia, Zdobywcy szczytu, klejnoty/życia/piętra/obóz match the app catalog.
- Plural agreement with facts values: 11 łamigłówek, 10 pięter, 3 próby, 30 graczy, 16 krain, 6/17 języków, 7 najlepszych / 5 ostatnich.
- All numbers/durations in delete (30 days, 12/24 months, 12 months inactivity, 30 days) and support (2 business days) unchanged.
- `home.score` "Piętra: {n}" kept (label form avoids plural inflection in a narrow table cell).
