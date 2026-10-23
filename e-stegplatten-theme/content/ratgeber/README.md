# Ratgeber e-stegplatten.de: Entwürfe

Stand: 22.10.2026 · Status: **Entwurf, nicht veröffentlicht**. Bitte vor dem Livegang fachlich gegenlesen, vor allem alle Punkte unter „Bitte prüfen“.

## Übersicht

| Nr. | H1 (title) | Handle | Wörter (Body) | FAQ | HowTo | Dateien |
|---|---|---|---|---|---|---|
| 1 | Doppelstegplatten verlegen: Schritt-für-Schritt-Anleitung für ein dichtes Dach | `doppelstegplatten-verlegen` | 1.401 | 5 | 8 Schritte | `.json`, `.html` |
| 2 | Polycarbonat oder Acrylglas: Welche Stegplatte passt zu Ihrem Projekt? | `polycarbonat-oder-acrylglas` | 1.044 | 4 | – | `.json`, `.html` |
| 3 | Welche Stärke? Stegplatten von 4,5 bis 25 mm richtig wählen | `stegplatten-staerke-waehlen` | 1.049 | 4 | – | `.json`, `.html` |
| 4 | Schneelast und Dachneigung bei Terrassenüberdachungen: Das sollten Sie vor dem Bau wissen | `schneelast-dachneigung-terrassendach` | 1.124 | 5 | – | `.json`, `.html` |
| 5 | Terrassendach selber bauen: Planung, Fundament und Montage Schritt für Schritt | `terrassendach-selber-bauen` | 1.348 | 5 | 9 Schritte | `.json`, `.html` |
| 6 | Gewächshaus selber bauen und Gewächshausplatten erneuern: Plattenwahl, Montage und Abdichtung | `gewaechshaus-selber-bauen` | 1.074 | 5 | 7 Schritte | `.json`, `.html` |

Gezählt werden die Wörter im `body_html` ohne HTML-Tags. Für alle Artikel gilt: `seo_title` ≤ 60 Zeichen, `seo_description` 140–155 Zeichen, unter jeder Frage-H2 steht ein Direkt-Antwort-Absatz mit 40–60 Wörtern, jeder Artikel hat mindestens eine Tabelle und ein Kurzfazit, und es gibt keine H1 im Body. Interne Links zeigen nur auf die freigegebenen Kollektionen und auf `/pages/contact`. Preise und fremde Bewertungszahlen kommen nicht vor. All das prüft `_build/build.py` automatisch.

### JSON-Felder

`handle`, `title`, `seo_title`, `seo_description`, `excerpt`, `body_html`, `faq` [{q,a}], `howto_steps` [{name,text}] (nur bei Artikel 1, 5 und 6, sonst nicht vorhanden), `internal_links` [{anchor,url}] (aus den Links im Body abgeleitet), `image_ideas` [{idea,alt}], `sources`, `uncertain`, `word_count`.

Die `.html`-Dateien sind eigenständige Vorschauen. Sie zeigen ein Suchergebnis-Mockup, den Artikel, FAQ und HowTo, die Prüfliste, Links, Bildideen, Quellen und einen JSON-LD-Vorschlag. Sie sind auf `noindex` gesetzt, und `<base href>` zeigt auf den Live-Shop, damit die Kollektionslinks funktionieren.

## Ziel-Suchbegriffe je Artikel

