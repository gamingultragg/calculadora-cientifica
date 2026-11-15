/**
 * Movimiento circular uniforme (MCU) — período, frecuencia, velocidad angular y lineal, aceleración centrípeta.
 *   ω = 2π/T = 2πf   ·   v = ω·r   ·   a = ω²·r = v²/r   ·   1 rpm = 1/60 Hz
 */
(function () {
  const TWO_PI = 2 * Math.PI;

  // Dato conocido ("T", "f", "rpm", "v", "w") → todas las magnitudes del movimiento.
  function circular(r, known, value) {
    const omega = { T: () => TWO_PI / value, f: () => TWO_PI * value, rpm: () => (TWO_PI * value) / 60, v: () => value / r, w: () => value }[known]();
    const f = omega / TWO_PI;
    return { omega, T: 1 / f, f, rpm: f * 60, v: omega * r, a: omega * omega * r };
  }

  if (typeof module !== "undefined") module.exports = { circular };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("mc-solve")) return;

  CCSimple.mount({
    prefix: "mc",
    compute(v, h) {
      const f = (x, d = 4) => h.fmt(x, d);
      const known = v.mode;
      const value = { T: v.T, f: v.f, rpm: v.rpm, v: v.v, w: v.w }[known];
      const r = circular(v.r, known, value);
      const lines = [
        `Período: T = ${f(r.T)} s (tiempo de una vuelta).`,
        `Frecuencia: f = ${f(r.f)} Hz = ${f(r.rpm)} rpm (vueltas por minuto).`,
        `Velocidad angular: ω = 2π/T = ${f(r.omega)} rad/s.`,
        `Velocidad lineal (tangencial): v = ω·r = ${f(r.v)} m/s = ${f(r.v * 3.6)} km/h.`,
        `Aceleración centrípeta: a = ω²·r = v²/r = <strong>${f(r.a)} m/s²</strong> (apunta siempre al centro).`,
      ];
      return { label: "Aceleración centrípeta", main: `${f(r.a)} m/s²`, lines };
    },
  });
})();
