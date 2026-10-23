// Produktkarten + Icon-Leiste: Preis einzeilig? Sterne/Preis auf gleicher Höhe? Icon-Elemente in einer Reihe?
const { chromium } = require('playwright');
const D = '/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad/design-review/v3/';
let pass = 0, fail = 0; const eq = (n, g, w) => { const ok = JSON.stringify(g) === JSON.stringify(w); ok ? pass++ : fail++; console.log(`${ok ? '✓' : '✗'} ${n}${ok ? '' : `  erwartet ${JSON.stringify(w)} erhalten ${JSON.stringify(g)}`}`); };
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  for (const w of [1280, 1100, 1000, 820, 390]) {
    await pg.setViewportSize({ width: w, height: 900 }); await pg.goto('file://' + D + 'cards.html'); await pg.evaluate(() => document.fonts.ready);
    const m = await pg.evaluate(() => {
      const r = e => e.getBoundingClientRect();
      const cards = [...document.querySelectorAll('.product-item')];
      const priceLines = cards.map(c => { const p = c.querySelector('.price--highlight'); const lh = parseFloat(getComputedStyle(p).lineHeight); return Math.round(r(p).height / lh); });
      const priceY = cards.map(c => Math.round(r(c.querySelector('.price--highlight')).top - r(c).top));
      const priceFs = cards.map(c => getComputedStyle(c.querySelector('.price--highlight')).fontSize);
      const starY = cards.filter(c => c.querySelector('.rating')).map(c => Math.round(r(c.querySelector('.rating')).top - r(c).top));
      const imgH = cards.map(c => Math.round(r(c.querySelector('.aspect-ratio')).height));
      const btnBottom = cards.map(c => Math.round(r(c).bottom - r(c.querySelector('.product-item__action-list')).bottom));
      const items = [...document.querySelectorAll('.text-with-icons__item')].map(e => Math.round(r(e).top));
      const rows = new Set(items).size;
      const flick = getComputedStyle(document.querySelector('.text-with-icons'), '::after').content;
      const clipped = [...document.querySelectorAll('.product-item__title, .product-item .rating, .product-item .price--highlight')].filter(e => e.scrollWidth > e.clientWidth + 1).map(e => e.className.split(' ')[0]);
      return { priceLines, priceY, priceFs, starY, imgH, btnBottom, rows, flick, clipped, cardsPerRow: new Set(cards.map(c => Math.round(r(c).top))).size };
    });
    console.log(`— ${w}px`, JSON.stringify(m));
    eq(`${w}: Preis einzeilig`, m.priceLines.every(x => x === 1), true);
    eq(`${w}: Preis in allen Karten auf gleicher Höhe`, new Set(m.priceY).size, 1);
    eq(`${w}: Sterne auf gleicher Höhe`, new Set(m.starY).size, 1);
    eq(`${w}: Bildboxen gleich hoch`, new Set(m.imgH).size, 1);
    eq(`${w}: Icon-Elemente in ${w >= 1000 ? 'einer Reihe' : 'zwei Reihen'}`, m.rows, w >= 1000 ? 1 : 2);
    eq(`${w}: kein Karussell`, m.flick !== '"flickity"', true);
    eq(`${w}: nichts abgeschnitten (Titel, Sterne, Preis)`, m.clipped, []);
    if (w === 1280) await pg.screenshot({ path: D + 'cards-1280.png', fullPage: true });
    if (w === 1100) await pg.screenshot({ path: D + 'cards-1100.png', fullPage: true });
    if (w === 390) await pg.screenshot({ path: D + 'cards-390.png', fullPage: true });
  }
  console.log(`\n${pass} bestanden, ${fail} fehlgeschlagen`); await b.close(); process.exit(fail ? 1 : 0);
})().catch(e => { console.error('ABBRUCH:', e.message); process.exit(2); });
