// Startseite v3: vollflächiger Hero (Foto, Text links, Konfigurator-Karte rechts, Maßlinien), Überschriften möglichst einzeilig. Screenshots + Messungen.
const { chromium } = require('playwright');
const D = '/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad/design-review/v3/';
let pass = 0, fail = 0;
const eq = (n, g, w) => { const ok = JSON.stringify(g) === JSON.stringify(w); ok ? pass++ : fail++; console.log(`${ok ? '✓' : '✗'} ${n}${ok ? '' : `\n    erwartet ${JSON.stringify(w)}\n    erhalten ${JSON.stringify(g)}`}`); };
const SEL = { 'Kachel-Titel': '.esl .cat h3', 'Kachel-Link': '.esl .cat .l', 'Trust-Titel': '.esl .trust b', 'Finder-Option': '.esl .fin__opt b, .esl .fin__opt strong', 'H2': '.esl h2', 'Tab': '.esl .ehx__tab span', 'Beleg': '.esl .proof b', 'Kicker': '.esl .ht .k', 'Hero-Link': '.esl .ht__link' };
const wraps = (pg) => pg.evaluate((SEL) => {
  const out = {};
  for (const [name, sel] of Object.entries(SEL)) {
    const bad = [];
    document.querySelectorAll(sel).forEach(el => {
      if (!el.offsetParent) return;
      const cs = getComputedStyle(el), lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.25;
      const lines = Math.round(el.getBoundingClientRect().height / lh);
      const over = el.scrollWidth > el.clientWidth + 1;
      if (lines > 1 || over) bad.push(`${el.textContent.trim().slice(0, 28)} (${lines}z${over ? ', abgeschnitten' : ''}, ${Math.round(parseFloat(cs.fontSize))}px)`);
    });
    if (bad.length) out[name] = bad;
  }
  return out;
}, SEL);
(async () => {
  const b = await chromium.launch();
  const errs = [];
  const pg = await b.newPage(); pg.on('pageerror', e => errs.push(e.message));
  await pg.setViewportSize({ width: 1280, height: 900 });
  await pg.goto('file://' + D + 'home.html'); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(200);
  const geo = await pg.evaluate(() => {
    const r = s => { const e = document.querySelector(s); const b = e.getBoundingClientRect(); return { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height) } };
    const img = document.querySelector('.hb__img');
    return { hero: r('.esl .hero'), hb: r('.hb'), ht: r('.ht'), hc: r('.hc'), proof: r('.proof'), imgLoaded: !!(img && img.naturalWidth), h1Color: getComputedStyle(document.querySelector('.ht h1')).color, cardBg: getComputedStyle(document.querySelector('.hcard')).backgroundColor, dimW: document.querySelector('[data-ehb-w]').textContent, dimD: document.querySelector('[data-ehb-d]').textContent, dims: getComputedStyle(document.querySelector('.hdim')).display };
  });
  eq('Desktop: Foto füllt den gesamten Hero', geo.hb.w === geo.hero.w && Math.abs(geo.hb.h - geo.hero.h) <= 2, true);
  eq('Desktop: Bild geladen', geo.imgLoaded, true);
  eq('Desktop: Text links, Karte rechts', geo.ht.x + geo.ht.w <= geo.hc.x, true);
  eq('Desktop: Belege unter dem Text, links der Karte', geo.proof.y >= geo.ht.y + geo.ht.h - 1 && geo.proof.x + geo.proof.w <= geo.hc.x, true);
  eq('Desktop: Hero ≥ 600 px hoch', geo.hero.h >= 600, true);
  eq('Desktop: Überschrift weiß, Karte weiß', [geo.h1Color, geo.cardBg], ['rgb(255, 255, 255)', 'rgb(255, 255, 255)']);
  eq('Desktop: Maßlinien sichtbar, zeigen die Vorauswahl', [geo.dims !== 'none', geo.dimW, geo.dimD], [true, 'Breite 5,00 m', 'Tiefe 3,00 m']);
  await pg.screenshot({ path: D + 'home-1280-fold.png' });
  await pg.click('[data-w="4,00 Meter"]'); await pg.waitForTimeout(120);
  eq('Desktop: Maßlinie folgt der Auswahl (4 m)', await pg.textContent('[data-ehb-w]'), 'Breite 4,00 m');
  await pg.click('[data-w="5,00 Meter"]');
  await pg.click('#ehx-t2-x'); await pg.waitForTimeout(150);
  eq('Desktop: Tabwechsel funktioniert', await pg.isVisible('.fin'), true);
  await pg.screenshot({ path: D + 'home-1280-finder.png' });
  await pg.click('#ehx-t1-x');
  for (const w of [1280, 1100, 1024, 1001, 1000, 820, 749, 507, 414, 390, 375, 360, 320]) {
    await pg.setViewportSize({ width: w, height: 900 }); await pg.waitForTimeout(120);
    const konfig = await wraps(pg);
    await pg.click('#ehx-t2-x'); await pg.waitForTimeout(80);
    const finder = await wraps(pg);
    await pg.click('#ehx-t1-x');
    const merged = { ...konfig }; for (const k of Object.keys(finder)) merged[k] = finder[k];
    const hs = await pg.evaluate(() => document.documentElement.scrollWidth <= innerWidth);
    console.log(`— ${w}px — ${hs ? '' : 'HORIZONTALES SCROLLEN! '}${Object.keys(merged).length ? JSON.stringify(merged) : 'alle Überschriften einzeilig'}`);
    if (w === 820) { await pg.evaluate(() => window.scrollTo(0, 0)); await pg.screenshot({ path: D + 'home-820-fold.png' }); }
    if (w === 507) { await pg.evaluate(() => { const e = document.querySelector('.cats'); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 90) }); await pg.waitForTimeout(100); await pg.screenshot({ path: D + 'home-507-cats.png' }); }
    if (w === 390) {
      const m = await pg.evaluate(() => { const R = s => document.querySelector(s).getBoundingClientRect(); const hb = R('.hb'), ht = R('.ht'), hc = R('.hc'), pr = R('.proof'); return { hbW: Math.round(hb.width), overlay: ht.bottom <= hb.bottom + 1 && ht.top >= hb.top - 1, cardBelow: hc.top >= hb.bottom - 1, proofAfterCard: pr.top >= hc.bottom - 1, dims: getComputedStyle(document.querySelector('.hdim')).display, lead: !!document.querySelector('.ht .lead').offsetParent, kicker: !!document.querySelector('.ht .k').offsetParent, cardW: Math.round(R('.hcard').width) } });
      eq('Mobil: Text auf dem Bild, Karte darunter, Belege danach', [m.overlay, m.cardBelow, m.proofAfterCard], [true, true, true]);
      eq('Mobil: Bild und Karte randlos (390 px)', [m.hbW, m.cardW], [390, 390]);
      eq('Mobil: Maßlinien aus, Lead aus, Kicker an', [m.dims, m.lead, m.kicker], ['none', false, true]);
      await pg.evaluate(() => window.scrollTo(0, 0)); await pg.waitForTimeout(100);
      await pg.screenshot({ path: D + 'home-390-fold.png' });
      await pg.screenshot({ path: D + 'home-390-full.png', fullPage: true });
      await pg.evaluate(() => { const e = document.querySelector('.cats'); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 90) }); await pg.waitForTimeout(100); await pg.screenshot({ path: D + 'home-390-cats.png' });
    }
  }
  eq('Keine JavaScript-Fehler', errs, []);
  console.log(`\n${pass} bestanden, ${fail} fehlgeschlagen`);
  await b.close(); process.exit(fail ? 1 : 0);
})().catch(e => { console.error('ABBRUCH:', e.message); process.exit(2); });
