const { chromium } = require('playwright');
const D = '/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad/design-review/cat/';
(async () => {
  const b = await chromium.launch();
  const m = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage();
  await m.goto('file://' + D + '665487704401.html'); await m.evaluate(() => document.fonts.ready); await m.waitForTimeout(300);
  const r = await m.evaluate(() => { const t = document.querySelector('[data-cs-txt]'), bt = document.querySelector('[data-cs-more]'), tb = document.querySelector('.es-cs__txt table');
    return { clamp: t.classList.contains('is-clamp'), btn: !bt.hidden, hscroll: document.documentElement.scrollWidth > innerWidth, tableScroll: tb.scrollWidth > tb.clientWidth, docW: document.documentElement.scrollWidth } });
  console.log('mobile', JSON.stringify(r));
  await m.screenshot({ path: D + 'cat-390-full.png', fullPage: true });
  await m.click('[data-cs-more]'); await m.waitForTimeout(400);
  console.log('after click', await m.evaluate(() => [document.querySelector('[data-cs-txt]').classList.contains('is-clamp'), document.querySelector('[data-cs-more]').textContent]));
  const d = await (await b.newContext({ viewport: { width: 1280, height: 900 } })).newPage();
  await d.goto('file://' + D + '665487704401.html'); await d.evaluate(() => document.fonts.ready); await d.waitForTimeout(300);
  await d.screenshot({ path: D + 'cat-1280-full.png', fullPage: true });
  await b.close();
})();
