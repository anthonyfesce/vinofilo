#!/usr/bin/env python3
"""Generatore statico di Vinofilo.

Sorgenti: content/articles/*.md (italiano; front matter: date, number, title, description, category, slug)
          content/i18n/<lingua>/<slug-italiano>.md (traduzioni: title, description, slug, cover + testo)
          lingue.py (testi fissi del sito in ogni lingua)
Output: italiano alla radice (index.html, articles/AAAA.MM.GG/slug/, categoria/<cat>/, privacy/),
        le altre lingue in /<lingua>/... ; sitemap.xml con hreflang, robots.txt, 404.html.
Gli articoli con data futura non vengono pubblicati (servono per la programmazione).
"""
import datetime as dt, hashlib, html, json, os, re, shutil, sys
import markdown
from zoneinfo import ZoneInfo
from lingue import L, ORDINE, ATTIVE, fmt_date, prefix

# "Oggi" sempre nel fuso italiano (anche quando gira su GitHub Actions, che è in UTC).
TODAY = (dt.date.fromisoformat(os.environ["VINOFILO_TODAY"]) if os.environ.get("VINOFILO_TODAY")
         else dt.datetime.now(ZoneInfo("Europe/Rome")).date())
# Dagli articoli in scorta in poi, si esce solo con l'illustrazione pronta.
AUTO_FROM = dt.date(2026, 10, 7)

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://vinofilo.com"
NAME = "Vinofilo"
GA_ID = "G-H26K5NGH04"  # ID di misurazione GA4 (G-XXXXXXXXXX). Vuoto = niente statistiche e niente banner.
CATS = {  # categoria (chiave italiana): (colore, testo)
    "Vitigni": ("#7E1C2B", "#FBF3E4"),
    "Territori": ("#2F5D50", "#F4EDE1"),
    "Tecnica": ("#E9B44C", "#1B1416"),
    "Servizio": ("#E07254", "#1B1416"),
    "Guide": ("#1F2E47", "#F4EDE1"),
}
CAT_IMG = {"Vitigni": "vitigni-dimenticati-che-tornano", "Territori": "chianti-e-chianti-classico",
           "Tecnica": "barrique-botte-cemento-acciaio", "Servizio": "forma-del-calice",
           "Guide": "vino-al-ristorante-carta-dei-vini"}  # immagine scelta per ogni tema in "Esplora per tema"
FONTS = '<link rel="stylesheet" href="/assets/fonts/fonts.css">'
AVAIL = ["it"]  # lingue effettivamente pubblicate (riempita da build())

def slugify(s):
    s = s.lower()
    for a, b in (("à","a"),("è","e"),("é","e"),("ì","i"),("ò","o"),("ù","u")): s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def esc(s): return html.escape(s, quote=True)

def jsonstr(s): return json.dumps(s, ensure_ascii=False)

def read_md(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
    if not m: sys.exit(f"Front matter mancante in {path}")
    meta = {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)}
    return meta, m.group(2).strip()

def ver(rel):
    """?v=<hash del file>: quando un'immagine cambia, cambia l'indirizzo e i browser non usano la copia vecchia."""
    with open(os.path.join(ROOT, rel), "rb") as f:
        return rel + "?v=" + hashlib.md5(f.read()).hexdigest()[:8]

def img_path(key):
    for ext in ("webp", "jpg", "png"):
        rel = f"assets/img/{key}.{ext}"
        if os.path.exists(os.path.join(ROOT, rel)):
            return "/" + ver(rel)
    return None

# ---------------------------------------------------------------- articoli

