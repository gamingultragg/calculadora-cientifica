/**
 * Calculadora de Interés Simple — I = C · i · t  y  M = C + I.
 * Tasa y tiempo se convierten a años (año comercial de 365 días, 12 meses) para
 * calcular, y los resultados se muestran en la unidad que eligió la persona.
 */
(function () {
  function normalizeNumberInput(value) {
    let str = String(value).trim();
    if (str.includes(",")) {
      str = str.replace(/\./g, "").replace(",", ".");
    } else if (/^-?[1-9]\d{0,2}(\.\d{3})+$/.test(str)) {
      str = str.replace(/\./g, "");
    }
    return str;
  }

  // Cuántos períodos de cada unidad entran en un año.
  const PER_YEAR = { anual: 1, mensual: 12, diaria: 365 };
  const TIME_PER_YEAR = { anios: 1, meses: 12, dias: 365 };

  const rateToAnnual = (rate, period) => rate * PER_YEAR[period];
  const annualToRate = (annual, period) => annual / PER_YEAR[period];
  const timeToYears = (t, unit) => t / TIME_PER_YEAR[unit];
  const yearsToTime = (y, unit) => y * TIME_PER_YEAR[unit];

  // capital C, tasa i (decimal anual), tiempo t (años)
  function interest(C, i, t) {
    return C * i * t;
  }
  function capitalFromInterest(I, i, t) {
    if (i === 0 || t === 0) throw new Error("La tasa y el tiempo tienen que ser mayores a 0 para despejar el capital.");
    return I / (i * t);
  }
  function rateFromInterest(C, I, t) {
    if (C === 0 || t === 0) throw new Error("El capital y el tiempo tienen que ser mayores a 0 para despejar la tasa.");
    return I / (C * t);
  }
  function timeFromInterest(C, I, i) {
    if (C === 0 || i === 0) throw new Error("El capital y la tasa tienen que ser mayores a 0 para despejar el tiempo.");
    return I / (C * i);
  }

  if (typeof module !== "undefined")
    module.exports = { interest, capitalFromInterest, rateFromInterest, timeFromInterest, rateToAnnual, annualToRate, timeToYears, yearsToTime };
  if (typeof document === "undefined" || !document.getElementById("is-target")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("is-result-panel");
  const fmtMoney = (n) => "$" + new Intl.NumberFormat("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(Math.round((n + 1e-9) * 100) / 100);
  const fmt = (n, d = 4) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: d }).format(Math.round((n + 1e-12) * 10 ** d) / 10 ** d);

  // Qué campos se muestran según lo que se quiere calcular.
  const FIELDS = {
    interes: ["capital", "tasa", "tiempo"],
    capital: ["interes", "tasa", "tiempo"],
    tasa: ["capital", "interes", "tiempo"],
    tiempo: ["capital", "interes", "tasa"],
  };
  function syncFields() {
    const target = $("is-target").value;
    document.querySelectorAll("[data-field]").forEach((el) => el.classList.toggle("hidden", !FIELDS[target].includes(el.dataset.field)));
    errorEl.classList.add("hidden");
    panel.classList.add("hidden");
  }

  function num(id, label, { positive = false } = {}) {
    const el = $(id);
    el.classList.remove("field-error");
    const s = normalizeNumberInput(el.value);
    if (s === "") {
      el.classList.add("field-error");
      throw new Error(`Completá el campo "${label}".`);
    }
    const v = Number(s);
    if (!Number.isFinite(v) || v < 0 || (positive && v === 0)) {
      el.classList.add("field-error");
      throw new Error(`"${label}" tiene que ser un número ${positive ? "mayor a 0" : "mayor o igual a 0"}.`);
    }
    return v;
  }

  function calculate() {
    errorEl.classList.add("hidden");
    try {
      const target = $("is-target").value;
      const ratePeriod = $("is-rate-period").value;
      const timeUnit = $("is-time-unit").value;
      const periodName = { anual: "anual", mensual: "mensual", diaria: "diaria" }[ratePeriod];
      const unitName = { anios: "años", meses: "meses", dias: "días" }[timeUnit];
      const get = {
        C: () => num("is-capital", "Capital", { positive: true }),
        I: () => num("is-interes", "Interés ganado"),
        i: () => rateToAnnual(num("is-tasa", "Tasa de interés", { positive: true }), ratePeriod) / 100,
        t: () => timeToYears(num("is-tiempo", "Tiempo", { positive: true }), timeUnit),
      };

      let main, mainLabel, lines = [];
      if (target === "interes") {
        const C = get.C(), i = get.i(), t = get.t();
        const I = interest(C, i, t);
        main = fmtMoney(I);
        mainLabel = "Interés ganado";
        lines = [`Monto final (capital + interés): <strong>${fmtMoney(C + I)}</strong>`, `I = C × i × t = ${fmtMoney(C)} × ${fmt(i * 100)}% anual × ${fmt(t)} años`];
      } else if (target === "capital") {
        const I = get.I(), i = get.i(), t = get.t();
        const C = capitalFromInterest(I, i, t);
        main = fmtMoney(C);
        mainLabel = "Capital inicial";
        lines = [`Monto final: <strong>${fmtMoney(C + I)}</strong>`, `C = I / (i × t) = ${fmtMoney(I)} / (${fmt(i * 100)}% × ${fmt(t)} años)`];
      } else if (target === "tasa") {
        const C = get.C(), I = get.I(), t = get.t();
        const i = rateFromInterest(C, I, t);
        main = `${fmt(annualToRate(i * 100, ratePeriod), 4)} % ${periodName}`;
        mainLabel = "Tasa de interés";
        lines = [`Equivale a ${fmt(i * 100)}% anual, ${fmt((i * 100) / 12)}% mensual y ${fmt((i * 100) / 365, 6)}% diaria.`, `i = I / (C × t) = ${fmtMoney(I)} / (${fmtMoney(C)} × ${fmt(t)} años)`];
      } else {
        const C = get.C(), I = get.I(), i = get.i();
        const years = timeFromInterest(C, I, i);
        main = `${fmt(yearsToTime(years, timeUnit), 4)} ${unitName}`;
        mainLabel = "Tiempo";
        lines = [`Equivale a ${fmt(years)} años, ${fmt(years * 12)} meses o ${fmt(years * 365, 2)} días.`, `t = I / (C × i) = ${fmtMoney(I)} / (${fmtMoney(C)} × ${fmt(i * 100)}% anual)`];
      }
      $("is-label").textContent = mainLabel;
      $("is-main").textContent = main;
      $("is-lines").innerHTML = lines.map((l) => `<p>${l}</p>`).join("");
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("is-target").addEventListener("change", syncFields);
  $("is-solve").addEventListener("click", calculate);
  document.querySelectorAll("input").forEach((el) =>
    el.addEventListener("keydown", (e) => {
      if (e.key === "Enter") calculate();
    })
  );
  syncFields();
})();
