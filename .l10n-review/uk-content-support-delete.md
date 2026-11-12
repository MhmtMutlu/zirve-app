# uk review: content/i18n/uk.json, src/support.uk.html, src/delete.uk.html

Checked: all 480 keys present (same as en), states `translated`; placeholders/markup/numbers/URLs identical to en;
support tags identical to en; delete tags identical except the required translation-note paragraph; tier and game
names match the app catalog; `python3 build.py` passes (only pre-existing first-view size warnings).

## Fixes (11)
1. delete.uk.html (note): "без зв’язку з твоїм обліковим записом" sat after the purchase-events clause only, so it read
   as if gem movements and cheat flags stayed linked to the account. Now explicitly applies to both (matches tr/en).
2. delete.uk.html: "квитанції магазину" -> "квитанції про покупки в магазині" (store receipts).
3. delete.uk.html: "обліковий запис та ідентифікатор (ідентифікатор гостя або зв’язок…)" -> "ідентифікаційні дані
   (ідентифікатор гостя або прив’язка до функції «Увійти з Apple»)" (identity, no repetition).
4. delete.uk.html: "якщо ти не можеш до нього дістатися" -> "якщо він тобі недоступний" (natural phrasing).
5. uk.json home.desc: "Жодної нав’язливої реклами" (no intrusive ads) -> "Жодної примусової реклами" (no forced ads; tr "Zorla reklam yok").
6. uk.json home.steps: gendered past "Не встиг зовсім трохи" -> "Забракло зовсім трохи часу" (glossary: no gendered past).
7. uk.json home.games colorSort: gendered "застряг?" -> "не виходить?".
8. uk.json home.games flags: gendered "ти позначаєш їх сам" -> "їх позначаєш ти".
9. uk.json home.values: gendered "коли ти сам її попросиш" -> "коли ти про неї просиш".
10. uk.json daily.desc: aspect mismatch "поширюй" -> "поширь".
11. uk.json daily.lead: "Рахується твоя найкраща спроба" -> "До рейтингу потрапляє твоя найкраща спроба" (en "is ranked").
