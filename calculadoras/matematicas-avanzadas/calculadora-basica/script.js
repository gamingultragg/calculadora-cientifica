/**
 * Calculadora Básica — evaluación secuencial (como una calculadora de
 * bolsillo real): cada operador resuelve inmediatamente la cuenta
 * pendiente, sin respetar la prioridad de operaciones (2+3×4 = 20, no 14).
 */
(function () {
  const resultEl = document.getElementById("bc-result");
  const exprEl = document.getElementById("bc-expr");

  const OP_SYMBOLS = { "+": "+", "-": "−", "*": "×", "/": "÷" };

  const state = {
    display: "0",
    previousValue: null,
    pendingOperator: null,
    shouldResetDisplay: false,
    error: false,
  };

  const fmt = (n) => {
    if (!Number.isFinite(n)) return "Error";
    const rounded = Math.round(n * 1e10) / 1e10;
    return new Intl.NumberFormat("es-AR", { maximumFractionDigits: 10 }).format(rounded);
  };

  function compute(a, b, op) {
    switch (op) {
      case "+":
        return a + b;
      case "-":
        return a - b;
      case "*":
        return a * b;
      case "/":
        if (b === 0) return null;
        return a / b;
      default:
        return b;
    }
  }

  function currentValue() {
    return parseFloat(state.display.replace(",", "."));
  }

  function render() {
    resultEl.textContent = state.error ? "Error" : displayFormatted();
    exprEl.textContent =
      state.previousValue !== null && state.pendingOperator
        ? `${fmt(state.previousValue)} ${OP_SYMBOLS[state.pendingOperator]}`
        : " ";
  }

  function displayFormatted() {
    // Mostrar el string tal cual se está tipeando (con coma decimal es-AR),
    // sin reformatear mientras el usuario todavía está escribiendo.
    return state.display.replace(".", ",");
  }

  function resetAll() {
    state.display = "0";
    state.previousValue = null;
    state.pendingOperator = null;
    state.shouldResetDisplay = false;
    state.error = false;
  }

  function pressDigit(d) {
    if (state.error) resetAll();
    if (state.shouldResetDisplay || state.display === "0") {
      state.display = d;
      state.shouldResetDisplay = false;
    } else {
      if (state.display.replace("-", "").length >= 15) return; // límite razonable de dígitos
      state.display += d;
    }
  }

  function pressDecimal() {
    if (state.error) resetAll();
    if (state.shouldResetDisplay) {
      state.display = "0.";
      state.shouldResetDisplay = false;
      return;
    }
    if (!state.display.includes(".")) state.display += ".";
  }

  function pressOperator(op) {
    if (state.error) return;
    const current = currentValue();
    if (state.pendingOperator && !state.shouldResetDisplay) {
      const result = compute(state.previousValue, current, state.pendingOperator);
      if (result === null) {
        state.error = true;
        return;
      }
      state.previousValue = result;
      state.display = String(result);
    } else {
      state.previousValue = current;
    }
    state.pendingOperator = op;
    state.shouldResetDisplay = true;
  }

  function pressEquals() {
    if (state.error || state.pendingOperator === null) return;
    const current = currentValue();
    const result = compute(state.previousValue, current, state.pendingOperator);
    if (result === null) {
      state.error = true;
      return;
    }
    state.display = String(result);
    state.previousValue = null;
    state.pendingOperator = null;
    state.shouldResetDisplay = true;
  }

  function pressPercent() {
    if (state.error) return;
    const value = currentValue() / 100;
    state.display = String(value);
    state.shouldResetDisplay = false;
  }

  function pressSign() {
    if (state.error) return;
    if (state.display === "0") return;
    state.display = state.display.startsWith("-") ? state.display.slice(1) : "-" + state.display;
  }

  function pressBackspace() {
    if (state.error) {
      resetAll();
      return;
    }
    if (state.shouldResetDisplay) return;
    state.display = state.display.length > 1 ? state.display.slice(0, -1) : "0";
  }

  function handleAction(action, value) {
    switch (action) {
      case "digit":
        pressDigit(value);
        break;
      case "decimal":
        pressDecimal();
        break;
      case "operator":
        pressOperator(value);
        break;
      case "equals":
        pressEquals();
        break;
      case "percent":
        pressPercent();
        break;
      case "sign":
        pressSign();
        break;
      case "backspace":
        pressBackspace();
        break;
      case "clear":
        resetAll();
        break;
    }
    render();
  }

  document.querySelectorAll("[data-action]").forEach((btn) => {
    btn.addEventListener("click", () => handleAction(btn.dataset.action, btn.dataset.value));
  });

  window.addEventListener("keydown", (e) => {
    const key = e.key;
    if (/[0-9]/.test(key)) {
      handleAction("digit", key);
      return;
    }
    if (key === ".") {
      handleAction("decimal");
      return;
    }
    if (["+", "-"].includes(key)) {
      handleAction("operator", key);
      return;
    }
    if (key === "*") {
      handleAction("operator", "*");
      return;
    }
    if (key === "/") {
      e.preventDefault();
      handleAction("operator", "/");
      return;
    }
    if (key === "Enter" || key === "=") {
      e.preventDefault();
      handleAction("equals");
      return;
    }
    if (key === "Backspace") {
      handleAction("backspace");
      return;
    }
    if (key === "Escape") {
      handleAction("clear");
      return;
    }
    if (key === "%") {
      handleAction("percent");
      return;
    }
  });

  render();
})();
