/**
 * Ley de Ohm — calcula V, I o R a partir de los otros dos valores, y la
 * potencia eléctrica resultante.
 */
(function () {
  const targetSelect = document.getElementById("oh-target");
  const inputsWrap = document.getElementById("oh-inputs");
  const errorEl = document.getElementById("oh-error");
  const resultPanel = document.getElementById("oh-result-panel");
  const stepsEl = document.getElementById("oh-steps");

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
    if (target === "v") {
      inputsWrap.innerHTML = fieldTemplate("oh-i", "Corriente (I)", "A") + fieldTemplate("oh-r", "Resistencia (R)", "Ω");
    } else if (target === "i") {
      inputsWrap.innerHTML = fieldTemplate("oh-v", "Voltaje (V)", "V") + fieldTemplate("oh-r", "Resistencia (R)", "Ω");
    } else {
      inputsWrap.innerHTML = fieldTemplate("oh-v", "Voltaje (V)", "V") + fieldTemplate("oh-i", "Corriente (I)", "A");
    }
  }
  targetSelect.addEventListener("change", () => {
    render();
    clearError();
    resultPanel.classList.add("hidden");
  });

  document.getElementById("oh-solve").addEventListener("click", () => {
    clearError();
    stepsEl.innerHTML = "";
    try {
      const target = targetSelect.value;
      let v, i, r;

      if (target === "v") {
        i = parseField("oh-i", "Corriente (I)");
        r = parseField("oh-r", "Resistencia (R)");
        v = i * r;
        addStep(`<strong>Fórmula:</strong> V = I × R`);
        addStep(`V = ${fmt(i)} × ${fmt(r)} = <strong class="text-[var(--color-primary)]">${fmt(v)} V</strong>`);
      } else if (target === "i") {
        v = parseField("oh-v", "Voltaje (V)");
        r = parseField("oh-r", "Resistencia (R)");
        if (r === 0) throw new Error("La resistencia no puede ser 0 al calcular la corriente.");
        i = v / r;
        addStep(`<strong>Fórmula:</strong> I = V / R`);
        addStep(`I = ${fmt(v)} / ${fmt(r)} = <strong class="text-[var(--color-primary)]">${fmt(i)} A</strong>`);
      } else {
        v = parseField("oh-v", "Voltaje (V)");
        i = parseField("oh-i", "Corriente (I)");
        if (i === 0) throw new Error("La corriente no puede ser 0 al calcular la resistencia.");
        r = v / i;
        addStep(`<strong>Fórmula:</strong> R = V / I`);
        addStep(`R = ${fmt(v)} / ${fmt(i)} = <strong class="text-[var(--color-primary)]">${fmt(r)} Ω</strong>`);
      }

      const p = v * i;
      addStep(`<strong>Potencia:</strong> P = V × I = ${fmt(v)} × ${fmt(i)} = <strong class="text-[var(--color-accent)]">${fmt(p)} W</strong>`);

      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });

  render();
})();
