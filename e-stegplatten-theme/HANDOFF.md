# e-stegplatten.de – Arbeitsstand Theme-Optimierung

Stand: 23.10.2026. Dieser Ordner sichert die Arbeitsdateien. Maßgeblich ist der Stand in Shopify.

## Wichtige IDs

| Was | ID / Handle |
|---|---|
| Neues Theme (unveröffentlicht) | `gid://shopify/OnlineStoreTheme/207286141265` – „e-Stegplatten – Neue Startseite (Claude) 30.09“ |
| Backup vor dem Design-Umbau | `gid://shopify/OnlineStoreTheme/209140842833` |
| Live-Theme (nicht anfassen) | `gid://shopify/OnlineStoreTheme/192027492689` – Warehouse |
| Blog „Ratgeber“ | `gid://shopify/Blog/132769513809` (`/blogs/ratgeber`) |
| Neue Kollektion Polycarbonatplatten | `gid://shopify/Collection/695266935121` (Smart, unveröffentlicht, 24 Produkte) |
| Neue Kollektion Hohlkammerplatten | `gid://shopify/Collection/695266967889` (Smart, unveröffentlicht, 19 Produkte) |

## In Shopify erledigt (geprüft)

1. **LED-Spots** bei Terrassendächern: eigenes Produkt (nicht einzeln kaufbar), Produktseite + Hero-Konfigurator, Warenkorb-Wächter `es-led-guard`.
2. **Design-Umbau v2** (Pakete 1–3, Hero mit zwei Tabs, eigene Archivo-Schrift): 25 Dateien byte-genau (`theme/v2`).
3. **Kategorieseiten:** SEO-Titel/-Beschreibung **live** für 9 Kollektionen; Metafelder `custom.intro`, `custom.seo_text`, `custom.seo_faq`; Section `es-collection-seo` in `collection.json` + `collection.stegplatten.json` (`theme/cat`). Texte: `content/kategorien`.
4. **Ratgeber:** 6 Artikel als **Entwurf** mit SEO-Feldern, FAQ/HowTo-Metafeldern (`custom.seo_faq`, `custom.howto`); Section `es-article-faq` in `article.json` (`theme/art`). Alle 6 gemeinsam veröffentlichen (verlinken sich gegenseitig). Offene Fachfragen: `content/ratgeber/README.md`.

## Lokal fertig, noch NICHT hochgeladen: `theme/v3` (8 Dateien)

Shopify-Verbindung war weg (Shop-Wechsel beim Lesen der TerrassenPost-Preise hat den Zugang zurückgesetzt; Connector muss neu verbunden werden). Tests grün: `tools/pdp_test.js` 61/61, `tools/guard_test.js` 12/12, `tools/led_test.js` 26/26, `tools/shoot_home.js` 12/12 (Startseite: Hero beginnt mit dem Bild; alle Überschriften von 320 bis 1280 px einzeilig). Screenshots: `screenshots/pdp-390-*.png`, `pdp-1280-montage-offer.png`, `hero-390.png`, `screenshots/v3/home-*.png`.