def load():
    """Articoli italiani pubblicabili oggi, dal più recente."""
    arts = []
    for fn in sorted(os.listdir(os.path.join(ROOT, "content/articles"))):
        if not fn.endswith(".md"): continue
        meta, body = read_md(os.path.join(ROOT, "content/articles", fn))
        for k in ("date", "title", "description", "category", "slug"):
            if not meta.get(k): sys.exit(f"Campo '{k}' mancante in {fn}")
        if meta["category"] not in CATS: sys.exit(f"Categoria sconosciuta in {fn}: {meta['category']}")
        d = dt.date.fromisoformat(meta["date"])
        arts.append(dict(meta, d=d, body=body, words=len(body.split()), key=meta["slug"], lang="it",
                         url=f"/articles/{d:%Y.%m.%d}/{meta['slug']}/",
                         number=int(meta.get("number", 0) or 0)))
    live = []
    for a in arts:
        if a["d"] > TODAY: continue  # data futura: resta in scorta, nessuna pagina né sitemap
        if a["d"] >= AUTO_FROM and not img_path(a["key"]):
            print(f"ATTENZIONE: {a['key']} ({a['d']}) non ha ancora l'illustrazione: rimandato", file=sys.stderr)
            continue
        live.append(a)
    live.sort(key=lambda a: (-a["d"].toordinal(), a["number"]))
    return live

def translate(arts, lg):
    """Versione degli articoli nella lingua lg: solo quelli con traduzione in content/i18n/<lg>/."""
    out, d = [], os.path.join(ROOT, "content/i18n", lg)
    for a in arts:
        p = os.path.join(d, a["key"] + ".md")
        if not os.path.exists(p): continue
        meta, body = read_md(p)
        for k in ("title", "description", "slug"):
            if not meta.get(k): sys.exit(f"Campo '{k}' mancante in {p}")
        t = dict(a, title=meta["title"], description=meta["description"], cover=meta.get("cover", a.get("cover", "")),
                 slug=meta["slug"], body=body, lang=lg, quote=meta.get("quote", ""), alt=meta.get("alt", ""),
                 url=f"{prefix(lg)}/articles/{a['d']:%Y.%m.%d}/{meta['slug']}/")
        t.pop("former", None)
        out.append(t)
    return out

NUMERI = [  # (slug, numero, didascalia): cifre già verificate negli articoli. La home ne mostra 4 a rotazione.
    ("nebbiolo-vitigno-piu-difficile", "1268", "L'anno della prima menzione documentata di un vino chiamato «nibiol», vicino a Torino"),
    ("nebbiolo-vitigno-piu-difficile", "38", "I mesi minimi di invecchiamento prima che un Barolo possa uscire, di cui 18 in legno"),
    ("nebbiolo-vitigno-piu-difficile", "1980", "L'anno delle prime DOCG italiane: Barolo, Barbaresco, Brunello e Nobile di Montepulciano"),
    ("etna-vulcano-del-vino", "142", "Le contrade dell'Etna che si possono citare in etichetta, dopo la nuova mappa del 2022"),
    ("etna-vulcano-del-vino", "1968", "L'anno in cui l'Etna diventò la prima DOC della Sicilia"),
    ("metodo-classico-charmat", "60", "I mesi minimi sui lieviti per un Franciacorta Riserva"),
    ("metodo-classico-charmat", "1895", "L'anno in cui Federico Martinotti descrisse la rifermentazione in grandi recipienti"),
    ("metodo-classico-charmat", "1993", "L'anno di nascita del Trento DOC, prima denominazione italiana riservata al metodo classico"),
    ("vini-orange", "2013", "L'anno in cui l'UNESCO ha riconosciuto la vinificazione georgiana in qvevri"),
    ("vini-orange", "1995", "L'anno in cui Stanko Radikon tornò a macerare la Ribolla sulle bucce"),
    ("amarone-appassimento", "14%", "Il titolo alcolometrico minimo dell'Amarone della Valpolicella"),
    ("leggere-etichetta-vino", "85%", "La quota minima di vino dell'annata dichiarata per i vini a denominazione"),
    ("leggere-etichetta-vino", "2023", "Da dicembre di quell'anno ingredienti e valori nutrizionali entrano nell'etichetta del vino"),
    ("temperatura-di-servizio", "6–10°", "La forchetta di temperatura per servire spumanti e Champagne"),
    ("cantina-in-casa", "12–14°", "La temperatura di cantina citata più spesso come ideale"),
    ("forma-del-calice", "1901", "L'anno delle misure di Hänig da cui nacque, per equivoco, la mappa della lingua"),
]

