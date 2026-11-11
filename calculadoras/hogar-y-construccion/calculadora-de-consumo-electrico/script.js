/**
 * Consumo eléctrico — kWh y costo de un artefacto: kWh = potencia (W) × horas / 1000.
 */
(function () {
  const dailyKwh = (watts, hoursPerDay, qty) => (watts * qty * hoursPerDay) / 1000;

  if (typeof module !== "undefined") module.exports = { dailyKwh };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("co-solve")) return;

  CCSimple.mount({
    prefix: "co",
    compute(v, h) {
      if (v.hours > 24) throw new Error('"Horas de uso por día" no puede ser mayor a 24.');
      if (v.days > 31) throw new Error('"Días de uso al mes" no puede ser mayor a 31.');
      const daily = dailyKwh(v.watts, v.hours, v.qty || 1);
      const monthly = daily * v.days;
      const lines = [
        `Consumo diario: <strong>${h.fmt(daily, 3)} kWh</strong> · Mensual: <strong>${h.fmt(monthly, 2)} kWh</strong> · Anual: ${h.fmt(monthly * 12, 1)} kWh.`,
        `Costo diario: ${h.money(daily * v.price)} · Anual: ${h.money(monthly * v.price * 12)} (con ${h.money(v.price)} el kWh).`,
        `Cuenta: ${h.fmt(v.watts, 0)} W × ${v.qty || 1} × ${h.fmt(v.hours, 1)} h × ${h.fmt(v.days, 0)} días / 1000.`,
      ];
      return { label: "Costo mensual", main: h.money(monthly * v.price), lines };
    },
  });
})();
