#!/usr/bin/env python3
"""Builds the Zirve website (https://zirve.mm-apps.com) into static HTML in the repository root, then checks it.

    python3 build.py            # build + every check (exit 1 on an error; warnings are printed)
    python3 build.py --today 2026-11-12   # date used for changed pages (default: today)

Sources (README → "Yapı"):
    data/facts.json        single source of truth for facts + the release flag (`live`)
    data/site.json         base URL, contact, IndexNow key, trademark line
    data/lastmod.json      page content hash → last change date (written by the build)
    content/i18n/<l>.json  every string of the site per language ({value, state})
    src/<doc>.<l>.html     legal bodies (privacy, terms, kvkk, delete, support)
    LANGS (below)          languages: path prefix, html lang, hreflang, og:locale, App Store badge, published flag

Output: index pages, 404.html, robots.txt, sitemap.xml, llms.txt, <IndexNow key>.txt, assets/og/manifest.json.
Static and hosting-agnostic: no server headers are assumed (CSP and referrer policy are <meta>), links are
root-relative, canonical/hreflang/OG URLs absolute. No cookies, no analytics, no third-party requests.
The app repo (../zirve or $ZIRVE_APP_REPO) is read, when present, to check facts and in-app names.
"""
import argparse, datetime, gzip, hashlib, html, json, os, pathlib, re
from dataclasses import dataclass
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent
SRC, DATA, I18N = ROOT / "src", ROOT / "data", ROOT / "content" / "i18n"
SITE = json.loads((DATA / "site.json").read_text())
FACTS = json.loads((DATA / "facts.json").read_text())
BASE = SITE["baseUrl"].rstrip("/")
LIVE = FACTS["versions"][FACTS["live"]]
APP_STORE_URL = f"https://apps.apple.com/app/id{FACTS['appStoreId']}"


# ---------------------------------------------------------------------------------------------- languages
@dataclass(frozen=True)
class Lang:
    code: str          # content/i18n/<code>.json, src/<doc>.<code>.html, facts language codes
    prefix: str        # URL path prefix ("" = site root)
    html_lang: str     # <html lang>, BCP 47
    hreflang: tuple    # hreflang values pointing at this language's URL (pt-BR also answers for pt)
    og_locale: str
    badge: str         # assets/badges/app-store-<badge>.svg (Apple's own artwork; en-us where Apple has none)
    script: str        # latin | cjk | thai | cyrillic | vietnamese | devanagari (fonts, page budget)
    name: str          # the language's own name, shown in the language menu
    published: bool    # intent to publish; the build fails if a published language has missing strings


LANGS = (
    Lang("tr", "", "tr", ("tr",), "tr_TR", "tr-tr", "latin", "Türkçe", True),
    Lang("en", "en/", "en", ("en",), "en_US", "en-us", "latin", "English", True),
    Lang("de", "de/", "de", ("de",), "de_DE", "de-de", "latin", "Deutsch", False),
    Lang("fr", "fr/", "fr", ("fr",), "fr_FR", "fr-fr", "latin", "Français", False),
    Lang("it", "it/", "it", ("it",), "it_IT", "it-it", "latin", "Italiano", False),
    Lang("es", "es/", "es", ("es",), "es_ES", "es-es", "latin", "Español", False),
    Lang("ja", "ja/", "ja", ("ja",), "ja_JP", "ja-jp", "cjk", "日本語", False),
    Lang("ko", "ko/", "ko", ("ko",), "ko_KR", "ko-kr", "cjk", "한국어", False),
    Lang("zh-Hant", "zh-hant/", "zh-Hant", ("zh-Hant",), "zh_TW", "zh-tw", "cjk", "繁體中文", False),
    Lang("zh-Hans", "zh-hans/", "zh-Hans", ("zh-Hans",), "zh_CN", "zh-cn", "cjk", "简体中文", False),
    Lang("nl", "nl/", "nl", ("nl",), "nl_NL", "nl-nl", "latin", "Nederlands", False),
    Lang("pl", "pl/", "pl", ("pl",), "pl_PL", "pl-pl", "latin", "Polski", False),
    Lang("sv", "sv/", "sv", ("sv",), "sv_SE", "sv-se", "latin", "Svenska", False),
    Lang("th", "th/", "th", ("th",), "th_TH", "th-th", "thai", "ไทย", False),
    Lang("id", "id/", "id", ("id",), "id_ID", "id-id", "latin", "Bahasa Indonesia", False),
    Lang("uk", "uk/", "uk", ("uk",), "uk_UA", "en-us", "cyrillic", "Українська", False),
    Lang("ru", "ru/", "ru", ("ru",), "ru_RU", "ru-ru", "cyrillic", "Русский", False),
    # Not in the 1.1 app; kept so they can be switched on later (plan §4.2).
    Lang("pt-BR", "pt-br/", "pt-BR", ("pt-BR", "pt"), "pt_BR", "pt-br", "latin", "Português (Brasil)", False),
    Lang("vi", "vi/", "vi", ("vi",), "vi_VN", "vi-vn", "vietnamese", "Tiếng Việt", False),
    Lang("hi", "hi/", "hi", ("hi",), "hi_IN", "en-us", "devanagari", "हिन्दी", False),
)
LANG = {l.code: l for l in LANGS}
X_DEFAULT = "en"          # x-default → the English version when the page has one, else Turkish
SOURCE_LANG = "tr"        # tr.json defines the full key set

# Page table: slug per language (Turkish keeps its 1.0 slugs; other languages use English ASCII slugs).
PAGES = {
    "home":    {"tr": "", "*": ""},
    "daily":   {"tr": "daily/", "*": "daily/"},
    "privacy": {"tr": "gizlilik/", "*": "privacy/"},
    "terms":   {"tr": "kosullar/", "*": "terms/"},
    "kvkk":    {"tr": "kvkk/", "*": "kvkk/"},
    "delete":  {"tr": "hesap-silme/", "*": "delete-account/"},
    "support": {"tr": "destek/", "*": "support/"},
}
DOCS = ("privacy", "terms", "kvkk", "delete", "support")    # bodies in src/<doc>.<lang>.html
SMART_BANNER_ARG = {"daily": "zirve://daily"}               # apple-itunes-app app-argument per page


def page_path(page, lang):
    """URL path without the leading slash ("" for the Turkish home)."""
    slugs = PAGES[page]
    return LANG[lang].prefix + slugs.get(lang, slugs["*"])


def page_url(page, lang):
    return f"{BASE}/{page_path(page, lang)}"


# ---------------------------------------------------------------------------------------------- strings
class Strings:
    """content/i18n/<lang>.json. Values may be strings, lists or objects; strings are formatted with {placeholders}."""

    def __init__(self, code):
        self.code = code
        path = I18N / f"{code}.json"
        self.entries = json.loads(path.read_text())["strings"] if path.exists() else {}

    def raw(self, key):
        return self.entries[key]["value"]


STRINGS = {l.code: Strings(l.code) for l in LANGS}


def required_keys(code):
    """Keys a language needs: every key of tr.json except the strings of legal pages it has no body for."""
    keys = set(STRINGS[SOURCE_LANG].entries)
    for doc in DOCS:
        if not (SRC / f"{doc}.{code}.html").exists():
            keys = {k for k in keys if not k.startswith(f"doc.{doc}.")}
    return keys


def gate(code):
    """(missing keys, keys needing review) of a language."""
    s = STRINGS[code]
    missing = sorted(required_keys(code) - set(s.entries))
    review = sorted(k for k, e in s.entries.items() if e.get("state") != "translated")
    return missing, review


ACTIVE = [l.code for l in LANGS if l.published]


def doc_langs(page):
    """Languages a page is built in (published languages that have its content)."""
    if page in DOCS:
        return [c for c in ACTIVE if (SRC / f"{page}.{c}.html").exists()]
    return list(ACTIVE)


