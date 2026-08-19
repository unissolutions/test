#!/usr/bin/env python3
"""Prueft einen campaign-plan.json gegen Google-Ads-Limits und -Richtlinien.

Fehler blockieren den Export, Warnungen zeigen Qualitaetsmaengel.
Aufruf:  python3 validate_plan.py campaign-plan.json [--json]
Exit 0 = keine Fehler, Exit 1 = Fehler gefunden.
"""
import json
import re
import sys
from pathlib import Path

LIMITS = {
    "headline": 30, "description": 90, "path": 15,
    "sitelink_text": 25, "sitelink_desc": 35, "callout": 25,
    "snippet_value": 25, "price_header": 25, "price_desc": 25,
    "pmax_headline": 30, "pmax_long_headline": 90,
    "pmax_short_description": 60, "pmax_description": 90,
    "pmax_business_name": 25, "promotion_item": 20,
}

MATCH_TYPES = {"Broad", "Phrase", "Exact"}
BID_STRATEGIES = {
    "Manual CPC", "Maximize clicks", "Maximize conversions",
    "Maximize conversion value", "Target CPA", "Target ROAS",
}
SNIPPET_HEADERS_DE = {
    "Ausstattung", "Dienstleistungen", "Kurse", "Marken", "Modelle",
    "Reiseziele", "Stadtteile", "Studiengänge", "Stile", "Typen",
    "Versicherungsschutz", "Vorstellungen", "Empfohlene Hotels", "Serviceleistungen",
}
SNIPPET_HEADERS_EN = {
    "Amenities", "Brands", "Courses", "Degree programs", "Destinations",
    "Featured hotels", "Insurance coverage", "Models", "Neighborhoods",
    "Service catalog", "Shows", "Styles", "Types",
}
PRICE_TYPES = {
    "Brands", "Events", "Locations", "Neighborhoods", "Product categories",
    "Product tiers", "Services", "Service categories", "Service tiers",
}
PRICE_QUALIFIERS = {"From", "Up to", "Average"}

BANNED_PHRASES = [
    (r"\bklicken\s+sie\s+hier\b", "'Klicken Sie hier' ist als Handlungsaufforderung untersagt"),
    (r"\bhier\s+klicken\b", "'Hier klicken' ist als Handlungsaufforderung untersagt"),
    (r"\bclick\s+here\b", "'Click here' ist als Handlungsaufforderung untersagt"),
    (r"\bjetzt\s+klicken\b", "'Jetzt klicken' ist als Handlungsaufforderung untersagt"),
]
UNPROVEN_SUPERLATIVES = [
    "beste", "bester", "besten", "nummer 1", "nr. 1", "nr.1", "weltweit führend",
    "marktführer", "testsieger", "günstigste", "billigste", "größte", "einzige",
]
PHONE_RE = re.compile(r"(\+?\d[\d\s/()-]{7,}\d)")
DKI_RE = re.compile(r"\{(?:KeyWord|Keyword|KEYWORD|keyword):([^}]*)\}", re.I)
URL_RE = re.compile(r"^https?://[^\s]+$", re.I)


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, msg):
        self.errors.append({"where": where, "message": msg})

    def warn(self, where, msg):
        self.warnings.append({"where": where, "message": msg})


def visible_length(text, keywords=None):
    """Zeichenlaenge wie Google sie zaehlt.

    Bei dynamischer Keyword-Einfuegung zaehlt die laengstmoegliche Einsetzung,
    nicht der Ersatztext - sonst rutscht die Anzeige im Livebetrieb ueber das Limit.
    """
    if not text:
        return 0
    m = DKI_RE.search(text)
    if not m:
        return len(text)
    longest = m.group(1)
    for kw in keywords or []:
        if len(kw) > len(longest):
            longest = kw
    return len(DKI_RE.sub(longest, text))


def check_text(rep, where, text, limit_key, keywords=None, label="Text"):
    limit = LIMITS[limit_key]
    n = visible_length(text, keywords)
    if n > limit:
        detail = ""
        if DKI_RE.search(text):
            detail = " (laengstmoegliche Keyword-Einsetzung eingerechnet)"
        rep.error(where, f"{label} hat {n} Zeichen, erlaubt sind {limit}{detail}: {text!r}")
    if not text or not text.strip():
        rep.error(where, f"{label} ist leer")
        return
    check_policy(rep, where, text, label)


