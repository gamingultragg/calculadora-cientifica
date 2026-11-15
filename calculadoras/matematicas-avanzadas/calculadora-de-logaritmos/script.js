/**
 * Logaritmos — log_b(x) = ln(x) / ln(b) y su operación inversa b^y.
 * Casos particulares: log₁₀ (decimal), ln (natural, base e) y log₂ (binario).
 */
(function () {
  function logBase(base, x) {
    if (!(base > 0) || base === 1) throw new Error("La base tiene que ser un número positivo distinto de 1.");
    if (!(x > 0)) throw new Error('"Número" tiene que ser mayor a 0: el logaritmo de 0 o de un negativo no existe en los reales.');
    if (base === 10) return Math.log10(x);
    if (base === 2) return Math.log2(x);
    if (base === Math.E) return Math.log(x);
    return Math.log(x) / Math.log(base);
  }
  function power(base, y) {
    if (!(base > 0)) throw new Error('"Base" tiene que ser mayor a 0.');
    return Math.pow(base, y);
  }

  if (typeof module !== "undefined") module.exports = { logBase, power };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("lo-solve")) return;

  // Número legible: decimal con hasta 6 decimales, o notación científica si es muy grande o muy chico.
  const show = (h, n) => {
    if (n !== 0 && (Math.abs(n) >= 1e12 || Math.abs(n) < 1e-6)) return n.toExponential(6).replace(".", ",").replace("e+", " × 10^").replace("e-", " × 10^−").replace("e", " × 10^");
    return h.fmt(n, 6);
  };

  CCSimple.mount({
    prefix: "lo",
    compute(v, h) {
      const isE = Math.abs(v.base - Math.E) < 1e-9;
      const b = isE ? "e" : show(h, v.base);
      if (v.mode === "log") {
        const r = logBase(v.base, v.x);
        const name = isE ? "ln" : `log<sub>${b}</sub>`;
        const lines = [
          `${name}(${show(h, v.x)}) = ln(${show(h, v.x)}) / ln(${b}) = <strong>${show(h, r)}</strong>.`,
          `Comprobación: ${b}<sup>${show(h, r)}</sup> = ${show(h, power(v.base, r))}.`,
          `Del mismo número: log₁₀ = ${show(h, Math.log10(v.x))} · ln = ${show(h, Math.log(v.x))} · log₂ = ${show(h, Math.log2(v.x))}.`,
        ];
        return { label: isE ? "Logaritmo natural (base e)" : `Logaritmo en base ${b}`, main: show(h, r), lines };
      }
      if (v.y > 1e6 || v.y < -1e6) throw new Error('"Exponente" es demasiado grande: usá un valor entre −1.000.000 y 1.000.000.');
      const p = power(v.base, v.y);
      if (!Number.isFinite(p)) throw new Error("El resultado es demasiado grande para mostrarlo. Probá con un exponente menor.");
      const lines = [
        `${b}<sup>${show(h, v.y)}</sup> = <strong>${show(h, p)}</strong>.`,
        p > 0 ? `Equivale a decir que ${isE ? "ln" : `log<sub>${b}</sub>`}(${show(h, p)}) = ${show(h, v.y)}.` : null,
      ];
      return { label: "Potencia", main: show(h, p), lines };
    },
  });
})();
