#!/usr/bin/env python3
"""v3: Montage zubuchbar, Angebot anfordern / Konfiguration teilen, Farbmuster-Links,
Trust-Texte, Judge.me-Gesamtbewertung im Hero. Patcht theme/v3/new/* ausgehend von theme/v3/orig/*."""
import json, pathlib, re, shutil

B = pathlib.Path('/tmp/claude-0/-home-user-test/beef7815-2c55-57f0-9ec2-48630e491a1b/scratchpad/theme/v3')
FILES = ['sections/es-pdp-terrasse.liquid', 'sections/es-landing.liquid', 'snippets/es-pdp-js.liquid',
         'snippets/es-pdp-css.liquid', 'snippets/es-hero-konfig.liquid', 'snippets/es-led-guard.liquid', 'snippets/es-landing-css.liquid', 'templates/index.json']
for f in FILES:
    shutil.copy(B / 'orig' / f, B / 'new' / f)


def patch(path, pairs):
    p = B / 'new' / path
    s = p.read_text(encoding='utf-8')
    for old, new in pairs:
        assert s.count(old) == 1, f'{path}: Fundstelle nicht eindeutig ({s.count(old)}x): {old[:70]!r}'
        s = s.replace(old, new)
    p.write_text(s, encoding='utf-8')


# ---------------------------------------------------------------- Produktseite (Liquid)
patch('sections/es-pdp-terrasse.liquid', [
    # Kopfkommentar
    ('Beleuchtung, Zubehör, Warenkorb, Draufsicht, Sticky-Bar bis 999 px.',
     'Beleuchtung, Montage (PLZ-Prüfung, Preis aus Montage-Produkt), Zubehör, Warenkorb, Angebot anfordern (Shopify-Kontaktformular) + Konfiguration teilen, Draufsicht, Sticky-Bar bis 999 px.'),
    # Montage-Produkt + Optionsindizes
    ("""    assign led = all_products['led-spots-terrassenueberdachung']
  endif
-%}""",
     """    assign led = all_products['led-spots-terrassenueberdachung']
  endif
  assign mo = section.settings.montage_steg
  if fam == 'vsg'
    assign mo = section.settings.montage_vsg
  endif
  unless mo.id
    if fam == 'vsg'
      assign mo = all_products['montage-terrassendach-vsg-glas']
    else
      assign mo = all_products['montage-terrassendach-stegplatten']
    endif
  endunless
  assign mwi = 0
  assign mdi = 1
  assign mli = 2
  for o in mo.options_with_values
    if o.name == 'Breite'
      assign mwi = forloop.index0
    elsif o.name == 'Tiefe' or o.name == 'Länge'
      assign mdi = forloop.index0
    elsif o.name == 'Zone'
      assign mli = forloop.index0
    endif
  endfor
  assign mo_on = false
  if section.settings.montage_on and mo.id != blank and mo.available
    assign mo_on = true
  endif
-%}"""),
    # Farbmuster-Link bei Dachplatte
    ("""{%- when 'Graphit' -%}getönt, schattig{%- else -%}maximal hell{%- endcase -%}</span></div>""",
     """{%- when 'Graphit' -%}getönt, schattig{%- else -%}maximal hell{%- endcase -%}{%- if section.settings.muster_url != blank -%} · <a class="es-pdp__ml" href="{{ section.settings.muster_url }}">Farbmuster</a>{%- endif -%}</span></div>"""),
    # Montage-Block nach LED
    ("""{%- endif -%}
{%- capture addons -%}""",
     """{%- endif -%}
{%- if mo_on -%}{%- capture mosvg -%}<svg width="36" height="36" viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 21.5 8 28a2.1 2.1 0 0 1-3-3l6.5-6.5"/><path d="M19 9a6 6 0 0 1 8 7l-5.5 5.5a6 6 0 0 1-8-8z"/><path d="m17 13 6 6"/></svg>{%- endcapture -%}
<div class="es-pdp__add es-pdp__mo" data-mo-box><div class="es-pdp__add-h">Montage</div>
<label class="es-pdp__ar es-pdp__lr"><input type="radio" name="es-mo-{{ section.id }}" value="" data-mo="0" checked><span class="es-pdp__li es-pdp__li--off" aria-hidden="true">{{ mosvg }}</span><span>Selbstmontage<small>{{ section.settings.montage_self | default: 'Anleitung liegt bei, Telefon-Support bei der Montage' }}</small></span><b>+ 0,00 €</b></label>
<label class="es-pdp__ar es-pdp__lr"><input type="radio" name="es-mo-{{ section.id }}" value="" data-mo="1" data-addon data-per="1" data-cents="0"><span class="es-pdp__li" aria-hidden="true">{{ mosvg }}</span><span>Montage durch unser Team<small>{{ section.settings.montage_sub | default: 'Preis nach Entfernung, Deutschland und Österreich' }}</small></span><b data-mo-price>Preis nach PLZ</b></label>
<div class="es-pdp__mop" data-mo-panel hidden><label for="es-mo-plz-{{ section.id }}">Postleitzahl des Montageorts</label><div class="es-pdp__mor"><input type="text" id="es-mo-plz-{{ section.id }}" inputmode="numeric" autocomplete="postal-code" placeholder="z. B. 45881" data-mo-plz><span data-mo-land></span></div><p class="es-pdp__moh" data-mo-hint></p></div>
<p class="es-pdp__lnote">{{ section.settings.montage_note | default: 'Montage nur zusammen mit dem Dach buchbar. Den Termin stimmen wir nach der Bestellung mit Ihnen ab.' }}</p></div>
{%- endif -%}
{%- capture addons -%}"""),
    # Angebot + Teilen unter der Kaufzeile
    ("""<p class="es-pdp__msg" data-msg hidden></p>
<div class="es-pdp__trust">""",
     """<p class="es-pdp__msg" data-msg hidden></p>
{%- capture ic_doc -%}<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>{%- endcapture -%}
{%- capture ic_share -%}<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg>{%- endcapture -%}
<div class="es-pdp__sec"><button type="button" class="es-pdp__sb" data-offer-tg aria-expanded="false" aria-controls="es-offer-{{ section.id }}">{{ ic_doc }}Angebot anfordern</button><button type="button" class="es-pdp__sb" data-share-tg aria-expanded="false" aria-controls="es-share-{{ section.id }}">{{ ic_share }}Konfiguration teilen</button></div>
<div class="es-pdp__panel" id="es-share-{{ section.id }}" data-share hidden>
<div class="es-pdp__add-h">Konfiguration speichern oder teilen</div>
<div class="es-pdp__pb">
<p class="es-pdp__psum" data-share-sum></p>
<div class="es-pdp__pr2"><input type="text" readonly aria-label="Link zur Konfiguration" data-share-url><button type="button" data-share-copy>Link kopieren</button></div>
<div class="es-pdp__pl"><a data-share-wa href="#" target="_blank" rel="noopener">Per WhatsApp senden</a><a data-share-mail href="#">Per E-Mail senden</a><button type="button" data-share-print>Drucken / als PDF sichern</button></div>
<p class="es-pdp__phint">Der Link öffnet diese Seite mit Ihrer Auswahl – zum Vergleichen, Abstimmen oder für später.</p>
</div></div>
<div class="es-pdp__panel" id="es-offer-{{ section.id }}" data-offer hidden>
<div class="es-pdp__add-h">Persönliches Angebot anfordern</div>
<div class="es-pdp__pb">
{%- form 'contact', id: 'es-offer-form', class: 'es-pdp__of' -%}
{%- if form.posted_successfully? -%}<p class="es-pdp__ok" role="status">Vielen Dank! Ihre Anfrage ist bei uns eingegangen. Wir melden uns in der Regel am selben Werktag (Mo–Fr 8–17 Uhr).</p>{%- endif -%}
{%- if form.errors -%}<p class="es-pdp__msg is-err" role="alert">Bitte prüfen Sie Ihre Angaben: {{ form.errors | default_errors }}</p>{%- endif -%}
<input type="hidden" name="contact[Anfrage]" value="Angebot Terrassendach">
<input type="hidden" name="contact[Konfiguration]" value="" data-offer-cfg>
<div class="es-pdp__fr"><label>Name<input type="text" name="contact[name]" autocomplete="name" required></label><label>E-Mail<input type="email" name="contact[email]" autocomplete="email" required></label></div>
<div class="es-pdp__fr"><label>Telefon (für Rückfragen)<input type="tel" name="contact[phone]" autocomplete="tel"></label><label>PLZ Montage- oder Lieferort<input type="text" name="contact[PLZ]" inputmode="numeric" maxlength="5" data-offer-plz></label></div>
<label>Ihre Nachricht<textarea name="contact[body]" rows="7" data-offer-body></textarea></label>
<p class="es-pdp__phint">Ihre Konfiguration (Maß, Farbe, Zubehör, Montage) fügen wir automatisch bei. {{ section.settings.offer_hint }}</p>
<button type="submit" class="es-pdp__atc es-pdp__atc--sec">Angebot anfordern</button>
{%- endform -%}
</div></div>
<div class="es-pdp__trust">"""),
    # Parameter an das JS-Snippet
    ("cover: cover, cw: cw, cd: cd %}",
     "cover: cover, cw: cw, cd: cd, mo: mo, mo_on: mo_on, mwi: mwi, mdi: mdi, mli: mli, marea: section.settings.montage_zonen %}"),
    # Schema
    ("""{"type":"text","id":"led_note","label":"Hinweis unter der LED-Auswahl","default":"Unsere vormontierten LED-Spots werden optimal auf die Anzahl der Träger abgestimmt."}
],""",
     """{"type":"text","id":"led_note","label":"Hinweis unter der LED-Auswahl","default":"Unsere vormontierten LED-Spots werden optimal auf die Anzahl der Träger abgestimmt."},
{"type":"header","content":"Farbmuster"},
{"type":"url","id":"muster_url","label":"Link Farbmuster-Produkt","info":"Leer = kein Link bei „Dachplatte“.","default":"/products/farbmuster"},
{"type":"header","content":"Montage"},
{"type":"checkbox","id":"montage_on","label":"Montage anbieten","default":true},
{"type":"product","id":"montage_steg","label":"Montage-Produkt für Stegplatten-Dächer","info":"Leer = Handle montage-terrassendach-stegplatten. Varianten: Breite × Tiefe × Zone (Werte wie beim Dach, Zonennamen wie unten)."},
{"type":"product","id":"montage_vsg","label":"Montage-Produkt für VSG-Glas-Dächer","info":"Leer = Handle montage-terrassendach-vsg-glas."},
{"type":"textarea","id":"montage_zonen","label":"Montagezonen","info":"Eine Zone je Zeile: Name|PLZ-Präfixe|Beschreibung. Präfixe 2-stellig, kommagetrennt, Bereiche mit Bindestrich; AT = Österreich (4-stellige PLZ). Reihenfolge = Prüfreihenfolge (erster Treffer gilt). Der Name muss dem Optionswert „Zone“ im Montage-Produkt entsprechen; Zeile löschen = Zone nur auf Anfrage.","default":"Zone 1|32,40-53,57-59|bis 170 km\\nZone 2|26-31,33-35,37-38,54-56,60-62,65|170–270 km\\nZone 3|20-21,36,39,63-69,97-99|270–370 km\\nZone 4|01-19,22-25,70-96|370–770 km\\nÖsterreich|AT|ganz Österreich"},
{"type":"text","id":"montage_sub","label":"Zusatz unter „Montage durch unser Team“","default":"Preis nach Entfernung, Deutschland und Österreich"},
{"type":"text","id":"montage_self","label":"Zusatz unter „Selbstmontage“","default":"Anleitung liegt bei, Telefon-Support bei der Montage"},
{"type":"text","id":"montage_note","label":"Hinweis unter der Montage-Auswahl","default":"Montage nur zusammen mit dem Dach buchbar. Den Termin stimmen wir nach der Bestellung mit Ihnen ab."},
{"type":"header","content":"Angebot anfordern"},
{"type":"text","id":"offer_hint","label":"Hinweis im Angebotsformular","default":"Keine Werbung, keine Weitergabe – nur unser Angebot."}
],"""),
])

