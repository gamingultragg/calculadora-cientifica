/**
 * Péndulo simple — T = 2π·√(L/g) para oscilaciones pequeñas, con despeje de la longitud y de la gravedad.
 * Corrección por amplitud: T ≈ T₀·(1 + θ₀²/16 + 11·θ₀⁴/3072), con θ₀ en radianes.
 */
(function () {
  const period = (L, g) => 2 * Math.PI * Math.sqrt(L / g);
  const length = (T, g) => (g * T * T) / (4 * Math.PI * Math.PI);
  const gravity = (L, T) => (4 * Math.PI * Math.PI * L) / (T * T);
  const amplitudeFactor = (theta0Rad) => 1 + (theta0Rad * theta0Rad) / 16 + (11 * Math.pow(theta0Rad, 4)) / 3072;

  if (typeof module !== "undefined") module.exports = { period, length, gravity, amplitudeFactor };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("pd-solve")) return;

  CCSimple.mount({
    prefix: "pd",
    compute(v, h) {
      const f = (x, d = 4) => h.fmt(x, d);
      let L = v.L;
      let T = v.T;
      let g = v.g;
      let label;
      let main;
      if (v.mode === "T") {
        T = period(L, g);
        label = "Período (T)";
        main = `${f(T)} s`;
      } else if (v.mode === "L") {
        L = length(T, g);
        label = "Longitud (L)";
        main = `${f(L)} m`;
      } else {
        g = gravity(L, T);
        label = "Gravedad (g)";
        main = `${f(g)} m/s²`;
      }
      const lines = [
        `T = 2π·√(L/g) = 2π·√(${f(L)} / ${f(g)}) = ${f(T)} s.`,
        `Frecuencia: f = 1/T = ${f(1 / T)} Hz (${f(60 / T, 2)} oscilaciones completas por minuto).`,
      ];
      if (v.mode === "T" && v.angle > 0) {
        if (v.angle >= 90) throw new Error('"Amplitud" tiene que ser menor a 90°.');
        const k = amplitudeFactor((v.angle * Math.PI) / 180);
        lines.push(`Con una amplitud de ${f(v.angle, 2)}° el período real es un ${f((k - 1) * 100, 2)} % mayor: ${f(T * k)} s.`);
      } else if (v.mode === "T") {
        lines.push("Vale para amplitudes chicas (menos de unos 15°). Para ángulos mayores, ingresá la amplitud y se aplica una corrección.");
      }
      lines.push("La masa del péndulo no influye en el período.");
      return { label, main, lines };
    },
  });
})();
