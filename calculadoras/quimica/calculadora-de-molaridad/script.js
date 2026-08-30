/**
 * Calculadora de Molaridad — interconvierte M, n y V, y calcula moles a
 * partir de la masa y la masa molar.
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

  const errorEl = document.getElementById("ml-error");
  const resultPanel = document.getElementById("ml-result-panel");
  const stepsEl = document.getElementById("ml-steps");

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
  function fieldTemplate(id, label, unit) {
    return `
      <div>
        <label for="${id}" class="block text-sm font-medium mb-1">${label} <span class="text-[var(--color-text-muted)]">(${unit})</span></label>
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

  // -------------------------------------------------------------- Tabs ---
  const tabButtons = document.querySelectorAll(".ml-tab-btn");
  const panels = { molaridad: document.getElementById("ml-panel-molaridad"), masa: document.getElementById("ml-panel-masa") };
  function setTab(tab) {
    tabButtons.forEach((btn) => {
      const active = btn.dataset.tab === tab;
      btn.classList.toggle("bg-[var(--color-primary)]", active);
      btn.classList.toggle("text-white", active);
    });
    Object.entries(panels).forEach(([key, el]) => el.classList.toggle("hidden", key !== tab));
    clearError();
    resultPanel.classList.add("hidden");
  }
  tabButtons.forEach((btn) => btn.addEventListener("click", () => setTab(btn.dataset.tab)));

  // --------------------------------------------------------- Molaridad ---
  const targetSelect = document.getElementById("ml-target");
  const inputsWrap = document.getElementById("ml-inputs");

  function renderMolaridad() {
    const target = targetSelect.value;
    if (target === "M") {
      inputsWrap.innerHTML = fieldTemplate("ml-n", "Moles (n)", "mol") + fieldTemplate("ml-v", "Volumen (V)", "L");
    } else if (target === "n") {
      inputsWrap.innerHTML = fieldTemplate("ml-m", "Molaridad (M)", "mol/L") + fieldTemplate("ml-v", "Volumen (V)", "L");
    } else {
      inputsWrap.innerHTML = fieldTemplate("ml-n", "Moles (n)", "mol") + fieldTemplate("ml-m", "Molaridad (M)", "mol/L");
    }
  }
  targetSelect.addEventListener("change", () => {
    renderMolaridad();
    clearError();
    resultPanel.classList.add("hidden");
  });

  document.getElementById("ml-solve").addEventListener("click", () => {
    clearError();
    stepsEl.innerHTML = "";
    try {
      const target = targetSelect.value;
      if (target === "M") {
        const n = parseField("ml-n", "Moles (n)");
        const v = parseField("ml-v", "Volumen (V)", { positive: true });
        const m = n / v;
        addStep(`<strong>Fórmula:</strong> M = n / V`);
        addStep(`M = ${fmt(n)} / ${fmt(v)} = <strong class="text-[var(--color-primary)]">${fmt(m)} mol/L</strong>`);
      } else if (target === "n") {
        const m = parseField("ml-m", "Molaridad (M)");
        const v = parseField("ml-v", "Volumen (V)", { positive: true });
        const n = m * v;
        addStep(`<strong>Fórmula:</strong> n = M × V`);
        addStep(`n = ${fmt(m)} × ${fmt(v)} = <strong class="text-[var(--color-primary)]">${fmt(n)} mol</strong>`);
      } else {
        const n = parseField("ml-n", "Moles (n)");
        const m = parseField("ml-m", "Molaridad (M)", { positive: true });
        const v = n / m;
        addStep(`<strong>Fórmula:</strong> V = n / M`);
        addStep(`V = ${fmt(n)} / ${fmt(m)} = <strong class="text-[var(--color-primary)]">${fmt(v)} L</strong>`);
      }
      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });

  // ---------------------------------------------------- Moles desde masa -
  document.getElementById("ml-masa-solve").addEventListener("click", () => {
    clearError();
    stepsEl.innerHTML = "";
    try {
      const masa = parseField("ml-masa", "Masa", { positive: true });
      const masaMolar = parseField("ml-masa-molar", "Masa molar", { positive: true });
      const n = masa / masaMolar;
      addStep(`<strong>Fórmula:</strong> n = masa / masa molar`);
      addStep(`n = ${fmt(masa)} / ${fmt(masaMolar)} = <strong class="text-[var(--color-primary)]">${fmt(n)} mol</strong>`);
      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });

  renderMolaridad();
  setTab("molaridad");
})();
