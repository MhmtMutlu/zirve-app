# es review: content + support + delete (2026-11-12)

Checked: es.json has every en.json key, all `translated`; placeholders, {href:...}, markup, numbers identical (script walk).
support.es / delete.es: tags, hrefs, {{tokens}} identical to .en; translation-note present in delete.es (support has none in any language).

Fixes (9 edits; 4 counts two app-term fixes in one string, 8 covers two files):
1. delete.es — note: "desaparece de las copias…" had "la eliminación" as subject (the deletion vanishes from backups); now "los datos eliminados desaparecen de las copias de seguridad cifradas en un plazo de 30 días" (EN: "it leaves the encrypted backups within 30 days").
2. delete.es — "sin el vínculo con tu cuenta" → "desvinculados de tu cuenta" (EN: "with the link to your account removed").
3. delete.es — "cuentas que han iniciado sesión con Apple" → "cuentas con sesión iniciada con Apple" (accounts don't sign in).
4. es.json home.faq_html — app terms: "packs de gemas" → "paquetes de gemas" (store.gemPacks), "set de temporada" → "pack de temporada" (store.season.buySet).
5. es.json home.features — "pisos limpios" → "pisos impecables" (chest.subtitle).
6. es.json home.games colorSort — "¿atascado?" (gendered) → "¿te atascas?" (play.hint.colorSort).
7. es.json daily.legend — "Continuando" → "Tras continuar" (EN "With a continue").
8. es.json daily.lead — "así nadie se lleva un spoiler" → "así no se le estropea la sorpresa a nadie"; support.es — "tu progreso se pasará contigo" → "tu progreso te acompañará" (matches home.values).

No omissions, additions, changed numbers/durations or legal-basis errors found.
