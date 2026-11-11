/**
 * Descuentos sucesivos — cada descuento se aplica sobre el precio que quedó del anterior.
 */
(function () {
  function parseDiscounts(text) {
    const tokens = String(text).trim().split(/[\s;]+/).filter(Boolean);
    if (!tokens.length) throw new Error("Ingresá al menos un descuento.");
    if (tokens.length > 30) throw new Error("Podés ingresar hasta 30 descuentos.");
    return tokens.map((t) => {
      const v = Number(t.replace("%", "").replace(",", "."));
      if (!Number.isFinite(v) || v < 0 || v >= 100) throw new Error(`"${t}" no es un descuento válido (entre 0 y 99,99).`);
      return v;
    });
  }

  function sequential(price, discounts) {
    const steps = [];
    let current = price;
    discounts.forEach((d) => {
      const amount = current * (d / 100);
      current -= amount;
      steps.push({ d, amount, price: current });
    });
    return { final: current, totalPct: 1 - current / price, sumPct: discounts.reduce((a, b) => a + b, 0) / 100, steps };
  }

  if (typeof module !== "undefined") module.exports = { parseDiscounts, sequential };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("dsc-solve")) return;

  CCSimple.mount({
    prefix: "dsc",
    compute(v, h) {
      const r = sequential(v.price, parseDiscounts(v.discounts));
      const rows = r.steps.map((s, i) => `<li>${i + 1}.º descuento de ${h.fmt(s.d, 2)} %: −${h.money(s.amount)} → ${h.money(s.price)}</li>`).join("");
      const lines = [
        `Descuento total equivalente: <strong>${h.pct(r.totalPct)}</strong> (ahorrás ${h.money(v.price - r.final)}).`,
        r.steps.length > 1 ? `No es la suma de los porcentajes (${h.pct(r.sumPct)}): cada descuento se calcula sobre un precio ya rebajado.` : "",
      ];
      return { label: "Precio final", main: h.money(r.final), lines, extra: `<ol class="list-decimal list-inside space-y-1 font-numeric">${rows}</ol>` };
    },
  });
})();