# ---------------------------------------------------------------- Produktseite (JS)
patch('snippets/es-pdp-js.liquid', [
    ('(Sticky-Bar erst, wenn der Preis aus dem Bild ist und der Warenkorb-Button nicht sichtbar ist)',
     '(Sticky-Bar erst, wenn der Preis aus dem Bild ist und der Warenkorb-Button nicht sichtbar ist; Montage mit PLZ-Prüfung; Angebot/Teilen-Panels)'),
    # Montage-Varianten als JSON
    ("""{%- endfor -%}]</script>
<script>(function(){""",
     """{%- endfor -%}]</script>
{%- if mo_on -%}<script type="application/json" data-mo-json>{"zones":{{ marea | default: '' | json }},"v":{ {%- for mv in mo.variants -%}{{ mv.options[mwi] | append: '|' | append: mv.options[mdi] | append: '|' | append: mv.options[mli] | json }}:[{{ mv.id }},{{ mv.price }},{{ mv.available }}]{%- unless forloop.last -%},{%- endunless -%}{%- endfor -%} }}</script>{%- endif -%}
<script>(function(){"""),
    # Summe: Montage zählt je Dach; danach Panels aktualisieren
    ("ex+=(+c.dataset.cents||0)*(c.dataset.led?qty:1)});var t=q('[data-tot]');if(t){t.hidden=!ex;if(ex)q('[data-tot-v]').textContent=eur(s+ex)}if(spr)spr.textContent=eur(s+ex)}",
     "ex+=(+c.dataset.cents||0)*((c.dataset.led||c.dataset.per)?qty:1)});var t=q('[data-tot]');if(t){t.hidden=!ex;if(ex)q('[data-tot-v]').textContent=eur(s+ex)}if(spr)spr.textContent=eur(s+ex);fill()}"),
    # Maßwechsel: Montagepreis neu bestimmen
    ("btn.disabled=!x[5];btn.textContent=x[5]?'In den Warenkorb':'Nicht verfügbar';tot();",
     "btn.disabled=!x[5];btn.textContent=x[5]?'In den Warenkorb':'Nicht verfügbar';moUpd();tot();"),
    # Warenkorb: Montage als eigene Zeile mit Zuordnung, Sperre ohne gültige PLZ
    ("""form.addEventListener('submit',function(e){e.preventDefault();var x=cur();if(!x||!x[5])return;var qty=Math.max(1,parseInt(qi.value,10)||1),items=[{id:x[2],quantity:qty}];
qa('[data-addon]').forEach(function(c){if(!c.checked)return;var it={id:+c.value,quantity:c.dataset.led?qty:1};if(c.dataset.led)it.properties={'Für Überdachung':TT+' – '+sm(n(st.w))+' × '+sm(n(st.d))+' m'};items.push(it)});""",
     """form.addEventListener('submit',function(e){e.preventDefault();var x=cur();if(!x||!x[5])return;var qty=Math.max(1,parseInt(qi.value,10)||1),items=[{id:x[2],quantity:qty}];
if(moR&&moR.checked&&!moR.dataset.ok){msg.className='es-pdp__msg is-err';msg.textContent=!moSt.plz?'Bitte die Postleitzahl des Montageorts eingeben.':moSt.z==='out'?'Montage für diese PLZ nur per Angebot. Bitte „Selbstmontage“ wählen oder ein Angebot anfordern.':'Für dieses Maß und diese PLZ können wir die Montage nicht direkt buchen. Bitte ein Angebot anfordern.';msg.hidden=false;if(moP)moP.focus();return}
var ref=TT+' – '+sm(n(st.w))+' × '+sm(n(st.d))+' m';
qa('[data-addon]').forEach(function(c){if(!c.checked||!c.value)return;var it={id:+c.value,quantity:(c.dataset.led||c.dataset.per)?qty:1};if(c.dataset.led)it.properties={'Für Überdachung':ref};if(c.dataset.mo)it.properties={'Für Überdachung':ref,'Montageort':moOrt()};items.push(it)});"""),
    # Montage + Angebot/Teilen vor der Sticky-Bar
    ("""var sb=q('[data-sticky]'),go=q('[data-sticky-go]'),mode='pick',pb=q('.es-pdp__pr'),vB=false,vP=!!pb;""",
     """var MO=null;try{MO=JSON.parse(q('[data-mo-json]').textContent)}catch(e){}
var moR=q('[data-mo="1"]'),moP=q('[data-mo-plz]'),moH=q('[data-mo-hint]'),moPr=q('[data-mo-price]'),moPan=q('[data-mo-panel]'),moLd=q('[data-mo-land]'),moSt={z:null,plz:''},ZN=[];
if(MO)String(MO.zones||'').split(/\\r?\\n/).forEach(function(l){var f=l.split('|');if(f.length<2||!f[0].trim())return;var z={n:f[0].trim(),l:(f[2]||'').trim(),at:false,r:[]};f[1].split(',').forEach(function(s){s=s.trim();if(/^AT$/i.test(s)){z.at=true;return}var m=s.match(/^(\\d{2})(?:-(\\d{2}))?$/);if(m)z.r.push([+m[1],+(m[2]||m[1])])});ZN.push(z)});
function moZone(z){var i;if(/^\\d{4}$/.test(z)){for(i=0;i<ZN.length;i++)if(ZN[i].at)return ZN[i];return 'out'}if(/^\\d{5}$/.test(z)){var p=+z.slice(0,2);for(i=0;i<ZN.length;i++)if(ZN[i].r.some(function(r){return p>=r[0]&&p<=r[1]}))return ZN[i];return 'out'}return null}
function moOrt(){var z=moSt.z;return z&&z.at?'Österreich, PLZ '+moSt.plz:'PLZ '+moSt.plz+(z&&z!=='out'?', '+z.n:'')}
function moUpd(){if(!MO||!moR)return;var on=moR.checked;if(moPan)moPan.hidden=!on;moSt.plz=(moP.value||'').replace(/\\D/g,'').slice(0,5);if(moP.value!==moSt.plz)moP.value=moSt.plz;moSt.z=moZone(moSt.plz);var z=moSt.z,zl=z&&z!=='out'?(z.at?'Österreich':z.n+(z.l?' · '+z.l:'')):'';
var v=z&&z!=='out'?MO.v[st.w+'|'+st.d+'|'+z.n]:null,ok=!!(v&&v[2]);
moR.value=ok?v[0]:'';moR.dataset.cents=ok?v[1]:0;moR.dataset.ok=ok?'1':'';
if(moLd)moLd.textContent=zl;
var h;if(!moSt.plz)h='PLZ eingeben – wir prüfen sofort, ob Ihr Ort im Montagegebiet liegt.';else if(!z)h='Bitte eine gültige PLZ eingeben (Deutschland 5-stellig, Österreich 4-stellig).';else if(z==='out')h='Außerhalb unseres Montagegebiets. Fragen Sie gern ein Angebot an – wir prüfen, ob wir Ihren Ort anfahren können.';else if(!ok)h='Für dieses Maß nennen wir den Montagepreis im persönlichen Angebot.';else h='Montage in '+(z.at?'Österreich':'PLZ '+moSt.plz)+' ('+zl+'): '+eur(v[1])+' inkl. MwSt. – Termin nach Bestellung.';
if(moH){moH.textContent=h;moH.classList.toggle('is-err',on&&!!moSt.plz&&!ok)}
if(moPr)moPr.textContent=ok?'+ '+eur(v[1]):(z==='out'?'auf Anfrage':'Preis nach PLZ');
try{if(moSt.plz)localStorage.setItem('es-plz',moSt.plz)}catch(e){}}
if(moR){moR.dataset.mo='1';qa('[data-mo]').forEach(function(r){r.addEventListener('change',function(){moUpd();tot();if(moR.checked&&moP&&!moP.value)moP.focus()})});moP.addEventListener('input',function(){moUpd();tot()});
try{var SPm=new URLSearchParams(location.search),MP=SPm.get('mp')||localStorage.getItem('es-plz');if(MP)moP.value=MP;if(SPm.get('mp'))moR.checked=true}catch(e){}}
var shT=q('[data-share-tg]'),shP=q('[data-share]'),ofT=q('[data-offer-tg]'),ofP=q('[data-offer]');
function ledTxt(){var c=qa('[data-led]').filter(function(x){return x.checked})[0];return c&&c.dataset.led!=='0'?'LED-Spots '+c.dataset.led+'er-Set':'ohne LED'}
function moTxt(){if(!moR||!moR.checked)return 'Selbstmontage';return (moR.dataset.ok?'Montage durch e-Stegplatten':'Montage angefragt')+(moSt.plz?' ('+moOrt()+')':'')}
function shareUrl(){var x=cur(),u=new URL(location.pathname,location.href);if(x)u.searchParams.set('variant',x[2]);var c=qa('[data-led]').filter(function(y){return y.checked})[0];if(c&&c.dataset.led!=='0')u.searchParams.set('led',c.dataset.led);if(moR&&moR.checked&&moSt.plz)u.searchParams.set('mp',moSt.plz);return u.toString()}
function cfgText(){var x=cur(),qty=Math.max(1,parseInt(qi.value,10)||1),ex=0;qa('[data-addon]').forEach(function(c){if(c.checked&&c.value)ex+=(+c.dataset.cents||0)*((c.dataset.led||c.dataset.per)?qty:1)});
return [TT,'Maß: '+sm(n(st.w))+' × '+sm(n(st.d))+' m','Rahmen: '+FR+' · Dachplatte: '+CV,'Beleuchtung: '+ledTxt(),'Montage: '+moTxt(),'Menge: '+qty,x?'Preis Dach: '+eur(x[3]*qty)+(ex?' · Gesamt mit Auswahl: '+eur(x[3]*qty+ex):''):'','Link: '+shareUrl()].filter(Boolean).join('\\n')}
function fill(){if(shP&&!shP.hidden){var u=shareUrl(),t=cfgText();q('[data-share-url]').value=u;q('[data-share-sum]').textContent=t.split('\\n').slice(0,6).join(' · ');q('[data-share-wa]').href='https://wa.me/?text='+encodeURIComponent(t);q('[data-share-mail]').href='mailto:?subject='+encodeURIComponent('Terrassendach-Konfiguration: '+TT)+'&body='+encodeURIComponent(t)}
if(ofP&&!ofP.hidden){var cf=q('[data-offer-cfg]'),ta=q('[data-offer-body]'),pz=q('[data-offer-plz]');if(cf)cf.value=cfgText();if(ta&&!ta.dataset.touched)ta.value='Bitte senden Sie mir ein Angebot für diese Konfiguration:\\n\\n'+cfgText();if(pz&&!pz.value&&moSt.plz)pz.value=moSt.plz}}
function pane(p,t,open){if(!p)return;p.hidden=!open;if(t)t.setAttribute('aria-expanded',open?'true':'false');if(open){if(p===ofP&&shP)pane(shP,shT,false);if(p===shP&&ofP)pane(ofP,ofT,false);fill()}}
if(shT)shT.addEventListener('click',function(){pane(shP,shT,shP.hidden)});
if(ofT)ofT.addEventListener('click',function(){pane(ofP,ofT,ofP.hidden);if(!ofP.hidden)ofP.scrollIntoView({block:'nearest',behavior:'smooth'})});
var ta0=q('[data-offer-body]');if(ta0)ta0.addEventListener('input',function(){ta0.dataset.touched='1'});
var cp=q('[data-share-copy]');if(cp)cp.addEventListener('click',function(){var inp=q('[data-share-url]');function done(){cp.textContent='Kopiert ✓';setTimeout(function(){cp.textContent='Link kopieren'},1800)}if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(inp.value).then(done,function(){inp.select()});else{inp.select();try{document.execCommand('copy');done()}catch(e){}}});
var pr=q('[data-share-print]');if(pr)pr.addEventListener('click',function(){window.print()});
try{var SPo=new URLSearchParams(location.search);if(SPo.get('angebot')==='1'||SPo.get('contact_posted')==='true'||location.hash==='#es-offer-form'){pane(ofP,ofT,true);setTimeout(function(){ofP.scrollIntoView({block:'start',behavior:'smooth'})},200)}}catch(e){}
var sb=q('[data-sticky]'),go=q('[data-sticky-go]'),mode='pick',pb=q('.es-pdp__pr'),vB=false,vP=!!pb;"""),
])

