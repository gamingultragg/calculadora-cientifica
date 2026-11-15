/**
 * Calor específico y calorimetría — Q = m · c · ΔT.
 * Q en joules (J), m en gramos (g), c en J/(g·°C) y ΔT en °C (o K). 1 cal = 4,184 J.
 */
(function () {
  const heat = (m, c, dT) => m * c * dT;
  const specificHeat = (q, m, dT) => {
    if (dT === 0) throw new Error('"Variación de temperatura" no puede ser 0 para despejar el calor específico.');
    return q / (m * dT);
  };
  const mass = (q, c, dT) => {
    if (dT === 0) throw new Error('"Variación de temperatura" no puede ser 0 para despejar la masa.');
    return q / (c * dT);
  };
  const deltaT = (q, m, c) => q / (m * c);
  const CAL = 4.184;

  if (typeof module !== "undefined") module.exports = { CAL, heat, specificHeat, mass, deltaT };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("ce-solve")) return;

  CCSimple.mount({
    prefix: "ce",
    compute(v, h) {
      const f = (x, d = 4) => h.fmt(x, d);
      let q = v.q;
      let m = v.m;
      let c = v.c;
      let dT = v.dT;
      let label;
      let main;
      if (v.mode === "q") {
        q = heat(m, c, dT);
        label = "Calor intercambiado (Q)";
        main = `${f(q)} J`;
      } else if (v.mode === "c") {
        if (q !== 0 && dT !== 0 && Math.sign(q) !== Math.sign(dT)) throw new Error("El calor y la variación de temperatura tienen que tener el mismo signo: si el cuerpo gana calor, se calienta (ΔT > 0).");
        c = specificHeat(q, m, dT);
        if (!(c > 0)) throw new Error("El calor específico tiene que dar positivo: revisá que Q no sea 0 y que Q y ΔT tengan el mismo signo.");
        label = "Calor específico (c)";
        main = `${f(c)} J/(g·°C)`;
      } else if (v.mode === "m") {
        m = mass(q, c, dT);
        if (m <= 0) throw new Error("El calor y la variación de temperatura tienen que tener el mismo signo: revisá los datos.");
        label = "Masa (m)";
        main = `${f(m)} g`;
      } else {
        dT = deltaT(q, m, c);
        label = "Variación de temperatura (ΔT)";
        main = `${f(dT)} °C`;
      }
      const lines = [
        `Q = m · c · ΔT = ${f(m)} g × ${f(c)} J/(g·°C) × ${f(dT)} °C = ${f(q)} J.`,
        `En otras unidades: ${f(q / 1000, 2)} kJ = ${f(q / CAL, 1)} cal = ${f(q / CAL / 1000, 2)} kcal.`,
        dT > 0 ? "El cuerpo <strong>absorbe</strong> calor y se calienta." : dT < 0 ? "El cuerpo <strong>cede</strong> calor y se enfría." : "No hay cambio de temperatura.",
        "Vale mientras no haya cambio de estado (fusión, ebullición): en ese caso se usa el calor latente.",
      ];
      return { label, main, lines };
    },
  });
})();
