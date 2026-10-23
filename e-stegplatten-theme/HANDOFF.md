# e-stegplatten.de – Arbeitsstand Theme-Optimierung

Stand: 22.10.2026. Dieser Ordner sichert die Arbeitsdateien. Maßgeblich ist der Stand in Shopify.

## Wichtige IDs

| Was | ID / Handle |
|---|---|
| Neues Theme (unveröffentlicht) | `gid://shopify/OnlineStoreTheme/207286141265` – „e-Stegplatten – Neue Startseite (Claude) 30.09“ |
| Backup vor dem Design-Umbau | `gid://shopify/OnlineStoreTheme/209140842833` |
| Live-Theme (nicht anfassen) | `gid://shopify/OnlineStoreTheme/192027492689` – Warehouse |
| Blog „Ratgeber“ | `gid://shopify/Blog/132769513809` (`/blogs/ratgeber`) |
| Neue Kollektion Polycarbonatplatten | `gid://shopify/Collection/695266935121` (Smart, unveröffentlicht, 24 Produkte) |
| Neue Kollektion Hohlkammerplatten | `gid://shopify/Collection/695266967889` (Smart, unveröffentlicht, 19 Produkte) |

## Erledigt (alles in Shopify geprüft)

1. **LED-Spots** bei Terrassendächern: eigenes Produkt (nicht einzeln kaufbar). Einbindung auf der Produktseite und im Hero-Konfigurator. `es-led-guard` entfernt LED aus dem Warenkorb, sobald kein Dach mehr drin ist.
2. **Design-Umbau v2** (Pakete 1–3, Hero mit zwei Tabs, eigene Archivo-Schrift): 25 Dateien hochgeladen und byte-genau geprüft (`theme/v2`).
3. **Kategorieseiten (SEO):**
   - SEO-Titel und -Beschreibung sind **live** gesetzt für 7 bestehende und 2 neue Kollektionen.
   - Neue Kollektions-Metafelder: `custom.intro`, `custom.seo_text`, `custom.seo_faq`. Die Texte erscheinen nur im neuen Theme.
   - Neue Section `es-collection-seo` (Ratgeber-Text, FAQ, FAQPage-Schema) in `templates/collection.json` und `collection.stegplatten.json` (`theme/cat`).
   - Texte und Quellen: `content/kategorien`.
4. **Ratgeber:**
   - 6 Artikel als **Entwurf** angelegt, mit SEO-Feldern, FAQ und HowTo-Metafeldern (`custom.seo_faq`, `custom.howto`). Die Artikel verlinken untereinander, deshalb **alle 6 gemeinsam veröffentlichen**.
   - Neue Section `es-article-faq` in `templates/article.json` (`theme/art`).
   - Inhalte und offene Fachfragen: `content/ratgeber/README.md`.

## Offen

- **#12 Montage zubuchbar:**
  - Modell TerrassenPost: Preis je Dachgröße, ca. 300 km um Gelsenkirchen, Österreich +35 %, als eigene Warenkorbzeile, nicht einzeln kaufbar.
  - **Fehlt:** die Montagepreise je Variante aus dem TerrassenPost-Shop.
  - Alternative Preisbasis aus dem 3D-Planer TerrassenConcept: €/m² nach PLZ-Zone (Stegplatten 67 / 82,50 / 97 / 112 €, Glas 97 / 112 / 127 / 142 €).
- **#13 Angebot anfordern / Konfiguration speichern** (Produktseite und Hero).
- **#5 Vertrauens-Elemente:**
  - Zuschnitt mm-genau und Kanten entgratet
  - Farbmuster-Produkt für 0 € mit Tag „Farbmuster“; Versand 6,90 € über eine Regel in Advanced Shipping Rules
  - eigene Judge.me-Bewertungen im Hero
- **#4 LocalBusiness-Schema** (TSZ GmbH, Magdeburgerstraße 37, 45881 Gelsenkirchen, 0209 513 078 34, Mo–Fr 8–17) und og:image für die Startseite.
  - Bugfix in `snippets/microdata-schema.liquid`: Die Breadcrumb eines Artikels nennt an Position 3 den Blog- statt den Artikeltitel.
  - Google-Maps-Link fehlt noch.
- **#15 Versand:**
  - Wenn in der App „höchste Gruppe zählt“ aktiv ist und AU→AT umbenannt wurde: die 26 Testkörbe neu prüfen.
  - Danach die Versandrichtlinie aktualisieren.
- **#14 Komplettcheck** vor dem Livegang.

## Go-live-Checkliste (für den Shop-Betreiber)

- Die 2 alten Versandarten „Montage bis 270km“ deaktivieren.
- `snippets/es-upload-test.liquid` in beiden Themes löschen (das Löschen ist über die API gesperrt).
- Advanced Shipping Rules:
  - „höchste Rate“ einstellen
  - Label „AU“ in „AT“ umbenennen
  - Regel für Farbmuster: 6,90 €
- Kollektionen Polycarbonatplatten und Hohlkammerplatten veröffentlichen und in die Navigation aufnehmen.
- 301-Weiterleitung `/collections/hohlkammerpaneele-1` → `/collections/hohlkammerplatten`.
- Die 6 Ratgeber-Artikel nach fachlicher Prüfung gemeinsam veröffentlichen und den Blog in Navigation und Footer verlinken.
- Kollektions-Metafeld `custom.lieferzeit` der 16-mm-Kollektion steht auf „4 - 12 Werktage“; die Texte nennen 5–8 Werktage. Bitte vereinheitlichen.
- In der Theme-Vorschau prüfen:
  - Header, Hero-Tabs, Sticky-Leiste
  - Klarna-Hinweis
  - Kategorieseiten mit Ratgeber-Text und FAQ
  - Artikel-Vorschau

## Werkzeuge (`tools/`)

- `upload.py`:
  - `stage` / `put` / `upsert` / `verify`: Sammel-Upload über Shopify Staged Uploads mit MD5-Abgleich.
- `cat_verify.py`, `art_verify.py`: vergleichen Kollektions- bzw. Artikeltexte in Shopify mit den lokalen Quellen.
- `render_cat.py`, `shoot_*.js`: lokale Vorschau (python-liquid und Playwright) mit Screenshots.
- `led_test.js`, `guard_test.js`: Funktionstests für LED-Logik und Warenkorb-Guard.
