/**
 * Peso ideal — fórmulas de Devine, Robinson, Miller y Hamwi (altura sobre 60 pulgadas = 152,4 cm) y rango saludable según el IMC (18,5 a 24,9).
 * Es una estimación orientativa para adultos: no reemplaza la consulta con un profesional de la salud.
 */
(function () {
  function idealWeights(sex, heightCm) {
    const over = heightCm / 2.54 - 60; // pulgadas por encima de 5 pies
    const m = sex === "hombre";
    return {
      devine: (m ? 50 : 45.5) + 2.3 * over,
      robinson: (m ? 52 : 49) + (m ? 1.9 : 1.7) * over,
      miller: (m ? 56.2 : 53.1) + (m ? 1.41 : 1.36) * over,
      hamwi: (m ? 48 : 45.5) + (m ? 2.7 : 2.2) * over,
    };
  }
  function healthyRange(heightCm) {
    const h = heightCm / 100;
    return { min: 18.5 * h * h, max: 24.9 * h * h };
  }

  if (typeof module !== "undefined") module.exports = { idealWeights, healthyRange };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("pi-solve")) return;

  CCSimple.mount({
    prefix: "pi",
    compute(v, h) {
      if (v.age < 18) throw new Error("Las fórmulas de peso ideal son para adultos (18 años o más). En menores se usan curvas de crecimiento que indica el pediatra.");
      if (v.height < 140 || v.height > 220) throw new Error('"Altura" tiene que estar entre 140 y 220 cm.');
      const f = (x) => h.fmt(x, 1);
      const w = idealWeights(v.sex, v.height);
      const r = healthyRange(v.height);
      const avg = (w.devine + w.robinson + w.miller + w.hamwi) / 4;
      const lines = [
        `Rango de peso saludable según el IMC (18,5 a 24,9): <strong>${f(r.min)} a ${f(r.max)} kg</strong>.`,
        `Devine: ${f(w.devine)} kg · Robinson: ${f(w.robinson)} kg · Miller: ${f(w.miller)} kg · Hamwi: ${f(w.hamwi)} kg.`,
        `Promedio de las cuatro fórmulas: ${f(avg)} kg.`,
        v.height < 152.4 ? "Con menos de 152,4 cm (60 pulgadas) las fórmulas extrapolan hacia abajo y pierden precisión: guiate más por el rango del IMC." : null,
        "Son estimaciones: no distinguen entre masa muscular y grasa, ni contemplan la contextura, la edad o el estado de salud. Consultá con un médico o nutricionista.",
      ];
      return { label: "Rango de peso saludable (IMC 18,5 a 24,9)", main: `${f(r.min)} – ${f(r.max)} kg`, lines };
    },
  });
})();