def numeri(lg):
    """Didascalie dei NUMERI nella lingua lg (content/i18n/<lg>/_numeri.json: "slug|numero" -> testo)."""
    if lg == "it": return NUMERI
    p = os.path.join(ROOT, "content/i18n", lg, "_numeri.json")
    tr = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    return [(s, n, tr[f"{s}|{n}"]) for s, n, _ in NUMERI if f"{s}|{n}" in tr]

# ---------------------------------------------------------------- pezzi di pagina

def cat_name(lg, c): return L[lg]["cats"][c][0]
def cat_desc(lg, c): return L[lg]["cats"][c][1]
def cat_url(lg, c): return f"{prefix(lg)}/{L[lg]['cat_dir']}/{L[lg]['cats'][c][2]}/"

def img(a, cls="", ar=None):
    """Illustrazione dell'articolo (assets/img/<slug-italiano>.jpg|.webp|.png) o segnaposto colorato."""
    bg, fg = CATS[a["category"]]
    style = f"--c:{bg};--fg:{fg}" + (f";--ar:{ar}" if ar else "")
    src = img_path(a["key"])
    if src:
        return (f'<div class="ph {cls}" style="{style}"><img src="{src}" alt="{esc(a.get("alt") or a["title"])}" '
                f'loading="lazy" decoding="async"></div>')
    name = a.get("cover") or a["title"]
    word = re.split(r"['’]", name.split()[-1])[-1]
    return f'<div class="ph {cls}" style="{style}" aria-hidden="true"><span class="ini">{esc(word[0].upper())}</span></div>'

def page(lg, title, desc, path, content, active="", og_type="website", extra_head="", image=None, alts=None):
    t = L[lg]
    image = image or img_path("og-vinofilo")
    og_img = (f'<meta property="og:image" content="{SITE}{image}"><meta property="og:image:width" content="1536">'
              f'<meta property="og:image:height" content="1024"><meta name="twitter:card" content="summary_large_image">'
              f'<meta name="twitter:image" content="{SITE}{image}">') if image else ""
    alts = alts or {lg: path}
    hreflang = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{u}">' for l, u in alts.items())
    if "it" in alts: hreflang += f'<link rel="alternate" hreflang="x-default" href="{SITE}{alts["it"]}">'
    nav = "".join(f'<a href="{cat_url(lg, c)}"{" class=on" if c == active else ""}>{esc(cat_name(lg, c))}</a>' for c in CATS)
    links = [(l, alts.get(l, prefix(l) + "/")) for l in AVAIL]
    # Menu a tendina in testata (regge molte lingue) + elenco completo e discreto nel piè di pagina.
    opts = "".join(f'<li><a href="{u}" hreflang="{l}" lang="{l}"{" aria-current=true class=on" if l == lg else ""}>{L[l]["name"]}</a></li>'
                   for l, u in links)
    langbar = (f'<details class="langsel"><summary aria-label="{esc(t["languages"])}">{L[lg]["name"]}</summary>'
               f'<ul>{opts}</ul></details>') if len(AVAIL) > 1 else ""
    langfoot = (f'<nav class="langs foot" aria-label="{esc(t["languages"])}">' +
                "".join(f'<a href="{u}" hreflang="{l}" lang="{l}"{" class=on" if l == lg else ""}>{L[l]["name"]}</a>' for l, u in links)
                + '</nav>') if len(AVAIL) > 1 else ""
    home = prefix(lg) + "/"
    canon = SITE + path
    full_title = title if title == NAME else f"{title} — {NAME}"
    consenso = (f'<script src="/{ver("assets/consenso.js")}" data-ga="{GA_ID}" data-t="{esc(t["banner"])}" data-ok="{esc(t["accept"])}" '
                f'data-no="{esc(t["reject"])}" data-p="{esc(t["privacy"])}" data-pu="{prefix(lg)}/privacy/" defer></script>') if GA_ID else ""
    pref = f' · <a href="#" onclick="vfPreferenzeCookie();return false">{esc(t["cookie_prefs"])}</a>' if GA_ID else ""
    return f"""<!doctype html>
<html lang="{lg}" dir="{t['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
{hreflang}
<meta property="og:type" content="{og_type}"><meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}">
<meta property="og:site_name" content="{NAME}"><meta property="og:locale" content="{t['locale']}">
{og_img}
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="robots" content="max-image-preview:large">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="/{ver("assets/style.css")}">
{extra_head}
{consenso}
</head>
<body>
<header class="masthead"><div class="wrap">
{langbar}
<a href="{home}" class="wordmark">VINOFILO</a><p class="tagline">{esc(t['tagline'])}</p>
</div></header>
<div class="wrap"><nav class="nav">{nav}</nav></div>
<main>
{content}
</main>
<footer><div class="wrap"><a href="{home}" class="wordmark">VINOFILO</a><p>{esc(t['tagline'])} · © {TODAY.year} · <a href="{prefix(lg)}/privacy/">{esc(t['privacy'])}</a>{pref}</p>
{langfoot}</div></footer>
</body>
</html>
"""

