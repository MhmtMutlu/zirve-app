# th review: content + support + delete (2026-11-12)

Independent review of `content/i18n/th.json`, `src/support.th.html`, `src/delete.th.html` against en.
Checks: all 480 JSON keys present and `translated`; tokens/placeholders/markup/digits identical per key;
support: `<` 62/62, `href=` 5/5, `{{` 5/5; delete: same except the required translation note (present).

## Fixes (12)
1. delete: "ประวัติการเลือกเรื่องสถิติ" -> "ประวัติตัวเลือกของคุณเกี่ยวกับสถิติการใช้งาน" (data category "history of your statistics choices" was vague).
2. delete: "ทำให้ไม่ระบุตัวตน" -> "ทำให้เป็นข้อมูลนิรนาม" ("made anonymous"; matches privacy.th).
3. delete: "ข้อมูลจะออกจากข้อมูลสำรอง..." -> "และข้อมูลจะหายไปจากข้อมูลสำรองที่เข้ารหัสภายใน 30 วัน" (natural, matches privacy.th; 30 days unchanged).
4. delete: "ตำแหน่งของคุณในตารางอันดับ" -> "อันดับของคุณในตารางอันดับต่างๆ" (glossary: place = อันดับ).
5. delete: "แนบข้อมูล" (attach) -> "ระบุข้อมูล" (include in the email).
6. delete: "ชั้นสถิติโดยประมาณ" -> "ชั้นสูงสุดที่เคยไปถึงโดยประมาณ" (record floor; app wording).
7. support: "อาจใช้เวลาสักครู่" (a moment) -> "อาจใช้เวลาสองสามนาที" (en: a few minutes).
8. support: heading "ความคืบหน้าไม่อยู่ใน..." -> "ความคืบหน้าหายไปใน..." (natural "is missing").
9. th.json home.games gates: "ก้าวแรกไม่มีทางเป็นทางออก" -> "ก้าวแรกไม่มีวันเป็นการพาบล็อกออก" (unclear wordplay).
10. th.json home.league_p: "จะตกลงไป" -> "จะตกลงหนึ่งระดับ" (move down a tier, parallel to move up).
11. th.json home.games lights: "แนวทแยงไม่ได้รับผล" -> "ช่องในแนวทแยงจะไม่สลับ" (natural).
12. th.json home.games colorMatch: "(แข็งตัวเมื่อเหลือ 0)" -> "(ถูกแช่แข็งเมื่อเหลือ 0)" (frozen tiles).

No omissions, additions, changed numbers/durations or legal bases found. Game terms (tiers, game names, เพชร, ชีวิต, ชั้น, แคมป์, หอคอยประจำวัน, ลงชื่อเข้าใช้ด้วย Apple, โค้ดช่วยเหลือ, กู้คืนการซื้อ) match the app catalog.
Not verified: full `build.py` run (not executed to avoid writing build output).
