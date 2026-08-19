# Keyword-Recherche für Google Ads

Ziel ist nicht die längste Liste, sondern die Liste, für die sich Bezahlen lohnt. Ein Keyword gehört nur dann in die Kampagne, wenn jemand mit Kaufabsicht danach sucht und die Webseite eine passende Antwort hat.

## Weg A — mit Ahrefs (echte Daten)

Prüfe mit `ToolSearch`, ob Ahrefs-Werkzeuge verbunden sind (`mcp__Ahrefs__…`). Falls ja, arbeite in dieser Reihenfolge. Ruf `mcp__Ahrefs__doc` für ein Werkzeug auf, bevor du es zum ersten Mal benutzt — die Parameter unterscheiden sich zwischen den Endpunkten.

**1. Was rankt die Domain bereits organisch?**
`site-explorer-organic-keywords` für die Domain. Diese Begriffe sind belegt relevant. Was organisch auf Position 5–20 steht, ist oft ein guter Ads-Kandidat: nachweislich passend, aber noch nicht sichtbar genug.

**2. Wer sind die Wettbewerber und worauf ranken sie?**
`site-explorer-organic-competitors`, danach `site-explorer-organic-keywords` für die zwei bis drei relevantesten. Das deckt Begriffe auf, die auf der eigenen Seite fehlen.

**3. Seed-Begriffe ausbauen.**
Aus dem Website-Scan hast du Produkt- und Leistungsbezeichnungen. Damit:
- `keywords-explorer-matching-terms` — alles, was den Seed enthält
- `keywords-explorer-related-terms` — thematisch verwandt, ohne den Seed zu enthalten
- `keywords-explorer-search-suggestions` — echte Autocomplete-Vorschläge, gut für Long-Tail

**4. Kennzahlen holen.**
`keywords-explorer-overview` liefert Volumen, Difficulty, CPC und Klickverhalten. Der CPC ist für die Budgetplanung entscheidend: Bei 4 € CPC und 20 € Tagesbudget sind fünf Klicks am Tag realistisch — das ist eine Zahl, die der Nutzer vor dem Start kennen sollte, nicht danach.

**5. Zielmarkt richtig setzen.**
`keywords-explorer-volume-by-country`, wenn die Zielregion nicht der Standardmarkt ist. Ein Volumen aus den USA hilft bei einer Kampagne für Österreich nicht weiter.

Achtung bei Geldbeträgen: Die Ahrefs-Endpunkte liefern Werte in **US-Cent**. Für die Anzeige durch 100 teilen und ausdrücklich als USD kennzeichnen — nicht stillschweigend in Euro umdeuten.

## Weg B — ohne Ahrefs (abgeleitet)

Ohne Datenquelle leitest du Keywords aus dem Seiteninhalt ab: Produktnamen, Leistungen, Kategorien, Synonyme, Ortsbezüge, Problemformulierungen der Zielgruppe.

Kombiniere systematisch:
- Leistung + Ort: `Rohrreinigung München`
- Leistung + Absicht: `Rohrreinigung Notdienst`, `Rohrreinigung Preis`
- Problem + Lösung: `Abfluss verstopft Hilfe`
- Marke + Produkt: `Bosch Spülmaschine kaufen`

**Kennzeichne dabei jede Volumen- oder Kostenangabe klar als Schätzung.** Schreib nicht `1.200 Suchanfragen/Monat`, sondern `Volumen unbekannt — ohne Keyword-Tool nicht messbar`. Eine erfundene Zahl, die wie eine Messung aussieht, führt zu falschen Budgetentscheidungen; das ist schädlicher als eine ehrliche Lücke.

Weise den Nutzer darauf hin, dass der Google Keyword-Planer im Ads-Konto kostenlos echte Spannen liefert, und biete an, die Liste nachzuschärfen, sobald diese Daten vorliegen.

## Suchintention zuordnen

Jedes Keyword bekommt eine Einordnung — sie steuert, ob es in die Kampagne kommt und in welche Gruppe.

| Intention | Signalwörter | Für Ads |
|---|---|---|
| Transaktional | kaufen, buchen, bestellen, Preis, günstig, in der Nähe, Angebot | Kern der Kampagne |
| Kommerziell | Vergleich, Test, beste, Erfahrungen, Alternative | Gut, meist teurer |
| Navigational | Markenname, Markenname + Login | Eigene Marken-Gruppe |
| Informational | was ist, wie funktioniert, Anleitung, Ursachen | Meist aussortieren |

Informational-Begriffe erzeugen Klicks ohne Kaufabsicht. Sie haben ihren Platz im Content-Marketing, nicht im Suchkampagnen-Budget. Willst du sie testen, dann nur in einer separaten Kampagne mit eigenem, kleinem Budget — sonst fressen sie das Geld der konvertierenden Begriffe.

## Negative Keywords

Gehören zur Lieferung, nicht in ein späteres Optimierungs-Nachspiel. Ohne sie zahlt der Nutzer ab dem ersten Tag für Suchanfragen ohne jede Kaufabsicht.

**Standardliste Deutsch (kostenlose Absicht):**
kostenlos, gratis, umsonst, free, selber machen, selbst, DIY, Anleitung, Tutorial, Vorlage, Muster, Beispiel, PDF, download

**Standardliste Deutsch (falsche Zielgruppe):**
Job, Jobs, Stelle, Stellenangebot, Ausbildung, Praktikum, Gehalt, Bewerbung, Studium, Definition, Wikipedia, Bedeutung

**Nach Geschäftsmodell:**
- Neuware verkauft → gebraucht, second hand, refurbished, Ersatzteile, Reparatur
- Dienstleistung → Software, App, Tool, Vorlage
- B2B → privat, für Zuhause, Hobby
- Hochpreisig → billig, Discount, Schnäppchen
- Kein Versand ins Ausland → Ländernamen außerhalb des Zielmarkts

**Aus dem Website-Scan ergänzen:** Alles, was das Unternehmen ausdrücklich *nicht* anbietet, gehört auf die Liste. Steht auf der Seite "keine Mietwagen", dann ist `mieten` ein negatives Keyword.

Wettbewerbernamen sind ein Sonderfall: als negatives Keyword sinnvoll, wenn das Budget knapp ist; bewusst bebietbar, wenn Verdrängung das Ziel ist. Frag im Zweifel nach, statt es stillschweigend zu entscheiden.

Match Type für negative Keywords: Phrase deckt Wortkombinationen ab, Exact nur die genaue Anfrage. Für Ausschlusslisten ist Phrase meist die richtige Wahl.

## Struktur-Vorschlag ableiten

Cluster die verbleibenden Keywords nach der Frage: **Welche Seite beantwortet diese Suchanfrage am besten?** Keywords mit derselben besten Landingpage gehören in dieselbe Anzeigengruppe.

Prüfe jedes Cluster gegen diese drei Fragen:
1. Passt eine einzige Anzeige zu allen Keywords darin?
2. Führen alle auf dieselbe Seite?
3. Sind es 5 bis 20 Keywords?

Dreimal ja heißt: Anzeigengruppe steht. Sonst teilen oder zusammenlegen.

## Dokumentation

Halte das Ergebnis in `keyword-recherche.md` fest — Spalten: Keyword, Match Type, Intention, Volumen (mit Quelle oder Kennzeichnung als Schätzung), CPC, Anzeigengruppe. Ergänze die Negativliste und eine kurze Begründung, warum aussortierte Begriffe draußen bleiben. Der Nutzer soll die Entscheidungen nachvollziehen und überstimmen können.
