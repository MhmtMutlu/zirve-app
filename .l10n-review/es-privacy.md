# es · privacy review (2026-11-12)

Reviewed src/privacy.es.html against privacy.en.html and privacy.tr.html, section by section.
Checks: tag sequence identical to en (only extra element: translation-note <p>, present); href=24, {{=11, {=22 match;
number sequence identical; legal bases (GDPR Art. 6(1)(a)/(b)/(c)/(f), KVKK Art. 5) unchanged; RevenueCat sentence
rendered as in TR (EN source has a broken sentence there). Game terms match the app (piso, gemas, torre del día,
modo relax, campamento, cofre, protector de racha, traje, marco, toque, te adelantó, En la cima, Restaurar compras,
Descargar mis datos, Eliminar cuenta, Estadísticas de uso, Código de soporte, Ver un anuncio, Condiciones de uso).

Fixes (10):
1. "la App Store" (5x: §1 usage stats, §5 RevenueCat x2, §5 Apple, §9 Children) -> "del App Store" (glossary: masculine, as on the site).
2. §6 "Jugadores menores de edad" (= under 18) shifted the condition; EN ties it to the age of consent -> "Jugadores por debajo de la edad de consentimiento". (legal precision)
3. §10 complaint: KVKK "Board" (Kurul) rendered as "Autoridad" -> "Consejo de Protección de Datos Personales (Kişisel Verileri Koruma Kurulu)". (legal precision)
4. §1 Progress: "recompensas obtenidas" (earned) -> "recompensas reclamadas" (EN: claimed rewards; glossary claim = reclamar).
5. §1 Social "When": "Al entrar en una liga" -> "Cuando se te asigna a una liga" (EN: when seated in a league).
6. §1 Technical: "contienen ... durante un máximo de 7 días" (unidiomatic) -> "guardan ... durante un máximo de 7 días".
7. §1 note below table: "resoluciones" (unnatural for solves) -> "puzles resueltos" (app: "Puzles resueltos en modo relax").
8. §7 Retention: same term, "las resoluciones del modo relax" -> "los puzles resueltos en modo relax".
9. §3 EEA: "hasta que respondes, ni nada si eliges" -> "hasta que respondas, ni tampoco si eliges" (grammar/naturalness).
10. §5 Google: "si lo permitiste" -> "si los permitiste" (agreement with IDFA + personalised ads).