| Datei | Änderung |
|---|---|
| `sections/es-pdp-terrasse.liquid` | Block **Montage** (Selbstmontage / Montage durch unser Team, PLZ-Feld, Zonenprüfung, Preis aus Montage-Produkt), **Angebot anfordern** (Shopify-Kontaktformular, Konfiguration vorausgefüllt), **Konfiguration teilen** (Link kopieren, WhatsApp, E-Mail, Drucken), Farbmuster-Link bei „Dachplatte“. Neue Einstellungen: Montage-Produkte, Montagezonen (`Name|PLZ-Präfixe|Beschreibung` je Zeile; Standard = TerrassenConcept-Zonen 1–4 + Österreich), Texte, `muster_url`. |
| `snippets/es-pdp-js.liquid` | Montage-Logik nach dem Modell aus der Preisliste: Zone über die ersten zwei PLZ-Ziffern (erster Treffer gilt, AT = 4-stellige PLZ), Preis = Variante Breite × Tiefe × Zone des Montage-Produkts; Warenkorbzeile mit „Für Überdachung“ + „Montageort“, Sperre ohne gültige PLZ, Panels, `?mp=PLZ`, `?angebot=1`, `contact_posted` öffnet das Formular. |
| `snippets/es-pdp-css.liquid` | Styles für Montage, Panels, Formular, Druckansicht. |
| `snippets/es-led-guard.liquid` | Wächter jetzt für LED **und** Montage (Handles in `ADD` + Liquid-Liste pflegen). |
| `snippets/es-hero-konfig.liquid` | Zeile „Farbmuster bestellen · Angebot anfordern“ (Link übergibt Variante/LED + `angebot=1`). Neuer Parameter `mu`. |
| `sections/es-landing.liquid` | **Hero beginnt mit dem Bild** (Kicker + H1 + Lead liegen auf dem Bild, Konfigurator rechts daneben, Belege darunter; mobil Bild → Konfigurator → Belege). Beleg 3 = Judge.me-Gesamtwertung („4,9 ★ aus 212 Bewertungen“ aus `shop.metafields.judgeme.all_reviews_*`, Fallback Text); Belege als Zeilen mit Haken. Kategorie-Titel ohne weiche Trennstriche. Einstellung `muster_url`. |
| `snippets/es-landing-css.liquid` | Hero-Raster (Bild/Konfigurator/Belege), Bildüberlagerung; **Überschriften möglichst einzeilig:** Kachel-Titel/-Links skalieren mit der Kachelbreite (`cqi`), keine Silbentrennung; Belege als Zeilen (Titel `nowrap`, Zusatz rückt darunter); Hero-Tabs verteilen die Breite nach Beschriftung; Trust-Leiste ≤ 480 px einspaltig; H2 ≤ 380 px 22 px; Kacheln ≤ 359 px als Liste (Bild links). |
| `templates/index.json` | Trust-Leiste: „Zuschnitt millimetergenau – rechtwinklig, Kanten entgratet, Kammern staubfrei“; Kacheln „Stegplatten“ / „Terrassendächer“, CTA „Nach Stärke“; Farbmuster-Link im Finder; `muster_url`. |

**Upload:** `python3 tools/upload.py stage theme/v3` → stagedUploadsCreate → `put` → `upsert` → Job abwarten → `verify` (Manifest aus `theme/v3/new` erzeugen).

## Nach dem Upload in Shopify anlegen

1. **Montage-Produkte** (2): Preise stehen in `content/montage/zonen.csv` (€/m² je PLZ-Zone aus der Preisliste TerrassenConcept; Österreich vorläufig Zone 4 × 1,35). `python3 tools/montage_product.py` → `productSet` mit `productset_stegplatten.json` / `productset_vsg.json` (je 175 Varianten, erweitertes Variantenmodell nötig), danach im Online Store veröffentlichen. Vorher die echten Breiten/Tiefen der Dächer prüfen (Optionswerte müssen übereinstimmen). Details und offene Punkte: `content/montage/README.md`.

**Offene Entscheidungen (Stand 23.10.):** Österreich-Satz und -Gebiet; alle 4 Zonen online buchbar oder nur bis ca. 300 km; Versand zusätzlich zur Montage; Leistungsumfang-Text; Empfänger-Adresse der Angebotsanfragen; Farbmuster-Sortiment/Versandweg; Fachfragen aus `content/ratgeber/README.md` und `content/kategorien/README.md` (Lieferzeit 16 mm, Dachneigung, Stirnseiten, Garantie, Wunschmaß-Bestellweg); Tag-Bereinigung bei Acryl-/Gewächshausplatten; Maps-Link und Straßenschreibweise.
2. **Farbmuster-Produkt:** `productSet` mit `content/farbmuster/productset.json` (0 €, Tag `Farbmuster`, Handle `farbmuster`), veröffentlichen. Versand 6,90 € per Regel in Advanced Shipping Rules (Tag `Farbmuster`).
3. **LocalBusiness + Breadcrumb-Fix:** `snippets/microdata-schema.liquid` aus dem Theme laden, `python3 tools/localbusiness_patch.py <orig> <neu>` ausführen, hochladen. Maps-Link (`hasMap`) ergänzen, sobald er vorliegt. Straßenschreibweise prüfen („Magdeburger Straße 37“).
4. **og:image:** `snippets/social-meta-tags.liquid` prüfen (Fallback-Bild für Startseite setzen).