# ---------------------------------------------------------------- Produktseite (CSS)
patch('snippets/es-pdp-css.liquid', [
    ("""/* Kaufen: L = 56 px */""",
     """/* Montage: PLZ-Zeile, Angebot/Teilen-Panels, Formular */
.es-pdp .es-pdp__ar span small{display:block;font-size:13px;color:var(--mu);font-weight:400;line-height:1.35}
.es-pdp .es-pdp__ml{color:var(--g6);font-weight:600;text-decoration:underline;text-underline-offset:2px}
.es-pdp .es-pdp__mop{padding:12px 16px 14px;border-top:1px solid var(--ln);background:#fff}
.es-pdp .es-pdp__mop>label{display:block;font-size:14px;font-weight:700;color:var(--ink);margin:0 0 6px}
.es-pdp .es-pdp__mor{display:flex;align-items:center;gap:12px}
.es-pdp .es-pdp__mor input{width:140px;height:var(--es-h-m,48px);border:1px solid var(--ui);padding:0 12px;font-family:inherit;font-size:17px;font-weight:600;color:var(--ink);background:#fff;letter-spacing:.04em}
.es-pdp .es-pdp__mor input:focus{outline:2px solid var(--g);outline-offset:1px;border-color:var(--g)}
.es-pdp .es-pdp__mor span{font-size:14px;color:var(--mu)}
.es-pdp .es-pdp__moh{margin:8px 0 0;font-size:13px;line-height:1.45;color:var(--tx)}.es-pdp .es-pdp__moh.is-err{color:#C93F3F}
.es-pdp .es-pdp__sec{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0 0 16px}
.es-pdp .es-pdp__sb{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:var(--es-h-m,48px);padding:0 12px;border:1px solid var(--ink);background:#fff;color:var(--ink);font-family:inherit;font-weight:700;font-size:15px;cursor:pointer;transition:background .12s,color .12s;white-space:nowrap}
.es-pdp .es-pdp__sb:hover,.es-pdp .es-pdp__sb[aria-expanded="true"]{background:var(--ink);color:#fff}
.es-pdp .es-pdp__sb svg{width:18px;height:18px;flex:none}
.es-pdp .es-pdp__panel{border:1px solid var(--ln);background:#fff;margin:0 0 16px}
.es-pdp .es-pdp__pb{padding:16px}
.es-pdp .es-pdp__psum{margin:0 0 12px;font-size:14px;line-height:1.5;color:var(--tx)}
.es-pdp .es-pdp__pr2{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;margin:0 0 12px}
.es-pdp .es-pdp__pr2 input{min-width:0;height:var(--es-h-m,48px);border:1px solid var(--ui);padding:0 12px;font-family:inherit;font-size:14px;color:var(--tx);background:var(--bg2)}
.es-pdp .es-pdp__pr2 button,.es-pdp .es-pdp__pl button,.es-pdp .es-pdp__pl a{display:inline-flex;align-items:center;justify-content:center;height:var(--es-h-m,48px);padding:0 14px;border:1px solid var(--ink);background:#fff;color:var(--ink)!important;font-family:inherit;font-weight:700;font-size:14px;text-decoration:none!important;cursor:pointer;white-space:nowrap}
.es-pdp .es-pdp__pr2 button:hover,.es-pdp .es-pdp__pl button:hover,.es-pdp .es-pdp__pl a:hover{background:var(--ink);color:#fff!important}
.es-pdp .es-pdp__pl{display:flex;flex-wrap:wrap;gap:8px}
.es-pdp .es-pdp__phint{margin:12px 0 0;font-size:13px;color:var(--mu);line-height:1.45}
.es-pdp .es-pdp__of label{display:block;font-size:14px;font-weight:700;color:var(--ink);margin:0 0 12px}
.es-pdp .es-pdp__of input,.es-pdp .es-pdp__of textarea{display:block;width:100%;margin-top:6px;border:1px solid var(--ui);padding:10px 12px;font-family:inherit;font-size:15px;font-weight:400;line-height:1.4;color:var(--tx);background:#fff}
.es-pdp .es-pdp__of input{height:var(--es-h-m,48px)}
.es-pdp .es-pdp__of input:focus,.es-pdp .es-pdp__of textarea:focus{outline:2px solid var(--g);outline-offset:1px;border-color:var(--g)}
.es-pdp .es-pdp__fr{display:grid;grid-template-columns:1fr 1fr;gap:0 12px}
.es-pdp .es-pdp__ok{margin:0 0 14px;padding:12px 14px;background:var(--gl);border-left:4px solid var(--g);color:var(--ink);font-weight:600;font-size:15px;line-height:1.45}
.es-pdp .es-pdp__atc--sec{width:100%;margin-top:4px}
@media print{.es-pdp .es-pdp__sticky,.es-pdp .es-pdp__sec,.es-pdp .es-pdp__buy,.es-pdp .es-pdp__pr2,.es-pdp .es-pdp__pl,.es-pdp .es-pdp__phint,.es-pdp .es-pdp__panel[data-offer],.es-pdp .es-pdp__ths{display:none!important}.es-pdp .es-pdp__g{grid-template-columns:1fr}.es-pdp .es-pdp__gal{position:static}}
/* Kaufen: L = 56 px */"""),
    (""".es-pdp .es-pdp__trust{grid-template-columns:1fr;font-size:14px}
}""",
     """.es-pdp .es-pdp__trust{grid-template-columns:1fr;font-size:14px}
.es-pdp .es-pdp__sb{font-size:14px;padding:0 8px;gap:6px}.es-pdp .es-pdp__sb svg{width:16px;height:16px}
.es-pdp .es-pdp__fr{grid-template-columns:1fr;gap:0}.es-pdp .es-pdp__pb{padding:12px}.es-pdp .es-pdp__mop{padding:10px 12px 12px}
.es-pdp .es-pdp__pl button,.es-pdp .es-pdp__pl a{flex:1 1 auto}
}"""),
    ("""@media(max-width:380px){.es-pdp .es-pdp__info{padding:0 12px}""",
     """@media(max-width:380px){.es-pdp .es-pdp__sec{grid-template-columns:1fr}.es-pdp .es-pdp__info{padding:0 12px}"""),
])

