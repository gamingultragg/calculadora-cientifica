/**
 * Propiedades coligativas — descenso crioscópico (ΔTf = i·Kf·m) y ascenso ebulloscópico (ΔTb = i·Kb·m) de una solución.
 * m = molalidad = moles de soluto / kg de solvente; i = factor de van't Hoff (cantidad de partículas que genera cada unidad de soluto).
 */
(function () {
  // Constantes crioscópica (Kf) y ebulloscópica (Kb) en °C·kg/mol, y puntos de congelación / ebullición del solvente puro (°C).
  const SOLVENTS = {
    agua: { name: "Agua", kf: 1.86, kb: 0.512, tf: 0, tb: 100 },
    benceno: { name: "Benceno", kf: 5.12, kb: 2.53, tf: 5.5, tb: 80.1 },
    etanol: { name: "Etanol", kf: 1.99, kb: 1.22, tf: -114.1, tb: 78.37 },
    acetico: { name: "Ácido acético", kf: 3.9, kb: 3.07, tf: 16.6, tb: 118.1 },
  };

  const molality = (soluteG, molarMass, solventG) => soluteG / molarMass / (solventG / 1000);
  const freezingDrop = (i, kf, m) => i * kf * m;
  const boilingRise = (i, kb, m) => i * kb * m;

  if (typeof module !== "undefined") module.exports = { SOLVENTS, molality, freezingDrop, boilingRise };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("pc-solve")) return;

  CCSimple.mount({
    prefix: "pc",
    compute(v, h) {
      const f = (x, d = 4) => h.fmt(x, d);
      const s = SOLVENTS[v.solv];
      const i = v.i || 1;
      const m = molality(v.mass, v.mm, v.solvent);
      const dTf = freezingDrop(i, s.kf, m);
      const dTb = boilingRise(i, s.kb, m);
      const lines = [
        `Molalidad: ${f(v.mass)} g / ${f(v.mm)} g/mol = ${f(v.mass / v.mm)} mol de soluto en ${f(v.solvent / 1000)} kg de ${s.name.toLowerCase()} → m = <strong>${f(m)} mol/kg</strong>.`,
        `Descenso del punto de congelación: ΔTf = i·Kf·m = ${f(i, 2)} × ${f(s.kf, 3)} × ${f(m)} = <strong>${f(dTf)} °C</strong> → congela a <strong>${f(s.tf - dTf)} °C</strong> (el solvente puro, a ${f(s.tf, 1)} °C).`,
        `Ascenso del punto de ebullición: ΔTb = i·Kb·m = ${f(i, 2)} × ${f(s.kb, 3)} × ${f(m)} = <strong>${f(dTb)} °C</strong> → hierve a <strong>${f(s.tb + dTb)} °C</strong> (el solvente puro, a ${f(s.tb, 1)} °C, a presión normal).`,
        "Vale para soluciones diluidas e ideales: en soluciones concentradas el resultado real se aparta.",
      ];
      return v.mode === "crio" ? { label: "Punto de congelación de la solución", main: `${f(s.tf - dTf)} °C`, lines } : { label: "Punto de ebullición de la solución", main: `${f(s.tb + dTb)} °C`, lines };
    },
  });
})();
