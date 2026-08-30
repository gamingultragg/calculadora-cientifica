/**
 * Cinemática (MRU / MRUA) — resuelve la variable pedida a partir de los
 * datos conocidos, con desarrollo paso a paso.
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

  const errorEl = document.getElementById("km-error");
  const resultPanel = document.getElementById("km-result-panel");
  const stepsEl = document.getElementById("km-steps");

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
  function parseField(id, label) {
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
    return value;
  }

  function fieldTemplate(id, label, unit) {
    return `
      <div>
        <label for="${id}" class="block text-sm font-medium mb-1">${label} <span class="text-[var(--color-text-muted)]">(${unit})</span></label>
        <input id="${id}" type="text" inputmode="decimal" placeholder="0"
          class="w-full rounded-xl surface px-3 py-2.5 font-numeric focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]" />
      </div>`;
  }

  // -------------------------------------------------------------- Tabs ---
  const tabButtons = document.querySelectorAll(".km-tab-btn");
  const panels = { mru: document.getElementById("km-panel-mru"), mrua: document.getElementById("km-panel-mrua") };

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

  // --------------------------------------------------------------- MRU ---
  const mruInputs = document.getElementById("mru-inputs");
  const mruTarget = document.getElementById("mru-target");

  function renderMru() {
    const target = mruTarget.value;
    if (target === "d") {
      mruInputs.innerHTML = fieldTemplate("mru-v", "Velocidad (v)", "m/s") + fieldTemplate("mru-t", "Tiempo (t)", "s");
    } else if (target === "v") {
      mruInputs.innerHTML = fieldTemplate("mru-d", "Distancia (d)", "m") + fieldTemplate("mru-t", "Tiempo (t)", "s");
    } else {
      mruInputs.innerHTML = fieldTemplate("mru-d", "Distancia (d)", "m") + fieldTemplate("mru-v", "Velocidad (v)", "m/s");
    }
  }
  mruTarget.addEventListener("change", () => {
    renderMru();
    clearError();
    resultPanel.classList.add("hidden");
  });

  document.getElementById("mru-solve").addEventListener("click", () => {
    clearError();
    try {
      const target = mruTarget.value;
      stepsEl.innerHTML = "";
      if (target === "d") {
        const v = parseField("mru-v", "Velocidad (v)");
        const t = parseField("mru-t", "Tiempo (t)");
        const d = v * t;
        addStep(`<strong>Fórmula:</strong> d = v × t`);
        addStep(`d = ${fmt(v)} × ${fmt(t)} = <strong class="text-[var(--color-primary)]">${fmt(d)} m</strong>`);
      } else if (target === "v") {
        const d = parseField("mru-d", "Distancia (d)");
        const t = parseField("mru-t", "Tiempo (t)");
        if (t === 0) throw new Error("El tiempo no puede ser 0 al calcular la velocidad.");
        const v = d / t;
        addStep(`<strong>Fórmula:</strong> v = d / t`);
        addStep(`v = ${fmt(d)} / ${fmt(t)} = <strong class="text-[var(--color-primary)]">${fmt(v)} m/s</strong>`);
      } else {
        const d = parseField("mru-d", "Distancia (d)");
        const v = parseField("mru-v", "Velocidad (v)");
        if (v === 0) throw new Error("La velocidad no puede ser 0 al calcular el tiempo.");
        const t = d / v;
        addStep(`<strong>Fórmula:</strong> t = d / v`);
        addStep(`t = ${fmt(d)} / ${fmt(v)} = <strong class="text-[var(--color-primary)]">${fmt(t)} s</strong>`);
      }
      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });

  // -------------------------------------------------------------- MRUA ---
  const mruaInputs = document.getElementById("mrua-inputs");
  const mruaTarget = document.getElementById("mrua-target");

  function renderMrua() {
    const target = mruaTarget.value;
    if (target === "vd") {
      mruaInputs.innerHTML =
        fieldTemplate("mrua-v0", "Velocidad inicial (v₀)", "m/s") +
        fieldTemplate("mrua-a", "Aceleración (a)", "m/s²") +
        fieldTemplate("mrua-t", "Tiempo (t)", "s");
    } else if (target === "v_from_d") {
      mruaInputs.innerHTML =
        fieldTemplate("mrua-v0", "Velocidad inicial (v₀)", "m/s") +
        fieldTemplate("mrua-a", "Aceleración (a)", "m/s²") +
        fieldTemplate("mrua-d", "Distancia (d)", "m");
    } else {
      mruaInputs.innerHTML =
        fieldTemplate("mrua-v0", "Velocidad inicial (v₀)", "m/s") +
        fieldTemplate("mrua-v", "Velocidad final (v)", "m/s") +
        fieldTemplate("mrua-a", "Aceleración (a)", "m/s²");
    }
  }
  mruaTarget.addEventListener("change", () => {
    renderMrua();
    clearError();
    resultPanel.classList.add("hidden");
  });

  document.getElementById("mrua-solve").addEventListener("click", () => {
    clearError();
    try {
      const target = mruaTarget.value;
      stepsEl.innerHTML = "";
      if (target === "vd") {
        const v0 = parseField("mrua-v0", "Velocidad inicial (v₀)");
        const a = parseField("mrua-a", "Aceleración (a)");
        const t = parseField("mrua-t", "Tiempo (t)");
        const v = v0 + a * t;
        const d = v0 * t + 0.5 * a * t * t;
        addStep(`<strong>Fórmula:</strong> v = v₀ + a·t`);
        addStep(`v = ${fmt(v0)} + (${fmt(a)})(${fmt(t)}) = <strong class="text-[var(--color-primary)]">${fmt(v)} m/s</strong>`);
        addStep(`<strong>Fórmula:</strong> d = v₀·t + ½·a·t²`);
        addStep(`d = ${fmt(v0)}(${fmt(t)}) + ½(${fmt(a)})(${fmt(t)})² = <strong class="text-[var(--color-primary)]">${fmt(d)} m</strong>`);
      } else if (target === "v_from_d") {
        const v0 = parseField("mrua-v0", "Velocidad inicial (v₀)");
        const a = parseField("mrua-a", "Aceleración (a)");
        const d = parseField("mrua-d", "Distancia (d)");
        const inner = v0 * v0 + 2 * a * d;
        addStep(`<strong>Fórmula:</strong> v² = v₀² + 2·a·d`);
        addStep(`v² = (${fmt(v0)})² + 2(${fmt(a)})(${fmt(d)}) = ${fmt(inner)}`);
        if (inner < 0) {
          throw new Error("No existe solución real: v₀² + 2·a·d es negativo (el móvil se detiene antes de recorrer esa distancia).");
        }
        const v = Math.sqrt(inner);
        addStep(`v = √${fmt(inner)} = <strong class="text-[var(--color-primary)]">${fmt(v)} m/s</strong>`);
      } else {
        const v0 = parseField("mrua-v0", "Velocidad inicial (v₀)");
        const v = parseField("mrua-v", "Velocidad final (v)");
        const a = parseField("mrua-a", "Aceleración (a)");
        if (a === 0) throw new Error("La aceleración no puede ser 0 al calcular el tiempo.");
        const t = (v - v0) / a;
        addStep(`<strong>Fórmula:</strong> t = (v − v₀) / a`);
        addStep(`t = (${fmt(v)} − ${fmt(v0)}) / ${fmt(a)} = <strong class="text-[var(--color-primary)]">${fmt(t)} s</strong>`);
      }
      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });

  // -------------------------------------------------------------- Init ---
  renderMru();
  renderMrua();
  setTab("mru");
})();