# ---------------------------------------------------------------- Warenkorb-Wächter (LED + Montage)
patch('snippets/es-led-guard.liquid', [
    ("""{%- comment -%}e-Stegplatten: LED-Spots (led-spots-terrassenueberdachung) gibt es nur zusammen mit einem Terrassendach. Entfernt LED-Sets aus dem Warenkorb, sobald kein Dach mehr darin liegt, und leitet die LED-Produktseite zu den Terrassenüberdachungen um.{%- endcomment -%}
{%- if request.page_type == 'product' and product.handle == 'led-spots-terrassenueberdachung' -%}""",
     """{%- comment -%}e-Stegplatten: LED-Spots und Montage gibt es nur zusammen mit einem Terrassendach. Entfernt diese Zusatzpositionen aus dem Warenkorb, sobald kein Dach mehr darin liegt, und leitet ihre Produktseiten zu den Terrassenüberdachungen um. Handles hier und in ADD pflegen.{%- endcomment -%}
{%- assign es_addons = 'led-spots-terrassenueberdachung,montage-terrassendach-stegplatten,montage-terrassendach-vsg-glas' | split: ',' -%}
{%- if request.page_type == 'product' and es_addons contains product.handle -%}"""),
    ("""var LED='led-spots-terrassenueberdachung',base=(window.routes&&window.routes.rootUrlWithoutSlash)||'',F=window.fetch.bind(window),busy=false;
function roof(i){return i.handle!==LED&&(i.product_type==='Terrassenüberdachung'||/terrassendach|terrassenüberdachung/i.test(i.product_title||''))}""",
     """var ADD=['led-spots-terrassenueberdachung','montage-terrassendach-stegplatten','montage-terrassendach-vsg-glas'],base=(window.routes&&window.routes.rootUrlWithoutSlash)||'',F=window.fetch.bind(window),busy=false;
function add(i){return ADD.indexOf(i.handle)>-1}
function roof(i){return !add(i)&&(i.product_type==='Terrassenüberdachung'||/terrassendach|terrassenüberdachung/i.test(i.product_title||''))}"""),
    ("c.items.forEach(function(i){if(i.handle===LED&&!has){u[i.key]=0;n++}});",
     "c.items.forEach(function(i){if(add(i)&&!has){u[i.key]=0;n++}});"),
])

