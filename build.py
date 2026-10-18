#!/usr/bin/env python3
"""Builds the Zirve website into static HTML (GitHub Pages serves the repository root).

    python3 build.py

Pages: landing (tr at /, en at /en/), privacy (gizlilik, en/privacy), KVKK, account deletion
(hesap-silme, en/delete-account), support (destek, en/support), 404. Legal bodies live in src/*.html;
this script wraps them in the shared header/footer. Paths are relative so the site works both at
https://<user>.github.io/zirve-app/ and on a custom domain. No cookies, no analytics, no third-party
requests: fonts are self-hosted.
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
CONTACT = "apps.support.mm@gmail.com"
UPDATED = {"tr": "19.10.2026", "en": "19 October 2026"}

# ---------------------------------------------------------------------------------------------- icons
def icon(paths, fill=None, stroke="currentColor", width=2, size=24):
    parts = []
    for d in paths:
        parts.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')
    for d in (fill or []):
        parts.append(f'<path d="{d}" fill="currentColor"/>')
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" aria-hidden="true">{"".join(parts)}</svg>'

HEART = "M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"
STAR = "M12 2l2.9 6.6 7.1.7-5.4 4.7 1.6 7L12 17.4 5.8 21l1.6-7L2 9.3l7.1-.7z"
I = {
    "life": icon([HEART], [HEART]),
    "gem": icon(["M7 3h10l4 6-9 12L3 9z", "M3 9h18M10 3l2 6 2-6"]),
    "star": icon([STAR], [STAR], width=1.5),
    "flame": icon(["M12 22c4 0 7-3 7-7 0-3-2-5-3-7-1 2-2 3-3 3 0-3-1-6-3-9-1 4-5 7-5 12 0 4 3 8 7 8z"]),
    "trophy": icon(["M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0z", "M7 6H4a3 3 0 0 0 3 4M17 6h3a3 3 0 0 1-3 4"]),
    "shield": icon(["M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z", "M9 12l2 2 4-4"]),
    "camp": icon(["M3 20h18L12 4z", "M12 20v-6"]),
    "daily": icon(["M12 3l3 4h-6zM7 7h10v14H7z", "M10 11h4M10 15h4"]),
    "season": icon(["M3 9a2 2 0 0 0 0 6v3h18v-3a2 2 0 0 0 0-6V6H3z", "M13 6v12"]),
    "friends": icon(["M12.5 8a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0z", "M2 20a7 7 0 0 1 14 0", "M20 9a3 3 0 1 1-6 0 3 3 0 0 1 6 0z", "M16 20a6 6 0 0 1 6-6"]),
    "clock": icon(["M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z", "M12 7v5l3 2"]),
    "hint": icon(["M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.7.6 1 1.4 1 2.5h6c0-1.1.3-1.9 1-2.5A6 6 0 0 0 12 3z"]),
    "check": icon(["M5 12l5 5 9-10"], width=3),
    "offline": icon(["M2 8.5a15 15 0 0 1 6-3.2M12 12.5a7 7 0 0 1 4.5 1.6M9 16.5a3 3 0 0 1 3-.5", "M3 3l18 18"]),
    "eye": icon(["M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z", "M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"]),
    "globe": icon(["M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z", "M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"]),
    "user": icon(["M16 8a4 4 0 1 1-8 0 4 4 0 0 1 8 0z", "M4 21a8 8 0 0 1 16 0"]),
    "puzzle": icon(["M4 7h4a2 2 0 1 1 4 0h4v4a2 2 0 1 1 0 4v4H4z"]),
}
APPLE = '<svg viewBox="0 0 24 28" aria-hidden="true"><path fill="currentColor" d="M19.7 14.9c0-3.3 2.7-4.9 2.8-5-1.5-2.2-3.9-2.5-4.7-2.6-2-.2-3.9 1.2-4.9 1.2s-2.6-1.2-4.2-1.1c-2.2 0-4.2 1.3-5.3 3.2-2.3 4-.6 9.8 1.6 13 1.1 1.6 2.4 3.3 4.1 3.3 1.6-.1 2.3-1.1 4.2-1.1s2.5 1.1 4.2 1 2.8-1.6 3.8-3.2c1.2-1.8 1.7-3.6 1.7-3.7 0 0-3.3-1.3-3.3-5.0zM16.6 5.2c.9-1.1 1.5-2.6 1.3-4.1-1.3.1-2.8.9-3.8 2-.8.9-1.6 2.5-1.4 3.9 1.5.1 2.9-.7 3.9-1.8z"/></svg>'

def mascot(body="#2E7D5B", hat="#F08A3C", band="#D9731F", cls=""):
    return (f'<svg class="{cls}" viewBox="0 0 64 68" aria-hidden="true">'
            f'<rect x="18" y="34" width="28" height="26" rx="12" fill="{body}"/><rect x="24" y="40" width="16" height="12" rx="6" fill="#F4F6F1"/>'
            f'<rect x="12" y="38" width="8" height="18" rx="4" fill="{body}"/><rect x="44" y="38" width="8" height="18" rx="4" fill="{body}"/>'
            f'<circle cx="32" cy="22" r="14" fill="#F8D9BF"/><path d="M16 22 a16 16 0 0 1 32 0 z" fill="{hat}"/>'
            f'<rect x="14" y="19" width="36" height="6" rx="3" fill="{band}"/><circle cx="32" cy="22" r="3.5" fill="#FFF4C2"/>'
            '<circle cx="27" cy="28" r="1.6" fill="#1F2A24"/><circle cx="37" cy="28" r="1.6" fill="#1F2A24"/>'
            '<path d="M28 32 q4 3 8 0" stroke="#1F2A24" stroke-width="1.6" stroke-linecap="round" fill="none"/></svg>')

# Mini illustrations of the eight puzzles (76×76), drawn with the app's tile colours.
G = {
    "colorMatch": '<svg viewBox="0 0 76 76" aria-hidden="true"><rect x="4" y="4" width="32" height="32" rx="9" fill="#7FB77E"/><circle cx="20" cy="20" r="6" fill="#fff"/><rect x="40" y="4" width="32" height="32" rx="9" fill="#7FB77E"/><circle cx="56" cy="20" r="6" fill="#fff"/><rect x="4" y="40" width="32" height="32" rx="9" fill="#6FA8DC"/><rect x="14" y="50" width="12" height="12" rx="3" fill="#fff"/><rect x="40" y="40" width="32" height="32" rx="9" fill="#F08A3C"/><path d="M56 47l8 14H48z" fill="#fff"/><path d="M31 20h14" stroke="#1F2A24" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="1 5"/></svg>',
    "pathDraw": '<svg viewBox="0 0 76 76" aria-hidden="true"><g fill="#C9D2CC"><circle cx="14" cy="14" r="4"/><circle cx="38" cy="14" r="4"/><circle cx="62" cy="38" r="4"/><circle cx="14" cy="38" r="4"/><circle cx="38" cy="62" r="4"/><circle cx="62" cy="62" r="4"/></g><path d="M14 62V38h24V14h24" stroke="#2B5E8E" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="14" cy="62" r="8" fill="#2E7D5B"/><circle cx="14" cy="62" r="3" fill="#fff"/><circle cx="38" cy="38" r="6" fill="#E0A93A"/><circle cx="62" cy="14" r="10" fill="#DCEBD6"/><path d="M58 20V8h7l-1.5 3 1.5 3h-7" stroke="#2E7D5B" stroke-width="2" fill="none" stroke-linejoin="round"/></svg>',
    "blockFit": '<svg viewBox="0 0 76 76" aria-hidden="true"><g fill="#CFE4C4"><rect x="4" y="4" width="20" height="20" rx="5"/><rect x="28" y="4" width="20" height="20" rx="5"/><rect x="52" y="52" width="20" height="20" rx="5"/></g><g fill="#A58AE0"><rect x="52" y="4" width="20" height="20" rx="5"/><rect x="52" y="28" width="20" height="20" rx="5"/></g><g fill="#F08A3C"><rect x="4" y="28" width="20" height="20" rx="5"/><rect x="28" y="28" width="20" height="20" rx="5"/><rect x="4" y="52" width="20" height="20" rx="5"/></g><rect x="28" y="52" width="20" height="20" rx="5" fill="none" stroke="#C9D2CC" stroke-width="2.5" stroke-dasharray="4 3"/></svg>',
    "memory": '<svg viewBox="0 0 76 76" aria-hidden="true"><rect x="4" y="8" width="30" height="40" rx="8" fill="#2B5E8E"/><circle cx="19" cy="28" r="6" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="2.5"/><rect x="40" y="8" width="30" height="40" rx="8" fill="#fff" stroke="#1F2A24" stroke-width="2.5"/><path d="M63 21C53 21 47 27 47 37c10 0 16-6 16-16z" fill="#7FB77E"/><rect x="22" y="34" width="30" height="40" rx="8" fill="#DCEBD6" stroke="#2E7D5B" stroke-width="2.5"/><path d="M45 47C35 47 29 53 29 63c10 0 16-6 16-16z" fill="#7FB77E"/></svg>',
    "pipes": '<svg viewBox="0 0 76 76" aria-hidden="true"><rect x="2" y="2" width="72" height="72" rx="14" fill="#E3EEF9"/><path d="M8 38h22a8 8 0 0 0 8-8V8" stroke="#6FA8DC" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M38 68V50a8 8 0 0 1 8-8h22" stroke="#C9D2CC" stroke-width="9" fill="none" stroke-linecap="round"/><circle cx="8" cy="38" r="7" fill="#2B5E8E"/><circle cx="68" cy="42" r="7" fill="#2E7D5B"/></svg>',
    "flow": '<svg viewBox="0 0 76 76" aria-hidden="true"><path d="M12 12h26v26h26" stroke="#E0565B" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 38v26h52" stroke="#6FA8DC" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="12" r="9" fill="#E0565B"/><circle cx="64" cy="38" r="9" fill="#E0565B"/><circle cx="12" cy="38" r="9" fill="#6FA8DC"/><circle cx="64" cy="64" r="9" fill="#6FA8DC"/></svg>',
    "colorSort": '<svg viewBox="0 0 76 76" aria-hidden="true"><g stroke="#8A958E" stroke-width="2.5" fill="none"><path d="M8 6v56a8 8 0 0 0 16 0V6"/><path d="M30 6v56a8 8 0 0 0 16 0V6"/><path d="M52 6v56a8 8 0 0 0 16 0V6"/></g><path d="M10 42h12v20a6 6 0 0 1-12 0z" fill="#F08A3C"/><rect x="10" y="26" width="12" height="16" fill="#A58AE0"/><path d="M32 30h12v32a6 6 0 0 1-12 0z" fill="#A58AE0"/><path d="M54 46h12v16a6 6 0 0 1-12 0z" fill="#F08A3C"/></svg>',
    "lights": '<svg viewBox="0 0 76 76" aria-hidden="true"><g fill="#F2B531"><rect x="2" y="2" width="22" height="22" rx="6"/><rect x="27" y="2" width="22" height="22" rx="6"/><rect x="52" y="27" width="22" height="22" rx="6"/><rect x="2" y="27" width="22" height="22" rx="6"/><rect x="27" y="52" width="22" height="22" rx="6"/></g><g fill="#F4F6F1" stroke="#E3E9E0" stroke-width="2"><rect x="52" y="2" width="22" height="22" rx="6"/><rect x="27" y="27" width="22" height="22" rx="6"/><rect x="2" y="52" width="22" height="22" rx="6"/><rect x="52" y="52" width="22" height="22" rx="6"/></g><g fill="#5A3E00"><circle cx="13" cy="13" r="4"/><circle cx="38" cy="13" r="4"/><circle cx="63" cy="38" r="4"/><circle cx="13" cy="38" r="4"/><circle cx="38" cy="63" r="4"/></g></svg>',
}

# ------------------------------------------------------------------------------------------- strings
S = {
"tr": {
  "lang": "tr", "other_lang": "en", "other_label": "EN", "other_name": "English",
  "title": "Zirve · Kuleye tırman, her kat bir bulmaca",
  "desc": "Zirve, 30–60 saniyelik bulmacalardan oluşan sonsuz bir kule. Çöz, bir kat yüksel, haftalık ligde arkadaşlarını geç. iPhone ve iPad için.",
  "nav": [("#nasil", "Nasıl oynanır"), ("#oyunlar", "Oyunlar"), ("#dunyalar", "Dünyalar"), ("#lig", "Lig"), ("#sss", "SSS")],
  "soon": "iPhone ve iPad için · çok yakında",
  "h1": "Kuleye tırman.<br><em>Her kat</em> bir bulmaca.",
  "lead": "Zirve, kısa bulmacalardan oluşan sonsuz bir kule. Çöz, bir kat yüksel, kampa ulaş ve haftalık ligde arkadaşlarını geç.",
  "badge_small": "Çok yakında", "badge_big": "App Store", "how_btn": "Nasıl oynanır",
  "trust": ["Ücretsiz", "Hesap gerekmez", "Çevrimdışı oynanır", "6 dil"],
  "f1": ("2 gün", "seri"), "f2": ("Kat 6 geçildi", ""), "f3": ("5/5", "can"),
  "how_eyebrow": "Nasıl oynanır", "how_h2": "Bir dakikadan kısa, beş saniyede anlaşılır.",
  "how_p": "Her kat tek bir bulmaca. Kuralları ekrana bakar bakmaz anlarsın; zorluk yükseldikçe tahta değişir, süre değil.",
  "steps": [("Katını aç", "Tırman'a bas, karşına o katın bulmacası gelsin: renkler, yollar, bloklar ya da kartlar."),
            ("Süre bitmeden çöz", "30–60 saniyen var. Kıl payı kaçırırsan tahta aynen kalır; bir nefes al ve bitir."),
            ("Yüksel, kampa ulaş", "Her 10 katta bir kamp seni bekler. Canların bitse bile rekorun yerinde durur.")],
  "games_eyebrow": "Oyunlar", "games_h2": "Sekiz bulmaca, tek kule.",
  "games_p": "Her kat farklı bir oyunla gelir; yükseldikçe yenileri açılır. Her tahta üretilirken bilgisayar tarafından çözülerek doğrulanır: çözümsüz bulmaca yok.",
  "games": [("colorMatch", "Renk birleştirme", "Aynı renkteki taşları yan yana sürükle, birleştir, tahtayı temizle."),
            ("pathDraw", "Yol çizme", "Parmağını kaldırmadan ara noktalardan geçip bayrağa ulaş. Duvarlara dikkat."),
            ("blockFit", "Blok yerleştirme", "Parçaları döndür, boşluklara tam oturt. Bazı parçaların aynası gerekir."),
            ("memory", "Hafıza", "Kartları çevir, eşleri bul. Yukarıda üçlüler seni bekliyor."),
            ("pipes", "Boru çevirme", "Boruları döndür, suyu kaynaktan bayrağa kesintisiz akıt."),
            ("flow", "Akış", "Aynı renkteki uçları birleştir; çizgiler hiç kesişmesin."),
            ("colorSort", "Renk dizme", "Tüplerdeki renkleri dök, her tüpte tek renk kalsın."),
            ("lights", "Işık", "Dokunduğun hücre ve dört komşusu yer değiştirir. Hepsini yak.")],
  "shots": [("play-path", "Yol çizme"), ("play-color", "Renk birleştirme"), ("play-blocks", "Blok yerleştirme"), ("play-lights", "Işık")],
  "worlds_eyebrow": "Dünyalar", "worlds_h2": "Dört dünya, sonu olmayan bir kule.",
  "worlds_p": "Ormandan başla, bulutların arasından uzaya çık, kristal zirveye ulaş. Her dünyada kurallar biraz daha zorlaşır.",
  "worlds": [("forest", "Orman", "Kat 1–29"), ("clouds", "Bulutlar", "Kat 30–59"), ("space", "Uzay", "Kat 60–99"), ("crystal", "Kristal Zirve", "Kat 100 ve üstü")],
  "floor": "Kat",
  "league_eyebrow": "Lig ve arkadaşlar", "league_h2": "Kat numaran, senin puanın.",
  "league_p": "Her hafta 30 kişilik bir ligdesin. Bu hafta geçtiğin katlar sıralamanı belirler; ilk yedi bir üst lige çıkar.",
  "tiers": ["Bronz", "Gümüş", "Altın", "Platin", "Elmas", "Usta", "Efsane"],
  "zone": "YÜKSELME BÖLGESİ · İLK 7", "you": "Sen", "kat": "kat",
  "rows": [("1", "Ece", "48"), ("2", "Sen", "41"), ("3", "Deniz", "37"), ("4", "Kerem", "33")],
  "features": [("daily", "#E3EEF9", "#2B5E8E", "Günün kulesi", "Herkese aynı on kat, üç deneme. Herkes arasında ve arkadaşların arasında kaçıncısın?"),
               ("season", "#E6D9F7", "#6A45B8", "Sezonlar", "Altı haftalık ödül yolu: tırmandıkça elmas, kostüm ve kule temaları kazan."),
               ("friends", "#DCEBD6", "#2E7D5B", "Arkadaşlar", "Davet kodunu paylaş, kulede kimin nerede olduğunu gör, geçince haberin olsun."),
               ("flame", "#FBE3D1", "#D9731F", "Günlük seri", "Her gün bir kat bile serini büyütür. Kaçırdığın gün için seri dondurucu var.")],
  "values_eyebrow": "Sakin ve adil", "values_h2": "Kafa dağıtmak için tasarlandı.",
  "values": [("check", "#DCEBD6", "#2E7D5B", "Her bulmacanın çözümü var", "Tahtalar üretilirken çözülerek doğrulanır; şansa değil hamlene bağlısın."),
             ("user", "#E3EEF9", "#2B5E8E", "Hesap gerekmez", "Hemen başla. İstersen Apple ile giriş yap; ilerlemen cihaz değiştirince de seninle gelir."),
             ("offline", "#FCEFCB", "#8A6400", "Çevrimdışı da oynanır", "Metroda, uçakta tırmanmaya devam et; katların bağlantı gelince eşitlenir."),
             ("eye", "#E6D9F7", "#6A45B8", "Renk körü dostu", "Her taş rengiyle birlikte bir şekil taşır: daire, kare, üçgen, yıldız…"),
             ("life", "#FBE3E3", "#E0565B", "Reklam senin seçimin", "Reklamlar yalnızca sen istediğinde: can ya da ek süre için. Araya giren reklam yok."),
             ("globe", "#E3EEF9", "#2B5E8E", "Altı dilde", "Türkçe, English, Deutsch, Français, Italiano, Español.")],
  "faq_eyebrow": "SSS", "faq_h2": "Sık sorulanlar",
  "faq": [("Zirve ücretsiz mi?", "Evet. İndirmek ve oynamak ücretsiz. Elmas paketleri ve sezonun premium ödül yolu isteğe bağlı uygulama içi satın almalardır; ödemeyi Apple alır."),
          ("Hangi cihazlarda oynanır?", "iOS 18 ve üzeri iPhone ve iPad'de. iPhone 11 ve sonrası desteklenir. Android sürümü şimdilik yok."),
          ("Hesap açmam gerekiyor mu?", "Hayır. İlk açılışta senin için otomatik bir misafir hesabı oluşur. İlerlemeni başka cihaza taşımak istersen Apple ile giriş yapabilirsin."),
          ("Canlarım bitince ne olur?", "Kampa dönersin ama rekorun silinmez. Canlar zamanla dolar; istersen reklam izleyerek ya da elmasla da doldurabilirsin."),
          ("Verilerim nasıl işleniyor?", "Yalnızca oyunun çalışması için gereken verileri işleriz; ayrıntılar <a href=\"{r}gizlilik/\">Gizlilik Politikası</a> ve <a href=\"{r}kvkk/\">KVKK Aydınlatma Metni</a>'nde."),
          ("Hesabımı nasıl silerim?", "Uygulamada Profil → Ayarlar → Hesap → Hesabı sil. Ayrıntılar <a href=\"{r}hesap-silme/\">Hesap silme</a> sayfasında.")],
  "cta_h2": "Zirvede görüşürüz.", "cta_p": "Zirve çok yakında App Store'da. İlk katlar seni bekliyor.",
  "footer_tag": "Kuleye tırman, her kat bir bulmaca.",
  "footer_links": [("gizlilik/", "Gizlilik"), ("kvkk/", "KVKK"), ("hesap-silme/", "Hesap silme"), ("destek/", "Destek")],
  "fine": "© 2026 Mehmet Mutlu · Zirve · Apple, App Store ve iPhone, Apple Inc.'in ticari markalarıdır. Bu sitede çerez ve izleme aracı kullanılmaz.",
  "back": "Ana sayfa",
},
"en": {
  "lang": "en", "other_lang": "tr", "other_label": "TR", "other_name": "Türkçe",
  "title": "Zirve · Climb the tower, every floor a puzzle",
  "desc": "Zirve is an endless tower of 30–60 second puzzles. Solve, climb a floor, pass your friends in the weekly league. For iPhone and iPad.",
  "nav": [("#how", "How to play"), ("#games", "Games"), ("#worlds", "Worlds"), ("#league", "League"), ("#faq", "FAQ")],
  "soon": "For iPhone and iPad · coming soon",
  "h1": "Climb the tower.<br><em>Every floor</em> a puzzle.",
  "lead": "Zirve is an endless tower of quick puzzles. Solve one, climb a floor, reach the next camp and pass your friends in the weekly league.",
  "badge_small": "Coming soon on the", "badge_big": "App Store", "how_btn": "How to play",
  "trust": ["Free", "No account needed", "Plays offline", "6 languages"],
  "f1": ("2 days", "streak"), "f2": ("Floor 6 cleared", ""), "f3": ("5/5", "lives"),
  "how_eyebrow": "How to play", "how_h2": "Under a minute. Understood in five seconds.",
  "how_p": "Every floor is a single puzzle. You get the rules at a glance; as you climb the board gets harder, not the clock.",
  "steps": [("Open your floor", "Tap Climb and meet the floor's puzzle: colours, paths, blocks or cards."),
            ("Solve before time runs out", "You have 30–60 seconds. Miss it by a hair and the board waits for you; take a breath and finish."),
            ("Climb to the next camp", "A camp waits every 10 floors. Even when your lives run out, your record stays.")],
  "games_eyebrow": "Games", "games_h2": "Eight puzzles, one tower.",
  "games_p": "Each floor brings a different game, and new ones unlock as you climb. Every board is solved by the computer before you see it: no unsolvable puzzles.",
  "games": [("colorMatch", "Colour match", "Drag matching tiles next to each other, merge them, clear the board."),
            ("pathDraw", "Path draw", "Pass the checkpoints and reach the flag without lifting your finger. Mind the walls."),
            ("blockFit", "Block fit", "Rotate the pieces and fit them into the gaps. Some need to be mirrored."),
            ("memory", "Memory", "Flip the cards and find the pairs. Triples wait higher up."),
            ("pipes", "Pipes", "Turn the pipes until the water flows from the source to the flag."),
            ("flow", "Flow", "Connect the matching ends; lines may never cross."),
            ("colorSort", "Colour sort", "Pour between tubes until every tube holds one colour."),
            ("lights", "Lights", "A tap flips the cell and its four neighbours. Light them all.")],
  "shots": [("play-path", "Path draw"), ("play-color", "Colour match"), ("play-blocks", "Block fit"), ("play-lights", "Lights")],
  "worlds_eyebrow": "Worlds", "worlds_h2": "Four worlds, a tower without an end.",
  "worlds_p": "Start in the forest, climb through the clouds into space and reach the crystal summit. Each world bends the rules a little more.",
  "worlds": [("forest", "Forest", "Floors 1–29"), ("clouds", "Clouds", "Floors 30–59"), ("space", "Space", "Floors 60–99"), ("crystal", "Crystal Summit", "Floor 100 and up")],
  "floor": "Floor",
  "league_eyebrow": "League and friends", "league_h2": "Your floor is your score.",
  "league_p": "Every week you join a league of 30 players. The floors you clear this week set your rank; the top seven move up a tier.",
  "tiers": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Legend"],
  "zone": "PROMOTION ZONE · TOP 7", "you": "You", "kat": "floors",
  "rows": [("1", "Ece", "48"), ("2", "You", "41"), ("3", "Deniz", "37"), ("4", "Kerem", "33")],
  "features": [("daily", "#E3EEF9", "#2B5E8E", "Tower of the day", "The same ten floors for everyone, three attempts. Where do you rank overall and among friends?"),
               ("season", "#E6D9F7", "#6A45B8", "Seasons", "A six-week reward track: earn gems, outfits and tower themes as you climb."),
               ("friends", "#DCEBD6", "#2E7D5B", "Friends", "Share your invite code, see where everyone is in the tower, get a heads-up when you pass them."),
               ("flame", "#FBE3D1", "#D9731F", "Daily streak", "One floor a day keeps the streak alive. A streak freeze covers a missed day.")],
  "values_eyebrow": "Calm and fair", "values_h2": "Made for a clear head.",
  "values": [("check", "#DCEBD6", "#2E7D5B", "Every puzzle has a solution", "Boards are solved as they are generated; it comes down to your moves, not luck."),
             ("user", "#E3EEF9", "#2B5E8E", "No account needed", "Start right away. Sign in with Apple if you like, and your progress follows you to a new device."),
             ("offline", "#FCEFCB", "#8A6400", "Plays offline", "Keep climbing on the train or a plane; your floors sync when you are back online."),
             ("eye", "#E6D9F7", "#6A45B8", "Colour-blind friendly", "Every tile carries a shape as well as a colour: circle, square, triangle, star…"),
             ("life", "#FBE3E3", "#E0565B", "Ads only when you choose", "Ads appear only when you ask for one: for a life or extra time. No interruptions."),
             ("globe", "#E3EEF9", "#2B5E8E", "Six languages", "Türkçe, English, Deutsch, Français, Italiano, Español.")],
  "faq_eyebrow": "FAQ", "faq_h2": "Questions",
  "faq": [("Is Zirve free?", "Yes. Downloading and playing are free. Gem packs and the season's premium reward track are optional in-app purchases, billed by Apple."),
          ("Which devices are supported?", "iPhone and iPad on iOS 18 or later, iPhone 11 and newer. There is no Android version for now."),
          ("Do I need an account?", "No. A guest account is created for you on first launch. To move your progress to another device, sign in with Apple."),
          ("What happens when I run out of lives?", "You return to camp, but your record stays. Lives refill over time; you can also refill by watching an ad or with gems."),
          ("How is my data handled?", "We only process what the game needs to work; see the <a href=\"{r}en/privacy/\">Privacy Policy</a>."),
          ("How do I delete my account?", "In the app: Profile → Settings → Account → Delete account. See <a href=\"{r}en/delete-account/\">Delete your account</a>.")],
  "cta_h2": "See you at the summit.", "cta_p": "Zirve is coming soon to the App Store. The first floors are waiting.",
  "footer_tag": "Climb the tower, every floor a puzzle.",
  "footer_links": [("en/privacy/", "Privacy"), ("en/delete-account/", "Delete account"), ("en/support/", "Support"), ("kvkk/", "KVKK (TR)")],
  "fine": "© 2026 Mehmet Mutlu · Zirve · Apple, App Store and iPhone are trademarks of Apple Inc. This site uses no cookies or trackers.",
  "back": "Home",
},
}

# ------------------------------------------------------------------------------------------- layout
def head(t, r, title, desc, canonical):
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#F4F6F1">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="https://mhmtmutlu.github.io/zirve-app/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{r}assets/icon-64.png" sizes="64x64" type="image/png">
<link rel="apple-touch-icon" href="{r}assets/icon-180.png">
<link rel="preload" href="{r}assets/fonts/Fredoka.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{r}assets/fonts/Nunito.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/site.css">
</head>
<body>
"""