| Nr. | Hauptkeyword | Nebenkeywords | Nachfrage (laut Briefing, Ahrefs DE) |
|---|---|---|---|
| 1 | doppelstegplatten verlegen | stegplatten verlegen, doppelstegplatten montageanleitung, stegplatten montage, doppelstegplatten befestigen, stegplatten richtig herum, antidust band | Traffic-Potenzial ca. 400–450 |
| 2 | polycarbonat oder acrylglas | acrylglas oder polycarbonat stegplatten, polycarbonat vs. acryl, unterschied acryl polycarbonat, hagelfeste stegplatten | im Briefing als gefragtes Thema genannt, ohne Zahl |
| 3 | stegplatten stärke | welche stärke stegplatten terrassendach, doppelstegplatten 16 mm oder 10 mm, stegplatten u-wert, sparrenabstand stegplatten | nicht beziffert |
| 4 | schneelast terrassenüberdachung | dachneigung terrassenüberdachung, dachneigung berechnen, schneelastzonen, mindestneigung stegplatten, terrassenüberdachung baugenehmigung | im Briefing als gefragt genannt (Dachneigung berechnen, Schneelast) |
| 5 | terrassendach selber bauen | terrassenüberdachung selber bauen, terrassenüberdachung fundament, terrassenüberdachung wandbefestigung, terrassendach montage; als Ausblick: wintergarten selber bauen | 350/Monat, Traffic-Potenzial 2.000; wintergarten selber bauen 1.200 (nur Ausblick) |
| 6 | gewächshaus selber bauen | gewächshausplatten, gewächshausplatten erneuern/austauschen, hohlkammerplatten gewächshaus, gewächshaus abdichten | ca. 3.200/Monat |

Die Nebenkeywords sind redaktionell gewählt. Ihr Suchvolumen wurde nicht separat geprüft.

## Interne Verlinkung zwischen den Artikeln

Im Moment gibt es im Shop nur den Blog `news` (0 Artikel), einen Blog `ratgeber` gibt es noch nicht. Darum stehen Verweise zwischen den Artikeln im Body **als Text ohne Link**, jeweils mit dem Titel in „…“. Sobald der Blog-Handle feststeht, empfehlen wir, diese Stellen zu verlinken, z. B. auf `/blogs/ratgeber/<handle>`.

| Von | Nach | Ankertext (steht bereits im Text) | Stelle |
|---|---|---|---|
| 1 Verlegen | 3 Stärke | „Welche Stärke? Stegplatten von 4,5 bis 25 mm richtig wählen“ | Einleitung, 2. Absatz |
| 1 Verlegen | 2 PC/PMMA | „Polycarbonat oder Acrylglas“ | Einleitung, 2. Absatz |
| 1 Verlegen | 4 Schneelast | „Schneelast und Dachneigung bei Terrassenüberdachungen“ | unter der Neigungstabelle |
| 2 PC/PMMA | 1 Verlegen | „Doppelstegplatten verlegen“ | Abschnitt Gewicht, Wärmeausdehnung und Montage |
| 2 PC/PMMA | 3 Stärke | „Welche Stärke? …“ | unter der Einsatz-Tabelle |
| 3 Stärke | 6 Gewächshaus | „Gewächshaus selber bauen und Gewächshausplatten erneuern“ | Abschnitt 4,5 bis 8 mm |
| 3 Stärke | 4 Schneelast | „Schneelast und Dachneigung bei Terrassenüberdachungen“ | Abschnitt Schneelast |
| 4 Schneelast | 5 Terrassendach | „Terrassendach selber bauen“ | nach der Checkliste |
| 5 Terrassendach | 4 Schneelast | „Schneelast und Dachneigung bei Terrassenüberdachungen“ | Planung, Breite und Tiefe |
| 5 Terrassendach | 1 Verlegen | „Doppelstegplatten verlegen“ | Montage, Schritt 7 |
| 6 Gewächshaus | 3 Stärke | „Welche Stärke? …“ | unter der Vergleichstabelle |
| 6 Gewächshaus | 1 Verlegen | „Doppelstegplatten verlegen“ | Abschnitt Platten montieren |

Die Artikel 4 (Schneelast) und 1 (Verlegen) werden am häufigsten verlinkt und sind die Hub-Seiten für Statik und Montage. Artikel 5 und 6 zielen auf die größte Suchnachfrage und verweisen auf diese Hubs.

### Kollektions-Links je Artikel (Auszug)

