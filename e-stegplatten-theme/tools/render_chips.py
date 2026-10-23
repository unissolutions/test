#!/usr/bin/env python3
"""Mock der Kollektions-Chips (Stärke/Plattenfarbe) mit es-design-system + es-mobile (v3)."""
import pathlib
S = pathlib.Path('/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad')
chips = lambda items: ''.join(f'<a class="es-chip{" is-active" if a else ""}" href="#">{t}</a>' for t, a in items)
rows = [('Stärke', [('4,5 mm', 0), ('6 mm', 0), ('8 mm', 0), ('10 mm', 0), ('16 mm', 1)]), ('Plattenfarbe', [('Klar', 0), ('Opal / Weiß', 0), ('Anthrazit / Graphit', 0), ('Bronze', 0)])]
html = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chips</title>'
        '<link rel="stylesheet" href="../../theme/v3/orig/assets/es-design-system.css"><link rel="stylesheet" href="../../theme/v3/new/assets/es-mobile.css">'
        '<style>body{margin:0;font-family:Archivo,system-ui,sans-serif;background:#fff}</style></head><body><div class="es-chips">'
        + ''.join(f'<div class="es-chips__row"><span class="es-chips__label">{l}</span><div class="es-chips__list">{chips(it)}</div></div>' for l, it in rows) + '</div></body></html>')
(S / 'design-review/v3/chips.html').write_text(html, encoding='utf-8'); print('chips.html')