def check_policy(rep, where, text, label):
    letters = [c for c in text if c.isalpha()]
    if len(letters) >= 4 and all(c.isupper() for c in letters):
        rep.error(where, f"{label} steht komplett in Grossbuchstaben: {text!r}")
    words = re.findall(r"\b[A-ZÄÖÜ]{4,}\b", text)
    for w in words:
        if w not in {"GMBH", "ISO", "TUEV"}:
            rep.warn(where, f"{label} enthaelt das durchgehend grossgeschriebene Wort {w!r} - Google lehnt uebermaessige Grossschreibung ab")
    if re.search(r"[!?]{2,}|\*{2,}", text):
        rep.error(where, f"{label} enthaelt wiederholte Satzzeichen: {text!r}")
    if text.count("!") > 1:
        rep.error(where, f"{label} enthaelt mehr als ein Ausrufezeichen: {text!r}")
    for pattern, msg in BANNED_PHRASES:
        if re.search(pattern, text, re.I):
            rep.error(where, f"{label}: {msg} ({text!r})")
    low = text.lower()
    for sup in UNPROVEN_SUPERLATIVES:
        if re.search(r"\b" + re.escape(sup) + r"\b", low):
            rep.warn(where, f"{label} enthaelt den Superlativ {sup!r} - nur zulaessig, wenn der Beleg auf der Landingpage steht: {text!r}")
            break
    if PHONE_RE.search(text):
        rep.warn(where, f"{label} sieht nach einer Telefonnummer aus - Nummern gehoeren ins Anruf-Asset: {text!r}")


def normalise(text):
    return re.sub(r"[^a-z0-9äöüß]+", " ", (text or "").lower()).strip()


def check_final_url(rep, where, url, required=True):
    if not url:
        if required:
            rep.error(where, "Finale URL fehlt")
        return
    if not URL_RE.match(url):
        rep.error(where, f"Finale URL ist ungueltig (muss mit http:// oder https:// beginnen): {url!r}")


