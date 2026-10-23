#!/usr/bin/env python3
"""Rendert die echten v3-Liquid-Dateien (Produktseite Terrassendach + Hero-Konfigurator) mit python-liquid
und Beispieldaten zu lauffähigen HTML-Seiten (design-review/v3/). Grundlage für Playwright-Tests und Screenshots."""
import json, re, pathlib, sys
from liquid import Environment, DictLoader

S = pathlib.Path('/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad')
V3 = S / 'theme/v3/new'
OUT = S / 'design-review/v3'
OUT.mkdir(parents=True, exist_ok=True)

# ---- Beispieldaten ----------------------------------------------------------------
W = ['3,00 Meter', '4,00 Meter', '5,00 Meter', '6,00 Meter', '7,00 Meter']
D = ['2,00 Meter', '2,50 Meter', '3,00 Meter', '3,50 Meter', '4,00 Meter', '4,50 Meter', '5,00 Meter']


def num(s):
    return float(s.replace(' Meter', '').replace(',', '.'))


def roof(pid, title, url, rate=12466):
    vs = []
    for i, (w, d) in enumerate([(w, d) for w in W for d in D]):
        vs.append({'id': pid * 1000 + i, 'title': f'{w} / {d}', 'price': round(num(w) * num(d) * rate), 'compare_at_price': None,
                   'available': not (w == '7,00 Meter' and d == '5,00 Meter'), 'sku': f'TU-{pid}-{int(num(w)*100)}x{int(num(d)*100)}', 'options': [w, d]})
    sel = [v for v in vs if v['options'] == ['5,00 Meter', '3,00 Meter']][0]
    return {'id': pid, 'title': title, 'url': url, 'handle': url.split('/')[-1], 'available': True,
            'options_with_values': [{'name': 'Breite', 'values': W}, {'name': 'Tiefe', 'values': D}],
            'variants': vs, 'selected_or_first_available_variant': sel,
            'media': [{'media_type': 'image', 'alt': '', 'width': 1200, 'height': 900, 'id': k} for k in range(3)],
            'metafields': {'reviews': {'rating_count': 12}, 'judgeme': {'badge': '<span style="color:#D9962B">★★★★★</span> <span style="color:#5E6863;font-size:13px">12 Bewertungen</span>'},
                           'custom': {'garantie_aluminium': {'value': '10 Jahre'}, 'garantie_stegplatten': {'value': '10 Jahre'}}},
            'collections': [{'metafields': {'custom': {'lieferzeit': {'value': 'ca. 10–40 Werktage'}}}}]}


P = roof(11, 'Terrassenüberdachung Premium Anthrazit Alu mit Stegplatten 16mm klar/farblos', '/products/dach-anthrazit-klar')
P_W = roof(12, 'Terrassenüberdachung Premium Weiß Alu mit Stegplatten 16mm klar/farblos', '/products/dach-weiss-klar')
P_O = roof(13, 'Terrassenüberdachung Premium Anthrazit Alu mit Stegplatten 16mm opal/weiß', '/products/dach-anthrazit-opal')
P_G = roof(14, 'Terrassenüberdachung Premium Anthrazit Alu mit Stegplatten 16mm graphit', '/products/dach-anthrazit-graphit')
KC = {'products': [P, P_W, P_O, P_G]}
LED = {'id': 9, 'handle': 'led-spots-terrassenueberdachung', 'available': True, 'featured_image': None,
       'variants': [{'id': 901, 'title': '6er-Set', 'price': 20000, 'available': True, 'image': None},
                    {'id': 902, 'title': '12er-Set', 'price': 35000, 'available': True, 'image': None},
                    {'id': 903, 'title': '18er-Set', 'price': 50000, 'available': True, 'image': None}]}


ZONES = [('Zone 1', 6700, 9700), ('Zone 2', 8250, 11200), ('Zone 3', 9700, 12700), ('Zone 4', 11200, 14200), ('Österreich', 15120, 19170)]  # €/m² in Cent (TerrassenConcept-Preisliste; AT = Zone 4 × 1,35)


def montage(pid, col):
    vs, i = [], 0
    for w in W:
        for d in D:
            for zn, rs, rv in ZONES:
                vs.append({'id': pid * 1000 + i, 'price': round(num(w) * num(d) * (rs if col == 'steg' else rv)), 'available': not (w == '7,00 Meter' and d == '5,00 Meter'), 'options': [w, d, zn]})
                i += 1
    return {'id': pid, 'available': True, 'options_with_values': [{'name': 'Breite', 'values': W}, {'name': 'Tiefe', 'values': D}, {'name': 'Zone', 'values': [z[0] for z in ZONES]}], 'variants': vs}


MO_S = montage(7, 'steg')
MO_V = montage(8, 'vsg')
ALL = {'led-spots-terrassenueberdachung': LED, 'montage-terrassendach-stegplatten': MO_S, 'montage-terrassendach-vsg-glas': MO_V}
COLS = {'terrassenuberdachung-alu-mit-stegplatten': KC, 'terrassenuberdachung-alu-mit-vsg-glas': {'products': []}}
ROUTES = {'root_url': '/', 'cart_add_url': '/cart/add', 'cart_url': '/cart', 'collections_url': '/collections'}

