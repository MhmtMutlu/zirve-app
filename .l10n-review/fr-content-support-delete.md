# fr review: content + support + delete (2026-11-12)

Checks: fr.json has all 480 keys of en.json, all state=translated, placeholders/markup/numbers identical per key;
support/delete tag, href, {{ and { counts match en (delete.fr has +1 <p> = translation note, present in header).
Game terms checked against App/Resources/Localizable.xcstrings (fr).

Fixes (8):
1. delete.fr: retention sentence said "en supprimant leur lien avec ton compte" (ambiguous: reads as the removal being the
   retention method) -> "…24 mois, sans lien avec ton compte, puis supprimés ou anonymisés" (EN: kept with the link to
   the account removed).
2. delete.fr: "nous la traitons sous 30 jours" (process/handle, weaker) -> "nous la finalisons sous 30 jours" (EN: complete).
3. delete.fr: "Tes données Game Center" (broader than EN) -> "Tes enregistrements Game Center" (EN: records).
4. delete.fr: "Si tu utilises Se connecter avec Apple" -> "Si ton compte est connecté avec Apple" (EN: if you signed in with Apple).
5. delete.fr: "liste zen" -> "liste du mode zen" (app: Mode zen).
6. support.fr: "Si elles manquent" -> "Si elles n'apparaissent pas" (natural phrasing).
7. fr.json home.league_p: "montent/descendent d'un niveau" -> "d'une ligue" (EN: tier; "niveau" is the app's season level term).
8. fr.json daily.card_time: "3:05 de temps total" -> "3:05 au total" (app daily.totalTime: "%@ au total").

Not changed: support pages carry no translation note in any language (consistent with other locales); support links to
{{R}}en/... kept as in every other locale (href values are frozen).
