# Anzeigentexte: Limits, Richtlinien, Muster

Inhalt:
1. Zeichenlimits aller Felder
2. Google-Richtlinien, an denen Anzeigen scheitern
3. Wie eine gute RSA aufgebaut ist
4. Keyword-Einfügung und Pinning
5. Structured-Snippet-Header (Listen)
6. Preis-Assets
7. Formulierungsbausteine Deutsch

---

## 1. Zeichenlimits

Zeichen zählen heißt: jedes Zeichen inklusive Leerzeichen und Satzzeichen. Emojis zählen als mindestens 2 und sind in Suchanzeigen ohnehin nicht zulässig. Umlaute zählen als ein Zeichen.

### Responsive Suchanzeige (RSA)

| Feld | Anzahl | Limit |
|---|---|---|
| Überschrift (Headline) | 3–15, empfohlen 15 | 30 |
| Beschreibung (Description) | 2–4, empfohlen 4 | 90 |
| Anzeigepfad 1 (Path 1) | optional | 15 |
| Anzeigepfad 2 (Path 2) | optional | 15 |
| Finale URL | Pflicht | — |

Erweiterte Textanzeigen (ETA) werden nicht mehr erstellt. Erzeuge sie nicht.

### Performance Max Asset Group

| Feld | Anzahl | Limit |
|---|---|---|
| Kurze Überschrift | 3–15 | 30 |
| Lange Überschrift | 1–5 | 90 |
| Kurze Beschreibung | 1 | 60 |
| Beschreibung | 1–4 | 90 |
| Unternehmensname | 1 | 25 |
| Handlungsaufforderung | 1 | vorgegebene Liste oder automatisch |

Mindestens eine kurze Beschreibung mit 60 Zeichen ist Pflicht — sie wird an Platzierungen ausgespielt, an denen wenig Raum ist. Wer sie vergisst, bekommt eine unvollständige Asset Group.

Bildanforderungen (nicht per CSV importierbar, nur zur Information für die Checkliste):

| Typ | Seitenverhältnis | Mindestgröße | Anzahl |
|---|---|---|---|
| Marketingbild | 1,91:1 | 600 × 314 | bis 20 |
| Marketingbild quadratisch | 1:1 | 300 × 300 | bis 20 |
| Marketingbild Hochformat | 4:5 | 480 × 600 | bis 20 |
| Logo | 1:1 | 128 × 128 | bis 5 |
| Logo quer | 4:1 | 512 × 128 | bis 5 |
| Video | — | ab 10 Sekunden | bis 5 |

Fehlt ein Video, erzeugt Google automatisch eines aus den Bildern. Das Ergebnis ist meist schwach — ein eigenes Video gehört auf die Checkliste.

### Assets / Erweiterungen

| Asset | Feld | Limit | Mindestanzahl |
|---|---|---|---|
| Sitelink | Linktext | 25 | 2, empfohlen 4–6 |
| Sitelink | Beschreibungszeile 1 | 35 | — |
| Sitelink | Beschreibungszeile 2 | 35 | — |
| Callout | Text | 25 | 2, empfohlen 4–8 |
| Structured Snippet | Header | vorgegebene Liste | 1, empfohlen 2 |
| Structured Snippet | Wert | 25 | 3–10 Werte je Header |
| Preis | Kopfzeile je Eintrag | 25 | 3–8 Einträge |
| Preis | Beschreibung je Eintrag | 25 | — |
| Promotion | Artikel | 20 | — |
| Anruf | Telefonnummer | — | verifiziert |

Beide Sitelink-Beschreibungszeilen entweder ausfüllen oder beide leer lassen. Nur eine gefüllte Zeile wird nicht ausgeliefert.

---

## 2. Richtlinien, an denen Anzeigen scheitern

Diese Punkte sind nicht Stilgeschmack, sondern führen zur Ablehnung oder zu schlechtem Anzeigenrang.

**Großschreibung.** Keine durchgehenden Großbuchstaben. `JETZT KAUFEN` wird abgelehnt, `Jetzt kaufen` ist in Ordnung. Etablierte Schreibweisen wie `GmbH`, `SEO`, `BMW` sind erlaubt.

