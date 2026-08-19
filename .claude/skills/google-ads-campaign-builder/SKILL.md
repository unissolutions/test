---
name: google-ads-campaign-builder
description: Analysiert eine Webseite, leitet daraus Keywords ab und baut komplette Google-Ads-Kampagnen (Suchkampagne oder Performance Max) inklusive Anzeigentiteln, langen Titeln, Beschreibungen, Sitelinks, Callouts, Snippets und Preis-Assets — und exportiert alles als CSV-Dateien, die sich direkt in den Google Ads Editor importieren lassen. Nutze diesen Skill immer, wenn es um Google Ads, SEA, Suchanzeigen, Performance Max, PMax, Anzeigentexte, RSA, Keyword-Recherche für bezahlte Werbung, Kampagnenstruktur, Anzeigenerweiterungen/Assets oder einen Google-Ads-Editor-Import geht — auch dann, wenn nur eine URL genannt wird und jemand sinngemäß fragt "mach mir daraus Werbung", "bewirb diese Seite", "ich will Anzeigen schalten" oder "erstell mir eine Kampagne". Ebenso bei Aufgaben wie Anzeigentexte optimieren, Keywords in Anzeigengruppen strukturieren, negative Keywords finden oder Zeichenlimits prüfen.
---

# Google Ads Campaign Builder

Aus einer Webseite wird eine importfertige Kampagne. Der Ablauf hat sechs Stufen:

**Briefing → Website-Scan → Keywords → Struktur → Texte & Assets → CSV-Export**

Jede Stufe baut auf der vorherigen auf. Überspringe keine — insbesondere der Website-Scan ist die Grundlage für alles Weitere, denn Anzeigentexte, die nichts mit dem tatsächlichen Seiteninhalt zu tun haben, ruinieren den Anzeigenrang und werden bei der Landingpage-Prüfung abgestraft.

Das Herzstück ist eine **Plan-Datei im JSON-Format**. Du schreibst die komplette Kampagne dort hinein, und die mitgelieferten Skripte erzeugen daraus die CSVs und prüfen jedes Zeichenlimit. Zähle Zeichen niemals im Kopf — dabei verzählt man sich, und eine Anzeige mit 31 Zeichen wird vom Editor kommentarlos abgelehnt. Der Validator ist dafür da.

## Stufe 1 — Briefing

Kläre diese Punkte. Frag nach, was du nicht aus der Webseite ableiten kannst, aber halte den Nutzer nicht mit Fragen auf, deren Antwort offensichtlich auf der Seite steht.

| Punkt | Warum es zählt |
|---|---|
| URL der Webseite | Basis für alles |
| Kampagnenziel | Leads, Verkäufe, Anrufe, Store-Besuche → bestimmt Gebotsstrategie und Assets |
| Land und Sprache | Bestimmt Währung, Snippet-Header-Liste und Textsprache |
| Tagesbudget | Pflichtfeld für die CSV |
| Kampagnentyp | Suchkampagne, Performance Max oder beides |
| Conversion-Tracking vorhanden? | Ohne Conversions funktioniert "Conversions maximieren" nicht — dann Manual CPC oder "Klicks maximieren" |
| Markenname und Schreibweise | Für Marken-Anzeigengruppen und die Business-Name-Vorgabe bei PMax |

**Wann welcher Kampagnentyp** — wenn der Nutzer unsicher ist, empfiehl anhand dieser Faustregeln statt beide Optionen nur aufzuzählen:

- **Suchkampagne**: klarer Suchbedarf, bekannte Keywords, Kontrolle über Texte und Gebote gewünscht, kleines Budget, wenig Conversion-Historie. Fast immer der richtige Start.
- **Performance Max**: Conversion-Tracking läuft stabil, mindestens ~30 Conversions/Monat, Bildmaterial vorhanden, Ziel ist Reichweite über alle Kanäle. PMax braucht Datenfutter — ohne Conversion-Historie verbrennt es Budget.
- **Beides**: sinnvoll bei größerem Budget. Dann Suchkampagne für Marke und Kern-Keywords, PMax für den Rest.

## Stufe 2 — Website-Scan

Ziel ist ein Bild davon, was das Unternehmen anbietet, mit welchen Worten es das tut und welche Seiten sich als Landingpages eignen.

Hol dir die Startseite und die wichtigsten Unterseiten. Nutze `WebFetch`, ersatzweise `curl -sL <url>`. Wenn eine Sitemap existiert (`/sitemap.xml`, `/robots.txt`), nutze sie, um die Seitenstruktur zu erfassen, statt zu raten.

Extrahiere pro Seite:

