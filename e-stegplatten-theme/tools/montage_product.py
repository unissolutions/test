#!/usr/bin/env python3
"""Baut die productSet-Eingaben für die beiden Montage-Produkte aus einer Preistabelle.

  montage_product.py <preise.csv> [--at 1.35]  -> schreibt content/montage/productset_steg.json + productset_vsg.json

preise.csv (Semikolon, Preise in EUR brutto, Deutschland):
  Breite;Tiefe;Stegplatten;VSG
  3,00 Meter;2,00 Meter;402,00;582,00
Werte für Breite/Tiefe exakt wie die Dach-Varianten („5,00 Meter“). Österreich = DE × Faktor (Standard 1,35), auf Cent gerundet.
Die Produkte sind nicht einzeln kaufbar: snippets/es-led-guard leitet die Produktseite um und entfernt Montage ohne Dach aus dem Warenkorb."""
import csv, json, pathlib, sys
from decimal import Decimal, ROUND_HALF_UP

B = pathlib.Path('/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad/content/montage')
B.mkdir(parents=True, exist_ok=True)
src = pathlib.Path(sys.argv[1])
at = Decimal(sys.argv[sys.argv.index('--at') + 1]) if '--at' in sys.argv else Decimal('1.35')


def eur(s):
    return Decimal(str(s).replace('.', '').replace(',', '.')) if ',' in str(s) else Decimal(str(s))


rows = list(csv.DictReader(src.open(encoding='utf-8'), delimiter=';'))
assert rows and {'Breite', 'Tiefe', 'Stegplatten', 'VSG'} <= set(rows[0]), 'Spalten: Breite;Tiefe;Stegplatten;VSG'
W = list(dict.fromkeys(r['Breite'].strip() for r in rows))
D = list(dict.fromkeys(r['Tiefe'].strip() for r in rows))

PRODUCTS = {
    'Stegplatten': ('montage-terrassendach-stegplatten', 'Montage Terrassendach mit Stegplatten', '16-mm-Stegplatten'),
    'VSG': ('montage-terrassendach-vsg-glas', 'Montage Terrassendach mit VSG-Glas', '8-mm-VSG-Glas'),
}
for col, (handle, title, dach) in PRODUCTS.items():
    variants = []
    for r in rows:
        de = eur(r[col])
        for land, f in (('Deutschland', Decimal(1)), ('Österreich', at)):
            price = (de * f).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            variants.append({'optionValues': [{'optionName': 'Breite', 'name': r['Breite'].strip()}, {'optionName': 'Tiefe', 'name': r['Tiefe'].strip()}, {'optionName': 'Land', 'name': land}],
                             'price': str(price), 'taxable': True, 'inventoryPolicy': 'CONTINUE',
                             'inventoryItem': {'tracked': False, 'requiresShipping': False},
                             'sku': f'MONT-{col[:3].upper()}-{int(float(r["Breite"].split()[0].replace(",", ".")) * 100)}x{int(float(r["Tiefe"].split()[0].replace(",", ".")) * 100)}-{"AT" if land == "Österreich" else "DE"}'})
    inp = {'title': title, 'handle': handle, 'productType': 'Montage', 'vendor': 'e-Stegplatten', 'status': 'ACTIVE',
           'tags': ['Montage', 'Nicht einzeln kaufbar'],
           'descriptionHtml': f'<p>Montage Ihrer Alu-Terrassenüberdachung mit {dach} durch unser eigenes Montageteam – im Umkreis von ca. 300 km um Gelsenkirchen sowie in Österreich. Der Preis richtet sich nach Dachgröße und Land und wird auf der Produktseite des Daches nach Eingabe der Postleitzahl angezeigt.</p><p>Die Montage ist nur zusammen mit einem Terrassendach buchbar. Den Termin stimmen wir nach der Bestellung mit Ihnen ab. Fundamente und Wanddübel sind nicht enthalten.</p>',
           'productOptions': [{'name': 'Breite', 'position': 1, 'values': [{'name': w} for w in W]},
                              {'name': 'Tiefe', 'position': 2, 'values': [{'name': d} for d in D]},
                              {'name': 'Land', 'position': 3, 'values': [{'name': 'Deutschland'}, {'name': 'Österreich'}]}],
           'variants': variants}
    out = B / f'productset_{col.lower()}.json'
    out.write_text(json.dumps({'input': inp, 'synchronous': True}, ensure_ascii=False, indent=1), encoding='utf-8')
    print(out.name, len(variants), 'Varianten', '(max. 100 je Produkt ohne erweitertes Variantenmodell)' if len(variants) > 100 else '')
