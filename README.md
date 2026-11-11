# zirve-app

Zirve'nin web sitesi: tanıtım sayfası, gizlilik politikası, KVKK aydınlatma metni, hesap silme ve destek.
GitHub Pages ile yayınlanır: <https://zirve.mm-apps.com/>

| Sayfa | Türkçe | English |
|---|---|---|
| Tanıtım | `/` | `/en/` |
| Günün kulesi (paylaşılan sonucun bağlantısı, Smart App Banner) | `/daily/` | `/en/daily/` |
| Gizlilik politikası | `/gizlilik/` | `/en/privacy/` |
| Kullanım koşulları | `/kosullar/` | `/en/terms/` |
| KVKK aydınlatma metni | `/kvkk/` | – |
| Hesap silme | `/hesap-silme/` | `/en/delete-account/` |
| Destek | `/destek/` | `/en/support/` |

## Yapı
`python3 build.py` bütün siteyi depo köküne üretir ve ardından denetimleri çalıştırır (hata varsa çıkış kodu 1,
uyarılar ekrana yazılır). Derlenmiş HTML commit'lenir; GitHub Pages ek derleme çalıştırmaz. Site statik ve
barındırmadan bağımsızdır: sunucu başlığı varsayılmaz (CSP ve referrer `<meta>` ile), iç bağlantılar köke göre
(`/en/privacy/`), canonical, hreflang ve OG adresleri `https://zirve.mm-apps.com` ile mutlak.

| Yer | İçerik |
|---|---|
| `data/facts.json` | Olguların tek kaynağı ve **sürüm bayrağı** (`live`). Lig kademeleri, uygulama dilleri, `softwareVersion` sürüme göre; bulmaca sayısı, dünya, lig, günün kulesi, mağaza adları, `offlineVerified`/`macVerified` |
| `data/site.json` | Taban adres, iletişim, IndexNow anahtarı, Apple ticari marka satırı |
| `data/lastmod.json` | Sayfa içeriğinin hash'i → son değişiklik tarihi (derleme yazar; tarih yalnızca içerik değişince ilerler) |
| `content/i18n/<dil>.json` | Sitenin bütün metinleri; her anahtar `{value, state}` (`translated` / `needs_review`). `{puzzleTypes}` gibi yer tutucular `facts.json`'dan, `{href:privacy}` sayfa tablosundan gelir; `_html` ile biten anahtarlar HTML içerebilir |
| `src/<belge>.<dil>.html` | Hukuk metinleri: privacy, terms, kvkk, delete, support (`{{CONTACT}}`, `{{UPDATED}}`, `{{R}}`) |
| `build.py` → `LANGS` | Dil tablosu: yol öneki, `html lang`, hreflang, `og:locale`, App Store rozeti, yazı sistemi, `published` |
| `build.py` → `PAGES` | Sayfa tablosu: sayfa başına dile göre yol (Türkçe 1.0 yollarını korur) |
| `assets/site.css`, `assets/site.js` | Stil ve tek betik (menüler, dil şeridi); satır içi betik yok |
| `assets/fonts/` | Yazı sistemine göre alt kümeler (`scripts/subset-fonts.py`, kaynaklar `assets-src/fonts/`) |
| `assets/badges/` | Apple'ın resmî "Download on the App Store" rozetleri, dile göre (`scripts/badges.sh`) |
| `assets/og/` | Dile göre OG görselleri: derleme `manifest.json`'ı yazar, `scripts/og.swift` çizer ve `rendered.json`'ı yazar |

Üretilenler: sayfalar, `404.html`, `robots.txt`, `sitemap.xml` (hreflang alternatifleriyle), `llms.txt`,
`<IndexNow anahtarı>.txt`, `assets/og/manifest.json`.

