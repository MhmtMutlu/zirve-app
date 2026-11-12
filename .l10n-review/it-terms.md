# it · terms (review 2026-11-12)

File: `src/terms.it.html` vs `terms.en.html` / `terms.tr.html`. Structure checked: `<` 456 (EN 454 + translation note), `href=` 31, `{{` 19, `{` 38, `id=` 18; hrefs, ids, tokens and all numbers identical to EN; tags balanced. Translation note present. Game terms checked against the app catalog and `scripts/i18n/it.json` glossary (gemme, vite, piani, forzieri, torre del giorno, modalità relax, aiuto tempo, In vetta, Scalatore, percorso premium, set stagionale, pacchetto iniziale, temi della torre, salvaserie, Ripristina acquisti, Accetto, iniziamo, Giocatori bloccati, Scarica i miei dati, Elimina account, codice di assistenza).

Fixes (12 changes in 9 points):
1. 17.2 "questa versione inglese è una traduzione" -> "la versione inglese è una traduzione" (the Italian page claimed to be the English version; EN/TR: the English version is the translation, Turkish prevails).
2. 5.6 "(l'app non si collega mai al nostro server)" -> "(senza che l'app si colleghi mai al nostro server)" (read as a general factual claim that the app never connects; EN: inactivity condition).
3. 5.2 + 13.4 "ripristini il dispositivo" / "ripristino del dispositivo" -> "inizializzi" / "inizializzazione" (device reset; "ripristinare" is also used in the same sentence for restoring progress, opposite meaning) — 2 places.
4. 3.1 "adatto a giocatori di qualsiasi età" -> "a cui può giocare chiunque, a qualsiasi età" (EN "can play" / TR "oynayabileceği"; "adatto" added a suitability claim).
5. 14.1 "sono tra te e noi, non con Apple" -> "sono conclusi tra te e noi, non con Apple" (ungrammatical, party position unclear).
6. 9.2 "respinto ingiustamente" -> "respinto per errore" (EN "wrongly").
7. "Türkiye" -> "Turchia" (1.1, 7.5, 16.2, 18, translation note; 5 places) for consistency with privacy/delete/content it and natural Italian. "Türkçe" link label unchanged.
8. Translation note moved inside `<header class="doc-head">` like every other locale, wording aligned with `privacy.it.html` ("prevale").
9. Summary "diritti di usarli nel Gioco" -> "diritti di utilizzo nel Gioco" (natural phrasing).

Not changed (noted): `privacy.it.html` also places the translation note outside the header; not part of this task.