## Danach

- **Versand (#15):** nach Umstellung der App auf „höchste Rate“ und AU→AT die 26 Testkörbe erneut rechnen (`draftOrderCalculate`), zusätzlich „Dach + Montage“ (DE 99 €, AT 199 €) und „Farbmuster allein“ (6,90 €). Dann Versandrichtlinie (`shopPolicyUpdate`) und Theme-Texte angleichen, Theme-Einstellung „Gratisversand ab 500 €“ entfernen.
- **Komplett-Check (#14):** MD5 aller Dateien, Liquid-Syntax, Funktionstests, Screenshots, Schema (FAQ, HowTo, LocalBusiness, Breadcrumb), Accessibility, Datenstand, unabhängiger Review-Agent, Go-live-Liste.

## Go-live-Checkliste (für den Shop-Betreiber)

- Die 2 alten Versandarten „Montage bis 270km“ deaktivieren.
- `snippets/es-upload-test.liquid` in beiden Themes löschen (Löschen per API gesperrt).
- Advanced Shipping Rules: „höchste Rate“, Label „AU“ → „AT“, Regel Farbmuster 6,90 €, Montage-Produkte (ohne Versand) lösen keine Gruppe aus.
- Kollektionen Polycarbonatplatten und Hohlkammerplatten veröffentlichen und in die Navigation aufnehmen; 301 `/collections/hohlkammerpaneele-1` → `/collections/hohlkammerplatten`.
- Die 6 Ratgeber-Artikel nach fachlicher Prüfung gemeinsam veröffentlichen; Blog in Navigation/Footer verlinken.
- Kontaktformular: Shopify sendet Angebotsanfragen an die Kunden-E-Mail des Shops; reCAPTCHA in den Shopify-Einstellungen aktiv lassen.
- Kollektions-Metafeld `custom.lieferzeit` der 16-mm-Kollektion („4 - 12 Werktage“) vs. Texte (5–8 Werktage) vereinheitlichen.
- Theme-Vorschau prüfen: Header, Hero-Tabs, Sticky-Leiste, Klarna, Montage-Block, Angebotsformular (Testanfrage senden), Kategorieseiten, Artikel.

## Werkzeuge (`tools/`)

- `upload.py` – `stage` / `put` / `upsert` / `verify`: Sammel-Upload über Staged Uploads mit MD5-Abgleich.
- `v3_patch.py` – erzeugt `theme/v3/new` reproduzierbar aus `theme/v3/orig`.
- `mockdata.py` – Beispieldaten + Liquid-Umgebung (python-liquid) für das lokale Rendern.
- `render_v3.py` – rendert Produktseite + Hero; `render_home.py` – rendert die Startseite (Hero, Trust-Leiste, Kategorien aus `index.json`) nach `design-review/v3/`.
- `pdp_test.js`, `guard_test.js <snippets/es-led-guard.liquid>`, `led_test.js theme/v3/flat` – Playwright-Funktionstests; `shoot_home.js` – Startseiten-Geometrie + Umbruch-Report aller Überschriften (320–1280 px) + Screenshots; `measure_home.js` – misst einzeilige Textbreite gegen verfügbaren Platz.

Aufruf (Playwright aus `/tmp`): `NODE_PATH=/opt/node-tools/node_modules node tools/<test>.js`.
- `montage_product.py`, `localbusiness_patch.py` – siehe oben.
- `cat_verify.py`, `art_verify.py`, `render_cat.py`, `shoot_*.js` – Kategorien/Ratgeber.