def nav(t, r, home, links, other_href):
    items = "".join(f'<a href="{h}">{html.escape(l)}</a>' for h, l in links)
    return f"""<header class="nav"><div class="wrap">
  <a class="brand" href="{home}" aria-label="Zirve">{mascot()}<span>Zirve</span></a>
  <nav class="nav-links" aria-label="{'Bölümler' if t['lang']=='tr' else 'Sections'}">{items}</nav>
  <a class="lang" href="{other_href}" hreflang="{t['other_lang']}" lang="{t['other_lang']}" title="{t['other_name']}">{t['other_label']}</a>
</div></header>
"""

SCRIPT = """<script>
  // Header border after scrolling (progressive enhancement; the page works without it).
  (function () { var n = document.querySelector('.nav'); if (!n) return;
    var f = function () { n.classList.toggle('is-scrolled', window.scrollY > 8); }; f(); window.addEventListener('scroll', f, { passive: true }); })();
</script>
</body>
</html>
"""

def footer(t, r):
    links = "".join(f'<a href="{r}{h}">{html.escape(l)}</a>' for h, l in t["footer_links"])
    links += f'<a href="mailto:{CONTACT}">{CONTACT}</a>'
    return f"""<footer><div class="wrap">
  <div><a class="brand" href="{r}{'en/' if t['lang']=='en' else ''}" aria-label="Zirve">{mascot()}<span>Zirve</span></a><p style="margin:12px 0 0">{html.escape(t['footer_tag'])}</p></div>
  <nav aria-label="{'Bağlantılar' if t['lang']=='tr' else 'Links'}">{links}</nav>
  <p class="fine">{html.escape(t['fine'])}</p>
</div></footer>
""" + SCRIPT