**Satzzeichen.** Keine wiederholten oder auffälligen Zeichen: `!!!`, `???`, `***`. Höchstens ein Ausrufezeichen pro Anzeige, und nie in der Überschrift.

**Superlative ohne Beleg.** `Bester Anbieter Deutschlands`, `Nummer 1` und `Testsieger` sind nur zulässig, wenn der Beleg auf der Landingpage steht und aus den letzten 12 Monaten stammt. Findest du beim Website-Scan keinen Beleg, formuliere um. Statt `Bester Steuerberater` besser `Seit 1998 in München` — konkret schlägt Superlativ ohnehin.

**Klick-Aufforderungen ohne Inhalt.** `Klicken Sie hier` ist untersagt. Die Handlungsaufforderung muss sagen, was passiert: `Termin buchen`, `Angebot anfordern`, `Preise ansehen`.

**Platzhalter und Fülltext.** Kein `xxx`, kein Lorem Ipsum, keine offenen Platzhalter wie `[Stadt]`, sofern nicht die echte Keyword-Einfügungssyntax verwendet wird.

**Telefonnummern im Anzeigentext.** Gehören ins Anruf-Asset, nicht in Überschrift oder Beschreibung.

**Markenrechte.** Fremde Marken gehören nicht in den Anzeigentext, auch nicht in Vergleichsform. Als Keyword ist eine fremde Marke zulässig, im Text nicht.

**Landingpage-Übereinstimmung.** Was die Anzeige verspricht, muss auf der Zielseite stehen. Ein Preis in der Anzeige, der auf der Seite nicht auffindbar ist, ist ein Verstoß gegen die Richtlinie zu unzutreffenden Angaben. Deshalb ist Stufe 2 nicht optional.

**Reglementierte Bereiche.** Bei Gesundheit, Finanzen, Glücksspiel, Alkohol, Arzneimitteln oder juristischen Dienstleistungen gelten Zusatzauflagen bis hin zur Zertifizierungspflicht. Erkennst du beim Website-Scan eine solche Branche, weise ausdrücklich darauf hin, statt die Kampagne kommentarlos zu bauen — der Nutzer soll vor dem Import wissen, dass eine Zertifizierung nötig sein kann.

**Dynamische Keyword-Einfügung** ersetzt keine Prüfung. Sie kann Texte erzeugen, die das Limit sprengen oder unsinnig lesen — siehe Abschnitt 4.

---

## 3. Aufbau einer guten RSA

15 Überschriften sind kein Füllauftrag. Der Algorithmus kombiniert sie, und er braucht **unterschiedliche Aussagen**, nicht 15 Varianten desselben Satzes. Diese Verteilung hat sich bewährt:

| Anzahl | Rolle | Beispiel |
|---|---|---|
| 3–4 | Keyword wörtlich oder eng | `Rohrreinigung München` |
| 2–3 | Hauptnutzen | `In 60 Minuten vor Ort` |
| 2 | Alleinstellungsmerkmal | `Festpreis ohne Aufschlag` |
| 2 | Preis oder Angebot | `Ab 89 € inkl. Anfahrt` |
| 2 | Vertrauen | `Seit 1998 · 4,8 Sterne` |
| 2 | Handlungsaufforderung | `Jetzt Termin sichern` |

Die vier Beschreibungen sollen ebenfalls verschiedene Aufgaben erfüllen: eine erklärt das Angebot, eine bringt den Beweis (Zahlen, Jahre, Bewertungen), eine räumt einen Einwand aus (Kosten, Aufwand, Risiko), eine fordert zur Handlung auf.

Der Anzeigepfad ist Gratis-Relevanz: `beispiel.de/Rohrreinigung/Notdienst` liest sich passender als die nackte Domain. Beide Pfadfelder nutzen.

**Vielfaltstest vor der Abgabe:** Nimm zwei beliebige Überschriften. Sagen sie im Kern dasselbe, ersetze eine.

---

## 4. Keyword-Einfügung und Pinning

Dynamische Keyword-Einfügung schreibt sich `{KeyWord:Ersatztext}`. Der Ersatztext greift, wenn das Keyword zu lang ist — er muss deshalb allein funktionieren und ins Limit passen. Rechne beim Prüfen mit der **längsten** möglichen Einsetzung, nicht mit dem Ersatztext.

