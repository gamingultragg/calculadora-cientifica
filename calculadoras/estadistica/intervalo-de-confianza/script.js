/**
 * Intervalo de confianza para la media: x̄ ± c · s/√n.
 * c es t de Student (n ≤ 30 con desvío muestral) o z (normal) en los demás casos.
 */
(function () {
  const Z = { 90: 1.645, 95: 1.96, 99: 2.576 };
  // valores críticos bilaterales de t para df = 1…30
  const T = {
    90: [6.314, 2.92, 2.353, 2.132, 2.015, 1.943, 1.895, 1.86, 1.833, 1.812, 1.796, 1.782, 1.771, 1.761, 1.753, 1.746, 1.74, 1.734, 1.729, 1.725, 1.721, 1.717, 1.714, 1.711, 1.708, 1.706, 1.703, 1.701, 1.699, 1.697],
    95: [12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.16, 2.145, 2.131, 2.12, 2.11, 2.101, 2.093, 2.086, 2.08, 2.074, 2.069, 2.064, 2.06, 2.056, 2.052, 2.048, 2.045, 2.042],
    99: [63.657, 9.925, 5.841, 4.604, 4.032, 3.707, 3.499, 3.355, 3.25, 3.169, 3.106, 3.055, 3.012, 2.977, 2.947, 2.921, 2.898, 2.878, 2.861, 2.845, 2.831, 2.819, 2.807, 2.797, 2.787, 2.779, 2.771, 2.763, 2.756, 2.75],
  };

  function critical(level, n, sampleSd) {
    if (!(level in Z)) throw new Error("Nivel de confianza no soportado.");
    if (sampleSd && n <= 30) {
      if (n < 2) throw new Error("Con desvío muestral hacen falta al menos 2 datos.");
      return { value: T[level][n - 2], kind: `t de Student (${n - 1} grados de libertad)` };
    }
    return { value: Z[level], kind: "z (normal)" };
  }

  function interval(mean, sd, n, level, sampleSd) {
    const c = critical(level, n, sampleSd);
    const se = sd / Math.sqrt(n);
    const margin = c.value * se;
    return { margin, lower: mean - margin, upper: mean + margin, se, critical: c };
  }

  if (typeof module !== "undefined") module.exports = { critical, interval };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("ic-solve")) return;

  CCSimple.mount({
    prefix: "ic",
    compute(v, h) {
      const r = interval(v.mean, v.sd, v.n, Number(v.level), v.sdtype === "muestral");
      const f = (x) => h.fmt(x, 4);
      return {
        label: `Intervalo de confianza del ${v.level} %`, main: `[${f(r.lower)} ; ${f(r.upper)}]`,
        lines: [`Margen de error: <strong>±${f(r.margin)}</strong> (error estándar ${f(r.se)} × valor crítico ${f(r.critical.value)})`, `Distribución usada: ${r.critical.kind}.`,
          `Interpretación: con ${v.level} % de confianza, la media verdadera de la población está entre ${f(r.lower)} y ${f(r.upper)}.`],
      };
    },
  });
})();
