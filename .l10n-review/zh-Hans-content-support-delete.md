# zh-Hans review: content + support + delete (2026-11-12)

Checked: every key of en.json present in zh-Hans.json (no missing/extra), placeholders, `{href:...}`, markup and
numbers identical (only the localized month numbers/date format differ, as intended). support/delete: `<`, `href=`,
`{{`, `{`, `<b>`, `<li>` counts and every href/class/hreflang/rel identical to .en.html; delete.zh-Hans.html carries
the translation-note paragraph (support pages have none in any locale). Game terms match the app catalog and
glossary (每日之塔, 高级路线, 恢复购买, 通过 Apple 登录, 支持代码, 账号, 登顶榜, 轻松模式, 时间辅助, 宝石, 生命, 营地).
No number, duration, retention period or legal statement changed. `build.check_strings`: no problems.

## Fixes (6)
src/delete.zh-Hans.html
1. Translation note: "本译文仅为方便阅读而提供……对于土耳其的玩家" added "only" (仅) and read as "players of Turkey";
   EN says "for players in Türkiye". -> "本文是为方便你阅读而提供的译文。……对于在土耳其的玩家，以土耳其语版为准。"
   (also aligns with privacy.zh-Hans.html).
2. "统计数据选择的历史记录" (unclear: "statistics-data selection history") -> "你对使用统计所做选择的历史记录"
   (EN: the history of your usage-statistics choices, i.e. consent choices).
3. "如果你购买过项目" (unnatural) -> "如果你进行过购买".
4. "保留在 Apple" (incomplete) -> "保留在 Apple 处".
src/support.zh-Hans.html
5. "宝石会在购买后立即添加" -> "立即到账" (natural, matches "未到账" in the same answer).
content/i18n/zh-Hans.json
6. daily.legend[0] title "三星速度" -> "3 星速度" (keep the numeral as in EN "At 3-star speed").
