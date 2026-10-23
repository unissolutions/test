// Funktionstests v3: Montage (PLZ-Prüfung, Preis, Warenkorb), Angebot/Teilen, Hero-Links – auf den echt gerenderten Seiten aus render_v3.py
const { chromium } = require('playwright');
const D = '/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad/design-review/v3/';
let pass = 0, fail = 0;
const eq = (name, got, want) => { const ok = JSON.stringify(got) === JSON.stringify(want); ok ? pass++ : fail++; console.log(`${ok ? '✓' : '✗'} ${name}${ok ? '' : `\n    erwartet: ${JSON.stringify(want)}\n    erhalten: ${JSON.stringify(got)}`}`); };
const has = (name, got, part) => eq(name, String(got).includes(part), true);

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
  const pg = await ctx.newPage();
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  const txt = s => pg.textContent(s);
  const items = async () => pg.evaluate(() => __calls.filter(c => c.u === '/cart/add.js').slice(-1)[0]?.body.items);

  console.log('— Produktseite: Montage —');
  await pg.goto('file://' + D + 'pdp.html'); await pg.waitForTimeout(100);
  eq('Start: Gesamtzeile versteckt', await pg.isHidden('[data-tot]'), true);
  eq('Start: Sticky-Preis = Dachpreis', await txt('[data-sticky-price]'), '1.869,90 €');
  eq('Start: PLZ-Feld versteckt', await pg.isHidden('[data-mo-panel]'), true);
  eq('Start: Montagepreis-Platzhalter', await txt('[data-mo-price]'), 'Preis nach PLZ');
  await pg.check('[data-mo="1"]');
  eq('Montage gewählt: PLZ-Feld sichtbar', await pg.isVisible('[data-mo-panel]'), true);
  has('Montage gewählt: Hinweis PLZ eingeben', await txt('[data-mo-hint]'), 'PLZ eingeben');
  eq('Montage ohne PLZ: kein Aufpreis', await pg.isHidden('[data-tot]'), true);
  await pg.fill('[data-mo-plz]', '45881');
  eq('PLZ 45881: Zone', await txt('[data-mo-land]'), 'Zone 1 · bis 170 km');
  eq('PLZ 45881: Preis 15 m² × 67 €', await txt('[data-mo-price]'), '+ 1.005,00 €');
  has('PLZ 45881: Hinweis mit Preis', await txt('[data-mo-hint]'), 'Montage in PLZ 45881 (Zone 1 · bis 170 km): 1.005,00 €');
  eq('PLZ 45881: Gesamt sichtbar', await pg.isVisible('[data-tot]'), true);
  eq('PLZ 45881: Gesamt 1.869,90 + 1.005', await txt('[data-tot-v]'), '2.874,90 €');
  eq('PLZ 45881: Sticky zeigt Gesamt', await txt('[data-sticky-price]'), '2.874,90 €');
  await pg.fill('[data-mo-plz]', '80331');
  eq('PLZ 80331 (München): Zone 4', await txt('[data-mo-land]'), 'Zone 4 · 370–770 km');
  eq('PLZ 80331: Preis 15 m² × 112 €', await txt('[data-mo-price]'), '+ 1.680,00 €');
  await pg.fill('[data-mo-plz]', '65185');
  eq('PLZ 65 (Überschneidung): erster Treffer = Zone 2', await txt('[data-mo-land]'), 'Zone 2 · 170–270 km');
  eq('PLZ 65185: Preis 15 m² × 82,50 €', await txt('[data-mo-price]'), '+ 1.237,50 €');
  await pg.fill('[data-mo-plz]', '00123');
  eq('PLZ 00123 (keine Zone): auf Anfrage', await txt('[data-mo-price]'), 'auf Anfrage');
  has('PLZ 00123: Hinweis außerhalb', await txt('[data-mo-hint]'), 'Außerhalb unseres Montagegebiets');
  eq('PLZ 00123: Hinweis rot', (await pg.getAttribute('[data-mo-hint]', 'class')).includes('is-err'), true);
  eq('PLZ 00123: kein Aufpreis', await pg.isHidden('[data-tot]'), true);
  await pg.click('[data-atc]'); await pg.waitForTimeout(150);
  eq('PLZ 00123: Warenkorb blockiert', await pg.evaluate(() => __calls.length), 0);
  has('PLZ 00123: Fehlermeldung', await txt('[data-msg]'), 'nur per Angebot');
  await pg.fill('[data-mo-plz]', '1010');
  eq('PLZ 1010 (Wien): Österreich', await txt('[data-mo-land]'), 'Österreich');
  eq('PLZ 1010: Preis 15 m² × 151,20 €', await txt('[data-mo-price]'), '+ 2.268,00 €');
  await pg.click('[data-atc]'); await pg.waitForTimeout(150);
  eq('Warenkorb AT: Dach + Montage mit Zuordnung', await items(), [
    { id: 11016, quantity: 1 },
    { id: 7084, quantity: 1, properties: { 'Für Überdachung': 'Terrassenüberdachung Premium Anthrazit Alu mit Stegplatten 16mm klar/farblos – 5 × 3 m', 'Montageort': 'Österreich, PLZ 1010' } }]);
  await pg.waitForTimeout(2300);
  await pg.fill('[data-mo-plz]', 'a4 5x8 81');
  eq('PLZ bereinigt (nur Ziffern)', await pg.inputValue('[data-mo-plz]'), '45881');
  await pg.click('[data-w="6,00 Meter"]');
  eq('Breite 6 m: Montagepreis folgt (18 m²)', await txt('[data-mo-price]'), '+ 1.206,00 €');
  await pg.click('[data-qd="1"]');
  eq('Menge 2: Dach×2 + Montage×2', await txt('[data-tot-v]'), (2 * 224388 / 100 + 2 * 1206).toLocaleString('de-DE', { minimumFractionDigits: 2 }) + ' €');
  await pg.check('input[data-led="12"]');
  await pg.click('[data-atc]'); await pg.waitForTimeout(150);
  eq('Warenkorb DE: Dach×2, LED×2, Montage×2', await items(), [
    { id: 11023, quantity: 2 },
    { id: 902, quantity: 2, properties: { 'Für Überdachung': 'Terrassenüberdachung Premium Anthrazit Alu mit Stegplatten 16mm klar/farblos – 6 × 3 m' } },
    { id: 7115, quantity: 2, properties: { 'Für Überdachung': 'Terrassenüberdachung Premium Anthrazit Alu mit Stegplatten 16mm klar/farblos – 6 × 3 m', 'Montageort': 'PLZ 45881, Zone 1' } }]);
  await pg.waitForTimeout(2300);
  await pg.check('[data-mo="0"]');
  eq('Selbstmontage: PLZ-Feld weg', await pg.isHidden('[data-mo-panel]'), true);
  await pg.click('[data-atc]'); await pg.waitForTimeout(150);
  eq('Selbstmontage: keine Montagezeile', (await items()).map(i => i.id), [11023, 902]);

  console.log('— Produktseite: Teilen + Angebot —');
  await pg.goto('file://' + D + 'pdp.html'); await pg.waitForTimeout(100);
  eq('Panels zu', [await pg.isHidden('[data-share]'), await pg.isHidden('[data-offer]')], [true, true]);
  await pg.check('[data-mo="1"]'); await pg.fill('[data-mo-plz]', '45881'); await pg.check('input[data-led="6"]');
  await pg.click('[data-share-tg]');
  eq('Teilen offen', await pg.isVisible('[data-share]'), true);
  eq('Teilen-Button aria-expanded', await pg.getAttribute('[data-share-tg]', 'aria-expanded'), 'true');
  const url = await pg.inputValue('[data-share-url]');
  has('Link: Variante', url, 'variant=11016'); has('Link: LED', url, 'led=6'); has('Link: PLZ', url, 'mp=45881');
  has('Zusammenfassung: Montage', await txt('[data-share-sum]'), 'Montage durch e-Stegplatten (PLZ 45881, Zone 1)');
  has('Zusammenfassung: LED', await txt('[data-share-sum]'), 'LED-Spots 6er-Set');
  has('WhatsApp-Link', await pg.getAttribute('[data-share-wa]', 'href'), 'https://wa.me/?text=');
  has('E-Mail-Link', await pg.getAttribute('[data-share-mail]', 'href'), 'mailto:?subject=');
  await pg.click('[data-w="6,00 Meter"]');
  has('Link folgt Maßwechsel', await pg.inputValue('[data-share-url]'), 'variant=11023');
  await pg.click('[data-offer-tg]');
  eq('Angebot offen, Teilen zu', [await pg.isVisible('[data-offer]'), await pg.isHidden('[data-share]')], [true, true]);
  const body = await pg.inputValue('[data-offer-body]');
  has('Formular: Maß', body, 'Maß: 6 × 3 m'); has('Formular: Montage', body, 'Montage: Montage durch e-Stegplatten (PLZ 45881, Zone 1)'); has('Formular: Gesamt', body, 'Gesamt mit Auswahl: 3.649,88 €');
  eq('Formular: PLZ übernommen', await pg.inputValue('[data-offer-plz]'), '45881');
  has('Formular: Konfiguration (hidden)', await pg.inputValue('[data-offer-cfg]'), 'Link: ');
  eq('Formular: Ziel = Shopify-Kontakt', await pg.getAttribute('#es-offer-form', 'action'), '/contact#es-offer-form');
  await pg.fill('[data-offer-body]', 'Eigener Text'); await pg.click('[data-d="4,00 Meter"]');
  eq('Formular: eigener Text bleibt', await pg.inputValue('[data-offer-body]'), 'Eigener Text');
  await pg.goto('file://' + D + 'pdp.html?angebot=1'); await pg.waitForTimeout(300);
  eq('?angebot=1 öffnet das Formular', await pg.isVisible('[data-offer]'), true);
  await pg.goto('file://' + D + 'pdp.html?variant=11016&led=6&mp=45881'); await pg.waitForTimeout(100);
  eq('Geteilter Link: Montage + PLZ + LED vorbelegt', [await pg.isChecked('[data-mo="1"]'), await pg.inputValue('[data-mo-plz]'), await pg.isChecked('input[data-led="6"]'), await txt('[data-tot-v]')], [true, '45881', true, '3.074,90 €']);

  console.log('— Hero-Konfigurator —');
  await pg.goto('file://' + D + 'hero.html'); await pg.waitForTimeout(100);
  eq('Farbmuster-Link', await pg.getAttribute('.ehk__alt a[href="/products/farbmuster"]', 'href'), '/products/farbmuster');
  eq('Angebot-Link', await pg.getAttribute('[data-kao]', 'href'), '/products/dach-anthrazit-klar?variant=11016&angebot=1');
  await pg.click('[data-led="12"]'); await pg.click('[data-w="6,00 Meter"]');
  eq('Angebot-Link folgt Auswahl', await pg.getAttribute('[data-kao]', 'href'), '/products/dach-anthrazit-klar?variant=11023&led=12&angebot=1');
  eq('Weiter-Link unverändert', await pg.getAttribute('[data-kgo]', 'href'), '/products/dach-anthrazit-klar?variant=11023&led=12');

  console.log('— Mobil 390 px —');
  const m = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage();
  await m.goto('file://' + D + 'pdp.html'); await m.evaluate(() => document.fonts.ready); await m.waitForTimeout(200);
  eq('Kein horizontales Scrollen', await m.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
  await m.check('[data-mo="1"]'); await m.fill('[data-mo-plz]', '45881'); await m.click('[data-share-tg]'); await m.waitForTimeout(100);
  eq('Mobil: kein horizontales Scrollen mit offenen Panels', await m.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
  const sb = await m.evaluate(() => [...document.querySelectorAll('.es-pdp__sb')].map(e => ({ w: Math.round(e.getBoundingClientRect().width), sw: e.scrollWidth })));
  eq('Mobil: Buttons nicht abgeschnitten', sb.every(x => x.sw <= x.w + 1), true);
  await m.evaluate(() => { const e = document.querySelector('[data-mo-box]'); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 70) }); await m.waitForTimeout(150);
  await m.screenshot({ path: D + 'pdp-390-montage.png' });
  await m.evaluate(() => { const e = document.querySelector('[data-share]'); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 120) }); await m.waitForTimeout(150);
  await m.screenshot({ path: D + 'pdp-390-share.png' });
  await m.click('[data-offer-tg]'); await m.waitForTimeout(150);
  await m.evaluate(() => { const e = document.querySelector('[data-offer]'); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 120) }); await m.waitForTimeout(150);
  await m.screenshot({ path: D + 'pdp-390-offer.png' });
  await pg.goto('file://' + D + 'pdp.html'); await pg.evaluate(() => document.fonts.ready); await pg.check('[data-mo="1"]'); await pg.fill('[data-mo-plz]', '45881'); await pg.click('[data-offer-tg]'); await pg.waitForTimeout(150);
  await pg.evaluate(() => { const e = document.querySelector('[data-mo-box]'); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 90) }); await pg.waitForTimeout(150);
  await pg.screenshot({ path: D + 'pdp-1280-montage-offer.png' });
  await m.goto('file://' + D + 'hero.html'); await m.evaluate(() => document.fonts.ready); await m.waitForTimeout(150);
  await m.screenshot({ path: D + 'hero-390.png', fullPage: true });

  eq('Keine JavaScript-Fehler', errs, []);
  console.log(`\n${pass} bestanden, ${fail} fehlgeschlagen`);
  await b.close(); process.exit(fail ? 1 : 0);
})().catch(e => { console.error('ABBRUCH:', e.message); process.exit(2); });
