# de · privacy review (2026-11-12)

Reviewed src/privacy.de.html against privacy.en.html and privacy.tr.html, section by section.
Checks: tags/attributes/ids/hrefs/{{tokens}} identical to en (only extra element: translation-note <p>, present);
numbers and durations identical; legal bases (GDPR Art. 6(1)(a)/(b)/(c)/(f), KVKK Art. 5) unchanged;
game terms match the app (Etage, Juwelen, Tagesturm, Ruhemodus, Lager, Truhe, Serienschutz, Turmthema, Rahmen,
Anstupsen, Gipfelstürmer, Käufe wiederherstellen, Meine Daten herunterladen, Konto löschen, Nutzungsstatistiken).
The broken EN sentence in the RevenueCat item ("...from Apple. and processes them...") is correctly rendered as in TR.

Fixes (11):
1. §10 requests: "Dort kannst du auch dein Konto löschen..." implied deletion/name change only under Konto; EN says "in the app" -> "In der App kannst du außerdem ...". (meaning)
2. §10 complaint: KVKK "Board" (Kurul) was rendered as "Behörde" (authority) -> "Rat für den Schutz personenbezogener Daten (Kişisel Verileri Koruma Kurulu)". (legal precision)
3. §6 "Minderjährige Spieler" (= under 18) narrowed/shifted the age-of-consent condition -> "Spieler unter dem Einwilligungsalter". (legal precision)
4. §1 Support emails: "ein beigefügter Support-Code" lost "any" (optional) -> "ein gegebenenfalls mitgeschickter Support-Code".
5. §1 Technical: "enthalten ... für höchstens 7 Tage" (unidiomatic) -> "speichern ... höchstens 7 Tage lang".
6. §1 Profile: agreement error "das von dir gewählte Outfit, Turmthema und der Rahmen" -> "das Outfit, das Turmthema und der Rahmen, die du wählst".
7. §5 Google: ambiguous "Es nutzt die IDFA" -> "Google nutzt die IDFA".
8. §7 Retention: "(die App verbindet sich nie ...)" -> "(in denen sich die App nie ... verbindet)".
9. §9 Children: "Daten gegeben hat" -> "Daten übermittelt hat".
10. §10: "innerhalb von 30 Tagen, kostenlos" -> "kostenlos innerhalb von 30 Tagen" (word order).
11. Translation note: "zur Erleichterung" (unnatural) -> "der Einfachheit halber".
