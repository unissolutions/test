#!/usr/bin/env python3
"""Wunschmaß-Bestätigung im Zuschnitt-Konfigurator (Stegplatten-Produktseiten).

  zuschnitt_patch.py <theme-datei> [<ausgabe>]

Patcht die Theme-Datei, die den Zuschnitt-Konfigurator enthält (id="save-z-btn", Button „Zuschnitte übernehmen“ –
z. B. snippets/es-zuschnitt.liquid). Änderungen:
  1. Pflicht-Checkbox über den Buttons: Kunde bestätigt, die Maße selbst geprüft zu haben (Zuschnitt nach Wunschmaß,
     kein Umtausch/Widerruf).
  2. „Zuschnitte übernehmen“ ist ohne Häkchen gesperrt (Fehlertext, Fokus auf die Checkbox).
  3. Warenkorb-Eigenschaft „Maße bestätigt: Ja – vom Kunden geprüft (Datum)“ wird mit übergeben, Hinweis in der Zusammenfassung.
  4. Beim erneuten Bearbeiten der Zuschnitte muss neu bestätigt werden.
Regex-basiert und whitespace-tolerant; jede Fundstelle muss genau einmal vorkommen (sonst Abbruch)."""
import re, sys, pathlib

src_path = pathlib.Path(sys.argv[1])
out_path = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else src_path
s = src_path.read_text(encoding='utf-8')
assert 'z-confirm-input' not in s, 'bereits gepatcht'


def sub1(pattern, repl, s):
    n = len(re.findall(pattern, s, re.S))
    assert n == 1, f'Fundstelle {n}x statt 1x: {pattern[:70]!r}'
    return re.sub(pattern, repl, s, count=1, flags=re.S)


CHECK = ('<label class="z-confirm" for="z-confirm-input"><input type="checkbox" id="z-confirm-input" value="1"> '
         '<span>Ich habe alle Maße selbst geprüft. Die Zuschnitte werden exakt nach meinen Angaben gefertigt – '
         'nachträgliche Maßänderung, Umtausch oder Widerruf sind ausgeschlossen.</span></label>'
         '<div class="z-field-error" id="z-confirm-error" aria-live="polite"></div>\n')
# 1) Checkbox vor dem Button-Block
s = sub1(r'(<div style="margin-top:\s*15px;?\s*">\s*<button type="button" id="save-z-btn")', lambda m: CHECK + m.group(1), s)
# 2) Sperre im Klick-Handler
GUARD = (" const zc = document.getElementById('z-confirm-input'), zce = document.getElementById('z-confirm-error');"
         " if (zc && !zc.checked) { if (zce) zce.textContent = 'Bitte bestätigen Sie, dass Sie die Maße geprüft haben.'; zc.focus(); return; }"
         " if (zce) zce.textContent = '';")
s = sub1(r"(document\.getElementById\('save-z-btn'\)\.onclick\s*=\s*\(\)\s*=>\s*\{\s*const productForm = findProductForm\(\);\s*if \(!productForm\) return;)",
         lambda m: m.group(1) + GUARD, s)
# 3) Eigenschaft + Hinweis in der Zusammenfassung
PROP = (" (function () { const c = document.createElement('input'); c.type = 'hidden'; c.name = 'properties[Maße bestätigt]';"
        " c.value = 'Ja – vom Kunden geprüft (' + new Date().toLocaleDateString('de-DE') + ')'; c.className = 'generated-prop'; productForm.appendChild(c); })();")
s = sub1(r"(toggleZuschnittRequestButton\(false\);\s*setProductQuantity\(productForm, totalQty\);)", lambda m: m.group(1) + PROP, s)
s = sub1(r"(document\.getElementById\('zuschnitte-summary-text'\)\.innerHTML = summaryHTML)(;)",
         lambda m: m.group(1) + " + '<div class=\"z-confirm-ok\">✓ Maße vom Kunden geprüft und bestätigt</div>'" + m.group(2), s)
# 4) Erneute Bestätigung nach „Bearbeiten“
s = sub1(r"(document\.getElementById\('edit-z-btn'\)\.onclick\s*=\s*\(\)\s*=>\s*\{)",
         lambda m: m.group(1) + " const zc2 = document.getElementById('z-confirm-input'); if (zc2) zc2.checked = false;", s)
# 5) Styles
CSS = ('.z-confirm { display: flex; gap: 10px; align-items: flex-start; margin: 14px 0 4px; font-size: 13px; line-height: 1.45; color: #171917; cursor: pointer; }'
       ' .z-confirm input { flex: none; width: 18px; height: 18px; margin: 1px 0 0; accent-color: #338258; }'
       ' .z-confirm-ok { margin-top: 6px; color: #2A6C49; font-weight: 600; } ')
s = sub1(r'(@media \(max-width:\s*640px\)\s*\{\s*\.z-grid)', lambda m: CSS + m.group(1), s)
out_path.write_text(s, encoding='utf-8')
print('gepatcht ->', out_path, len(s.encode('utf-8')), 'Bytes')
