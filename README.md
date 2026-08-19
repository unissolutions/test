# test

Repository mit einem Claude-Code-Skill.

## Skills

### `google-ads-campaign-builder`

Baut aus einer Webseite eine importfertige Google-Ads-Kampagne: Website-Scan →
Keyword-Recherche → Kampagnenstruktur → Anzeigentexte und Assets → CSV-Dateien
für den Google Ads Editor. Unterstützt Suchkampagnen und Performance Max.

**Nutzung:** Einfach die Aufgabe beschreiben — der Skill greift automatisch,
sobald es um Google Ads, Anzeigentexte, Keyword-Recherche für bezahlte Werbung
oder einen Editor-Import geht.

```
Bau mir eine Google-Ads-Suchkampagne für https://meine-seite.de,
Budget 40 € am Tag, Zielgebiet München.
```

**Aufbau:**

| Pfad | Inhalt |
|---|---|
| `SKILL.md` | Der sechsstufige Arbeitsablauf |
| `references/ad-copy-rules.md` | Zeichenlimits aller Felder, Google-Richtlinien, RSA-Aufbau |
| `references/keyword-research.md` | Recherche mit und ohne Ahrefs, Suchintention, negative Keywords |
| `references/csv-schema.md` | Spalten je Entität, Importreihenfolge, Fehlerbehebung |
| `scripts/validate_plan.py` | Prüft Zeichenlimits, Pflichtfelder, Duplikate und Richtlinienverstöße |
| `scripts/build_csv.py` | Erzeugt die Editor-CSVs samt Importanleitung |
| `assets/campaign-plan.example.json` | Vollständiges Beispiel (Suche + Performance Max) |
| `assets/campaign-plan.schema.json` | Formale Definition des Planformats |

**Selbst ausprobieren** — beides läuft mit purem Python 3, ohne Zusatzpakete:

```bash
SKILL=.claude/skills/google-ads-campaign-builder
python3 "$SKILL/scripts/validate_plan.py" "$SKILL/assets/campaign-plan.example.json"
python3 "$SKILL/scripts/build_csv.py"     "$SKILL/assets/campaign-plan.example.json" --out ./export
```

**Warum ein Validator?** Zeichen zählt man beim Schreiben zuverlässig falsch, und
der Google Ads Editor lehnt eine Anzeige mit 31 statt 30 Zeichen kommentarlos ab.
Das Skript rechnet zusätzlich die längstmögliche dynamische Keyword-Einsetzung
mit ein — ein Text, der auf dem Papier passt, kann im Livebetrieb darüber liegen.

**Spaltennamen:** Google benennt CSV-Spalten zwischen Editor-Versionen und
Oberflächensprachen um. Mit `--reference-export <kontoexport.csv>` richtet sich
die Ausgabe an einem echten Export der installierten Version aus. Zusätzlich
bietet der Editor beim Import eine manuelle Spaltenzuordnung an.