- **1:** doppelstegplatten, doppelstegplatten-16mm, profile-zubehor-fur-16mm, profile-zubehor-fur-10mm, doppelstegplatten-komplettset-dachhaut, pages/contact
- **2:** doppelstegplatten-16mm, gewachshausplatten, doppelstegplatten-10mm, doppelstegplatten, polycarbonat-wellplatten, acrylglas-wellplatten, pages/contact
- **3:** alle Stärken-Kollektionen 4/6/8/10/16 mm, gewachshausplatten, terrassenuberdachung-alu-mit-stegplatten, profile-zubehor-fur-4/6/8/10/16/25mm, pages/contact
- **4:** terrassenuberdachung-alu-mit-stegplatten, terrassenuberdachung-alu-mit-vsg-glas, doppelstegplatten-16mm, terrassenuberdachung, pages/contact
- **5:** terrassenuberdachung, terrassenuberdachung-alu-mit-stegplatten, terrassenuberdachung-alu-mit-vsg-glas, pages/contact
- **6:** gewachshausplatten, doppelstegplatten-4mm, doppelstegplatten-6mm, polycarbonat-wellplatten, profile-zubehor-fur-4mm, profile-zubehor-fur-6mm, pages/contact

Alle Ziel-Kollektionen wurden am 22.10.2026 per lesender Shopify-Abfrage geprüft: Sie existieren und enthalten Produkte.

## Hinweise zur Umsetzung in Shopify

- `body_html` kommt in den Artikel-Body, `excerpt` in den Auszug (Summary), `seo_title`/`seo_description` in die SEO-Felder des Artikels.
- FAQ und HowTo werden **nicht** im Body ausgegeben. Sie liegen als Daten vor und können über ein Theme-Snippet oder Metafelder als FAQ-Block und JSON-LD eingebunden werden (Vorschlag in jeder `.html`-Vorschau). Google zeigt FAQ-Rich-Results seit 2023 nur noch für ausgewählte Behörden- und Gesundheitsseiten und hat HowTo-Rich-Results eingestellt. Für Antwortmaschinen und KI-Suche sind die strukturierten Frage-Antwort-Paare trotzdem nützlich.
- Es gibt bereits die Seite `/pages/verlegeanleitung` mit vier PDF-Verlegeanleitungen (Alu-Alu Komplettsystem, Alu-Alu Thermosystem, Alu-Gummi Komplettsystem, PVC-Sprossensystem). Artikel 1 überschneidet sich thematisch damit. Wir empfehlen, aus Artikel 1 dorthin zu verlinken. Die Seite steht nicht auf der Link-Whitelist und ist deshalb noch nicht verlinkt. Außerdem sollten die Angaben abgeglichen werden (Stirnseiten oben/unten, Schraubenabstände, Mindestneigung). Die PDFs ließen sich aus der Arbeitsumgebung nicht abrufen.
- Die Bilder sind nur Ideen mit Alt-Text-Vorschlag. Es wurden keine Bilder erzeugt oder ausgewählt.

## Bitte prüfen: wichtigste unsichere Aussagen (Auszug, vollständig im Feld `uncertain` jeder Datei)