def kick(lg, a, date=True):
    return f'<div class="kick">{esc(cat_name(lg, a["category"]))}' + (f' <span>· {fmt_date(lg, a["d"])}</span>' if date else "") + '</div>'

def card(lg, a, desc=True):
    d = f'<p>{esc(a["description"])}</p>' if desc else ""
    return f'<a class="card" href="{a["url"]}">{img(a)}{kick(lg, a)}<h3>{esc(a["title"])}</h3>{d}</a>'

def circle(lg, a):
    sub = a.get("tagline") or a["description"]
    return (f'<a href="{a["url"]}">{img(a, "circle")}<h3>{esc(re.split(r"[:：]", a["title"])[0])}</h3>'
            f'<p>{esc(sub)}</p><div class="tags">{esc(L[lg]["in_cat"])} <b>{esc(cat_name(lg, a["category"]))}</b></div></a>')

def sect(title, sub="", link=None, lg="it"):
    l = f'<a href="{link}">{esc(L[lg]["see_all"])}</a>' if link else ""
    s = f'<p class="sect-sub">{esc(sub)}</p>' if sub else ""
    return f'<div class="sect"><h2>{esc(title)}</h2>{l}</div>{s}'

def write(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)

def short_title(a):
    return a.get("cover") or re.split(r"[:：,，]", a["title"])[0]

# ---------------------------------------------------------------- generazione

