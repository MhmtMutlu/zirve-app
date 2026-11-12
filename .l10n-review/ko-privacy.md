# ko privacy review (2026-11-12)

Reviewed src/privacy.ko.html against privacy.en.html / privacy.tr.html section by section. Tags, hrefs, ids, {{tokens}}, numbers, durations, legal references and the translation note checked (counts match en except the note paragraph).

Fixes:
1. Technical and security row: "<b>IP 주소</b>나 … <b>기록하지 않아요</b>" had an extra bold (56 vs 55 `<b>`); restored a single bold matching "We do <b>not record your IP address</b>".
2. Anti-cheat paragraph: "동의하지 않으면" (reads as "if you don't consent") -> "이에 이의가 있으면" (if you disagree with the decision); also smoothed "검사 결과 어떤 결과가".
3. Social row: "passed you" notification "추월" -> "나를 앞질렀어요" (app: friends.passed / push.passed).
4. Purposes row (notifications): "콕 찌르거나 추월했을 때" -> "나를 콕 찌르거나 앞질렀을 때" (same app term).
5. Game progress row: "매일 연속 기록" -> "일일 연속 기록" (natural for "daily streak").
6. Summary + Technical row: bare English "rate limiting" -> "요청 횟수 제한(rate limiting)" / "요청 횟수 제한".

No omissions, additions, wrong numbers or wrong legal bases found.