def check_ad(rep, where, ad, keywords):
    headlines = ad.get("headlines") or []
    descriptions = ad.get("descriptions") or []

    if len(headlines) < 3:
        rep.error(where, f"Nur {len(headlines)} Ueberschriften - mindestens 3 sind Pflicht")
    if len(headlines) > 15:
        rep.error(where, f"{len(headlines)} Ueberschriften - hoechstens 15 sind erlaubt")
    if 3 <= len(headlines) < 15:
        rep.warn(where, f"Nur {len(headlines)} von 15 Ueberschriften genutzt - ungenutzte Plaetze verschenken Kombinationen, die Google testen koennte")
    if len(descriptions) < 2:
        rep.error(where, f"Nur {len(descriptions)} Beschreibungen - mindestens 2 sind Pflicht")
    if len(descriptions) > 4:
        rep.error(where, f"{len(descriptions)} Beschreibungen - hoechstens 4 sind erlaubt")
    if len(descriptions) == 3:
        rep.warn(where, "Nur 3 von 4 Beschreibungen genutzt")

    seen = {}
    for i, h in enumerate(headlines, 1):
        text = h["text"] if isinstance(h, dict) else h
        check_text(rep, f"{where} > Ueberschrift {i}", text, "headline", keywords, "Ueberschrift")
        key = normalise(text)
        if key and key in seen:
            rep.error(f"{where} > Ueberschrift {i}", f"Doppelt zu Ueberschrift {seen[key]}: {text!r}")
        else:
            seen[key] = i
        if isinstance(h, dict) and h.get("position") not in (None, "", 0):
            pos = h["position"]
            if pos not in (1, 2, 3):
                rep.error(f"{where} > Ueberschrift {i}", f"Pinning-Position {pos!r} ungueltig, erlaubt sind 1, 2 oder 3")

    pinned = [h.get("position") for h in headlines if isinstance(h, dict) and h.get("position") in (1, 2, 3)]
    for pos in (1, 2, 3):
        n = pinned.count(pos)
        if n == 1:
            rep.warn(where, f"Nur eine Ueberschrift auf Position {pos} gepinnt - Google hat dort nichts zu testen. Mindestens 2-3 pinnen oder das Pinning weglassen")
    if len(pinned) > 6:
        rep.warn(where, f"{len(pinned)} Ueberschriften gepinnt - starkes Pinning senkt die Anzeigenstaerke deutlich")

    seen_d = {}
    for i, d in enumerate(descriptions, 1):
        text = d["text"] if isinstance(d, dict) else d
        check_text(rep, f"{where} > Beschreibung {i}", text, "description", keywords, "Beschreibung")
        key = normalise(text)
        if key and key in seen_d:
            rep.error(f"{where} > Beschreibung {i}", f"Doppelt zu Beschreibung {seen_d[key]}: {text!r}")
        else:
            seen_d[key] = i

    for field in ("path1", "path2"):
        if ad.get(field):
            check_text(rep, f"{where} > {field}", ad[field], "path", None, field)
            if "/" in ad[field] or " " in ad[field]:
                rep.error(f"{where} > {field}", f"Anzeigepfad darf keine Schraegstriche oder Leerzeichen enthalten: {ad[field]!r}")
    if ad.get("path2") and not ad.get("path1"):
        rep.error(where, "Pfad 2 ist gesetzt, Pfad 1 aber leer - Pfad 2 wird dann nicht ausgeliefert")

    check_final_url(rep, where, ad.get("final_url"))

    # Vielfalt: sagen zu viele Ueberschriften dasselbe?
    tokens = [set(normalise(h["text"] if isinstance(h, dict) else h).split()) for h in headlines]
    overlaps = 0
    for i in range(len(tokens)):
        for j in range(i + 1, len(tokens)):
            if tokens[i] and tokens[j]:
                shared = len(tokens[i] & tokens[j]) / max(len(tokens[i]), len(tokens[j]))
                if shared >= 0.75:
                    overlaps += 1
    if overlaps >= 3:
        rep.warn(where, f"{overlaps} Ueberschriftenpaare sind inhaltlich fast gleich - der Algorithmus braucht unterschiedliche Aussagen, nicht Umformulierungen desselben Versprechens")


def check_keywords(rep, where, keywords, negative=False):
    seen = set()
    for kw in keywords:
        text = kw["text"] if isinstance(kw, dict) else kw
        match = (kw.get("match") if isinstance(kw, dict) else None) or "Phrase"
        loc = f"{where} > {text!r}"
        if not text or not text.strip():
            rep.error(where, "Leeres Keyword")
            continue
        if match not in MATCH_TYPES:
            rep.error(loc, f"Match Type {match!r} ungueltig, erlaubt sind {sorted(MATCH_TYPES)}")
        if text[0] in '"[' or text[-1] in '"]':
            rep.error(loc, "Keyword enthaelt Anfuehrungszeichen oder eckige Klammern - der Match Type gehoert in die eigene Spalte, nicht in den Text")
        if len(text) > 80:
            rep.error(loc, f"Keyword hat {len(text)} Zeichen, erlaubt sind 80")
        if len(text.split()) > 10:
            rep.error(loc, f"Keyword hat {len(text.split())} Woerter, erlaubt sind 10")
        key = (text.lower().strip(), match)
        if key in seen:
            rep.warn(loc, f"Keyword doppelt mit demselben Match Type {match}")
        seen.add(key)
        if not negative and match == "Broad":
            rep.warn(loc, "Broad Match ohne Smart Bidding ist eine Budgetfalle - nur einsetzen, wenn Conversion-Tracking laeuft und die Negativliste gepflegt ist")


