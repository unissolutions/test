import sys, pathlib
base = pathlib.Path(sys.argv[1])
orig, new = base/'orig', base/'new'

def patch(name, reps):
    s = (orig/name).read_text(encoding='utf-8')
    for old, rep in reps:
        n = s.count(old)
        if n != 1:
            sys.exit(f'{name}: expected 1 match, got {n} for: {old[:70]!r}')
        s = s.replace(old, rep)
    (new/name).write_text(s, encoding='utf-8')
    print(f'{name}: {len(reps)} edits ok')

LEDSVG = r"""<svg width="36" height="36" viewBox="0 0 36 36" fill="none"><rect x="3" y="8" width="30" height="5" fill="#3B4043"/><path class="bm" d="M9 17 5 31h8zM18 17l-4 14h8zM27 17l-4 14h8z" fill="currentColor" fill-opacity=".28"/><circle cx="9" cy="16" r="2.6" fill="currentColor"/><circle cx="18" cy="16" r="2.6" fill="currentColor"/><circle cx="27" cy="16" r="2.6" fill="currentColor"/></svg>"""

# ---------- Produktseite: Section ----------
patch('es-pdp-terrasse.liquid', [
 ("  assign imgs = p.media | where: 'media_type', 'image'\n-%}",
  "  assign imgs = p.media | where: 'media_type', 'image'\n"
  "  assign led = section.settings.led_product\n"
  "  if led == blank\n"
  "    assign led = all_products['led-spots-terrassenueberdachung']\n"
  "  endif\n-%}"),
 ("{% render 'es-pdp-css' %}\n",
  "{% render 'es-pdp-css' %}\n"
  "<style>.es-pdp .es-pdp__lr input{-webkit-appearance:radio;appearance:auto}"
  ".es-pdp .es-pdp__lr:has(input:checked){background:var(--gl);box-shadow:inset 3px 0 0 var(--g)}"
  ".es-pdp .es-pdp__li{display:flex;align-items:center;justify-content:center;width:58px;height:58px;border:1px solid var(--ln);background:#1F2427;color:#F2C94C}"
  ".es-pdp .es-pdp__li--off{background:#fff;color:#C9CFCB}.es-pdp .es-pdp__li--off .bm{display:none}"
  ".es-pdp .es-pdp__lnote{margin:0;padding:12px 20px;border-top:1px solid var(--ln);background:var(--bg2);font-size:14px;color:var(--tx)}"
  ".es-pdp .es-pdp__tot{margin:-6px 0 14px;font-size:16px;color:var(--tx)}.es-pdp .es-pdp__tot b{color:var(--ink);font-size:20px;font-stretch:115%}"
  "@media(max-width:749px){.es-pdp .es-pdp__li{width:48px;height:48px;grid-row:span 2}.es-pdp .es-pdp__lnote{padding:10px 14px;font-size:13px}}</style>\n"),
 ("{%- capture addons -%}",
  "{%- if led.id != blank and led.available -%}{%- capture ledsvg -%}" + LEDSVG + "{%- endcapture -%}\n"
  "<div class=\"es-pdp__add es-pdp__led r14\" data-led-box><div class=\"es-pdp__add-h\">Beleuchtung</div>\n"
  "<label class=\"es-pdp__ar es-pdp__lr\"><input type=\"radio\" name=\"es-led-{{ section.id }}\" value=\"\" data-led=\"0\" checked><span class=\"es-pdp__li es-pdp__li--off r10\" aria-hidden=\"true\">{{ ledsvg }}</span><span>Ohne LED-Beleuchtung</span><b>+ 0 €</b></label>\n"
  "{%- for lv in led.variants -%}{%- unless lv.available -%}{%- continue -%}{%- endunless -%}{%- assign lcnt = lv.title | split: 'er' | first | strip -%}{%- assign limg = lv.image | default: led.featured_image -%}"
  "<label class=\"es-pdp__ar es-pdp__lr\"><input type=\"radio\" name=\"es-led-{{ section.id }}\" value=\"{{ lv.id }}\" data-addon data-led=\"{{ lcnt }}\" data-cents=\"{{ lv.price }}\">"
  "{%- if limg != blank -%}<img class=\"r10\" src=\"{{ limg | image_url: width: 120 }}\" alt=\"\" loading=\"lazy\" width=\"58\" height=\"58\">{%- else -%}<span class=\"es-pdp__li r10\" aria-hidden=\"true\">{{ ledsvg }}</span>{%- endif -%}"
  "<span>LED-Spots – {{ lv.title }}</span><b>+ {{ lv.price | money_without_currency | remove: ',00' }} €</b></label>{%- endfor -%}\n"
  "<p class=\"es-pdp__lnote\">{{ section.settings.led_note | default: 'Unsere vormontierten LED-Spots werden optimal auf die Anzahl der Träger abgestimmt.' }}</p></div>\n"
  "{%- endif -%}\n"
  "{%- capture addons -%}"),
 ('<input type="checkbox" data-addon value="{{ av.id }}">',
  '<input type="checkbox" data-addon value="{{ av.id }}" data-cents="{{ av.price }}">'),
 ('<form class="es-pdp__buy"',
  '<p class="es-pdp__tot" data-tot hidden>Gesamt inkl. Auswahl: <b data-tot-v></b></p>\n<form class="es-pdp__buy"'),
 ('"default":"Montageanleitung liegt bei, Telefon-Support bei der Montage"}\n],"blocks"',
  '"default":"Montageanleitung liegt bei, Telefon-Support bei der Montage"},\n'
  '{"type":"header","content":"LED-Beleuchtung"},\n'
  '{"type":"product","id":"led_product","label":"LED-Produkt (Varianten = Sets)","info":"Leer = Produkt mit Handle led-spots-terrassenueberdachung. Ohne Produkt wird die Auswahl ausgeblendet."},\n'
  '{"type":"text","id":"led_note","label":"Hinweis unter der LED-Auswahl","default":"Unsere vormontierten LED-Spots werden optimal auf die Anzahl der Träger abgestimmt."}\n'
  '],"blocks"'),
])

