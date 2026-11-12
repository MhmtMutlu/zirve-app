# sv · privacy review (2026-11-12)

Reviewed src/privacy.sv.html against privacy.en.html and privacy.tr.html, section by section.
Checks: tags/attributes/ids/hrefs/{{tokens}} identical to en (only extra element: translation-note <p>, present);
counts '<' 540+2 (note), href= 24, '{{' 11, '{' 22; number sequence identical to en; legal bases (GDPR Art. 6(1)(a)/(b)/(c)/(f),
KVKK Art. 5) unchanged; game terms match the app sv catalog (våning, ädelstenar, Dagens torn, lugnt läge, läger, kista,
svitskydd, torntema, ram, puff/puffa, gick om dig, Toppklättrare, Återställ köp, Ladda ned mina data, Radera konto,
Användningsstatistik, Integritetsval, Se reklam, Dela / Dela inte, Supportkod).
The broken EN sentence in the RevenueCat item is correctly rendered as in TR.

Fixes (15; item 6 covers 4 occurrences):
1. §1 Ads row: ", som behandlas av Google AdMob" attached only to the IDFA; EN says AdMob processes all listed data ->
   "När du väljer att se en reklamfilm med belöning behandlar Google AdMob enhets- och appinformation, ...". (meaning/scope)
2. §6 "Minderåriga spelare" (= under 18) shifted the age-of-consent condition -> "Spelare under åldersgränsen". (legal precision)
3. §10 complaint body left in English ("Personal Data Protection Board") -> "Kişisel Verileri Koruma Kurulu (Turkiets nämnd för skydd av personuppgifter)".
4. §1 Social + §2 notifications: "gick/går förbi dig" -> "gick/går om dig" (app: friends.passed / push.passed "gick om dig"). (game term)
5. §6 ATT: "visas iOS fråga om att ”Tillåt appar att begära spårning”" (ungrammatical) -> "visar iOS frågan ”Tillåt appar att begära spårning”".
6. Summary/§1/§2: genitive "iOS spårningsbehörighet" (4x: 3 "i iOS ..." + 1 "efter iOS ...") -> "iOS:s spårningsbehörighet".
7. §1 Technical: "loggar ... innehåller ... i högst 7 dagar" -> "sparar ... i högst 7 dagar".
8. §1 Economy "När": "När du tjänar och använder" (no object) -> "När du tjänar in och använder dem".
9. §1 Notifications: "Token sparas" -> "Tokenen sparas" (definite form).
10. §2 purchases: "tillgodoräkna ädelstenar och premium" (wrong sense: credit oneself) -> "lägga till ädelstenar och premium på ditt konto".
11. §5 Email: "leverantör av e-postvidarebefordran" (= forwarding) -> "leverantör av e-postrelä (mail relay)".
12. §7 guest account: "(appen ansluter aldrig till vår server)" read as a separate claim -> "(det vill säga att appen aldrig ansluter till vår server)".
13. §9 Children: "har gett oss personuppgifter" -> "har lämnat personuppgifter till oss".
14. §10 requests: "bifogar den supportkod" (= attach a file) -> "tar med den supportkod" (app: "Ta med den här koden").
15. Translation note: "för din bekvämlighet" (anglicism) -> "för att underlätta för dig".