def build_lang(lg, arts, alt_art, md, sitemap):
    t, P = L[lg], prefix(lg)
    mins = lambda a: max(1, round(a["words"] / 220))

    # Articoli
    for a in arts:
        if lg == "it":  # vecchi indirizzi (articolo spostato di data): pagina di rimando verso quello nuovo
            for old in filter(None, (u.strip() for u in a.get("former", "").split(","))):
                new = SITE + a["url"]
                write(old.strip("/") + "/index.html",
                      f'<!doctype html><html lang="it"><head><meta charset="utf-8"><title>{esc(a["title"])}</title>'
                      f'<link rel="canonical" href="{new}"><meta name="robots" content="noindex">'
                      f'<meta http-equiv="refresh" content="0; url={a["url"]}"></head>'
                      f'<body><p><a href="{a["url"]}">{esc(a["title"])}</a></p></body></html>\n')
        md.reset()
        body = md.convert(a["body"])
        body = re.sub(r"(\w)‘(\d)", r"\1’\2", body)  # l’80%, non l‘80%
        rel = [x for x in arts if x is not a and x["category"] == a["category"]][:3]
        rel += [x for x in arts if x is not a and x not in rel][:3 - len(rel)]
        im = img_path(a["key"])
        ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article",'
              f'"headline":{jsonstr(a["title"])},"description":{jsonstr(a["description"])},'
              f'"datePublished":"{a["d"].isoformat()}","inLanguage":"{lg}","mainEntityOfPage":"{SITE}{a["url"]}",'
              f'"publisher":{{"@type":"Organization","name":"{NAME}"}}'
              + (f',"image":"{SITE}{im}"' if im else "") + '}</script>')
        content = f"""<article>
<header class="art-head"><div class="kick"><a href="{cat_url(lg, a['category'])}">{esc(cat_name(lg, a['category']))}</a></div>
<h1>{esc(a['title'])}</h1><p class="standfirst">{esc(a['description'])}</p>
<div class="byline">{fmt_date(lg, a['d'])} · {t['read_time'].format(n=mins(a))}</div></header>
<div class="art-cover">{img(a)}</div>
<div class="body">{body}<p class="fin">❦</p></div>
</article>
<section class="wrap related">{sect(t['more'], lg=lg)}<div class="row3">{''.join(card(lg, x) for x in rel)}</div></section>"""
        alts = alt_art[a["key"]]
        write(a["url"].strip("/") + "/index.html",
              page(lg, a["title"], a["description"], a["url"], content, a["category"], "article", ld, im, alts))
        sitemap.append((a["url"], a["d"], alts))

    # Home
    lead, side, rest = arts[0], arts[1:4], arts[4:]
    circ, rest = rest[:6], rest[6:]
    row, rest = rest[:4], rest[4:]
    q = next((a for a in arts if a.get("quote")), arts[min(3, len(arts) - 1)])
    qtext = q.get("quote") or q["description"]
    side_html = "".join(f'<a href="{a["url"]}">{img(a) if i == 0 else ""}{kick(lg, a, False)}'
                        f'<h3>{esc(a["title"])}</h3><div class="meta">{fmt_date(lg, a["d"])}</div></a>' for i, a in enumerate(side))
    home = f"""<div class="wrap">
<section class="hero"><a class="hero-main" href="{lead['url']}">{img(lead, ar="3/2")}
<div class="kick" style="margin-top:18px">{esc(cat_name(lg, lead['category']))} <span>· {fmt_date(lg, lead['d'])}</span></div>
<h2>{esc(lead['title'])}</h2><p>{esc(lead['description'])}</p></a>
<div class="side-list">{side_html}</div></section>"""
    if circ:
        home += sect(t["selection"], t["selection_sub"]) + f'<div class="circles">{"".join(circle(lg, a) for a in circ)}</div>'
    home += "</div>"
    home += f'<section class="quote"><div class="wrap"><p>“{esc(qtext)}”</p><a href="{q["url"]}">{esc(q["title"])} →</a></div></section>'
    home += '<div class="wrap">'
    pool = [a for a in arts if a not in [lead] + side]
    if len(pool) >= 4:  # seconda apertura, specchiata: la lettura più lunga
        lead2 = max(pool, key=lambda a: a["words"])
        side2 = [a for a in pool if a is not lead2][-3:]
        side2_html = "".join(f'<a href="{a["url"]}">{img(a) if i == 0 else ""}{kick(lg, a, False)}'
                             f'<h3>{esc(a["title"])}</h3><div class="meta">{fmt_date(lg, a["d"])}</div></a>' for i, a in enumerate(side2))
        home += f"""<section class="hero rev">
<div class="side-list">{side2_html}</div>
<a class="hero-main" href="{lead2['url']}">{img(lead2, ar="3/2")}
<div class="kick" style="margin-top:18px">{esc(t['long_read'])} <span>· {esc(cat_name(lg, lead2['category']))} · {t['minutes'].format(n=mins(lead2))}</span></div>
<h2>{esc(lead2['title'])}</h2><p>{esc(lead2['description'])}</p></a></section>"""
    by = {a["key"]: a for a in arts}
    pool_n = [{"u": by[sl]["url"], "n": n, "t": tx} for sl, n, tx in numeri(lg) if sl in by]
    if len(pool_n) >= 4:
        first, used = [], set()
        for x in pool_n:
            if x["u"] not in used: first.append(x); used.add(x["u"])
            if len(first) == 4: break
        rd = t["read"]
        cells = "".join(f'<a href="{x["u"]}"><b>{esc(x["n"])}</b><p>{esc(x["t"])}</p><span>{esc(rd)}</span></a>' for x in first)
        data = json.dumps(pool_n, ensure_ascii=False).replace("</", "<\\/")
        home += sect(t["numbers"], t["numbers_sub"]) + f'<div class="nums" id="nums">{cells}</div>' + (
            '<script>(function(){var P=' + data + ',R=' + jsonstr(rd) + ';var o=[],u={};P.sort(function(){return Math.random()-.5});'
            'for(var i=0;i<P.length&&o.length<4;i++){if(!u[P[i].u]){u[P[i].u]=1;o.push(P[i])}}'
            'var e=function(s){return s.replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c]})};'
            'document.getElementById("nums").innerHTML=o.map(function(x){return\'<a href="\'+x.u+\'"><b>\'+e(x.n)+\'</b><p>\'+e(x.t)+\'</p><span>\'+e(R)+\'</span></a>\'}).join("")})();</script>')
    if row:
        home += sect(t["latest"], t["latest_sub"]) + f'<div class="row4">{"".join(card(lg, a, False) for a in row)}</div>'
    counts = {c: sum(1 for a in arts if a["category"] == c) for c in CATS}
    shown = set(re.findall(r'href="([^"]*/articles/[^"]+)"', home))
    def cat_pick(c):  # immagine scelta; se manca, l'articolo più recente non già visibile in home
        its = [a for a in arts if a["category"] == c]
        fav = next((a for a in its if a["key"] == CAT_IMG.get(c)), None)
        return fav or (next((a for a in its if a["url"] not in shown), its[0]) if its else None)
    rows = ""
    for i, c in enumerate(CATS, 1):
        its = [a for a in arts if a["category"] == c]
        a = cat_pick(c)
        tit = "".join(f'<li>{esc(short_title(x))}</li>' for x in its[:3])
        rows += (f'<a class="ix" href="{cat_url(lg, c)}"><span class="ix-n">{i:02d}</span>{img(a, "ix-ph", "1/1") if a else ""}'
                 f'<div class="ix-m"><h3>{esc(cat_name(lg, c))}</h3><p>{esc(cat_desc(lg, c))}</p></div><ul class="ix-l">{tit}</ul>'
                 f'<span class="ix-c">{esc(t["n_articles"].format(n=counts[c]))} {"‹" if t["dir"] == "rtl" else "›"}</span></a>')
    home += sect(t["explore"], t["explore_sub"]) + f'<div class="idx" id="esplora">{rows}</div></div>'
    home_alts = {l: prefix(l) + "/" for l in ORDINE if alt_art.get("__home__", {}).get(l)}
    write((P.strip("/") + "/index.html").lstrip("/"), page(lg, NAME, t["home_desc"], P + "/", home, alts=home_alts))
    sitemap.append((P + "/", arts[0]["d"], home_alts))

    # Categorie
    cat_alts = {c: {l: cat_url(l, c) for l in home_alts} for c in CATS}
    for c in CATS:
        items = [a for a in arts if a["category"] == c]
        inner = "".join(card(lg, a) for a in items) or f"<p>{esc(t['coming'])}</p>"
        content = (f'<div class="wrap"><div class="cat-head"><div class="kick">{esc(cat_desc(lg, c))}</div><h1>{esc(cat_name(lg, c))}</h1></div>'
                   f'{sect(t["n_articles"].format(n=len(items)))}<div class="row3">{inner}</div></div>')
        u = cat_url(lg, c)
        write(u.strip("/") + "/index.html",
              page(lg, cat_name(lg, c), t["cat_desc"].format(cat=cat_name(lg, c), desc=cat_desc(lg, c)), u, content, c, alts=cat_alts[c]))
        sitemap.append((u, None, cat_alts[c]))

    # Pagine statiche (privacy ecc.): italiano in content/pagine/, traduzioni in content/i18n/<lg>/pagine/
    pdir = os.path.join(ROOT, "content/pagine") if lg == "it" else os.path.join(ROOT, "content/i18n", lg, "pagine")
    for fn in sorted(os.listdir(pdir)) if os.path.isdir(pdir) else []:
        if not fn.endswith(".md"): continue
        meta, txt = read_md(os.path.join(pdir, fn))
        keep, drop = ("ga", "noga") if GA_ID else ("noga", "ga")
        txt = re.sub(rf"<!--{drop}-->.*?<!--/{drop}-->\n?", "", txt, flags=re.S)
        txt = re.sub(rf"<!--/?{keep}-->\n?", "", txt)
        md.reset()
        body = md.convert(txt)
        path = f"{P}/{meta['slug']}/"
        palts = {l: f"{prefix(l)}/{meta['slug']}/" for l in ORDINE
                 if l == "it" or os.path.exists(os.path.join(ROOT, "content/i18n", l, "pagine", fn))}
        content = (f'<article><header class="art-head"><h1>{esc(meta["title"])}</h1></header>'
                   f'<div class="body page">{body}</div></article>')
        if lg == "it": shutil.rmtree(os.path.join(ROOT, meta["slug"]), ignore_errors=True)
        write(path.strip("/") + "/index.html", page(lg, meta["title"], meta["description"], path, content, alts=palts))
        sitemap.append((path, None, palts))