# ---------------------------------------------------------------- Hero-Konfigurator
patch('snippets/es-hero-konfig.liquid', [
    ("Parameter: kc (Kollektion mit den Geschwister-Produkten), lz (Lieferzeit-Text).",
     "Parameter: kc (Kollektion mit den Geschwister-Produkten), lz (Lieferzeit-Text), mu (Link Farbmuster, optional). Zweite Zeile unter dem Preis: Farbmuster + Angebot anfordern (öffnet das Angebotsformular der Produktseite)."),
    ("""<p class="ehk__alt">Nur Platten gesucht? <a href="/collections/doppelstegplatten">Stegplatten nach Stärke</a> · <a href="/collections/doppelstegplatten-komplettset-dachhaut">Komplettsets</a></p>""",
     """<p class="ehk__alt">{%- if mu != blank -%}Unsicher bei der Farbe? <a href="{{ mu }}">Farbmuster bestellen</a> · {% endif -%}Lieber ein persönliches Angebot? <a data-kao href="{{ p0.url }}?variant={{ v0.id }}&amp;angebot=1">Angebot anfordern</a></p>
<p class="ehk__alt">Nur Platten gesucht? <a href="/collections/doppelstegplatten">Stegplatten nach Stärke</a> · <a href="/collections/doppelstegplatten-komplettset-dachhaut">Komplettsets</a></p>"""),
    ("var kp=R.querySelector('[data-kp]'),ks=R.querySelector('[data-ks]'),go=R.querySelector('[data-kgo]'),kl=R.querySelector('[data-kl]');",
     "var kp=R.querySelector('[data-kp]'),ks=R.querySelector('[data-ks]'),go=R.querySelector('[data-kgo]'),kl=R.querySelector('[data-kl]'),kao=R.querySelector('[data-kao]');"),
    ("go.setAttribute('href',p.u+'?variant='+v[0]+(st.l!=='0'?'&led='+st.l:''))}else{kp.textContent='–';ks.textContent='Maß auf Anfrage';go.setAttribute('href',p?p.u:'/collections/terrassenuberdachung')}",
     "go.setAttribute('href',p.u+'?variant='+v[0]+(st.l!=='0'?'&led='+st.l:''));if(kao)kao.setAttribute('href',p.u+'?variant='+v[0]+(st.l!=='0'?'&led='+st.l:'')+'&angebot=1')}else{kp.textContent='–';ks.textContent='Maß auf Anfrage';go.setAttribute('href',p?p.u:'/collections/terrassenuberdachung');if(kao)kao.setAttribute('href',(p?p.u:'/collections/terrassenuberdachung')+'?angebot=1')}"),
    (".esl .ehk__alt{font-size:13px;color:var(--mu,#5E6863);margin:14px 0 0}",
     ".esl .ehk__alt{font-size:13px;color:var(--mu,#5E6863);margin:14px 0 0}.esl .ehk__alt+.ehk__alt{margin-top:6px}"),
])

