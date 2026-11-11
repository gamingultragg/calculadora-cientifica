/**
 * Calculadora de Moles — a partir de la masa, la molaridad y el volumen, el número de partículas
 * o el volumen de un gas en condiciones normales (CNPT). También pasa de moles a gramos.
 */
(function () {
  const NA = 6.02214076e23; // número de Avogadro
  const MOLAR_VOLUME = 22.414; // L/mol a 0 °C y 1 atm

  function normalizeNumberInput(value) {
    let str = String(value).trim();
    if (str.includes(",")) {
      str = str.replace(/\./g, "").replace(",", ".");
    } else if (/^-?[1-9]\d{0,2}(\.\d{3})+$/.test(str)) {
      str = str.replace(/\./g, "");
    }
    return str;
  }

  const molesFromMass = (mass, molarMass) => {
    if (!(molarMass > 0)) throw new Error("La masa molar tiene que ser mayor a 0.");
    return mass / molarMass;
  };
  const massFromMoles = (moles, molarMass) => moles * molarMass;
  const molesFromMolarity = (molarity, liters) => molarity * liters;
  const molesFromParticles = (particles) => particles / NA;
  const molesFromGas = (liters) => liters / MOLAR_VOLUME;

  if (typeof module !== "undefined")
    module.exports = { NA, MOLAR_VOLUME, molesFromMass, massFromMoles, molesFromMolarity, molesFromParticles, molesFromGas };
  if (typeof document === "undefined" || !document.getElementById("mo-mode")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("mo-result-panel");
  const fmt = (n, d = 6) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: d }).format(Number(n.toPrecision(7)));
  const sci = (n) => {
    const [m, e] = n.toExponential(4).split("e");
    return `${m.replace(".", ",")} × 10${String(Number(e)).replace(/-/g, "⁻").replace(/\d/g, (d) => "⁰¹²³⁴⁵⁶⁷⁸⁹"[d])}`;
  };

  const FIELDS = {
    masa: ["mass", "molar"],
    gramos: ["moles", "molar"],
    molaridad: ["molarity", "volume"],
    particulas: ["particles"],
    gas: ["gasvol"],
  };
  function sync() {
    const mode = $("mo-mode").value;
    document.querySelectorAll("[data-field]").forEach((el) => el.classList.toggle("hidden", !FIELDS[mode].includes(el.dataset.field)));
    errorEl.classList.add("hidden");
    panel.classList.add("hidden");
  }

  function read(id, label, { positive = true } = {}) {
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
      throw new Error(`"${label}" tiene que ser un número mayor a 0.`);
    }
    return v;
  }

  function calculate() {
    errorEl.classList.add("hidden");
    try {
      const mode = $("mo-mode").value;
      let moles, title, formula, mass = null;
      let molar = null;
      if (mode === "masa") {
        const m = read("mo-mass", "Masa (g)");
        molar = read("mo-molar", "Masa molar (g/mol)");
        moles = molesFromMass(m, molar);
        title = "Moles";
        formula = `n = m / M = ${fmt(m)} g / ${fmt(molar)} g/mol`;
        mass = m;
      } else if (mode === "gramos") {
        moles = read("mo-moles", "Moles");
        molar = read("mo-molar", "Masa molar (g/mol)");
        mass = massFromMoles(moles, molar);
        title = "Masa";
        formula = `m = n × M = ${fmt(moles)} mol × ${fmt(molar)} g/mol`;
      } else if (mode === "molaridad") {
        const M = read("mo-molarity", "Molaridad (mol/L)");
        const v = read("mo-volume", "Volumen");
        const liters = $("mo-volume-unit").value === "ml" ? v / 1000 : v;
        moles = molesFromMolarity(M, liters);
        title = "Moles de soluto";
        formula = `n = M × V = ${fmt(M)} mol/L × ${fmt(liters)} L`;
      } else if (mode === "particulas") {
        const n = read("mo-particles", "Partículas");
        moles = molesFromParticles(n);
        title = "Moles";
        formula = `n = N / Nₐ = ${sci(n)} / 6,022 × 10²³`;
      } else {
        const v = read("mo-gasvol", "Volumen del gas (L)");
        moles = molesFromGas(v);
        title = "Moles de gas";
        formula = `n = V / 22,414 L/mol = ${fmt(v)} L / 22,414`;
      }
      $("mo-label").textContent = title;
      $("mo-main").textContent = mode === "gramos" ? `${fmt(mass)} g` : `${fmt(moles)} mol`;
      const lines = [`<p>${formula}</p>`];
      if (mode !== "gramos") {
        lines.push(`<p>Partículas: <strong>${sci(moles * NA)}</strong> · Volumen de gas a CNPT: <strong>${fmt(moles * MOLAR_VOLUME)} L</strong></p>`);
        if (molar) lines.push(`<p>Masa: <strong>${fmt(moles * molar)} g</strong></p>`);
      } else {
        lines.push(`<p>Equivale a ${fmt(moles)} mol · ${sci(moles * NA)} partículas.</p>`);
      }
      $("mo-lines").innerHTML = lines.join("");
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("mo-mode").addEventListener("change", sync);
  $("mo-solve").addEventListener("click", calculate);
  document.querySelectorAll("input").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && calculate()));
  document.querySelectorAll("[data-example]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const [mode, ...vals] = btn.dataset.example.split("|");
      $("mo-mode").value = mode;
      sync();
      const ids = { masa: ["mo-mass", "mo-molar"], gramos: ["mo-moles", "mo-molar"], molaridad: ["mo-molarity", "mo-volume"], particulas: ["mo-particles"], gas: ["mo-gasvol"] }[mode];
      ids.forEach((id, i) => ($(id).value = vals[i] || ""));
      calculate();
    })
  );
  sync();
})();
