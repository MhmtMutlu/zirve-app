# sv · terms (review 2026-11-12)

File: `src/terms.sv.html` vs `terms.en.html` / `terms.tr.html`. Structure checked after edits: `<` 456 (EN 454 + translation note), `href=` 31 (identical list), `{{` 19, `{` 38, `id=` 18, all numbers identical in order. Translation note present. Game terms checked against app catalog / `docs/l10n/sv/glossary.md` (ädelstenar, liv, våning, Dagens torn, lugnt läge, tidshjälp, Toppklättrare, Klättrare, premiumspår, säsongsset, Startpaket, tornteman, Återställ köp, Se reklam, Integritetsval, ”Jag godkänner, nu kör vi”).

Fixes (16 changes in 14 points):
1. 9.2 "under en period på 5 timmar" -> "under valfri period på 5 timmar" (EN "in any 5 hours": rolling window, not one fixed block).
2. 7.5 EU bullet "ditt medgivande om att du förlorar rätten" -> "din bekräftelse av att du förlorar rätten" (EN "acknowledgement"; "medgivande" reads as a second consent).
3. 5.6 "(appen ansluter aldrig till vår server)" -> "(det vill säga utan att appen har anslutit till vår server)" (read as a general claim that the app never connects; EN defines "without any use").
4. 11.1 "upp en nivå" -> "upp en liga" (glossary: "nivå" is reserved for season level).
5. 11.1 word order: unclaimed season rewards "ges ... automatiskt" was ambiguous (could read "not collected automatically") -> "får du automatiskt de belöningar som du har nått men inte samlat in".
6. 14.1 "gäller mellan dig och oss, inte Apple" -> "ingås mellan dig och oss, inte med Apple" (party wording).
7. "Türkiye" -> "Turkiet" (5x: note, 1.1, 7.5, 16.2, 18) for natural Swedish and consistency with `privacy.sv.html`; link label "Türkçe" unchanged.
8. "torntema" -> "tornteman" in plural lists (summary, 6.1, 6.3), matching app ("tornteman").
9. 3.2 "Be om köp" -> "Be om att köpa" (Apple's Swedish name for Ask to Buy; believed correct, worth a spot check on a Swedish iOS device).
10. 8.2 "integritetsalternativ" -> "integritetsval" (app label settings.adPrivacy).
11. 8.3 "en olämplig reklam" -> "en olämplig annons" (reklam is a mass noun).
12. 5.2 "loggar in med Apple till ett konto" -> "på ett konto".
13. 6.5 "ändra dess balans" -> "ändra spelbalansen".
14. 9.1 colloquial "den sparade datan" -> "sparade data".

Not changed: 17.2 kept as in all other languages (says "the English version is a translation"), consistent with the template.
