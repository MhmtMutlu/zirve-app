# nl · privacy review (2026-11-12)

Reviewed src/privacy.nl.html against privacy.en.html and privacy.tr.html, section by section.
Checks: tags/attributes/ids/hrefs/{{tokens}} identical to en ('<' 540+2, href= 24, '{{' 11, '{' 22; only extra
element is the translation-note <p>, present); numbers and durations identical; legal bases (GDPR Art. 6(1)(a)/(b)/(c)/(f),
KVKK Art. 5) unchanged; game terms match the app nl catalog (etage, edelstenen, Dagtoren, rustmodus, kist, reeksbevriezer,
competitie(frame), porren, Topklimmers, uitleg, Advertentie kijken, Inloggen met Apple, Aankopen herstellen,
Mijn gegevens downloaden, Account verwijderen, Gebruiksstatistieken, Supportcode).
The broken EN sentence in the RevenueCat item ("...from Apple. and processes them...") is rendered as in TR ("RevenueCat verwerkt deze gegevens ...").

Fixes (12):
1. §6 "Minderjarige spelers" (= under 18) narrowed/shifted the age-of-consent condition -> "Spelers onder de leeftijdsgrens"; "leeftijd voor toestemming" -> "leeftijdsgrens voor toestemming" (2x). (legal precision)
2. §5 "gegevens bekendmaken aan bevoegde autoriteiten" (= publicise) -> "verstrekken aan" (GDPR/AVG term for disclose). (legal precision)
3. §1 Purchases: "het land van de winkel" (could read as the in-game Winkel) -> "het App Store-land" (storefront country).
4. §1 Technical: "bevatten ... gedurende maximaal 7 dagen" (unidiomatic) -> "bevatten ... en worden maximaal 7 dagen bewaard".
5. §5 Google: ambiguous "Het gebruikt de IDFA" -> "Google gebruikt de IDFA".
6. §7 Guest account: "(de app maakt nooit verbinding ...)" -> "(waarin de app nooit verbinding maakt ...)".
7. §9 Children: "(of een hogere leeftijd waar je land dat vereist)" -> "(of jonger dan een hogere leeftijd als je land dat vereist)".
8. §4 Top climbers: "op hoogste torenetage" -> "op basis van de hoogste etage in de toren".
9. §1 Profile: "het uiterlijk van de toren en het frame dat je kiest" (choice attached only to frame) -> "het torenuiterlijk en het frame die je kiest".
10. §10: "binnen 30 dagen, kosteloos" -> "kosteloos binnen 30 dagen" (word order).
11. §10: "mail je ons rechtstreeks op" -> "via".
12. Country name "Türkiye" -> "Turkije" (17x, incl. translation note) — standard Dutch (Taalunie) and consistent with terms.nl.html and content/i18n/nl.json.
Translation note present in header; wording kept.

Not changed (uncertain): Dutch iOS wording of the ATT setting quoted in §6 ("Sta apps toe om te vragen je activiteit te volgen") was not verified against iOS nl.
