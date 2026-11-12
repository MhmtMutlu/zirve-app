# nl review: content + support + delete (independent reviewer, 2026-11-12)

Checks: 480/480 keys in nl.json vs en.json, same placeholders/markup/numbers in every value; support.nl.html and
delete.nl.html have the same tag sequence, href, hreflang, {{ }} tokens as .en.html (delete adds the required
translation-note paragraph, present; support has none, as in en/de). `python3 build.py`: all checks passed.

## Fixes (9)
1. delete: "Je aankoopbewijzen van de winkel" → "Je App Store-aankoopbewijzen" (en "store receipts"; "winkel" read as
   the in-game Winkel/Store screen, i.e. the wrong place).
2. delete: "valsspeelmeldingen" → "markeringen voor valsspelen" (en "cheat flags"; "meldingen" reads as
   reports/notifications, a different data category).
3. delete: "accounts waarmee is ingelogd met Apple" → "accounts waarbij je met Apple bent ingelogd" (ungrammatical).
4. delete: "rustlijst" → "rustmoduslijst" (app term is "rustmodus"; "rustlijst" is not used in the app).
5. support: "App Store-bon" → "App Store-aankoopbewijs" (consistent with delete page; Apple receipt wording).
6. support: "tik ... op Aankopen herstellen en sluit de app en open hem opnieuw" → "..., sluit de app daarna af en
   open hem opnieuw" (keeps en "then", removes double "en").
7. nl.json home.values: "Alleen advertenties als jij dat kiest" → "Advertenties alleen als jij dat kiest" (old order
   could read as "only ads").
8. nl.json definition: "korte puzzel op tijd" → "korte puzzel met tijdslimiet" (natural Dutch for "timed puzzle").
9. nl.json daily.lead: "zodat niemand de verrassing wordt ontnomen" → "zodat je de verrassing voor niemand verpest"
   (stiff construction; same meaning as "nobody's surprise is spoiled").

## Left as is / notes
- support links point to {{R}}en/delete-account/ and {{R}}en/privacy/, same as en and de/fr sources (not changed).
- "seizoenspremium" (en "season premium") kept; app uses "Premiumseizoen"/"premiumpad"; meaning is clear.
