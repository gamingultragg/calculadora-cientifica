/**
 * Calculadora de Porcentajes — 3 modos: "¿cuánto es X% de Y?", "¿X es qué
 * % de Y?" y "variación porcentual entre A y B".
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

  const errorEl = document.getElementById("pj-error");
  const resultPanel = document.getElementById("pj-result-panel");
  const resultEl = document.getElementById("pj-result");
  const detailEl = document.getElementById("pj-detail");

  const fmt = (n) =>
    new Intl.NumberFormat("es-AR", { maximumFractionDigits: 4 }).format(
      Object.is(n, -0) ? 0 : Math.round(n * 1e6) / 1e6
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
  function parseField(id, label, { nonZero = false } = {}) {
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
    if (nonZero && value === 0) {
      el.classList.add("field-error");
      throw new Error(`El campo "${label}" no puede ser 0.`);
    }
    return value;
  }

  // -------------------------------------------------------------- Tabs ---
  const tabButtons = document.querySelectorAll(".pc-tab-btn");
  const panels = {
    de: document.getElementById("pj-panel-de"),
    es: document.getElementById("pj-panel-es"),
    var: document.getElementById("pj-panel-var"),
  };
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

  // -------------------------------------------------------- Modo: X% de Y
  document.getElementById("de-solve").addEventListener("click", () => {
    clearError();
    try {
      const x = parseField("de-x", "Porcentaje (%)");
      const y = parseField("de-y", "Del valor");
      const result = y * (x / 100);
      resultEl.textContent = fmt(result);
      detailEl.textContent = `El ${fmt(x)}% de ${fmt(y)} es ${fmt(result)}.`;
      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });

  // -------------------------------------------------------- Modo: X es %Y
  document.getElementById("es-solve").addEventListener("click", () => {
    clearError();
    try {
      const x = parseField("es-x", "Valor (X)");
      const y = parseField("es-y", "Es porcentaje de (Y)", { nonZero: true });
      const result = (x / y) * 100;
      resultEl.textContent = `${fmt(result)}%`;
      detailEl.textContent = `${fmt(x)} es el ${fmt(result)}% de ${fmt(y)}.`;
      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });

  // ------------------------------------------------ Modo: variación (A→B)
  document.getElementById("var-solve").addEventListener("click", () => {
    clearError();
    try {
      const a = parseField("var-a", "Valor inicial (A)", { nonZero: true });
      const b = parseField("var-b", "Valor final (B)");
      const variacion = ((b - a) / a) * 100;
      const signo = variacion >= 0 ? "+" : "";
      resultEl.textContent = `${signo}${fmt(variacion)}%`;
      detailEl.textContent =
        variacion >= 0
          ? `De ${fmt(a)} a ${fmt(b)} hay un aumento del ${fmt(Math.abs(variacion))}%.`
          : `De ${fmt(a)} a ${fmt(b)} hay una disminución del ${fmt(Math.abs(variacion))}%.`;
      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });

  setTab("de");
})();