Einsetzen lohnt sich in ein bis zwei Überschriften, nicht durchgehend. Bei Anzeigengruppen mit sehr unterschiedlichen Keywords lieber weglassen — die Ergebnisse lesen sich dann oft holprig.

**Pinning** fixiert eine Überschrift auf Position 1, 2 oder 3. Es schränkt die Kombinationsmöglichkeiten stark ein und senkt in der Regel die Anzeigenstärke. Nur einsetzen, wenn es einen echten Grund gibt: Pflichtangaben, rechtlich nötige Hinweise oder ein Markenname, der immer zuerst stehen muss. Wenn du pinnst, pinne mindestens zwei bis drei Überschriften auf dieselbe Position, damit Google noch etwas zu testen hat.

---

## 5. Structured-Snippet-Header

Der Header muss aus der von Google vorgegebenen Liste stammen und zur Anzeigensprache passen. Freitext wird abgelehnt.

**Deutsch:** Ausstattung, Dienstleistungen, Kurse, Marken, Modelle, Reiseziele, Stadtteile, Studiengänge, Stile, Typen, Versicherungsschutz, Vorstellungen, Empfohlene Hotels, Serviceleistungen

**Englisch:** Amenities, Brands, Courses, Degree programs, Destinations, Featured hotels, Insurance coverage, Models, Neighborhoods, Service catalog, Shows, Styles, Types

Pro Header 3 bis 10 Werte, jeder maximal 25 Zeichen. Die Werte müssen echte Aufzählungsglieder derselben Kategorie sein — `Marken: Bosch, Siemens, Miele` funktioniert, `Marken: Günstig, Schnell, Gut` nicht.

Die Liste kann sich ändern. Passt keiner der Header, ist das ein Grund, kein Snippet zu bauen — nicht, einen Header zu erfinden.

---

## 6. Preis-Assets

Preis-Assets zeigen 3 bis 8 Einträge mit Preis und Link. Sie sind stark, weil sie Fläche belegen und Preisvergleicher vorqualifizieren.

Pro Eintrag: Kopfzeile (25), Beschreibung (25), Betrag, Währung, optional Einheit (pro Stunde, pro Tag, pro Monat …) und eigene finale URL.

Preisangabe (`Ab`, `Bis zu`, `Durchschnittlich`) sauber wählen. **Der Preis muss auf der Zielseite auffindbar sein.** Findest du beim Website-Scan keine Preise, baue kein Preis-Asset und weise darauf hin — geschätzte Preise in Anzeigen sind ein Richtlinienverstoß mit realem Ärgerpotenzial.

Alle Einträge eines Preis-Assets brauchen denselben Typ (etwa alle `Dienstleistungen`) und dieselbe Währung.

---

## 7. Formulierungsbausteine Deutsch

Als Startpunkt, nicht zum wörtlichen Abschreiben — generische Anzeigen wirken generisch.

**Überschriften mit Nutzen:** In 24 Std. geliefert · Ohne Grundgebühr · Termin in 48 Std. · Kostenlos testen · Beratung ohne Kosten · Rückruf in 15 Minuten

**Vertrauen:** Seit {Jahr} am Markt · Über {n} Kunden · 4,8 von 5 Sternen · TÜV-geprüft · Meisterbetrieb · Zertifiziert nach ISO 9001

**Preis und Angebot:** Ab {Betrag} € · Festpreis garantiert · Keine versteckten Kosten · Versandkostenfrei ab {Betrag} €

**Handlungsaufforderung:** Jetzt Angebot anfordern · Termin online buchen · Preise vergleichen · Kostenlos beraten lassen · Direkt online bestellen

**Für Beschreibungen:** Beginne mit dem konkreten Nutzen, bring im zweiten Satz den Beleg, schließe mit der Handlungsaufforderung. Beispiel mit 88 Zeichen: `Rohrreinigung zum Festpreis, rund um die Uhr. Meisterbetrieb seit 1998. Jetzt anrufen.`

Achte auf die Ansprache der Webseite. Siezt sie, siezen die Anzeigen. Duzt sie, duzen sie — Bruch in der Ansprache zwischen Anzeige und Landingpage kostet Vertrauen.
