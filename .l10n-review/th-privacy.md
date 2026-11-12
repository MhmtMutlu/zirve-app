# th · privacy review (2026-11-12)

Reviewed src/privacy.th.html against privacy.en.html and privacy.tr.html, section by section.
Checks: tags/attributes/ids/hrefs/{{tokens}} identical to en (only extra element: translation-note <p>, present;
counts '<' 540+2, href= 24, '{{' 11, '{' 22); all numbers and durations identical to en (digit multiset equal);
legal bases (GDPR Art. 6(1)(a)/(b)/(c)/(f), UK GDPR, KVKK Art. 5(1), 5(2)(c)/(ç)/(f)) unchanged; KVKK not translated.
Game/app terms checked against the th String Catalog and docs/l10n/th/glossary.md: เพชร, ชีวิต, ชั้น, แคมป์, หีบ,
หอคอยประจำวัน (รอบ = attempt), โหมดผ่อนคลาย, ตัวป้องกันสตรีค, ธีมหอคอย, กรอบลีก, สะกิด / แซงคุณแล้ว, สุดยอดนักปีน,
กู้คืนการซื้อ, ดาวน์โหลดข้อมูลของฉัน, ลบบัญชี, โค้ดช่วยเหลือ, สถิติการใช้งาน, แชร์ / ไม่แชร์, ตัวเลือกความเป็นส่วนตัว.
RevenueCat item renders the broken EN sentence as TR does (correct).

Fixes (6 issues, 15 text changes):
1. Intro: "ไม่จำเป็นต้องให้ความยินยอมหรือตกลงใดๆ" (no consent or agreement needed) -> "ไม่จำเป็นต้องตกลงยอมรับ".
   EN/TR say only "needs no agreement"; the added "consent" contradicted the consent-based processing (EEA statistics,
   personalised ads). (most serious)
2. §1 Diagnostics: "...หรือข้อมูลติดต่อ ผูกกับ ID บัญชีของคุณ" could be read as "no contact details linked to your
   account ID" -> "...หรือข้อมูลติดต่อ รายงานนี้ผูกกับ ID บัญชีของคุณ" (the link to the account is a disclosure).
3. "ไม่เคย" (= have never, a past-tense statement) -> "จะไม่ ... เลย" (forward-looking policy commitment, as EN
   "never"): summary (ad targeting/sharing), §1 Purchases (card details), §1 Technical (private key), §2 statistics
   use, §3 statistics (3 places), §6 own statistics (2 places).
4. §3 Other countries: "แจ้งให้คุณทราบในหนึ่งบรรทัด" -> "แจ้งให้คุณทราบด้วยข้อความหนึ่งบรรทัด" (naturalness).
5. §5 and §8: "หน่วยงานที่มีอำนาจ" -> "หน่วยงานที่มีอำนาจหน้าที่" (standard Thai legal term for competent authority). (2 places)
6. §7 deletion: "เพิกถอนการอนุญาตลงชื่อเข้าใช้ด้วย Apple ของแอป" -> "เพิกถอนการอนุญาต “ลงชื่อเข้าใช้ด้วย Apple” ที่ให้ไว้กับแอปนี้" (readability).
No omissions, wrong numbers, wrong legal bases or mistranslated data categories were found.
