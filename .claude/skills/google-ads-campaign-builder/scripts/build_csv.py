#!/usr/bin/env python3
"""Erzeugt aus campaign-plan.json die CSV-Dateien fuer den Google Ads Editor.

Aufruf:
  python3 build_csv.py campaign-plan.json --out ./google-ads-export
  python3 build_csv.py campaign-plan.json --out ./export --reference-export account.csv

--reference-export gleicht die Spaltenueberschriften an einen echten Kontoexport
an. Google benennt Spalten zwischen Editor-Versionen und Oberflaechensprachen
um; der Abgleich macht die Ausgabe unabhaengig davon.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

ENCODING = "utf-8-sig"  # BOM, damit Excel Umlaute korrekt anzeigt


def norm(header):
    return re.sub(r"[^a-z0-9]", "", header.lower())


class HeaderMap:
    """Bildet kanonische Ueberschriften auf die der installierten Editor-Version ab."""

    def __init__(self, reference_path=None):
        self.lookup = {}
        if not reference_path:
            return
        try:
            with open(reference_path, newline="", encoding=ENCODING, errors="replace") as fh:
                for row in csv.reader(fh):
                    if row and any(c.strip() for c in row):
                        for cell in row:
                            cell = cell.strip()
                            if cell:
                                self.lookup.setdefault(norm(cell), cell)
                        break
        except OSError as e:
            print(f"Warnung: Referenz-Export nicht lesbar ({e}) - Standardueberschriften werden verwendet.", file=sys.stderr)
            return
        print(f"Referenz-Export gelesen: {len(self.lookup)} Spaltenueberschriften uebernommen.")

    def __call__(self, header):
        return self.lookup.get(norm(header), header)

    def row(self, headers):
        return [self(h) for h in headers]


def write_csv(out_dir, filename, headers, rows, hmap):
    if not rows:
        return None
    path = out_dir / filename
    with open(path, "w", newline="", encoding=ENCODING) as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
        w.writerow(hmap.row(headers))
        for row in rows:
            w.writerow(["" if row.get(h) is None else row.get(h) for h in headers])
    return path


def joined(values):
    return ";".join(str(v) for v in values or [])


def text_of(item):
    return item["text"] if isinstance(item, dict) else item


def build(plan, out_dir, hmap):
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []

    campaigns, ad_groups, keywords, negatives = [], [], [], []
    rsas, sitelinks, callouts, snippets, prices, asset_groups = [], [], [], [], [], []

    has_pmax = False

    for camp in plan.get("campaigns") or []:
        cname = camp.get("name")
        campaigns.append({
            "Campaign": cname,
            "Campaign Type": camp.get("type"),
            "Campaign Status": camp.get("status", "Paused"),
            "Budget": camp.get("budget"),
            "Budget Type": camp.get("budget_type", "Daily"),
            "Bid Strategy Type": camp.get("bid_strategy"),
            "Target CPA": camp.get("target_cpa"),
            "Target ROAS": camp.get("target_roas"),
            "Networks": camp.get("networks", "Google search;Search partners" if camp.get("type") == "Search" else ""),
            "Languages": joined(camp.get("languages")),
            "Location": joined(camp.get("locations")),
            "Excluded Location": joined(camp.get("excluded_locations")),
            "Start Date": camp.get("start_date"),
            "End Date": camp.get("end_date"),
        })

        for neg in camp.get("negative_keywords") or []:
            match = (neg.get("match") if isinstance(neg, dict) else None) or "Phrase"
            negatives.append({
                "Campaign": cname, "Ad Group": "",
                "Keyword": text_of(neg), "Match Type": match,
                "Criterion Type": f"Negative {match}",
            })

        for ag in camp.get("ad_groups") or []:
            agname = ag.get("name")
            ad_groups.append({
                "Campaign": cname, "Ad Group": agname,
                "Ad Group Status": ag.get("status", "Enabled"),
                "Max CPC": ag.get("max_cpc"),
                "Ad Group Type": ag.get("ad_group_type", "Standard"),
                "Target CPA": ag.get("target_cpa"),
            })
            for kw in ag.get("keywords") or []:
                keywords.append({
                    "Campaign": cname, "Ad Group": agname,
                    "Keyword": text_of(kw),
                    "Match Type": (kw.get("match") if isinstance(kw, dict) else None) or "Phrase",
                    "Status": (kw.get("status") if isinstance(kw, dict) else None) or "Enabled",
                    "Max CPC": kw.get("max_cpc") if isinstance(kw, dict) else None,
                    "Final URL": kw.get("final_url") if isinstance(kw, dict) else None,
                })
            for neg in ag.get("negative_keywords") or []:
                match = (neg.get("match") if isinstance(neg, dict) else None) or "Phrase"
                negatives.append({
                    "Campaign": cname, "Ad Group": agname,
                    "Keyword": text_of(neg), "Match Type": match,
                    "Criterion Type": f"Negative {match}",
                })
            for ad in ag.get("ads") or []:
                row = {
                    "Campaign": cname, "Ad Group": agname,
                    "Ad Type": "Responsive search ad",
                    "Path 1": ad.get("path1"), "Path 2": ad.get("path2"),
                    "Final URL": ad.get("final_url") or ag.get("final_url"),
                    "Status": ad.get("status", "Enabled"),
                }
                for i, h in enumerate(ad.get("headlines") or [], 1):
                    row[f"Headline {i}"] = text_of(h)
                    pos = h.get("position") if isinstance(h, dict) else None
                    if pos in (1, 2, 3):
                        row[f"Headline {i} Position"] = pos
                for i, d in enumerate(ad.get("descriptions") or [], 1):
                    row[f"Description {i}"] = text_of(d)
                    pos = d.get("position") if isinstance(d, dict) else None
                    if pos in (1, 2):
                        row[f"Description {i} Position"] = pos
                rsas.append(row)

        for ag in camp.get("asset_groups") or []:
            has_pmax = True
            row = {
                "Campaign": cname,
                "Asset Group": ag.get("name"),
                "Asset Group Status": ag.get("status", "Paused"),
                "Final URL": ag.get("final_url"),
                "Business Name": ag.get("business_name"),
                "Call To Action": ag.get("call_to_action"),
                "Path 1": ag.get("path1"), "Path 2": ag.get("path2"),
            }
            for i, h in enumerate(ag.get("headlines") or [], 1):
                row[f"Headline {i}"] = h
            for i, h in enumerate(ag.get("long_headlines") or [], 1):
                row[f"Long Headline {i}"] = h
            descs = ([ag["short_description"]] if ag.get("short_description") else []) + list(ag.get("descriptions") or [])
            for i, d in enumerate(descs, 1):
                row[f"Description {i}"] = d
            asset_groups.append(row)

        assets = camp.get("assets") or {}
        for sl in assets.get("sitelinks") or []:
            sitelinks.append({
                "Campaign": cname, "Ad Group": sl.get("ad_group", ""),
                "Sitelink Text": sl.get("text"),
                "Description Line 1": sl.get("desc1"),
                "Description Line 2": sl.get("desc2"),
                "Final URL": sl.get("final_url"),
                "Status": sl.get("status", "Enabled"),
            })
        for co in assets.get("callouts") or []:
            callouts.append({
                "Campaign": cname, "Ad Group": "",
                "Callout Text": text_of(co), "Status": "Enabled",
            })
        for sn in assets.get("structured_snippets") or []:
            snippets.append({
                "Campaign": cname, "Ad Group": "",
                "Header": sn.get("header"),
                "Snippet Values": joined(sn.get("values")),
                "Status": "Enabled",
            })
        for pr in assets.get("prices") or []:
            for it in pr.get("items") or []:
                prices.append({
                    "Campaign": cname,
                    "Price Type": pr.get("type"),
                    "Price Qualifier": pr.get("qualifier"),
                    "Language": pr.get("language", (plan.get("meta") or {}).get("language", "de")),
                    "Currency": pr.get("currency", (plan.get("meta") or {}).get("currency", "EUR")),
                    "Item Header": it.get("header"),
                    "Item Description": it.get("description"),
                    "Item Price": it.get("price"),
                    "Item Unit": it.get("unit"),
                    "Item Final URL": it.get("final_url"),
                })

    max_h = max((len(a.get("headlines") or []) for c in plan.get("campaigns") or [] for g in c.get("ad_groups") or [] for a in g.get("ads") or []), default=0)
    max_d = max((len(a.get("descriptions") or []) for c in plan.get("campaigns") or [] for g in c.get("ad_groups") or [] for a in g.get("ads") or []), default=0)
    rsa_headers = ["Campaign", "Ad Group", "Ad Type"]
    for i in range(1, max_h + 1):
        rsa_headers += [f"Headline {i}", f"Headline {i} Position"]
    for i in range(1, max_d + 1):
        rsa_headers += [f"Description {i}", f"Description {i} Position"]
    rsa_headers += ["Path 1", "Path 2", "Final URL", "Status"]

    ag_max_h = max((len(g.get("headlines") or []) for c in plan.get("campaigns") or [] for g in c.get("asset_groups") or []), default=0)
    ag_max_lh = max((len(g.get("long_headlines") or []) for c in plan.get("campaigns") or [] for g in c.get("asset_groups") or []), default=0)
    ag_max_d = max(((1 if g.get("short_description") else 0) + len(g.get("descriptions") or []) for c in plan.get("campaigns") or [] for g in c.get("asset_groups") or []), default=0)
    pmax_headers = ["Campaign", "Asset Group", "Asset Group Status", "Final URL"]
    pmax_headers += [f"Headline {i}" for i in range(1, ag_max_h + 1)]
    pmax_headers += [f"Long Headline {i}" for i in range(1, ag_max_lh + 1)]
    pmax_headers += [f"Description {i}" for i in range(1, ag_max_d + 1)]
    pmax_headers += ["Business Name", "Call To Action", "Path 1", "Path 2"]

    files = [
        ("01_campaigns.csv", ["Campaign", "Campaign Type", "Campaign Status", "Budget", "Budget Type",
                              "Bid Strategy Type", "Target CPA", "Target ROAS", "Networks", "Languages",
                              "Location", "Excluded Location", "Start Date", "End Date"], campaigns),
        ("02_ad_groups.csv", ["Campaign", "Ad Group", "Ad Group Status", "Max CPC", "Ad Group Type", "Target CPA"], ad_groups),
        ("03_keywords.csv", ["Campaign", "Ad Group", "Keyword", "Match Type", "Status", "Max CPC", "Final URL"], keywords),
        ("04_negative_keywords.csv", ["Campaign", "Ad Group", "Keyword", "Match Type", "Criterion Type"], negatives),
        ("05_responsive_search_ads.csv", rsa_headers, rsas),
        ("06_sitelinks.csv", ["Campaign", "Ad Group", "Sitelink Text", "Description Line 1", "Description Line 2", "Final URL", "Status"], sitelinks),
        ("07_callouts.csv", ["Campaign", "Ad Group", "Callout Text", "Status"], callouts),
        ("08_structured_snippets.csv", ["Campaign", "Ad Group", "Header", "Snippet Values", "Status"], snippets),
        ("09_prices.csv", ["Campaign", "Price Type", "Price Qualifier", "Language", "Currency",
                           "Item Header", "Item Description", "Item Price", "Item Unit", "Item Final URL"], prices),
        ("10_pmax_asset_groups.csv", pmax_headers, asset_groups),
    ]

    for filename, headers, rows in files:
        path = write_csv(out_dir, filename, headers, rows, hmap)
        if path:
            written.append((path.name, len(rows)))

    write_instructions(out_dir, written, has_pmax, hmap)
    return written


def write_instructions(out_dir, written, has_pmax, hmap):
    lines = [
        "# Import in den Google Ads Editor",
        "",
        "## Bevor du startest",
        "",
        "Der Import im Editor **veraendert das Live-Konto noch nicht**. Alles landet",
        "zunaechst als lokaler Entwurf und wird als Vorschau angezeigt. Erst *Posten*",
        "uebertraegt die Aenderungen. Ein Testimport ist also gefahrlos.",
        "",
        "## Reihenfolge",
        "",
        "Importiere die Dateien einzeln und genau in dieser Reihenfolge. Uebergeordnete",
        "Ebenen zuerst, sonst finden die Zeilen ihren Elternknoten nicht:",
        "",
    ]
    for i, (name, count) in enumerate(written, 1):
        lines.append(f"{i}. `{name}` — {count} Zeile{'n' if count != 1 else ''}")
    lines += [
        "",
        "## Schritt fuer Schritt",
        "",
        "1. Google Ads Editor oeffnen und das Zielkonto herunterladen (*Aktuelle Aenderungen abrufen*).",
        "2. *Konto → Importieren → Aus Datei importieren* waehlen.",
        "3. Die erste CSV auswaehlen.",
        "4. **Spaltenzuordnung pruefen.** Der Editor zeigt eine Vorschau. Nicht erkannte",
        "   Spalten lassen sich dort manuell zuordnen oder ignorieren — eine abweichende",
        "   Ueberschrift ist damit kein Grund, die Datei neu zu bauen.",
        "5. Vorschau der Aenderungen durchsehen, dann bestaetigen.",
        "6. Mit der naechsten Datei wiederholen.",
        "7. Erst wenn alles stimmt: *Posten*.",
        "",
        "## Haeufige Fehler",
        "",
        "| Symptom | Ursache |",
        "|---|---|",
        "| \"Kampagne nicht gefunden\" | Kampagnenname weicht zwischen den Dateien ab — er muss zeichengenau identisch sein |",
        "| Umlaute als `Ã¼` | Datei wurde nicht als UTF-8 gespeichert |",
        "| Keyword abgelehnt | Anfuehrungszeichen oder eckige Klammern im Keyword-Text; der Match Type gehoert in die eigene Spalte |",
        "| Anzeige abgelehnt | Text ueber dem Zeichenlimit oder Richtlinienverstoss — `validate_plan.py` erneut laufen lassen |",
        "| Spalten nicht erkannt | Im Importdialog manuell zuordnen, oder `build_csv.py --reference-export` mit einem Kontoexport nutzen |",
        "",
        "## Nach dem Import noch zu erledigen",
        "",
        "- Conversion-Tracking pruefen — ohne Conversions arbeiten Smart-Bidding-Strategien blind",
        "- Zeitplan und Gebotsanpassungen nach Geraet festlegen",
        "- Anruf-Assets mit verifizierter Rufnummer ergaenzen",
        "- Standort-Targeting feinjustieren (Radius, Ausschluesse)",
        "- Kampagnen erst aktivieren, wenn die Texte gegengelesen sind",
    ]
    if has_pmax:
        lines += [
            "",
            "## Performance Max — Pflichtschritte ausserhalb der CSV",
            "",
            "Die Asset Group ist nach dem Import **unvollstaendig und wird nicht ausgeliefert**,",
            "solange diese Punkte fehlen. Sie lassen sich nicht per CSV importieren:",
            "",
            "- **Bilder**: mindestens je eines in 1,91:1 (ab 600×314), 1:1 (ab 300×300) und 4:5 (ab 480×600)",
            "- **Logo**: 1:1 ab 128×128, zusaetzlich 4:1 empfohlen",
            "- **Video**: ab 10 Sekunden. Fehlt es, generiert Google automatisch eines aus den Bildern — das Ergebnis ist meist schwach",
            "- **Zielgruppensignale**: manuell setzen, sie werden per CSV nicht zuverlaessig uebernommen",
        ]
    (out_dir / "IMPORT-ANLEITUNG.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description="Erzeugt Google-Ads-Editor-CSVs aus einem Kampagnenplan.")
    p.add_argument("plan")
    p.add_argument("--out", default="./google-ads-export")
    p.add_argument("--reference-export", default=None,
                   help="Kontoexport aus dem Google Ads Editor, an dessen Spaltenueberschriften die Ausgabe angeglichen wird")
    args = p.parse_args()

    try:
        plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {args.plan}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"Ungueltiges JSON in {args.plan}: {e}", file=sys.stderr)
        return 2

    out_dir = Path(args.out)
    hmap = HeaderMap(args.reference_export)
    written = build(plan, out_dir, hmap)

    print(f"\n{len(written)} Dateien geschrieben nach {out_dir}/:")
    for name, count in written:
        print(f"  {name:34} {count:4} Zeilen")
    print(f"  {'IMPORT-ANLEITUNG.md':34}")
    if not args.reference_export:
        print("\nHinweis: Ohne --reference-export werden Standardueberschriften verwendet.")
        print("Der Editor bietet beim Import eine Spaltenzuordnung an, falls eine Ueberschrift abweicht.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
