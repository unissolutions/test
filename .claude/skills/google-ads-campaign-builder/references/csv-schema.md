# CSV-Struktur für den Google Ads Editor

## Grundregeln des Imports

Der Editor liest die **erste Zeile als Spaltenüberschriften**. Erkennt er eine Überschrift, ordnet er sie automatisch zu; erkennt er sie nicht, bietet er beim Import eine **manuelle Spaltenzuordnung** an. Das ist die wichtigste Absicherung: Selbst wenn eine Überschrift zwischen Editor-Versionen abweicht, lässt sich der Import retten, ohne die Datei neu zu bauen.

Weitere Regeln:

- **Leeres Feld = keine Änderung.** Um einen bestehenden Wert zu löschen, gehören eckige Klammern `[]` ins Feld.
- **Mehrere Werte in einer Zelle** werden mit Semikolon getrennt: `de;en`.
- **Kontoweite Assets** entstehen, indem in der Spalte `Campaign` der Wert `<Account-level>` steht statt eines Kampagnennamens.
- Überschriften sind **auf Englisch** zu erwarten. Groß-/Kleinschreibung und Leerzeichen spielen keine Rolle — `Ad Group`, `ad group` und `adgroup` sind gleichwertig.
- Zeichensatz **UTF-8**, Trennzeichen Komma, Textfelder in Anführungszeichen. Umlaute brauchen UTF-8, sonst landen `Ã¼`-Artefakte im Konto.
- Der Import wirkt **nur lokal**. Änderungen erscheinen als Entwurf und gehen erst mit *Posten* live. Ein Testimport ist deshalb ungefährlich und der beste Weg, die Datei zu prüfen.

## Warum getrennte Dateien pro Entität

`build_csv.py` schreibt je Entitätstyp eine eigene Datei. Gemischte Dateien mit Kampagnen-, Anzeigengruppen- und Keyword-Zeilen in einem Dokument erzeugen viele leere Spalten, und die automatische Zuordnung greift dann oft daneben. Eine Datei pro Typ importiert sauber und ist bei Fehlern leichter zu korrigieren.

**Importreihenfolge** — Über- vor Untergeordnetem, sonst finden die Zeilen ihren Elternknoten nicht:

1. `01_campaigns.csv`
2. `02_ad_groups.csv`
3. `03_keywords.csv`
4. `04_negative_keywords.csv`
5. `05_responsive_search_ads.csv`
6. `06_sitelinks.csv`, `07_callouts.csv`, `08_structured_snippets.csv`, `09_prices.csv`
7. `10_pmax_asset_groups.csv` (nur bei Performance Max)

## Spalten je Entität

Die folgenden Überschriften sind der Standardsatz, den `build_csv.py` erzeugt. Weicht die installierte Editor-Version ab, gleicht `--reference-export` sie an einen echten Kontoexport an.

### Kampagnen — `01_campaigns.csv`

| Spalte | Werte / Hinweise |
|---|---|
| `Campaign` | Name, eindeutig im Konto |
| `Campaign Type` | `Search`, `Performance Max` |
| `Campaign Status` | `Enabled`, `Paused` — neue Kampagnen als `Paused` anlegen |
| `Budget` | Tagesbudget als Zahl, Punkt als Dezimaltrenner |
| `Budget Type` | `Daily` |
| `Bid Strategy Type` | `Manual CPC`, `Maximize clicks`, `Maximize conversions`, `Maximize conversion value`, `Target CPA`, `Target ROAS` |
| `Target CPA` | nur bei `Target CPA` |
| `Target ROAS` | nur bei `Target ROAS`, als Faktor (`4.0` = 400 %) |
| `Networks` | `Google search;Search partners` |
| `Languages` | `de`, `en`, mehrere per Semikolon |
| `Location` | Zielregionen, per Semikolon |
| `Excluded Location` | optional |
| `Start Date` | `YYYY-MM-DD` |
| `End Date` | optional |

Neue Kampagnen grundsätzlich pausiert anlegen. Nach dem Posten kann sonst sofort Budget abfließen, bevor jemand die Texte gegengelesen hat.

### Anzeigengruppen — `02_ad_groups.csv`

`Campaign`, `Ad Group`, `Ad Group Status`, `Max CPC`, `Ad Group Type` (`Standard`), optional `Target CPA`

### Keywords — `03_keywords.csv`

`Campaign`, `Ad Group`, `Keyword`, `Match Type` (`Broad`, `Phrase`, `Exact`), `Status`, optional `Max CPC`, `Final URL`