# ---------------------------------------------------------------- Startseite: Judge.me-Gesamtwertung, Farbmuster-Link
patch('sections/es-landing.liquid', [
    ("<div><b>{{ s.proof3_t }}</b>{{ s.proof3_s }}</div></div>",
     "{%- assign jc = shop.metafields.judgeme.all_reviews_count | plus: 0 -%}{%- assign jr = shop.metafields.judgeme.all_reviews_rating | times: 1.0 | round: 1 -%}<div>{%- if jc > 0 -%}<b>{{ jr | replace: '.', ',' }} ★ aus {{ jc }} Bewertungen</b>{%- else -%}<b>{{ s.proof3_t }}</b>{%- endif -%}{{ s.proof3_s }}</div></div>"),
    ("""{"type":"text","id":"proof3_t","label":"Beleg 3","default":"Echte Bewertungen"},{"type":"text","id":"proof3_s","label":"Beleg 3 Zusatz","default":"verifiziert über Judge.me"},""",
     """{"type":"text","id":"proof3_t","label":"Beleg 3 (Fallback, sonst Judge.me-Gesamtwertung)","default":"Echte Bewertungen"},{"type":"text","id":"proof3_s","label":"Beleg 3 Zusatz","default":"verifiziert über Judge.me"},
{"type":"url","id":"muster_url","label":"Link Farbmuster-Produkt (Konfigurator)","info":"z. B. /products/farbmuster – leer = kein Link"},"""),
])
s = (B / 'new/sections/es-landing.liquid').read_text(encoding='utf-8')
assert s.count("{% render 'es-hero-konfig', kc: kc, lz: s.lz_terrassen %}") == 2
s = s.replace("{% render 'es-hero-konfig', kc: kc, lz: s.lz_terrassen %}", "{% render 'es-hero-konfig', kc: kc, lz: s.lz_terrassen, mu: s.muster_url %}")
(B / 'new/sections/es-landing.liquid').write_text(s, encoding='utf-8')

# ---------------------------------------------------------------- Startseite: Hero beginnt mit dem Bild, Kategorie-Titel ohne Trennstriche
patch('sections/es-landing.liquid', [
    ("""<section class="hero" data-screen-label="Hero">
<div class="c">
<div>
{%- if s.kicker != blank -%}<p class="k">{{ s.kicker }}</p>{%- endif -%}
<h1>{{ s.hero_title }}</h1>
{%- if s.hero_text != blank -%}<p class="lead">{{ s.hero_text }}</p>{%- endif -%}
{%- assign kh""",
     """<section class="hero" data-screen-label="Hero">
<div class="c">
<div class="hv">
{%- if s.hero_image != blank -%}<picture>{%- if s.hero_image_m -%}<source media="(max-width:749px)" srcset="{{ s.hero_image_m | image_url: width: 480 }} 480w, {{ s.hero_image_m | image_url: width: 720 }} 720w, {{ s.hero_image_m | image_url: width: 960 }} 960w, {{ s.hero_image_m | image_url: width: 1200 }} 1200w" sizes="100vw">{%- endif -%}<img class="hv__img" src="{{ s.hero_image | image_url: width: 1400 }}" srcset="{{ s.hero_image | image_url: width: 700 }} 700w, {{ s.hero_image | image_url: width: 1000 }} 1000w, {{ s.hero_image | image_url: width: 1400 }} 1400w" sizes="(max-width:999px) 100vw, 660px" alt="{{ s.hero_image.alt | default: s.hero_title | escape }}" width="{{ s.hero_image.width | default: 1400 }}" height="{{ s.hero_image.height | default: 1050 }}" fetchpriority="high"></picture>{%- endif -%}
<div class="hv__tx">
{%- if s.kicker != blank -%}<p class="k">{{ s.kicker }}</p>{%- endif -%}
<h1>{{ s.hero_title }}</h1>
{%- if s.hero_text != blank -%}<p class="lead">{{ s.hero_text }}</p>{%- endif -%}
</div>
</div>
<div class="hc">
{%- assign kh"""),
    ("""{% render 'es-hero-konfig', kc: kc, lz: s.lz_terrassen, mu: s.muster_url %}
{%- endif -%}
</div>
<div>
{%- if s.hero_image != blank -%}<img src="{{ s.hero_image | image_url: width: 1200 }}" srcset="{{ s.hero_image | image_url: width: 700 }} 700w, {{ s.hero_image | image_url: width: 1200 }} 1200w" sizes="(max-width:1000px) 100vw, 600px" alt="{{ s.hero_image.alt | default: s.hero_title | escape }}" fetchpriority="high">{%- endif -%}
<div class="proof">""",
     """{% render 'es-hero-konfig', kc: kc, lz: s.lz_terrassen, mu: s.muster_url %}
{%- endif -%}
</div>
<div class="proof">"""),
    ("""
</div>
</div>
</section>
<section class="trust" data-screen-label="Vertrauen">""",
     """
</div>
</section>
<section class="trust" data-screen-label="Vertrauen">"""),
    ('{"type":"image_picker","id":"hero_image","label":"Bild"},',
     '{"type":"image_picker","id":"hero_image","label":"Bild"},{"type":"image_picker","id":"hero_image_m","label":"Bild für Handys (optional, 4:3 – Dach oben, ruhige Fläche unten)","info":"Ohne Auswahl wird das Bild oben auch auf Handys verwendet."},'),
    ("""<h3>{{ b.settings.title | escape | replace: 'Terrassenüberdachung', 'Terrassen&shy;überdachung' | replace: 'Stegplatten', 'Steg&shy;platten' }}</h3>""",
     """<h3>{{ b.settings.title | escape }}</h3>"""),
])

