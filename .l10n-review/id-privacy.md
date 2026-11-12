# id · privacy review (2026-11-12)

Reviewed src/privacy.id.html against privacy.en.html and privacy.tr.html, section by section.
Checks: tags/attributes/ids/hrefs/{{tokens}} identical to en (only extra element: translation-note <p>, present);
counts '<' 542 (en 540 + 2 for the note), href= 24, '{{' 11, '{' 22; number sequence identical to en; legal bases
(GDPR Art. 6(1)(a)/(b)/(c)/(f), KVKK Art. 5) unchanged; game/app terms match the id String Catalog (lantai, permata,
Menara Harian, mode santai, peti, kamp, runtunan, pembeku runtunan, bingkai, kostum, Colek, Pendaki Teratas,
Pulihkan pembelian, Unduh dataku, Hapus akun, Kode dukungan, Statistik penggunaan, Bagikan / Jangan bagikan, Tonton iklan).
The broken EN sentence in the RevenueCat item is rendered as in TR ("RevenueCat memproses data ini atas nama kami ...").

Fixes (9):
1. Summary: "Kami menyimpan data sesingkat mungkin" (as briefly as possible) strengthened "We keep data briefly" (TR "Kısa saklarız") -> "dalam waktu singkat". (obligation strengthened)
2. §6 "Pemain di bawah umur" (= minors, under 18) shifted the age-of-consent condition -> "Pemain di bawah usia persetujuan". (legal precision)
3. §10 right to object: "menolak" (refuse) -> "mengajukan keberatan (atas pemrosesan)", the standard term for the right to object; also in the rights list. (legal precision)
4. §1 Support emails: "kode dukungan yang kamu sertakan" lost "any" (optional) -> "serta kode dukungan jika kamu menyertakannya". (omission)
5. Summary: "data dengan nama samaran" (clashes with the "nickname" advice) -> "data pseudonim". (data category precision)
6. "merekam/direkam/perekaman" (audio/video recording) -> "mencatat/dicatat/pencatatan" for IP and statistics logging (5 places). (naturalness)
7. §7 guest account: "(aplikasi tidak pernah terhubung ...)" could read as "never connected at all" -> "(selama itu aplikasi tidak pernah terhubung ...)". (meaning)
8. §7 account deletion: "keluar dari cadangan" -> "terhapus dari cadangan". (naturalness)
9. §7 account deletion: "dengan tautan ke akunmu dihapus" ("tautan" = hyperlink) -> "dengan keterkaitannya ke akunmu diputus". (meaning)