- **Title und Meta-Description** — die Wörter, mit denen sich der Anbieter selbst beschreibt
- **H1 bis H3** — die Themenstruktur, oft schon die Vorlage für Anzeigengruppen
- **Produkte und Leistungen** mit Namen und Varianten
- **Preise**, Preisspannen, "ab"-Preise — Grundlage für Preis-Assets und glaubwürdige Anzeigentexte
- **Alleinstellungsmerkmale** — kostenloser Versand, Zertifikate, Jahre Erfahrung, Garantie, Öffnungszeiten
- **Belege für Behauptungen** — Testsiegel, Bewertungen, Mitgliedschaften. Ohne Beleg keine Superlative im Anzeigentext, siehe `references/ad-copy-rules.md`
- **Handlungsaufforderungen** — was soll der Besucher tun
- **Kontaktdaten und Standorte** — für Anruf-Assets und Standort-Targeting

Wenn eine Seite kein sinnvolles Ziel für bezahlten Traffic ist (Impressum, AGB, Blog-Archiv), notiere sie als ungeeignet und verwende sie nicht als Final URL.

Halte das Ergebnis in einer Datei `website-analyse.md` fest. Der Nutzer soll nachvollziehen können, worauf die Kampagne aufbaut.

## Stufe 3 — Keyword-Recherche

Details und konkrete Werkzeugaufrufe: **`references/keyword-research.md`**. Lies die Datei, bevor du mit der Recherche beginnst.

Kurzfassung: Wenn ein Ahrefs-MCP verbunden ist, nutze es für echte Suchvolumina, Keyword-Difficulty und die Keywords der Wettbewerber. Ohne Ahrefs leitest du Keywords aus dem Seiteninhalt ab und **kennzeichnest alle Volumenangaben ausdrücklich als Schätzung**. Erfundene Suchvolumina, die wie Messwerte aussehen, sind schlimmer als gar keine Zahlen — auf ihrer Basis werden Budgets falsch verteilt.

Jedes Keyword bekommt eine Suchintention zugeordnet: transaktional (kaufen, buchen, Preis, in der Nähe), kommerziell (Vergleich, Test, beste), informational (was ist, Anleitung), navigational (Markenname). **Für Suchkampagnen zählen transaktionale und kommerzielle Keywords.** Informational bringt teuren Traffic ohne Conversion — sortiere solche Begriffe aus oder lege sie bewusst als eigene, separat budgetierte Gruppe an.

Negative Keywords sind kein Nachgedanke, sondern Teil der Lieferung. Ohne sie zahlt der Nutzer ab Tag eins für "kostenlos", "gratis", "Job", "Ausbildung", "gebraucht", "selber machen" und Wettbewerbernamen. Die Standardliste steht in `references/keyword-research.md`.

## Stufe 4 — Kampagnenstruktur

Gruppiere Keywords nach **Suchintention und passender Landingpage**, nicht nach oberflächlicher Wortähnlichkeit. Der Test: Passt eine einzige Anzeige zu allen Keywords der Gruppe und führt sie auf dieselbe Seite? Wenn nein, teile die Gruppe.

Bewährte Größenordnung: 5 bis 20 Keywords pro Anzeigengruppe, 3 bis 10 Anzeigengruppen pro Kampagne. Sehr viel kleinere Gruppen (ein Keyword pro Gruppe) sammeln heute zu wenig Daten, weil Google Varianten ohnehin zusammenfasst.

Zu den Match Types: Nimm **Phrase** und **Exact** als Rückgrat. Broad Match nur, wenn Conversion-Tracking läuft und eine Smart-Bidding-Strategie aktiv ist — sonst ist es eine Budgetfalle. Für jedes Keyword in Broad gehört eine wachsame Negativliste dazu.

Lege eine eigene **Marken-Anzeigengruppe** an, sofern der Markenname Suchvolumen hat. Sie ist billig, konvertiert stark und verhindert, dass Wettbewerber auf den Markennamen bieten.

## Stufe 5 — Texte und Assets

Zeichenlimits, Google-Richtlinien und Formulierungsmuster: **`references/ad-copy-rules.md`**. Diese Datei ist verpflichtende Lektüre, bevor du die erste Überschrift schreibst — sie enthält die Regeln, an denen Anzeigen in der Prüfung scheitern.

Die wichtigsten Leitplanken:

**Responsive Suchanzeige (RSA)** — 15 Überschriften à max. 30 Zeichen, 4 Beschreibungen à max. 90 Zeichen. Nutze alle Plätze; Google testet die Kombinationen, und wer nur drei Überschriften liefert, verschenkt den Mechanismus. Sorge dabei für echte Vielfalt: Wiederholst du dasselbe Versprechen fünfmal anders formuliert, hat der Algorithmus nichts zu testen. Decke Nutzen, Alleinstellungsmerkmal, Preis/Angebot, Vertrauen, Handlungsaufforderung und das Keyword selbst ab.