1. **Mindestneigung und Produktseiten:** Die Plattenhersteller nennen mindestens 5° (teils 7°). Die Produktseiten der Shop-Terrassendächer nennen dagegen „Dachneigung 3–10°“. Das bitte mit dem Systemhersteller klären. Die Artikel nennen 5° als übliche Mindestneigung und verweisen auf die Systemangabe.
2. **Stirnseiten:** Hersteller empfehlen oben einen dichten Abschluss mit Alu-Klebeband und unten luftdurchlässiges Antidust-Band. Laut Shop-Fakten kommt Antidust-Band „an die Stirnseiten“. Die Artikel sagen: unten immer Antidust, oben je nach System. Bitte festlegen, was e-stegplatten oben empfiehlt.
3. **Schneelastzonen:** Formeln und Übergangshöhen stammen aus einer Sekundärquelle und wurden nachgerechnet. Der Faktor für das Norddeutsche Tiefland wird bewusst nicht genannt. Bitte gegen den Normtext prüfen lassen.
4. **Baurecht:** Die NRW-Grenze (30 m², 4,50 m) ist gut belegt. Die Werte für Bayern und Sachsen (30 m², 3 m) stützen sich nur auf Sekundärquellen. Die Gewächshaus-Grenzen (NRW 75 m³, BW 40 m³) sind nur Beispiele, und ob sie für private Gewächshäuser gelten, ist nicht eindeutig.
5. **Technische Kennwerte:** U-Werte, Gewichte, Lichtdurchlässigkeit, Brandklassen und die Wärmeausdehnung von PMMA sind Spannen aus Datenblättern Dritter. Bitte durch die Datenblätter der eigenen Platten ersetzen, vor allem bei der 16-mm-X-Struktur.
6. **Montagewerte:** Schraubenabstand ca. 25 cm, Bohrloch-Übermaß 2–3 mm, Sparrenabstand = Plattenbreite + 20–25 mm, 30 mm Auflage und Frosttiefe ≥ 80 cm sind systemabhängig bzw. regional verschieden.
7. **Lieferumfang Terrassendach:** Formuliert als „laut Herstellerangaben“. Offen ist, ob Pfostenanker, Fußplatten, Dichtbänder und Alu-Klebeband enthalten sind.
8. **Benennung:** Die Gewächshausplatten heißen im Shop „4 mm“, die Kollektion „4,5 mm“. Bitte vereinheitlichen.
9. **Nicht verwendet, weil nicht in den bestätigten Shop-Fakten:** „10 Jahre Garantie“, „Videoanleitung“ und „Dachneigung 3–10°“ von den Produktseiten sowie „10 Jahre auf Aluminium“ von der FAQ-Seite.

## Quellenlage und Vorgehen

- Die Recherche lief über die Websuche. Direkte Seitenabrufe (PDF-Download) waren in der Arbeitsumgebung durch den Netzwerk-Proxy gesperrt. Die Fakten wurden daher anhand der Suchergebnis-Auszüge der angegebenen Quellen geprüft und, wo möglich, mit mehreren unabhängigen Quellen abgeglichen. Werte, die je Hersteller schwanken, stehen als Spanne mit Verweis auf die Herstellerangabe im Text.
- Quellen sind Herstelleranleitungen und Datenblätter (TUJ/TEJA, Löffert, Scobalit/dwz, SABIC Lexan über Händler, Plexiglas, DIBt-Zulassung), Normen-Sekundärliteratur (mb-news, Dlubal, Forum Verlag), Merkblätter von Kommunen (Monheim, Hagen, Bielefeld, Unna, Porta Westfalica, Radebeul, Gerlingen) und Ratgeberseiten. Die URLs stehen je Artikel im Feld `sources`.
- Texte von Wettbewerbern wurden nicht übernommen. Alle Formulierungen sind eigenständig.
- Shopify wurde nur lesend genutzt (Kollektionen, zwei Produktgruppen, Blogs und Seiten). Es wurde nichts geschrieben.
- Für Statik und Baurecht enthalten die Artikel keine verbindlichen Zusagen. Sie sagen ausdrücklich, wann ein Statiker oder das Bauamt gefragt werden sollte.

## Neu erzeugen

Die Artikeltexte liegen als Python-Module in `_build/articles/`. Nach Änderungen dort neu bauen und prüfen:

```bash
cd content/ratgeber && python3 -I _build/build.py
```

Das Skript schreibt alle `.json`- und `.html`-Dateien neu und bricht bei Regelverstößen mit einer Fehlermeldung ab. Wer stattdessen direkt in den JSON-Dateien redigiert, muss die Vorschauen von Hand anpassen.
