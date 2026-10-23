#!/usr/bin/env python3
"""Mock für Warehouse-Produktkarten (product-item) und die Icon-Leiste (text-with-icons) mit Theme-Basisregeln + es-design-system + es-overrides (v3)."""
import re, pathlib
S = pathlib.Path('/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad')
OUT = S / 'design-review/v3'; OUT.mkdir(parents=True, exist_ok=True)
ov = (S / 'theme/v3/new/snippets/es-overrides.liquid').read_text(encoding='utf-8')
ov = re.sub(r'{%-?\s*comment\s*-?%}.*?{%-?\s*endcomment\s*-?%}', '', ov, flags=re.S)
ov = re.sub(r'{{[^}]*}}|{%[^%]*%}', '', ov)
ds = (S / 'theme/v3/orig/assets/es-design-system.css').read_text(encoding='utf-8')
# Warehouse-Basisregeln (aus theme.css der Live-Seite extrahiert, gekürzt)
WH = """
:root{--base-text-font-size:16px;--default-text-font-size:16px;--accent-color:#1B1F1D;--product-on-sale-accent:#C93F3F;--text-color:#272D2A;--text-color-rgb:39,45,42;--border-color:#DCE3DE;--product-review-star-color:#D9962B}
*{box-sizing:border-box}body{margin:0;font-family:Archivo,system-ui,sans-serif;font-size:16px;color:#272D2A;background:#fff}
.container{max-width:1280px;margin:0 auto;padding:0 24px}
.product-list{display:flex;flex-wrap:wrap;margin:0 -12px}.product-item{padding:0 12px;width:25%;margin-bottom:24px}
@media(max-width:999px){.product-item{width:50%}}@media(max-width:749px){.product-list{margin:0 -6px}.product-item{padding:0 6px;width:50%}}
.product-item--vertical,.product-item--vertical .product-item__info{flex-direction:column;display:flex}
.product-item--vertical .product-item__info{flex:1 0 auto;justify-content:space-between}
.product-item__image-wrapper{margin-bottom:20px;display:block;position:relative}.aspect-ratio{position:relative;display:block}.aspect-ratio img{position:absolute;top:0;left:0;width:100%;height:100%}
.product-item__label-list{position:absolute;top:8px;left:8px;z-index:1}.product-label{display:inline-block;background:#338258;color:#fff;font-size:12px;padding:3px 8px;font-weight:700}
.product-item__info{min-width:0}.product-item__price-list:first-child{margin-bottom:10px}.product-item__price-list{margin-top:-5px;margin-bottom:-5px}
.product-item__price-list .price{margin-top:5px;margin-bottom:5px;display:inline-block}
.product-item__vendor,.product-item__title{line-height:1.55;display:block}.product-item__title{margin-bottom:12px;font-size:14px;text-decoration:none;color:inherit}
.product-item__reviews-badge{margin-top:8px;display:block;text-decoration:none;color:inherit}
.price-list{align-items:baseline;line-height:1;display:inline-flex}.price{font-size:24px;color:var(--accent-color);font-weight:700}
.price--highlight{color:var(--product-on-sale-accent);margin-right:.7em}.price--compare{color:var(--text-color);font-size:16px;text-decoration:line-through;position:relative;font-weight:400}
.product-item .price--compare{font-size:14px}.product-item--vertical .price:not(.price--compare){font-size:20px}
.rating{vertical-align:bottom;line-height:inherit;align-items:center;display:flex}.rating__stars{grid-auto-flow:column;column-gap:2px;display:grid}
.rating__star{color:var(--product-review-star-color);width:14px;height:14px}.rating__caption{font-size:13px;margin-left:7px;position:relative;top:1px}
.visually-hidden{position:absolute!important;overflow:hidden;width:1px;height:1px;margin:-1px;padding:0;border:0;clip:rect(0 0 0 0)}
.product-item--vertical .product-item__action-list{margin:15px -5px -5px}.button-stack{display:flex;flex-direction:column}
.product-item--vertical .product-item__action-button{flex:1 0 auto;margin:5px!important}.button{font:inherit;cursor:pointer}
.section{padding:40px 0}.section--tight{padding:28px 0}
.text-with-icons__item{width:100%;line-height:1.6}.text-with-icons__title{margin-bottom:4px}.text-with-icons__icon-wrapper{margin-bottom:15px}.text-with-icons__icon-wrapper svg{vertical-align:middle;width:30px;height:30px}
.text-with-icons__content>p{margin-bottom:0}.text-with-icons__content p{margin:0}.text-with-icons{text-align:center;padding-bottom:28px}.text-with-icons:after{content:"flickity";display:none}
@media screen and (min-width:641px){.text-with-icons{flex-wrap:wrap;margin:0 -40px -45px;display:flex}.text-with-icons__item{flex-basis:calc(50% - 90px);margin:0 40px 45px;display:flex}.text-with-icons__icon-wrapper{margin:.5em 18px 0 0}}
@media screen and (min-width:1000px){.text-with-icons{justify-content:center;padding:0 100px}.text-with-icons__item{flex-basis:calc(50% - 140px);display:flex}}
@media screen and (min-width:1280px){.text-with-icons{flex-wrap:nowrap;justify-content:space-around;margin:0 -35px;padding:0}.text-with-icons__item{flex-basis:calc(25% - 70px);margin:0 35px}}
.text--strong{font-weight:700}.footer{background:#1B1F1D;height:60px}
"""
STAR = '<svg class="rating__star" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3 6.6 7 .8-5.2 4.8 1.4 7L12 17.7 5.8 21.2l1.4-7L2 9.4l7-.8z"/></svg>'
def svg_box(ratio):
    w, h = (1000, 1000) if ratio == '1:1' else (1600, 1200)
    return f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}'%3E%3Crect width='{w}' height='{h}' fill='%23F3F5F4'/%3E%3Cpolygon points='{w*.15:.0f},{h*.35:.0f} {w*.85:.0f},{h*.3:.0f} {w*.85:.0f},{h*.75:.0f} {w*.15:.0f},{h*.8:.0f}' fill='%23B9C3BE'/%3E%3C/svg%3E"