**Performance Max Asset Group** — 3–15 kurze Überschriften (30), 1–5 lange Überschriften (90), eine kurze Beschreibung (60) plus bis zu vier lange (90), Unternehmensname (25). Bilder und Videos lassen sich **nicht** per CSV hochladen; sie müssen im Konto vorhanden sein. Liste sie deshalb in der Übergabe-Checkliste als manuellen Schritt auf, statt so zu tun, als sei die Kampagne nach dem Import fertig.

**Assets/Erweiterungen** sind nicht optional. Eine Suchanzeige ohne Sitelinks und Callouts verliert Fläche in den Ergebnissen und damit Klickrate. Liefere mindestens 4 Sitelinks, 4 Callouts, 2 Structured Snippets und — wenn die Webseite Preise nennt — Preis-Assets.

Schreibe in der Sprache der Zielgruppe und in der Ansprache der Webseite. Siezt die Seite, siezen die Anzeigen.

## Stufe 6 — Plan schreiben, validieren, exportieren

Schreibe die komplette Kampagne als JSON in `campaign-plan.json`. Struktur und ein vollständiges Beispiel: `assets/campaign-plan.example.json`, formale Definition: `assets/campaign-plan.schema.json`.

Dann:

Die Skripte liegen im Skill-Verzeichnis. Setze `$SKILL` einmal auf dessen Pfad
(dort, wo diese `SKILL.md` liegt), dann funktionieren die Aufrufe aus jedem
Arbeitsverzeichnis:

```bash
SKILL=.claude/skills/google-ads-campaign-builder   # ggf. anpassen

# 1) Prüfen: Zeichenlimits, Pflichtfelder, Duplikate, verbotene Muster
python3 "$SKILL/scripts/validate_plan.py" campaign-plan.json

# 2) Erst wenn die Prüfung sauber ist: CSVs erzeugen
python3 "$SKILL/scripts/build_csv.py" campaign-plan.json --out ./google-ads-export
```

Beide Skripte laufen mit purem Python 3 ohne Zusatzpakete.

`validate_plan.py` meldet Fehler (blockieren den Export) und Warnungen (Qualitätsmängel). **Behebe Fehler, indem du den Plan korrigierst und erneut prüfst.** Ein zu langer Text wird umformuliert, nicht abgeschnitten — abgeschnittene Anzeigentexte lesen sich kaputt und kosten Klickrate.

`build_csv.py` schreibt pro Entitätstyp eine eigene CSV plus eine `IMPORT-ANLEITUNG.md`. Getrennte Dateien sind Absicht: Der Editor importiert eine Datei nach der anderen und zeigt vor dem Import eine Spaltenzuordnung an — bei gemischten Dateien geht diese Zuordnung schief.

### Spaltennamen an die eigene Editor-Version angleichen

Google ändert Spaltenbezeichnungen zwischen Editor-Versionen und je nach Oberflächensprache. Statt darauf zu hoffen, dass die Vorgaben passen, gibt es zwei Absicherungen:

1. **Referenz-Export nutzen (empfohlen).** Bitte den Nutzer, im Google Ads Editor über *Konto → Exportieren → Ganzes Konto als CSV exportieren* eine Datei zu ziehen, und übergib sie:
   ```bash
   python3 "$SKILL/scripts/build_csv.py" campaign-plan.json \
       --out ./google-ads-export --reference-export ~/Downloads/account-export.csv
   ```
   Das Skript liest die Spaltenüberschriften aus dem Export und richtet die Ausgabe daran aus. Damit passt sie exakt zur installierten Editor-Version.

2. **Spaltenzuordnung beim Import.** Der Editor zeigt beim CSV-Import eine Vorschau, in der jede Spalte manuell zugeordnet oder ignoriert werden kann. Weise den Nutzer darauf hin — damit ist auch eine abweichende Überschrift kein Problem.

Erkläre außerdem: **Der Import im Editor ändert noch nichts am Live-Konto.** Änderungen landen zunächst lokal, werden als Vorschau angezeigt und gehen erst mit *Posten* live. Ein Testimport ist also gefahrlos und der richtige Weg, die Datei zu prüfen.

## Übergabe

Liefere am Ende:

1. `website-analyse.md` — was gefunden wurde
2. `keyword-recherche.md` — Keywords mit Intention, Volumen (oder ausgewiesener Schätzung), Zuordnung zu Anzeigengruppen, Negativliste
3. `campaign-plan.json` — der vollständige Plan
4. `google-ads-export/` — die CSVs plus Importanleitung
5. Eine kurze **Checkliste der manuellen Schritte**, die der Import nicht abdeckt: Bilder und Videos für PMax, Conversion-Tracking, Zahlungsdaten, Standort- und Zeitplan-Feinschliff, Anruf-Assets mit verifizierter Nummer

Sag klar, was noch fehlt. Eine Kampagne, die als "fertig" übergeben wird und dann wegen fehlender Assets nicht ausgeliefert wird, kostet den Nutzer Zeit und Vertrauen.
