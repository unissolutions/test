#!/usr/bin/env python3
"""Vergleicht Kollektions-SEO + Metafelder aus einer Shopify-Antwortdatei mit cats.jsonl.
  cat_verify.py <antwort.json>   (collections.nodes mit id, seo, descriptionHtml, metafields)"""
import json,sys,difflib
B='/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad/content/kategorien/_bulk/cats.jsonl'
want={}
for l in open(B,encoding='utf-8'):
    i=json.loads(l)['input'];want[i['id']]=i
raw=json.load(open(sys.argv[1]))
nodes=raw['data']['nodes'] if 'nodes' in raw['data'] else raw['data']['collections']['nodes']
ok=True
for n in nodes:
    if not n or n['id'] not in want: continue
    w=want[n['id']];bad=[]
    if n['seo']!=w['seo']: bad.append(('seo',json.dumps(w['seo'],ensure_ascii=False),json.dumps(n['seo'],ensure_ascii=False)))
    have={m['key']:m['value'] for m in n['metafields']['nodes'] if m['namespace']=='custom'}
    for m in w['metafields']:
        h=have.get(m['key'])
        if m['type']=='json':
            same = h is not None and json.loads(h)==json.loads(m['value'])
        else:
            same = h==m['value']
        if not same: bad.append((m['key'],m['value'],h or ''))
    if 'descriptionHtml' in w and n.get('descriptionHtml')!=w['descriptionHtml']:
        bad.append(('descriptionHtml',w['descriptionHtml'],n.get('descriptionHtml') or ''))
    print(('✓' if not bad else '✗'),n['handle'])
    for k,a,b in bad:
        ok=False
        sm=difflib.SequenceMatcher(None,a,b)
        for op,i1,i2,j1,j2 in sm.get_opcodes():
            if op!='equal': print(f'   {k}: {op} soll={a[max(0,i1-30):i2+30]!r}\n          ist={b[max(0,j1-30):j2+30]!r}')
print('ALLES IDENTISCH' if ok else 'ABWEICHUNGEN')
