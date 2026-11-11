/**
 * Tamaño de muestra para estimar una proporción: n₀ = z² · p · (1 − p) / e²,
 * con corrección por población finita n = n₀ / (1 + (n₀ − 1)/N).
 */
(function () {
  const Z = { 90: 1.645, 95: 1.96, 99: 2.576 };

  function sampleSize(level, errorPct, pPct, population) {
    const z = Z[level];
    if (!z) throw new Error("Nivel de confianza no soportado.");
    const e = errorPct / 100, p = pPct / 100;
    const n0 = (z * z * p * (1 - p)) / (e * e);
    const n = population ? n0 / (1 + (n0 - 1) / population) : n0;
    return { z, n0: Math.ceil(n0 - 1e-9), n: Math.ceil(n - 1e-9) };
  }

  if (typeof module !== "undefined") module.exports = { sampleSize };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("tm-solve")) return;

  CCSimple.mount({
    prefix: "tm",
    compute(v, h) {
      if (v.error >= 50) throw new Error('"Margen de error" tiene que ser menor al 50 %.');
      if (v.p > 100) throw new Error('"Proporción esperada" tiene que estar entre 0 y 100 %.');
      const r = sampleSize(Number(v.level), v.error, v.p, v.population);
      return {
        label: "Tamaño de muestra necesario", main: `${h.fmt(r.n, 0)} personas`,
        lines: [`Con z = ${h.fmt(r.z, 3)}, proporción esperada ${h.fmt(v.p, 1)} % y margen de error ±${h.fmt(v.error, 2)} %: n₀ = <strong>${h.fmt(r.n0, 0)}</strong>.`,
          v.population ? `Con una población de ${h.fmt(v.population, 0)}, la corrección por población finita reduce la muestra a <strong>${h.fmt(r.n, 0)}</strong>.` : "Sin dato de población se asume una población muy grande (infinita).",
          "Si no conocés la proporción, usá 50 %: es el caso más exigente y da la muestra más grande."],
      };
    },
  });
})();
