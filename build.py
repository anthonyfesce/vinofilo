#!/usr/bin/env python3
"""Generatore statico di Vinofilo.

Sorgenti: content/articles/*.md (front matter: date, number, title, description, category, slug)
Output: index.html, articles/AAAA.MM.GG/slug/index.html, categoria/<cat>/index.html,
        sitemap.xml, robots.txt, 404.html — direttamente nella radice del repository.
Gli articoli con data futura non vengono pubblicati (servono per la programmazione).
"""
import datetime as dt, html, os, re, shutil, sys
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://vinofilo.com"
NAME = "Vinofilo"
TAGLINE = "Storie, territori e tecnica del vino"
MESI = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
CATS = {  # categoria: (sfondo, testo, lettera di fondo)
    "Vitigni": ("#7E1C2B", "#FBF3E4", "rgba(255,255,255,.10)"),
    "Territori": ("#2F5D50", "#F4EDE1", "rgba(255,255,255,.10)"),
    "Tecnica": ("#E9B44C", "#1B1416", "rgba(0,0,0,.08)"),
    "Servizio": ("#E07254", "#1B1416", "rgba(0,0,0,.08)"),
    "Guide": ("#1F2E47", "#F4EDE1", "rgba(255,255,255,.09)"),
}
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,300;1,400;1,500'
         '&family=Inter:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">')

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

def label(a, big=False):
    name = a.get("cover") or a["title"].split(":")[0]
    word = re.split(r"['’]", name.split()[-1])[-1]
    bg, fg, bl = CATS[a["category"]]
    stamp = f'<span class="stamp">N°<b>{a["number"]:02d}</b></span>' if a["number"] else ""
    return (f'<div class="label{" big" if big else ""}" style="--c:{bg};--fg:{fg};--bgl:{bl}" aria-hidden="true">'
            f'<span class="bg">{esc(word[0].upper())}</span><span class="k">{esc(a["category"])}</span>{stamp}'
            f'<span class="t">{esc(name)}</span></div>')

def page(title, desc, path, content, active="", og_type="website", extra_head=""):
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
<meta name="theme-color" content="#F5F0E6">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="/assets/style.css">
{extra_head}
</head>
<body>
<div class="strip"><div class="wrap"><span>Rivista di vino</span><em>bere meglio, capire di più</em><span>Italia</span></div></div>
<header class="masthead"><div class="wrap">
<a href="/" class="wordmark">Vino<i>filo</i></a>
<p class="tagline">{TAGLINE}</p>
<nav class="nav">{nav}</nav>
</div></header>
<main>
{content}
</main>
<footer><div class="wrap"><a href="/" class="wordmark">Vino<i>filo</i></a><p>{TAGLINE} · © {dt.date.today().year}</p></div></footer>
</body>
</html>
"""

def card(a):
    return (f'<a class="card" href="{a["url"]}">{label(a)}<div class="kick">{esc(a["category"])} <span>· {itdate(a["d"])}</span></div>'
            f'<h3>{esc(a["title"])}</h3><p>{esc(a["description"])}</p></a>')

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
        md.reset()
        body = md.convert(a["body"])
        body = re.sub(r"(\w)‘(\d)", r"\1’\2", body)  # l’80%, non l‘80%
        mins = max(1, round(a["words"] / 220))
        rel = [x for x in arts if x is not a and x["category"] == a["category"]][:3]
        rel += [x for x in arts if x is not a and x not in rel][:3 - len(rel)]
        ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article",'
              f'"headline":{jsonstr(a["title"])},"description":{jsonstr(a["description"])},'
              f'"datePublished":"{a["d"].isoformat()}","inLanguage":"it","mainEntityOfPage":"{SITE}{a["url"]}",'
              f'"publisher":{{"@type":"Organization","name":"{NAME}"}}}}</script>')
        content = f"""<article>
<header class="art-head"><div class="kick"><a href="/categoria/{slugify(a['category'])}/">{esc(a['category'])}</a></div>
<h1>{esc(a['title'])}</h1><p class="standfirst">{esc(a['description'])}</p>
<div class="byline">{itdate(a['d'])} · {mins} minuti di lettura</div></header>
<div class="art-cover">{label(a, big=True)}</div>
<div class="body">{body}<p class="fin">❦</p></div>
</article>
<section class="wrap related"><div class="sect"><h2>Da leggere ancora</h2><span>Vinofilo</span></div><div class="grid">{''.join(card(x) for x in rel)}</div></section>"""
        write(a["url"].strip("/") + "/index.html",
              page(a["title"], a["description"], a["url"], content, a["category"], "article", ld))

    # Home
    lead, rest = arts[0], arts[1:]
    duo, grid = rest[:2], rest[2:]
    q = grid[0] if grid else lead
    home = f"""<div class="wrap">
<section class="lead"><a href="{lead['url']}">{label(lead, big=True)}</a>
<div><div class="kick">{esc(lead['category'])} <span>· {itdate(lead['d'])}</span></div>
<a href="{lead['url']}"><h2>{esc(lead['title'])}</h2></a><p>{esc(lead['description'])}</p>
<a class="more" href="{lead['url']}">Leggi l'articolo</a></div></section>
<div class="sect"><h2>Ultimi articoli</h2><span>{len(arts)} storie</span></div>
<div class="duo">{''.join(card(a) for a in duo)}</div></div>
<section class="quote"><div class="wrap"><p>“{esc(q['description'])}”</p><a href="{q['url']}">{esc(q['title'])} →</a></div></section>
<div class="wrap"><div class="grid">{''.join(card(a) for a in grid)}</div></div>"""
    write("index.html", page(NAME, f"{NAME}: {TAGLINE.lower()}. Vitigni, territori, tecnica e servizio raccontati con un punto di vista.", "/", home))

    # Categorie
    for c in CATS:
        items = [a for a in arts if a["category"] == c]
        inner = "".join(card(a) for a in items) or "<p>Articoli in arrivo.</p>"
        content = f'<div class="wrap"><div class="cat-head"><div class="kick">Categoria</div><h1>{c}</h1></div><div class="grid" style="margin-top:44px">{inner}</div></div>'
        write(f"categoria/{slugify(c)}/index.html", page(c, f"Articoli su {c.lower()} del vino — {NAME}.", f"/categoria/{slugify(c)}/", content, c))

    # 404, sitemap, robots
    write("404.html", page("Pagina non trovata", "Pagina non trovata.", "/404.html",
          '<div class="wrap"><div class="cat-head"><h1>Bottiglia vuota</h1><p class="standfirst">Questa pagina non esiste. <a href="/" class="more">Torna alla home</a></p></div></div>'))
    urls = [("/", arts[0]["d"])] + [(a["url"], a["d"]) for a in arts] + [(f"/categoria/{slugify(c)}/", None) for c in CATS]
    sm = "".join(f"<url><loc>{SITE}{u}</loc>{f'<lastmod>{d.isoformat()}</lastmod>' if d else ''}</url>" for u, d in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print(f"OK: {len(arts)} articoli pubblicati")

def jsonstr(s):
    import json
    return json.dumps(s, ensure_ascii=False)

if __name__ == "__main__":
    build()
