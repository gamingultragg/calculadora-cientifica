/**
 * Segunda Ley de Newton — calcula F, m o a a partir de los otros dos
 * valores (F = m·a).
 */
(function () {
  const targetSelect = document.getElementById("nw-target");
  const inputsWrap = document.getElementById("nw-inputs");
  const errorEl = document.getElementById("nw-error");
  const resultPanel = document.getElementById("nw-result-panel");
  const stepsEl = document.getElementById("nw-steps");

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
    const raw = el.value.trim().replace(",", ".");
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
      inputsWrap.innerHTML = fieldTemplate("nw-m", "Masa (m)", "kg") + fieldTemplate("nw-a", "Aceleración (a)", "m/s²");
    } else if (target === "m") {
      inputsWrap.innerHTML = fieldTemplate("nw-f", "Fuerza (F)", "N") + fieldTemplate("nw-a", "Aceleración (a)", "m/s²");
    } else {
      inputsWrap.innerHTML = fieldTemplate("nw-f", "Fuerza (F)", "N") + fieldTemplate("nw-m", "Masa (m)", "kg");
    }
  }
  targetSelect.addEventListener("change", () => {
    render();
    clearError();
    resultPanel.classList.add("hidden");
  });

  document.getElementById("nw-solve").addEventListener("click", () => {
    clearError();
    stepsEl.innerHTML = "";
    try {
      const target = targetSelect.value;

      if (target === "f") {
        const m = parseField("nw-m", "Masa (m)");
        const a = parseField("nw-a", "Aceleración (a)");
        const f = m * a;
        addStep(`<strong>Fórmula:</strong> F = m × a`);
        addStep(`F = ${fmt(m)} × ${fmt(a)} = <strong class="text-[var(--color-primary)]">${fmt(f)} N</strong>`);
      } else if (target === "m") {
        const f = parseField("nw-f", "Fuerza (F)");
        const a = parseField("nw-a", "Aceleración (a)");
        if (a === 0) throw new Error("La aceleración no puede ser 0 al calcular la masa.");
        const m = f / a;
        addStep(`<strong>Fórmula:</strong> m = F / a`);
        addStep(`m = ${fmt(f)} / ${fmt(a)} = <strong class="text-[var(--color-primary)]">${fmt(m)} kg</strong>`);
      } else {
        const f = parseField("nw-f", "Fuerza (F)");
        const m = parseField("nw-m", "Masa (m)");
        if (m === 0) throw new Error("La masa no puede ser 0 al calcular la aceleración.");
        const a = f / m;
        addStep(`<strong>Fórmula:</strong> a = F / m`);
        addStep(`a = ${fmt(f)} / ${fmt(m)} = <strong class="text-[var(--color-primary)]">${fmt(a)} m/s²</strong>`);
      }

      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });

  render();
})();
