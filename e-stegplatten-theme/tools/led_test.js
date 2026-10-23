const { chromium } = require('playwright');
const fs = require('fs');
const base = process.argv[2];
const read = f => fs.readFileSync(`${base}/new/${f}`, 'utf8');
const scriptOf = s => s.match(/<script>([\s\S]*?)<\/script>/)[1];
const noLiquid = (js, name) => { const m = js.match(/\{\{[\s\S]*?\}\}|\{%[\s\S]*?%\}/); if (m) throw new Error(`${name}: ungelöstes Liquid ${m[0]}`); return js; };

const pjs = noLiquid(scriptOf(read('es-pdp-js.liquid'))
  .replace(/\{\{ sid \}\}/g, 'S').replace(/\{\{ p\.title \| json \}\}/g, '"Premium Dach"')
  .replace(/\{\{ frame \| json \}\}/g, '"Anthrazit"').replace(/\{\{ cover \| json \}\}/g, '"Klar"')
  .replace(/\{\{ cw \| json \}\}/g, '"5,00 Meter"').replace(/\{\{ cd \| json \}\}/g, '"3,00 Meter"'), 'pdp');
const hjs = noLiquid(scriptOf(read('es-hero-konfig.liquid'))
  .replace(/\{\{ dw \| json \}\}/g, '"5,00 Meter"').replace(/\{\{ dd \| json \}\}/g, '"3,00 Meter"'), 'hero');

const mock = `<script>window.__calls=[];window.theme={cartType:'drawer'};window.fetch=(u,o)=>{__calls.push({u,body:JSON.parse(o.body)});return Promise.resolve({ok:true,json:()=>Promise.resolve({})})}</script>`;
const pdpHtml = `<!doctype html><meta charset=utf-8>${mock}<div id="es-pdp-S">
<script type="application/json" data-v-json>[["5,00 Meter","3,00 Meter",111,150000,0,true,"TD-5-3"],["6,00 Meter","3,00 Meter",112,170000,0,true,"TD-6-3"]]</script>
<script type="application/json" data-sib-json>[]</script>
<span data-price></span><span data-sqm></span><span data-sku-wrap><span data-sku></span></span>
<div data-opts><button data-w="5,00 Meter">5</button><button data-w="6,00 Meter">6</button><button data-d="3,00 Meter">3</button></div>
<svg data-plan></svg><span data-plan-l></span><p data-stock><b></b></p>
<input type="radio" name="es-led-S" value="" data-led="0" checked>
<input type="radio" name="es-led-S" value="901" data-addon data-led="6" data-cents="20000">
<input type="radio" name="es-led-S" value="902" data-addon data-led="12" data-cents="35000">
<input type="radio" name="es-led-S" value="903" data-addon data-led="18" data-cents="50000">
<input type="checkbox" data-addon value="801" data-cents="2990">
<p data-tot hidden>Gesamt: <b data-tot-v></b></p>
<form data-form><input type="hidden" data-id><button type="button" data-qd="-1">-</button><input data-qty value="1"><button type="button" data-qd="1">+</button><button type="submit" data-atc>In den Warenkorb</button></form>
<p data-msg hidden></p><div data-sticky><b data-sticky-price></b><button data-sticky-go></button></div>
<script>${pjs}</script></div>`;
const heroHtml = `<!doctype html><meta charset=utf-8><div data-ehk>
<button data-f="Anthrazit">A</button><button data-c="Klar">K</button>
<button data-w="5,00 Meter">5</button><button data-w="6,00 Meter">6</button><button data-d="3,00 Meter">3</button>
<span data-klp></span><button data-led="0" data-lc="0">Ohne</button><button data-led="6" data-lc="20000">6er</button><button data-led="12" data-lc="35000">12er</button>
<div data-kp></div><span data-ks></span><a data-kgo href="#">Weiter mit <span data-kl></span></a>
<script type="application/json" data-k-json>[{"f":"Anthrazit","c":"Klar","u":"/products/dach-klar","v":{"5,00 Meter|3,00 Meter":[111,150000,true],"6,00 Meter|3,00 Meter":[112,170000,true]}}]</script>
</div><script>${hjs}</script>`;

let pass = 0, fail = 0;
const eq = (name, got, want) => { const ok = JSON.stringify(got) === JSON.stringify(want); ok ? pass++ : fail++; console.log(`${ok ? '✓' : '✗'} ${name}${ok ? '' : `\n    erwartet: ${JSON.stringify(want)}\n    erhalten: ${JSON.stringify(got)}`}`); };

