#!/usr/bin/env python3
"""Generatore statico di Vinofilo.

Sorgenti: content/articles/*.md (front matter: date, number, title, description, category, slug)
Output: index.html, articles/AAAA.MM.GG/slug/index.html, categoria/<cat>/index.html,
        sitemap.xml, robots.txt, 404.html — direttamente nella radice del repository.
Gli articoli con data futura non vengono pubblicati (servono per la programmazione).
"""
import datetime as dt, hashlib, html, json, os, re, shutil, sys
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://vinofilo.com"
NAME = "Vinofilo"
TAGLINE = "Storie, territori e tecnica del vino"
GA_ID = "G-H26K5NGH04"  # ID di misurazione GA4 (G-XXXXXXXXXX). Vuoto = niente statistiche e niente banner.
MESI = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
CATS = {  # categoria: (colore, testo, descrizione)
    "Vitigni": ("#7E1C2B", "#FBF3E4", "Le uve e il loro carattere"),
    "Territori": ("#2F5D50", "#F4EDE1", "Dove nasce il vino"),
    "Tecnica": ("#E9B44C", "#1B1416", "Come si fa, davvero"),
    "Servizio": ("#E07254", "#1B1416", "Bicchieri, gradi, decanter"),
    "Guide": ("#1F2E47", "#F4EDE1", "Per orientarsi"),
}
FONTS = '<link rel="stylesheet" href="/assets/fonts/fonts.css">'

def slugify(s):
    s = s.lower()
    for a, b in (("à","a"),("è","e"),("é","e"),("ì","i"),("ò","o"),("ù","u")): s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def esc(s): return html.escape(s, quote=True)

def load():
    arts = []
    for fn in sorted(os.listdir(os.path.join(ROOT, "content/articles"))):
        if not fn.endswith(".md"): continue
        raw = open(os.path.join(ROOT, "content/articles", fn), encoding="utf-8").read()
        m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
        if not m: sys.exit(f"Front matter mancante in {fn}")
        meta = dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        for k in ("date", "title", "description", "category", "slug"):
            if not meta.get(k): sys.exit(f"Campo '{k}' mancante in {fn}")
        if meta["category"] not in CATS: sys.exit(f"Categoria sconosciuta in {fn}: {meta['category']}")
        d = dt.date.fromisoformat(meta["date"])
        body = m.group(2).strip()
        arts.append(dict(meta, d=d, body=body, words=len(body.split()),
                         url=f"/articles/{d:%Y.%m.%d}/{meta['slug']}/",
                         number=int(meta.get("number", 0) or 0)))
    today = dt.date.fromisoformat(os.environ["VINOFILO_TODAY"]) if os.environ.get("VINOFILO_TODAY") else dt.date.today()
    live = [a for a in arts if a["d"] <= today]
    live.sort(key=lambda a: (-a["d"].toordinal(), a["number"]))
    return live

def itdate(d): return f"{d.day} {MESI[d.month-1]} {d.year}"

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

def ver(rel):
    """?v=<hash del file>: quando un'immagine cambia, cambia l'indirizzo e i browser non usano la copia vecchia."""
    with open(os.path.join(ROOT, rel), "rb") as f:
        return rel + "?v=" + hashlib.md5(f.read()).hexdigest()[:8]

def img(a, cls="", ar=None):
    """Illustrazione dell'articolo (assets/img/<slug>.jpg|.webp|.png) o segnaposto colorato."""
    bg, fg, _ = CATS[a["category"]]
    style = f"--c:{bg};--fg:{fg}" + (f";--ar:{ar}" if ar else "")
    for ext in ("webp", "jpg", "png"):
        rel = f"assets/img/{a['slug']}.{ext}"
        if os.path.exists(os.path.join(ROOT, rel)):
            return (f'<div class="ph {cls}" style="{style}"><img src="/{ver(rel)}" alt="{esc(a.get("alt") or a["title"])}" '
                    f'loading="lazy" decoding="async"></div>')
    name = a.get("cover") or a["title"]
    word = re.split(r"['’]", name.split()[-1])[-1]
    return f'<div class="ph {cls}" style="{style}" aria-hidden="true"><span class="ini">{esc(word[0].upper())}</span></div>'

