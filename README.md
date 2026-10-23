# zirve-app

Zirve'nin web sitesi: tanıtım sayfası, gizlilik politikası, KVKK aydınlatma metni, hesap silme ve destek.
GitHub Pages ile yayınlanır: <https://mhmtmutlu.github.io/zirve-app/>

| Sayfa | Türkçe | English |
|---|---|---|
| Tanıtım | `/` | `/en/` |
| Günün kulesi (paylaşılan sonucun bağlantısı, Smart App Banner) | `/daily/` | `/en/daily/` |
| Gizlilik politikası | `/gizlilik/` | `/en/privacy/` |
| KVKK aydınlatma metni | `/kvkk/` | – |
| Hesap silme | `/hesap-silme/` | `/en/delete-account/` |
| Destek | `/destek/` | `/en/support/` |

## Düzenleme
- Metinler: tanıtım sayfası `build.py` içindeki `S` sözlüğünde, günün kulesi sayfası `DAILY` sözlüğünde, hukuki
  sayfalar `src/*.html`.
- Yayın günü: `build.py` → `APP_STORE_LIVE = True` (tek anahtar). App Store rozetleri gerçek bağlantı olur, "Çok yakında"
  ve TestFlight notları kalkar. Günün kulesi sayfasındaki Smart App Banner (`apple-itunes-app`, `app-argument=zirve://daily`)
  her zaman sayfadadır; Safari onu uygulama mağazada yayındayken gösterir.
- Derleme: `python3 build.py` (statik HTML'i depo köküne yazar ve tüm iç bağlantıları kontrol eder). Derlenmiş HTML de
  commit'lenir; GitHub Pages ek bir derleme adımı çalıştırmaz.
- Stil: `assets/site.css` (renkler ve yazı tipleri uygulamanın ZirveDesign tokenlarıyla aynı).
- Ekran görüntüleri `assets/shots/` (iPhone 17 Pro simülatörü, `-ZirveDebugCleanUI`, 9:41 durum çubuğu, WebP).

## Gizlilik
Site çerez, analiz veya üçüncü taraf istek kullanmaz; Fredoka ve Nunito yazı tipleri (SIL OFL) `assets/fonts/` altından
sunulur.

## app-ads.txt
`app-ads.txt` AdMob doğrulaması içindir. Google bu dosyayı App Store'daki geliştirici web sitesi alan adının **kökünde**
arar (ör. `https://mhmtmutlu.github.io/app-ads.txt`). Proje sitesi `/zirve-app/` altında olduğundan, kök alan adında
yayınlanması için aynı dosyanın `MhmtMutlu.github.io` deposuna da konması ya da bu siteye özel alan adı bağlanması gerekir.

## Yayına alma
Settings → Pages → Source: *Deploy from a branch* → Branch: `main` / `(root)`.
