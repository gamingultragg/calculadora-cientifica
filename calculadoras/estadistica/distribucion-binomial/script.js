/**
 * Distribución binomial — P(X = k) = C(n, k) · p^k · (1 − p)^(n − k).
 * Se calcula con logaritmos (log-gamma de Lanczos) para evitar desbordes con n grande.
 */
(function () {
  const G = 7;
  const COEF = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];

  function lgamma(z) {
    if (z < 0.5) return Math.log(Math.PI / Math.sin(Math.PI * z)) - lgamma(1 - z);
    z -= 1;
    let x = COEF[0];
    for (let i = 1; i < G + 2; i++) x += COEF[i] / (z + i);
    const t = z + G + 0.5;
    return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
  }
  const logChoose = (n, k) => lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1);

  function pmf(n, p, k) {
    if (k < 0 || k > n) return 0;
    if (p === 0) return k === 0 ? 1 : 0;
    if (p === 1) return k === n ? 1 : 0;
    return Math.exp(logChoose(n, k) + k * Math.log(p) + (n - k) * Math.log(1 - p));
  }

  function binomial(n, p, k) {
    let cdf = 0;
    for (let i = 0; i <= k; i++) cdf += pmf(n, p, i);
    cdf = Math.min(1, cdf);
    const exact = pmf(n, p, k);
    return { exact, cdf, lt: Math.max(0, cdf - exact), ge: Math.max(0, 1 - (cdf - exact)), gt: Math.max(0, 1 - cdf), mean: n * p, variance: n * p * (1 - p), sd: Math.sqrt(n * p * (1 - p)) };
  }

  if (typeof module !== "undefined") module.exports = { lgamma, pmf, binomial };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("bi-solve")) return;

  CCSimple.mount({
    prefix: "bi",
    compute(v, h) {
      if (!Number.isInteger(v.k)) throw new Error('"Cantidad de éxitos" tiene que ser un número entero.');
      if (v.n > 5000) throw new Error('"Cantidad de ensayos" no puede superar 5.000.');
      if (v.p > 100) throw new Error('"Probabilidad de éxito" tiene que estar entre 0 y 100 %.');
      if (v.k > v.n) throw new Error('"Cantidad de éxitos" no puede ser mayor que los ensayos.');
      const r = binomial(v.n, v.p / 100, v.k);
      const pc = (x) => h.pct(x, 4);
      return {
        label: `P(X = ${h.fmt(v.k, 0)})`, main: pc(r.exact),
        lines: [`P(X ≤ ${v.k}) = <strong>${pc(r.cdf)}</strong> · P(X &lt; ${v.k}) = ${pc(r.lt)}`, `P(X ≥ ${v.k}) = <strong>${pc(r.ge)}</strong> · P(X &gt; ${v.k}) = ${pc(r.gt)}`,
          `Media (n·p) = <strong>${h.fmt(r.mean, 4)}</strong> · Varianza = ${h.fmt(r.variance, 4)} · Desvío estándar = ${h.fmt(r.sd, 4)}`],
      };
    },
  });
})();
