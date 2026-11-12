# it review: content + support + delete (2026-11-12)

Checked: every key of en.json present in it.json, all `.state` = translated; `{placeholders}`, `{href:...}`, markup and numbers identical (script comparison). Game names, tier names (design catalog), Torre del giorno, Aiuto tempo, Sali, forziere stellare, 10 piani puliti, salvaserie, In vetta, modalità relax, Ripristina acquisti, Codice di assistenza match the app String Catalog. support/delete: tag, href, `{{...}}`, `{` and number counts identical to .en.html; delete.it.html has the translation-note paragraph (+1 `<p>`, the only difference); support pages carry none in any locale. No meaning, number, duration, retention period or legal statement changed. `build.check_strings`: it ready.

## Fixes (9)
content/i18n/it.json
1. home.faq_html[0] (in-app purchases): "il percorso premi premium della stagione" -> "il percorso premium della stagione" (app term `season.premium.body` "percorso premium"; doubled "premi premium").
2. daily.legend[2] title: "Con un continua" -> "Con ripresa" (ungrammatical; app `fail.ad.subtitle` "Riprendi da dove eri").
3. home.steps[1]: "Se ti manca un soffio" -> "Se non ce la fai per un soffio" ("miss it by a hair"; app `fail.title` "Per un soffio!").
4. home.values_eyebrow: "Calmo e leale" -> "Calmo e corretto" ("leale" describes people, not a fair game).
5. home.values[0].p: "vengono risolte mentre sono generate" -> "vengono risolte già in fase di generazione" (unnatural).
6. home.values[4].h: "Pubblicità solo se la scegli" -> "Pubblicità solo se lo scegli tu" (ads only when *you* choose).
7. daily.steps[0]: "tocca la scheda Torre del giorno" -> "tocca il riquadro Torre del giorno" ("scheda" is the word used for app tabs, e.g. "scheda Profilo"; this is a card).
src/delete.it.html
8. Note paragraph: "i dati escono dai backup crittografati entro 30 giorni" -> "entro 30 giorni i dati vengono rimossi anche dai backup crittografati" (unnatural; same meaning and duration).
9. Manual deletion: "al tuo piano record approssimativo" -> "e, all'incirca, al tuo piano record" ("roughly your record floor"; "approssimativo" read as the record being approximate).

src/support.it.html: no changes needed.
