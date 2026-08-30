/**
 * Calculadora de Diluciones — resuelve C1, V1, C2 o V2 a partir de los
 * otros tres valores, con la ley de dilución C1V1 = C2V2.
 */
(function () {
  // Convierte un input numérico en formato es-AR ("15.000" con punto de
  // miles, "1.234,56" con punto de miles y coma decimal, o un número
  // simple como "9.8") al formato que entiende Number(). Un punto seguido
  // de 1, 2 o más de 3 dígitos se interpreta como separador decimal (no
  // de miles), evitando falsos positivos como "3.14" o "0.5".
  function normalizeNumberInput(value) {
    let str = String(value).trim();
    if (str.includes(",")) {
      str = str.replace(/\./g, "").replace(",", ".");
    } else if (/^-?[1-9]\d{0,2}(\.\d{3})+$/.test(str)) {
      str = str.replace(/\./g, "");
    }
    return str;
  }

  const targetSelect = document.getElementById("dl-target");
  const inputsWrap = document.getElementById("dl-inputs");
  const errorEl = document.getElementById("dl-error");
  const resultPanel = document.getElementById("dl-result-panel");
  const stepsEl = document.getElementById("dl-steps");

  const fmt = (n) =>
    new Intl.NumberFormat("es-AR", { maximumFractionDigits: 6 }).format(
      Object.is(n, -0) ? 0 : Math.round(n * 1e8) / 1e8
    );

  function showError(message) {
    errorEl.textContent = message;
    errorEl.classList.remove("hidden");
    resultPanel.classList.add("hidden");
  }
  function clearError() {
    errorEl.classList.add("hidden");
    errorEl.textContent = "";
  }
  function addStep(html) {
    const li = document.createElement("li");
    li.innerHTML = html;
    stepsEl.appendChild(li);
  }
  function fieldTemplate(id, label) {
    return `
      <div>
        <label for="${id}" class="block text-sm font-medium mb-1">${label}</label>
        <input id="${id}" type="text" inputmode="decimal" placeholder="0"
          class="w-full rounded-xl surface px-3 py-2.5 font-numeric focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]" />
      </div>`;
  }
  function parseField(id, label, { positive = false } = {}) {
    const el = document.getElementById(id);
    el.classList.remove("field-error");
    const raw = normalizeNumberInput(el.value);
    if (raw === "") {
      el.classList.add("field-error");
      throw new Error(`El campo "${label}" no puede estar vacío.`);
    }
    const value = Number(raw);
    if (!Number.isFinite(value)) {
      el.classList.add("field-error");
      throw new Error(`El campo "${label}" debe ser un número válido.`);
    }
    if (positive && value <= 0) {
      el.classList.add("field-error");
      throw new Error(`El campo "${label}" debe ser mayor a 0.`);
    }
    return value;
  }

  const FIELDS = {
    C1: fieldTemplate("dl-c1", "Concentración inicial (C₁)"),
    V1: fieldTemplate("dl-v1", "Volumen inicial (V₁)"),
    C2: fieldTemplate("dl-c2", "Concentración final (C₂)"),
    V2: fieldTemplate("dl-v2", "Volumen final (V₂)"),
  };

  function render() {
    const target = targetSelect.value;
    inputsWrap.innerHTML = Object.keys(FIELDS)
      .filter((k) => k !== target)
      .map((k) => FIELDS[k])
      .join("");
  }
  targetSelect.addEventListener("change", () => {
    render();
    clearError();
    resultPanel.classList.add("hidden");
  });

  document.getElementById("dl-solve").addEventListener("click", () => {
    clearError();
    stepsEl.innerHTML = "";
    try {
      const target = targetSelect.value;

      if (target === "C1") {
        const v1 = parseField("dl-v1", "Volumen inicial (V₁)", { positive: true });
        const c2 = parseField("dl-c2", "Concentración final (C₂)");
        const v2 = parseField("dl-v2", "Volumen final (V₂)");
        const c1 = (c2 * v2) / v1;
        addStep(`<strong>Fórmula:</strong> C₁ = (C₂ × V₂) / V₁`);
        addStep(`C₁ = (${fmt(c2)} × ${fmt(v2)}) / ${fmt(v1)} = <strong class="text-[var(--color-primary)]">${fmt(c1)}</strong>`);
      } else if (target === "V1") {
        const c1 = parseField("dl-c1", "Concentración inicial (C₁)", { positive: true });
        const c2 = parseField("dl-c2", "Concentración final (C₂)");
        const v2 = parseField("dl-v2", "Volumen final (V₂)");
        const v1 = (c2 * v2) / c1;
        addStep(`<strong>Fórmula:</strong> V₁ = (C₂ × V₂) / C₁`);
        addStep(`V₁ = (${fmt(c2)} × ${fmt(v2)}) / ${fmt(c1)} = <strong class="text-[var(--color-primary)]">${fmt(v1)}</strong>`);
      } else if (target === "C2") {
        const c1 = parseField("dl-c1", "Concentración inicial (C₁)");
        const v1 = parseField("dl-v1", "Volumen inicial (V₁)");
        const v2 = parseField("dl-v2", "Volumen final (V₂)", { positive: true });
        const c2 = (c1 * v1) / v2;
        addStep(`<strong>Fórmula:</strong> C₂ = (C₁ × V₁) / V₂`);
        addStep(`C₂ = (${fmt(c1)} × ${fmt(v1)}) / ${fmt(v2)} = <strong class="text-[var(--color-primary)]">${fmt(c2)}</strong>`);
      } else {
        const c1 = parseField("dl-c1", "Concentración inicial (C₁)");
        const v1 = parseField("dl-v1", "Volumen inicial (V₁)");
        const c2 = parseField("dl-c2", "Concentración final (C₂)", { positive: true });
        const v2 = (c1 * v1) / c2;
        addStep(`<strong>Fórmula:</strong> V₂ = (C₁ × V₁) / C₂`);
        addStep(`V₂ = (${fmt(c1)} × ${fmt(v1)}) / ${fmt(c2)} = <strong class="text-[var(--color-primary)]">${fmt(v2)}</strong>`);
      }

      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });

  render();
})();
