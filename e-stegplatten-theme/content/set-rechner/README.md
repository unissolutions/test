# Komplettset selbst zusammenstellen – Mengenregeln (16-mm-Stegplatten, Alu-Profilsystem 60 mm)

Quelle: Lieferumfang der Komplettsets im Shop („Lieferumfang – Das ist alles dabei“) und die Set-Breiten
3070 / 4080 / 5080 / 6090 / 7090 / 8100 mm (= 3…8 Platten à 980 mm). Umgesetzt in `snippets/es-steg-zubehoer.liquid`
(Block „Komplettset selbst zusammenstellen“ auf den Stegplatten-Produktseiten); Referenz-Modul: `theme/v3/extra/es-set-mengen.js`.

| Eingabe | Regel |
|---|---|
| Plattenanzahl n | Dachbreite = n × (Plattenbreite + 30 mm) + 40 mm → n = ⌈(Dachbreite − 40) / (Plattenbreite + 30)⌉ (980er: 3070 → 3, 4080 → 4, … 8100 → 8; 1200er: 3070 → 3) |
| Dachtiefe | = Plattenlänge der gewählten Variante (2000 … 7000 mm) |
| Fertige Dachbreite | n × (Plattenbreite + 30) + 40 mm (letzte Platte kann kostenfrei schmaler geschnitten werden) |

| Teil | Menge | Variante |
|---|---|---|
| Stegplatten | n | gewählte Länge × Breite (Menge im Produkt wird automatisch auf n gesetzt) |
| Mittelprofil Alu-Alu Premium 60 mm (Verbindungsprofil) | n − 1 | kleinste Länge ≥ Plattenlänge |
| Randprofil Alu-Alu Premium 60 mm | 2 | kleinste Länge ≥ Plattenlänge |
| U-Profil Abschlussprofil mit Tropfkante | n | = Plattenbreite (980 / 1200 mm) |
| Abrutsch-/Haltewinkel | n + 1 (je Profil 1) | 1 Stück |
| Anti-Dust-Tape 43 mm | 2 × n × Plattenbreite (oben + unten) | Rolle 7,5 / 15 m für 16 mm |
| Schrauben Unterprofil | (n + 1) × (⌈Plattenlänge / 500⌉ + 1) – Richtwert Raster 50 cm | Holz: Edelstahl 4,5×35 · Metall: Bohrschraube 4,2×32 (Packungen 20 / 100) |
| Schrauben Oberprofil | gleiche Anzahl | 6,3×32 (Packungen 20 / 100) |
| Schrauben Haltewinkel | 2 je Winkel | 4,2×16 TORX (Packungen 20 / 100) |
| Spezial-Silikon | 1 (ab 7 Platten 2) | – |
| Wandanschlussprofil | nicht Teil der Komplettsets (optional, Länge ≥ fertige Dachbreite: 3100/4100/5150/6200/7100 mm) | |

Verhalten: Breite tippen oder Plattenvariante wechseln → Plattenanzahl, Menge oben, alle Zubehör-Mengen und die Profil-Längen
werden neu gesetzt (manuell geänderte Mengen werden bei Breiten-/Variantenwechsel zurückgesetzt). Unterkonstruktion Holz/Metall
schaltet die passenden Schrauben um. „Komplettset in den Warenkorb“ legt Platten + angehakte Zubehörteile in einem Schritt in den Warenkorb.
Variant-IDs der Zubehörteile: `zubehoer.json`.