patch('snippets/es-landing-css.liquid', [
    ("""/* Hero */
.esl .hero{border-bottom:1px solid var(--ln)}
.esl .hero .c{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:48px;align-items:start;padding-top:32px;padding-bottom:48px}
.esl .hero img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;border:1px solid var(--ln)}
.esl .proof{display:grid;grid-template-columns:repeat(3,1fr);border:1px solid var(--ln);border-top:none;background:#fff}""",
     """/* Hero: Bild zuerst (Überschrift auf dem Bild), daneben der Konfigurator; mobil Bild → Konfigurator → Belege */
.esl .hero{border-bottom:1px solid var(--ln)}
.esl .hero .c{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);grid-template-rows:minmax(0,1fr) auto;grid-template-areas:"hv hc" "proof hc";gap:0 48px;align-items:start;padding-top:24px;padding-bottom:48px}
.esl .hv{grid-area:hv;position:relative;align-self:stretch;min-height:440px;display:flex;flex-direction:column;justify-content:flex-end;background:var(--ink);border:1px solid var(--ln);overflow:hidden}
.esl .hv__img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.esl .hv__tx{position:relative;padding:140px 28px 28px;background:linear-gradient(180deg,rgba(27,31,29,0) 0%,rgba(27,31,29,.55) 40%,rgba(27,31,29,.9) 100%)}
.esl .hv__tx .k{color:#A9DBBE;margin-bottom:8px}
.esl .hv__tx h1{color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.35)}
.esl .hv__tx .lead{color:rgba(255,255,255,.92);margin-top:10px;text-shadow:0 1px 2px rgba(0,0,0,.35)}
.esl .hc{grid-area:hc;min-width:0}
.esl .proof{grid-area:proof;display:grid;grid-template-columns:repeat(3,1fr);border:1px solid var(--ln);border-top:none;background:#fff}"""),
    (".esl .ehx{margin-top:24px}", ".esl .ehx{margin-top:0}"),
    (".esl .cat{display:flex;flex-direction:column;min-width:0;border:1px solid var(--ln);",
     ".esl .cat{display:flex;flex-direction:column;min-width:0;container-type:inline-size;border:1px solid var(--ln);"),
    (".esl .cat h3{font-weight:800;line-height:1.25;hyphens:auto;-webkit-hyphens:auto;overflow-wrap:anywhere}",
     "/* Titel/Link skalieren mit der Kachelbreite, damit sie möglichst einzeilig bleiben; keine Silbentrennung */\n.esl .cat h3{font-weight:800;line-height:1.25;font-size:clamp(14px,6.4cqi,18px);hyphens:manual;-webkit-hyphens:manual;overflow-wrap:normal;text-wrap:balance}"),
    (".esl .cat .l{margin-top:auto;padding-top:8px;font-weight:700;color:var(--g6);display:inline-flex;gap:6px;align-items:center;font-size:15px;white-space:nowrap}",
     ".esl .cat .l{margin-top:auto;padding-top:8px;font-weight:700;color:var(--g6);display:inline-flex;gap:6px;align-items:center;font-size:clamp(13px,5.6cqi,15px);white-space:nowrap}"),
    (""".esl .hero .c{grid-template-columns:1fr;gap:24px}
.esl .cats,.esl .steps,.esl .prods{grid-template-columns:repeat(2,minmax(0,1fr))}""",
     """.esl .hero .c{grid-template-columns:1fr;grid-template-rows:auto;grid-template-areas:"hv" "hc" "proof";gap:20px 0}
.esl .hv{min-height:0;aspect-ratio:3/2;align-self:auto}
.esl .hv__tx{padding:80px 20px 20px}
.esl .cats,.esl .steps,.esl .prods{grid-template-columns:repeat(2,minmax(0,1fr))}"""),
    (""".esl .hero .c{padding-top:12px;padding-bottom:24px;gap:20px}
.esl .hero .k,.esl .lead{display:none}
.esl .hero .c>div:last-child{margin:0 -16px}
.esl .hero img{aspect-ratio:16/10;border-left:0;border-right:0}
.esl .proof{border-left:0;border-right:0}""",
     """.esl .hero .c{padding-top:0;padding-bottom:24px;gap:16px 0}
.esl .hv{margin:0 -16px;border-left:0;border-right:0;aspect-ratio:4/3}
.esl .hv__tx{padding:56px 16px 16px}
.esl .hv__tx .lead{display:none}
.esl .proof{border-left:0;border-right:0;margin:0 -16px}"""),
    (".esl .ehx{margin:12px -16px 0}", ".esl .ehx{margin:0 -16px}"),
    (""".esl .cat h3{font-size:15px;min-height:2.5em}
.esl .cat .l{font-size:14px;gap:4px;white-space:normal;line-height:1.3}""",
     """.esl .cat .l{gap:4px}"""),
])

# ---------------------------------------------------------------- Startseite: Überschriften möglichst einzeilig (Belege, Tabs, Trust-Leiste, H2, Kacheln ≤ 359 px)
patch('sections/es-landing.liquid', [
    ("""<div class="proof"><div><b>{{ s.proof1_t }}</b>{{ s.proof1_s }}</div><div><b>{{ s.proof2_t }}</b>{{ s.proof2_s }}</div>""",
     """<div class="proof"><div>{{ ic_check }}<b>{{ s.proof1_t }}</b><span>{{ s.proof1_s }}</span></div><div>{{ ic_check }}<b>{{ s.proof2_t }}</b><span>{{ s.proof2_s }}</span></div>"""),
    ("""<div>{%- if jc > 0 -%}<b>{{ jr | replace: '.', ',' }} ★ aus {{ jc }} Bewertungen</b>{%- else -%}<b>{{ s.proof3_t }}</b>{%- endif -%}{{ s.proof3_s }}</div></div>""",
     """<div>{{ ic_check }}{%- if jc > 0 -%}<b>{{ jr | replace: '.', ',' }} ★ aus {{ jc }} Bewertungen</b>{%- else -%}<b>{{ s.proof3_t }}</b>{%- endif -%}<span>{{ s.proof3_s }}</span></div></div>"""),
])

