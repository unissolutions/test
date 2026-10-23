// Komplettset-Rechner: Mengen/Varianten folgen Breite + Plattenvariante; Layout ohne Überlauf in schmaler Spalte und mobil.
const { chromium } = require('playwright');
const D = '/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad/design-review/v3/';
let pass = 0, fail = 0; const eq = (n, g, w) => { const ok = JSON.stringify(g) === JSON.stringify(w); ok ? pass++ : fail++; console.log(`${ok ? '✓' : '✗'} ${n}${ok ? '' : `  erwartet ${JSON.stringify(w)} erhalten ${JSON.stringify(g)}`}`); };
const state = pg => pg.evaluate(() => { const R = document.querySelector('.es-sz'); const row = k => { const el = [...R.querySelectorAll('.es-sz__r')].find(r => JSON.parse(r.querySelector('[data-sz-v]').textContent).r === k); return el && !el.hidden ? { qty: +el.querySelector('[data-sz-q]').value, v: el.querySelector('[data-sz-u]').textContent.trim() } : null };
  return { calc: R.querySelector('[data-sz-calc]').textContent.replace(/\s+/g, ' ').trim(), qty: +document.getElementById('qty').value, l: R.querySelector('[data-sz-l]').textContent, mid: row('mid'), rand: row('rand'), u: row('u'), win: row('win'), tape: row('tape'), sh: row('sh'), so: row('so'), sw: row('sw'), sil: row('sil'), btn: R.querySelector('[data-sz-add]').textContent.trim() }; });
const layout = pg => pg.evaluate(() => { const R = document.querySelector('.es-sz'); const col = document.querySelector('.col'); const over = [...R.querySelectorAll('*')].filter(e => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflow !== 'hidden').map(e => (e.className || e.tagName) + '(' + e.scrollWidth + '>' + e.clientWidth + ' ' + e.textContent.trim().slice(0, 18) + ')').slice(0, 6); return { pageScroll: document.documentElement.scrollWidth <= innerWidth, fits: R.getBoundingClientRect().right <= col.getBoundingClientRect().right + 1, over, dimCols: getComputedStyle(R.querySelector('.es-sz__dim')).gridTemplateColumns.split(' ').length }; });
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.setViewportSize({ width: 1100, height: 1400 }); await pg.goto('file://' + D + 'sz.html'); await pg.waitForTimeout(600);
  let s = await state(pg); console.log('Start:', JSON.stringify(s));
  eq('3070 mm, Platte 2000×1200 → 3 Platten, Menge 3', [s.calc.includes('3 Platten à 2000 × 1200 mm'), s.qty], [true, 3]);
  eq('Mittelprofile n−1 = 2 (2000 mm), Randprofile 2, U-Profile 3 (1200 mm), Winkel 4', [s.mid.qty, s.mid.v, s.rand.qty, s.u.qty, s.u.v, s.win.qty], [2, '2000mm', 2, 3, '1200mm', 4]);
  const uk = () => pg.evaluate(() => [...document.querySelectorAll('.es-sz__r[data-uk]')].filter(r => r.dataset.uk).map(r => r.dataset.uk + ':' + (r.hidden ? 'aus' : 'an')));
  eq('Schrauben Holz sichtbar, Metall ausgeblendet', await uk(), ['holz:an', 'metall:aus']);
  // Variante wechseln: 3000 × 980
  await pg.evaluate(() => { const sel = document.getElementById('vsel'); sel.value = [...sel.options].find(o => o.textContent === '3000mm / 980mm').value; }); await pg.waitForTimeout(700);
  s = await state(pg); console.log('Nach Variante 3000×980:', JSON.stringify({ calc: s.calc, mid: s.mid, u: s.u, qty: s.qty }));
  eq('Variante 3000×980 → 3 Platten, Mittelprofil 3000 mm, U-Profil 980 mm', [s.calc.includes('3 Platten à 3000 × 980 mm'), s.mid.v, s.u.v, s.qty], [true, '3000mm', '980mm', 3]);
  // Breite ändern: 5080
  await pg.fill('[data-sz-b]', '5080'); await pg.waitForTimeout(600);
  s = await state(pg); console.log('Nach Breite 5080:', JSON.stringify({ calc: s.calc, mid: s.mid, u: s.u, win: s.win, qty: s.qty }));
  eq('Breite 5080 → 5 Platten, 4 Mittelprofile, 5 U-Profile, 6 Winkel, Menge 5', [s.calc.includes('5 Platten'), s.mid.qty, s.u.qty, s.win.qty, s.qty], [true, 4, 5, 6, 5]);
  // Unterkonstruktion Metall
  await pg.click('input[name="es-sz-uk"][value="metall"]'); await pg.waitForTimeout(300);
  eq('Metall → Holz-Schrauben aus, Metall-Schrauben an', await uk(), ['holz:aus', 'metall:an']);
  // Layout schmale Desktop-Spalte (400 px) und mobil (390 px)
  let l = await layout(pg); console.log('Layout 400px-Spalte:', JSON.stringify(l));
  eq('Desktop-Spalte 400 px: kein Überlauf', [l.fits, l.over], [true, []]);
  await pg.screenshot({ path: D + 'sz-400.png', fullPage: true });
  await pg.setViewportSize({ width: 390, height: 900 }); await pg.waitForTimeout(300); l = await layout(pg); console.log('Layout 390px:', JSON.stringify(l));
  eq('Mobil 390 px: kein Überlauf, kein horizontales Scrollen', [l.pageScroll, l.fits, l.over], [true, true, []]);
  await pg.screenshot({ path: D + 'sz-390.png', fullPage: true });
  await pg.setViewportSize({ width: 360, height: 900 }); await pg.waitForTimeout(300); l = await layout(pg);
  eq('Mobil 360 px: kein Überlauf', [l.pageScroll, l.over], [true, []]);
  eq('Keine JavaScript-Fehler', errs, []);
  console.log(`\n${pass} bestanden, ${fail} fehlgeschlagen`); await b.close(); process.exit(fail ? 1 : 0);
})().catch(e => { console.error('ABBRUCH:', e.message); process.exit(2); });
