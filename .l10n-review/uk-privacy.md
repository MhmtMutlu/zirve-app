# uk · privacy review (2026-11-12)

Reviewed src/privacy.uk.html against privacy.en.html and privacy.tr.html, section by section.
Checks: tag sequence identical to en except the translation-note <p> (present, wording matches other languages);
counts match (href=24, {{=11, {=22, id=9, <=540+2); all numbers/durations (60 d, 7 d, 30 d, 90 d, 12/13/24 months,
1 h, 3 years, 13) and legal bases (GDPR Art. 6(1)(a)/(b)/(c)/(f), KVKK Art. 5) unchanged; game/UI terms match the uk
String Catalog (поверх, самоцвіти, Вежа дня, спокійний режим, табір, скриня, заморозка серії, рамка ліги, Штурхнути,
«попереду тебе», Підкорювачі вершин, Відновити покупки, Завантажити мої дані, Видалити обліковий запис,
Статистика використання, Код підтримки, Ділитися / Не ділитися, Параметри). The broken EN RevenueCat sentence is
rendered as a full sentence, as in TR.

Fixes (9):
1. §6 "Неповнолітні гравці" (= under 18) shifted the condition; EN means under the age of consent -> "Гравці, які не досягли віку згоди". (legal precision)
2. §7 Guest account: "(застосунок жодного разу не з’єднувався з нашим сервером)" read as "never connected at all" -> "(протягом цього часу застосунок жодного разу не з’єднується з нашим сервером)". (condition precision)
3. §7 Account deletion: "без зв’язку з твоїм обліковим записом" -> "після видалення зв’язку з твоїм обліковим записом" (EN "with the link ... removed").
4. §1 Technical: logs "містять ... не довше 7 днів" -> "зберігають ... не довше 7 днів" (retention, not content).
5. Summary + §1 Technical: calque "лише в моменті, під час з’єднання" -> "лише під час самого з’єднання"; "для ... для захисту" -> "з метою захисту".
6. Summary: duplicated "адресу" (email address / address) -> "поштову адресу".
7. §1 Social: calm-mode boards "проходиш" -> "розв’язуєш" (EN "solve").
8. §8 Breach: "зробимо повідомлення" -> "надішлемо повідомлення" (natural phrasing).
9. Header meta: "Набуває чинності й востаннє оновлено:" (mixed tense label) -> "Набрання чинності й останнє оновлення:".

Not changed / notes: "GDPR Art. …" kept in Latin form, consistent with all other languages. The iOS prompt name
"Дозволити програмам запитувати про відстеження" not verified against iOS uk; left as is. terms.uk.html header uses
"Набирає чинності та востаннє оновлено" — same mixed-tense label (not in this file's scope).
