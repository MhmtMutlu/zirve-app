# de review: content + support + delete (2026-11-12)

Checked: every key of en.json present in de.json, all `.state` = translated; placeholders, `{href:...}`, markup and numbers identical (only reordered numbers in one `harder` line, same values). support/delete: tag, href, class, hreflang, `{{...}}` and number counts identical to .en.html; delete.de.html carries the translation-note paragraph (support pages have none in any language, as in the other locales). No meaning, number, duration, retention period or legal statement changed. `build.check_strings`: de ready.

## Fixes (10 edits in 9 items)
content/i18n/de.json
1. home.features[3] chest text: "fehlerfreien Etagen" -> "makellosen Etagen" (app term, chest.subtitle "10 makellose Etagen").
2. home.games[10].how[0] Lights: "(ein +) wechseln" -> "schalten um" (app: lights.a11y.hint "schaltet ... um"; "wechseln" was vague).
3. home.games[10].how[1]: "welche Felder wechseln" -> "welche Felder umschalten".
4. daily.card_try (sample share card): "Du bist dran" -> "Jetzt du" (app daily.share.tryIt on the same card).
5. daily.steps[1] text: "der beste kommt in die Rangliste deines Landes und unter Freunden" -> "der beste zählt für die Rangliste in deinem Land und unter Freunden" (ungrammatical coordination).
6. home.games_p: "?-Taste" -> "?-Schaltfläche" (on-screen button, not a key).
7. home.games[9].harder[1] Lookouts: "für dich gepunktet" -> "schon mit Punkten markiert" (unnatural).
src/support.de.html
8. Season premium answer: "aktualisiert deinen Saisonstatus vom Server" -> "lädt deinen Saisonstatus neu vom Server" (unnatural).
src/delete.de.html
9. "Konten, die mit Apple angemeldet sind" -> "Konten, bei denen du dich mit Apple angemeldet hast" (accounts are not signed in; the player is); also "falls du ihn nicht erreichst" -> "falls du ihn nicht abrufen kannst" (support code).

Not changed (noted): translation-note wording "zu deiner Erleichterung" is slightly stiff but identical across all de legal pages; left for consistency.