CARDS = [('Terrassenüberdachung Premium Anthrazit Alu mit Stegplatten 16mm anthrazit/graphit', '1:1', 'ab €989,90', '€2.043,56', 9, '51%'),
         ('Terrassenüberdachung Premium Weiß Alu mit Stegplatten 16mm klar/farblos', '1:1', 'ab €1.089,90', '€1.961,44', 3, '44%'),
         ('Terrassenüberdachung Premium Weiß Alu mit Stegplatten 16mm opal/weiß', '1:1', 'ab €1.079,90', '€1.942,73', 0, '44%'),
         ('Terrassenüberdachung Premium Anthrazit Alu mit Stegplatten 16mm klar/farblos', '4:3', 'ab €939,90', '€1.907,39', 1, '51%')]
def card(t, ratio, price, cmp, n, sv):
    pb = '100.0%' if ratio == '1:1' else '75.0%'
    badge = f'<a class="product-item__reviews-badge link" href="#"><div class="rating"><div class="rating__stars" role="img" aria-label="5 von 5 Sternen">{STAR*5}</div><span class="rating__caption">{n} Bewertungen</span></div></a>' if n else ''
    return f'''<div class="product-item product-item--vertical"><div class="product-item__label-list"><span class="product-label product-label--on-sale">Einsparung {sv}</span></div>
<a href="#" class="product-item__image-wrapper"><div class="aspect-ratio" style="padding-bottom: {pb}"><img src="{svg_box(ratio)}" alt="" class="product-item__primary-image"></div></a>
<div class="product-item__info"><div class="product-item__info-inner"><a class="product-item__vendor link" href="#">e-Stegplatten</a> <a href="#" class="product-item__title text--strong link">{t}</a>
<div class="product-item__price-list price-list"><span class="price price--highlight"><span class="visually-hidden">Sonderpreis</span>{price}</span> <span class="price price--compare"><span class="visually-hidden">Normalpreis</span>{cmp}</span></div>{badge}</div>
<form class="product-item__action-list button-stack"><button type="button" class="product-item__action-button button button--small button--primary">Größe wählen</button><button type="button" class="product-item__action-button button button--small button--ternary">Schnellansicht</button></form></div></div>'''
ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="#338258" stroke-width="1.6"><path d="M3 7l9-4 9 4-9 4-9-4zm0 0v10l9 4 9-4V7"/></svg>'
ITEMS = [('Schnell versendet', 'Zuverlässig &amp; Sicher'), ('Sicherer Transport', 'Zuverlässige Versandpartner'), ('Kundenservice', 'Persönliche Beratung'), ('Sichere Bezahlung', 'Online sichere Zahlung mit PayPal &amp; Klarna')]
twi = ''.join(f'<div class="text-with-icons__item"><div class="text-with-icons__icon-wrapper">{ICON}</div><div class="text-with-icons__content-wrapper"><p class="text-with-icons__title text--strong">{a}</p><div class="text-with-icons__content rte"><p>{b}</p></div></div></div>' for a, b in ITEMS)
html = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Karten-Mock</title>
<style>{WH}</style><link rel="stylesheet" href="../../theme/v3/orig/assets/es-design-system.css">{ov}</head><body>
<section class="section"><div class="container"><div class="product-list">{''.join(card(*c) for c in CARDS)}</div></div></section>
<section class="section section--tight"><div class="container container--flush"><div class="text-with-icons ">{twi}</div></div></section><div class="footer"></div></body></html>'''
(OUT / 'cards.html').write_text(html, encoding='utf-8'); print('cards ->', OUT / 'cards.html', len(html))