patch('snippets/es-landing-css.liquid', [
    # Belege: Zeilen statt drei schmaler Spalten – der Titel bleibt immer einzeilig, der Zusatz rückt bei Platzmangel darunter
    (""".esl .proof{grid-area:proof;display:grid;grid-template-columns:repeat(3,1fr);border:1px solid var(--ln);border-top:none;background:#fff}
.esl .proof div{padding:14px 16px;border-right:1px solid var(--ln);font-size:14px;line-height:1.4;color:var(--mu)}
.esl .proof div:last-child{border-right:none}
.esl .proof b{display:block;color:var(--ink);font-size:15px;margin-bottom:2px}""",
     """.esl .proof{grid-area:proof;display:grid;grid-template-columns:1fr;border:1px solid var(--ln);border-top:none;background:#fff}
.esl .proof div{display:flex;flex-wrap:wrap;align-items:baseline;gap:0 8px;padding:9px 16px;border-bottom:1px solid var(--ln);font-size:14px;line-height:1.4;color:var(--mu)}
.esl .proof div:last-child{border-bottom:none}
.esl .proof svg{color:var(--g);flex:none;width:16px;height:16px;align-self:center;margin-right:2px}
.esl .proof b{display:inline;white-space:nowrap;color:var(--ink);font-size:15px}"""),
    (""".esl .proof{border-left:0;border-right:0;margin:0 -16px}
.esl .proof div{padding:10px 8px;font-size:12px;line-height:1.35}
.esl .proof b{font-size:13px;line-height:1.25}""",
     """.esl .proof{border-left:0;border-right:0;margin:0 -16px}
.esl .proof div{padding:8px 16px;font-size:13px;line-height:1.35}
.esl .proof b{font-size:14px}"""),
    # Tabs: Breite nach Beschriftung verteilen, damit „Terrassendach konfigurieren" auch bei 1000–1100 px und auf Handys einzeilig bleibt
    (""".esl .ehx__tabs{display:grid;grid-template-columns:1fr 1fr;border:1px solid var(--ln);border-bottom:0;background:var(--bg2)}
.esl .ehx__tab{display:flex;flex-direction:column;""",
     """.esl .ehx__tabs{display:flex;border:1px solid var(--ln);border-bottom:0;background:var(--bg2)}
.esl .ehx__tab{flex:1 1 auto;min-width:0;display:flex;flex-direction:column;"""),
    (".esl .ehx__tab small{font-size:12px;font-weight:500;color:var(--mu)}",
     ".esl .ehx__tab small{display:block;width:0;min-width:100%;font-size:12px;font-weight:500;color:var(--mu)}"),
    (".esl .ehx__tab{padding:8px 12px;font-size:14px}.esl .ehx__tab small{display:none}",
     ".esl .ehx__tab{padding:8px 10px;font-size:14px;align-items:center;text-align:center}.esl .ehx__tab small{display:none}"),
    # Trust-Leiste auf Handys einspaltig (Titel nowrap, Zusatz daneben oder darunter); H2 und Kacheln bei sehr schmalen Geräten
    ("@media(max-width:380px){.esl h1{font-size:24px}}",
     """@media(max-width:480px){
.esl .hv__tx .k{font-size:11px;letter-spacing:.07em}
.esl .trust .c{grid-template-columns:1fr}
.esl .trust .c>div{padding:10px 16px}
.esl .trust span{display:flex;flex-wrap:wrap;align-items:baseline;gap:0 8px}
.esl .trust b{white-space:nowrap}
.esl .trust span span{margin-top:0}
}
@media(max-width:380px){.esl h1{font-size:24px}.esl h2{font-size:22px}}
@media(max-width:359px){
.esl .ehx__tab{font-size:13px;padding:8px 6px}
.esl .cats{grid-template-columns:1fr;gap:10px}
.esl .cat{flex-direction:row}
.esl .cat .es-cimg{width:104px;flex:none;aspect-ratio:auto;border-bottom:0;border-right:1px solid var(--ln)}
.esl .cat .tx{justify-content:center;gap:4px;padding:10px 12px}
.esl .cat h3{font-size:16px}
.esl .cat .l{margin-top:0;padding-top:2px;font-size:14px}
}"""),
])

# ---------------------------------------------------------------- index.json: Trust-Text, Farbmuster
p = B / 'new/templates/index.json'
raw = p.read_text(encoding='utf-8')
head = re.match(r'(\s*/\*.*?\*/\s*)', raw, re.S).group(1)
d = json.loads(raw[len(head):])
L = d['sections']['es_landing']
L['blocks']['t2']['settings'] = {'title': 'Zuschnitt millimetergenau', 'text': 'rechtwinklig, Kanten entgratet, Kammern staubfrei'}
L['settings']['muster_url'] = '/products/farbmuster'
# Hero-Bilder (Higgsfield-Generate, Quelle content/hero/*.jpg) – Dateien müssen vor dem Theme-Upload in Shopify > Inhalte > Dateien liegen
L['settings']['hero_image'] = 'shopify://shop_images/hero-terrassendach-stegplatten.jpg'
L['settings']['hero_image_m'] = 'shopify://shop_images/hero-terrassendach-stegplatten-mobil.jpg'
L['blocks']['c1']['settings'].update({'title': 'Stegplatten', 'text': 'Doppelstegplatten 4,5–16 mm, Polycarbonat oder Acrylglas – millimetergenau zugeschnitten.'})
L['blocks']['c2']['settings']['title'] = 'Terrassendächer'
L['blocks']['c4']['settings']['cta'] = 'Nach Stärke'
L['settings']['fin_alt'] = L['settings']['fin_alt'].replace('</p>', ' · Unsicher bei der Farbe? <a href="/products/farbmuster">Farbmuster bestellen</a></p>')
p.write_text(head + json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# ---------------------------------------------------------------- Prüfungen
import collections
for f in FILES:
    t = (B / 'new' / f).read_text(encoding='utf-8')
    if f.endswith('.liquid'):
        c = collections.Counter(re.findall(r'{%-?\s*(\w+)', t))
        for a, b_ in [('if', 'endif'), ('for', 'endfor'), ('unless', 'endunless'), ('capture', 'endcapture'), ('comment', 'endcomment'), ('form', 'endform'), ('case', 'endcase')]:
            assert c[a] == c[b_], f'{f}: {a}={c[a]} {b_}={c[b_]}'
        m = re.search(r'{% schema %}(.*){% endschema %}', t, re.S)
        if m:
            json.loads(m.group(1))
    else:
        json.loads(t[len(head):])
    print('ok', f, len(t.encode('utf-8')))
