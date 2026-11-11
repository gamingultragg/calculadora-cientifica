/**
 * Calculadora Científica — motor de evaluación propio (sin eval/Function).
 * Tokeniza y parsea con descenso recursivo:
 *   expr   := term (('+'|'-') term)*
 *   term   := power (('*'|'/') power)*
 *   power  := unary ('^' power)?           // asociativo a la derecha
 *   unary  := '-' unary | postfix
 *   postfix:= primary ('!')*
 *   primary:= number | const | func '(' expr ')' | '(' expr ')'
 */
(function () {
  const FUNCTIONS = ["sin", "cos", "tan", "log", "ln", "sqrt", "exp"];
  const CONSTANTS = { pi: Math.PI, e: Math.E };

  class CalcError extends Error {}

  function tokenize(input) {
    const tokens = [];
    let i = 0;
    while (i < input.length) {
      const ch = input[i];
      if (/\s/.test(ch)) {
        i++;
        continue;
      }
      if (/[0-9.]/.test(ch)) {
        let num = "";
        while (i < input.length && /[0-9.]/.test(input[i])) {
          num += input[i];
          i++;
        }
        if ((num.match(/\./g) || []).length > 1) {
          throw new CalcError("Número inválido: demasiados puntos decimales.");
        }
        tokens.push({ type: "num", value: parseFloat(num) });
        continue;
      }
      if (/[a-zA-Z]/.test(ch)) {
        let word = "";
        while (i < input.length && /[a-zA-Z]/.test(input[i])) {
          word += input[i];
          i++;
        }
        if (FUNCTIONS.includes(word)) {
          tokens.push({ type: "func", value: word });
        } else if (word in CONSTANTS) {
          tokens.push({ type: "const", value: word });
        } else {
          throw new CalcError(`Función o constante desconocida: "${word}".`);
        }
        continue;
      }
      if ("+-*/^!().".includes(ch)) {
        tokens.push({ type: "op", value: ch });
        i++;
        continue;
      }
      throw new CalcError(`Carácter no válido: "${ch}".`);
    }
    return tokens;
  }

  function parse(tokens) {
    let pos = 0;
    const peek = () => tokens[pos];
    const next = () => tokens[pos++];

    function parseExpr() {
      let value = parseTerm();
      while (peek() && peek().type === "op" && (peek().value === "+" || peek().value === "-")) {
        const op = next().value;
        const rhs = parseTerm();
        value = op === "+" ? value + rhs : value - rhs;
      }
      return value;
    }

    function parseTerm() {
      let value = parsePower();
      while (peek() && peek().type === "op" && (peek().value === "*" || peek().value === "/")) {
        const op = next().value;
        const rhs = parsePower();
        if (op === "/") {
          if (rhs === 0) throw new CalcError("Error: división por cero.");
          value = value / rhs;
        } else {
          value = value * rhs;
        }
      }
      return value;
    }

    function parsePower() {
      const base = parseUnary();
      if (peek() && peek().type === "op" && peek().value === "^") {
        next();
        const exponent = parsePower(); // asociativo a la derecha
        return Math.pow(base, exponent);
      }
      return base;
    }

    function parseUnary() {
      if (peek() && peek().type === "op" && peek().value === "-") {
        next();
        return -parseUnary();
      }
      return parsePostfix();
    }

    function parsePostfix() {
      let value = parsePrimary();
      while (peek() && peek().type === "op" && peek().value === "!") {
        next();
        value = factorial(value);
      }
      return value;
    }

    function parsePrimary() {
      const tok = peek();
      if (!tok) throw new CalcError("Expresión incompleta.");

      if (tok.type === "num") {
        next();
        return tok.value;
      }
      if (tok.type === "const") {
        next();
        return CONSTANTS[tok.value];
      }
      if (tok.type === "func") {
        next();
        expectOp("(");
        const arg = parseExpr();
        expectOp(")");
        return applyFunction(tok.value, arg);
      }
      if (tok.type === "op" && tok.value === "(") {
        next();
        const value = parseExpr();
        expectOp(")");
        return value;
      }
      throw new CalcError("Expresión mal formada.");
    }

    function expectOp(value) {
      const tok = peek();
      if (!tok || tok.type !== "op" || tok.value !== value) {
        throw new CalcError(`Se esperaba "${value}".`);
      }
      next();
    }

    if (tokens.length === 0) throw new CalcError("Ingresá una expresión.");
    const result = parseExpr();
    if (pos < tokens.length) throw new CalcError("Expresión mal formada.");
    return result;
  }

  function factorial(n) {
    if (!Number.isFinite(n) || n < 0 || Math.abs(n - Math.round(n)) > 1e-9) {
      throw new CalcError("El factorial solo está definido para enteros ≥ 0.");
    }
    n = Math.round(n);
    if (n > 170) throw new CalcError("Número demasiado grande para calcular su factorial.");
    let result = 1;
    for (let k = 2; k <= n; k++) result *= k;
    return result;
  }

  function applyFunction(name, arg) {
    const toRad = (deg) => (deg * Math.PI) / 180;
    switch (name) {
      case "sin":
        return Math.sin(state.angleMode === "DEG" ? toRad(arg) : arg);
      case "cos":
        return Math.cos(state.angleMode === "DEG" ? toRad(arg) : arg);
      case "tan": {
        const radians = state.angleMode === "DEG" ? toRad(arg) : arg;
        const cosVal = Math.cos(radians);
        if (Math.abs(cosVal) < 1e-12) throw new CalcError("Tangente no definida para este ángulo.");
        return Math.tan(radians);
      }
      case "log":
        if (arg <= 0) throw new CalcError("El logaritmo requiere un valor mayor a 0.");
        return Math.log10(arg);
      case "ln":
        if (arg <= 0) throw new CalcError("El logaritmo natural requiere un valor mayor a 0.");
        return Math.log(arg);
      case "sqrt":
        if (arg < 0) throw new CalcError("No existe raíz cuadrada real de un número negativo.");
        return Math.sqrt(arg);
      case "exp":
        return Math.exp(arg);
      default:
        throw new CalcError(`Función no soportada: ${name}`);
    }
  }

  function evaluate(expression) {
    const tokens = tokenize(expression);
    const value = parse(tokens);
    if (!Number.isFinite(value)) throw new CalcError("El resultado no es un número finito.");
    return value;
  }

  function formatNumber(n) {
    if (Object.is(n, -0)) n = 0;
    const rounded = Math.round(n * 1e10) / 1e10;
    return new Intl.NumberFormat("es-AR", { maximumFractionDigits: 10 }).format(rounded);
  }

  // ------------------------------------------------------------------ UI --
  const state = {
    expr: "",
    angleMode: "DEG",
    memory: 0,
    justEvaluated: false, // tras "=", un número/función nuevo empieza de cero; un operador sigue con el resultado
  };

  const exprEl = document.getElementById("cc-expr");
  const resultEl = document.getElementById("cc-result");
  const errorEl = document.getElementById("cc-error");
  const angleLabel = document.getElementById("cc-angle-label");
  const memoryLabel = document.getElementById("cc-memory-label");

  function toDisplay(expr) {
    return expr
      .replace(/\*/g, "×")
      .replace(/\//g, "÷")
      .replace(/pi/g, "π")
      .replace(/sqrt\(/g, "√(");
  }

  function showError(message) {
    errorEl.textContent = message;
    errorEl.classList.remove("hidden");
  }

  function clearError() {
    errorEl.classList.add("hidden");
    errorEl.textContent = "";
  }

  function render() {
    exprEl.textContent = state.expr ? toDisplay(state.expr) : "0";
    angleLabel.textContent = state.angleMode;
    memoryLabel.textContent = formatNumber(state.memory);
  }

  function tryLivePreview() {
    if (!state.expr) {
      resultEl.textContent = "0";
      return;
    }
    try {
      const value = evaluate(state.expr);
      resultEl.textContent = formatNumber(value);
      clearError();
    } catch {
      // Mientras se escribe, una expresión incompleta es normal: no mostramos error.
    }
  }

  document.querySelectorAll("[data-action]").forEach((btn) => {
    btn.addEventListener("click", () => handleAction(btn.dataset.action, btn.dataset.value));
  });

  // ------------------------------------------------------- historial --
  // Se guarda solo en este navegador (localStorage). Máximo 30 cálculos.
  const HISTORY_KEY = "cc-sci-history";
  const HISTORY_MAX = 30;
  const historyEl = document.getElementById("cc-history");
  const historyEmptyEl = document.getElementById("cc-history-empty");
  const historyClearBtn = document.getElementById("cc-history-clear");
  let history = [];
  try {
    const saved = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
    if (Array.isArray(saved)) history = saved.filter((h) => h && typeof h.expr === "string" && typeof h.res === "string").slice(0, HISTORY_MAX);
  } catch {
    history = [];
  }

  function saveHistory() {
    try {
      localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    } catch {
      // Sin almacenamiento (modo privado, etc.): el historial dura solo mientras la página está abierta.
    }
  }

  function pushHistory(expr, value) {
    // "raw" es el valor sin formato (punto decimal) para poder reutilizarlo en una cuenta nueva.
    const entry = { expr, res: formatNumber(value), raw: String(value) };
    if (history[0] && history[0].expr === entry.expr && history[0].raw === entry.raw) return;
    history.unshift(entry);
    history = history.slice(0, HISTORY_MAX);
    saveHistory();
    renderHistory();
  }

  function renderHistory() {
    if (!historyEl) return;
    historyEl.textContent = "";
    history.forEach((h) => {
      const li = document.createElement("li");
      li.className = "cc-history-item";
      const useExpr = document.createElement("button");
      useExpr.type = "button";
      useExpr.className = "cc-history-expr";
      useExpr.textContent = toDisplay(h.expr);
      useExpr.title = "Volver a cargar esta cuenta";
      useExpr.addEventListener("click", () => {
        clearError();
        state.expr = h.expr;
        state.justEvaluated = false;
        render();
        tryLivePreview();
      });
      const useRes = document.createElement("button");
      useRes.type = "button";
      useRes.className = "cc-history-res";
      useRes.textContent = "= " + h.res;
      useRes.title = "Usar este resultado en la cuenta actual";
      useRes.addEventListener("click", () => {
        clearError();
        if (state.justEvaluated) state.expr = "";
        state.justEvaluated = false;
        state.expr += h.raw;
        render();
        tryLivePreview();
      });
      li.append(useExpr, useRes);
      historyEl.append(li);
    });
    if (historyEmptyEl) historyEmptyEl.hidden = history.length > 0;
    if (historyClearBtn) historyClearBtn.hidden = history.length === 0;
  }

  if (historyClearBtn) {
    historyClearBtn.addEventListener("click", () => {
      history = [];
      saveHistory();
      renderHistory();
    });
  }

  const STARTS_NEW = new Set(["digit", "func", "mr"]);

  function handleAction(action, value) {
    clearError();
    // Después de "=": un número o función nuevo reemplaza el resultado; un operador lo continúa.
    const startsNew = state.justEvaluated && (STARTS_NEW.has(action) || (action === "insert" && /^(\(|pi|e|\.)$/.test(value)));
    if (startsNew) state.expr = "";
    if (action !== "equals") state.justEvaluated = false;
    switch (action) {
      case "digit":
        state.expr += value;
        break;
      case "insert":
        state.expr += value;
        break;
      case "func":
        state.expr += value;
        break;
      case "clear":
        state.expr = "";
        state.justEvaluated = false;
        resultEl.textContent = "0";
        break;
      case "backspace":
        state.expr = state.expr.slice(0, -1);
        break;
      case "toggle-angle":
        state.angleMode = state.angleMode === "DEG" ? "RAD" : "DEG";
        tryLivePreview();
        break;
      case "mc":
        state.memory = 0;
        break;
      case "mr":
        state.expr += formatMemoryForInsert();
        break;
      case "mplus":
      case "mminus": {
        try {
          const value = state.expr ? evaluate(state.expr) : 0;
          state.memory += action === "mplus" ? value : -value;
        } catch {
          showError("No hay un resultado válido para guardar en memoria.");
        }
        break;
      }
      case "equals": {
        try {
          if (!state.expr) break;
          const value = evaluate(state.expr);
          resultEl.textContent = formatNumber(value);
          pushHistory(state.expr, value);
          state.justEvaluated = true;
          // El expr interno queda en formato numérico "crudo" (punto decimal) para
          // que el motor de parseo lo pueda seguir usando en la próxima operación.
          state.expr = String(value);
          render();
          return;
        } catch (err) {
          showError(err instanceof CalcError ? err.message : "Expresión inválida.");
          return;
        }
      }
      default:
        break;
    }
    render();
    tryLivePreview();
  }

  function formatMemoryForInsert() {
    // Inserta el valor de memoria como número "crudo" (con punto decimal) para que el parser lo entienda.
    return String(state.memory);
  }

  // Soporte de teclado físico
  const LETTER_SHORTCUTS = {
    s: ["func", "sin("],
    c: ["func", "cos("],
    t: ["func", "tan("],
    l: ["func", "log("],
    n: ["func", "ln("],
    r: ["func", "sqrt("],
    p: ["insert", "pi"],
    e: ["insert", "e"],
    a: ["toggle-angle"],
  };

  window.addEventListener("keydown", (e) => {
    // No pisamos atajos del navegador (Ctrl+C, Ctrl+R…) ni lo que se escribe en otros campos.
    if (e.ctrlKey || e.metaKey || e.altKey || e.isComposing) return;
    const t = e.target;
    if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;

    const key = e.key;
    if (/^[0-9]$/.test(key)) {
      e.preventDefault();
      handleAction("digit", key);
      return;
    }
    if (key === "." || key === ",") {
      e.preventDefault();
      handleAction("digit", ".");
      return;
    }
    if (key === "x" || key === "X" || key === "*") {
      e.preventDefault();
      handleAction("insert", "*");
      return;
    }
    if (["+", "-", "/", "^", "(", ")", "!"].includes(key)) {
      e.preventDefault();
      handleAction("insert", key);
      return;
    }
    if (key === "Enter" || key === "=") {
      e.preventDefault();
      handleAction("equals");
      return;
    }
    if (key === "Backspace") {
      e.preventDefault();
      handleAction("backspace");
      return;
    }
    if (key === "Escape" || key === "Delete") {
      handleAction("clear");
      return;
    }
    const sc = LETTER_SHORTCUTS[key.toLowerCase()];
    if (sc && key.length === 1) {
      e.preventDefault();
      handleAction(sc[0], sc[1]);
    }
  });

  renderHistory();
  render();
})();
