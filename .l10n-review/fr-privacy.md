# fr · privacy (src/privacy.fr.html) — independent review, 2026-11-12

Compared section by section with privacy.en.html and privacy.tr.html. Tags, href/id values, {{tokens}} and all numbers
identical to EN (only difference: the required `translation-note` paragraph, present). Glossary: scripts/i18n/fr.json
(no docs/l10n/fr/glossary.md) + App Localizable.xcstrings.

Fixes (6):
1. Retention §7, guest account: "(l'app ne s'étant jamais connectée à notre serveur)" read as "the app never connected
   at all" (a guest account always connected once). Now "(l'app ne s'est connectée à notre serveur à aucun moment pendant
   cette période)" = EN "the app never connecting to our server" during the 12 months / TR "uygulama sunucuya hiç bağlanmazsa".
2-3. Game term: app fr uses "énigme" for puzzle (glossary "puzzle": "énigme"; "Énigmes résolues en mode zen").
   "type de puzzle" -> "type d'énigme" (×2, data table: progress + social).
   "le nombre de puzzles que tu as résolus" -> "le nombre d'énigmes que tu as résolues" (§4 calm list).
4. §9 Children: "jeu de puzzles" -> "jeu d'énigmes".
5. §6 Ads: "Si tu la désactives" (referent "ta décision", unclear) -> "Si tu désactives le suivi" (EN "If you turn it off" = tracking).
6. §10 Rights: "auprès de l'autorité locale" -> "auprès de ton autorité locale" (EN "your local data protection authority").

Checked, no change: all legal bases (GDPR/KVKK refs kept verbatim), every duration (7/30/60/90 days, 1 h, 12/13/24 months,
3 years), RevenueCat sentence (EN source has a broken "Apple. and processes" fragment; FR correctly follows TR:
"RevenueCat traite ces données pour notre compte ..."), game terms (tour du jour, mode zen, gemmes, gel de série, relance,
cadre de ligue, thème de la tour, Au sommet, Réglages paths, Télécharger mes données, Supprimer le compte, Restaurer les achats,
Code d'assistance), iOS path Réglages → Confidentialité et sécurité → Suivi.
