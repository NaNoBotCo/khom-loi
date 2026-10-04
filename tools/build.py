#!/usr/bin/env python3
"""build.py — writes docs/index.html (English) and docs/th/index.html (Thai), sitemap.xml,
robots.txt and llms.txt. All copy, both languages, is written by hand in copy.py.

Run:  python3 tools/build.py [--motdang]
"""
import html
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from copy_text import UI, PHOTOS, SOURCES  # noqa: E402

SLUG = "khom-loi"
DOCS = os.path.join(HERE, "..", "docs")
GH = f"https://nanobotco.github.io/{SLUG}/"
CANON = f"https://motdang.net/sites/{SLUG}/"
MD_ROOT = f"/sites/{SLUG}/"
SIB = "https://motdang.net/sites/krathong/"
E = html.escape
CSS = open(os.path.join(HERE, "site.css")).read()
GOOGLE_ESCAPE = '<script>if(/[.]translate[.]goog$/.test(location.hostname))location.replace("https://"+location.hostname.slice(0,-15).replace(/--/g,"~").replace(/-/g,".").replace(/~/g,"-")+location.pathname+location.search.replace(/([?&])_x_tr_[^&]*/g,"$1").replace(/[?&]+$/,"").replace(/[?]&+/,"?")+location.hash)</script>'


def paras(ps):
    return "".join(f"<p>{p}</p>" for p in ps)


def rng(id_, label, lo, hi, step, val, out=None):
    o = f' <b id="{out}"></b>' if out else ""
    return f'<label class="lab" for="{id_}">{E(label)}{o}</label><input id="{id_}" type="range" min="{lo}" max="{hi}" step="{step}" value="{val}">'


def ro(label, id_):
    return f'<div><span>{E(label)}</span><b id="{id_}">–</b></div>'