# ---------- Produktseite: Logik ----------
patch('es-pdp-js.liquid', [
 ("var FR={{ frame | json }},CV={{ cover | json }},",
  "var TT={{ p.title | json }},FR={{ frame | json }},CV={{ cover | json }},"),
 ("var btn=q('[data-atc]'),spr=q('[data-sticky-price]'),idIn=q('[data-id]');\n",
  "var btn=q('[data-atc]'),spr=q('[data-sticky-price]'),idIn=q('[data-id]');\n"
  "function tot(){var x=cur();if(!x)return;var qty=Math.max(1,parseInt(qi.value,10)||1),s=x[3]*qty,ex=0;"
  "qa('[data-addon]').forEach(function(c){if(c.checked)ex+=(+c.dataset.cents||0)*(c.dataset.led?qty:1)});"
  "var t=q('[data-tot]');if(t){t.hidden=!ex;if(ex)q('[data-tot-v]').textContent=eur(s+ex)}if(spr)spr.textContent=eur(s+ex)}\n"),
 ("btn.textContent=x[5]?'In den Warenkorb':'Nicht verfügbar';if(spr)spr.textContent=eur(x[3]);",
  "btn.textContent=x[5]?'In den Warenkorb':'Nicht verfügbar';tot();"),
 ("qi.value=Math.max(1,(parseInt(qi.value,10)||1)+(+b.dataset.qd))})});",
  "qi.value=Math.max(1,(parseInt(qi.value,10)||1)+(+b.dataset.qd));tot()})});"
  "qi.addEventListener('input',tot);qa('[data-addon],[data-led]').forEach(function(c){c.addEventListener('change',tot)});\n"
  "try{var L=new URLSearchParams(location.search).get('led');if(L)qa('[data-led]').forEach(function(c){if(c.dataset.led===L)c.checked=true})}catch(e){}"),
 ("qa('[data-addon]').forEach(function(c){if(c.checked)items.push({id:+c.value,quantity:1})});",
  "qa('[data-addon]').forEach(function(c){if(!c.checked)return;var it={id:+c.value,quantity:c.dataset.led?qty:1};"
  "if(c.dataset.led)it.properties={'Für Überdachung':TT+' – '+sm(n(st.w))+' × '+sm(n(st.d))+' m'};items.push(it)});"),
])

# ---------- Startseite: Hero-Konfigurator ----------
patch('es-hero-konfig.liquid', [
 ("  assign ld = dd | remove: ',00' | replace: ',50', ',5' | replace: ' Meter', ' m'\n-%}",
  "  assign ld = dd | remove: ',00' | replace: ',50', ',5' | replace: ' Meter', ' m'\n"
  "  assign led = all_products['led-spots-terrassenueberdachung']\n-%}"),
 ('<div class="ehk__ft">',
  "{%- if led.id != blank and led.available -%}<div class=\"ehk__o\"><div class=\"ehk__l\"><b>LED-Spots</b><span data-klp>vormontiert, optional</span></div><div class=\"ehk__p\">"
  "<button type=\"button\" class=\"ehk__pill is-on\" data-led=\"0\" data-lc=\"0\">Ohne</button>"
  "{%- for lv in led.variants -%}{%- if lv.available -%}{%- assign lcnt = lv.title | split: 'er' | first | strip -%}"
  "<button type=\"button\" class=\"ehk__pill\" data-led=\"{{ lcnt }}\" data-lc=\"{{ lv.price }}\">{{ lcnt }}er</button>{%- endif -%}{%- endfor -%}"
  "</div></div>{%- endif -%}\n<div class=\"ehk__ft\">"),
 ("st={f:'Anthrazit',c:'Klar',w:{{ dw | json }},d:{{ dd | json }}};",
  "st={f:'Anthrazit',c:'Klar',w:{{ dw | json }},d:{{ dd | json }},l:'0',lc:0};"),
 ("b.classList.toggle('is-na',!(v&&v[2]))});\n",
  "b.classList.toggle('is-na',!(v&&v[2]))});\n"
  "R.querySelectorAll('[data-led]').forEach(function(b){b.classList.toggle('is-on',b.dataset.led===st.l)});"
  "var lp=R.querySelector('[data-klp]');if(lp)lp.textContent=st.lc?'+ '+eur(st.lc)+' · vormontiert':'vormontiert, optional';\n"),
 ("if(v){kp.textContent=eur(v[1]);var a=n(st.w)*n(st.d);ks.textContent=a?eur(Math.round(v[1]/a))+'/m²':'';go.setAttribute('href',p.u+'?variant='+v[0])}",
  "if(v){kp.textContent=eur(v[1]+st.lc);var a=n(st.w)*n(st.d);ks.textContent=(a?eur(Math.round(v[1]/a))+'/m²'+(st.lc?' Dach':''):'')+(st.lc?' · inkl. LED-Spots':'');"
  "go.setAttribute('href',p.u+'?variant='+v[0]+(st.l!=='0'?'&led='+st.l:''))}"),
 ("if(b.dataset[k]!==undefined)st[k]=b.dataset[k]});upd()});",
  "if(b.dataset[k]!==undefined)st[k]=b.dataset[k]});if(b.dataset.led!==undefined){st.l=b.dataset.led;st.lc=+b.dataset.lc||0}upd()});"),
])
