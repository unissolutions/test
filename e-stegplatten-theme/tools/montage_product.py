#!/usr/bin/env python3
"""Baut die productSet-Eingaben für die beiden Montage-Produkte (Stegplatten / VSG-Glas) aus der Zonentabelle.

  montage_product.py [content/montage/zonen.csv] [--sizes sizes.csv]

zonen.csv (Semikolon):  Zone;PLZ;Beschreibung;Stegplatten;VSG   – €/m² brutto je Zone, PLZ = 2-stellige Präfixe/Bereiche oder AT
sizes.csv (optional):   Breite;Tiefe  – Optionswerte exakt wie bei den Dächern („5,00 Meter“); Standard: 3–7 m × 2–5 m (0,5-m-Schritte)

Preis je Variante = Breite × Tiefe × €/m², auf Cent gerundet. Option „Zone“ = Zonenname; er muss der Theme-Einstellung
„Montagezonen“ entsprechen (diese Zeilen schreibt das Skript zusätzlich nach zonen_theme.txt).
Nicht einzeln kaufbar: snippets/es-led-guard leitet die Produktseiten um und entfernt Montage ohne Dach aus dem Warenkorb."""
import csv, json, pathlib, sys
from decimal import Decimal, ROUND_HALF_UP

B = pathlib.Path('/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad/content/montage')
args = [a for a in sys.argv[1:] if not a.startswith('--')]
zon = pathlib.Path(args[0]) if args else B / 'zonen.csv'
sizes = None
if '--sizes' in sys.argv:
    sizes = [(r['Breite'].strip(), r['Tiefe'].strip()) for r in csv.DictReader(open(sys.argv[sys.argv.index('--sizes') + 1], encoding='utf-8'), delimiter=';')]
else:
    W = ['3,00 Meter', '4,00 Meter', '5,00 Meter', '6,00 Meter', '7,00 Meter']
    D = ['2,00 Meter', '2,50 Meter', '3,00 Meter', '3,50 Meter', '4,00 Meter', '4,50 Meter', '5,00 Meter']
    sizes = [(w, d) for w in W for d in D]


def dec(s):
    return Decimal(str(s).strip().replace('.', '').replace(',', '.'))


def metres(s):
    return Decimal(s.split()[0].replace(',', '.'))


zones = list(csv.DictReader(zon.open(encoding='utf-8'), delimiter=';'))
assert zones and {'Zone', 'PLZ', 'Stegplatten', 'VSG'} <= set(zones[0]), 'Spalten: Zone;PLZ;Beschreibung;Stegplatten;VSG'
widths = list(dict.fromkeys(w for w, _ in sizes))
depths = list(dict.fromkeys(d for _, d in sizes))

PRODUCTS = {'Stegplatten': ('montage-terrassendach-stegplatten', 'Montage Terrassendach mit Stegplatten', '16-mm-Stegplatten'),
            'VSG': ('montage-terrassendach-vsg-glas', 'Montage Terrassendach mit VSG-Glas', '8-mm-VSG-Glas')}
for col, (handle, title, dach) in PRODUCTS.items():
    variants = []
    for w, d in sizes:
        for z in zones:
            price = (metres(w) * metres(d) * dec(z[col])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            zk = ''.join(c for c in z['Zone'].upper().replace('Ä', 'AE').replace('Ö', 'OE').replace('Ü', 'UE').replace('ß', 'SS') if c.isalnum() and c.isascii())[:8]
            variants.append({'optionValues': [{'optionName': 'Breite', 'name': w}, {'optionName': 'Tiefe', 'name': d}, {'optionName': 'Zone', 'name': z['Zone'].strip()}],
                             'price': str(price), 'taxable': True, 'inventoryPolicy': 'CONTINUE',
                             'inventoryItem': {'tracked': False, 'requiresShipping': False},
                             'sku': f'MONT-{col[:3].upper()}-{int(metres(w) * 100)}x{int(metres(d) * 100)}-{zk}'})
    inp = {'title': title, 'handle': handle, 'productType': 'Montage', 'vendor': 'e-Stegplatten', 'status': 'ACTIVE',
           'tags': ['Montage', 'Nicht einzeln kaufbar'],
           'descriptionHtml': f'<p>Montage Ihrer Alu-Terrassenüberdachung mit {dach} durch unser eigenes Montageteam. Der Preis richtet sich nach Dachfläche und Entfernung (Montagezone nach Postleitzahl) und wird auf der Produktseite des Daches nach Eingabe der PLZ angezeigt.</p><p>Die Montage ist nur zusammen mit einem Terrassendach buchbar. Den Termin stimmen wir nach der Bestellung mit Ihnen ab. Fundamente und Wanddübel sind nicht enthalten.</p>',
           'productOptions': [{'name': 'Breite', 'position': 1, 'values': [{'name': w} for w in widths]},
                              {'name': 'Tiefe', 'position': 2, 'values': [{'name': d} for d in depths]},
                              {'name': 'Zone', 'position': 3, 'values': [{'name': z['Zone'].strip()} for z in zones]}],
           'variants': variants}
    out = B / f'productset_{col.lower()}.json'
    out.write_text(json.dumps({'input': inp, 'synchronous': True}, ensure_ascii=False, indent=1), encoding='utf-8')
    print(out.name, len(variants), 'Varianten' + (' – über 100: braucht das erweiterte Variantenmodell (bis 2.048), sonst je Zone ein Produkt' if len(variants) > 100 else ''))

theme_lines = '\n'.join(f"{z['Zone'].strip()}|{z['PLZ'].strip()}|{(z.get('Beschreibung') or '').strip()}" for z in zones)
(B / 'zonen_theme.txt').write_text(theme_lines + '\n', encoding='utf-8')
print('Theme-Einstellung „Montagezonen“:\n' + theme_lines)
