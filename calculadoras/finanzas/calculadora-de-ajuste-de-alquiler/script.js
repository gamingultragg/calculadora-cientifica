/**
 * Ajuste de alquiler — por índice (nuevo = actual × índice final / índice inicial) o por porcentaje.
 * El usuario carga los valores del índice del contrato (ICL, IPC, CER, etc.): la calculadora no consulta datos externos.
 */
(function () {
  const byIndex = (rent, i0, i1) => rent * (i1 / i0);
  const byPercent = (rent, pct) => rent * (1 + pct / 100);

  if (typeof module !== "undefined") module.exports = { byIndex, byPercent };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("al-solve")) return;

  CCSimple.mount({
    prefix: "al",
    compute(v, h) {
      const next = v.mode === "indice" ? byIndex(v.rent, v.i0, v.i1) : byPercent(v.rent, v.pct);
      const rise = next / v.rent - 1;
      const lines = [
        `Aumento: <strong>${h.money(next - v.rent)}</strong> (${h.pct(rise)}) sobre el alquiler actual de ${h.money(v.rent)}.`,
        v.mode === "indice" ? `Cuenta: ${h.money(v.rent)} × ${h.fmt(v.i1, 4)} / ${h.fmt(v.i0, 4)}` : `Cuenta: ${h.money(v.rent)} × (1 + ${h.fmt(v.pct, 2)} %)`,
        `Con este valor, en 12 meses pagarías ${h.money(next * 12)}.`,
      ];
      return { label: "Nuevo alquiler", main: h.money(next), lines };
    },
  });
})();
