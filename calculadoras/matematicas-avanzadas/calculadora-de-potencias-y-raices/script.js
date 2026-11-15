/**
 * Potencias y raíces — aⁿ, raíz n-ésima, comprobación de potencias perfectas y simplificación de radicales
 * (por ejemplo √72 = 6√2). La simplificación factoriza el número, así que trabaja con enteros hasta 10¹².
 */
(function () {
  function power(a, n) {
    if (a === 0 && n < 0) throw new Error("0 elevado a un exponente negativo no está definido (sería dividir por 0).");
    const r = Math.pow(a, n);
    if (Number.isNaN(r)) throw new Error("Con una base negativa el exponente tiene que ser entero: el resultado no es un número real.");
    if (!Number.isFinite(r)) throw new Error("El resultado es demasiado grande para mostrarlo.");
    return r;
  }

  function root(x, n) {
    if (!Number.isInteger(n) || n < 2) throw new Error('"Índice" tiene que ser un entero de 2 o más.');
    if (x < 0 && n % 2 === 0) throw new Error("No existe la raíz de índice par de un número negativo en los números reales.");
    const r = x < 0 ? -Math.pow(-x, 1 / n) : Math.pow(x, 1 / n);
    const rounded = Math.round(r);
    return Math.abs(Math.pow(rounded, n) - x) < 1e-9 * Math.max(1, Math.abs(x)) ? rounded : r; // devuelve el entero exacto si es potencia perfecta
  }

  // Saca de la raíz todo lo que se pueda: ⁿ√x = out · ⁿ√inside. Solo para enteros positivos.
  function simplify(x, n) {
    if (!Number.isInteger(x) || x < 1 || x > 1e12) return null;
    let rest = x;
    let out = 1;
    let inside = 1;
    for (let p = 2; p * p <= rest; p++) {
      if (rest % p !== 0) continue;
      let e = 0;
      while (rest % p === 0) {
        rest /= p;
        e++;
      }
      out *= Math.pow(p, Math.floor(e / n));
      inside *= Math.pow(p, e % n);
    }
    if (rest > 1) inside *= rest; // factor primo restante, con exponente 1 (< n)
    return { out, inside };
  }

  if (typeof module !== "undefined") module.exports = { power, root, simplify };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("pr-solve")) return;

  const show = (h, n) => (n !== 0 && (Math.abs(n) >= 1e12 || Math.abs(n) < 1e-6) ? n.toExponential(6).replace(".", ",").replace("e+", " × 10^").replace("e-", " × 10^−") : h.fmt(n, 8));

  CCSimple.mount({
    prefix: "pr",
    compute(v, h) {
      if (v.mode === "pot") {
        const r = power(v.a, v.n);
        const lines = [`${show(h, v.a)}<sup>${show(h, v.n)}</sup> = <strong>${show(h, r)}</strong>.`];
        if (v.n < 0 && v.a !== 0) lines.push(`Un exponente negativo es la inversa: ${show(h, v.a)}<sup>${show(h, v.n)}</sup> = 1 / ${show(h, v.a)}<sup>${show(h, -v.n)}</sup>.`);
        if (Number.isInteger(v.n) === false && v.a > 0) lines.push("Un exponente fraccionario es una raíz: a<sup>p/q</sup> = <sup>q</sup>√(a<sup>p</sup>).");
        lines.push(`Del mismo número: cuadrado = ${show(h, v.a * v.a)} · cubo = ${show(h, v.a * v.a * v.a)}` + (v.a >= 0 ? ` · raíz cuadrada = ${show(h, Math.sqrt(v.a))} · raíz cúbica = ${show(h, Math.cbrt(v.a))}.` : ` · raíz cúbica = ${show(h, Math.cbrt(v.a))}.`));
        return { label: "Potencia", main: show(h, r), lines };
      }
      if (!Number.isInteger(v.k)) throw new Error('"Índice" tiene que ser un entero de 2 o más.');
      const r = root(v.a, v.k);
      const name = v.k === 2 ? "√" : `<sup>${v.k}</sup>√`;
      const lines = [`${name}${show(h, v.a)} = <strong>${show(h, r)}</strong>.`];
      const exact = Number.isInteger(r) && Math.abs(Math.pow(r, v.k) - v.a) < 1e-9 * Math.max(1, Math.abs(v.a));
      if (exact) lines.push(`Es una raíz exacta: ${show(h, v.a)} es una potencia perfecta (${show(h, r)}<sup>${v.k}</sup> = ${show(h, v.a)}).`);
      else {
        const s = simplify(Math.abs(v.a), v.k);
        if (s && s.out > 1) lines.push(`Simplificada: ${name}${show(h, v.a)} = ${v.a < 0 ? "−" : ""}<strong>${s.out}${v.k === 2 ? "√" : `<sup>${v.k}</sup>√`}${s.inside}</strong>.`);
        else if (s) lines.push("No se puede simplificar: el radicando no tiene factores que sean potencias perfectas.");
      }
      lines.push(`Comprobación: ${show(h, r)}<sup>${v.k}</sup> = ${show(h, Math.pow(r, v.k))}.`);
      return { label: v.k === 2 ? "Raíz cuadrada" : `Raíz de índice ${v.k}`, main: show(h, r), lines };
    },
  });
})();
