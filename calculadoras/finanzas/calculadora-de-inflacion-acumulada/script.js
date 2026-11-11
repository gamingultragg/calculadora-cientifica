/**
 * Inflación acumulada — compone las inflaciones mensuales: acumulada = Π(1 + r) − 1.
 */
(function () {
  function parseRates(text) {
    const tokens = String(text).trim().split(/[\s;]+/).filter(Boolean);
    if (tokens.length < 1) throw new Error("Ingresá al menos una inflación mensual.");
    if (tokens.length > 600) throw new Error("Podés ingresar hasta 600 valores.");
    return tokens.map((t) => {
      const s = t.replace("%", "").replace(",", ".");
      const v = Number(s);
      if (!Number.isFinite(v) || v <= -100) throw new Error(`"${t}" no es un porcentaje válido (usá números como 4,2 o 3.5).`);
      return v;
    });
  }

  function accumulate(ratesPct) {
    const factor = ratesPct.reduce((a, r) => a * (1 + r / 100), 1);
    const n = ratesPct.length;
    const geo = Math.pow(factor, 1 / n) - 1;
    return { factor, cumulative: factor - 1, monthlyGeo: geo, annualized: Math.pow(1 + geo, 12) - 1, n };
  }

  if (typeof module !== "undefined") module.exports = { parseRates, accumulate };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("ia-solve")) return;

  CCSimple.mount({
    prefix: "ia",
    compute(v, h) {
      const r = accumulate(parseRates(v.rates));
      const lines = [
        `Meses considerados: <strong>${r.n}</strong> · Promedio mensual (geométrico): <strong>${h.pct(r.monthlyGeo)}</strong>`,
        `Anualizada a ese ritmo: <strong>${h.pct(r.annualized)}</strong>`,
        `Poder adquisitivo perdido: ${h.pct(1 - 1 / r.factor)} (con la plata de antes comprás ese porcentaje menos).`,
      ];
      if (v.amount !== undefined) {
        lines.push(`Para mantener el poder de compra, ${h.money(v.amount)} de antes equivalen hoy a <strong>${h.money(v.amount * r.factor)}</strong>.`);
      }
      return { label: "Inflación acumulada", main: h.pct(r.cumulative), lines };
    },
  });
})();
