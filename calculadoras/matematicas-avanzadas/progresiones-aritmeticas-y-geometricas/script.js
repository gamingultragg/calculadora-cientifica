/**
 * Progresiones aritméticas y geométricas — término n-ésimo y suma de los primeros n términos.
 *   aritmética:  aₙ = a₁ + (n − 1)·d     Sₙ = n·(a₁ + aₙ) / 2
 *   geométrica:  aₙ = a₁·r^(n−1)         Sₙ = a₁·(rⁿ − 1)/(r − 1)   (r ≠ 1)    S∞ = a₁/(1 − r) si |r| < 1
 */
(function () {
  function arithmetic(a1, d, n) {
    const an = a1 + (n - 1) * d;
    return { an, sn: (n * (a1 + an)) / 2 };
  }
  function geometric(a1, r, n) {
    const an = a1 * Math.pow(r, n - 1);
    const sn = r === 1 ? a1 * n : (a1 * (Math.pow(r, n) - 1)) / (r - 1);
    return { an, sn, infinite: Math.abs(r) < 1 ? a1 / (1 - r) : null };
  }

  if (typeof module !== "undefined") module.exports = { arithmetic, geometric };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("pg-solve")) return;

  CCSimple.mount({
    prefix: "pg",
    compute(v, h) {
      if (v.n > 1e6) throw new Error('"Cantidad de términos" no puede superar 1.000.000.');
      const f = (x) => (Math.abs(x) >= 1e15 || (x !== 0 && Math.abs(x) < 1e-6) ? x.toExponential(4).replace(".", ",") : h.fmt(x, 6));
      if (v.mode === "ar") {
        const r = arithmetic(v.a1, v.d, v.n);
        return { label: `Término a${v.n}`, main: f(r.an), lines: [`Suma de los primeros ${h.fmt(v.n, 0)} términos: <strong>${f(r.sn)}</strong>`, `aₙ = a₁ + (n − 1)·d = ${f(v.a1)} + ${h.fmt(v.n - 1, 0)} × ${f(v.d)}`] };
      }
      const r = geometric(v.a1, v.r, v.n);
      if (!Number.isFinite(r.an) || !Number.isFinite(r.sn)) throw new Error("El resultado es demasiado grande para mostrarlo: probá con menos términos o una razón más chica.");
      return { label: `Término a${v.n}`, main: f(r.an), lines: [`Suma de los primeros ${h.fmt(v.n, 0)} términos: <strong>${f(r.sn)}</strong>`, r.infinite !== null ? `Como |r| < 1, la suma de infinitos términos converge a <strong>${f(r.infinite)}</strong>.` : "Con |r| ≥ 1 la suma de infinitos términos no converge.", `aₙ = a₁·r^(n−1) = ${f(v.a1)} × ${f(v.r)}^${h.fmt(v.n - 1, 0)}`] };
    },
  });
})();