def check_assets(rep, where, assets, language, campaign_type="Search"):
    # Sitelinks und Callouts sind Erweiterungen der Suchanzeige. Bei Performance Max
    # steuert Google die Darstellung selbst - ein Fehlen ist dort kein Maengel.
    search_ads = campaign_type == "Search"
    sitelinks = assets.get("sitelinks") or []
    if 0 < len(sitelinks) < 2:
        rep.error(f"{where} > Sitelinks", "Mindestens 2 Sitelinks sind noetig, damit sie ausgeliefert werden")
    if 0 < len(sitelinks) < 4:
        rep.warn(f"{where} > Sitelinks", f"Nur {len(sitelinks)} Sitelinks - 4 bis 6 belegen deutlich mehr Flaeche im Suchergebnis")
    if not sitelinks and search_ads:
        rep.warn(f"{where} > Sitelinks", "Keine Sitelinks - eine Suchanzeige ohne Sitelinks verliert Flaeche im Suchergebnis und damit Klickrate")
    seen_sl = set()
    for i, sl in enumerate(sitelinks, 1):
        loc = f"{where} > Sitelink {i}"
        check_text(rep, loc, sl.get("text"), "sitelink_text", None, "Linktext")
        d1, d2 = sl.get("desc1"), sl.get("desc2")
        if bool(d1) != bool(d2):
            rep.error(loc, "Nur eine der beiden Beschreibungszeilen ist gefuellt - dann wird keine ausgeliefert. Beide fuellen oder beide leer lassen")
        for name, val in (("Beschreibungszeile 1", d1), ("Beschreibungszeile 2", d2)):
            if val:
                check_text(rep, loc, val, "sitelink_desc", None, name)
        check_final_url(rep, loc, sl.get("final_url"))
        key = normalise(sl.get("text"))
        if key in seen_sl:
            rep.error(loc, f"Linktext doppelt: {sl.get('text')!r}")
        seen_sl.add(key)

    callouts = assets.get("callouts") or []
    if 0 < len(callouts) < 2:
        rep.error(f"{where} > Callouts", "Mindestens 2 Callouts sind noetig, damit sie ausgeliefert werden")
    if not callouts and search_ads:
        rep.warn(f"{where} > Callouts", "Keine Callouts - 4 bis 8 kurze Nutzenversprechen kosten nichts und erhoehen die Klickrate")
    seen_co = set()
    for i, co in enumerate(callouts, 1):
        text = co["text"] if isinstance(co, dict) else co
        check_text(rep, f"{where} > Callout {i}", text, "callout", None, "Callout")
        if normalise(text) in seen_co:
            rep.error(f"{where} > Callout {i}", f"Callout doppelt: {text!r}")
        seen_co.add(normalise(text))

    allowed_headers = SNIPPET_HEADERS_DE if language.startswith("de") else SNIPPET_HEADERS_EN
    for i, sn in enumerate(assets.get("structured_snippets") or [], 1):
        loc = f"{where} > Structured Snippet {i}"
        header = sn.get("header")
        if header not in allowed_headers:
            rep.error(loc, f"Header {header!r} steht nicht in Googles Vorgabeliste fuer die Sprache {language!r}. Erlaubt: {sorted(allowed_headers)}")
        values = sn.get("values") or []
        if not 3 <= len(values) <= 10:
            rep.error(loc, f"{len(values)} Werte - erlaubt sind 3 bis 10")
        for v in values:
            check_text(rep, loc, v, "snippet_value", None, "Snippet-Wert")

    for i, pr in enumerate(assets.get("prices") or [], 1):
        loc = f"{where} > Preis-Asset {i}"
        if pr.get("type") not in PRICE_TYPES:
            rep.error(loc, f"Price Type {pr.get('type')!r} ungueltig. Erlaubt: {sorted(PRICE_TYPES)}")
        if pr.get("qualifier") and pr["qualifier"] not in PRICE_QUALIFIERS:
            rep.error(loc, f"Price Qualifier {pr.get('qualifier')!r} ungueltig. Erlaubt: {sorted(PRICE_QUALIFIERS)}")
        items = pr.get("items") or []
        if not 3 <= len(items) <= 8:
            rep.error(loc, f"{len(items)} Eintraege - erlaubt sind 3 bis 8")
        for j, it in enumerate(items, 1):
            iloc = f"{loc} > Eintrag {j}"
            check_text(rep, iloc, it.get("header"), "price_header", None, "Kopfzeile")
            check_text(rep, iloc, it.get("description"), "price_desc", None, "Beschreibung")
            check_final_url(rep, iloc, it.get("final_url"))
            if it.get("price") in (None, ""):
                rep.error(iloc, "Preis fehlt")


