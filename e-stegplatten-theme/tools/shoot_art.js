const { chromium } = require('playwright');
const D = '/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad/design-review/cat/';
(async () => {
  const b = await chromium.launch();
  const m = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage();
  await m.goto('file://' + D + 'article.html'); await m.evaluate(() => document.fonts.ready); await m.waitForTimeout(300);
  console.log(JSON.stringify(await m.evaluate(() => ({ hscroll: document.documentElement.scrollWidth > innerWidth, tables: [...document.querySelectorAll('.rte table')].map(t => t.scrollWidth > t.clientWidth) }))));
  await m.evaluate(() => { const e = document.querySelector('.es-af'); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 20) }); await m.waitForTimeout(200);
  await m.screenshot({ path: D + 'article-390-faq.png' });
  await m.evaluate(() => { const e = document.querySelector('.rte table'); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 120) }); await m.waitForTimeout(200);
  await m.screenshot({ path: D + 'article-390-table.png' });
  await b.close();
})();
