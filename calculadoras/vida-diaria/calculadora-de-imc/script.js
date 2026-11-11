/**
 * Calculadora de IMC (índice de masa corporal) — IMC = peso (kg) / altura (m)².
 * Categorías de la OMS para adultos. Es un indicador orientativo, no un diagnóstico.
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

  const toKg = (v, unit) => (unit === "lb" ? v * 0.45359237 : v);
  const toMeters = (v, unit) => (unit === "cm" ? v / 100 : unit === "in" ? v * 0.0254 : v);
  const bmi = (kg, m) => kg / (m * m);

  const CATEGORIES = [
    [18.5, "Bajo peso", "low"],
    [25, "Peso normal", "ok"],
    [30, "Sobrepeso", "warn"],
    [35, "Obesidad grado I", "high"],
    [40, "Obesidad grado II", "high"],
    [Infinity, "Obesidad grado III", "high"],
  ];
  function category(value) {
    return CATEGORIES.find(([limit]) => value < limit)[1];
  }
  // Rango de peso con IMC entre 18,5 y 24,9 para una altura dada.
  function healthyRange(m) {
    return { min: 18.5 * m * m, max: 24.9 * m * m };
  }

  if (typeof module !== "undefined") module.exports = { toKg, toMeters, bmi, category, healthyRange };
  if (typeof document === "undefined" || !document.getElementById("im-weight")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("im-result-panel");
  const fmt = (n, d = 1) => new Intl.NumberFormat("es-AR", { minimumFractionDigits: d, maximumFractionDigits: d }).format(n);

  function read(id, label) {
    const el = $(id);
    el.classList.remove("field-error");
    const s = normalizeNumberInput(el.value);
    if (s === "") {
      el.classList.add("field-error");
      throw new Error(`Completá el campo "${label}".`);
    }
    const v = Number(s);
    if (!Number.isFinite(v) || v <= 0) {
      el.classList.add("field-error");
      throw new Error(`"${label}" tiene que ser un número mayor a 0.`);
    }
    return v;
  }

  function calculate() {
    errorEl.classList.add("hidden");
    try {
      const wUnit = $("im-weight-unit").value, hUnit = $("im-height-unit").value;
      const kg = toKg(read("im-weight", "Peso"), wUnit);
      const m = toMeters(read("im-height", "Altura"), hUnit);
      if (kg < 20 || kg > 400) {
        $("im-weight").classList.add("field-error");
        throw new Error("El peso parece fuera de rango: revisá el valor y la unidad.");
      }
      if (m < 0.9 || m > 2.5) {
        $("im-height").classList.add("field-error");
        throw new Error("La altura parece fuera de rango: revisá el valor y la unidad (cm, m o pulgadas).");
      }
      const value = bmi(kg, m);
      const cat = category(value);
      const r = healthyRange(m);
      $("im-main").textContent = fmt(value);
      $("im-cat").textContent = cat;
      const wShown = (x) => (wUnit === "lb" ? `${fmt(x / 0.45359237)} lb` : `${fmt(x)} kg`);
      $("im-lines").innerHTML = [
        `<p>Con tu altura de ${fmt(m, 2)} m, el rango de peso con IMC normal (18,5 a 24,9) es de <strong>${wShown(r.min)} a ${wShown(r.max)}</strong>.</p>`,
        `<p class="font-numeric">IMC = ${fmt(kg)} kg / (${fmt(m, 2)} m)² = ${fmt(value, 2)}</p>`,
        `<p>El IMC es solo un indicador orientativo para adultos: no distingue músculo de grasa ni se aplica a menores de 18 años, embarazadas o deportistas de alto rendimiento. Ante dudas, consultá con un profesional de la salud.</p>`,
      ].join("");
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("im-solve").addEventListener("click", calculate);
  document.querySelectorAll("input").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && calculate()));
  document.querySelectorAll("[data-example]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const [w, h] = btn.dataset.example.split("|");
      $("im-weight-unit").value = "kg";
      $("im-height-unit").value = "cm";
      $("im-weight").value = w;
      $("im-height").value = h;
      calculate();
    })
  );
})();
