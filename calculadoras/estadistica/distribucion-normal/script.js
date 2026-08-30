/**
 * Distribución Normal (Puntaje Z) — calcula z = (x-μ)/σ y la probabilidad
 * acumulada P(Z≤z) usando una aproximación numérica de la función erf
 * (Abramowitz & Stegun 7.1.26, error máximo ~1.5e-7).
 */
(function () {
  const form = document.getElementById("dn-form");
  const errorEl = document.getElementById("dn-error");
  const resultPanel = document.getElementById("dn-result-panel");
  const noteEl = document.getElementById("dn-note");

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

  function erf(x) {
    const sign = x < 0 ? -1 : 1;
    x = Math.abs(x);
    const a1 = 0.254829592,
      a2 = -0.284496736,
      a3 = 1.421413741,
      a4 = -1.453152027,
      a5 = 1.061405429,
      p = 0.3275911;
    const t = 1 / (1 + p * x);
    const y = 1 - ((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
    return sign * y;
  }

  function normalCdf(z) {
    return 0.5 * (1 + erf(z / Math.SQRT2));
  }

  function parseField(id, label, { positive = false } = {}) {
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
    if (positive && value <= 0) {
      el.classList.add("field-error");
      throw new Error(`El campo "${label}" debe ser mayor a 0.`);
    }
    return value;
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    clearError();
    document.querySelectorAll("#dn-form input").forEach((input) => input.classList.remove("field-error"));

    try {
      const x = parseField("dn-x", "Valor (x)");
      const mean = parseField("dn-mean", "Media (μ)");
      const std = parseField("dn-std", "Desvío estándar (σ)", { positive: true });

      const z = (x - mean) / std;
      const p = normalCdf(z);

      document.getElementById("dn-z").textContent = fmt(z);
      document.getElementById("dn-p").textContent = `${fmt(p * 100)}%`;
      noteEl.textContent = `El valor x = ${fmt(x)} está ${fmt(Math.abs(z))} desvíos estándar ${z >= 0 ? "por encima" : "por debajo"} de la media. Aproximadamente el ${fmt(p * 100)}% de los datos son menores o iguales a este valor.`;

      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });
})();