### Denetimler (`build.py`)
Hata (yayın yok): yayındaki bir dilde eksik ya da `needs_review` anahtar; olgu sayısının metne çıplak rakamla yazılması
(`{puzzleTypes}` yerine "11 bulmaca"); `facts.json` ↔ uygulama deposu (bulmaca türleri ve açılış kampları, dünya sayısı,
1.1 lig kademeleri, lig boyutu/yükselme/düşme, günün kulesi, uygulama dilleri, her dilde oyun ve kademe adları; depo
`../zirve` ya da `ZIRVE_APP_REPO`); sürüm bayrağı; canonical ve karşılıklı hreflang + `x-default`; sitemap ↔ dosyalar;
JSON-LD sözdizimi, tek `@graph`, `FAQPage` yalnızca destekte, JSON-LD metinlerinin görünür metinde birebir geçmesi;
kırık iç bağlantı, `<img>` alt/boyut, tek H1; başlık, H1 ve URL'de yasaklı ifade.
Uyarı (insan bakar): gövdede yasaklı ifade, ilk görünüm bütçesi (Latin 100 KB), güncel olmayan OG görseli. İncelenen
bir gövde uyarısı `data/lint-allow.json`'a `{"page", "phrase", "reason"}` olarak eklenip susturulabilir.

### Yayın günü (1.1)
`data/facts.json` → `"live": "1.1"` ve `versions.1.1.releaseDate`; `python3 build.py`. Lig kademeleri, dil sayısı ve
adları, JSON-LD `softwareVersion`/`inLanguage`, `llms.txt` birlikte değişir. OG görselleri sayı içeriyorsa
`scripts/og.swift` yeniden çalıştırılır.

### Yeni dil eklemek
1. `content/i18n/<kod>.json`: `tr.json`'daki bütün anahtarlar, `state: "translated"` (oyun ve kademe adları uygulamanın
   String Catalog'undakiyle aynı olmalı; derleme karşılaştırır).
2. Hukuk sayfaları için `src/<belge>.<kod>.html` (yoksa o sayfa o dilde üretilmez, bağlantılar Türkçeye düşer).
3. `build.py` → `LANGS` satırında `published=True`. Eksik ya da `needs_review` anahtar varsa derleme durur; diğer
   diller etkilenmez.
4. `python3 build.py`; Latin dışı yazıda OG kartı için `scripts/og.swift` başka yazı tipi ister (şimdilik varsayılan
   Türkçe görsel kullanılır, uyarı verilir).
5. Rozet: `LANGS` → `badge` (Apple'ın o dilde rozeti yoksa `en-us`).

### Yardımcı betikler (`scripts/`)
- `indexnow.sh`: deploy **sonrası** değişen sayfaları IndexNow'a bildirir (`DRY_RUN=1` ile yalnızca yazdırır).
- `subset-fonts.py`: yazı tipi alt kümeleri (fontTools + brotli gerekir).
- `images.sh`: hero görselinin AVIF/WebP boyutları (macOS `sips`, `cwebp`).
- `badges.sh`: Apple rozetlerini yeniden indirir.
- `og.swift`: OG görselleri (`swiftc -O scripts/og.swift -o /tmp/zirve-og && /tmp/zirve-og ../zirve/App/Resources/Fonts assets/og/manifest.json`).
- Ekran görüntüleri `assets/shots/` (iPhone 17 Pro simülatörü, `-ZirveDebugCleanUI`, 9:41 durum çubuğu, WebP).

## Gizlilik
Site çerez, analiz veya üçüncü taraf istek kullanmaz; Fredoka ve Nunito yazı tipleri (SIL OFL) `assets/fonts/` altından
sunulur. `robots.txt` bütün tarayıcılara açık (arama, kullanıcı getirmeleri ve eğitim; `Google-Extended` dahil).

## app-ads.txt
`app-ads.txt` AdMob doğrulaması içindir. Google bu dosyayı App Store'daki geliştirici web sitesi alan adının **kökünde**
arar; site `zirve.mm-apps.com` kökünde yayınlandığı için <https://zirve.mm-apps.com/app-ads.txt> doğrudan geçerlidir.
App Store Connect'teki pazarlama adresi de bu alan adında olmalıdır.

## Yayına alma
Settings → Pages → Source: *Deploy from a branch* → Branch: `main` / `(root)`.