def page(lang, md=False):
    u = UI[lang]
    root = MD_ROOT if md else ("" if lang == "en" else "../")
    url = CANON if lang == "en" else CANON + "th/"
    js = {k: u[k] for k in ("spare", "short", "l_lift", "l_weight", "f_char", "f_never", "compass", "sites", "map_labels")}
    js["lang"] = lang
    nav = "".join(f'<a href="#{a}">{E(b)}</a>' for a, b in u["nav"])
    other = (MD_ROOT + ("th/" if lang == "en" else "")) if md else ("th/" if lang == "en" else "../")
    sib = ("/sites/krathong/" if md else SIB) + ("th/" if lang == "th" else "")
    sibicon = ("/sites/krathong/" if md else SIB) + "icon.svg"
    head = f'''<!doctype html><html lang="{lang}" translate="no" class="notranslate"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate">
{GOOGLE_ESCAPE}
<title>{E(u["title"])} · {E(u["other_title"])}</title>
<meta name="description" content="{E(u["desc"])}">
<meta name="theme-color" content="#0e1030">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{CANON}"><link rel="alternate" hreflang="th" href="{CANON}th/"><link rel="alternate" hreflang="x-default" href="{CANON}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Khom Loi, Drawn · โคมลอย วาดด้วยคณิต">
<meta property="og:title" content="{E(u["title"])}"><meta property="og:description" content="{E(u["desc"])}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{CANON}card.jpg"><meta property="og:image:secure_url" content="{CANON}card.jpg"><meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(u["card_alt"])}">
<meta property="og:locale" content="{"en_US" if lang == "en" else "th_TH"}"><meta property="og:locale:alternate" content="{"th_TH" if lang == "en" else "en_US"}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{CANON}card.jpg">
<link rel="icon" href="{root}icon.svg" type="image/svg+xml">
<link rel="alternate" type="text/plain" href="{CANON}llms.txt" title="llms.txt">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Noto+Sans+Thai:wght@400;600;700&family=Noto+Serif+Thai:wght@600;700&display=swap" rel="stylesheet">
<script>if(/[?&]card/.test(location.search))document.documentElement.classList.add("card")</script>
<style>{CSS}</style>
</head><body>
<header class="top"><div class="in"><a class="brand" href="#top"><img src="{root}icon.svg" width="28" height="28" alt=""><span>{E(u["title"])}</span></a>
<nav aria-label="{E(u["nav_label"])}">{nav}</nav>
<span class="lang"><b>{E(u["lang_this"])}</b> | <a href="{other}" hreflang="{"th" if lang == "en" else "en"}">{E(u["lang_other"])}</a></span></div></header>
'''
    hero = f'''<section id="top" class="hero"><canvas id="scene" role="img" aria-label="{E(u["hero_alt"])}"></canvas>
<div class="hero-t"><p class="kick">{E(u["kicker"])}</p><h1>{E(u["title"])}</h1><p class="lede">{E(u["lede"])}</p><p class="hint">{E(u["hint"])}</p><p class="cardline">{E(u["cardline"])}<br><span>motdang.net/sites/{SLUG}</span></p></div></section>
'''
    what = f'''<section id="what" class="sec"><div class="in"><p class="kick">{E(u["what_kick"])}</p><h2>{E(u["what_h"])}</h2>{paras(u["what_p"])}</div></section>
'''
    lift = f'''<section id="lift" class="sec dark"><div class="in two"><div><canvas id="liftcv" class="cv" role="img" aria-label="{E(u["lift_h"])}"></canvas>
<p class="legend"><span><i style="background:#96c8ff"></i>{E(u["l_out"])}</span><span><i style="background:#ffbe6e"></i>{E(u["l_in"])}</span></p></div>
<div><p class="kick">{E(u["lift_kick"])}</p><h2>{E(u["lift_h"])}</h2>{paras(u["lift_p"])}
<p class="eq">{u["lift_eq"]}</p>
{rng("ti", u["l_ti"], 30, 280, 1, 140, "tio")}{rng("ta", u["l_ta"], 5, 38, 1, 22, "tao")}{rng("lh", u["l_h"], 50, 180, 1, 100, "lho")}
<div class="readout">{ro(u["l_lift"], "rlift")}{ro(u["l_weight"], "rweight")}{ro(u["l_rho"], "rrho")}</div>
<p><b id="rnet"></b></p><p id="hotwarn" class="warn" hidden>{E(u["l_hot"])}</p>
<p class="note">{u["lift_note"]}</p></div></div></section>
'''
    flight = f'''<section id="flight" class="sec"><div class="in"><p class="kick">{E(u["fl_kick"])}</p><h2>{E(u["fl_h"])}</h2>{paras(u["fl_p"])}
<canvas id="flightcv" class="cv" role="img" aria-label="{E(u["fl_h"])}"></canvas>
<p class="legend"><span><i style="background:#8fd3ff"></i>{E(u["fl_height"])}</span><span><i style="background:#ffb347"></i>{E(u["fl_heat"])}</span><span><i style="background:rgba(255,200,120,.5)"></i>{E(u["fl_burning"])}</span></p>
<div class="readout" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))"><div>{rng("ff", u["f_fuel"], 5, 55, 1, 30, "ffo")}</div><div>{rng("fh", u["f_h"], 60, 160, 1, 100, "fho")}</div><div>{rng("fg", u["f_gsm"], 12, 45, 1, 22, "fgo")}</div><div>{rng("fta", u["f_ta"], 5, 38, 1, 22, "ftao")}</div></div>
<div class="readout">{ro(u["f_hold"], "fhold")}{ro(u["f_top"], "ftop")}{ro(u["f_aloft"], "faloft")}{ro(u["f_hot"], "fhot")}</div>
{paras(u["fl_p2"])}<p class="note">{u["fl_note"]}</p></div></section>
'''
    sites = "".join(f'<button class="pill" type="button" data-site="{i}" aria-pressed="{"true" if i == 0 else "false"}">{E(s["name"])}</button>' for i, s in enumerate(u["sites"]))
    tix = "".join(f'<a href="{E(h)}" rel="sponsored nofollow noopener" target="_blank">{E(t)}</a>' for t, h in u["tix"])
    tix = f'<div class="tix"><b>{E(u["tix_h"])}</b>{tix}<small>{E(u["tix_note"])}</small></div>'
    drift = f'''<section id="drift" class="sec rock"><div class="in"><p class="kick">{E(u["dr_kick"])}</p><h2>{E(u["dr_h"])}</h2>{paras(u["dr_p"])}
{tix}
<div class="seg" role="group" aria-label="{E(u["dr_site"])}">{sites}</div>
<canvas id="driftcv" class="cv" data-map="{root}map.json" role="img" aria-label="{E(u["dr_h"])}"></canvas>
<p class="legend"><span><i style="background:#7a3d12"></i>{E(u["dr_land"])}</span><span><i style="background:#1f6fb5"></i>{E(u["dr_water"])}</span><span><i style="background:#c0262d"></i>{E(u["dr_air"])}</span></p>
<div class="readout" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))"><div>{rng("wd", u["d_from"], 0, 359, 1, 45, "wdo")}</div><div>{rng("ws", u["d_speed"], 0, 60, 1, 20, "wso")}</div></div>
<div class="btns"><button id="dgo" class="pill hot" type="button">{E(u["d_go"])}</button></div>
<div class="readout">{ro(u["d_med"], "dmed")}{ro(u["d_far"], "dfar")}{ro(u["d_air"], "dair")}{ro(u["d_wat"], "dwat")}</div>
{paras(u["dr_p2"])}<p class="note">{u["dr_note"]}</p></div></section>
'''
    sky = f'''<section id="sky" class="sec dark"><div class="in two"><div><canvas id="skycv" class="cv" role="img" aria-label="{E(u["sk_h"])}"></canvas></div>
<div><p class="kick">{E(u["sk_kick"])}</p><h2>{E(u["sk_h"])}</h2>{paras(u["sk_p"])}
<p class="eq">{u["sk_eq"]}</p>
{rng("lam", u["s_lam"], 1, 200, 1, 40, "lamo")}{rng("lmin", u["s_min"], 5, 90, 1, 30, "lmino")}
<div class="readout">{ro(u["s_w"], "lw")}{ro(u["s_peak"], "lpeak")}{ro(u["s_total"], "ltotal")}</div>
<p class="note">{u["sk_note"]}</p></div></div></section>
'''
    dates = "".join(f'<div><b>{E(a)}</b><span>{b}</span></div>' for a, b in u["dates"])
    yp = f'''<section id="yipeng" class="sec"><div class="in"><p class="kick">{E(u["yp_kick"])}</p><h2>{E(u["yp_h"])}</h2>{paras(u["yp_p"])}
<div class="dates">{dates}</div>{paras(u["yp_p2"])}
<a class="sib" href="{sib}"><img src="{sibicon}" width="48" height="48" alt=""><span><b>{E(u["sib_h"])}</b>{E(u["sib_p"])}</span></a></div></section>
'''
    figs = []
    for p in PHOTOS:
        licl = f'<a href="{p["license_url"]}">{E(p["license"])}</a>' if p.get("license_url") else E(p["license"])
        cap = p["caption_" + lang]
        figs.append(f'<figure><img loading="lazy" src="{root}img/{p["file"]}" width="{p["width"]}" height="{p["height"]}" alt="{E(cap)}"><figcaption>{E(cap)} <a href="{p["commons_page"]}">{E(p["author"])}</a> · {licl}</figcaption></figure>')
    pics = f'''<section id="pictures" class="sec rock"><div class="in"><p class="kick">{E(u["pic_kick"])}</p><h2>{E(u["pic_h"])}</h2><div class="ph">{"".join(figs)}</div></div></section>
''' if figs else ""
    words = "".join(f'<div><b>{E(a)}</b><i>{E(b)}</i><p>{E(c)}</p></div>' for a, b, c in u["words"])
    wd = f'''<section id="words" class="sec"><div class="in"><h2>{E(u["words_h"])}</h2><div class="glos">{words}</div></div></section>
'''
    src = "".join(f'<li><a href="{h}">{E(t)}</a></li>' for t, h in SOURCES)
    so = f'''<section id="sources" class="sec"><div class="in"><h2>{E(u["src_h"])}</h2><p>{E(u["src_p"])}</p><ul class="src">{src}</ul></div></section>
'''
    tail = f'''<footer class="bot"><div class="in">{E(u["foot"])} · <a href="https://github.com/NaNoBotCo/{SLUG}">GitHub</a> · <a href="https://motdang.net/">motdang.net</a> · <a href="https://hongdam.net/">hongdam.net</a></div></footer>
<script>window.UI={json.dumps(js, ensure_ascii=False)};</script>
<script src="{root}lantern.js"></script><script src="{root}app.js"></script><script src="{root}top.js"></script>
</body></html>
'''
    return head + "<main>" + hero + what + lift + flight + drift + sky + yp + pics + wd + so + "</main>" + tail


