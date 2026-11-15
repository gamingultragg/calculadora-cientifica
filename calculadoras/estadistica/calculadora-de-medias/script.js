/**
 * Medias — aritmética, geométrica, armónica y cuadrática de una lista de números.
 *   AM = Σx/n   ·   GM = (Πx)^(1/n)   ·   HM = n / Σ(1/x)   ·   QM = √(Σx²/n)   —   Para números positivos: HM ≤ GM ≤ AM ≤ QM.
 */
(function () {
  function normalizeNumber(value) {
    let str = String(value).trim();
    if (str.includes(",")) str = str.replace(/\./g, "").replace(",", ".");
    else if (/^-?[1-9]\d{0,2}(\.\d{3})+$/.test(str)) str = str.replace(/\./g, "");
    return str;
  }

  // Separadores: espacios, saltos de línea o punto y coma. La coma es el separador decimal ("1, 2, 3" también se acepta).
  function parseList(text) {
    const tokens = String(text).replace(/,\s+/g, " ").split(/[\s;]+/).filter(Boolean);
    const out = tokens.map((t) => Number(normalizeNumber(t.replace(/,$/, ""))));
    if (out.length < 2) throw new Error("Ingresá al menos dos números.");
    if (out.length > 1000) throw new Error("Ingresá hasta 1.000 números.");
    if (out.some((n) => !Number.isFinite(n))) throw new Error("Hay un valor que no es un número válido. Separá los números con espacios o punto y coma.");
    return out;
  }

  function means(list) {
    const n = list.length;
    const positive = list.every((x) => x > 0);
    return {
      n,
      arithmetic: list.reduce((s, x) => s + x, 0) / n,
      geometric: positive ? Math.exp(list.reduce((s, x) => s + Math.log(x), 0) / n) : null,
      harmonic: positive ? n / list.reduce((s, x) => s + 1 / x, 0) : null,
      quadratic: Math.sqrt(list.reduce((s, x) => s + x * x, 0) / n),
    };
  }

  if (typeof module !== "undefined") module.exports = { parseList, means };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("md-solve")) return;

  CCSimple.mount({
    prefix: "md",
    compute(v, h) {
      const list = parseList(v.list);
      const m = means(list);
      const f = (x) => h.fmt(x, 6);
      const lines = [
        `Cantidad de datos: ${m.n}.`,
        `Media aritmética: <strong>${f(m.arithmetic)}</strong> (suma ÷ cantidad).`,
        m.geometric !== null ? `Media geométrica: <strong>${f(m.geometric)}</strong> (raíz n-ésima del producto).` : "Media geométrica: no se define (hay valores iguales o menores que 0).",
        m.harmonic !== null ? `Media armónica: <strong>${f(m.harmonic)}</strong> (n ÷ suma de las inversas).` : "Media armónica: no se define (hay valores iguales o menores que 0).",
        `Media cuadrática: ${f(m.quadratic)} (raíz del promedio de los cuadrados).`,
        m.geometric !== null ? "Para números positivos siempre se cumple: armónica ≤ geométrica ≤ aritmética ≤ cuadrática (y son iguales solo si todos los datos son iguales)." : null,
      ];
      return { label: "Media aritmética", main: f(m.arithmetic), lines };
    },
  });
})();