def img_path(slug):
    for ext in ("webp", "jpg", "png"):
        rel = f"assets/img/{slug}.{ext}"
        if os.path.exists(os.path.join(ROOT, rel)):
            return "/" + ver(rel)
    return None

CONSENSO = f'<script src="/assets/consenso.js" data-ga="{GA_ID}" defer></script>' if GA_ID else ""
PREF = ' · <a href="#" onclick="vfPreferenzeCookie();return false">Preferenze cookie</a>' if GA_ID else ""

def page(title, desc, path, content, active="", og_type="website", extra_head="", image=None):
    image = image or img_path("og-vinofilo")
    og_img = (f'<meta property="og:image" content="{SITE}{image}"><meta property="og:image:width" content="1536">'
              f'<meta property="og:image:height" content="1024"><meta name="twitter:card" content="summary_large_image">'
              f'<meta name="twitter:image" content="{SITE}{image}">') if image else ""
    nav = "".join(f'<a href="/categoria/{slugify(c)}/"{" class=on" if c == active else ""}>{c}</a>' for c in CATS)
    canon = SITE + path
    full_title = title if title == NAME else f"{title} — {NAME}"
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="{og_type}"><meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}">
<meta property="og:site_name" content="{NAME}"><meta property="og:locale" content="it_IT">
{og_img}
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="/{ver("assets/style.css")}">
{extra_head}
{CONSENSO}
</head>
<body>
<header class="masthead"><div class="wrap">
<a href="/" class="wordmark">VINOFILO</a><p class="tagline">{TAGLINE}</p>
</div></header>
<div class="wrap"><nav class="nav">{nav}</nav></div>
<main>
{content}
</main>
<footer><div class="wrap"><a href="/" class="wordmark">VINOFILO</a><p>{TAGLINE} · © {dt.date.today().year} · <a href="/privacy/">Privacy e cookie</a>{PREF}</p></div></footer>
</body>
</html>
"""

def card(a, desc=True):
    d = f'<p>{esc(a["description"])}</p>' if desc else ""
    return (f'<a class="card" href="{a["url"]}">{img(a)}<div class="kick">{esc(a["category"])} <span>· {itdate(a["d"])}</span></div>'
            f'<h3>{esc(a["title"])}</h3>{d}</a>')

def circle(a):
    sub = a.get("tagline") or a["description"]
    return (f'<a href="{a["url"]}">{img(a, "circle")}<h3>{esc(a["title"].split(":")[0])}</h3>'
            f'<p>{esc(sub)}</p><div class="tags">in <b>{esc(a["category"])}</b></div></a>')

def sect(title, sub="", link=None):
    l = f'<a href="{link}">Vedi tutti ›</a>' if link else ""
    s = f'<p class="sect-sub">{esc(sub)}</p>' if sub else ""
    return f'<div class="sect"><h2>{esc(title)}</h2>{l}</div>{s}'

def write(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)

def build():
    arts = load()
    if not arts: sys.exit("Nessun articolo pubblicabile")
    # pulizia output generato
    for d in ("articles", "categoria"):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)

    # Articoli
    md = markdown.Markdown(extensions=["extra", "smarty"], extension_configs={"smarty": {"substitutions": {
        "left-double-quote": "“", "right-double-quote": "”", "left-single-quote": "‘", "right-single-quote": "’"}}})
    for a in arts:
        # vecchi indirizzi (es. articolo spostato di data): pagina di rimando verso quello nuovo
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
        mins = max(1, round(a["words"] / 220))
        rel = [x for x in arts if x is not a and x["category"] == a["category"]][:3]
        rel += [x for x in arts if x is not a and x not in rel][:3 - len(rel)]
        ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article",'
              f'"headline":{jsonstr(a["title"])},"description":{jsonstr(a["description"])},'
              f'"datePublished":"{a["d"].isoformat()}","inLanguage":"it","mainEntityOfPage":"{SITE}{a["url"]}",'
              f'"publisher":{{"@type":"Organization","name":"{NAME}"}}'
              + (f',"image":"{SITE}{img_path(a["slug"])}"' if img_path(a["slug"]) else "") + '}</script>')
        content = f"""<article>
