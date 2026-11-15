/**
 * Probabilidad básica — casos favorables sobre posibles, dos eventos independientes y "al menos uno" en n intentos.
 *   P = favorables / posibles   ·   P(A y B) = P(A)·P(B)   ·   P(A o B) = P(A) + P(B) − P(A)·P(B)   ·   1 − (1 − p)ⁿ
 */
(function () {
  function simple(fav, tot) {
    if (tot <= 0) throw new Error('"Casos posibles" tiene que ser mayor a 0.');
    if (fav > tot) throw new Error('Los casos favorables no pueden ser más que los posibles.');
    const p = fav / tot;
    return { p, complement: 1 - p, oneIn: p > 0 ? 1 / p : Infinity };
  }
  function twoEvents(pa, pb) {
    return {
      and: pa * pb,
      or: pa + pb - pa * pb,
      none: (1 - pa) * (1 - pb),
      onlyA: pa * (1 - pb),
      onlyB: pb * (1 - pa),
      exactlyOne: pa * (1 - pb) + pb * (1 - pa),
      orExclusive: pa + pb, // si A y B no pueden ocurrir a la vez
    };
  }
  function atLeastOne(p, n) {
    const none = Math.pow(1 - p, n);
    return { none, atLeast: 1 - none, expected: n * p };
  }

  if (typeof module !== "undefined") module.exports = { simple, twoEvents, atLeastOne };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("pb-solve")) return;

  CCSimple.mount({
    prefix: "pb",
    compute(v, h) {
      const pct = (x) => h.pct(x, 4);
      const pr = (x) => h.fmt(x, 6);
      if (v.mode === "simple") {
        const r = simple(v.fav, v.tot);
        return {
          label: "Probabilidad del evento",
          main: pct(r.p),
          lines: [
            `P = ${h.fmt(v.fav, 6)} / ${h.fmt(v.tot, 6)} = <strong>${pr(r.p)}</strong> (${pct(r.p)}).`,
            `Probabilidad de que NO ocurra: ${pr(r.complement)} (${pct(r.complement)}).`,
            r.p > 0 ? `Equivale a 1 posibilidad cada ${h.fmt(r.oneIn, 2)}.` : "Es un evento imposible.",
          ],
        };
      }
      if (v.mode === "dos") {
        if (v.pa > 100 || v.pb > 100) throw new Error("Las probabilidades se ingresan en porcentaje, entre 0 y 100.");
        const a = v.pa / 100;
        const b = v.pb / 100;
        const r = twoEvents(a, b);
        return {
          label: "Que ocurran A y B (independientes)",
          main: pct(r.and),
          lines: [
            `A y B: P(A)·P(B) = ${pr(a)} × ${pr(b)} = <strong>${pct(r.and)}</strong>.`,
            `A o B (al menos uno): P(A) + P(B) − P(A y B) = <strong>${pct(r.or)}</strong>.`,
            `Ninguno de los dos: ${pct(r.none)}.`,
            `Exactamente uno de los dos: ${pct(r.exactlyOne)} (solo A: ${pct(r.onlyA)}, solo B: ${pct(r.onlyB)}).`,
            a + b <= 1 ? `Si A y B fueran excluyentes (no pueden pasar juntos), P(A o B) sería ${pct(r.orExclusive)}.` : null,
          ],
        };
      }
      if (v.p > 100) throw new Error("La probabilidad se ingresa en porcentaje, entre 0 y 100.");
      const r = atLeastOne(v.p / 100, v.n);
      return {
        label: `Al menos un éxito en ${v.n} intento${v.n === 1 ? "" : "s"}`,
        main: pct(r.atLeast),
        lines: [
          `P(al menos uno) = 1 − (1 − p)<sup>n</sup> = 1 − ${pr(1 - v.p / 100)}<sup>${v.n}</sup> = <strong>${pct(r.atLeast)}</strong>.`,
          `Probabilidad de ningún éxito: ${pct(r.none)}.`,
          `Cantidad esperada de éxitos: ${h.fmt(r.expected, 4)}.`,
        ],
      };
    },
  });
})();
