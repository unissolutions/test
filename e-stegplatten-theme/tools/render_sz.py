#!/usr/bin/env python3
"""Rendert snippets/es-steg-zubehoer.liquid (Komplettset selbst zusammenstellen) mit echten Zubehör-Daten (content/set-rechner/zubehoer.json)
und einem 16-mm-Stegplatten-Produkt in eine Testseite (design-review/v3/sz.html). Aufruf: render_sz.py [orig|new]"""
import json, re, sys, pathlib
from mockdata import make_env, PH
S = pathlib.Path('/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad')
which = sys.argv[1] if len(sys.argv) > 1 else 'new'
src = (S / f'theme/v3/{which}/snippets/es-steg-zubehoer.liquid').read_text(encoding='utf-8')
Z = json.load(open(S / 'content/set-rechner/zubehoer.json', encoding='utf-8'))
TITLES = {'mittelprofil': 'Mittelprofil Alu-Alu Premium 60mm breit – für 16mm Stegplatten', 'randprofil': 'Randprofil Alu-Alu Premium 60mm breit – für 16mm Stegplatten',
          'uprofil': 'U-Profil Abschlussprofil Premium Alu pressblank für 16mm Stegplatten mit Tropfkante', 'antidust': 'Anti Dust Tape / Diffusionsband selbstklebend 43mm breit für den Verschluss von Stegplatten',
          'haltewinkel': 'Abrutsch – und Haltewinkel Aluminium pressblank für 16mm - 25mm Stegplatten', 'schraube_unten_holz': 'Edelstahlschraube 4,5×35 zur Befestigung des Unterprofils auf Holz-Unterkonstruktion',
          'schraube_unten_metall': 'Bohrschraube Edelstahl 4,2×32 zur Befestigung des Profilunterteils auf der Metallunterkonstruktion', 'schraube_oben_metall': 'Edelstahlschraube 6,3×32 Befestigung des Oberteils auf dem Unterprofil',
          'schraube_haltewinkel': 'Edelstahlschraube 4,2×16 TORX zur Befestigung der Haltewinkel und Unterprofil auf Metall', 'silikon': 'Spezial Silikon', 'wandanschluss': 'Wandanschlußprofil Premium Alu-pressblank inkl. hellgrauer Dichtlippe'}
PRICES = {'mittelprofil': {'2000mm': 2580, '2500mm': 3225, '3000mm': 3870, '3500mm': 4515, '4000mm': 5160, '4500mm': 5805, '5000mm': 6450, '6000mm': 7740, '7000mm': 9030}}
def zprod(key):
    z = Z[key]; vs = []
    for i, (vt, vid) in enumerate(z['variants'].items()):
        title = vt if key != 'antidust' else vt + ' / für 16mm Stegplatten'
        if key == 'silikon': title = 'Default Title'
        price = PRICES.get(key, {}).get(vt, 500 + i * 100)
        vs.append({'id': vid, 'price': price, 'title': title, 'available': True})
    return {'title': TITLES[key], 'available': True, 'featured_image': {'alt': ''}, 'url': '/products/' + z['handle'], 'variants': vs}
ZC = {'url': '/collections/profile-zubehor-fur-16mm', 'products': [zprod(k) for k in TITLES]}
L = ['2000mm', '2500mm', '3000mm', '3500mm', '4000mm', '4500mm', '5000mm', '6000mm', '7000mm']; W = ['980mm', '1200mm']
P16 = {'2000mm/980mm': 3450, '2000mm/1200mm': 4230, '3000mm/980mm': 5180, '3000mm/1200mm': 6340, '5000mm/980mm': 8630}
variants = [{'id': 52732477079889 + i, 'options': [l, w], 'price': P16.get(f'{l}/{w}', 4000 + i * 500), 'available': True, 'title': f'{l} / {w}'} for i, (l, w) in enumerate((l, w) for l in L for w in W)]
product = {'title': 'Doppelstegplatten 16 mm Polycarbonat X-Struktur klar/farblos', 'tags': ['16mm Stegplatten', 'Polycarbonat'], 'metafields': {'custom': {'plattenstarke': '16mm'}},
           'options_with_values': [{'name': 'Länge', 'values': L}, {'name': 'Breite', 'values': W}], 'variants': variants}
class Cols(dict):
    def __missing__(self, k): return {'products': [], 'url': '/collections/' + k}
env = make_env({})
html = env.from_string(src).render(product=product, collections=Cols({'profile-zubehor-fur-16mm': ZC}))
qty_css = re.search(r'<style[^>]*>.*?</style>', (S / 'theme/v3/fetched/snippets/es-pdp-qty.liquid').read_text(encoding='utf-8'), re.S).group(0)
ds_css = '<link rel="stylesheet" href="../../theme/v3/orig/assets/es-design-system.css">'
assert 'es-sz-tpl' in html and '{{' not in html, 'Rechner nicht gerendert'
vid = [v for v in variants if v['options'] == ['2000mm', '1200mm']][0]['id']
opts = ''.join(f'<option value="{v["id"]}">{v["title"]}</option>' for v in variants)
page = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Komplettset-Rechner</title>
{ds_css}{qty_css}<style>body{{margin:0;font-family:Archivo,system-ui,sans-serif}}.col{{max-width:var(--col,400px);margin:0 auto;padding:16px}}@media(max-width:749px){{.col{{padding:16px;max-width:none}}}}</style></head><body>
<div class="col"><form class="product-form" action="/cart/add"><select name="id" id="vsel">{opts}</select> <input type="number" name="quantity" value="1" id="qty"></form><div class="product-form__payment-container">[Kaufen]</div>{html}</div>
<script>document.getElementById('vsel').value='{vid}';</script></body></html>'''
(S / 'design-review/v3/sz.html').write_text(page, encoding='utf-8'); print('sz.html', which, len(page))
