/**
 * Código de colores de resistencias — 4 y 5 bandas.
 */
(function () {
  const DIGIT = { negro: 0, marron: 1, rojo: 2, naranja: 3, amarillo: 4, verde: 5, azul: 6, violeta: 7, gris: 8, blanco: 9 };
  const MULT = { ...Object.fromEntries(Object.entries(DIGIT).map(([k, v]) => [k, Math.pow(10, v)])), dorado: 0.1, plateado: 0.01 };
  const TOL = { marron: 1, rojo: 2, verde: 0.5, azul: 0.25, violeta: 0.1, gris: 0.05, dorado: 5, plateado: 10 };

  function resistorValue(digits, multiplier, tolerance) {
    const base = digits.reduce((acc, c) => acc * 10 + DIGIT[c], 0);
    const ohms = base * MULT[multiplier];
    return { ohms, tolerance: TOL[tolerance], min: ohms * (1 - TOL[tolerance] / 100), max: ohms * (1 + TOL[tolerance] / 100) };
  }

  function format(ohms) {
    const trim = (x) => String(Math.round(x * 1000) / 1000).replace(".", ",");
    if (ohms >= 1e6) return `${trim(ohms / 1e6)} MΩ`;
    if (ohms >= 1e3) return `${trim(ohms / 1e3)} kΩ`;
    return `${trim(ohms)} Ω`;
  }

  if (typeof module !== "undefined") module.exports = { DIGIT, MULT, TOL, resistorValue, format };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("rc-solve")) return;

  CCSimple.mount({
    prefix: "rc",
    compute(v) {
      const digits = v.bands === "5" ? [v.b1, v.b2, v.b3] : [v.b1, v.b2];
      const r = resistorValue(digits, v.mult, v.tol);
      return { label: "Valor de la resistencia", main: `${format(r.ohms)} ±${r.tolerance} %`, lines: [`Rango real: de ${format(r.min)} a ${format(r.max)}.`, `Valor exacto: ${String(r.ohms).replace(".", ",")} Ω.`] };
    },
  });
})();
