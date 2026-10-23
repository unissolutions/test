#!/usr/bin/env python3
"""Vergleicht Ratgeber-Artikel aus Shopify-Antwortdatei mit content/ratgeber/_upload/articles.json."""
import json,sys,difflib,re
B='/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad/content/ratgeber/_upload/articles.json'
want={a['handle']:a for a in json.load(open(B,encoding='utf-8'))}
nodes=json.load(open(sys.argv[1]))['data']['blog']['articles']['nodes']
ok=True
for n in nodes:
    w=want.get(n['handle'])
    if not w: continue
    bad=[]
    N=lambda x: re.sub(r'\s*\n\s*','',x)
    for k,h in [('title',n['title']),('body',n['body']),('summary',n['summary'])]:
        if N(w[k])!=N(h): bad.append((k,N(w[k]),N(h)))
    if n['isPublished']: bad.append(('isPublished','False','True'))
    if sorted(n['tags'])!=sorted(w['tags']): bad.append(('tags',str(w['tags']),str(n['tags'])))
    have={(m['namespace'],m['key']):m['value'] for m in n['metafields']['nodes']}
    for m in w['metafields']:
        h=have.get((m['namespace'],m['key']))
        same = h is not None and (json.loads(h)==json.loads(m['value']) if m['type']=='json' else h==m['value'])
        if not same: bad.append((m['key'],m['value'],h or ''))
    print(('✓' if not bad else '✗'),n['handle'],n['id'])
    for k,a,b in bad:
        ok=False
        for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
            if op!='equal': print(f'   {k}: {op} soll={a[max(0,i1-25):i2+25]!r}\n          ist={b[max(0,j1-25):j2+25]!r}')
print('ALLES IDENTISCH' if ok else 'ABWEICHUNGEN')
