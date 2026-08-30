/**
 * Resistencias en Serie y Paralelo — lista dinámica de resistores con
 * cálculo automático de la resistencia total según la configuración.
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

  const form = document.getElementById("rs-form");
  const input = document.getElementById("rs-input");
  const errorEl = document.getElementById("rs-error");
  const chipsEl = document.getElementById("rs-chips");
  const chipsEmpty = document.getElementById("rs-chips-empty");
  const countEl = document.getElementById("rs-count");
  const clearBtn = document.getElementById("rs-clear");
  const resultPanel = document.getElementById("rs-result-panel");
  const totalEl = document.getElementById("rs-total");
  const configLabel = document.getElementById("rs-config-label");
  const configButtons = document.querySelectorAll(".rs-config-btn");

  let data = [];
  let config = "serie";

  const fmt = (n) =>
    new Intl.NumberFormat("es-AR", { maximumFractionDigits: 6 }).format(
      Object.is(n, -0) ? 0 : Math.round(n * 1e8) / 1e8
    );

  function showError(message) {
    errorEl.textContent = message;
    errorEl.classList.remove("hidden");
  }
  function clearError() {
    errorEl.classList.add("hidden");
    errorEl.textContent = "";
  }

  function setConfig(next) {
    config = next;
    configButtons.forEach((btn) => {
      const active = btn.dataset.config === config;
      btn.classList.toggle("bg-[var(--color-primary)]", active);
      btn.classList.toggle("text-white", active);
    });
    configLabel.textContent = config;
    recalculate();
  }
  configButtons.forEach((btn) => btn.addEventListener("click", () => setConfig(btn.dataset.config)));

  function renderChips() {
    chipsEl.querySelectorAll("[data-chip]").forEach((el) => el.remove());
    chipsEmpty.classList.toggle("hidden", data.length > 0);

    data.forEach((value, index) => {
      const chip = document.createElement("span");
      chip.dataset.chip = "true";
      chip.className =
        "inline-flex items-center gap-1.5 font-numeric text-sm rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)] px-3 py-1";
      chip.innerHTML = `${fmt(value)} Ω <button type="button" aria-label="Eliminar resistor ${fmt(value)} ohm" class="hover:text-[var(--color-danger)] font-bold">×</button>`;
      chip.querySelector("button").addEventListener("click", () => {
        data.splice(index, 1);
        renderChips();
        recalculate();
      });
      chipsEl.appendChild(chip);
    });

    countEl.textContent = String(data.length);
  }

  function recalculate() {
    clearError();
    if (data.length === 0) {
      resultPanel.classList.add("hidden");
      return;
    }
    let total;
    if (config === "serie") {
      total = data.reduce((sum, r) => sum + r, 0);
    } else {
      if (data.some((r) => r === 0)) {
        showError("Un resistor de 0 Ω en paralelo produce un cortocircuito (división por cero). Quitalo de la lista.");
        resultPanel.classList.add("hidden");
        return;
      }
      const sumInverse = data.reduce((sum, r) => sum + 1 / r, 0);
      total = 1 / sumInverse;
    }
    totalEl.textContent = `${fmt(total)} Ω`;
    resultPanel.classList.remove("hidden");
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    clearError();

    const raw = normalizeNumberInput(input.value);
    if (raw === "") {
      showError("Ingresá el valor del resistor antes de agregar.");
      return;
    }
    const value = Number(raw);
    if (!Number.isFinite(value) || value < 0) {
      showError(`"${input.value}" no es un valor de resistencia válido.`);
      return;
    }

    data.push(value);
    input.value = "";
    input.focus();
    renderChips();
    recalculate();
  });

  clearBtn.addEventListener("click", () => {
    data = [];
    clearError();
    renderChips();
    recalculate();
  });

  renderChips();
  setConfig("serie");
})();
