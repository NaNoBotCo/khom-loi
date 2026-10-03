/* app.js — every drawing on the page. The physics lives in lantern.js (window.L). */
(function () {
  "use strict";
  var U = window.UI || {}, TAU = Math.PI * 2, DPR = Math.min(2, window.devicePixelRatio || 1);
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var CARD = document.documentElement.classList.contains("card");
  var $ = function (id) { return document.getElementById(id); };
  var TH = U.lang === "th";

  function fit(cv, h) {
    var w = cv.clientWidth || 600;
    if (typeof h === "function") h = h(w);
    cv.width = Math.round(w * DPR); cv.height = Math.round(h * DPR); cv.style.height = h + "px";
    var c = cv.getContext("2d"); c.setTransform(DPR, 0, 0, DPR, 0, 0);
    return { c: c, w: w, h: h };
  }
  function onVisible(el, fn) {
    if (!("IntersectionObserver" in window)) { fn(true); return; }
    new IntersectionObserver(function (es) { es.forEach(function (e) { fn(e.isIntersecting); }); }, { rootMargin: "120px" }).observe(el);
  }
  function loop(el, draw) {
    var on = false, raf = 0, last = 0;
    function tick(t) { var dt = Math.min(0.05, (t - (last || t)) / 1000); last = t; draw(t / 1000, dt); if (on && !reduce) raf = requestAnimationFrame(tick); }
    onVisible(el, function (v) { on = v; cancelAnimationFrame(raf); last = 0; if (v) raf = requestAnimationFrame(tick); });
    return function () { if (!on || reduce) draw(performance.now() / 1000, 0); };
  }
  function fmt(n, d) { return Number(n).toLocaleString(TH ? "th-TH" : "en-US", { maximumFractionDigits: d == null ? 0 : d, minimumFractionDigits: d == null ? 0 : d }); }
  function val(id) { var e = $(id); return e ? +e.value : 0; }
  function on(ids, fn) { ids.forEach(function (id) { var e = $(id); if (e) e.addEventListener("input", fn); }); }
  function setText(id, s) { var e = $(id); if (e) e.textContent = s; }
  function rnd(seed) { var s = seed >>> 0 || 1; return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }

  /* ---------- drawing a lantern ---------- */
  function lanternPath(c, x, y, s) {          // y = mouth; s = height in px; wider at the top
    var wm = s * 0.31, wt = s * 0.37, bulge = s * 0.05;
    c.beginPath();
    c.moveTo(x - wm, y);
    c.bezierCurveTo(x - wm - bulge, y - s * 0.4, x - wt - bulge, y - s * 0.8, x - wt, y - s);
    c.quadraticCurveTo(x, y - s * 1.06, x + wt, y - s);
    c.bezierCurveTo(x + wt + bulge, y - s * 0.8, x + wm + bulge, y - s * 0.4, x + wm, y);
    c.closePath();
  }
  function drawLantern(c, x, y, s, glow, flick, fade) {
    var a = fade == null ? 1 : fade;
    if (a <= 0) return;
    c.save(); c.globalAlpha = a;
    if (glow > 0.02) {
      var r = s * (1.5 + glow);
      var g = c.createRadialGradient(x, y - s * 0.45, 0, x, y - s * 0.45, r);
      g.addColorStop(0, "rgba(255,190,90," + (0.5 * glow) + ")"); g.addColorStop(1, "rgba(255,140,40,0)");
      c.fillStyle = g; c.fillRect(x - r, y - s * 0.45 - r, r * 2, r * 2);
    }
    lanternPath(c, x, y, s);
    var lg = c.createLinearGradient(x, y, x, y - s);
    var k = Math.max(0, Math.min(1, glow)) * (0.9 + 0.1 * (flick || 0));
    lg.addColorStop(0, "rgb(" + Math.round(150 + 105 * k) + "," + Math.round(70 + 150 * k) + "," + Math.round(40 + 90 * k) + ")");
    lg.addColorStop(1, "rgb(" + Math.round(110 + 120 * k) + "," + Math.round(40 + 90 * k) + "," + Math.round(30 + 40 * k) + ")");
    c.fillStyle = lg; c.fill();
    if (s > 10) {                               // the paper seams
      c.strokeStyle = "rgba(120,40,10," + (0.35 * a) + ")"; c.lineWidth = Math.max(0.6, s / 90);
      for (var i = -1; i <= 1; i++) { c.beginPath(); c.moveTo(x + i * s * 0.15, y); c.lineTo(x + i * s * 0.18, y - s * 1.02); c.stroke(); }
    }
    if (glow > 0.05 && s > 6) {                 // the fuel burning at the mouth
      c.beginPath(); c.ellipse(x, y - s * 0.06, s * 0.07, s * (0.09 + 0.03 * (flick || 0)), 0, 0, TAU);
      c.fillStyle = "rgba(255,250,220," + Math.min(1, glow) + ")"; c.fill();
    }
    c.restore();
  }

  /* ---------- the hero: a Yi Peng sky over the Ping ---------- */
  (function hero() {
    var cv = $("scene"); if (!cv) return;
    var S, stars = [], lans = [], R = rnd(7), clock = 0, spawnAt = 0;
    var profiles = [];
    function flights() {                        // a few flights to borrow paths from, timed in seconds
      [[1, 18], [0.9, 22], [1.1, 28], [1, 32], [0.85, 16]].forEach(function (p) {
        profiles.push(L.fly({ H: p[0], fuel: p[1], wind: 1.6, from: 70, every: 2 }));
      });
    }
    function size() {
      S = fit(cv, function (w) { return CARD ? innerHeight : Math.max(460, Math.min(innerHeight * 0.78, 720)); });
      stars = []; var r = rnd(3);
      for (var i = 0; i < 160; i++) stars.push([r() * S.w, r() * S.h * 0.62, r() * 1.3 + 0.2, r() * TAU]);
    }
    function spawn(x, depth) {
      var p = profiles[Math.floor(R() * profiles.length)];
      lans.push({ x0: x == null ? S.w * (0.08 + 0.84 * R()) : x, d: depth || 0.35 + 0.65 * R(), p: p, t: 0, ph: R() * TAU, sp: 9 + 5 * R() });
    }
    function at(p, t) {                          // the flight sample at time t (s since release)
      var pts = p.pts, i0 = 0;
      var tt = p.hold + t;
      var i = Math.min(pts.length - 1, Math.max(0, Math.floor(tt / 2)));
      for (i0 = i; i0 > 0 && pts[i0][0] > tt; i0--);
      return pts[i0];
    }
    function horizonY() { return S.h * 0.76; }
    function ridge(x) {                          // Doi Suthep and Doi Pui, west of town, as a sum of hills
      var u = x / S.w, y = 0;
      y += 0.20 * Math.exp(-Math.pow((u - 0.16) / 0.13, 2));
      y += 0.15 * Math.exp(-Math.pow((u - 0.33) / 0.10, 2));
      y += 0.07 * Math.exp(-Math.pow((u - 0.50) / 0.12, 2));
      y += 0.04 * Math.sin(u * 23) * Math.exp(-Math.pow((u - 0.25) / 0.25, 2)) * 0.4;
      return horizonY() - y * S.h * 0.75;
    }
    function draw(now, dt) {
      var c = S.c, w = S.w, h = S.h, hy = horizonY();
      clock += dt * 1.0;
      var sky = c.createLinearGradient(0, 0, 0, hy);
      sky.addColorStop(0, "#0b0d2e"); sky.addColorStop(0.55, "#23195a"); sky.addColorStop(1, "#6a2f5e");
      c.fillStyle = sky; c.fillRect(0, 0, w, hy + 2);
      stars.forEach(function (s) { c.fillStyle = "rgba(255,248,230," + (0.35 + 0.35 * Math.sin(now * 1.3 + s[3])) + ")"; c.fillRect(s[0], s[1], s[2], s[2]); });
      // the full moon of the twelfth month
      var mx = w * 0.8, my = h * 0.17, mr = Math.max(18, Math.min(w, h) * 0.055);
      var mg = c.createRadialGradient(mx, my, mr * 0.5, mx, my, mr * 4);
      mg.addColorStop(0, "rgba(255,240,200,.35)"); mg.addColorStop(1, "rgba(255,240,200,0)");
      c.fillStyle = mg; c.fillRect(mx - mr * 4, my - mr * 4, mr * 8, mr * 8);
      c.beginPath(); c.arc(mx, my, mr, 0, TAU); c.fillStyle = "#fff4d6"; c.fill();
      c.fillStyle = "rgba(200,180,140,.25)";
      [[-.3, -.2, .28], [.25, .1, .2], [-.05, .35, .16]].forEach(function (m) { c.beginPath(); c.arc(mx + m[0] * mr, my + m[1] * mr, m[2] * mr, 0, TAU); c.fill(); });
      // the hills
      c.beginPath(); c.moveTo(0, hy);
      for (var x = 0; x <= w; x += 4) c.lineTo(x, ridge(x));
      c.lineTo(w, hy); c.closePath(); c.fillStyle = "#1a1238"; c.fill();
      c.fillStyle = "rgba(255,220,150,.9)"; c.beginPath(); c.arc(w * 0.205, ridge(w * 0.205) + 6, 1.8, 0, TAU); c.fill(); // the wat on the hill
      // lanterns, far ones first
      if (!reduce && clock > spawnAt) { spawn(); spawnAt = clock + 0.35 + R() * 0.9; }
      lans.sort(function (a, b) { return a.d - b.d; });
      var alive = [];
      lans.forEach(function (l) {
        l.t += dt * l.sp;
        var p = at(l.p, l.t), z = p[1], hot = p[2] - 22;
        var sc = l.d * h / 900;
        var x = l.x0 + p[3] * sc * 0.9, y = hy - 8 * l.d - z * sc;
        var s = 26 * l.d * (1 - Math.min(0.5, z / 2400));
        var glow = Math.max(0, Math.min(1, hot / 120));
        var fade = l.t > l.p.aloft - 40 ? Math.max(0, (l.p.aloft - l.t) / 40) : 1;
        if (y < -40 || x > w + 40 || fade <= 0) return;
        drawLantern(c, x, y, s, glow, Math.sin(now * 17 + l.ph), fade);
        alive.push(l);
      });
      lans = alive;
      // the town and the river
      c.fillStyle = "#120c26"; c.fillRect(0, hy, w, h - hy);
      var r2 = rnd(11);
      for (var i = 0; i < w / 6; i++) { var lx = r2() * w, ly = hy + 2 + r2() * 10; c.fillStyle = "rgba(255," + Math.round(170 + r2() * 70) + ",90," + (0.5 + 0.4 * r2()) + ")"; c.fillRect(lx, ly, 1.6, 1.6); }
      var ry = hy + 18;
      var rg = c.createLinearGradient(0, ry, 0, h); rg.addColorStop(0, "#1c1846"); rg.addColorStop(1, "#0a0820");
      c.fillStyle = rg; c.fillRect(0, ry, w, h - ry);
      // reflections: each lantern again, under the water, broken by ripples
      c.save(); c.globalCompositeOperation = "lighter";
      lans.forEach(function (l) {
        var p = at(l.p, l.t), sc = l.d * h / 900, x = l.x0 + p[3] * sc * 0.9, z = p[1];
        var yy = ry + (z * sc + 8 * l.d) * 0.35;
        if (yy > h) return;
        var a = 0.25 * Math.max(0, Math.min(1, (p[2] - 22) / 120));
        for (var k = 0; k < 3; k++) {
          c.fillStyle = "rgba(255,170,80," + a / (k + 1) + ")";
          c.fillRect(x - 6 * l.d + Math.sin(now * 2 + k + yy) * 3, yy + k * 3, 12 * l.d, 1.4);
        }
      });
      var mry = ry + (hy - my) * 0.35;
      for (var k = 0; k < 7; k++) { c.fillStyle = "rgba(255,240,200," + (0.18 - k * 0.02) + ")"; c.fillRect(mx - mr * (1 - k * 0.1) + Math.sin(now * 1.7 + k) * 4, mry + k * 5, mr * 2 * (1 - k * 0.1), 2); }
      c.restore();
    }
    flights(); size();
    // a sky already full when the page opens
    for (var i = 0; i < (CARD ? 70 : 36); i++) { spawn(); lans[lans.length - 1].t = R() * 500; }
    var redraw = loop(cv, draw);
    addEventListener("resize", function () { size(); redraw(); });
    cv.addEventListener("pointerdown", function (e) {
      var r = cv.getBoundingClientRect(); spawn(e.clientX - r.left, 0.9 + 0.1 * Math.random()); redraw();
    });
    if (reduce || CARD) draw(0, 0);
  })();

  /* ---------- why it rises: the air inside and out ---------- */
  (function lift() {
    var cv = $("liftcv"); if (!cv) return;
    var S, dots = [], R = rnd(5);
    function size() { S = fit(cv, function (w) { return Math.min(460, w * 0.95); }); }
    function draw(now, dt) {
      var Ti = val("ti"), Ta = val("ta"), H = val("lh") / 100;
      var b = L.balance(H, 22, 30, Ti, Ta), c = S.c, w = S.w, h = S.h;
      setText("tio", fmt(Ti) + " °C"); setText("tao", fmt(Ta) + " °C"); setText("lho", fmt(H * 100) + " cm");
      setText("rlift", fmt(b.lift) + " g"); setText("rweight", fmt(b.weight) + " g");
      var net = b.lift - b.weight;
      setText("rnet", (net >= 0 ? (TH ? "ลอยขึ้น " : "rises, ") : (TH ? "ยังไม่ลอย " : "stays, ")) + fmt(Math.abs(net)) + " g " + (net >= 0 ? U.spare : U.short));
      setText("rrho", fmt(b.ra, 3) + " / " + fmt(b.ri, 3));
      var warn = $("hotwarn"); if (warn) warn.hidden = Ti < L.P.ignite;
      c.fillStyle = "#0e1030"; c.fillRect(0, 0, w, h);
      // air outside: dots spaced by density; inside: fewer, faster
      var s = h * 0.62 * (0.55 + 0.45 * H / 1.6), x0 = w * 0.36, y0 = h * 0.86;
      var nOut = Math.round(620 * b.ra / 1.2), nIn = Math.min(440, Math.round(nOut * 0.66 * s * s / (w * h) * b.ri / b.ra));
      while (dots.length < 1200) dots.push([R(), R(), R() * TAU]);
      var vOut = Math.sqrt(Ta + 273), vIn = Math.sqrt(Ti + 273);
      lanternPath(c, x0, y0, s); c.fillStyle = "rgba(255,170,80,.13)"; c.fill(); c.strokeStyle = "rgba(255,190,110,.9)"; c.lineWidth = 2; c.stroke();
      var wm = s * 0.31;
      function inside(x, y) { if (y > y0 + 4 || y < y0 - s * 1.08) return false; var half = wm + (s * 0.37 - wm) * (y0 - y) / s + s * 0.06; return Math.abs(x - x0) < half; }
      c.fillStyle = "rgba(150,200,255,.65)";
      for (var i = 0; i < nOut; i++) {
        var d = dots[i], x = (d[0] * w + Math.sin(now * vOut / 9 + d[2]) * 5), y = (d[1] * h + Math.cos(now * vOut / 11 + d[2] * 2) * 5);
        if (!inside(x, y)) c.fillRect(x, y, 2.2, 2.2);
      }
      for (var j = 0; j < nIn; j++) {
        var e = dots[700 + j], u = e[0], v = e[1];
        var yy = y0 - s * 0.05 - v * s * 0.92, half = wm + (s * 0.37 - wm) * (y0 - yy) / s;
        var xx = x0 + (u * 2 - 1) * half * 0.86 + Math.sin(now * vIn / 6 + e[2]) * 4;
        c.fillStyle = "rgba(255,190,110,.9)"; c.fillRect(xx, yy + Math.cos(now * vIn / 7 + e[2]) * 4, 2.4, 2.4);
      }
      drawLantern(c, x0, y0, Math.min(18, s * 0.12), 0.9, Math.sin(now * 15), 1);
      // the scale: lift up, weight down
      var bx = w * 0.78, by = h * 0.5, k = Math.min(1.1, (h * 0.36) / Math.max(150, b.lift, b.weight));
      arrow(c, bx - 16, by, by - b.lift * k, "#7ee08a", U.l_lift);
      arrow(c, bx + 16, by, by + b.weight * k, "#ff8f7a", U.l_weight);
      c.strokeStyle = "rgba(255,255,255,.35)"; c.beginPath(); c.moveTo(bx - 50, by); c.lineTo(bx + 50, by); c.stroke();
    }
    function arrow(c, x, y0, y1, col, lab) {
      c.strokeStyle = col; c.fillStyle = col; c.lineWidth = 7; c.lineCap = "round";
      c.beginPath(); c.moveTo(x, y0); c.lineTo(x, y1); c.stroke();
      var dir = y1 < y0 ? -1 : 1;
      c.beginPath(); c.moveTo(x - 9, y1 - dir * 4); c.lineTo(x + 9, y1 - dir * 4); c.lineTo(x, y1 + dir * 10); c.closePath(); c.fill();
      c.font = "600 14px 'Noto Sans Thai',system-ui,sans-serif"; c.textAlign = "center";
      c.fillText(lab, x, y1 + dir * 26);
    }
    size(); var redraw = loop(cv, draw);
    on(["ti", "ta", "lh"], function () { redraw(); });
    addEventListener("resize", function () { size(); redraw(); });
    draw(0, 0);
  })();

  /* ---------- one flight: height and heat against time ---------- */
  (function flight() {
    var cv = $("flightcv"); if (!cv) return;
    var S;
    function size() { S = fit(cv, function (w) { return Math.min(420, Math.max(300, w * 0.55)); }); }
    function draw() {
      var o = { H: val("fh") / 100, fuel: val("ff"), gsm: val("fg"), Ta: val("fta"), wind: 0 };
      setText("fho", fmt(o.H * 100) + " cm"); setText("ffo", fmt(o.fuel) + " g"); setText("fgo", fmt(o.gsm) + " g/m²"); setText("ftao", fmt(o.Ta) + " °C");
      var r = L.fly(o), c = S.c, w = S.w, h = S.h, pad = { l: 52, r: 52, t: 20, b: 40 };
      c.fillStyle = "#0e1030"; c.fillRect(0, 0, w, h);
      var tmax = Math.max(600, Math.ceil((r.pts.length ? r.pts[r.pts.length - 1][0] : 600) / 300) * 300);
      var zmax = Math.max(200, Math.ceil(r.top / 200) * 200), Tmax = 300;
      var X = function (t) { return pad.l + (w - pad.l - pad.r) * t / tmax; };
      var Yz = function (z) { return h - pad.b - (h - pad.t - pad.b) * z / zmax; };
      var YT = function (T) { return h - pad.b - (h - pad.t - pad.b) * T / Tmax; };
      c.font = "13px 'Noto Sans Thai',system-ui,sans-serif"; c.lineWidth = 1;
      c.strokeStyle = "rgba(255,255,255,.1)"; c.fillStyle = "rgba(230,225,255,.75)";
      for (var m = 0; m <= tmax; m += (tmax > 1800 ? 600 : 300)) { c.beginPath(); c.moveTo(X(m), pad.t); c.lineTo(X(m), h - pad.b); c.stroke(); c.textAlign = "center"; c.fillText(fmt(m / 60) + (TH ? " นาที" : " min"), X(m), h - pad.b + 18); }
      for (var z = 0; z <= zmax; z += zmax / 4) { c.textAlign = "right"; c.fillStyle = "#9fd0ff"; c.fillText(fmt(z) + " m", pad.l - 6, Yz(z) + 4); }
      for (var T = 0; T <= Tmax; T += 100) { c.textAlign = "left"; c.fillStyle = "#ffc27a"; c.fillText(fmt(T) + "°", w - pad.r + 6, YT(T) + 4); }
      // the paper's danger line
      c.setLineDash([6, 5]); c.strokeStyle = "rgba(255,110,110,.7)"; c.beginPath(); c.moveTo(pad.l, YT(L.P.ignite)); c.lineTo(w - pad.r, YT(L.P.ignite)); c.stroke(); c.setLineDash([]);
      c.fillStyle = "rgba(255,140,140,.9)"; c.textAlign = "left"; c.fillText(U.f_char, pad.l + 6, YT(L.P.ignite) - 6);
      if (r.burn) { c.fillStyle = "rgba(255,200,120,.08)"; c.fillRect(X(0), pad.t, X(r.burn) - X(0), h - pad.t - pad.b); }
      function line(ix, Y, col, wd) {
        c.strokeStyle = col; c.lineWidth = wd; c.beginPath();
        r.pts.forEach(function (p, i) { var x = X(p[0]), y = Y(p[ix]); if (i) c.lineTo(x, y); else c.moveTo(x, y); }); c.stroke();
      }
      line(2, YT, "#ffb347", 2.5); line(1, Yz, "#8fd3ff", 3.5);
      if (!r.up) { c.fillStyle = "#ffd2c8"; c.textAlign = "center"; c.font = "600 17px 'Noto Sans Thai',system-ui,sans-serif"; c.fillText(U.f_never, w / 2, h / 2); }
      setText("fhold", r.up ? fmt(r.hold) + (TH ? " วินาที" : " s") : "–");
      setText("ftop", r.up ? fmt(r.top) + " m" : "–");
      setText("faloft", r.up ? fmt(r.aloft / 60, 1) + (TH ? " นาที" : " min") : "–");
      setText("fhot", fmt(r.hot) + " °C");
    }
    size(); draw();
    on(["fh", "ff", "fg", "fta"], draw);
    addEventListener("resize", function () { size(); draw(); });
  })();

  /* ---------- where it comes down: Chiang Mai from above ---------- */
  (function drift() {
    var cv = $("driftcv"); if (!cv) return;
    var S, map = null, site = 0, runs = [], anim = 0, t0 = 0, sites = U.sites || [];
    var LAT0 = 18.79, KX = Math.cos(LAT0 * Math.PI / 180) * 111320, KY = 110540;
    function size() { S = fit(cv, function (w) { return Math.min(620, Math.max(360, w * 0.8)); }); }
    function view() {                           // metres → px around the release site, 9 km a side on a phone
      var s0 = sites[site], AL = 18.767, AG = 98.9628;   // the middle of the runway
      var dx = Math.abs((AG - s0.lng) * KX), dy = Math.abs((AL - s0.lat) * KY);
      var k = Math.min(S.w / Math.max(9000, dx + 7000), S.h / Math.max(9000, dy + 7000));
      var lat = (s0.lat + AL) / 2, lng = (s0.lng + AG) / 2;
      return { cx: S.w / 2, cy: S.h / 2, k: k, lat: lat, lng: lng };
    }
    function P(v, lat, lng) { return [v.cx + (lng - v.lng) * KX * v.k, v.cy - (lat - v.lat) * KY * v.k]; }
    function inPoly(pt, ring) {
      var x = pt[0], y = pt[1], ins = false;
      for (var i = 0, j = ring.length - 1; i < ring.length; j = i++) {
        var xi = ring[i][1], yi = ring[i][0], xj = ring[j][1], yj = ring[j][0];
        if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) ins = !ins;
      }
      return ins;
    }
    function where(lat, lng) {
      var p = [lng, lat], k = "land";
      (map.air || []).forEach(function (poly) { if (inPoly(p, poly[0])) k = "air"; });
      if (k === "land") (map.water || []).forEach(function (poly) { poly.forEach(function (r) { if (inPoly(p, r)) k = "water"; }); });
      return k;
    }
    function base(v) {
      var c = S.c, w = S.w, h = S.h;
      c.fillStyle = "#f6efe2"; c.fillRect(0, 0, w, h);
      if (!map) return;
      c.fillStyle = "#e3d7ee"; (map.air || []).forEach(function (poly) { ring(c, v, poly[0]); c.fill(); });
      c.fillStyle = "#7fc4ef";
      (map.water || []).forEach(function (poly) { c.beginPath(); poly.forEach(function (r) { r.forEach(function (q, i) { var p = P(v, q[0], q[1]); if (i) c.lineTo(p[0], p[1]); else c.moveTo(p[0], p[1]); }); c.closePath(); }); c.fill("evenodd"); });
      c.strokeStyle = "#6b4fa0"; c.lineWidth = 5; c.lineCap = "round";
      (map.runways || []).forEach(function (r) { var a = P(v, r[0], r[1]), b = P(v, r[2], r[3]); c.beginPath(); c.moveTo(a[0], a[1]); c.lineTo(b[0], b[1]); c.stroke(); });
      c.font = "600 13px 'Noto Sans Thai',system-ui,sans-serif"; c.textAlign = "left"; c.fillStyle = "#4a3a6e";
      (U.map_labels || []).forEach(function (m) { var p = P(v, m[0], m[1]); c.fillText(m[2], p[0] + 6, p[1] + 4); });
      // scale bar, 1 km
      var kb = 1000 * v.k; c.fillStyle = "#2a2140"; c.fillRect(14, h - 22, kb, 4); c.fillText(TH ? "1 กม." : "1 km", 14, h - 30);
      // north
      c.textAlign = "center"; c.fillText(TH ? "เหนือ" : "N", w - 22, 24); c.beginPath(); c.moveTo(w - 22, 30); c.lineTo(w - 28, 44); c.lineTo(w - 16, 44); c.closePath(); c.fill();
    }
    function ring(c, v, r) { c.beginPath(); r.forEach(function (q, i) { var p = P(v, q[0], q[1]); if (i) c.lineTo(p[0], p[1]); else c.moveTo(p[0], p[1]); }); c.closePath(); }
    function release() {
      var s0 = sites[site], from = val("wd"), wind = val("ws") / 10, R = rnd(Date.now() % 100000);
      setText("wdo", compass(from)); setText("wso", fmt(wind, 1) + " m/s");
      runs = [];
      for (var i = 0; i < 40; i++) {
        var r = L.fly({ H: 0.85 + 0.35 * R(), fuel: 20 + 35 * R(), wind: wind, gust: 0.8 + 0.4 * R(), from: from + (R() - 0.5) * 40, every: 10 });
        var lat = s0.lat + r.land[1] / KY, lng = s0.lng + r.land[0] / KX;
        r.where = where(lat, lng); r.lat = lat; r.lng = lng;
        runs.push(r);
      }
      var air = runs.filter(function (r) { return r.where === "air"; }).length, wat = runs.filter(function (r) { return r.where === "water"; }).length;
      var ds = runs.map(function (r) { return r.dist; }).sort(function (a, b) { return a - b; });
      setText("dmed", fmt(ds[20] / 1000, 1) + (TH ? " กม." : " km"));
      setText("dfar", fmt(ds[39] / 1000, 1) + (TH ? " กม." : " km"));
      setText("dair", fmt(air) + " / 40"); setText("dwat", fmt(wat) + " / 40");
      t0 = performance.now(); cancelAnimationFrame(anim); tick();
    }
    function tick() {
      var v = view(), c = S.c, el = (performance.now() - t0) / 1000 * 90, done = true;
      base(v);
      runs.forEach(function (r) {
        var pts = r.pts, last = null;
        c.strokeStyle = "rgba(230,110,40,.35)"; c.lineWidth = 1.2; c.beginPath();
        for (var i = 0; i < pts.length; i++) {
          if (pts[i][0] - r.hold > el) { done = false; break; }
          var p = P(v, sites[site].lat + pts[i][4] / KY, sites[site].lng + pts[i][3] / KX);
          if (last) c.lineTo(p[0], p[1]); else c.moveTo(p[0], p[1]); last = p;
        }
        c.stroke();
        if (last) {
          var landed = i >= pts.length;
          if (landed) { c.fillStyle = r.where === "air" ? "#c0262d" : r.where === "water" ? "#1f6fb5" : "#7a3d12"; c.beginPath(); c.arc(last[0], last[1], 3.5, 0, TAU); c.fill(); }
          else { var z = pts[i - 1] ? pts[i - 1][1] : 0; drawLantern(c, last[0], last[1], 8 + z / 150, 0.45 * Math.min(1, (pts[i - 1] ? pts[i - 1][2] - 22 : 0) / 120), 0, 1); }
        }
      });
      var p0 = P(v, sites[site].lat, sites[site].lng);
      c.fillStyle = "#1b1440"; c.beginPath(); c.arc(p0[0], p0[1], 6, 0, TAU); c.fill(); c.fillStyle = "#ffd36b"; c.beginPath(); c.arc(p0[0], p0[1], 3, 0, TAU); c.fill();
      if (!done && !reduce) anim = requestAnimationFrame(tick);
      else if (!done) { el = 1e9; t0 = -1e12; tick(); }
    }
    function compass(d) { var n = U.compass || ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]; return n[Math.round(((d % 360) + 360) % 360 / 45) % 8] + " " + fmt(d) + "°"; }
    document.querySelectorAll("[data-site]").forEach(function (b) {
      b.addEventListener("click", function () {
        site = +b.getAttribute("data-site");
        document.querySelectorAll("[data-site]").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        release();
      });
    });
    on(["wd", "ws"], function () { setText("wdo", compass(val("wd"))); setText("wso", fmt(val("ws") / 10, 1) + " m/s"); });
    var go = $("dgo"); if (go) go.addEventListener("click", release);
    size(); base(view());
    fetch(cv.getAttribute("data-map")).then(function (r) { return r.json(); }).then(function (m) { map = m; onVisible(cv, function (vis) { if (vis && !runs.length) release(); }); }).catch(function () {});
    addEventListener("resize", function () { size(); if (runs.length) { t0 = -1e12; tick(); } else base(view()); });
  })();

  /* ---------- a thousand lanterns: how many are up at once ---------- */
  (function sky() {
    var cv = $("skycv"); if (!cv) return;
    var S, fl = L.fly({ H: 1, fuel: 30, wind: 0, every: 5 }), W = fl.aloft / 60, zmax = fl.top;
    function size() { S = fit(cv, function (w) { return Math.min(520, Math.max(380, w * 0.75)); }); }
    function nice(m) { var p = Math.pow(10, Math.floor(Math.log10(m))), f = m / p; return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * p; }
    function heightAt(age) {                     // metres, from the one-flight curve, age in minutes
      var t = fl.hold + age * 60, pts = fl.pts, i = Math.min(pts.length - 1, Math.max(0, Math.round(t / 5)));
      return pts[i][1];
    }
    function hash(i) { var x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }
    function draw(now) {
      var lam = val("lam"), mins = val("lmin"), c = S.c, w = S.w, h = S.h;
      setText("lamo", fmt(lam) + (TH ? " ดวงต่อนาที" : " a minute")); setText("lmino", fmt(mins) + (TH ? " นาที" : " min"));
      var peak = lam * Math.min(mins, W), tmax = mins + W + 3;
      setText("lpeak", fmt(Math.round(peak))); setText("ltotal", fmt(lam * mins)); setText("lw", fmt(W, 1) + (TH ? " นาที" : " min"));
      var cur = reduce ? Math.min(mins, W) + 0.01 : (now / 9 % 1) * tmax;     // the clock sweeps the night every 9 s
      var skyH = h * 0.56, pad = { l: 52, r: 16, t: skyH + 16, b: 34 };
      var sg = c.createLinearGradient(0, 0, 0, skyH); sg.addColorStop(0, "#0b0d2e"); sg.addColorStop(1, "#4a2a62");
      c.fillStyle = sg; c.fillRect(0, 0, w, skyH);
      c.fillStyle = "#0e1030"; c.fillRect(0, skyH, w, h - skyH);
      var total = Math.round(lam * mins), shown = 0, up = 0;
      for (var i = 0; i < total; i++) {
        var age = cur - i / lam;
        if (age < 0 || age > W) continue;
        up++;
        if (shown > 900) continue;
        var z = heightAt(age), x = 8 + hash(i) * (w - 16) + age * 3, y = skyH - 6 - z / zmax * (skyH - 18);
        var hot = age * 60 < (fl.burn || 0) - fl.hold + 60;
        c.fillStyle = hot ? "rgba(255,190,90,.9)" : "rgba(150,110,90,.6)"; c.fillRect(x, y, 2.6, 3.4); shown++;
      }
      c.fillStyle = "#fff"; c.font = "600 15px 'Noto Sans Thai',system-ui,sans-serif"; c.textAlign = "left";
      c.fillText((TH ? "นาทีที่ " : "minute ") + fmt(cur) + " · " + fmt(up) + (TH ? " ดวงบนฟ้า" : " up"), 12, 22);
      var ymax = nice(Math.max(10, peak * 1.15)), X = function (t) { return pad.l + (w - pad.l - pad.r) * t / tmax; }, Y = function (n) { return h - pad.b - (h - pad.t - pad.b) * n / ymax; };
      c.font = "12px 'Noto Sans Thai',system-ui,sans-serif"; c.fillStyle = "rgba(230,225,255,.75)";
      c.textAlign = "right"; for (var n = 0; n <= ymax; n += ymax / 2) c.fillText(fmt(n), pad.l - 6, Y(n) + 4);
      c.textAlign = "center"; var st = tmax > 80 ? 20 : 10; for (var t = 0; t <= tmax - st / 2; t += st) c.fillText(fmt(t) + (t === 0 ? (TH ? " นาที" : " min") : ""), X(t), h - pad.b + 16);
      c.beginPath(); c.moveTo(X(0), Y(0));
      for (var tt = 0; tt <= tmax; tt += tmax / 300) c.lineTo(X(tt), Y(lam * Math.max(0, Math.min(tt, mins) - Math.max(0, tt - W))));
      c.lineTo(X(tmax), Y(0)); c.closePath();
      var g = c.createLinearGradient(0, pad.t, 0, h - pad.b); g.addColorStop(0, "rgba(255,180,80,.85)"); g.addColorStop(1, "rgba(255,120,60,.2)");
      c.fillStyle = g; c.fill();
      c.setLineDash([5, 5]); c.strokeStyle = "rgba(255,255,255,.5)"; c.beginPath(); c.moveTo(pad.l, Y(peak)); c.lineTo(w - pad.r, Y(peak)); c.stroke(); c.setLineDash([]);
      c.fillStyle = "#fff"; c.textAlign = "left"; c.fillText("λ × W = " + fmt(Math.round(peak)), pad.l + 8, Y(peak) - 6);
      c.strokeStyle = "#fff"; c.lineWidth = 1.5; c.beginPath(); c.moveTo(X(cur), pad.t - 6); c.lineTo(X(cur), h - pad.b); c.stroke();
    }
    size(); var redraw = loop(cv, draw); on(["lam", "lmin"], function () { redraw(); });
    addEventListener("resize", function () { size(); redraw(); });
    draw(0);
  })();
})();
