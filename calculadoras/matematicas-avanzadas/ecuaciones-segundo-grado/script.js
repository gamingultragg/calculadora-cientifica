/**
 * Ecuaciones de Segundo Grado — resolución por fórmula cuadrática con
 * desarrollo paso a paso y soporte de raíces complejas.
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

  const form = document.getElementById("eq-form");
  const clearBtn = document.getElementById("eq-clear");
  const errorEl = document.getElementById("eq-error");
  const resultPanel = document.getElementById("eq-result-panel");
  const stepsEl = document.getElementById("eq-steps");
  const rootsEl = document.getElementById("eq-roots");

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

  function parseCoefficient(rawValue, fieldLabel) {
    const trimmed = normalizeNumberInput((rawValue ?? ""));
    if (trimmed === "") {
      throw new Error(`El campo "${fieldLabel}" no puede estar vacío.`);
    }
    const value = Number(trimmed);
    if (!Number.isFinite(value)) {
      throw new Error(`El campo "${fieldLabel}" debe ser un número válido.`);
    }
    return value;
  }

  function addStep(html) {
    const li = document.createElement("li");
    li.innerHTML = html;
    stepsEl.appendChild(li);
  }

  function solve(a, b, c) {
    if (a === 0) {
      throw new Error("El coeficiente \"a\" no puede ser 0 (dejaría de ser una ecuación cuadrática).");
    }

    stepsEl.innerHTML = "";
    addStep(`<strong>1.</strong> Identificar coeficientes: a = ${fmt(a)}, b = ${fmt(b)}, c = ${fmt(c)}`);
    addStep(`<strong>2.</strong> Aplicar la fórmula: x = (-b ± √(b² - 4ac)) / 2a`);

    const discriminant = b * b - 4 * a * c;
    addStep(
      `<strong>3.</strong> Calcular el discriminante: Δ = b² - 4ac = (${fmt(b)})² - 4(${fmt(a)})(${fmt(c)}) = ${fmt(discriminant)}`
    );

    const twoA = 2 * a;

    if (discriminant > 0) {
      const sqrtD = Math.sqrt(discriminant);
      const x1 = (-b + sqrtD) / twoA;
      const x2 = (-b - sqrtD) / twoA;
      addStep(`<strong>4.</strong> Como Δ &gt; 0, hay dos raíces reales distintas.`);
      addStep(`<strong>5.</strong> x₁ = (${fmt(-b)} + √${fmt(discriminant)}) / ${fmt(twoA)} = ${fmt(x1)}`);
      addStep(`<strong>6.</strong> x₂ = (${fmt(-b)} − √${fmt(discriminant)}) / ${fmt(twoA)} = ${fmt(x2)}`);
      rootsEl.innerHTML = `x₁ = ${fmt(x1)} &nbsp;&nbsp; x₂ = ${fmt(x2)}`;
    } else if (discriminant === 0) {
      const x = -b / twoA;
      addStep(`<strong>4.</strong> Como Δ = 0, hay una única raíz real doble.`);
      addStep(`<strong>5.</strong> x = -b / 2a = ${fmt(-b)} / ${fmt(twoA)} = ${fmt(x)}`);
      rootsEl.innerHTML = `x = ${fmt(x)} (raíz doble)`;
    } else {
      const realPart = -b / twoA;
      const imagPart = Math.sqrt(-discriminant) / twoA;
      addStep(`<strong>4.</strong> Como Δ &lt; 0, no hay raíces reales: las soluciones son complejas.`);
      addStep(
        `<strong>5.</strong> x = ${fmt(-b)} / ${fmt(twoA)} ± (√${fmt(-discriminant)} / ${fmt(twoA)})i`
      );
      rootsEl.innerHTML = `x₁ = ${fmt(realPart)} + ${fmt(imagPart)}i &nbsp;&nbsp; x₂ = ${fmt(realPart)} − ${fmt(imagPart)}i`;
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    clearError();
    document.querySelectorAll("#eq-form input").forEach((input) => input.classList.remove("field-error"));

    try {
      const a = parseCoefficient(document.getElementById("eq-a").value, "a");
      const b = parseCoefficient(document.getElementById("eq-b").value, "b");
      const c = parseCoefficient(document.getElementById("eq-c").value, "c");
      solve(a, b, c);
      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });

  clearBtn.addEventListener("click", () => {
    form.reset();
    clearError();
    resultPanel.classList.add("hidden");
    document.querySelectorAll("#eq-form input").forEach((input) => input.classList.remove("field-error"));
  });
})();
