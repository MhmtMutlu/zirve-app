# zh-Hant review: content + support + delete (2026-11-12)

Checked: all keys present in content/i18n/zh-Hant.json (none missing/extra, all `translated`); placeholders, {href:...}, markup identical to en.json. support/delete: tag sequence identical to .en.html (only addition: translation-note in delete, as required; support pages carry no note in any language); href=, {{ }}, { } counts match. Game terms checked against App/Resources/Localizable.xcstrings (zh-Hant) and docs/l10n/zh-Hant/glossary.md.

Fixes (7):
1. delete.zh-Hant.html (note, retention): "期間會移除與你帳號的連結，之後刪除或匿名化" read as the account link being removed at some point during retention. EN: kept *with the link to your account removed*, then deleted/anonymised. Now: "保留期間這些資料已移除與你帳號的連結，期滿後刪除或匿名化". (most serious)
2. delete.zh-Hant.html: "你的統計資料選擇紀錄" -> "你對使用統計資料所做選擇的紀錄" (history of usage-statistics choices; app term 使用統計資料).
3. delete.zh-Hant.html: "Game Center 紀錄會保留在 Apple" -> "Game Center 紀錄由 Apple 保留" (natural phrasing, same meaning).
4. support.zh-Hant.html: "生命會隨時間自動補滿" -> "自動恢復" (EN "refill over time"; app lives.out.body uses 自動恢復; 補滿 implied a full refill).
5. support.zh-Hant.html: "跟著你移過去" -> "跟著你轉移過去" (natural phrasing).
6. zh-Hant.json home.faq_html: "生命會隨時間補滿" -> "生命會隨時間恢復" (same as 4).
7. zh-Hant.json home.games flags: "瞭望塔絕不會相鄰" -> "瞭望塔不能相鄰" (a rule, not a prediction).