def fact_context(code):
    names = [LANG[c].name for c in LIVE["appLanguages"]]
    return {
        "puzzleTypes": len(FACTS["puzzleKinds"]),
        "worlds": FACTS["worlds"],
        "leagueSize": FACTS["league"]["size"],
        "leaguePromote": FACTS["league"]["promote"],
        "leagueRelegate": FACTS["league"]["relegate"],
        "leagueTiers": len(LIVE["leagueTiers"]),
        "dailyFloors": FACTS["dailyTower"]["floors"],
        "dailyAttempts": FACTS["dailyTower"]["attempts"],
        "appLanguageCount": len(names),
        "appLanguageNames": ", ".join(names),
        "storeName": FACTS["storeNames"].get(code, FACTS["storeNames"]["en"]),
        "year": SITE["copyrightYear"],
        "holder": SITE["copyrightHolder"],
    }


PLACEHOLDER = re.compile(r"\{([A-Za-z][A-Za-z0-9_]*(?::[a-z]+)?)\}")


class T:
    """Strings of one language, formatted for one page (links resolve per page)."""

    def __init__(self, code):
        self.code, self.lang = code, LANG[code]
        self.s = STRINGS[code]
        self.ctx = fact_context(code)

    def href(self, page):
        """Root-relative link to a page in this language, or in Turkish when it does not exist in this language."""
        lang = self.code if self.code in doc_langs(page) else SOURCE_LANG
        return "/" + page_path(page, lang)

    def fmt(self, value, **extra):
        if isinstance(value, str):
            def sub(m):
                name = m.group(1)
                if name.startswith("href:"):
                    return self.href(name[5:])
                if name in extra:
                    return str(extra[name])
                if name in self.ctx:
                    return str(self.ctx[name])
                raise KeyError(f"{self.code}: unknown placeholder {{{name}}}")
            return PLACEHOLDER.sub(sub, value)
        if isinstance(value, list):
            return [self.fmt(v, **extra) for v in value]
        if isinstance(value, dict):
            return {k: self.fmt(v, **extra) for k, v in value.items()}
        return value

    def __call__(self, key, **extra):
        return self.fmt(self.s.raw(key), **extra)

    def e(self, key, **extra):
        """HTML-escaped string."""
        return html.escape(self(key, **extra))

    def date(self, iso):
        d = datetime.date.fromisoformat(iso)
        return self("date.format", d=d.day, month=self.s.raw("date.months")[d.month - 1], y=d.year)


def requirement_met(item):
    req = item.get("requires") if isinstance(item, dict) else None
    return not req or bool(FACTS.get(req))


# Sentinels replaced once the page's content hash is known (data/lastmod.json).
LASTMOD_ISO, LASTMOD_HUMAN = "__LASTMOD_ISO__", "__LASTMOD_HUMAN__"


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
    "retry": icon(["M4 12a8 8 0 1 0 2.3-5.7", "M4 4v5h5"], width=2.4),
    "close": icon(["M6 6l12 12M18 6L6 18"], width=2.6),
    "offline": icon(["M2 8.5a15 15 0 0 1 6-3.2M12 12.5a7 7 0 0 1 4.5 1.6M9 16.5a3 3 0 0 1 3-.5", "M3 3l18 18"]),
    "eye": icon(["M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z", "M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"]),
    "globe": icon(["M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z", "M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"]),
    "user": icon(["M16 8a4 4 0 1 1-8 0 4 4 0 0 1 8 0z", "M4 21a8 8 0 0 1 16 0"]),
    "puzzle": icon(["M4 7h4a2 2 0 1 1 4 0h4v4a2 2 0 1 1 0 4v4H4z"]),
}

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
    "arrows": '<svg viewBox="0 0 76 76" aria-hidden="true"><g fill="none" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path d="M14 60V36h22" stroke="#F08A3C"/><path d="M50 62V22" stroke="#6FA8DC"/><path d="M20 16h30" stroke="#A58AE0"/></g><path d="M36 28l10 8-10 8z" fill="#F08A3C"/><path d="M42 24l8-12 8 12z" fill="#6FA8DC"/><path d="M50 8l12 8-12 8z" fill="#A58AE0"/></svg>',
    "gates": '<svg viewBox="0 0 76 76" aria-hidden="true"><rect x="4" y="4" width="68" height="68" rx="12" fill="#F4F6F1"/><rect x="10" y="14" width="34" height="14" rx="6" fill="#6FA8DC"/><rect x="50" y="10" width="14" height="34" rx="6" fill="#F08A3C"/><rect x="14" y="48" width="34" height="14" rx="6" fill="#7FB77E"/><rect x="0" y="16" width="5" height="10" rx="2.5" fill="#6FA8DC"/><rect x="52" y="71" width="10" height="5" rx="2.5" fill="#F08A3C"/><rect x="71" y="50" width="5" height="10" rx="2.5" fill="#7FB77E"/></svg>',
    "flags": '<svg viewBox="0 0 76 76" aria-hidden="true"><g><rect x="4" y="4" width="32" height="32" rx="9" fill="#DCEFD8"/><rect x="40" y="4" width="32" height="32" rx="9" fill="#D6E7F7"/><rect x="4" y="40" width="32" height="32" rx="9" fill="#FBE0CC"/><rect x="40" y="40" width="32" height="32" rx="9" fill="#E6DDF6"/></g><g transform="translate(8 6) scale(1)" fill="#2E7D5B"><path d="M12 1.5L18 8.6H6z"/><path d="M5.4 9.6h13.2v1.8H5.4z"/><path d="M7.4 12.2h9.2l.9 9.3H6.5z"/></g><g transform="translate(44 42)" fill="#2E7D5B"><path d="M12 1.5L18 8.6H6z"/><path d="M5.4 9.6h13.2v1.8H5.4z"/><path d="M7.4 12.2h9.2l.9 9.3H6.5z"/></g></svg>',
    "lights": '<svg viewBox="0 0 76 76" aria-hidden="true"><g fill="#F2B531"><rect x="2" y="2" width="22" height="22" rx="6"/><rect x="27" y="2" width="22" height="22" rx="6"/><rect x="52" y="27" width="22" height="22" rx="6"/><rect x="2" y="27" width="22" height="22" rx="6"/><rect x="27" y="52" width="22" height="22" rx="6"/></g><g fill="#F4F6F1" stroke="#E3E9E0" stroke-width="2"><rect x="52" y="2" width="22" height="22" rx="6"/><rect x="27" y="27" width="22" height="22" rx="6"/><rect x="2" y="52" width="22" height="22" rx="6"/><rect x="52" y="52" width="22" height="22" rx="6"/></g><g fill="#5A3E00"><circle cx="13" cy="13" r="4"/><circle cx="38" cy="13" r="4"/><circle cx="63" cy="38" r="4"/><circle cx="13" cy="38" r="4"/><circle cx="38" cy="63" r="4"/></g></svg>',
}

# ------------------------------------------------------------------------------------------- assets
def asset_version(rel):
    """Short content hash for cache busting (?v=…), so a changed file never hits a stale cache."""
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()[:10]


FONT_PRELOAD = ("assets/fonts/fredoka-latin.woff2", "assets/fonts/nunito-latin.woff2")
HERO = "tower-forest"
CSP = ("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
       "font-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'self'; form-action 'none'; "
       "upgrade-insecure-requests")


def badge_size(code):
    """Official badge rendered 48 px high (Apple: at least 40 px); width from the SVG's own aspect ratio."""
    svg = (ROOT / f"assets/badges/app-store-{LANG[code].badge}.svg").read_text()
    w, h = (float(x) for x in re.search(r'width="([\d.]+)" height="([\d.]+)"', svg).groups())
    return round(48 * w / h), 48


def badge(t, cls=""):
    w, h = badge_size(t.code)
    klass = f"store-badge {cls}".strip()
    return (f'<a class="{klass}" href="{APP_STORE_URL}"><img src="/assets/badges/app-store-{t.lang.badge}.svg" '
            f'width="{w}" height="{h}" alt="{t.e("badge.alt")}"></a>')


def og_image(code):
    """Localised OG card when it is rendered and current (assets/og/rendered.json), else the Turkish default."""
    path = f"assets/og/og-{code}.jpg"
    if (ROOT / path).exists() and og_fresh(code):
        return path
    return "assets/og.jpg"


def og_card(code):
    t = T(code)
    return {"file": f"assets/og/og-{code}.jpg", "line1": t("og.line1"), "line2": t("og.line2"), "subline": t("og.sub")}


