/**
 * Interés Compuesto — capital final, total aportado e interés ganado,
 * con aportes periódicos opcionales (anualidad ordinaria).
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

  const form = document.getElementById("ic-form");
  const errorEl = document.getElementById("ic-error");
  const resultPanel = document.getElementById("ic-result-panel");
  const stepsEl = document.getElementById("ic-steps");

  const out = {
    final: document.getElementById("ic-final"),
    contributed: document.getElementById("ic-contributed"),
    interest: document.getElementById("ic-interest"),
  };

  const fmtMoney = (n) =>
    new Intl.NumberFormat("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(
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
  function addStep(html) {
    const li = document.createElement("li");
    li.innerHTML = html;
    stepsEl.appendChild(li);
  }

  function parseRequired(id, label, { allowZero = true } = {}) {
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
    if (value < 0 || (!allowZero && value === 0)) {
      el.classList.add("field-error");
      throw new Error(`El campo "${label}" debe ser mayor a 0.`);
    }
    return value;
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    clearError();
    document.querySelectorAll("#ic-form input").forEach((input) => input.classList.remove("field-error"));

    try {
      const principal = parseRequired("ic-principal", "Capital inicial");
      const ratePercent = parseRequired("ic-rate", "Tasa de interés anual (%)");
      const years = parseRequired("ic-years", "Tiempo (años)", { allowZero: false });
      const n = Number(document.getElementById("ic-frequency").value);

      const contributionRaw = normalizeNumberInput(document.getElementById("ic-contribution").value);
      let contribution = 0;
      if (contributionRaw !== "") {
        contribution = Number(contributionRaw);
        if (!Number.isFinite(contribution) || contribution < 0) {
          document.getElementById("ic-contribution").classList.add("field-error");
          throw new Error('El campo "Aporte por período" debe ser un número mayor o igual a 0.');
        }
      }

      const r = ratePercent / 100;
      const periods = n * years;
      const ratePerPeriod = r / n;

      const growthFactor = Math.pow(1 + ratePerPeriod, periods);
      const principalFV = principal * growthFactor;
      const contributionsFV =
        contribution > 0
          ? ratePerPeriod === 0
            ? contribution * periods
            : contribution * ((growthFactor - 1) / ratePerPeriod)
          : 0;

      const finalAmount = principalFV + contributionsFV;
      const totalContributed = principal + contribution * periods;
      const interestEarned = finalAmount - totalContributed;

      stepsEl.innerHTML = "";
      addStep(`<strong>Fórmula:</strong> A = P × (1 + r/n)^(n·t)`);
      addStep(
        `Capital compuesto: ${fmtMoney(principal)} × (1 + ${fmtMoney(ratePerPeriod)})^${fmt0(periods)} = ${fmtMoney(principalFV)}`
      );
      if (contribution > 0) {
        addStep(`<strong>Fórmula aportes:</strong> PMT × [((1 + r/n)^(n·t) − 1) / (r/n)]`);
        addStep(`Valor futuro de los aportes: ${fmtMoney(contributionsFV)} (${fmt0(periods)} aportes de ${fmtMoney(contribution)})`);
      }
      addStep(`<strong>Total (capital + aportes):</strong> ${fmtMoney(finalAmount)}`);

      out.final.textContent = fmtMoney(finalAmount);
      out.contributed.textContent = fmtMoney(totalContributed);
      out.interest.textContent = fmtMoney(interestEarned);
      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });

  function fmt0(n) {
    return new Intl.NumberFormat("es-AR", { maximumFractionDigits: 2 }).format(n);
  }
})();