Der Keyword-Text selbst enthält **keine** Sonderzeichen für den Match Type. Nicht `"schuhe kaufen"` oder `[schuhe kaufen]`, sondern `schuhe kaufen` mit `Phrase` beziehungsweise `Exact` in der eigenen Spalte. Anführungszeichen und Klammern im Text sind ein häufiger Importfehler.

### Negative Keywords — `04_negative_keywords.csv`

`Campaign`, `Ad Group`, `Keyword`, `Match Type`, `Criterion Type`

`Criterion Type` trägt `Negative Broad`, `Negative Phrase` oder `Negative Exact`. Bleibt `Ad Group` leer, gilt der Ausschluss für die gesamte Kampagne — das ist für die meisten Ausschlüsse die richtige Ebene.

### Responsive Suchanzeigen — `05_responsive_search_ads.csv`

`Campaign`, `Ad Group`, `Ad Type` (`Responsive search ad`), `Headline 1` bis `Headline 15`, `Headline 1 Position` bis `Headline 15 Position` (nur bei Pinning), `Description 1` bis `Description 4`, `Description 1 Position` bis `Description 4 Position`, `Path 1`, `Path 2`, `Final URL`, `Status`

Ungenutzte Überschriftenspalten bleiben leer. Positionsspalten nur befüllen, wenn wirklich gepinnt wird — ein versehentlich gesetzter Wert schränkt die Ausspielung ein.

### Assets

**`06_sitelinks.csv`** — `Campaign`, `Ad Group`, `Sitelink Text`, `Description Line 1`, `Description Line 2`, `Final URL`, `Status`

**`07_callouts.csv`** — `Campaign`, `Ad Group`, `Callout Text`, `Status`

**`08_structured_snippets.csv`** — `Campaign`, `Ad Group`, `Header`, `Snippet Values`, `Status`. Die Werte stehen semikolongetrennt in einer Zelle.

**`09_prices.csv`** — `Campaign`, `Price Type`, `Price Qualifier`, `Language`, `Currency`, `Item Header`, `Item Description`, `Item Price`, `Item Unit`, `Item Final URL`

`Price Type`: `Brands`, `Events`, `Locations`, `Neighborhoods`, `Product categories`, `Product tiers`, `Services`, `Service categories`, `Service tiers`
`Price Qualifier`: `From`, `Up to`, `Average`
`Item Unit`: `per hour`, `per day`, `per week`, `per month`, `per year`, `per night`

Bleibt `Ad Group` bei einem Asset leer, hängt es an der Kampagne. Das ist der Normalfall — Assets auf Anzeigengruppenebene lohnen sich nur, wenn sich die Aussagen zwischen den Gruppen deutlich unterscheiden.

### Performance Max Asset Groups — `10_pmax_asset_groups.csv`

`Campaign`, `Asset Group`, `Asset Group Status`, `Final URL`, `Headline 1`–`Headline 5`, `Long Headline 1`–`Long Headline 5`, `Description 1`–`Description 5`, `Business Name`, `Call To Action`, `Path 1`, `Path 2`

**Grenzen des CSV-Imports bei PMax, die im Übergabeprotokoll stehen müssen:**

- **Bilder, Logos und Videos lassen sich nicht per CSV hochladen.** Sie müssen vorher als Assets im Konto liegen; die Zuordnung erfolgt im Editor oder in der Weboberfläche.
- **Zielgruppensignale** werden nicht zuverlässig per CSV übernommen und sind manuell zu setzen.
- Ohne Bilder und Logos ist die Asset Group unvollständig und die Kampagne **wird nicht ausgeliefert**. Genau deshalb gehört dieser Punkt sichtbar auf die Checkliste und nicht in eine Fußnote.

## Wenn der Import trotzdem klemmt

1. **Spaltenzuordnung im Importdialog prüfen.** Nicht erkannte Spalten lassen sich dort zuordnen oder ignorieren.
2. **Nur die Kampagnendatei importieren.** Läuft die durch, liegt der Fehler in einer der abhängigen Dateien.
3. **Kodierung prüfen.** Falsch dargestellte Umlaute deuten auf eine Datei hin, die nicht als UTF-8 gespeichert wurde.
4. **Kampagnenname abgleichen.** Er muss in allen Dateien zeichengenau identisch sein, inklusive Leerzeichen. Das ist die mit Abstand häufigste Fehlerquelle.
5. **Kontoexport ziehen und angleichen.** *Konto → Exportieren → Ganzes Konto als CSV exportieren* liefert die exakten Überschriften der installierten Version; damit dann `build_csv.py --reference-export` laufen lassen.
