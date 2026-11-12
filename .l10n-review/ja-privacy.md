# ja · privacy review (2026-11-12)

Reviewed src/privacy.ja.html against privacy.en.html and privacy.tr.html, section by section.
Checks: tags/attributes/ids/hrefs/{{tokens}} identical to en (only extra element: translation-note <p>, present;
counts '<' 540+2, href= 24, '{{' 11, '{' 22); all numbers and durations identical (extra digits only from the
Japanese date format 2026年10月30日, 「1日あたり」 and 「頂上の20人」); legal bases (GDPR Art. 6(1)(a)/(b)/(c)/(f),
UK GDPR, KVKK Art. 5(1), 5(2)(c)/(ç)/(f)) unchanged; KVKK not translated. Game terms checked against the app's ja
String Catalog: ジェム, ライフ, 階, キャンプ, 宝箱, 今日のタワー, のんびりモード, 連続記録フリーズ, リーグフレーム,
衣装, つつく / 追い抜かれました, 頂上の20人, 購入を復元, データをダウンロード, アカウントを削除, サポートコード,
利用統計, プライバシーの選択. The broken EN sentence in the RevenueCat item is correctly rendered as in TR.

Fixes (11 issues, 16 text changes):
1. §6 heading "年齢に満たないプレイヤー" (under what age? unclear condition) -> "同意年齢未満のプレイヤー". (legal precision)
2. Translation note: "英語版が適用されます" -> "英語版が優先されます" (EN version prevails on discrepancy); "トルコのプレイヤー" -> "トルコにいるプレイヤー".
3. §1 Profile and §4: "タワーの見た目" -> "タワーテーマ" (app term, store.themes). (2 places)
4. §1 note and §7: calm-mode "解答" (= answer) -> "解いた盤面の記録" (app wording). (2 places)
5. §2 data column: "経済" -> "ゲーム内経済", matching the §1 category name. (2 places)
6. §1 and §4: "シェアした/シェアしない" -> "共有した/共有しない" (app uses 共有). (2 sentences)
7. §5 and §8: "権限のある当局" -> "管轄当局" (natural legal term). (2 places)
8. §1 Game progress "When": "各階のあと" -> "各階のプレイ後".
9. §6 intro: added "または" so the three ad uses read as alternatives, as in EN "or".
10. §7 deletion: "AppleにこのアプリのAppleでサインインの認可の取り消し" -> "Appleに、このアプリに対する「Appleでサインイン」の認可の取り消し" (readability).
11. §7: "Appleアカウント" -> "Apple Account" (consistent with §1 and Apple's ja naming).
No omissions, additions, softened/strengthened obligations, wrong numbers or wrong legal bases were found.
