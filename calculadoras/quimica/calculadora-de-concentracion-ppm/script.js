/**
 * Concentración en ppm y porcentaje — soluciones diluidas en agua (densidad ≈ 1 g/mL).
 *   ppm = mg de soluto por litro de solución   ·   % m/v = g de soluto cada 100 mL   ·   1 % = 10.000 ppm
 */
(function () {
  const MG = { mg: 1, g: 1000, kg: 1e6 };
  const LITERS = { L: 1, mL: 1e-3 };

  // mgSolute: mg de soluto · liters: litros de solución
  function concentration(mgSolute, liters) {
    const mgL = mgSolute / liters;
    return { mgL, gL: mgL / 1000, pctMV: mgL / 10000 };
  }
  // ppm → otras unidades (en agua diluida, 1 ppm = 1 mg/L = 1 µg/mL)
  const fromPpm = (ppm) => ({ mgL: ppm, gL: ppm / 1000, pctMV: ppm / 10000, ugMl: ppm });
  // mg de soluto necesarios para una concentración ppm en cierto volumen (L)
  const massNeeded = (ppm, liters) => ppm * liters;

  if (typeof module !== "undefined") module.exports = { MG, LITERS, concentration, fromPpm, massNeeded };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("cn-solve")) return;

  CCSimple.mount({
    prefix: "cn",
    compute(v, h) {
      const f = (x, d = 4) => h.fmt(x, d);
      if (v.mode === "conc") {
        const liters = v.vol * LITERS[v.vu];
        const r = concentration(v.s * MG[v.su], liters);
        return {
          label: "Concentración",
          main: `${f(r.mgL)} ppm`,
          lines: [
            `${f(v.s)} ${v.su} de soluto en ${f(v.vol)} ${v.vu} de solución.`,
            `<strong>${f(r.mgL)} mg/L</strong> = ${f(r.mgL)} ppm.`,
            `${f(r.gL)} g/L.`,
            `${f(r.pctMV, 6)} % m/v (gramos de soluto cada 100 mL de solución).`,
          ],
        };
      }
      if (v.mode === "ppm") {
        const r = fromPpm(v.p);
        return {
          label: "Equivalencias",
          main: `${f(r.pctMV, 6)} %`,
          lines: [
            `${f(v.p)} ppm = <strong>${f(r.mgL)} mg/L</strong> = ${f(r.ugMl)} µg/mL.`,
            `${f(r.gL, 6)} g/L.`,
            `${f(r.pctMV, 6)} % m/v.`,
            "Vale para soluciones diluidas en agua, donde 1 litro pesa unos 1.000 g.",
          ],
        };
      }
      const liters = v.vol * LITERS[v.vu];
      const mg = massNeeded(v.p, liters);
      return {
        label: "Soluto necesario",
        main: mg >= 1000 ? `${f(mg / 1000)} g` : `${f(mg)} mg`,
        lines: [
          `Para ${f(v.p)} ppm en ${f(v.vol)} ${v.vu} hacen falta ${f(mg)} mg = ${f(mg / 1000, 6)} g de soluto.`,
          "Se disuelve en parte del agua y se completa hasta el volumen final.",
        ],
      };
    },
  });
})();