def og_fresh(code):
    rendered = ROOT / "assets/og/rendered.json"
    if not rendered.exists():
        return False
    cards = {c["file"]: c for c in json.loads(rendered.read_text()).get("cards", [])}
    return cards.get(f"assets/og/og-{code}.jpg") == og_card(code)


# ------------------------------------------------------------------------------------------- JSON-LD
ORG_ID, SITE_ID, APP_ID = "https://mm-apps.com/#org", f"{BASE}/#site", f"{BASE}/#app"


def jsonld(nodes):
    data = {"@context": "https://schema.org", "@graph": nodes}
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return '<script type="application/ld+json">' + text.replace("</", "<\\/") + "</script>"


def common_nodes(t, url, title, desc, *, types="WebPage", crumbs=None, image=None, extra=None):
    page = {"@type": types, "@id": url + "#webpage", "url": url, "name": title, "description": desc,
            "inLanguage": t.lang.html_lang, "isPartOf": {"@id": SITE_ID}, "about": {"@id": APP_ID},
            "dateModified": LASTMOD_ISO}
    if image:
        page["primaryImageOfPage"] = {"@type": "ImageObject", "url": image}
    nodes = [
        {"@type": "Organization", "@id": ORG_ID, "name": FACTS["developer"], "url": SITE["developerUrl"]},
        {"@type": "WebSite", "@id": SITE_ID, "url": BASE + "/", "name": "Zirve",
         "inLanguage": [LANG[c].html_lang for c in ACTIVE], "publisher": {"@id": ORG_ID}},
        page,
    ]
    if crumbs:
        page["breadcrumb"] = {"@id": url + "#breadcrumb"}
        items = []
        for i, (name, link) in enumerate(crumbs, 1):
            item = {"@type": "ListItem", "position": i, "name": name}
            if link:
                item["item"] = link
            items.append(item)
        nodes.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": items})
    page.update(extra or {})
    return nodes


def app_node(t):
    """The app (VideoGame + MobileApplication), same @id in every language; honest fields only (plan §5.14 B)."""
    names = [FACTS["storeNames"][c] for c in LIVE["appLanguages"] if c in FACTS["storeNames"]]
    node = {
        "@type": ["VideoGame", "MobileApplication"], "@id": APP_ID, "name": "Zirve",
        "alternateName": list(dict.fromkeys(names)),
        "description": t("definition"),
        "url": page_url("home", t.code),
        "image": f"{BASE}/assets/icon-512.png",
        "screenshot": [f"{BASE}/assets/shots/{n}.webp" for n in ("tower-forest", "play-path", "play-color", "play-blocks", "play-arrows")],
        "applicationCategory": "GameApplication", "applicationSubCategory": "Puzzle",
        "operatingSystem": f"iOS {FACTS['minOS']} or later, iPadOS {FACTS['minOS']} or later",
        "gamePlatform": FACTS["platforms"], "genre": ["Puzzle", "Logic puzzle"], "playMode": "SinglePlayer",
        "inLanguage": LIVE["appLanguages"], "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "installUrl": APP_STORE_URL, "sameAs": [APP_STORE_URL, SITE["developerAppPage"]],
        "datePublished": FACTS["datePublished"], "softwareVersion": LIVE["softwareVersion"],
        "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID},
    }
    if FACTS["schemaAccessibilityFeature"]:
        node["accessibilityFeature"] = FACTS["schemaAccessibilityFeature"]
    if FACTS["ageRating"]:
        node["contentRating"] = FACTS["ageRating"]
    return node


# ------------------------------------------------------------------------------------------- layout
def head(t, page, title, desc, *, graph=None, noindex=False, preload=False):
    langs = doc_langs(page) if page else []
    url = page_url(page, t.code) if page else None
    out = [f'<!doctype html>\n<html lang="{t.lang.html_lang}">\n<head>\n<meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
           f"<title>{html.escape(title)}</title>",
           f'<meta name="description" content="{html.escape(desc)}">',
           f'<meta http-equiv="Content-Security-Policy" content="{CSP}">',
           '<meta name="referrer" content="strict-origin-when-cross-origin">',
           '<meta name="theme-color" content="#F4F6F1">']
    if noindex:
        out.append('<meta name="robots" content="noindex">')
    else:
        out.append(f'<meta http-equiv="content-language" content="{t.lang.html_lang}">')
        out.append(f'<link rel="canonical" href="{url}">')
        for c in langs:
            for code in LANG[c].hreflang:
                out.append(f'<link rel="alternate" hreflang="{code}" href="{page_url(page, c)}">')
        default = X_DEFAULT if X_DEFAULT in langs else SOURCE_LANG
        out.append(f'<link rel="alternate" hreflang="x-default" href="{page_url(page, default)}">')
    arg = SMART_BANNER_ARG.get(page)
    out.append(f'<meta name="apple-itunes-app" content="app-id={FACTS["appStoreId"]}' + (f', app-argument={arg}"' if arg else '"') + ">")
    og = og_image(t.code)
    out += ['<meta property="og:type" content="website">', '<meta property="og:site_name" content="Zirve">',
            f'<meta property="og:title" content="{html.escape(title)}">',
            f'<meta property="og:description" content="{html.escape(desc)}">',
            f'<meta property="og:locale" content="{t.lang.og_locale}">']
    if url:
        out.append(f'<meta property="og:url" content="{url}">')
    out += [f'<meta property="og:locale:alternate" content="{LANG[c].og_locale}">' for c in langs if c != t.code]
    out += [f'<meta property="og:image" content="{BASE}/{og}">', '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            f'<meta property="og:image:alt" content="{t.e("og.alt") if og.endswith(t.code + ".jpg") else html.escape(T(SOURCE_LANG)("og.alt"))}">',
            '<meta name="twitter:card" content="summary_large_image">',
            '<link rel="icon" href="/assets/icon-64.png" sizes="64x64" type="image/png">',
            '<link rel="apple-touch-icon" href="/assets/icon-180.png">']
    if preload and t.lang.script == "latin":
        out += [f'<link rel="preload" href="/{f}" as="font" type="font/woff2" crossorigin>' for f in FONT_PRELOAD]
    out += [f'<link rel="stylesheet" href="/assets/site.css?v={asset_version("assets/site.css")}">',
            f'<script src="/assets/site.js?v={asset_version("assets/site.js")}" defer></script>']
    if graph:
        out.append(jsonld(graph))
    out.append("</head>\n<body>")
    return "\n".join(out) + "\n"


def lang_menu(t, page):
    """<details> language menu (no JS needed). Each language links to this page in that language, or to its home."""
    available = doc_langs(page) if page else []
    items = []
    for c in ACTIVE:
        other = T(c)
        target = page if c in available else "home"
        current = ' aria-current="true"' if c == t.code else ""
        alt = ' data-alternate="1"' if target == page and c != t.code else ""
        items.append(f'<li><a href="/{page_path(target, c)}" hreflang="{LANG[c].html_lang}" lang="{LANG[c].html_lang}"{current}{alt}'
                     f' data-hint="{other.e("langhint.text")}" data-close="{other.e("langhint.close")}">{html.escape(LANG[c].name)}</a></li>')
    return (f'<details class="langs"><summary aria-label="{t.e("nav.language")}: {html.escape(t.lang.name)}">{I["globe"]}'
            f'<span>{html.escape(t.lang.html_lang if "-" in t.lang.html_lang else t.lang.html_lang.upper())}</span></summary><ul>{"".join(items)}</ul></details>')


def nav(t, page, links):
    home = t.href("home")
    items = "".join(f'<a href="{h}">{html.escape(l)}</a>' for h, l in links)
    menu = (f'<details class="menu"><summary>{t.e("nav.menu")}</summary><nav aria-label="{t.e("nav.sections")}">{items}</nav></details>'
            if links else "")
    return f"""<a class="skip" href="#main">{t.e("nav.skip")}</a>
<header class="nav"><div class="wrap">
  <a class="brand" href="{home}" aria-label="Zirve">{mascot()}<span>Zirve</span></a>
  <nav class="nav-links" aria-label="{t.e("nav.sections")}">{items}</nav>
  {menu}{lang_menu(t, page)}
</div></header>
"""