# ---- Liquid-Umgebung --------------------------------------------------------------
PH = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='600'%3E%3Crect width='800' height='600' fill='%23D9DEDB'/%3E%3Ctext x='400' y='310' text-anchor='middle' font-family='sans-serif' font-size='28' fill='%235E6863'%3EProduktbild%3C/text%3E%3C/svg%3E"


def money(c):
    try:
        c = float(c)
    except (TypeError, ValueError):
        return ''
    return f'{c/100:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def handle(s):
    s = str(s).lower().replace('ß', 'ss').replace('ä', 'a').replace('ö', 'o').replace('ü', 'u')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


src = {}
for n in ['es-pdp-css', 'es-pdp-js', 'es-hero-konfig', 'es-landing-css']:
    src[n] = (V3 / 'snippets' / f'{n}.liquid').read_text(encoding='utf-8') if (V3 / 'snippets' / f'{n}.liquid').exists() else (S / 'theme/v2/new/snippets' / f'{n}.liquid').read_text(encoding='utf-8')
env = Environment(loader=DictLoader(src))
env.add_filter('json', lambda v: json.dumps(v, ensure_ascii=False))
env.add_filter('image_url', lambda v, width=None: PH)
env.add_filter('money_without_currency', money)
env.add_filter('handle', handle)
env.add_filter('default_errors', lambda v: '')
env.add_filter('url_encode', lambda v: __import__('urllib.parse').parse.quote_plus(str(v)))

sec_src = (V3 / 'sections/es-pdp-terrasse.liquid').read_text(encoding='utf-8')
schema = json.loads(re.search(r'{% schema %}(.*){% endschema %}', sec_src, re.S).group(1))
settings = {s['id']: s.get('default') for s in schema['settings'] if 'id' in s}
settings['led_product'] = LED  # python-liquid kennt `nil == blank` nicht; der Shopify-Fallback ist bereits live geprüft
sec_src = re.sub(r'{% schema %}.*{% endschema %}', '', sec_src, flags=re.S)
sec_src = re.sub(r"{%-?\s*form 'contact', id: 'es-offer-form', class: 'es-pdp__of'\s*-?%}",
                 '<form method="post" action="/contact#es-offer-form" id="es-offer-form" class="es-pdp__of" accept-charset="UTF-8"><input type="hidden" name="form_type" value="contact"><input type="hidden" name="utf8" value="✓">', sec_src)
sec_src = re.sub(r'{%-?\s*endform\s*-?%}', '</form>', sec_src)
sec_src = sec_src.replace('form.posted_successfully?', 'form.posted')
assert '{%- form' not in sec_src and 'endform' not in sec_src

ctx = {'product': P, 'section': {'id': 'x', 'settings': settings, 'blocks': []}, 'all_products': ALL, 'collections': COLS,
       'routes': ROUTES, 'form': {'posted': False, 'errors': False}}
html_pdp = env.from_string(sec_src).render(**ctx)
assert '{{' not in html_pdp and '{%' not in html_pdp, 'ungelöstes Liquid in der Produktseite'

# ---- Seitenrahmen aus build_v2 (Fonts, Design-System, Mock-Header) -------------------
b2 = (S / 'design-review/v2/tools/build_v2.py').read_text(encoding='utf-8')
b2 = b2.replace("home('konfig'); home('finder'); pdp(); pdp(led=True, sticky=True); collection()", '')
ns = {}
exec(compile(b2, 'build_v2', 'exec'), ns)
MOCK = ("<script>window.__calls=[];window.theme={cartType:'drawer',pageType:'product',cartCount:0};window.routes={rootUrl:'/',rootUrlWithoutSlash:'',cartUrl:'/cart',cartAddUrl:'/cart/add'};"
        "window.fetch=function(u,o){__calls.push({u:String(u),body:o&&o.body?JSON.parse(o.body):null});return Promise.resolve({ok:true,json:function(){return Promise.resolve({})}})};"
        "try{localStorage.clear()}catch(e){}</script>")
head = ns['head'](ns['BODY_CSS']() + [ns['styles']('snippets/es-overrides-pdp.liquid'), ns['PDPFULL']]) + MOCK
body = ns['TOPBAR'] + ns['HEADER'] + '<main>' + html_pdp + '</main>'
(OUT / 'pdp.html').write_text(ns['page']('Terrassendach v3', head, body, 'template-product'), encoding='utf-8')

# ---- Hero-Konfigurator ---------------------------------------------------------------
hero_html = env.get_template('es-hero-konfig').render(kc=KC, lz='ca. 10–40 Werktage', mu='/products/farbmuster', all_products=ALL)
assert '{{' not in hero_html and '{%' not in hero_html
hhead = ns['head'](ns['BODY_CSS']() + [ns['styles']('snippets/es-landing-css.liquid')])
hbody = ns['TOPBAR'] + ns['HEADER'] + '<main><section class="esl" id="esl-x"><div class="c" style="max-width:640px;margin:0 auto;padding:24px 16px">' + hero_html + '</div></section></main>'
(OUT / 'hero.html').write_text(ns['page']('Hero v3', hhead, hbody), encoding='utf-8')
print('pdp', len(html_pdp), 'hero', len(hero_html), '->', OUT)