def check_asset_group(rep, where, ag):
    heads = ag.get("headlines") or []
    longs = ag.get("long_headlines") or []
    descs = ag.get("descriptions") or []

    if not 3 <= len(heads) <= 15:
        rep.error(where, f"{len(heads)} kurze Ueberschriften - erlaubt sind 3 bis 15")
    for i, h in enumerate(heads, 1):
        check_text(rep, f"{where} > Ueberschrift {i}", h, "pmax_headline", None, "Ueberschrift")

    if not 1 <= len(longs) <= 5:
        rep.error(where, f"{len(longs)} lange Ueberschriften - erlaubt sind 1 bis 5")
    for i, h in enumerate(longs, 1):
        check_text(rep, f"{where} > Lange Ueberschrift {i}", h, "pmax_long_headline", None, "Lange Ueberschrift")

    short = ag.get("short_description")
    if not short:
        rep.error(where, "Kurze Beschreibung (max. 60 Zeichen) fehlt - sie ist Pflicht und wird an platzarmen Platzierungen ausgespielt")
    else:
        check_text(rep, f"{where} > Kurze Beschreibung", short, "pmax_short_description", None, "Kurze Beschreibung")

    if not 1 <= len(descs) <= 4:
        rep.error(where, f"{len(descs)} Beschreibungen - erlaubt sind 1 bis 4 (zusaetzlich zur kurzen Beschreibung)")
    for i, d in enumerate(descs, 1):
        check_text(rep, f"{where} > Beschreibung {i}", d, "pmax_description", None, "Beschreibung")

    bn = ag.get("business_name")
    if not bn:
        rep.error(where, "Unternehmensname fehlt - er ist bei Performance Max Pflicht")
    else:
        check_text(rep, f"{where} > Unternehmensname", bn, "pmax_business_name", None, "Unternehmensname")

    check_final_url(rep, where, ag.get("final_url"))
    rep.warn(where, "Bilder, Logos und Videos lassen sich nicht per CSV importieren. Ohne sie wird die Asset Group nicht ausgeliefert - dieser Schritt gehoert in die Uebergabe-Checkliste")


