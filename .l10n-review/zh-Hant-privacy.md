# zh-Hant · privacy review (2026-11-12)

Reviewed src/privacy.zh-Hant.html against privacy.en.html and privacy.tr.html, section by section.
Checks: tags/attributes/ids/hrefs/{{tokens}} identical to en (only extra element: translation-note <p>, present);
counts href= 24, {{ 11, { 22 match en; numbers and durations identical (extra "10" only from 2026 年 10 月 30 日);
legal bases (GDPR Art. 6(1)(a)/(b)/(c)/(f), KVKK Art. 5) unchanged; game terms match the app catalog
(層, 寶石, 每日高塔, 悠閒模式, 營地, 寶箱, 連續保護卡, 高塔主題, 頭像框, 戳一下, 頂尖攀登者, 回復購買項目,
下載我的資料, 刪除帳號, 使用統計資料, 客服代碼, 分享／不分享, 隱私權選項). RevenueCat sentence follows TR (complete sentence).

Fixes (9):
1. Intro: "本政策僅供你參考" ("for reference only", reads as non-binding/softened) -> "本政策旨在向你說明相關資訊" (TR: bilgilendirme amaçlı). (legal meaning)
2. §6 Ads: "加倍獎勵" (double the reward, stronger than source) -> "提高獎勵" (EN boost / TR ödülü artırmak). (meaning)
3. §6 "未達年齡的玩家" (incomplete) -> "未達同意年齡的玩家" (age of consent). (legal precision)
4. Summary: "用於廣告投放" (ad serving) -> "用於鎖定廣告對象" (ad targeting); sentence restructured so "never share" stays absolute. (meaning)
5. §1 Social: "你在聯賽週以前 3 名結束時" ("以前" misreads as "previously") -> "聯賽週結束時你名列前 3 名所獲得的獎項". (ambiguity)
6. §1 Social calm boards: "時間和花費多久" -> "解開的時間和花費時長" (when solved + duration). (clarity)
7. §1 Support emails: "你附上的客服代碼" -> "你附上的任何客服代碼" (optional, EN "any"). (meaning)
8. §5 Email: "郵件轉寄服務供應商" (forwarding) -> "郵件中繼（relay）服務供應商". (technical accuracy)
9. §3: "位於土耳其的我們的伺服器上" (unnatural) -> "在我們位於土耳其的伺服器上". (style)