def build():
    base = load()
    if not base: sys.exit("Nessun articolo pubblicabile")
    by_lang = {"it": base}
    for lg in ORDINE[1:]:
        if lg not in ATTIVE: continue
        tr = translate(base, lg)
        if tr: by_lang[lg] = tr
    # mappa delle versioni di ogni articolo: chiave italiana -> {lingua: url}
    alt_art = {a["key"]: {} for a in base}
    for lg in ORDINE:
        for a in by_lang.get(lg, []): alt_art[a["key"]][lg] = a["url"]
    alt_art["__home__"] = {lg: True for lg in by_lang}
    AVAIL[:] = [lg for lg in ORDINE if lg in by_lang]
    if os.environ.get("DEMO_TUTTE_LINGUE"): AVAIL[:] = ORDINE  # solo per le anteprime

    # pulizia output generato
    for d in ("articles", "categoria"):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)
    for lg in ORDINE[1:]:
        shutil.rmtree(os.path.join(ROOT, lg), ignore_errors=True)

    md = markdown.Markdown(extensions=["extra", "smarty"], extension_configs={"smarty": {"substitutions": {
        "left-double-quote": "“", "right-double-quote": "”", "left-single-quote": "‘", "right-single-quote": "’"}}})
    sitemap = []
    for lg in ORDINE:
        if lg in by_lang:
            build_lang(lg, by_lang[lg], alt_art, md, sitemap)

    # 404, sitemap (con hreflang), robots
    t = L["it"]
    write("404.html", page("it", t["nf_title"], t["nf_title"] + ".", "/404.html",
          f'<div class="wrap"><div class="nf"><b>{t["nf_big"]}</b><h1>{t["nf_h1"]}</h1><p class="standfirst">{t["nf_text"]}</p>'
          f'<a href="/">{t["nf_back"]}</a></div></div>'))
    def url_xml(u, d, alts):
        x = f"<url><loc>{SITE}{u}</loc>" + (f"<lastmod>{d.isoformat()}</lastmod>" if d else "")
        if len(alts) > 1:
            x += "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{v}"/>' for l, v in alts.items())
            if "it" in alts: x += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{alts["it"]}"/>'
        return x + "</url>"
    sm = "".join(url_xml(*s) for s in sitemap)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          f'xmlns:xhtml="http://www.w3.org/1999/xhtml">{sm}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print(f"OK: {len(base)} articoli pubblicati; lingue: " + ", ".join(f"{lg} {len(v)}" for lg, v in by_lang.items()))

if __name__ == "__main__":
    build()
