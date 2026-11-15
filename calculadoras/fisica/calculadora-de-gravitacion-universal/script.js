/**
 * Gravitación universal — F = G·m₁·m₂ / r², aceleración de la gravedad g = G·M / r² y movimiento orbital circular.
 * G = 6,6743 × 10⁻¹¹ N·m²/kg². Velocidad orbital v = √(G·M/r), de escape √(2·G·M/r) y período T = 2π·√(r³/(G·M)).
 */
(function () {
  const G = 6.6743e-11;
  const force = (m1, m2, r) => (G * m1 * m2) / (r * r);
  const surfaceGravity = (M, r) => (G * M) / (r * r);
  const orbitalSpeed = (M, r) => Math.sqrt((G * M) / r);
  const escapeSpeed = (M, r) => Math.sqrt((2 * G * M) / r);
  const orbitPeriod = (M, r) => 2 * Math.PI * Math.sqrt((r * r * r) / (G * M));

  if (typeof module !== "undefined") module.exports = { G, force, surfaceGravity, orbitalSpeed, escapeSpeed, orbitPeriod };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("gv-solve")) return;

  const show = (h, n, d = 4) => {
    if (n === 0) return "0";
    return Math.abs(n) >= 1e6 || Math.abs(n) < 1e-3 ? n.toExponential(4).replace(".", ",").replace("e+", " × 10^").replace("e-", " × 10^−") : h.fmt(n, d);
  };
  const time = (h, s) => (s >= 86400 ? `${h.fmt(s / 86400, 2)} días` : s >= 7200 ? `${h.fmt(s / 3600, 2)} h` : s >= 120 ? `${h.fmt(s / 60, 2)} min` : `${h.fmt(s, 2)} s`);

  CCSimple.mount({
    prefix: "gv",
    compute(v, h) {
      const r = v.r * (v.ru === "km" ? 1000 : 1);
      if (v.mode === "f") {
        const F = force(v.m1, v.m2, r);
        return { label: "Fuerza gravitatoria", main: `${show(h, F)} N`, lines: [`F = G·m₁·m₂ / r² = ${show(h, G)} × ${show(h, v.m1)} × ${show(h, v.m2)} / ${show(h, r)}² = <strong>${show(h, F)} N</strong>.`, "Es siempre atractiva y actúa con igual intensidad sobre los dos cuerpos."] };
      }
      if (v.mode === "g") {
        const g = surfaceGravity(v.M, r);
        return {
          label: "Aceleración de la gravedad",
          main: `${show(h, g, 3)} m/s²`,
          lines: [`g = G·M / r² = ${show(h, G)} × ${show(h, v.M)} / ${show(h, r)}² = <strong>${show(h, g, 3)} m/s²</strong>.`, `Es ${h.fmt(g / 9.80665, 3)} veces la gravedad terrestre normal (9,80665 m/s²).`, `Velocidad de escape a esa distancia: ${show(h, escapeSpeed(v.M, r), 1)} m/s (${h.fmt(escapeSpeed(v.M, r) / 1000, 2)} km/s).`] };
      }
      const vel = orbitalSpeed(v.M, r);
      const T = orbitPeriod(v.M, r);
      return {
        label: "Velocidad orbital",
        main: `${show(h, vel, 1)} m/s`,
        lines: [`Velocidad orbital circular: v = √(G·M / r) = <strong>${show(h, vel, 1)} m/s</strong> (${h.fmt(vel * 3.6, 0)} km/h).`, `Período orbital: T = 2π·√(r³ / (G·M)) = <strong>${time(h, T)}</strong>.`, `Velocidad de escape: ${show(h, escapeSpeed(v.M, r), 1)} m/s (√2 veces la orbital).`, "Supone una órbita circular y un cuerpo central mucho más masivo que el que orbita."] };
    },
  });
})();
