/**
 * Consumo de combustible — rendimiento (km/L y L/100 km), litros y costo de un viaje, y autonomía del tanque.
 *   L/100 km = 100 / (km/L)   ·   litros = km × (L/100 km) / 100   ·   autonomía = litros / (L/100 km) × 100
 */
(function () {
  function efficiency(km, liters) {
    const kmL = km / liters;
    return { kmL, l100: 100 / kmL };
  }
  const tripLiters = (km, l100) => (km * l100) / 100;
  const range = (liters, l100) => (liters / l100) * 100;

  if (typeof module !== "undefined") module.exports = { efficiency, tripLiters, range };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("cf-solve")) return;

  CCSimple.mount({
    prefix: "cf",
    compute(v, h) {
      const f = (x, d = 2) => h.fmt(x, d);
      const price = v.price || 0;
      if (v.mode === "consumo") {
        const r = efficiency(v.km, v.lit);
        const lines = [
          `Rendimiento: <strong>${f(r.kmL)} km/L</strong> (cada litro te lleva ${f(r.kmL)} km).`,
          `Consumo: <strong>${f(r.l100)} L cada 100 km</strong>.`,
        ];
        if (price > 0) lines.push(`Costo por km: ${h.money((v.lit * price) / v.km)} · Costo por cada 100 km: ${h.money(r.l100 * price)}.`, `Gastaste ${h.money(v.lit * price)} en ${f(v.lit)} L.`);
        return { label: "Rendimiento", main: `${f(r.kmL)} km/L`, lines };
      }
      if (v.mode === "viaje") {
        const l = tripLiters(v.km, v.cons);
        const lines = [`Para ${f(v.km)} km con ${f(v.cons)} L/100 km necesitás <strong>${f(l)} litros</strong>.`];
        if (price > 0) lines.push(`Costo del viaje: <strong>${h.money(l * price)}</strong> (${h.money((l * price) / v.km)} por km).`);
        return { label: "Combustible necesario", main: `${f(l)} L`, lines };
      }
      const km = range(v.tank, v.cons);
      const lines = [`Con ${f(v.tank)} L y ${f(v.cons)} L/100 km podés recorrer unos <strong>${f(km, 0)} km</strong>.`];
      if (price > 0) lines.push(`Llenar el tanque cuesta ${h.money(v.tank * price)}.`);
      lines.push("Es un valor teórico: el consumo real cambia con la velocidad, el tránsito y la carga.");
      return { label: "Autonomía", main: `${f(km, 0)} km`, lines };
    },
  });
})();
