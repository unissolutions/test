"""Beispieldaten + Liquid-Umgebung (python-liquid) zum lokalen Rendern der e-Stegplatten-Theme-Dateien.
Genutzt von render_v3.py (Produktseite, Hero) und render_home.py (Startseite)."""
import json, re, pathlib, urllib.parse
from liquid import Environment, DictLoader

S = pathlib.Path('/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad')
V3 = S / 'theme/v3/new'

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
    return {'id': pid, 'title': title, 'url': url, 'handle': url.split('/')[-1], 'available': True, 'price': vs[0]['price'], 'compare_at_price': None,
            'featured_image': {'alt': title, 'width': 800, 'height': 600}, 'images': [{'alt': title}],
            'options_with_values': [{'name': 'Breite', 'values': W}, {'name': 'Tiefe', 'values': D}],
            'variants': vs, 'selected_or_first_available_variant': sel, 'first_available_variant': sel,
            'media': [{'media_type': 'image', 'alt': '', 'width': 1200, 'height': 900, 'id': k} for k in range(3)],
            'metafields': {'reviews': {'rating_count': 12}, 'judgeme': {'badge': '<span style="color:#D9962B">★★★★★</span> <span style="color:#5E6863;font-size:13px">12 Bewertungen</span>'},
                           'custom': {'garantie_aluminium': {'value': '10 Jahre'}, 'garantie_stegplatten': {'value': '10 Jahre'}}},
            'collections': [{'metafields': {'custom': {'lieferzeit': {'value': 'ca. 10–40 Werktage'}}}}]}


P = roof(11, 'Terrassenüberdachung Premium Anthrazit Alu mit Stegplatten 16mm klar/farblos', '/products/dach-anthrazit-klar')
P_W = roof(12, 'Terrassenüberdachung Premium Weiß Alu mit Stegplatten 16mm klar/farblos', '/products/dach-weiss-klar')
P_O = roof(13, 'Terrassenüberdachung Premium Anthrazit Alu mit Stegplatten 16mm opal/weiß', '/products/dach-anthrazit-opal')
P_G = roof(14, 'Terrassenüberdachung Premium Anthrazit Alu mit Stegplatten 16mm graphit', '/products/dach-anthrazit-graphit')
KC = {'products': [P, P_W, P_O, P_G], 'url': '/collections/terrassenuberdachung-alu-mit-stegplatten', 'title': 'Terrassenüberdachung Alu mit Stegplatten', 'products_count': 4, 'all_products_count': 4}
GENERIC_COL = {'products': [P, P_W, P_O, P_G], 'url': '/collections/doppelstegplatten-16mm', 'title': 'Doppelstegplatten 16 mm', 'products_count': 16, 'all_products_count': 16}
LED = {'id': 9, 'handle': 'led-spots-terrassenueberdachung', 'available': True, 'featured_image': None,
       'variants': [{'id': 901, 'title': '6er-Set', 'price': 20000, 'available': True, 'image': None},
                    {'id': 902, 'title': '12er-Set', 'price': 35000, 'available': True, 'image': None},
                    {'id': 903, 'title': '18er-Set', 'price': 50000, 'available': True, 'image': None}]}
ZONES = [('Zone 1', 6700, 9700), ('Zone 2', 8250, 11200), ('Zone 3', 9700, 12700), ('Zone 4', 11200, 14200), ('Österreich', 15120, 19170)]  # €/m² in Cent


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
ROUTES = {'root_url': '/', 'cart_add_url': '/cart/add', 'cart_url': '/cart', 'collections_url': '/collections', 'search_url': '/search'}
SHOP = {'name': 'e-Stegplatten', 'url': 'https://e-stegplatten.de', 'metafields': {'judgeme': {'all_reviews_count': 212, 'all_reviews_rating': '4.9'}}}


class Cols(dict):
    """collections['handle'] liefert für unbekannte Handles eine Beispielkollektion."""
    def __missing__(self, k):
        return GENERIC_COL

    def get(self, k, d=None):
        return self[k]