def footer(t):
    links = "".join(f'<a href="{t.href(p)}">{html.escape(l)}</a>' for p, l in t("footer.links"))
    links += f'<a href="mailto:{SITE["contact"]}">{SITE["contact"]}</a>'
    updated = t.e("footer.updated", date="\x00").replace("\x00", f'<time datetime="{LASTMOD_ISO}">{LASTMOD_HUMAN}</time>')
    return f"""<footer><div class="wrap">
  <div class="footer-brand"><a class="brand" href="{t.href("home")}" aria-label="Zirve">{mascot()}<span>Zirve</span></a><p class="tag">{t.e("footer.tag")}</p><p class="definition">{t.e("definition")}</p></div>
  <nav aria-label="{t.e("footer.links_label")}">{links}</nav>
  <p class="fine">{t.e("footer.fine")} · <a href="{SITE["developerAppPage"]}">{t.e("footer.by")}</a> · {updated}</p>
  <p class="fine" lang="en">{html.escape(SITE["trademarkLine"])}</p>
</div></footer>
</body>
</html>
"""


# ------------------------------------------------------------------------------------------- landing
WORLD_DECO = {
    "forest": '<i class="deco" style="width:160px;height:120px;background:#A9CFA0;right:-50px;bottom:60px;opacity:.6"></i>',
    # 16 zones since 31 Oct; the site shows four of them, the show growing with the climb.
    "dusk": '<i class="deco" style="width:130px;height:130px;background:#F28C38;right:-40px;bottom:50px;border-radius:50%;opacity:.8"></i><i class="deco" style="width:180px;height:30px;background:#FCE9D6;left:-30px;bottom:40px;opacity:.9"></i>',
    "lights": '<i class="deco" style="width:260px;height:60px;background:linear-gradient(90deg,transparent,#7FE0B0,transparent);left:-40px;top:30px;filter:blur(8px);opacity:.8"></i><i class="deco" style="width:240px;height:44px;background:linear-gradient(90deg,transparent,#A58AE0,transparent);right:-50px;top:90px;filter:blur(8px);opacity:.7"></i><i class="deco" style="width:3px;height:3px;background:#fff;left:70%;bottom:150px"></i>',
    "summit": '<i class="deco" style="width:220px;height:220px;background:radial-gradient(circle,#F5C542 0%,transparent 65%);left:50%;top:-110px;transform:translateX(-50%);opacity:.7"></i><i class="deco" style="width:46px;height:46px;background:#B6E3EC;right:16px;bottom:120px;border-radius:10px;transform:rotate(45deg);box-shadow:0 0 18px #B6E3EC;opacity:.9"></i><i class="deco" style="width:5px;height:5px;background:#FFF4C2;left:24%;bottom:150px;box-shadow:0 0 8px #F5C542"></i>',
}
WORLD_BASE = {"forest": 6, "dusk": 86, "lights": 146, "summit": 306}
UNLOCK = {k["id"]: k["unlockCamp"] for k in FACTS["puzzleKinds"]}


def hero_picture(alt):
    shots = "/assets/shots/" + HERO
    sizes = "(max-width: 900px) min(74vw, 290px), 330px"
    return (f'<picture><source type="image/avif" srcset="{shots}-320.avif 320w, {shots}.avif 603w" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{shots}-320.webp 320w, {shots}.webp 603w" sizes="{sizes}">'
            f'<img src="{shots}.webp" width="603" height="1311" fetchpriority="high" decoding="async" alt="{html.escape(alt)}"></picture>')


def landing(code):
    t = T(code)
    ids = [h[1:] for h, _ in t("home.nav")]
    title, desc = t("home.title"), t("home.desc")
    url = page_url("home", code)
    graph = common_nodes(t, url, title, desc, image=f"{BASE}/assets/shots/{HERO}.webp") + [app_node(t)]
    out = head(t, "home", title, desc, graph=graph, preload=True)
    out += nav(t, "home", t("home.nav"))
    trust = "".join(f"<li>{I['check']}{html.escape(x['text'])}</li>" for x in t("home.trust") if requirement_met(x))
    stars = "".join(f'<span class="star">{I["star"]}</span>' for _ in range(3))
    f1, f2, f3 = t("home.float")
    out += f"""<main id="main">
<section class="hero"><div class="wrap">
  <div>
    <span class="chip-soon"><i></i>{t.e('home.chip')}</span>
    <h1>{t('home.h1_html')}</h1>
    <p class="lead">{t.e('home.lead')}</p>
    <div class="hero-cta">{badge(t)}<a class="btn btn-ghost" href="#{ids[0]}">{t.e('home.how_btn')}</a></div>
    <ul class="trust">{trust}</ul>
  </div>
  <div class="hero-art">
    <div class="phone">{hero_picture(t('home.hero_alt'))}</div>
    <div class="float f1"><span class="ic-flame">{I['flame']}</span><span>{html.escape(f1[0])}<small>{html.escape(f1[1])}</small></span></div>
    <div class="float f2"><span class="stars">{stars}</span><span>{html.escape(f2[0])}</span></div>
    <div class="float f3"><span class="ic-life">{I['life']}</span><span>{html.escape(f3[0])}<small>{html.escape(f3[1])}</small></span></div>
  </div>
</div></section>
"""
    steps = "".join(f'<div class="step"><div class="num">{i+1}</div><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>'
                    for i, (h, p) in enumerate(t("home.steps")))
    out += f"""<section id="{ids[0]}"><div class="wrap">
  <div class="section-head"><span class="eyebrow">{t.e('home.how_eyebrow')}</span><h2>{t.e('home.how_h2')}</h2><p>{t.e('home.how_p')}</p></div>
  <div class="steps">{steps}</div>
</div></section>
"""

    def game(g):
        k = g["id"]
        name = t(f"game.name.{k}")
        how = "".join(f"<li>{html.escape(x)}</li>" for x in g["how"])
        more = "".join(f"<li>{html.escape(x)}</li>" for x in g["harder"])
        return (f'<article class="game" id="{k}"><div class="art">{G[k]}</div><div class="body">'
                f'<div class="game-head"><h3>{html.escape(name)}</h3><span class="unlock">{t.e("game.unlock", floor=UNLOCK[k] + 1)}</span></div>'
                f'<p class="goal">{html.escape(g["goal"])}</p>'
                f'<h4>{t.e("home.how_label")}</h4><ol>{how}</ol>'
                f'<h4>{t.e("home.harder_label")}</h4><ul>{more}</ul></div></article>')

    games = "".join(game(g) for g in t("home.games"))
    shot = lambda f, cap: (f'<figure><div class="phone sm"><img src="/assets/shots/{f}.webp" width="603" height="1311" loading="lazy" '
                           f'decoding="async" alt="{html.escape(cap)}"></div><figcaption>{html.escape(cap)}</figcaption></figure>')
    shots = "".join(shot(f, t(f"game.name.{k}")) for f, k in t("home.shots"))
    out += f"""<section id="{ids[1]}" class="white"><div class="wrap">
  <div class="section-head"><span class="eyebrow">{t.e('home.games_eyebrow')}</span><h2>{t.e('home.games_h2')}</h2><p>{t.e('home.games_p')}</p></div>
  <div class="games">{games}</div>
  <div class="shots">{shots}</div>
</div></section>
"""

    def world(key, name, floors):
        base = WORLD_BASE[key]
        rows = "".join(f'<span>{t.e("home.floor")} {base + i}</span>' for i in (3, 2, 1))
        rows += f'<span class="you">{t.e("home.floor")} {base}</span>'
        return (f'<article class="world {key}">{WORLD_DECO[key]}<div class="rows" aria-hidden="true">{rows}</div>'
                f'<h3>{html.escape(name)}</h3><p>{html.escape(floors)}</p></article>')

    worlds = t("home.worlds")
    world_shots = "".join(shot(f"tower-{w[0]}", w[1]) for w in worlds)
    out += f"""<section id="{ids[2]}"><div class="wrap">
  <div class="section-head"><span class="eyebrow">{t.e('home.worlds_eyebrow')}</span><h2>{t.e('home.worlds_h2')}</h2><p>{t.e('home.worlds_p')}</p></div>
  <div class="worlds">{"".join(world(*w) for w in worlds)}</div>
  <div class="shots">{world_shots}</div>
</div></section>
"""
    tiers = "".join(f'<span class="{"on" if i == 0 else ""}"><i></i>{t.e(f"tier.{tid}")}</span>' for i, tid in enumerate(LIVE["leagueTiers"]))
    outfits = [("#E0A93A", "#E0A93A", "#B57F1A"), ("#2E7D5B", "#F08A3C", "#D9731F"), ("#2B5E8E", "#B6E3EC", "#6FA8DC"), ("#2E7D5B", "#F08A3C", "#D9731F")]
    rows = ""
    for (rank, name, score), (b, h, bd) in zip(t("home.rows"), outfits):
        cls = "me" if name == t("home.you") else "up"
        rows += (f'<div class="row {cls}"><span class="rank">{rank}</span><span class="av">{mascot(b, h, bd)}</span>'
                 f'<span>{html.escape(name)}</span><span class="score">{t.e("home.score", n=score)}</span></div>')
    feats = "".join(f'<div class="feature"><span class="ic" style="background:{bg};color:{fg}">{I[ic]}</span><div><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div></div>'
                    for ic, bg, fg, h, p in t("home.features"))
    out += f"""<section id="{ids[3]}" class="white"><div class="wrap league">
  <div class="board" role="img" aria-label="{t.e('home.board_label')}">
    <div class="tiers">{tiers}</div>
    <div class="zone">↑ {t.e('home.zone')}</div>
    {rows}
  </div>
  <div>
    <div class="section-head flush"><span class="eyebrow">{t.e('home.league_eyebrow')}</span><h2>{t.e('home.league_h2')}</h2><p>{t.e('home.league_p')}</p></div>
    <div class="features">{feats}</div>
  </div>
</div></section>
"""
    values = "".join(f'<div class="value"><span class="ic" style="background:{v["bg"]};color:{v["fg"]}">{I[v["icon"]]}</span><h3>{html.escape(v["h"])}</h3><p>{html.escape(v["p"])}</p></div>'
                     for v in t("home.values") if requirement_met(v))
    out += f"""<section><div class="wrap">
  <div class="section-head center"><span class="eyebrow">{t.e('home.values_eyebrow')}</span><h2>{t.e('home.values_h2')}</h2></div>
  <div class="values">{values}</div>
</div></section>
"""
    faq = "".join(f"<details><summary>{html.escape(q)}</summary><p>{a}</p></details>" for q, a in t("home.faq_html"))
    out += f"""<section id="{ids[4]}" class="flush-top"><div class="wrap">
  <div class="section-head center"><span class="eyebrow">{t.e('home.faq_eyebrow')}</span><h2>{t.e('home.faq_h2')}</h2></div>
  <div class="faq">{faq}</div>
</div></section>
<div class="cta-band"><div class="wrap"><div class="cta-card">
  {mascot(cls="mascot")}
  <div><h2>{t.e('home.cta_h2')}</h2><p>{t.e('home.cta_p')}</p></div>
  {badge(t)}
</div></div></div>
</main>
"""
    return out + footer(t)


