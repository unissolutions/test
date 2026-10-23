/* e-Stegplatten – Mengenlogik „Komplettset selbst zusammenstellen“ (16-mm-Stegplatten, Alu-Profilsystem 60 mm).
   Abgeleitet aus dem Lieferumfang der Komplettsets (Mittel-/Randprofile Alu-Alu 60 mm, Haltewinkel, Anti-Dust-Tape,
   U-Profil mit Tropfkante, Spezial-Silikon, Schrauben je Unterkonstruktion) und den Set-Breiten 3070/4080/5080/6090/7090/8100 mm
   (= n Platten à 980 mm + (n−1) × 25 mm Profilspalt + 2 × 20 mm Randüberstand).
   Aufruf: esSetMengen({breite: 3070, tiefe: 2000, pb: 1200, uk: 'holz'}) → {n, fertig, laenge, teile:[…]} */
(function (w) {
  var JOINT = 26, EDGE = 39, SCHRAUBABSTAND = 500;   // 60-mm-Profil: je Stoß +26 mm, je Rand +39 mm → ergibt genau die Set-Breiten 3070/4080/5080/6090/7090/8100
  var LEN = [2000, 2500, 3000, 3500, 4000, 4500, 5000, 6000, 7000];
  var WAND = [3100, 4100, 5150, 6200, 7100];
  function up(list, v) { for (var i = 0; i < list.length; i++) if (list[i] >= v) return list[i]; return null; }
  function packs(stk, sizes) { // kleinste Packungskombination, die stk abdeckt (sizes absteigend, z. B. [100,20])
    var out = [], rest = stk;
    for (var i = 0; i < sizes.length; i++) { var s = sizes[i], last = i === sizes.length - 1; var q = last ? Math.ceil(rest / s) : Math.floor(rest / s); if (q > 0) { out.push({ size: s, qty: q }); rest -= q * s; } }
    // Vergleich: eine große Packung statt vieler kleiner (z. B. 6×20 → 1×100)
    if (sizes.length > 1) { var small = out.filter(function (p) { return p.size === sizes[sizes.length - 1]; })[0]; if (small && small.qty * small.size > sizes[0] * 0.6) { var big = out.filter(function (p) { return p.size === sizes[0]; })[0]; if (big) big.qty += 1; else out.unshift({ size: sizes[0], qty: 1 }); out = out.filter(function (p) { return p !== small; }); } }
    return out;
  }
  w.esSetMengen = function (o) {
    var pb = +o.pb || 980, tiefe = +o.tiefe || 2000, breite = +o.breite || 0, uk = o.uk === 'metall' ? 'metall' : 'holz';
    var n = Math.max(1, Math.ceil((breite - 2 * EDGE + JOINT - 20) / (pb + JOINT)));   // 20 mm Toleranz (Set-Breiten sind auf 10 mm gerundet)
    var voll = n * pb + (n - 1) * JOINT + 2 * EDGE;          // alle Platten in voller Breite
    var fertig = voll > breite ? breite : voll;              // mit Zuschnitt der letzten Platte = Dachbreite
    var letzte = voll > breite ? pb - (voll - breite) : pb;  // Breite der letzten Platte nach Zuschnitt
    var laenge = up(LEN, tiefe) || LEN[LEN.length - 1];
    var wandL = up(WAND, fertig);
    var profile = n + 1;                                     // (n−1) Mittelprofile + 2 Randprofile
    var schraubenJeProfil = Math.ceil(tiefe / SCHRAUBABSTAND) + 1;
    var schrauben = profile * schraubenJeProfil;
    var tapeMeter = Math.ceil(2 * n * pb / 100) / 10;        // oben + unten je Platte
    var teile = [
      { key: 'platte', name: 'Stegplatten ' + tiefe + ' × ' + pb + ' mm', qty: n, variante: tiefe + 'mm / ' + pb + 'mm' },
      { key: 'mittelprofil', name: 'Mittelprofil Alu-Alu Premium 60 mm', qty: n - 1, variante: laenge + 'mm', hinweis: laenge > tiefe ? 'vor Ort auf ' + tiefe + ' mm kürzen' : '' },
      { key: 'randprofil', name: 'Randprofil Alu-Alu Premium 60 mm', qty: 2, variante: laenge + 'mm', hinweis: laenge > tiefe ? 'vor Ort auf ' + tiefe + ' mm kürzen' : '' },
      { key: 'wandanschluss', name: 'Wandanschlussprofil Alu pressblank', qty: wandL ? 1 : 2, variante: (wandL || WAND[WAND.length - 1]) + 'mm', hinweis: wandL ? '' : 'zwei Längen stoßen' },
      { key: 'uprofil', name: 'U-Profil Abschlussprofil mit Tropfkante', qty: n, variante: pb + 'mm' },
      { key: 'haltewinkel', name: 'Abrutsch- und Haltewinkel Alu', qty: profile, packs: packs(profile, [5, 1]) },
      { key: 'antidust', name: 'Anti-Dust-Tape 43 mm', meter: tapeMeter, packs: packs(Math.ceil(tapeMeter * 10), [150, 75]).map(function (p) { return { size: p.size / 10 + ' Meter', qty: p.qty }; }) },
      { key: 'silikon', name: 'Spezial-Silikon', qty: Math.max(1, Math.ceil(n / 6)) },
      { key: 'schraube_haltewinkel', name: 'Edelstahlschraube 4,2×16 TORX (Haltewinkel)', qty: 2 * profile, packs: packs(2 * profile, [100, 20]) }
    ];
    if (uk === 'holz') {
      teile.push({ key: 'schraube_unten', name: 'Edelstahlschraube 4,5×35 (Unterprofil auf Holz)', qty: schrauben, packs: packs(schrauben, [100, 20]) });
      teile.push({ key: 'schraube_oben', name: 'Bohrschraube 5,5×34 (Oberprofil auf Unterprofil)', qty: schrauben, packs: packs(schrauben, [100, 20]) });
    } else {
      teile.push({ key: 'schraube_unten', name: 'Bohrschraube Edelstahl 4,2×32 (Unterprofil auf Metall)', qty: schrauben, packs: packs(schrauben, [100, 20]) });
      teile.push({ key: 'schraube_oben', name: 'Edelstahlschraube 6,3×32 (Oberteil auf Unterprofil)', qty: schrauben, packs: packs(schrauben, [100, 20]) });
    }
    teile.push({ key: 'alutape', name: 'Alu-Klebeband 60 mm (Sparren, optional)', meter: Math.ceil(profile * tiefe / 100) / 10, optional: true, packs: [{ size: '50 Meter', qty: Math.ceil(profile * tiefe / 50000) }] });
    return { n: n, fertig: fertig, voll: voll, letzte: letzte, laenge: laenge, uk: uk, teile: teile.filter(function (t) { return t.qty !== 0; }) };
  };
})(typeof window !== 'undefined' ? window : globalThis);
