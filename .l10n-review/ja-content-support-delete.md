# ja review: content + support + delete (2026-11-12)

Checked: every en.json key present in ja.json (state translated), placeholders/{href:..}/markup identical; support.ja.html and delete.ja.html tag sequence, href, {{R}}/{{CONTACT}}/{{UPDATED}} identical to .en.html; translation note present in delete.ja.html (not required on support). `python3 build.py` passes.

Fixes (10):
1. delete.ja.html: data category "League entries" was 「リーグの記録」 (league records); now 「リーグへの参加記録」.
2. delete.ja.html: "calm list" was the invented 「のんびりリスト」; now 「のんびりモードのリスト」 (app: のんびりモード).
3. delete.ja.html: translation note "players in Turkey" 「トルコのプレイヤー」 → 「トルコ国内のプレイヤー」 (precise, matches privacy.ja).
4. ja.json home.steps[1][1]: "Miss it by a hair" read as "almost run out of time"; now 「あと少しのところで時間切れになっても」.
5. ja.json home.games[8].how[1]: invented 「脇に止めて」 → app wording 「わきによけて」 (howto.gates.2).
6. ja.json home.games[8].harder[1]: invented noun 「計画的な脇止め」 → 「計画的にブロックをわきによける手が最低3回、のちに4回必要」.
7. ja.json home.games_p: 「時間が始まる前に」 (unnatural) → 「タイマーが動き出す前に」.
8. ja.json definition: run-on relative clause rewritten, same meaning: 「タワーを登っていくゲームで、どの階も{puzzleTypes}種類のなかから出題される、短い時間制限つきのパズルです。」
9. ja.json home.desc: same rewrite (no "timed", as in en).
10. ja.json home.how_h2: 「1分かからない」 → 「1分もかからない」.

No omissions, additions, number/duration or legal-basis errors found; support.ja.html needed no changes.
