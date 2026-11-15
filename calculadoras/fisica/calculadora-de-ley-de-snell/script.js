/**
 * Ley de Snell — n₁·sen θ₁ = n₂·sen θ₂. Ángulo refractado, índice de refracción desconocido, ángulo crítico y reflexión total interna.
 * Velocidad de la luz en un medio: v = c / n, con c = 299.792.458 m/s.
 */
(function () {
  const C = 299792458;
  const rad = (d) => (d * Math.PI) / 180;
  const deg = (r) => (r * 180) / Math.PI;

  // Devuelve { tir: true } si no hay rayo refractado (reflexión total interna), o { theta2 } en grados.
  function refract(n1, n2, theta1Deg) {
    const s = (n1 * Math.sin(rad(theta1Deg))) / n2;
    if (s > 1) return { tir: true, sin: s };
    return { tir: false, theta2: deg(Math.asin(s)), sin: s };
  }
  const index2 = (n1, theta1Deg, theta2Deg) => (n1 * Math.sin(rad(theta1Deg))) / Math.sin(rad(theta2Deg));
  // Ángulo crítico: solo existe al pasar de un medio más refringente a uno menos refringente (n₁ > n₂).
  const critical = (n1, n2) => (n1 > n2 ? deg(Math.asin(n2 / n1)) : null);

  if (typeof module !== "undefined") module.exports = { C, refract, index2, critical };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("sn-solve")) return;

  CCSimple.mount({
    prefix: "sn",
    compute(v, h) {
      const f = (x, d = 4) => h.fmt(x, d);
      const speed = (n) => `${h.fmt(C / n / 1000, 0)} km/s`;
      if (v.mode === "t2") {
        if (v.a1 >= 90) throw new Error('"Ángulo de incidencia" tiene que ser menor a 90°.');
        const r = refract(v.n1, v.n2, v.a1);
        const crit = critical(v.n1, v.n2);
        if (r.tir) {
          return { label: "Resultado", main: "Reflexión total interna", lines: [`n₁·sen θ₁ / n₂ = ${f(r.sin)} es mayor que 1: no existe ángulo refractado, <strong>la luz se refleja por completo</strong> en la superficie.`, `El ángulo crítico entre estos medios es ${f(crit, 2)}°: con ángulos de incidencia mayores hay reflexión total.`] };
        }
        const lines = [
          `θ₂ = arcsen(n₁·sen θ₁ / n₂) = arcsen(${f(v.n1)} × sen ${f(v.a1, 2)}° / ${f(v.n2)}) = <strong>${f(r.theta2, 2)}°</strong>.`,
          r.theta2 < v.a1 ? "El rayo se acerca a la normal (pasa a un medio más refringente)." : r.theta2 > v.a1 ? "El rayo se aleja de la normal (pasa a un medio menos refringente)." : "No se desvía.",
          `Velocidad de la luz: ${speed(v.n1)} en el medio 1 y ${speed(v.n2)} en el medio 2.`,
          crit ? `Ángulo crítico (de 1 a 2): ${f(crit, 2)}°.` : null,
        ];
        return { label: "Ángulo de refracción θ₂", main: `${f(r.theta2, 2)}°`, lines };
      }
      if (v.mode === "n2") {
        if (v.a1 >= 90 || v.a2 >= 90) throw new Error("Los ángulos tienen que ser menores a 90°.");
        const n2 = index2(v.n1, v.a1, v.a2);
        return { label: "Índice de refracción n₂", main: f(n2), lines: [`n₂ = n₁·sen θ₁ / sen θ₂ = ${f(v.n1)} × sen ${f(v.a1, 2)}° / sen ${f(v.a2, 2)}° = <strong>${f(n2)}</strong>.`, `La luz viaja en ese medio a ${speed(n2)} (${f((1 / n2) * 100, 1)} % de c).`] };
      }
      const crit = critical(v.n1, v.n2);
      if (crit === null) throw new Error("No hay ángulo crítico: la luz tiene que pasar de un medio con mayor índice (n₁) a uno con menor índice (n₂).");
      return { label: "Ángulo crítico", main: `${f(crit, 2)}°`, lines: [`θc = arcsen(n₂ / n₁) = arcsen(${f(v.n2)} / ${f(v.n1)}) = <strong>${f(crit, 2)}°</strong>.`, "Con ángulos de incidencia mayores que el crítico no hay refracción: la luz se refleja por completo (reflexión total interna), como ocurre en la fibra óptica."] };
    },
  });
})();
