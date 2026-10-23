// Misst je Viewport die einzeilige Textbreite (nowrap) gegen den verfügbaren Platz für alle Überschriften-Elemente der Startseite.
const { chromium } = require('playwright');
const D = '/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad/design-review/v3/';
const SEL = { Kachel: '.esl .cat h3', KLink: '.esl .cat .l', Trust: '.esl .trust b', H2: '.esl h2', Tab: '.esl .ehx__tab span', Beleg: '.esl .proof b', BelegSub: '.esl .proof div', TrustSub: '.esl .trust span span' };
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('file://' + D + 'home.html'); await pg.evaluate(() => document.fonts.ready);
  for (const w of (process.argv[2] ? process.argv[2].split(',').map(Number) : [1280, 1100, 1024, 1001, 820, 749, 507, 414, 390, 375, 360, 320])) {
    await pg.setViewportSize({ width: w, height: 900 }); await pg.waitForTimeout(80);
    const rows = await pg.evaluate((SEL) => {
      const out = [];
      for (const [name, sel] of Object.entries(SEL)) document.querySelectorAll(sel).forEach(el => {
        if (!el.offsetParent) return;
        const cs = getComputedStyle(el); const avail = el.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
        const r = document.createRange(); r.selectNodeContents(el); const old = el.style.whiteSpace; el.style.whiteSpace = 'nowrap';
        const tw = Math.ceil(r.getBoundingClientRect().width); el.style.whiteSpace = old;
        out.push(`${name} ${Math.round(parseFloat(cs.fontSize))}px ${tw}/${Math.round(avail)}${tw > avail ? ' ✗' : ''} ${el.textContent.trim().slice(0, 30)}`);
      });
      return out;
    }, SEL);
    console.log(`— ${w}px\n  ` + rows.join('\n  '));
  }
  await b.close();
})();