def store_badge(t, cls=""):
    return (f'<a class="store-badge {cls}" aria-disabled="true" role="link" aria-label="{html.escape(t["badge_small"] + " " + t["badge_big"])}">'
            f'{APPLE}<span><small>{html.escape(t["badge_small"])}</small><b>{t["badge_big"]}</b></span></a>')

# ------------------------------------------------------------------------------------------- landing
def landing(lang):
    t = S[lang]
    r = "" if lang == "tr" else "../"
    ids = {"tr": ("nasil", "oyunlar", "dunyalar", "lig", "sss"), "en": ("how", "games", "worlds", "league", "faq")}[lang]
    canonical = "https://mhmtmutlu.github.io/zirve-app/" + ("" if lang == "tr" else "en/")
    out = head(t, r, t["title"], t["desc"], canonical)
    out += nav(t, r, "./", t["nav"], ("en/" if lang == "tr" else "../"))
    trust = "".join(f"<li>{I['check']}{html.escape(x)}</li>" for x in t["trust"])
    stars = "".join(f'<span style="color:#F2B531">{I["star"]}</span>' for _ in range(3))
    out += f"""<main>
<section class="hero"><div class="wrap">
  <div>
    <span class="chip-soon"><i></i>{html.escape(t['soon'])}</span>
    <h1>{t['h1']}</h1>
    <p class="lead">{html.escape(t['lead'])}</p>
    <div class="hero-cta">{store_badge(t)}<a class="btn btn-ghost" href="#{ids[0]}">{html.escape(t['how_btn'])}</a></div>
    <ul class="trust">{trust}</ul>
  </div>
  <div class="hero-art">
    <div class="phone"><img src="{r}assets/shots/tower-forest.webp" width="603" height="1311" alt="{'Zirve ana ekranı: orman temasında kule, kat 6' if lang=='tr' else 'Zirve home screen: the forest tower at floor 6'}"></div>
    <div class="float f1"><span style="color:#D9731F">{I['flame']}</span><span>{t['f1'][0]}<small>{t['f1'][1]}</small></span></div>
    <div class="float f2"><span class="stars">{stars}</span><span>{t['f2'][0]}</span></div>
    <div class="float f3"><span style="color:#E0565B">{I['life']}</span><span>{t['f3'][0]}<small>{t['f3'][1]}</small></span></div>
  </div>
</div></section>
"""
    steps = "".join(f'<div class="step"><div class="num">{i+1}</div><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>' for i, (h, p) in enumerate(t["steps"]))
    out += f"""<section id="{ids[0]}"><div class="wrap">
  <div class="section-head"><span class="eyebrow">{t['how_eyebrow']}</span><h2>{html.escape(t['how_h2'])}</h2><p>{html.escape(t['how_p'])}</p></div>
  <div class="steps">{steps}</div>
</div></section>
"""
    games = "".join(f'<article class="game"><div class="art">{G[k]}</div><h3>{html.escape(n)}</h3><p>{html.escape(d)}</p></article>' for k, n, d in t["games"])
    shots = "".join(f'<figure><div class="phone sm"><img src="{r}assets/shots/{f}.webp" width="603" height="1311" loading="lazy" alt="{html.escape(c)}"></div><figcaption>{html.escape(c)}</figcaption></figure>' for f, c in t["shots"])
    out += f"""<section id="{ids[1]}" style="background:#fff"><div class="wrap">
  <div class="section-head"><span class="eyebrow">{t['games_eyebrow']}</span><h2>{html.escape(t['games_h2'])}</h2><p>{html.escape(t['games_p'])}</p></div>
  <div class="games">{games}</div>
  <div class="shots">{shots}</div>
</div></section>
"""
    def world(key, name, floors):
        base = {"forest": 6, "clouds": 35, "space": 72, "crystal": 115}[key]
        rows = "".join(f'<span>{t["floor"]} {base + i}</span>' for i in (3, 2, 1))
        rows += f'<span class="you">{t["floor"]} {base}</span>'
        deco = {"forest": '<i class="deco" style="width:160px;height:120px;background:#A9CFA0;right:-50px;bottom:60px;opacity:.6"></i>',
                "clouds": '<i class="deco" style="width:170px;height:60px;background:#fff;right:-40px;bottom:90px;opacity:.9"></i><i class="deco" style="width:110px;height:44px;background:#fff;left:-30px;bottom:150px;opacity:.8"></i>',
                "space": '<i class="deco" style="width:120px;height:120px;background:#8C8FA6;right:-40px;bottom:70px;opacity:.55"></i><i class="deco" style="width:4px;height:4px;background:#FFF4C2;left:30%;bottom:120px"></i><i class="deco" style="width:3px;height:3px;background:#fff;left:70%;bottom:150px"></i>',
                "crystal": '<i class="deco" style="width:110px;height:110px;background:#B6E3EC;right:-30px;bottom:70px;border-radius:24px;transform:rotate(45deg);opacity:.8"></i>'}[key]
        return f'<article class="world {key}">{deco}<div class="rows" aria-hidden="true">{rows}</div><h3>{html.escape(name)}</h3><p>{html.escape(floors)}</p></article>'
    worlds = "".join(world(*w) for w in t["worlds"])
    out += f"""<section id="{ids[2]}"><div class="wrap">
  <div class="section-head"><span class="eyebrow">{t['worlds_eyebrow']}</span><h2>{html.escape(t['worlds_h2'])}</h2><p>{html.escape(t['worlds_p'])}</p></div>
  <div class="worlds">{worlds}</div>
  <div class="shots">""" + "".join(f'<figure><div class="phone sm"><img src="{r}assets/shots/{f}.webp" width="603" height="1311" loading="lazy" alt="{html.escape(c)}"></div><figcaption>{html.escape(c)}</figcaption></figure>'
                                 for f, c in [("tower-forest", t["worlds"][0][1]), ("tower-clouds", t["worlds"][1][1]), ("play-lights", t["worlds"][2][1]), ("tower-crystal", t["worlds"][3][1])]) + """</div>
</div></section>
"""
    tiers = "".join(f'<span class="{"on" if i == 0 else ""}"><i></i>{html.escape(n)}</span>' for i, n in enumerate(t["tiers"]))
    outfits = [("#2E7D5B", "#F08A3C", "#D9731F"), ("#2E7D5B", "#F08A3C", "#D9731F"), ("#E0A93A", "#E0A93A", "#B57F1A"), ("#2B5E8E", "#B6E3EC", "#6FA8DC")]
    rows = ""
    for (rank, name, score), (b, h, bd) in zip(t["rows"], [outfits[2], outfits[0], outfits[3], outfits[1]]):
        cls = "me" if name in ("Sen", "You") else "up"
        rows += f'<div class="row {cls}"><span class="rank">{rank}</span><span class="av">{mascot(b, h, bd)}</span><span>{html.escape(name)}</span><span class="score">{score} {t["kat"]}</span></div>'
    feats = "".join(f'<div class="feature"><span class="ic" style="background:{bg};color:{fg}">{I[ic]}</span><div><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div></div>' for ic, bg, fg, h, p in t["features"])
    out += f"""<section id="{ids[3]}" style="background:#fff"><div class="wrap league">
  <div class="board" role="img" aria-label="{'Örnek lig sıralaması' if lang=='tr' else 'Sample league standings'}">
    <div class="tiers">{tiers}</div>
    <div class="zone">↑ {t['zone']}</div>
    {rows}
  </div>
  <div>
    <div class="section-head" style="margin-bottom:0"><span class="eyebrow">{t['league_eyebrow']}</span><h2>{html.escape(t['league_h2'])}</h2><p>{html.escape(t['league_p'])}</p></div>
    <div class="features">{feats}</div>
  </div>
</div></section>
"""
    values = "".join(f'<div class="value"><span class="ic" style="background:{bg};color:{fg}">{I[ic]}</span><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>' for ic, bg, fg, h, p in t["values"])
    out += f"""<section><div class="wrap">
  <div class="section-head center"><span class="eyebrow">{t['values_eyebrow']}</span><h2>{html.escape(t['values_h2'])}</h2></div>
  <div class="values">{values}</div>
</div></section>
"""
    faq = "".join(f"<details><summary>{html.escape(q)}</summary><p>{a.format(r=r)}</p></details>" for q, a in t["faq"])
    out += f"""<section id="{ids[4]}" style="padding-top:0"><div class="wrap">
  <div class="section-head center"><span class="eyebrow">{t['faq_eyebrow']}</span><h2>{html.escape(t['faq_h2'])}</h2></div>
  <div class="faq">{faq}</div>
</div></section>
<div class="cta-band"><div class="wrap"><div class="cta-card">
  {mascot(cls="mascot")}
  <div><h2>{html.escape(t['cta_h2'])}</h2><p>{html.escape(t['cta_p'])}</p></div>
  {store_badge(t)}
</div></div></div>
</main>
"""
    out += footer(t, r)
    return out