def write_site(out, md):
    os.makedirs(os.path.join(out, "th"), exist_ok=True)
    host = CANON if md else GH
    for lang, path in (("en", "index.html"), ("th", "th/index.html")):
        with open(os.path.join(out, path), "w") as f:
            f.write(page(lang, md))
    with open(os.path.join(out, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                f'<url><loc>{host}</loc></url>\n<url><loc>{host}th/</loc></url>\n</urlset>\n')
    if not md:
        with open(os.path.join(out, "robots.txt"), "w") as f:
            f.write(f"User-agent: *\nAllow: /\nSitemap: {host}sitemap.xml\n")
    u = UI["en"]
    strip = lambda s: html.unescape(re.sub("<[^>]+>", "", s))
    lines = ["# Khom Loi, Drawn · โคมลอย วาดด้วยคณิต", "", u["desc"], "", f"English: {CANON}", f"Thai: {CANON}th/", ""]
    for key in ("what", "lift", "fl", "dr", "sk", "yp"):
        lines += ["## " + strip(u[key + "_h"]), ""] + [strip(p) for p in u[key + "_p"]] + [""]
    lines += ["## Dates", ""] + [f"- {a}: {strip(b)}" for a, b in u["dates"]] + [""]
    lines += ["## Words", ""] + [f"- {a} ({b}): {c}" for a, b, c in u["words"]]
    lines += ["", "## Sources", ""] + [f"- {t}: {h}" for t, h in SOURCES]
    lines += ["", "## Licence", "", "Text CC BY 4.0, NaNoBotCo. Code MIT. Map: OpenStreetMap contributors, ODbL. Photographs keep their own licences, listed on the page.", ""]
    with open(os.path.join(out, "llms.txt"), "w") as f:
        f.write("\n".join(lines))


def main():
    write_site(DOCS, False)
    print("built en + th -> docs/")
    if "--motdang" in sys.argv:
        md = os.path.join(HERE, "..", "..", "mot-dang")
        for sub in (f"assets/sites/{SLUG}", f"docs/sites/{SLUG}"):
            out = os.path.join(md, sub)
            if os.path.isdir(out):
                shutil.rmtree(out)
            shutil.copytree(DOCS, out, ignore=shutil.ignore_patterns("robots.txt", ".DS_Store"))
            write_site(out, True)
            shutil.copy(os.path.join(HERE, "motdang_card.json"), os.path.join(out, "card.json"))
            print("built en + th ->", os.path.normpath(out))


if __name__ == "__main__":
    main()
