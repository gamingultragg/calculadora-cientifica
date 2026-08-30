/**
 * Permutaciones y Combinaciones — análisis combinatorio con y sin
 * repetición, más factorial simple, usando productos iterativos para
 * mantener buena precisión numérica en valores grandes.
 */
(function () {
  const modeSelect = document.getElementById("pc-mode");
  const rWrap = document.getElementById("pc-r-wrap");
  const errorEl = document.getElementById("pc-error");
  const resultPanel = document.getElementById("pc-result-panel");
  const stepsEl = document.getElementById("pc-steps");

  const fmt = (n) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: 0 }).format(n);

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

  function parseNonNegativeInt(id, label) {
    const el = document.getElementById(id);
    el.classList.remove("field-error");
    const raw = el.value.trim().replace(",", ".");
    if (raw === "") {
      el.classList.add("field-error");
      throw new Error(`El campo "${label}" no puede estar vacío.`);
    }
    const value = Number(raw);
    if (!Number.isFinite(value) || value < 0 || Math.abs(value - Math.round(value)) > 1e-9) {
      el.classList.add("field-error");
      throw new Error(`El campo "${label}" debe ser un número entero mayor o igual a 0.`);
    }
    if (value > 1000) {
      el.classList.add("field-error");
      throw new Error(`El campo "${label}" es demasiado grande (máximo 1000).`);
    }
    return Math.round(value);
  }

  function factorial(n) {
    let result = 1;
    for (let k = 2; k <= n; k++) result *= k;
    return result;
  }

  // Producto n*(n-1)*...*(n-r+1), evitando calcular factoriales enormes innecesarios.
  function fallingProduct(n, r) {
    let result = 1;
    for (let k = 0; k < r; k++) result *= n - k;
    return result;
  }

  // C(n,r) por fórmula multiplicativa: mantiene los resultados intermedios enteros.
  function combination(n, r) {
    r = Math.min(r, n - r);
    let result = 1;
    for (let i = 1; i <= r; i++) result = (result * (n - r + i)) / i;
    return Math.round(result);
  }

  modeSelect.addEventListener("change", () => {
    rWrap.classList.toggle("hidden", modeSelect.value === "fact");
    clearError();
    resultPanel.classList.add("hidden");
  });

  document.getElementById("pc-solve").addEventListener("click", () => {
    clearError();
    document.querySelectorAll("#pc-n, #pc-r").forEach((el) => el.classList.remove("field-error"));
    stepsEl.innerHTML = "";

    try {
      const mode = modeSelect.value;
      const n = parseNonNegativeInt("pc-n", "n");

      if (mode === "fact") {
        const result = factorial(n);
        addStep(`<strong>Fórmula:</strong> n! = n × (n-1) × … × 1`);
        addStep(`${fmt(n)}! = <strong class="text-[var(--color-primary)]">${fmt(result)}</strong>`);
        resultPanel.classList.remove("hidden");
        return;
      }

      const r = parseNonNegativeInt("pc-r", "r");

      if (mode === "perm") {
        if (r > n) throw new Error("r no puede ser mayor que n en permutaciones sin repetición.");
        const result = fallingProduct(n, r);
        addStep(`<strong>Fórmula:</strong> P(n,r) = n! / (n − r)!`);
        addStep(`P(${fmt(n)},${fmt(r)}) = ${fmt(n)} × ${fmt(n - 1)} × … × ${fmt(n - r + 1)} = <strong class="text-[var(--color-primary)]">${fmt(result)}</strong>`);
      } else if (mode === "comb") {
        if (r > n) throw new Error("r no puede ser mayor que n en combinaciones sin repetición.");
        const result = combination(n, r);
        addStep(`<strong>Fórmula:</strong> C(n,r) = n! / (r!(n − r)!)`);
        addStep(`C(${fmt(n)},${fmt(r)}) = <strong class="text-[var(--color-primary)]">${fmt(result)}</strong>`);
      } else if (mode === "perm_rep") {
        const result = Math.pow(n, r);
        addStep(`<strong>Fórmula:</strong> nʳ`);
        addStep(`${fmt(n)}^${fmt(r)} = <strong class="text-[var(--color-primary)]">${fmt(result)}</strong>`);
      } else if (mode === "comb_rep") {
        const result = combination(n + r - 1, r);
        addStep(`<strong>Fórmula:</strong> C(n + r − 1, r)`);
        addStep(`C(${fmt(n)} + ${fmt(r)} − 1, ${fmt(r)}) = C(${fmt(n + r - 1)},${fmt(r)}) = <strong class="text-[var(--color-primary)]">${fmt(result)}</strong>`);
      }

      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });
})();