# ------------------------------------------------------------------------------------------- documents
DOCS = [
    # (output dir, lang, source file, title, description)
    ("gizlilik", "tr", "privacy.tr.html", "Gizlilik Politikası · Zirve", "Zirve mobil oyununda kişisel verilerin nasıl işlendiği."),
    ("en/privacy", "en", "privacy.en.html", "Privacy Policy · Zirve", "How the Zirve mobile game processes personal data."),
    ("kvkk", "tr", "kvkk.tr.html", "KVKK Aydınlatma Metni · Zirve", "6698 sayılı Kanun m.10 kapsamında Zirve aydınlatma metni."),
    ("hesap-silme", "tr", "delete.tr.html", "Hesap Silme · Zirve", "Zirve hesabını ve oyun verilerini silme."),
    ("en/delete-account", "en", "delete.en.html", "Delete your account · Zirve", "How to delete your Zirve account and game data."),
    ("destek", "tr", "support.tr.html", "Destek · Zirve", "Zirve için yardım ve iletişim."),
    ("en/support", "en", "support.en.html", "Support · Zirve", "Help and contact for Zirve."),
]
OTHER = {"gizlilik": "en/privacy", "en/privacy": "gizlilik", "hesap-silme": "en/delete-account", "en/delete-account": "hesap-silme",
         "destek": "en/support", "en/support": "destek", "kvkk": "en/privacy"}

