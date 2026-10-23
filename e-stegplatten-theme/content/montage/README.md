# Montage zubuchbar – Datenstand

## Preismodell (aus der Datei „Preisliste Montage TerrassenConcept“)

Montagepreis = Breite (m) × Tiefe (m) × €/m² der Zone. Die Zone ergibt sich aus den ersten zwei Ziffern der PLZ, Zonen werden der Reihe nach geprüft, der erste Treffer gilt (PLZ 65 → Zone 2).

| Zone | Entfernung | PLZ-Präfixe | Stegplatten €/m² | VSG-Glas €/m² |
|---|---|---|---|---|
| 1 | bis 170 km | 32, 40–53, 57–59 | 67,00 | 97,00 |
| 2 | 170–270 km | 26–31, 33–35, 37–38, 54–56, 60–62, 65 | 82,50 | 112,00 |
| 3 | 270–370 km | 20–21, 36, 39, 63–69, 97–99 | 97,00 | 127,00 |
| 4 | 370–770 km | 01–19, 22–25, 70–96 | 112,00 | 142,00 |
| Österreich | 4-stellige PLZ | AT | 151,20 | 191,70 |

**Offen (siehe Fragenliste):** Österreich-Satz (hier vorläufig Zone 4 × 1,35), ob alle vier Zonen online buchbar sind oder nur bis ca. 300 km, Versand bei Montage, Leistungsumfang.

`zonen.csv` ist die einzige Quelle für die Preise. Änderungen dort → Skript erneut laufen lassen → Produkte per `productSet` aktualisieren (gleicher Handle, Varianten werden ersetzt).

## Anlegen in Shopify

1. Dachmaße prüfen: Optionswerte Breite/Tiefe der Dach-Produkte lesen; weichen sie von 3–7 m × 2–5 m (0,5-m-Schritte) ab, `--sizes sizes.csv` verwenden.
2. `python3 tools/montage_product.py content/montage/zonen.csv`
3. `productSet` mit `productset_stegplatten.json` und `productset_vsg.json` (synchron). 175 Varianten je Produkt: braucht das erweiterte Variantenmodell (bis 2.048). Lehnt Shopify das ab, je Zone ein Produkt anlegen (Handle-Schema dann in Theme-Einstellung und Wächter nachziehen).
4. Beide Produkte im Vertriebskanal „Online Store“ veröffentlichen, sonst lassen sie sich nicht in den Warenkorb legen.
5. Theme-Einstellung „Montagezonen“ (Section „ES Produkt Terrassendach“) mit dem Inhalt von `zonen_theme.txt` abgleichen (Standardwert ist identisch).
6. Advanced Shipping Rules: Montage-Produkte haben `requiresShipping = false`; Testkorb „Dach + Montage“ muss weiterhin 99 € (DE) bzw. 199 € (AT) ergeben – sofern Versand bei Montage berechnet werden soll.

## Funktionsweise im Theme

- Produktseite Terrassendach: Block „Montage“ – Selbstmontage / Montage durch unser Team, PLZ-Feld, Zonenprüfung (DE 5-stellig, AT 4-stellig), Preis aus der Variante Breite × Tiefe × Zone des Montage-Produkts (Stegplatten- oder VSG-Produkt je nach Dach).
- Warenkorb: Montage als eigene Zeile, Menge = Dachmenge, Eigenschaften „Für Überdachung“ und „Montageort“ (z. B. „PLZ 45881, Zone 1“ / „Österreich, PLZ 1010“).
- Ohne Zone (PLZ nicht in der Tabelle) oder ohne passende Variante: Hinweis „auf Anfrage“ + Verweis auf „Angebot anfordern“; Warenkorb bleibt gesperrt, bis Selbstmontage gewählt oder die PLZ korrigiert ist.
- `snippets/es-led-guard.liquid`: entfernt Montage und LED ohne Dach, leitet die Montage-Produktseiten auf die Terrassenüberdachungen um.
- Geteilte Links übergeben die PLZ (`?mp=45881`), das Angebotsformular übernimmt sie.
