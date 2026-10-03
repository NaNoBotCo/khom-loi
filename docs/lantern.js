/* lantern.js — the physics of one khom loi, shared by every drawing on the page (window.L).
   Air is an ideal gas: density ρ = p / (R·T). The lantern rises while the air it holds weighs
   less than the air it pushes aside by more than the paper, the hoop and the fuel weigh.
   The constants marked "tuned" are this page's own choices, set so a one-metre lantern holds about
   140 °C inside while its fuel burns; nobody has published a measured value for a Yi Peng lantern. */
(function () {
  "use strict";
  var P = {
    g: 9.81,          // m/s²
    R: 287.05,        // J/(kg·K), dry air
    p0: 96500,        // Pa, the air pressure Chiang Mai University measured in its lantern lab
    cp: 1005,         // J/(kg·K)
    heat: 42000,      // J per gram of paraffin wax burned
    burn: 0.11,       // g of fuel per second: TU Delft timed 100–330 s burns; 55 g, the legal most, lasts 8 min
    eta: 0.25,        // share of the flame's heat that stays in the air inside (tuned)
    U: 3.7,           // W/(m²·K) lost through the paper and out of the mouth (tuned)
    Cd: 0.9,          // drag of a blunt paper drum
    hoop: 12,         // g, bamboo hoop and wire
    shear: 0.25,      // wind grows with height as (z/10 m)^shear on a calm night
    ignite: 230       // °C, near where paper starts to char and catch
  };

  /* a khom loi of height H (m): a drum, a little wider at the top than at the mouth */
  function shape(H, gsm) {
    var Dm = H * 0.62, Dt = H * 0.72;
    var V = Math.PI / 12 * H * (Dt * Dt + Dt * Dm + Dm * Dm);
    var slant = Math.hypot(H, (Dt - Dm) / 2);
    var A = Math.PI * (Dt + Dm) / 2 * slant + Math.PI * Dt * Dt / 4;
    return { H: H, Dm: Dm, Dt: Dt, V: V, A: A, front: Math.PI * Dt * Dt / 4, paper: A * (gsm == null ? 22 : gsm) };
  }

  function rho(Tk, z) { return P.p0 * Math.exp(-z / 8400) / (P.R * Tk); }

  /* lift and weight in grams for a lantern held still, inside at Ti °C, night at Ta °C */
  function balance(H, gsm, fuel, Ti, Ta) {
    var s = shape(H, gsm), ra = rho(Ta + 273.15, 0), ri = rho(Ti + 273.15, 0);
    return { s: s, ra: ra, ri: ri, lift: s.V * (ra - ri) * 1000, weight: s.paper + P.hoop + fuel };
  }

  /* one flight. o: {H, gsm, fuel (g), Ta (°C), wind (m/s at 10 m), from (deg, where the wind comes from)}
     returns samples every `every` seconds: [t, z, Ti °C, x east m, y north m, fuel g] */
  function fly(o) {
    var s = shape(o.H || 1, o.gsm), T0 = (o.Ta == null ? 22 : o.Ta) + 273.15;
    var fuel = o.fuel == null ? 25 : o.fuel, m0 = (s.paper + P.hoop) / 1000;
    var dir = ((o.from == null ? 45 : o.from) + 180) * Math.PI / 180, ex = Math.sin(dir), ny = Math.cos(dir);
    var wind = o.wind == null ? 2 : o.wind, gust = o.gust || 1;
    var z = 0, v = 0, dT = 0, t = 0, x = 0, y = 0, up = false, hold = null, dt = 0.25, every = o.every || 5;
    var out = [], top = 0, hot = 0, next = 0, burnt = null;
    while (t < 5400) {
      var Ta = T0 - 0.0065 * z, ra = rho(Ta, z), ri = rho(Ta + dT, z);
      var Q = fuel > 0 ? P.burn * P.heat : 0;
      if (fuel > 0) { fuel = Math.max(0, fuel - P.burn * dt); if (fuel === 0) burnt = t; }
      dT += (P.eta * Q - P.U * s.A * dT) / (ri * P.cp * s.V) * dt;
      var m = m0 + fuel / 1000, B = s.V * P.g * (ra - ri), W = m * P.g;
      if (!up) {
        if (B > W * 1.03) { up = true; hold = t; }
        else if (fuel === 0) break;                         // never pulled out of your hands
      }
      if (up) {
        var F = B - W - 0.5 * ra * P.Cd * s.front * v * Math.abs(v);
        v += F / (m + ri * s.V + 0.5 * ra * s.V) * dt;
        z += v * dt;
        if (z <= 0) { z = 0; if (t - hold > 10) { push(); break; } v = Math.max(v, 0); }
        var u = wind * gust * Math.pow(Math.max(z, 2) / 10, P.shear);
        x += u * ex * dt; y += u * ny * dt;
      }
      top = Math.max(top, z); hot = Math.max(hot, dT);
      if (t >= next) { push(); next += every; }
      t += dt;
    }
    function push() { out.push([t, z, Ta - 273.15 + dT, x, y, fuel]); }
    return { pts: out, up: up, hold: hold, top: top, hot: hot + T0 - 273.15, aloft: up ? t - hold : 0,
             burn: burnt, land: [x, y], dist: Math.hypot(x, y), s: s };
  }

  window.L = { P: P, shape: shape, rho: rho, balance: balance, fly: fly };
})();