<header class="art-head"><div class="kick"><a href="/categoria/{slugify(a['category'])}/">{esc(a['category'])}</a></div>
<h1>{esc(a['title'])}</h1><p class="standfirst">{esc(a['description'])}</p>
<div class="byline">{itdate(a['d'])} · {mins} minuti di lettura</div></header>
<div class="art-cover">{img(a)}</div>
<div class="body">{body}<p class="fin">❦</p></div>
</article>
<section class="wrap related">{sect("Da leggere ancora")}<div class="row3">{''.join(card(x) for x in rel)}</div></section>"""
        write(a["url"].strip("/") + "/index.html",
              page(a["title"], a["description"], a["url"], content, a["category"], "article", ld, img_path(a["slug"])))

    # Home
    lead, side, rest = arts[0], arts[1:4], arts[4:]
    circ, rest = rest[:6], rest[6:]
    row, rest = rest[:4], rest[4:]
    longr = rest[0] if rest else None
    q = next((a for a in arts if a.get("quote")), arts[min(3, len(arts) - 1)])
    qtext = q.get("quote") or q["description"]
    side_html = "".join(f'<a href="{a["url"]}">{img(a) if i == 0 else ""}<div class="kick">{esc(a["category"])}</div>'
                        f'<h3>{esc(a["title"])}</h3><div class="meta">{itdate(a["d"])}</div></a>' for i, a in enumerate(side))
    home = f"""<div class="wrap">
<section class="hero"><a class="hero-main" href="{lead['url']}">{img(lead, ar="3/2")}
<div class="kick" style="margin-top:18px">{esc(lead['category'])} <span>· {itdate(lead['d'])}</span></div>
<h2>{esc(lead['title'])}</h2><p>{esc(lead['description'])}</p></a>
<div class="side-list">{side_html}</div></section>"""
    if circ:
        home += sect("Da bere e da sapere", "Una selezione dall'archivio di Vinofilo") + f'<div class="circles">{"".join(circle(a) for a in circ)}</div>'
    home += "</div>"
    home += f'<section class="quote"><div class="wrap"><p>“{esc(qtext)}”</p><a href="{q["url"]}">{esc(q["title"])} →</a></div></section>'
    home += '<div class="wrap">'
    # Seconda apertura, specchiata: la lettura più lunga fra quelle sotto la prima apertura
    pool = [a for a in arts if a not in [lead] + side]
    if len(pool) >= 4:
        lead2 = max(pool, key=lambda a: a["words"])
        side2 = [a for a in pool if a is not lead2][-3:]
        side2_html = "".join(f'<a href="{a["url"]}">{img(a) if i == 0 else ""}<div class="kick">{esc(a["category"])}</div>'
                             f'<h3>{esc(a["title"])}</h3><div class="meta">{itdate(a["d"])}</div></a>' for i, a in enumerate(side2))
        home += f"""<section class="hero rev">
