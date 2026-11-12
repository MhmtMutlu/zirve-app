# it · privacy review (2026-11-12)

Reviewed src/privacy.it.html against privacy.en.html and privacy.tr.html, section by section.
Checks: tags/attributes/ids/hrefs/{{tokens}} identical to en (only extra element: translation-note <p>, present);
counts '<' 540+2, 'href=' 24, '{{' 11, '{' 22; all numbers/durations identical; legal bases (GDPR Art. 6(1)(a)/(b)/(c)/(f),
KVKK Art. 5) unchanged; game terms match the app String Catalog (piano, gemme, torre del giorno, modalità relax, campo,
forziere, salvaserie, costume, tema della torre, cornice, codice invito, punzecchiata, In vetta, Guarda la pubblicità,
Ripristina acquisti, Scarica i miei dati, Elimina account, Codice di assistenza, Statistiche di utilizzo).
The broken EN sentence in the RevenueCat item ("...from Apple. and processes them...") is rendered as in TR (correct).

Fixes (10):
1. §7 Retention: "(l'app non si collega mai al nostro server)" read as a general fact ("the app never connects") instead of
   the condition of the 12-month period -> "(senza che l'app si colleghi mai al nostro server)". (meaning)
2. §6 Under-age players: ungrammatical "hai meno dell'età del consenso" -> "sei al di sotto dell'età del consenso".
3. §6 ATT: "(per niente se hai rifiutato ...)" -> "(e non viene mostrata affatto se hai rifiutato ...)"; "dopo di che" -> "dopodiché".
4. §10 Complaint: KVKK "Board" (Kurul) rendered as "Comitato" (committee) -> "Consiglio per la protezione dei dati personali". (legal precision)
5. §5 Transfers: "rapporto diretto" added "direct" to EN "your own relationship" -> "rapporto personale".
6. §1 Technical: "contengono ... per al massimo 7 giorni" (unidiomatic with a duration) -> "conservano ...".
7. §3 Statistics: "Capiamo la tua area ... se non è possibile capirlo" (colloquial, agreement) -> "Determiniamo ... determinarla".
8. §9 Children: "un gioco ... che chiunque può giocare" -> "a cui chiunque può giocare" (grammar).
9. §7 Retention: elliptical "e i tuoi record di Game Center presso Apple" -> "..., e i tuoi record di Game Center restano presso Apple".
10. §2 Statistics purpose: "prezzi oppure offerte" -> "risultati di lega, prezzi o offerte" (natural list).

Not changed (flag for the owner): links to Terms/Delete account point to {{R}}en/... as in de/fr although terms.it.html and
delete.it.html exist (href values are out of scope for translation review). EN/TR RevenueCat item mentions RevenueCat's
published "data processing addendum"; translated faithfully, worth a legal-owner check against the no-agreements rule.
