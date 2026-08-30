/**
 * Calculadora de IVA — 2 modos: "agregar IVA a un neto" y "discriminar IVA
 * de un total", con alícuotas de Argentina (21%, 10,5%, 27%) o una tasa
 * personalizada.
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

  const errorEl = document.getElementById("iva-error");
  const resultPanel = document.getElementById("iva-result-panel");
  const outNeto = document.getElementById("iva-out-neto");
  const outIva = document.getElementById("iva-out-iva");
  const outTotal = document.getElementById("iva-out-total");

  const fmt = (n) =>
    new Intl.NumberFormat("es-AR", { maximumFractionDigits: 2 }).format(
      Object.is(n, -0) ? 0 : Math.round(n * 100) / 100
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
  function parseField(id, label, { nonNegative = false } = {}) {
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
    if (nonNegative && value < 0) {
      el.classList.add("field-error");
      throw new Error(`El campo "${label}" no puede ser negativo.`);
    }
    return value;
  }
  function resolveRate(selectId, customWrapId, customInputId) {
    const select = document.getElementById(selectId);
    if (select.value !== "custom") return Number(select.value);
    document.getElementById(customWrapId).classList.remove("hidden");
    const rate = parseField(customInputId, "Alícuota personalizada", { nonNegative: true });
    return rate;
  }

  // -------------------------------------------------------------- Tabs ---
  const tabButtons = document.querySelectorAll(".iva-tab-btn");
  const panels = {
    agregar: document.getElementById("iva-panel-agregar"),
    discriminar: document.getElementById("iva-panel-discriminar"),
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

  // Mostrar/ocultar el campo de alícuota personalizada según el <select>.
  document.getElementById("add-rate").addEventListener("change", (e) => {
    document.getElementById("add-custom-wrap").classList.toggle("hidden", e.target.value !== "custom");
  });
  document.getElementById("sub-rate").addEventListener("change", (e) => {
    document.getElementById("sub-custom-wrap").classList.toggle("hidden", e.target.value !== "custom");
  });

  function renderResult(neto, iva, total) {
    outNeto.textContent = `$${fmt(neto)}`;
    outIva.textContent = `$${fmt(iva)}`;
    outTotal.textContent = `$${fmt(total)}`;
    resultPanel.classList.remove("hidden");
  }

  // ------------------------------------------------------ Modo: Agregar ---
  document.getElementById("add-solve").addEventListener("click", () => {
    clearError();
    try {
      const neto = parseField("add-monto", "Monto neto", { nonNegative: true });
      const rate = resolveRate("add-rate", "add-custom-wrap", "add-custom");
      const iva = neto * (rate / 100);
      const total = neto + iva;
      renderResult(neto, iva, total);
    } catch (err) {
      showError(err.message);
    }
  });

  // -------------------------------------------------- Modo: Discriminar ---
  document.getElementById("sub-solve").addEventListener("click", () => {
    clearError();
    try {
      const total = parseField("sub-monto", "Monto total", { nonNegative: true });
      const rate = resolveRate("sub-rate", "sub-custom-wrap", "sub-custom");
      const neto = total / (1 + rate / 100);
      const iva = total - neto;
      renderResult(neto, iva, total);
    } catch (err) {
      showError(err.message);
    }
  });

  setTab("agregar");
})();