# ------------------------------------------------------------------------------------------- daily tower
# The page a shared daily result links to (the app's "Sonucu paylaş"). Tile colours and icons match the share card.
DAILY_SAMPLE = ["perfect", "perfect", "cleared", "perfect", "perfect", "cleared", "continued", "failed", None, None]
TILE_ICON = {"perfect": "star", "cleared": "check", "continued": "retry", "failed": "close"}


def tile(kind):
    return f'<span class="tile {kind or "unreached"}">{I[TILE_ICON[kind]] if kind in TILE_ICON else ""}</span>'


def daily(code):
    t = T(code)
    title, desc = t("daily.title"), t("daily.desc")
    url = page_url("daily", code)
    h1_text = re.sub(r"<[^>]+>", "", t("daily.h1_html"))
    graph = common_nodes(t, url, title, desc, crumbs=[("Zirve", page_url("home", code)), (h1_text, None)])
    out = head(t, "daily", title, desc, graph=graph, preload=True)
    out += nav(t, "daily", [(t.href("home"), t("nav.back"))])
    legend = "".join(f'<li>{tile(None if k == "unreached" else k)}<div><h3><span aria-hidden="true">{e}</span> {html.escape(h)}</h3><p>{html.escape(p)}</p></div></li>'
                     for k, e, h, p in t("daily.legend"))
    steps = "".join(f'<div class="step"><div class="num">{i+1}</div><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>'
                    for i, (h, p) in enumerate(t("daily.steps")))
    out += f"""<main id="main">
<section class="hero daily-hero"><div class="wrap">
  <div>
    <span class="chip-soon"><i></i>{t.e('daily.chip')}</span>
    <h1>{t('daily.h1_html')}</h1>
    <p class="lead">{t.e('daily.lead')}</p>
    <div class="hero-cta">{badge(t)}</div>
    <p class="store-note">{t.e('daily.note')}</p>
  </div>
  <div class="result-card" role="img" aria-label="{t.e('daily.card_label')}">
    <div class="result-head"><span class="brand">{mascot()}<span>Zirve</span></span><span class="result-day">{t.e('daily.card_title')}</span></div>
    <p class="result-score">7<small>/10</small></p>
    <p class="result-time">{I['clock']}{t.e('daily.card_time')}</p>
    <div class="result-grid">{"".join(tile(k) for k in DAILY_SAMPLE)}</div>
    <p class="result-try">{t.e('daily.card_try')}</p>
  </div>
</div></section>
<section class="white"><div class="wrap">
  <div class="section-head"><span class="eyebrow">{t.e('daily.grid_eyebrow')}</span><h2>{t.e('daily.grid_h2')}</h2><p>{t.e('daily.grid_p')}</p></div>
  <ul class="legend">{legend}</ul>
  <p class="legend-assist">{t.e('daily.assist')}</p>
</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">{t.e('daily.how_eyebrow')}</span><h2>{t.e('daily.how_h2')}</h2></div>
  <div class="steps">{steps}</div>
</div></section>
<div class="cta-band"><div class="wrap"><div class="cta-card">
  {mascot(cls="mascot")}
  <div><h2>{t.e('daily.cta_h2')}</h2><p>{t.e('daily.cta_p')}</p></div>
  {badge(t)}
</div></div></div>
</main>
"""
    return out + footer(t)


# ------------------------------------------------------------------------------------------- documents
def text_of(fragment):
    """Visible text of an inline HTML fragment (tags removed, entities decoded, spaces collapsed)."""
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", fragment)).split())


