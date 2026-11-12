# ru review: content + support + delete (2026-11-12)

Checked: every key of en.json present in ru.json (no missing/extra), all states translated; placeholders, `{href:...}`, markup and numbers identical per key. Plural forms with fact placeholders verified against current values (11 головоломок, 16 миров, 10 этажей, 3 попытки). support/delete: tag sequence, href values and `{{...}}` tokens identical to .en.html; delete.ru.html carries the translation-note paragraph (only difference: +1 `<p class="translation-note">`); support pages have no note in any locale. No meaning, number, duration, retention period or legal statement changed. `build.check_strings`: language gate and fact-number checks pass.

## Fixes (12)
content/i18n/ru.json
1. daily.card_try (sample share card): "Твоя очередь" -> "Попробуй и ты" (app daily.share.tryIt on the same card; cta_h2 "Твоя очередь." left as is).
2. home.games[8].how[1] Gates: "отставить блок в сторону" -> "отодвинуть блок в сторону" (app term: howto.gates.2 / gates.reason.blocked "отодвинь").
3. home.games[8].harder[1]: "минимум 3, позже 4 заранее продуманных отставления в сторону" (unnatural noun) -> "блок придётся отодвинуть в сторону минимум 3 раза, позже — 4".
4. home.games[10].how[0] Lights: "светлые гаснут" -> "горящие гаснут" (app lights.on "Горит"; "lit" is not "light-coloured").
5. home.games_p: "кнопка ? возвращает её" -> "кнопка ? снова показывает её" ("brings it back" = shows the animation again).
src/support.ru.html
6. "с тем же Apple ID" -> "с тем же аккаунтом Apple" (Apple's current RU term on iOS 18+, same as delete.ru.html "аккаунте Apple").
7. "обновляет статус твоего сезона с сервера" -> "заново загружает с сервера статус твоего сезона" (unnatural).
8. "толкает тебя или обгоняет тебя" -> "толкает или обгоняет тебя" (redundant pronoun).
src/delete.ru.html
9. "неиспользованные кристаллы (не возвращаются)" -> "(деньги за них не возвращаются)" (en "not refundable" = no money refund; "не возвращаются" was ambiguous with gems being returned).
10. "дружба" -> "связи с друзьями" (friendships as data records; "дружба" read as the feeling).
11. "примерным этажом рекорда" -> "примерным рекордным этажом".
12. "мы можем попросить дополнительную проверку" -> "мы можем попросить тебя пройти дополнительную проверку" (en "ask you to verify further": the player verifies, not us requesting a check).

Not changed (noted): generic masculine past tense ("ты входил", "удалил", "Я открыл") kept, per docs/l10n/ru/qa.md policy. "Загрузите в App Store" is Apple's official RU badge text (Вы-form intentional). "номер заказа" for App Store Order ID left as is.
