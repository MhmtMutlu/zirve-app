# pl · privacy review (2026-11-12)

Reviewed src/privacy.pl.html against privacy.en.html and privacy.tr.html, section by section.
Checks: tag sequence identical to en except the translation-note <p> (present, correct wording); counts match
(href=24, {{=11, {=22, ids=9); all numbers/durations (60 d, 7 d, 30 d, 90 d, 12/13/24 months, 1 h, 3 years, 13) and
legal bases (GDPR Art. 6(1)(a)/(b)/(c)/(f), KVKK Art. 5) unchanged; game terms match the app String Catalog
(piętro, klejnoty, Wieża dnia, tryb relaksu, obóz, skrzynia, ochrona serii, ramka ligowa, Szturchnij, Zdobywcy szczytu,
Przywróć zakupy, Pobierz moje dane, Usuń konto, Statystyki użytkowania, Kod wsparcia, Opcje prywatności).
The broken EN RevenueCat sentence ("...from Apple. and processes them...") is rendered as a full sentence, as in TR.

Fixes (6):
1. §6 "Niepełnoletni gracze" (= under 18) shifted the condition; EN is about the age of consent -> "Gracze poniżej wieku zgody". (legal precision)
2. §6 ATT: the quoted iOS prompt name was dropped -> pytanie iOS „Pozwalaj aplikacjom prosić o śledzenie”; "(wcale," -> "(wcale nie,". (omission)
3. §11 "w razie potrzeby" (if needed) softened "where required" -> "gdy jest to wymagane". (obligation)
4. §9 "poniżej 13. roku życia" is ambiguous in Polish (13th year of life = age 12) -> "w wieku poniżej 13 lat". (legal precision)
5. §1 Technical: logs "zawierają ... przez maksymalnie 7 dni" (unidiomatic) -> "przechowują ... maksymalnie przez 7 dni".
6. §7 Guest account: "nigdy nie zostało zalogowane przez Apple" + "(gdy aplikacja w ogóle nie łączy się...)" -> "na którym nigdy nie zalogowano się przez Apple ani nie dokonano zakupu ... (w tym czasie aplikacja ani razu nie łączy się z naszym serwerem)".
