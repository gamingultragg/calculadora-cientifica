/**
 * Margen y markup. Margen = (precio − costo) / precio. Markup = (precio − costo) / costo.
 */
(function () {
  function priceFromMargin(cost, marginPct) {
    if (marginPct >= 100) throw new Error("El margen tiene que ser menor al 100 %.");
    return cost / (1 - marginPct / 100);
  }
  const priceFromMarkup = (cost, markupPct) => cost * (1 + markupPct / 100);
  function fromPrices(cost, price) {
    return { profit: price - cost, margin: (price - cost) / price, markup: (price - cost) / cost };
  }

  if (typeof module !== "undefined") module.exports = { priceFromMargin, priceFromMarkup, fromPrices };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("mk-solve")) return;

  CCSimple.mount({
    prefix: "mk",
    compute(v, h) {
      let price;
      if (v.mode === "margen") price = priceFromMargin(v.cost, v.margin);
      else if (v.mode === "markup") price = priceFromMarkup(v.cost, v.markup);
      else price = v.price;
      const r = fromPrices(v.cost, price);
      const lines = [
        `Ganancia por unidad: <strong>${h.money(r.profit)}</strong>`,
        `Margen sobre el precio: <strong>${h.pct(r.margin)}</strong> · Markup sobre el costo: <strong>${h.pct(r.markup)}</strong>`,
        `Con IVA 21 %, el precio al público sería ${h.money(price * 1.21)}.`,
        r.profit < 0 ? "El precio está por debajo del costo: vendés con pérdida." : "",
      ];
      return { label: v.mode === "calc" ? "Margen" : "Precio de venta", main: v.mode === "calc" ? h.pct(r.margin) : h.money(price), lines };
    },
  });
})();
