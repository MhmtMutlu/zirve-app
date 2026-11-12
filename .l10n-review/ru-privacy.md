# ru · privacy review (2026-11-12)

Reviewed src/privacy.ru.html against privacy.en.html and privacy.tr.html, section by section.
Checks: tag sequence identical to en (540 tags; only extra element is the translation-note <p>, present);
href= 24/24, {{ 11/11, { 22/22; all numbers/durations/dates identical; legal bases (GDPR Art. 6(1)(a)/(b)/(c)/(f),
KVKK Art. 5) unchanged; app terms match the ru catalog (этаж, кристаллы, Башня дня, Спокойный режим, лагерь, сундук,
заморозка серии, тема башни, рамка, Толкнуть, Лучшие альпинисты, Восстановить покупки, Скачать мои данные,
Удалить аккаунт, Код поддержки, Статистика использования). The broken EN RevenueCat sentence is rendered as in TR.

Fixes (13):
1. Intro: "не требует твоего согласия" could be read as "processing needs no consent" (stats in EEA do) -> "принимать её не нужно" (EN: needs no agreement). (meaning)
2. §7 Guest account: "(приложение ни разу не подключалось...)" read as never connected at all -> "(если за это время приложение ни разу не подключалось...)". (condition)
3. §9 Children: "младше 13 лет (или более старшего возраста...)" read as "a child of an older age" -> "или младше более высокого возраста, если его устанавливает твоя страна". (condition)
4. §6 "Несовершеннолетние игроки" (= under 18) shifted the age-of-consent condition -> "Игроки младше возраста согласия". (legal precision)
5. §7 RevenueCat: ambiguous "удалить свою запись" -> "хранящуюся у него запись о клиенте".
6. §7 Deletion record: "фиксируем ... на 3 года" -> "фиксируем, указывая только дату ... и храним эту запись 3 года".
7. §6 "Если ты его отключишь" (unclear antecedent) -> "Если ты отключишь отслеживание".
8. Summary: slang "в моменте" + "для ограничения частоты запросов против атак" -> "лишь кратковременно ... чтобы ограничивать частоту запросов для защиты от атак".
9. §1 Technical: same "в моменте" -> "лишь кратковременно ... чтобы ограничивать частоту запросов".
10. §1 Technical: logs "содержат ... не более 7 дней" -> "хранят ... не более 7 дней".
11. §2 table: "запросы ... и в поддержку" (broken coordination) -> "и обращения в поддержку".
12. Intro: "независимый разработчик из Турции" -> "живущий в Турции" (based in / yaşayan).
13. §10: "в течение 30 дней, бесплатно" -> "бесплатно в течение 30 дней" (word order).
