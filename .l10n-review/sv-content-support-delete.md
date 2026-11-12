# sv review: content + support + delete (2026-11-12)

Checked: every key of en.json present in sv.json, all `.state` = translated; placeholders, `{href:...}`, markup and numbers identical. support/delete: tag, href, `{{...}}`, `{` and number counts identical to .en.html (delete.sv.html has 2 extra `<` from the translation-note paragraph, which is present; support pages carry none in any locale). No meaning, number, duration, retention period or legal statement changed. `build.check_strings`: sv ready.

## Fixes (12)
src/delete.sv.html
1. Retention note: "Raderingen ... sker omedelbart; den försvinner ur de krypterade säkerhetskopiorna" -> "uppgifterna försvinner ur ..." ("den" grammatically referred to the deletion itself, not the data; now matches privacy.sv / de / nl).
2. "inventarie" -> "förråd" (inventarie = a fixture/piece of furniture; privacy.sv uses "förråd" for the same data category).
3. "fuskmarkeringar" -> "fuskflaggor" (same data category as privacy.sv).
4. "Dina kvitton från butiken" -> "Dina köpkvitton" ("butiken" reads as the in-game Butik; receipts are Apple's, sentence already says Apple-konto).
src/support.sv.html
5. h3 "Ädelstenar som jag köpt har inte kommit" -> "Ädelstenarna jag köpte har inte kommit fram" (natural phrasing).
6-7. "på Butik-skärmen" (2x) -> "i Butik" (unnatural hyphen compound; terms.sv uses "i Butik").
content/i18n/sv.json
8-9. home.games[10].how[0..1] Lights: "växlar" -> "vänds" (app lights.a11y.hint "Vänder den här rutan ...").
10. daily.card_time: "3:05 total tid" -> "3:05 totalt" (app daily.totalTime "%@ totalt" on the same card).
11. daily.note: "banderollen" -> "bannern" (banderoll is a physical banner; Smart App Banner is "bannern").
12. daily.legend[0] label: "I 3-stjärnetempo" -> "I 3-stjärnigt tempo" (non-standard compound).

Not changed (noted): translation-note wording differs slightly between sv legal pages ("som tillhandahålls" in delete/terms vs "som vi tillhandahåller" in privacy; terms.sv says "Türkiye", privacy/delete "Turkiet"); outside this part, left for the privacy/terms reviewers. daily.legend[2] "Med fortsättning" is acceptable but slightly literal.