PH = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='600'%3E%3Crect width='800' height='600' fill='%23D9DEDB'/%3E%3Ctext x='400' y='310' text-anchor='middle' font-family='sans-serif' font-size='28' fill='%235E6863'%3EProduktbild%3C/text%3E%3C/svg%3E"
_HERO_SVG = """<svg xmlns='http://www.w3.org/2000/svg' width='1400' height='1050' viewBox='0 0 1400 1050'>
<defs><linearGradient id='sky' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#9CC7E8'/><stop offset='1' stop-color='#E8F1F6'/></linearGradient>
<linearGradient id='lawn' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#7FB069'/><stop offset='1' stop-color='#4E8A3C'/></linearGradient>
<linearGradient id='wall' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#F1EEE6'/><stop offset='1' stop-color='#D9D3C6'/></linearGradient></defs>
<rect width='1400' height='1050' fill='url(#sky)'/><rect y='700' width='1400' height='350' fill='url(#lawn)'/>
<rect x='0' y='120' width='520' height='620' fill='url(#wall)'/><rect x='80' y='220' width='160' height='220' fill='#B9D4E6' stroke='#9FB2BE' stroke-width='6'/>
<polygon points='300,240 1250,330 1250,380 300,300' fill='#D7E6F0' fill-opacity='.85'/>
<g stroke='#3B4043' stroke-width='10'><line x1='300' y1='300' x2='1250' y2='380'/><line x1='300' y1='240' x2='1250' y2='330'/><line x1='520' y1='262' x2='520' y2='720'/><line x1='1240' y1='380' x2='1240' y2='720'/><line x1='860' y1='324' x2='860' y2='720'/></g>
<g stroke='#3B4043' stroke-width='4' stroke-opacity='.55'>%s</g>
<rect x='520' y='560' width='720' height='160' fill='#C9B79C'/><rect x='560' y='500' width='110' height='70' fill='#7A6A55'/><rect x='700' y='500' width='110' height='70' fill='#7A6A55'/>
</svg>""" % ''.join(f"<line x1='{300+ (1250-300)*k/12:.0f}' y1='{240+90*k/12:.0f}' x2='{300+(1250-300)*k/12:.0f}' y2='{300+80*k/12:.0f}'/>" for k in range(1, 12))
HERO = 'data:image/svg+xml,' + urllib.parse.quote(_HERO_SVG)


def money(c):
    try:
        c = float(c)
    except (TypeError, ValueError):
        return ''
    return f'{c/100:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def handle(s):
    s = str(s).lower().replace('ß', 'ss').replace('ä', 'a').replace('ö', 'o').replace('ü', 'u')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def load_snippet(name):
    for base in (V3 / 'snippets', S / 'theme/v3/orig/snippets', S / 'theme/v2/new/snippets'):
        p = base / f'{name}.liquid'
        if p.exists():
            return p.read_text(encoding='utf-8')
    raise FileNotFoundError(name)


def make_env(snippets):
    env = Environment(loader=DictLoader(snippets))
    env.add_filter('json', lambda v: json.dumps(v, ensure_ascii=False))
    env.add_filter('image_url', lambda v, width=None: HERO if isinstance(v, dict) and v.get('hero') else PH)
    env.add_filter('money_without_currency', money)
    env.add_filter('money', lambda v: money(v) + ' €')
    env.add_filter('handle', handle)
    env.add_filter('handleize', handle)
    env.add_filter('default_errors', lambda v: '')
    env.add_filter('url_encode', lambda v: urllib.parse.quote_plus(str(v)))
    env.add_filter('t', lambda v, **kw: str(v))
    return env


def frame():
    """Seitenrahmen (Fonts, Design-System-CSS, Mock-Header) aus design-review/v2/tools/build_v2.py."""
    b2 = (S / 'design-review/v2/tools/build_v2.py').read_text(encoding='utf-8')
    b2 = b2.replace("home('konfig'); home('finder'); pdp(); pdp(led=True, sticky=True); collection()", '')
    ns = {}
    exec(compile(b2, 'build_v2', 'exec'), ns)
    return ns


def read_index():
    raw = (V3 / 'templates/index.json').read_text(encoding='utf-8')
    return json.loads(raw[re.match(r'\s*/\*.*?\*/\s*', raw, re.S).end():])
