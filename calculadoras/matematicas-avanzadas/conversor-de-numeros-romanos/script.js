/**
 * Conversor de números romanos — de 1 a 3999, en ambos sentidos, con validación estricta.
 */
(function () {
  const TABLE = [[1000, "M"], [900, "CM"], [500, "D"], [400, "CD"], [100, "C"], [90, "XC"], [50, "L"], [40, "XL"], [10, "X"], [9, "IX"], [5, "V"], [4, "IV"], [1, "I"]];
  const VALUES = { I: 1, V: 5, X: 10, L: 50, C: 100, D: 500, M: 1000 };

  function toRoman(n) {
    if (!Number.isInteger(n) || n < 1 || n > 3999) throw new Error("Los números romanos estándar van de 1 a 3999.");
    let out = "";
    for (const [v, s] of TABLE) while (n >= v) { out += s; n -= v; }
    return out;
  }

  function fromRoman(text) {
    const s = String(text).trim().toUpperCase();
    if (!/^[IVXLCDM]+$/.test(s)) throw new Error("Solo se permiten las letras I, V, X, L, C, D y M.");
    let total = 0;
    for (let i = 0; i < s.length; i++) {
      const cur = VALUES[s[i]], next = VALUES[s[i + 1]] || 0;
      total += cur < next ? -cur : cur;
    }
    if (toRoman(total) !== s) throw new Error(`"${s}" no es un número romano bien escrito (se escribiría ${total > 0 && total < 4000 ? toRoman(total) : "de otra forma"}).`);
    return total;
  }

  if (typeof module !== "undefined") module.exports = { toRoman, fromRoman };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("nr-solve")) return;

  CCSimple.mount({
    prefix: "nr",
    compute(v, h) {
      const t = v.value.trim();
      if (/^\d+$/.test(t)) {
        const n = Number(t);
        const r = toRoman(n);
        return { label: `${h.fmt(n, 0)} en números romanos`, main: r, lines: [`Descomposición: ${TABLE.reduce((acc, [val, sym]) => { while (n - acc.used >= val) { acc.used += val; acc.parts.push(`${sym} (${val})`); } return acc; }, { used: 0, parts: [] }).parts.join(" + ")}`] };
      }
      const n = fromRoman(t);
      return { label: `${t.toUpperCase()} en números arábigos`, main: String(n), lines: [`Se suman los valores de las letras y se resta el de las que preceden a una mayor (IV = 5 − 1 = 4).`] };
    },
  });
})();