def check_campaign(rep, camp, language):
    name = camp.get("name")
    where = f"Kampagne {name!r}"
    if not name:
        rep.error("Kampagne", "Name fehlt")
    ctype = camp.get("type")
    if ctype not in {"Search", "Performance Max"}:
        rep.error(where, f"Campaign Type {ctype!r} ungueltig - erlaubt sind 'Search' und 'Performance Max'")
    if camp.get("status") == "Enabled":
        rep.warn(where, "Kampagne ist auf 'Enabled' gesetzt. Neue Kampagnen pausiert anlegen, sonst laeuft nach dem Posten sofort Budget, bevor jemand die Texte gegengelesen hat")
    budget = camp.get("budget")
    if budget in (None, "") or float(budget) <= 0:
        rep.error(where, "Tagesbudget fehlt oder ist nicht positiv")
    strategy = camp.get("bid_strategy")
    if strategy not in BID_STRATEGIES:
        rep.error(where, f"Bid Strategy {strategy!r} ungueltig. Erlaubt: {sorted(BID_STRATEGIES)}")
    if strategy == "Target CPA" and not camp.get("target_cpa"):
        rep.error(where, "Bid Strategy 'Target CPA' gesetzt, aber kein target_cpa angegeben")
    if strategy == "Target ROAS" and not camp.get("target_roas"):
        rep.error(where, "Bid Strategy 'Target ROAS' gesetzt, aber kein target_roas angegeben")
    if strategy in {"Maximize conversions", "Maximize conversion value", "Target CPA", "Target ROAS"} and not camp.get("conversion_tracking", True):
        rep.error(where, f"Strategie {strategy!r} braucht funktionierendes Conversion-Tracking. Ohne Conversion-Daten 'Maximize clicks' oder 'Manual CPC' waehlen")
    if not camp.get("locations"):
        rep.warn(where, "Keine Zielregion gesetzt - die Kampagne laeuft sonst mit Googles Standardgebiet")

    all_keywords = []
    for ag in camp.get("ad_groups") or []:
        for kw in ag.get("keywords") or []:
            all_keywords.append(kw["text"] if isinstance(kw, dict) else kw)

    if ctype == "Search":
        ad_groups = camp.get("ad_groups") or []
        if not ad_groups:
            rep.error(where, "Suchkampagne ohne Anzeigengruppen")
        for ag in ad_groups:
            agw = f"{where} > Anzeigengruppe {ag.get('name')!r}"
            if not ag.get("name"):
                rep.error(where, "Anzeigengruppe ohne Namen")
            kws = ag.get("keywords") or []
            if not kws:
                rep.error(agw, "Anzeigengruppe ohne Keywords")
            if len(kws) > 30:
                rep.warn(agw, f"{len(kws)} Keywords - ueber 20 wird das Thema meist zu breit fuer eine einzige Anzeige")
            check_keywords(rep, agw, kws)
            check_keywords(rep, f"{agw} > Negative", ag.get("negative_keywords") or [], negative=True)
            ads = ag.get("ads") or []
            if not ads:
                rep.error(agw, "Anzeigengruppe ohne Anzeige")
            ag_kw = [k["text"] if isinstance(k, dict) else k for k in kws]
            for i, ad in enumerate(ads, 1):
                check_ad(rep, f"{agw} > Anzeige {i}", ad, ag_kw)
    elif ctype == "Performance Max":
        ags = camp.get("asset_groups") or []
        if not ags:
            rep.error(where, "Performance-Max-Kampagne ohne Asset Group")
        for ag in ags:
            check_asset_group(rep, f"{where} > Asset Group {ag.get('name')!r}", ag)

    check_keywords(rep, f"{where} > Negative (Kampagnenebene)", camp.get("negative_keywords") or [], negative=True)
    if not (camp.get("negative_keywords") or []):
        rep.warn(where, "Keine negativen Keywords auf Kampagnenebene - ohne sie zahlt das Konto ab dem ersten Tag fuer 'kostenlos', 'Job', 'selber machen' und aehnliche Anfragen")
    check_assets(rep, where, camp.get("assets") or {}, language, ctype)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    if not args:
        print("Aufruf: validate_plan.py campaign-plan.json [--json]", file=sys.stderr)
        return 2
    path = Path(args[0])
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"Ungueltiges JSON in {path}: {e}", file=sys.stderr)
        return 2

    rep = Report()
    language = (plan.get("meta") or {}).get("language", "de")
    campaigns = plan.get("campaigns") or []
    if not campaigns:
        rep.error("Plan", "Keine Kampagnen im Plan")
    names = set()
    for camp in campaigns:
        if camp.get("name") in names:
            rep.error("Plan", f"Kampagnenname doppelt: {camp.get('name')!r}")
        names.add(camp.get("name"))
        check_campaign(rep, camp, language)

    if as_json:
        print(json.dumps({"errors": rep.errors, "warnings": rep.warnings}, ensure_ascii=False, indent=2))
    else:
        if rep.errors:
            print(f"\n=== {len(rep.errors)} FEHLER (blockieren den Export) ===")
            for e in rep.errors:
                print(f"  [{e['where']}]\n      {e['message']}")
        if rep.warnings:
            print(f"\n=== {len(rep.warnings)} WARNUNGEN (Qualitaet) ===")
            for w in rep.warnings:
                print(f"  [{w['where']}]\n      {w['message']}")
        if not rep.errors and not rep.warnings:
            print("Pruefung sauber - keine Fehler, keine Warnungen.")
        elif not rep.errors:
            print(f"\nKeine Fehler. {len(rep.warnings)} Warnungen - Export moeglich.")
        else:
            print(f"\nExport blockiert. Behebe die {len(rep.errors)} Fehler im Plan und pruefe erneut.")
            print("Zu lange Texte werden umformuliert, nicht abgeschnitten.")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