(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  const txt = s => pg.textContent(s);
  fs.writeFileSync('/tmp/es_pdp.html', pdpHtml); fs.writeFileSync('/tmp/es_hero.html', heroHtml);

  console.log('— Produktseite —');
  await pg.goto('file:///tmp/es_pdp.html');
  eq('Start: Gesamtzeile versteckt', await pg.isHidden('[data-tot]'), true);
  eq('Start: Sticky-Preis = Dachpreis', await txt('[data-sticky-price]'), '1.500,00 €');
  await pg.check('input[data-led="12"]');
  eq('LED 12er: Gesamt sichtbar', await pg.isVisible('[data-tot]'), true);
  eq('LED 12er: Gesamt 1.500 + 350', await txt('[data-tot-v]'), '1.850,00 €');
  eq('LED 12er: Sticky zeigt Gesamt', await txt('[data-sticky-price]'), '1.850,00 €');
  await pg.check('input[type=checkbox][data-addon]');
  eq('+ Zubehör 29,90', await txt('[data-tot-v]'), '1.879,90 €');
  await pg.click('[data-qd="1"]');
  eq('Menge 2: Dach×2 + LED×2 + Zubehör×1', await txt('[data-tot-v]'), '3.729,90 €');
  await pg.click('[data-atc]'); await pg.waitForTimeout(150);
  eq('Warenkorb-Aufruf an /cart/add.js', (await pg.evaluate(() => __calls[0] && __calls[0].u)), '/cart/add.js');
  eq('Warenkorb-Inhalt (Dach, LED mit Zuordnung, Zubehör)', await pg.evaluate(() => __calls[0].body.items), [
    { id: 111, quantity: 2 },
    { id: 902, quantity: 2, properties: { 'Für Überdachung': 'Premium Dach – 5 × 3 m' } },
    { id: 801, quantity: 1 }]);
  await pg.click('[data-w="6,00 Meter"]');
  eq('Breite 6 m: Gesamt aktualisiert', await txt('[data-tot-v]'), '4.129,90 €');
  await pg.check('input[data-led="0"]'); await pg.uncheck('input[type=checkbox][data-addon]');
  eq('Ohne LED + ohne Zubehör: Gesamt versteckt', await pg.isHidden('[data-tot]'), true);
  await pg.click('[data-atc]'); await pg.waitForTimeout(2300); await pg.click('[data-atc]'); await pg.waitForTimeout(150);
  eq('Ohne LED: nur Dach im Warenkorb', await pg.evaluate(() => __calls[__calls.length - 1].body.items), [{ id: 112, quantity: 2 }]);
  await pg.goto('file:///tmp/es_pdp.html?led=6');
  eq('?led=6 aus Hero: 6er vorausgewählt', await pg.isChecked('input[data-led="6"]'), true);
  eq('?led=6: Gesamt 1.500 + 200', await txt('[data-tot-v]'), '1.700,00 €');

  console.log('— Startseiten-Hero —');
  await pg.goto('file:///tmp/es_hero.html');
  eq('Start: Preis', await txt('[data-kp]'), '1.500,00 €');
  eq('Start: Link ohne LED', await pg.getAttribute('[data-kgo]', 'href'), '/products/dach-klar?variant=111');
  eq('Start: LED-Hinweis', await txt('[data-klp]'), 'vormontiert, optional');
  await pg.click('[data-led="12"]');
  eq('12er: Preis inkl. LED', await txt('[data-kp]'), '1.850,00 €');
  eq('12er: Link übergibt led=12', await pg.getAttribute('[data-kgo]', 'href'), '/products/dach-klar?variant=111&led=12');
  eq('12er: Hinweis Aufpreis', await txt('[data-klp]'), '+ 350,00 € · vormontiert');
  eq('12er: Pill aktiv', await pg.getAttribute('[data-led="12"]', 'class'), 'is-on');
  await pg.click('[data-w="6,00 Meter"]');
  eq('Breite 6 m + 12er', await txt('[data-kp]'), '2.050,00 €');
  eq('Link Variante 112 + led', await pg.getAttribute('[data-kgo]', 'href'), '/products/dach-klar?variant=112&led=12');
  await pg.click('[data-led="0"]');
  eq('Ohne: Preis zurück', await txt('[data-kp]'), '1.700,00 €');
  eq('Ohne: Link ohne led', await pg.getAttribute('[data-kgo]', 'href'), '/products/dach-klar?variant=112');

  eq('Keine JavaScript-Fehler', errs, []);
  console.log(`\n${pass} bestanden, ${fail} fehlgeschlagen`);
  await b.close(); process.exit(fail ? 1 : 0);
})().catch(e => { console.error('ABBRUCH:', e.message); process.exit(2); });
