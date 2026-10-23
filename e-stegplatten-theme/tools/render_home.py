#!/usr/bin/env python3
"""Rendert die Startseite (sections/es-landing.liquid: Hero, Vertrauens-Leiste, Kategorien) mit den echten
v3-Liquid-Dateien, den Einstellungen/Blocks aus templates/index.json und Beispieldaten nach design-review/v3/home.html."""
import json, re
from mockdata import *  # noqa: F401,F403

OUT = S / 'design-review/v3'
OUT.mkdir(parents=True, exist_ok=True)
src = (V3 / 'sections/es-landing.liquid').read_text(encoding='utf-8')
schema = json.loads(re.search(r'{% schema %}(.*){% endschema %}', src, re.S).group(1))
defaults = {x['id']: x.get('default') for x in schema['settings'] if 'id' in x}
i = src.index('<section class="s" data-screen-label="Kategorien">')
j = src.index('</section>', i) + len('</section>')
body_src = src[:j] + '\n</div>'
assert '{% schema %}' not in body_src

idx = read_index()
L = idx['sections']['es_landing']
settings = {**defaults, **L['settings']}
hd, hm = S / 'content/hero/hero-desktop.jpg', S / 'content/hero/hero-mobile.jpg'
settings['hero_image'] = {'alt': '', 'width': 1536, 'height': 1024, 'src': hd.as_uri()} if hd.exists() else {'alt': '', 'width': 1400, 'height': 1050, 'hero': True}
if hm.exists():
    settings['hero_image_m'] = {'alt': '', 'width': 1024, 'height': 768, 'src': hm.as_uri()}
else:
    settings.pop('hero_image_m', None)
blocks = [{'type': L['blocks'][k]['type'], 'settings': L['blocks'][k]['settings'], 'shopify_attributes': ''} for k in L['block_order']]
kh = settings.get('konfig_handle') or 'terrassenuberdachung-alu-mit-stegplatten'

env = make_env({n: load_snippet(n) for n in ['es-landing-css', 'es-hero-konfig', 'es-landing-finder']})
html = env.from_string(body_src).render(section={'id': 'x', 'settings': settings, 'blocks': blocks}, collections=Cols({kh: KC}),
                                        linklists={}, all_products=ALL, routes=ROUTES, shop=SHOP)
assert '{{' not in html and '{%' not in html, 'ungelöstes Liquid in der Startseite'

ns = frame()
head = ns['head'](ns['BODY_CSS']())
body = ns['TOPBAR'] + ns['HEADER'] + '<main>' + html + '</main>'
(OUT / 'home.html').write_text(ns['page']('Startseite v3', head, body, 'template-index'), encoding='utf-8')
print('home', len(html), '->', OUT / 'home.html')
