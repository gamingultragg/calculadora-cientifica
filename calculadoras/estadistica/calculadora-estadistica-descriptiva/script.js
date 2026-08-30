/**
 * Estadística Descriptiva — lista dinámica de datos con cálculo automático
 * de media, mediana, moda, varianza, desviación estándar y rango.
 */
(function () {
  const form = document.getElementById("ed-form");
  const input = document.getElementById("ed-input");
  const errorEl = document.getElementById("ed-error");
  const chipsEl = document.getElementById("ed-chips");
  const chipsEmpty = document.getElementById("ed-chips-empty");
  const countEl = document.getElementById("ed-count");
  const clearBtn = document.getElementById("ed-clear");
  const resultPanel = document.getElementById("ed-result-panel");
  const noteEl = document.getElementById("ed-note");

  const fields = {
    mean: document.getElementById("ed-mean"),
    median: document.getElementById("ed-median"),
    mode: document.getElementById("ed-mode"),
    range: document.getElementById("ed-range"),
    varSample: document.getElementById("ed-var-sample"),
    stdSample: document.getElementById("ed-std-sample"),
    varPop: document.getElementById("ed-var-pop"),
    stdPop: document.getElementById("ed-std-pop"),
  };

  let data = [];

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

  function renderChips() {
    chipsEl.querySelectorAll("[data-chip]").forEach((el) => el.remove());
    chipsEmpty.classList.toggle("hidden", data.length > 0);

    data.forEach((value, index) => {
      const chip = document.createElement("span");
      chip.dataset.chip = "true";
      chip.className =
        "inline-flex items-center gap-1.5 font-numeric text-sm rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)] px-3 py-1";
      chip.innerHTML = `${fmt(value)} <button type="button" aria-label="Eliminar dato ${fmt(value)}" class="hover:text-[var(--color-danger)] font-bold">×</button>`;
      chip.querySelector("button").addEventListener("click", () => {
        data.splice(index, 1);
        renderChips();
        recalculate();
      });
      chipsEl.appendChild(chip);
    });

    countEl.textContent = String(data.length);
  }

  function mean(values) {
    return values.reduce((sum, v) => sum + v, 0) / values.length;
  }

  function median(values) {
    const sorted = [...values].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    return sorted.length % 2 === 0 ? (sorted[mid - 1] + sorted[mid]) / 2 : sorted[mid];
  }

  function modes(values) {
    const freq = new Map();
    values.forEach((v) => freq.set(v, (freq.get(v) || 0) + 1));
    const maxFreq = Math.max(...freq.values());
    if (maxFreq === 1) return { values: [], maxFreq };
    const modalValues = [...freq.entries()].filter(([, f]) => f === maxFreq).map(([v]) => v);
    return { values: modalValues.sort((a, b) => a - b), maxFreq };
  }

  function variance(values, avg, divisor) {
    const sumSquares = values.reduce((sum, v) => sum + (v - avg) ** 2, 0);
    return sumSquares / divisor;
  }

  function recalculate() {
    if (data.length === 0) {
      resultPanel.classList.add("hidden");
      return;
    }

    resultPanel.classList.remove("hidden");
    const n = data.length;
    const avg = mean(data);
    const med = median(data);
    const { values: modalValues } = modes(data);
    const range = Math.max(...data) - Math.min(...data);

    fields.mean.textContent = fmt(avg);
    fields.median.textContent = fmt(med);
    fields.mode.textContent = modalValues.length === 0 ? "Sin moda" : modalValues.map(fmt).join(", ");
    fields.range.textContent = fmt(range);

    if (n >= 2) {
      const varSample = variance(data, avg, n - 1);
      fields.varSample.textContent = fmt(varSample);
      fields.stdSample.textContent = fmt(Math.sqrt(varSample));
      noteEl.textContent = "";
    } else {
      fields.varSample.textContent = "N/D";
      fields.stdSample.textContent = "N/D";
      noteEl.textContent = "Se necesitan al menos 2 datos para calcular la varianza y desviación estándar muestral.";
    }

    const varPop = variance(data, avg, n);
    fields.varPop.textContent = fmt(varPop);
    fields.stdPop.textContent = fmt(Math.sqrt(varPop));
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    clearError();

    const raw = input.value.trim().replace(",", ".");
    if (raw === "") {
      showError("Ingresá un valor numérico antes de agregar.");
      return;
    }
    const value = Number(raw);
    if (!Number.isFinite(value)) {
      showError(`"${input.value}" no es un número válido.`);
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
})();