def faq_pairs(body):
    """Question/answer pairs of the support page: every <h3> followed by its <p> (FAQPage source, plan §5.7)."""
    return [(text_of(q), text_of(a)) for q, a in re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", body, re.S)]


def document(doc, code):
    t = T(code)
    body = ((SRC / f"{doc}.{code}.html").read_text().replace("{{CONTACT}}", SITE["contact"])
            .replace("{{UPDATED}}", t("legal.updated")).replace("{{R}}", "/"))
    title, desc = t(f"doc.{doc}.title"), t(f"doc.{doc}.desc")
    url = page_url(doc, code)
    h1 = text_of(re.search(r"<h1>(.*?)</h1>", body, re.S).group(1))
    extra, types = None, "WebPage"
    if doc == "support":
        pairs = faq_pairs(body)
        types = ["WebPage", "FAQPage"]
        extra = {"mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}
    graph = common_nodes(t, url, title, desc, types=types, crumbs=[("Zirve", page_url("home", code)), (h1, None)], extra=extra)
    page = head(t, doc, title, desc, graph=graph)
    page += nav(t, doc, [(t.href("home"), t("nav.back"))])
    page += f'<main id="main" class="doc"><div class="wrap">{body}</div></main>\n'
    return page + footer(t)


def not_found():
    """One page for every language (served for any missing path): noindex, no canonical, no hreflang (plan §5.13)."""
    t = T(SOURCE_LANG)
    lines = "".join(f'<li lang="{LANG[c].html_lang}"><span>{T(c).e("notfound.line")}</span> '
                    f'<a href="/{page_path("home", c)}">{T(c).e("notfound.home")}</a></li>' for c in ACTIVE)
    out = head(t, None, t("notfound.title"), t("notfound.line"), noindex=True)
    out += nav(t, None, [])
    out += (f'<main id="main" class="doc notfound"><div class="wrap"><h1>{t.e("notfound.h1")}</h1>'
            f'<ul class="notfound-list">{lines}</ul></div></main>\n')
    return out + footer(t)


# ------------------------------------------------------------------------------------------- root files
ROBOTS = """# Zirve: all crawlers welcome (search, user-initiated fetches and training)
User-agent: *
Allow: /

User-agent: Googlebot
User-agent: Bingbot
User-agent: Applebot
User-agent: Applebot-Extended
User-agent: Google-Extended
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: GPTBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: ClaudeBot
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: CCBot
Allow: /

Sitemap: {base}/sitemap.xml
"""


def sitemap(pages, lastmod):
    """Every indexable page with its real last change and its language alternates (xhtml:link)."""
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for page, code in pages:
        langs = doc_langs(page)
        out.append(f"  <url><loc>{page_url(page, code)}</loc><lastmod>{lastmod[page_path(page, code)]['date']}</lastmod>")
        for c in langs:
            for h in LANG[c].hreflang:
                out.append(f'    <xhtml:link rel="alternate" hreflang="{h}" href="{page_url(page, c)}"/>')
        default = X_DEFAULT if X_DEFAULT in langs else SOURCE_LANG
        out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url(page, default)}"/>')
        out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def llms_txt(lastmod):
    """/llms.txt (plan §6.6, speculative): English, generated from facts.json, no claim the pages do not make."""
    t = T("en")
    kinds = ", ".join(t(f"game.name.{k['id']}") for k in FACTS["puzzleKinds"])
    langs = ", ".join(LANG[c].name for c in LIVE["appLanguages"])
    tiers = len(LIVE["leagueTiers"])
    stores = {"CN": "mainland China", "BR": "Brazil", "RU": "Russia", "BY": "Belarus"}
    missing = ", ".join(stores[s] for s in FACTS["unavailableStorefronts"])
    updated = max(v["date"] for v in lastmod.values())
    pages = [("Home", "home"), ("Daily tower", "daily"), ("Support", "support"), ("Privacy policy", "privacy"),
             ("Terms of use", "terms"), ("Delete your account", "delete")]
    lines = ["# Zirve", "", f"> {t('definition')}", "",
             f"{FACTS['storeNames']['en']} is a free iPhone and iPad game by {FACTS['developer']} (Türkiye), released "
             f"{t.date(FACTS['datePublished'])}.", "", "## Facts",
             f"- Platforms: {', '.join(FACTS['platforms'])} (iOS/iPadOS {FACTS['minOS'].split('.')[0]} or later)",
             "- Price: free; optional gem packs",
             "- Ads: no forced or interstitial ads; rewarded ads only when the player chooses (lives, continue, double chest)",
             f"- Puzzle types: {len(FACTS['puzzleKinds'])} ({kinds})",
             f"- Modes: tower with camps every {FACTS['campEveryFloors']} floors; daily tower (same {FACTS['dailyTower']['floors']} floors "
             f"for everyone, {FACTS['dailyTower']['attempts']} tries); weekly leagues ({tiers} tiers)",
             f"- Accessibility labels declared on the App Store: {', '.join(FACTS['accessibilityLabels'])}",
             f"- Languages: {langs}",
             f"- Current version: {LIVE['softwareVersion']}",
             f"- Not available in: {missing} App Stores",
             f"- App Store: {APP_STORE_URL}",
             f"- Last updated: {updated}", "", "## Pages"]
    lines += [f"- [{name}]({page_url(p, 'en')})" for name, p in pages if "en" in doc_langs(p)]
    lines += ["", "## Other languages"]
    lines += [f"- {LANG[c].name}: {page_url('home', c)}" for c in ACTIVE if c != "en"]
    lines += ["", "## Optional", f"- [Developer]({SITE['developerUrl']})", ""]
    return "\n".join(lines)


# ------------------------------------------------------------------------------------------- build
def stamp(rel, text, code, lastmod, today):
    """Replaces the last-modified sentinels: the date only moves when the page's content hash changes."""
    content = re.sub(r"\?v=[0-9a-f]+", "", text)
    digest = hashlib.sha256(content.encode()).hexdigest()[:16]
    entry = lastmod.get(rel)
    if not entry or entry["hash"] != digest:
        entry = {"hash": digest, "date": today}
    lastmod[rel] = entry
    return text.replace(LASTMOD_ISO, entry["date"]).replace(LASTMOD_HUMAN, html.escape(T(code).date(entry["date"])))


def build(today):
    for code in ACTIVE:
        missing, review = gate(code)
        if missing or review:
            raise SystemExit(f"{code} is published but not ready: missing {missing[:8]}… review {review[:8]}")
    lastmod_path = DATA / "lastmod.json"
    old = json.loads(lastmod_path.read_text()) if lastmod_path.exists() else {}
    lastmod, written, pages = {}, [], []

    def write(rel, text):
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        written.append(rel)

    lastmod.update(old)
    for page in PAGES:
        for code in doc_langs(page):
            render = landing if page == "home" else daily if page == "daily" else (lambda c, d=page: document(d, c))
            text = render(code)
            path = page_path(page, code)
            write(path + "index.html", stamp(path, text, code, lastmod, today))
            pages.append((page, code))
    lastmod = {k: v for k, v in lastmod.items() if k in {page_path(p, c) for p, c in pages} | {"404.html"}}
    write("404.html", stamp("404.html", not_found(), SOURCE_LANG, lastmod, today))
    lastmod_path.write_text(json.dumps(lastmod, indent=1, sort_keys=True) + "\n")
    write("robots.txt", ROBOTS.format(base=BASE))
    write("sitemap.xml", sitemap(pages, lastmod))
    write("llms.txt", llms_txt(lastmod))
    write(f"{SITE['indexNowKey']}.txt", SITE["indexNowKey"])
    (ROOT / "assets/og").mkdir(exist_ok=True)
    cards = [og_card(c) for c in ACTIVE]
    # The Turkish card also replaces assets/og.jpg, the image every page used before (and social caches still hold).
    cards.append(dict(og_card(SOURCE_LANG), file="assets/og.jpg"))
    write("assets/og/manifest.json", json.dumps({"base": "assets-src/og-base.jpg", "cards": cards}, ensure_ascii=False, indent=1) + "\n")
    return written, pages, lastmod


# ------------------------------------------------------------------------------------------- checks
class Report:
    def __init__(self):
        self.errors, self.warnings, self.passed = [], [], []

    def check(self, name, problems, warn=False):
        (self.warnings if warn else self.errors).extend(f"{name}: {p}" for p in problems)
        if not problems:
            self.passed.append(name)


class Page(HTMLParser):
    """What the checks need from a built page."""
    SKIP = {"script", "style", "head", "title"}
    VOID = {"meta", "link", "img", "source", "br", "hr", "input", "wbr"}
    BLOCK = {"p", "div", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "section", "header", "footer", "nav", "main",
             "article", "details", "summary", "figure", "figcaption", "td", "th", "tr", "dt", "dd", "br", "table"}

    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.title = self.desc = self.canonical = self.robots = None
        self.alternates, self.jsonld, self.links, self.imgs, self.h1 = [], [], [], [], []
        self._stack, self._text, self._in_jsonld, self._in_h1, self._in_title = [], [], False, 0, False
        self.feed(text)
        self.text = " ".join("".join(self._text).split())

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in self.VOID:
            self._stack.append(tag)
        if tag in self.BLOCK:
            self._text.append(" ")
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        if tag == "meta" and a.get("name") == "robots":
            self.robots = a.get("content")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.alternates.append((a["hreflang"], a["href"]))
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_jsonld = True
            self.jsonld.append("")
        if tag in ("a", "link") and a.get("href"):
            self.links.append(a["href"])
        if tag in ("img", "script", "source") and (a.get("src") or a.get("srcset")):
            self.links += [s.split()[0] for s in (a.get("srcset") or a.get("src")).split(",")]
        if tag == "img":
            self.imgs.append(a)
        if tag == "h1":
            self._in_h1 += 1
            self.h1.append("")
        if tag == "title":
            self._in_title = True
            self.title = ""

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in self.BLOCK:
            self._text.append(" ")
        if self._stack and tag in self._stack:
            while self._stack.pop() != tag:
                pass
        if tag == "script":
            self._in_jsonld = False
        if tag == "h1":
            self._in_h1 -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_jsonld:
            self.jsonld[-1] += data
            return
        if self._in_title:
            self.title += data
            return
        if self._in_h1:
            self.h1[-1] += data
        if not any(t in self.SKIP for t in self._stack):
            self._text.append(data)


def norm(s):
    return " ".join((s or "").split())


BANNED = ["reklamsız", "no ads", "ad-free", "takip yok", "no tracking", "veri toplamıyoruz", "#1", "en iyi", "best",
          "Gehirnjogging", "치매", "dementia", "demans", "Alzheimer", "hafıza gelişir", "beyin geliştirir", "improves memory",
          "Wordle", "Flow Free", "Rush Hour", "Unblock Me", "LinkedIn", "Queens", "Block Blast", "Two Dots"]
BANNED_BARE = ["sans pub", "ohne Werbung"]     # banned unless qualified (plan §4.9 #7); flagged for a human look
BANNED_UNLESS = {"macVerified": ["Mac"],
                 "offlineVerified": ["offline", "internetsiz", "sin internet", "çevrimdışı", "hors ligne", "senza internet"]}


def banned_in(text):
    found = []
    phrases = BANNED + BANNED_BARE + [p for flag, ps in BANNED_UNLESS.items() if not FACTS.get(flag) for p in ps]
    for p in phrases:
        if re.search(r"(?<![\w#])" + re.escape(p) + r"(?!\w)", text, 0 if p == "Mac" else re.I):
            found.append(p)
    return found


def app_repo():
    path = pathlib.Path(os.environ.get("ZIRVE_APP_REPO", ROOT.parent / "zirve"))
    return path if (path / "Packages/ZirveCore").exists() else None


def xcstrings(path):
    data = json.loads(path.read_text())
    langs, values = set(), {}
    for key, entry in data["strings"].items():
        for lang, loc in entry.get("localizations", {}).items():
            langs.add(lang)
            unit = loc.get("stringUnit")
            if unit:
                values[(key, lang)] = unit["value"]
    return langs, values


def check_facts(report):
    """facts.json (and the in-app names in content/i18n) against the app repo; a mismatch fails the build."""
    repo = app_repo()
    if not repo:
        report.warnings.append("facts vs app repo: skipped (no ../zirve; set ZIRVE_APP_REPO)")
        return
    res = repo / "Packages/ZirveCore/Sources/ZirveCore/Resources"
    economy = json.loads((res / "economy.json").read_text())
    balance = json.loads((res / "balance.json").read_text())
    themes = json.loads((res / "themes.json").read_text())
    core = (repo / "Packages/ZirveCore/Sources/ZirveCore/Puzzles/PuzzleCore.swift").read_text()
    kinds = re.findall(r'public static let (\w+) = PuzzleKind\("(\w+)"\)', core)
    p = []
    site_kinds = [k["id"] for k in FACTS["puzzleKinds"]]
    if sorted(k for _, k in kinds) != sorted(site_kinds):
        p.append(f"puzzle kinds: app {sorted(k for _, k in kinds)} vs facts {sorted(site_kinds)}")
    unlocks = balance.get("unlocks", {})
    for k in FACTS["puzzleKinds"]:
        if unlocks.get(k["id"], 0) != k["unlockCamp"]:
            p.append(f"unlock camp of {k['id']}: app {unlocks.get(k['id'], 0)} vs facts {k['unlockCamp']}")
    if len(themes["themes"]) != FACTS["worlds"]:
        p.append(f"worlds: app {len(themes['themes'])} vs facts {FACTS['worlds']}")
    if economy["league"]["tiers"] != FACTS["versions"]["1.1"]["leagueTiers"]:
        p.append(f"league tiers (1.1): app {economy['league']['tiers']} vs facts")
    if FACTS["versions"]["1.1"]["leagueTiers"][:len(FACTS["versions"]["1.0"]["leagueTiers"])] != FACTS["versions"]["1.0"]["leagueTiers"]:
        p.append("league tiers: 1.0 tiers are not the first tiers of 1.1")
    for key in ("size", "promote", "relegate"):
        if economy["league"][key] != FACTS["league"][key]:
            p.append(f"league {key}: app {economy['league'][key]} vs facts {FACTS['league'][key]}")
    if economy["dailyTower"]["attempts"] != FACTS["dailyTower"]["attempts"]:
        p.append("daily attempts differ")
    if balance["dailyTower"]["floors"] != FACTS["dailyTower"]["floors"]:
        p.append("daily floors differ")
    if [r["floors"] for r in economy["dailyTower"]["rewards"]] != FACTS["dailyTower"]["rewardFloors"]:
        p.append("daily reward floors differ")
    if economy["camp"]["everyFloors"] != FACTS["campEveryFloors"]:
        p.append("camp interval differs")
    app_langs, app_strings = xcstrings(repo / "App/Resources/Localizable.xcstrings")
    if app_langs != set(FACTS["versions"]["1.1"]["appLanguages"]):
        p.append(f"app languages (1.1): app {sorted(app_langs)} vs facts {sorted(FACTS['versions']['1.1']['appLanguages'])}")
    unknown = set(FACTS["versions"]["1.1"]["appLanguages"]) - set(LANG)
    if unknown:
        p.append(f"app languages missing from LANGS: {sorted(unknown)}")
    _, design_strings = xcstrings(repo / "Packages/ZirveDesign/Sources/ZirveDesign/Resources/Localizable.xcstrings")
    for code, s in STRINGS.items():
        for key in s.entries:
            if key.startswith("game.name."):
                app = app_strings.get((key, code))
            elif key.startswith("tier."):
                app = design_strings.get((key, code))
            else:
                continue
            if app is not None and s.raw(key) != app:
                p.append(f"{code} {key}: site '{s.raw(key)}' vs app '{app}'")
    report.check("facts vs app repo", p)


def check_release_flag(report):
    p = []
    if FACTS["live"] not in FACTS["versions"]:
        p.append(f"live version {FACTS['live']} not in versions")
    elif not LIVE["releaseDate"]:
        p.append(f"live version {FACTS['live']} has no releaseDate")
    report.check("release flag", p)


FACT_NOUNS = r"(?:bulmaca|puzzles?|dil|dilde|languages?|dünya|worlds?|kademe|tiers?|kişilik|players)"


def check_strings(report):
    """Gate per language + facts written as placeholders, not literal numbers (plan §4.9 #3, #4)."""
    status, problems, literal = [], [], []
    for l in LANGS:
        if not STRINGS[l.code].entries:
            status.append(f"{l.code}: no strings (unpublished)")
            continue
        missing, review = gate(l.code)
        state = "ready" if not (missing or review) else f"{len(missing)} missing, {len(review)} needs_review"
        status.append(f"{l.code}: {state}{' (published)' if l.published else ' (unpublished)'}")
        if l.published and (missing or review):
            problems.append(f"{l.code} is published but {state}")
        for key, entry in STRINGS[l.code].entries.items():
            for s in json.dumps(entry["value"], ensure_ascii=False).split('"'):
                if re.search(r"\b\d+\s+" + FACT_NOUNS + r"\b", s, re.I):
                    literal.append(f"{l.code} {key}: '{s[:60]}'")
    report.check("language gate", problems)
    report.check("fact numbers as placeholders", literal)
    return status


def check_pages(report, written, pages):
    built = {}
    for rel in written:
        if rel.endswith(".html"):
            built[rel] = Page((ROOT / rel).read_text())
    url_of = lambda rel: BASE + "/" + rel[: -len("index.html")] if rel.endswith("index.html") else BASE + "/" + rel
    by_url = {url_of(rel): (rel, p) for rel, p in built.items()}

    # 1 canonical self, hreflang targets exist and the sets are identical across a group (reciprocal), x-default
    p = []
    for rel, page in built.items():
        if rel == "404.html":
            if page.canonical or page.alternates or page.robots != "noindex" or page.jsonld:
                p.append("404: needs noindex and no canonical, hreflang or JSON-LD")
            continue
        url = url_of(rel)
        if page.canonical != url:
            p.append(f"{rel}: canonical {page.canonical}")
        alts = set(page.alternates)
        if not any(h == "x-default" for h, _ in alts):
            p.append(f"{rel}: no x-default")
        if (page.canonical and not any(href == url for h, href in alts if h != "x-default")):
            p.append(f"{rel}: hreflang set does not include itself")
        for h, href in alts:
            if href not in by_url:
                p.append(f"{rel}: hreflang {h} → missing {href}")
            elif set(by_url[href][1].alternates) != alts:
                p.append(f"{rel}: hreflang set differs on {href}")
    report.check("canonical + hreflang reciprocity", p)

    # 2 sitemap == indexable files on disk
    sm = (ROOT / "sitemap.xml").read_text()
    sm_urls = set(re.findall(r"<loc>(.*?)</loc>", sm))
    files = {url_of(str(f.relative_to(ROOT))) for f in ROOT.rglob("index.html")
             if not any(part.startswith(".") or part in ("assets-src", "node_modules", "content", "data", "src") for part in f.relative_to(ROOT).parts)}
    noindex = {url_of(rel) for rel, pg in built.items() if pg.robots and "noindex" in pg.robots}
    p = [f"in sitemap, not a file: {u}" for u in sorted(sm_urls - files)]
    p += [f"file not in sitemap: {u}" for u in sorted(files - sm_urls)]
    p += [f"noindex page in sitemap: {u}" for u in sorted(sm_urls & noindex)]
    sm_alts = re.findall(r'hreflang="([^"]+)" href="([^"]+)"', sm)
    p += [f"sitemap alternate to missing page: {h} {u}" for h, u in sm_alts if u not in sm_urls]
    report.check("sitemap vs files", p)

    # 5 JSON-LD: valid JSON, one @graph, FAQPage only on support pages, texts visible on the page
    p = []
    support_urls = {page_url("support", c) for c in doc_langs("support")}
    for rel, page in built.items():
        if rel == "404.html":
            continue
        if len(page.jsonld) != 1:
            p.append(f"{rel}: {len(page.jsonld)} JSON-LD blocks")
            continue
        try:
            data = json.loads(page.jsonld[0])
        except json.JSONDecodeError as e:
            p.append(f"{rel}: invalid JSON-LD ({e})")
            continue
        nodes = data.get("@graph", [])
        if data.get("@context") != "https://schema.org" or not nodes:
            p.append(f"{rel}: no schema.org @graph")
        url = url_of(rel)
        visible = norm(page.text)
        for n in nodes:
            types = n["@type"] if isinstance(n["@type"], list) else [n["@type"]]
            if "FAQPage" in types and url not in support_urls:
                p.append(f"{rel}: FAQPage outside the support page")
            for bad in ("aggregateRating", "review", "award", "accessibilityHazard"):
                if bad in n:
                    p.append(f"{rel}: forbidden {bad}")
            if "WebPage" in types:
                if norm(n.get("name")) != norm(page.title):
                    p.append(f"{rel}: WebPage name ≠ <title>")
                if norm(n.get("description")) != norm(page.desc):
                    p.append(f"{rel}: WebPage description ≠ meta description")
                for q in n.get("mainEntity", []):
                    for txt in (q["name"], q["acceptedAnswer"]["text"]):
                        if norm(txt) not in visible:
                            p.append(f"{rel}: FAQ text not visible: {txt[:50]}")
            if "VideoGame" in types and norm(n["description"]) not in visible:
                p.append(f"{rel}: app description not visible")
            if "BreadcrumbList" in types:
                for item in n["itemListElement"]:
                    if norm(item["name"]) not in visible:
                        p.append(f"{rel}: breadcrumb '{item['name']}' not visible")
    report.check("JSON-LD syntax + visible text", p)

    # 6 links and images
    p = []
    for rel, page in built.items():
        base = (ROOT / rel).parent
        for href in page.links:
            if re.match(r"^(https?:|mailto:|#)", href):
                continue
            path = href.split("#")[0].split("?")[0]
            target = (ROOT / path.lstrip("/")) if path.startswith("/") else base / path
            if path.endswith("/") or target.is_dir():
                target = target / "index.html"
            if not target.exists():
                p.append(f"{rel}: broken link {href}")
        for img in page.imgs:
            if not img.get("alt") or not img.get("width") or not img.get("height"):
                p.append(f"{rel}: <img {img.get('src')}> needs alt, width and height")
        if len(page.h1) != 1:
            p.append(f"{rel}: {len(page.h1)} <h1>")
    report.check("links, images, single h1", p)

    # 7 banned phrases: title, H1 and URL fail; body and description warn
    errors, warnings = [], []
    allow = json.loads((DATA / "lint-allow.json").read_text()) if (DATA / "lint-allow.json").exists() else []
    allowed = {(a["page"], a["phrase"]) for a in allow}
    for rel, page in built.items():
        for where, text in (("title", page.title), ("h1", " ".join(page.h1)), ("url", rel)):
            errors += [f"{rel} {where}: '{w}'" for w in banned_in(text or "")]
        for where, text in (("description", page.desc), ("body", page.text)):
            warnings += [f"{rel} {where}: '{w}'" for w in banned_in(text or "") if (rel, w) not in allowed]
    report.check("banned phrases in title/H1/URL", errors)
    report.check("banned phrases in body (human review)", warnings, warn=True)

    # 8 first-view budget (gzip): HTML + CSS + JS + preloaded fonts + hero + badge
    p = []
    css = len(gzip.compress((ROOT / "assets/site.css").read_bytes()))
    js = len(gzip.compress((ROOT / "assets/site.js").read_bytes()))
    fonts = sum((ROOT / f).stat().st_size for f in FONT_PRELOAD)
    sizes = []
    for page, code in pages:
        if page not in ("home", "daily"):
            continue
        rel = page_path(page, code) + "index.html"
        total = len(gzip.compress((ROOT / rel).read_bytes())) + css + js
        total += len(gzip.compress((ROOT / f"assets/badges/app-store-{LANG[code].badge}.svg").read_bytes()))
        if LANG[code].script == "latin":
            total += fonts
        if page == "home":
            total += (ROOT / f"assets/shots/{HERO}.avif").stat().st_size
        limit = 100 if LANG[code].script in ("latin", "cyrillic", "vietnamese") else 60
        sizes.append(f"{rel} {total // 1024} KB")
        if total > limit * 1024:
            p.append(f"{rel}: first view {total // 1024} KB > {limit} KB")
    report.check("first-view budget", p, warn=True)

    # OG cards current
    p = [f"assets/og/og-{c}.jpg missing or out of date (run scripts/og.swift; falling back to assets/og.jpg)" for c in ACTIVE if not og_fresh(c)]
    report.check("OG images current", p, warn=True)
    return sizes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--today", default=datetime.date.today().isoformat(), help="date for pages whose content changed")
    args = ap.parse_args()
    report = Report()
    status = check_strings(report)
    if report.errors:
        print("\n".join(report.errors))
        raise SystemExit(1)
    written, pages, _ = build(args.today)
    check_release_flag(report)
    check_facts(report)
    sizes = check_pages(report, written, pages)
    print(f"live version {FACTS['live']} · published: {', '.join(ACTIVE)} · {len(pages)} pages + 404")
    print("languages: " + "; ".join(status))
    print("first view: " + "; ".join(sizes))
    print("passed: " + ", ".join(report.passed))
    for w in report.warnings:
        print("WARN  " + w)
    for e in report.errors:
        print("ERROR " + e)
    if report.errors:
        raise SystemExit(1)
    print("all checks passed" + (f" ({len(report.warnings)} warnings)" if report.warnings else ""))


if __name__ == "__main__":
    main()