def document(out_dir, lang, src, title, desc):
    t = S[lang]
    depth = out_dir.count("/") + 1
    r = "../" * depth
    body = (SRC / src).read_text().replace("{{CONTACT}}", CONTACT).replace("{{UPDATED}}", UPDATED[lang]).replace("{{R}}", r)
    home = r + ("en/" if lang == "en" else "")
    page = head(t, r, title, desc, f"https://mhmtmutlu.github.io/zirve-app/{out_dir}/")
    page += nav(t, r, home, [(home, t["back"])], r + OTHER[out_dir] + "/")
    page += f'<main class="doc"><div class="wrap">{body}</div></main>\n'
    page += footer(t, r)
    return page

def build():
    written = []
    def write(rel, text):
        p = ROOT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text); written.append(rel)
    write("index.html", landing("tr"))
    write("en/index.html", landing("en"))
    for d in DOCS:
        write(f"{d[0]}/index.html", document(*d))
    nf = S["tr"]
    write("404.html", head(nf, "/zirve-app/", "Sayfa bulunamadı · Zirve", "Sayfa bulunamadı.", "https://mhmtmutlu.github.io/zirve-app/")
          + nav(nf, "/zirve-app/", "/zirve-app/", [], "/zirve-app/en/")
          + '<main class="doc"><div class="wrap" style="text-align:center;padding:60px 0"><h1>Bu kat boş.</h1><p class="meta" style="margin:14px 0 28px">Aradığın sayfa yok. / This page does not exist.</p>'
          + '<a class="btn btn-primary" href="/zirve-app/">Ana sayfa / Home</a></div></main>' + footer(nf, "/zirve-app/"))
    # Every relative link must resolve to a built file or an asset.
    missing = []
    for rel in written:
        page = (ROOT / rel).read_text()
        for href in re.findall(r'(?:href|src)="([^"#:]+?)"', page):
            if href.startswith("/zirve-app/") or href.startswith("mailto"):
                continue
            target = (ROOT / rel).parent / href
            if href.endswith("/"):
                target = target / "index.html"
            if not target.resolve().exists():
                missing.append((rel, href))
    print("built:", ", ".join(written))
    if missing:
        raise SystemExit(f"broken links: {missing}")
    print("links ok")

if __name__ == "__main__":
    build()
