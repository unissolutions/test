#!/usr/bin/env python3
"""Rendert die echten v3-Liquid-Dateien (Produktseite Terrassendach + Hero-Konfigurator) mit python-liquid
und Beispieldaten (mockdata.py) zu lauffähigen HTML-Seiten (design-review/v3/). Grundlage für Playwright-Tests und Screenshots."""
import json, re
from mockdata import *  # noqa: F401,F403

OUT = S / 'design-review/v3'
OUT.mkdir(parents=True, exist_ok=True)
env = make_env({n: load_snippet(n) for n in ['es-pdp-css', 'es-pdp-js', 'es-hero-konfig', 'es-landing-css']})

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

ns = frame()
MOCK = ("<script>window.__calls=[];window.theme={cartType:'drawer',pageType:'product',cartCount:0};window.routes={rootUrl:'/',rootUrlWithoutSlash:'',cartUrl:'/cart',cartAddUrl:'/cart/add'};"
        "window.fetch=function(u,o){__calls.push({u:String(u),body:o&&o.body?JSON.parse(o.body):null});return Promise.resolve({ok:true,json:function(){return Promise.resolve({})}})};"
        "try{localStorage.clear()}catch(e){}</script>")
head = ns['head'](ns['BODY_CSS']() + [ns['styles']('snippets/es-overrides-pdp.liquid'), ns['PDPFULL']]) + MOCK
body = ns['TOPBAR'] + ns['HEADER'] + '<main>' + html_pdp + '</main>'
(OUT / 'pdp.html').write_text(ns['page']('Terrassendach v3', head, body, 'template-product'), encoding='utf-8')

hero_html = env.get_template('es-hero-konfig').render(kc=KC, lz='ca. 10–40 Werktage', mu='/products/farbmuster', all_products=ALL)
assert '{{' not in hero_html and '{%' not in hero_html
hhead = ns['head'](ns['BODY_CSS']() + [ns['styles']('snippets/es-landing-css.liquid')])
hbody = ns['TOPBAR'] + ns['HEADER'] + '<main><section class="esl" id="esl-x"><div class="c" style="max-width:640px;margin:0 auto;padding:24px 16px">' + hero_html + '</div></section></main>'
(OUT / 'hero.html').write_text(ns['page']('Hero v3', hhead, hbody), encoding='utf-8')
print('pdp', len(html_pdp), 'hero', len(hero_html), '->', OUT)
