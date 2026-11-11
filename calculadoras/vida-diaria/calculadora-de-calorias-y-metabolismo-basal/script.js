/**
 * Calorías diarias y metabolismo basal — ecuación de Mifflin-St Jeor y factor de actividad.
 *   TMB = 10·peso(kg) + 6,25·altura(cm) − 5·edad + 5 (hombres) o − 161 (mujeres)
 * Es una estimación orientativa: no reemplaza la consulta con un profesional de la salud.
 */
(function () {
  const ACTIVITY = { sedentario: 1.2, ligero: 1.375, moderado: 1.55, intenso: 1.725, muyintenso: 1.9 };

  function bmr(sex, weightKg, heightCm, age) {
    return 10 * weightKg + 6.25 * heightCm - 5 * age + (sex === "hombre" ? 5 : -161);
  }
  const maintenance = (bmrValue, level) => bmrValue * ACTIVITY[level];

  if (typeof module !== "undefined") module.exports = { ACTIVITY, bmr, maintenance };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("ca-solve")) return;

  CCSimple.mount({
    prefix: "ca",
    compute(v, h) {
      if (v.age < 15 || v.age > 100) throw new Error('"Edad" tiene que estar entre 15 y 100 años (la fórmula es para adultos).');
      if (v.weight < 30 || v.weight > 300) throw new Error('"Peso" parece fuera de rango: revisá el valor en kg.');
      if (v.height < 100 || v.height > 250) throw new Error('"Altura" parece fuera de rango: revisá el valor en cm.');
      const b = bmr(v.sex, v.weight, v.height, v.age);
      const m = maintenance(b, v.activity);
      const f = (x) => h.fmt(Math.round(x), 0);
      const floor = v.sex === "hombre" ? 1500 : 1200;
      const lose = Math.max(m - 500, floor);
      const lines = [
        `Metabolismo basal (TMB): <strong>${f(b)} kcal/día</strong> — lo que gasta tu cuerpo en reposo.`,
        `Para <strong>mantener</strong> el peso: ${f(m)} kcal/día (factor de actividad ${v.activity === "sedentario" ? "1,2" : String(ACTIVITY[v.activity]).replace(".", ",")}).`,
        `Para <strong>bajar</strong> ~0,5 kg por semana: ${f(lose)} kcal/día${lose > m - 500 ? ` (no se baja de ${floor} kcal por seguridad)` : ""}.`,
        `Para <strong>subir</strong> de forma gradual: ${f(m + 300)} kcal/día.`,
        "Es una estimación: el metabolismo varía entre personas. Consultá con un profesional de la salud antes de hacer cambios importantes en tu alimentación.",
      ];
      return { label: "Calorías para mantener tu peso", main: `${f(m)} kcal/día`, lines };
    },
  });
})();
