/**
 * Calculadora de Matrices 2×2 y 3×3 — determinante, inversa, transpuesta y
 * multiplicación, con validación estricta de entradas vacías o inválidas.
 */
(function () {
  const gridA = document.getElementById("mx-grid-a");
  const gridB = document.getElementById("mx-grid-b");
  const errorEl = document.getElementById("mx-error");
  const resultPanel = document.getElementById("mx-result-panel");
  const resultTitle = document.getElementById("mx-result-title");
  const resultBody = document.getElementById("mx-result-body");
  const sizeButtons = document.querySelectorAll(".mx-size-btn");

  let size = 2;

  const fmt = (n) =>
    new Intl.NumberFormat("es-AR", { maximumFractionDigits: 6 }).format(
      Object.is(n, -0) ? 0 : Math.round(n * 1e8) / 1e8
    );

  // ---------------------------------------------------------------- UI ---
  function buildGrid(container, prefix) {
    container.innerHTML = "";
    container.style.gridTemplateColumns = `repeat(${size}, minmax(0, 1fr))`;
    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        const input = document.createElement("input");
        input.type = "text";
        input.inputMode = "decimal";
        input.placeholder = "0";
        input.dataset.row = String(r);
        input.dataset.col = String(c);
        input.id = `${prefix}-${r}-${c}`;
        input.className =
          "w-16 sm:w-20 text-center rounded-lg surface px-2 py-2 font-numeric focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]";
        container.appendChild(input);
      }
    }
  }

  function setSize(newSize) {
    size = newSize;
    sizeButtons.forEach((btn) => {
      const active = Number(btn.dataset.size) === size;
      btn.classList.toggle("bg-[var(--color-primary)]", active);
      btn.classList.toggle("text-white", active);
    });
    buildGrid(gridA, "a");
    buildGrid(gridB, "b");
    hideResult();
    clearError();
  }

  sizeButtons.forEach((btn) => btn.addEventListener("click", () => setSize(Number(btn.dataset.size))));

  function showError(message) {
    errorEl.textContent = message;
    errorEl.classList.remove("hidden");
    hideResult();
  }
  function clearError() {
    errorEl.classList.add("hidden");
    errorEl.textContent = "";
  }
  function hideResult() {
    resultPanel.classList.add("hidden");
  }

  function readMatrix(prefix) {
    const matrix = [];
    for (let r = 0; r < size; r++) {
      const row = [];
      for (let c = 0; c < size; c++) {
        const el = document.getElementById(`${prefix}-${r}-${c}`);
        const raw = el.value.trim().replace(",", ".");
        el.classList.remove("field-error");
        if (raw === "") {
          el.classList.add("field-error");
          throw new Error(`Completá todos los campos de la matriz ${prefix.toUpperCase()} (falta la celda fila ${r + 1}, columna ${c + 1}).`);
        }
        const value = Number(raw);
        if (!Number.isFinite(value)) {
          el.classList.add("field-error");
          throw new Error(`El valor en la fila ${r + 1}, columna ${c + 1} de la matriz ${prefix.toUpperCase()} no es un número válido.`);
        }
        row.push(value);
      }
      matrix.push(row);
    }
    return matrix;
  }

  // ------------------------------------------------------------- Álgebra --
  function minor(m, row, col) {
    return m
      .filter((_, r) => r !== row)
      .map((r) => r.filter((_, c) => c !== col));
  }

  function determinant(m) {
    const n = m.length;
    if (n === 1) return m[0][0];
    if (n === 2) return m[0][0] * m[1][1] - m[0][1] * m[1][0];
    let det = 0;
    for (let c = 0; c < n; c++) {
      const sign = c % 2 === 0 ? 1 : -1;
      det += sign * m[0][c] * determinant(minor(m, 0, c));
    }
    return det;
  }

  function transpose(m) {
    return m[0].map((_, c) => m.map((row) => row[c]));
  }

  function cofactorMatrix(m) {
    const n = m.length;
    const result = [];
    for (let r = 0; r < n; r++) {
      const row = [];
      for (let c = 0; c < n; c++) {
        const sign = (r + c) % 2 === 0 ? 1 : -1;
        row.push(sign * determinant(minor(m, r, c)));
      }
      result.push(row);
    }
    return result;
  }

  function inverse(m) {
    const det = determinant(m);
    if (Math.abs(det) < 1e-10) {
      throw new Error("Esta matriz no tiene inversa porque su determinante es 0 (matriz singular).");
    }
    const adjugate = transpose(cofactorMatrix(m));
    return adjugate.map((row) => row.map((v) => v / det));
  }

  function multiply(a, b) {
    const n = a.length;
    const result = [];
    for (let r = 0; r < n; r++) {
      const row = [];
      for (let c = 0; c < n; c++) {
        let sum = 0;
        for (let k = 0; k < n; k++) sum += a[r][k] * b[k][c];
        row.push(sum);
      }
      result.push(row);
    }
    return result;
  }

  // ---------------------------------------------------------------- Render -
  function renderMatrix(m) {
    const rows = m
      .map(
        (row) =>
          `<tr>${row.map((v) => `<td class="px-3 py-1.5 border border-[var(--color-border)] text-center">${fmt(v)}</td>`).join("")}</tr>`
      )
      .join("");
    return `<table class="border-collapse"><tbody>${rows}</tbody></table>`;
  }

  function renderScalar(label, value) {
    resultBody.innerHTML = `<p>${label} = <strong class="text-[var(--color-primary)]">${fmt(value)}</strong></p>`;
  }

  // ---------------------------------------------------------------- Eventos
  document.querySelectorAll("[data-op]").forEach((btn) => {
    btn.addEventListener("click", () => {
      clearError();
      const op = btn.dataset.op;
      const target = btn.dataset.target;
      try {
        if (op === "det") {
          const m = readMatrix(target.toLowerCase());
          resultTitle.textContent = `Determinante de ${target}`;
          renderScalar(`det(${target})`, determinant(m));
        } else if (op === "transpose") {
          const m = readMatrix(target.toLowerCase());
          resultTitle.textContent = `Transpuesta de ${target}`;
          resultBody.innerHTML = renderMatrix(transpose(m));
        } else if (op === "inverse") {
          const m = readMatrix(target.toLowerCase());
          resultTitle.textContent = `Inversa de ${target}`;
          resultBody.innerHTML = renderMatrix(inverse(m));
        } else if (op === "multiply-ab") {
          const a = readMatrix("a");
          const b = readMatrix("b");
          resultTitle.textContent = "A × B";
          resultBody.innerHTML = renderMatrix(multiply(a, b));
        } else if (op === "multiply-ba") {
          const a = readMatrix("a");
          const b = readMatrix("b");
          resultTitle.textContent = "B × A";
          resultBody.innerHTML = renderMatrix(multiply(b, a));
        }
        resultPanel.classList.remove("hidden");
      } catch (err) {
        showError(err.message);
      }
    });
  });

  setSize(2);
})();
