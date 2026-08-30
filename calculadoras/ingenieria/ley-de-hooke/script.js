/**
 * Ley de Hooke — calcula F, k o x a partir de los otros dos valores
 * (F = k·x).
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

  const targetSelect = document.getElementById("hk-target");
  const inputsWrap = document.getElementById("hk-inputs");
  const errorEl = document.getElementById("hk-error");
  const resultPanel = document.getElementById("hk-result-panel");
  const stepsEl = document.getElementById("hk-steps");

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

  function render() {
    const target = targetSelect.value;
    if (target === "f") {
      inputsWrap.innerHTML = fieldTemplate("hk-k", "Constante del resorte (k)", "N/m") + fieldTemplate("hk-x", "Deformación (x)", "m");
    } else if (target === "k") {
      inputsWrap.innerHTML = fieldTemplate("hk-f", "Fuerza elástica (F)", "N") + fieldTemplate("hk-x", "Deformación (x)", "m");
    } else {
      inputsWrap.innerHTML = fieldTemplate("hk-f", "Fuerza elástica (F)", "N") + fieldTemplate("hk-k", "Constante del resorte (k)", "N/m");
    }
  }
  targetSelect.addEventListener("change", () => {
    render();
    clearError();
    resultPanel.classList.add("hidden");
  });

  document.getElementById("hk-solve").addEventListener("click", () => {
    clearError();
    stepsEl.innerHTML = "";
    try {
      const target = targetSelect.value;

      if (target === "f") {
        const k = parseField("hk-k", "Constante del resorte (k)");
        const x = parseField("hk-x", "Deformación (x)");
        const f = k * x;
        addStep(`<strong>Fórmula:</strong> F = k × x`);
        addStep(`F = ${fmt(k)} × ${fmt(x)} = <strong class="text-[var(--color-primary)]">${fmt(f)} N</strong>`);
      } else if (target === "k") {
        const f = parseField("hk-f", "Fuerza elástica (F)");
        const x = parseField("hk-x", "Deformación (x)");
        if (x === 0) throw new Error("La deformación no puede ser 0 al calcular la constante del resorte.");
        const k = f / x;
        addStep(`<strong>Fórmula:</strong> k = F / x`);
        addStep(`k = ${fmt(f)} / ${fmt(x)} = <strong class="text-[var(--color-primary)]">${fmt(k)} N/m</strong>`);
      } else {
        const f = parseField("hk-f", "Fuerza elástica (F)");
        const k = parseField("hk-k", "Constante del resorte (k)");
        if (k === 0) throw new Error("La constante del resorte no puede ser 0 al calcular la deformación.");
        const x = f / k;
        addStep(`<strong>Fórmula:</strong> x = F / k`);
        addStep(`x = ${fmt(f)} / ${fmt(k)} = <strong class="text-[var(--color-primary)]">${fmt(x)} m</strong>`);
      }

      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });

  render();
})();
