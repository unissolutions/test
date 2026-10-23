// Startseite v3: Hero beginnt mit dem Bild, Überschriften möglichst einzeilig. Screenshots + Messungen.
const { chromium } = require('playwright');
const D = '/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad/design-review/v3/';
let pass = 0, fail = 0;
const eq = (n, g, w) => { const ok = JSON.stringify(g) === JSON.stringify(w); ok ? pass++ : fail++; console.log(`${ok ? '✓' : '✗'} ${n}${ok ? '' : `\n    erwartet ${JSON.stringify(w)}\n    erhalten ${JSON.stringify(g)}`}`); };
const SEL = { 'Kachel-Titel': '.esl .cat h3', 'Kachel-Link': '.esl .cat .l', 'Trust-Titel': '.esl .trust b', 'Finder-Option': '.esl .fin__opt b, .esl .fin__opt strong', 'H2': '.esl h2', 'Tab': '.esl .ehx__tab span', 'Beleg': '.esl .proof b', 'Kicker': '.esl .hv__tx .k' };
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
    const img = document.querySelector('.hv__img');
    return { hv: r('.hv'), hc: r('.hc'), proof: r('.proof'), h1: r('.hv h1'), imgLoaded: !!(img && img.naturalWidth), h1Color: getComputedStyle(document.querySelector('.hv h1')).color, firstInHero: document.querySelector('.hero .c').firstElementChild.className };
  });
  eq('Desktop: erstes Element im Hero ist der Bildblock', geo.firstInHero, 'hv');
  eq('Desktop: Bild geladen', geo.imgLoaded, true);
  eq('Desktop: Konfigurator rechts neben dem Bild', geo.hc.x > geo.hv.x + geo.hv.w - 1, true);
  eq('Desktop: Bild oben links, Belege darunter', geo.proof.y >= geo.hv.y + geo.hv.h - 1, true);
  eq('Desktop: Bildhöhe ≥ 420 px', geo.hv.h >= 420, true);
  eq('Desktop: Überschrift liegt im Bild', geo.h1.y > geo.hv.y && geo.h1.y + geo.h1.h <= geo.hv.y + geo.hv.h, true);
  eq('Desktop: Überschrift weiß', geo.h1Color, 'rgb(255, 255, 255)');
  await pg.screenshot({ path: D + 'home-1280-fold.png' });
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
    if (w === 507) { await pg.evaluate(() => { const e = document.querySelector('.cats'); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 90) }); await pg.waitForTimeout(100); await pg.screenshot({ path: D + 'home-507-cats.png' }); }
    if (w === 390) {
      const m = await pg.evaluate(() => { const hv = document.querySelector('.hv').getBoundingClientRect(), hc = document.querySelector('.hc').getBoundingClientRect(), pr = document.querySelector('.proof').getBoundingClientRect(); return { hvY: Math.round(hv.y), hvH: Math.round(hv.height), hvW: Math.round(hv.width), order: hv.y < hc.y && hc.y < pr.y, lead: !!document.querySelector('.hv .lead').offsetParent, kicker: !!document.querySelector('.hv .k').offsetParent } });
      eq('Mobil: Reihenfolge Bild → Konfigurator → Belege', m.order, true);
      eq('Mobil: Bild randlos (390 px breit)', m.hvW, 390);
      eq('Mobil: Lead-Text ausgeblendet, Kicker sichtbar', [m.lead, m.kicker], [false, true]);
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
