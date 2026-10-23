#!/usr/bin/env python3
"""Rendert sections/es-collection-seo.liquid lokal (python-liquid) mit echten Kollektionsdaten -> HTML zum Screenshot."""
import json,re,sys,pathlib
from liquid import Environment
B='/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad'
env=Environment()
env.add_filter('json',lambda v: json.dumps(v,ensure_ascii=False))
src=open(f'{B}/theme/cat/new/sections/es-collection-seo.liquid',encoding='utf-8').read()
src=re.sub(r'{% schema %}.*?{% endschema %}','',src,flags=re.S)
sch=json.loads(re.search(r'{% schema %}(.*){% endschema %}',open(f'{B}/theme/cat/new/sections/es-collection-seo.liquid',encoding='utf-8').read(),re.S).group(1))
settings={s['id']:s.get('default') for s in sch['settings'] if 'id' in s}
tpl=env.from_string(src)
css=open(f'{B}/theme/v2/new/assets/es-design-system.css',encoding='utf-8').read().split('\n')[0]
out=pathlib.Path(f'{B}/design-review/cat'); 
for l in open(f'{B}/content/kategorien/_bulk/cats.jsonl',encoding='utf-8'):
    i=json.loads(l)['input']; mf={m['key']:m['value'] for m in i['metafields']}
    h=[x for x in ['doppelstegplatten-16mm','doppelstegplatten','hohlkammerplatten','gewachshausplatten'] if x in i['seo']['title'].lower().replace(' ','-') or True][0]
    handle=i['id'].split('/')[-1]
    coll={'title':i['seo']['title'].split(' |')[0].split(':')[0],'description':'',
          'metafields':{'custom':{'seo_text':{'value':mf['seo_text']},'seo_faq':{'value':json.loads(mf['seo_faq'])}}}}
    html=tpl.render(section={'id':'t1','settings':settings},collection=coll)
    page=f'<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..800&display=swap" rel="stylesheet"><style>{css}body{{margin:0;font-family:Archivo,system-ui,sans-serif;background:#fff}}</style></head><body>{html}</body></html>'
    (out/f'{handle}.html').write_text(page,encoding='utf-8')
    # JSON-LD validieren
    ld=re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)
    n=len(json.loads(ld.group(1))['mainEntity']) if ld else 0
    print(handle, len(html), 'FAQ-LD', n, 'details', html.count('<details'))