<div class="side-list">{side2_html}</div>
<a class="hero-main" href="{lead2['url']}">{img(lead2, ar="3/2")}
<div class="kick" style="margin-top:18px">Lettura lunga <span>· {esc(lead2['category'])} · {round(lead2['words'] / 220)} minuti</span></div>
<h2>{esc(lead2['title'])}</h2><p>{esc(lead2['description'])}</p></a></section>"""
    by = {a["slug"]: a for a in arts}
    pool_n = [{"u": by[sl]["url"], "n": n, "t": t} for sl, n, t in NUMERI if sl in by]
    if len(pool_n) >= 4:
        first, used = [], set()
        for x in pool_n:
            if x["u"] not in used: first.append(x); used.add(x["u"])
            if len(first) == 4: break
        cells = "".join(f'<a href="{x["u"]}"><b>{esc(x["n"])}</b><p>{esc(x["t"])}</p><span>Leggi ›</span></a>' for x in first)
        data = json.dumps(pool_n, ensure_ascii=False).replace("</", "<\\/")
        home += sect("I numeri", "Quattro cifre dagli articoli, ogni volta diverse") + f'<div class="nums" id="nums">{cells}</div>' + (
            '<script>(function(){var P=' + data + ';var o=[],u={};P.sort(function(){return Math.random()-.5});'
            'for(var i=0;i<P.length&&o.length<4;i++){if(!u[P[i].u]){u[P[i].u]=1;o.push(P[i])}}'
            'var e=function(s){return s.replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c]})};'
            'document.getElementById("nums").innerHTML=o.map(function(x){return\'<a href="\'+x.u+\'"><b>\'+e(x.n)+\'</b><p>\'+e(x.t)+\'</p><span>Leggi ›</span></a>\'}).join("")})();</script>')
    if row:
        home += sect("Ultimi articoli", "Appena usciti dalla cantina") + f'<div class="row4">{"".join(card(a, False) for a in row)}</div>'
    counts = {c: sum(1 for a in arts if a["category"] == c) for c in CATS}
    tiles = "".join(f'<a href="/categoria/{slugify(c)}/" style="--c:{v[0]};--fg:{v[1]}"><b>{c}</b><span>{v[2]} · {counts[c]} articoli</span></a>' for c, v in CATS.items())
    home += sect("Esplora per tema") + f'<div class="cats">{tiles}</div></div>'
    write("index.html", page(NAME, f"{NAME}: {TAGLINE.lower()}. Vitigni, territori, tecnica e servizio raccontati con un punto di vista.", "/", home))

    # Categorie
    for c in CATS:
        items = [a for a in arts if a["category"] == c]
        inner = "".join(card(a) for a in items) or "<p>Articoli in arrivo.</p>"
        content = f'<div class="wrap"><div class="cat-head"><div class="kick">{esc(CATS[c][2])}</div><h1>{c}</h1></div>{sect(f"{len(items)} articoli")}<div class="row3">{inner}</div></div>'
        write(f"categoria/{slugify(c)}/index.html", page(c, f"Articoli su {c.lower()} del vino — {NAME}.", f"/categoria/{slugify(c)}/", content, c))

    # Pagine statiche (content/pagine/*.md): privacy ecc.
    pages = []
    pdir = os.path.join(ROOT, "content/pagine")
    for fn in sorted(os.listdir(pdir)) if os.path.isdir(pdir) else []:
        if not fn.endswith(".md"): continue
        raw = open(os.path.join(pdir, fn), encoding="utf-8").read()
        m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
        meta = {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)}
        txt = m.group(2).strip()
        keep, drop = ("ga", "noga") if GA_ID else ("noga", "ga")
        txt = re.sub(rf"<!--{drop}-->.*?<!--/{drop}-->\n?", "", txt, flags=re.S)
        txt = re.sub(rf"<!--/?{keep}-->\n?", "", txt)
        md.reset()
        body = md.convert(txt)
        path = f"/{meta['slug']}/"
        content = (f'<article><header class="art-head"><h1>{esc(meta["title"])}</h1></header>'
                   f'<div class="body page">{body}</div></article>')
        shutil.rmtree(os.path.join(ROOT, meta["slug"]), ignore_errors=True)
        write(f"{meta['slug']}/index.html", page(meta["title"], meta["description"], path, content))
        pages.append(path)

    # 404, sitemap, robots
    write("404.html", page("Pagina non trovata", "Pagina non trovata.", "/404.html",
          '<div class="wrap"><div class="cat-head"><h1>Bottiglia vuota</h1><p class="standfirst">Questa pagina non esiste. <a href="/" style="color:var(--accent)">Torna alla home ›</a></p></div></div>'))
    urls = [("/", arts[0]["d"])] + [(a["url"], a["d"]) for a in arts] + [(f"/categoria/{slugify(c)}/", None) for c in CATS] + [(p, None) for p in pages]
    sm = "".join(f"<url><loc>{SITE}{u}</loc>{f'<lastmod>{d.isoformat()}</lastmod>' if d else ''}</url>" for u, d in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print(f"OK: {len(arts)} articoli pubblicati")

def jsonstr(s):
    import json
    return json.dumps(s, ensure_ascii=False)

if __name__ == "__main__":
    build()
