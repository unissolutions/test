# Montage zubuchbar – Datenstand

## Preistabelle `preise.csv`

**Platzhalter!** Die Zahlen sind aus dem TerrassenConcept-3D-Planer abgeleitet (Zone 1: Stegplatten 67 €/m², VSG 97 €/m², jeweils × Dachfläche) und dienen nur zum Testen. Die echten Montagepreise je Dachgröße aus dem TerrassenPost-Shop bitte hier eintragen (Spalten `Stegplatten` und `VSG`, EUR brutto, Deutschland). Österreich wird automatisch mit × 1,35 berechnet.

Die Maßwerte (z. B. `5,00 Meter`) müssen exakt den Optionswerten der Dach-Produkte entsprechen – welche Breiten/Tiefen die Dächer wirklich haben, wird beim Anlegen gegen den Shop geprüft (siehe HANDOFF).

## Anlegen in Shopify

1. `python3 tools/montage_product.py content/montage/preise.csv`
2. `productSet` mit `content/montage/productset_stegplatten.json` und `productset_vsg.json` ausführen (synchron).
3. Beide Produkte im Vertriebskanal „Online Store“ veröffentlichen (`publishablePublish`), sonst lassen sie sich nicht in den Warenkorb legen.
4. Advanced Shipping Rules: Produkte ohne Versand (requiresShipping = false) dürfen keine Versandgruppe auslösen – im Testkorb „Dach + Montage“ prüfen, dass weiterhin 99 € (DE) bzw. 199 € (AT) berechnet werden.
5. Theme-Einstellung „Montagegebiet Deutschland (PLZ-Präfixe)“ prüfen. Standard: `26-35,37-38,40-62,65` (entspricht den TerrassenConcept-Zonen 1–2, bis ca. 270 km). Für „ca. 300 km“ ggf. um Präfixe der Zone 3 ergänzen (20–21, 36, 39, 63–69).

## Funktionsweise im Theme

- Produktseite Terrassendach: Block „Montage“ mit Selbstmontage / Montage durch unser Team, PLZ-Feld, Gebietsprüfung (DE 5-stellig nach Präfixliste, AT 4-stellig), Preis aus der Variante Breite × Tiefe × Land.
- Warenkorb: Montage als eigene Zeile mit Eigenschaften „Für Überdachung“ und „Montageort“, Menge = Dachmenge.
- `snippets/es-led-guard.liquid`: entfernt Montage (und LED) ohne Dach, leitet die Montage-Produktseite auf die Terrassenüberdachungen um.
- Außerhalb des Gebiets oder ohne passende Variante: Hinweis + Verweis auf „Angebot anfordern“, Warenkorb blockiert, bis Selbstmontage gewählt oder PLZ korrigiert ist.
