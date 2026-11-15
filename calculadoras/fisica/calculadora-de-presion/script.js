/**
 * Presión — P = F/A (fuerza sobre una superficie) y presión hidrostática P = ρ·g·h (columna de líquido).
 * La presión absoluta a cierta profundidad suma la atmosférica (101.325 Pa).
 */
(function () {
  const ATM = 101325;
  const AREA = { m2: 1, cm2: 1e-4, mm2: 1e-6 };
  const pressure = (forceN, areaM2) => forceN / areaM2;
  const hydrostatic = (rho, g, h) => rho * g * h;
  // Equivalencias de 1 Pa
  const UNITS = { Pa: 1, kPa: 1e-3, bar: 1e-5, atm: 1 / ATM, mmHg: 1 / 133.322387415, psi: 1 / 6894.757293168 };

  if (typeof module !== "undefined") module.exports = { ATM, AREA, UNITS, pressure, hydrostatic };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("ps-solve")) return;

  CCSimple.mount({
    prefix: "ps",
    compute(v, h) {
      const f = (x, d = 4) => h.fmt(x, d);
      const conv = (pa) => `${f(pa, 2)} Pa = ${f(pa * UNITS.kPa)} kPa = ${f(pa * UNITS.atm)} atm = ${f(pa * UNITS.bar)} bar = ${f(pa * UNITS.mmHg, 2)} mmHg = ${f(pa * UNITS.psi)} psi`;
      if (v.mode === "sol") {
        const a = v.A * AREA[v.Au];
        const p = pressure(v.F, a);
        return { label: "Presión", main: `${f(p, 2)} Pa`, lines: [`P = F / A = ${f(v.F)} N / ${f(a, 6)} m² = <strong>${f(p, 2)} Pa</strong>.`, `Equivale a ${conv(p)}.`, "1 Pa = 1 N/m². A igual fuerza, cuanto menor es la superficie, mayor es la presión."] };
      }
      const p = hydrostatic(v.rho, v.g, v.h);
      return {
        label: "Presión hidrostática",
        main: `${f(p, 2)} Pa`,
        lines: [
          `P = ρ·g·h = ${f(v.rho)} kg/m³ × ${f(v.g)} m/s² × ${f(v.h)} m = <strong>${f(p, 2)} Pa</strong>.`,
          `Equivale a ${conv(p)}.`,
          `Presión absoluta a esa profundidad (sumando la atmosférica): <strong>${f(p + ATM, 2)} Pa</strong> = ${f((p + ATM) * UNITS.atm)} atm.`,
          "No depende de la forma del recipiente: solo de la profundidad, la densidad del líquido y la gravedad.",
        ],
      };
    },
  });
})();
