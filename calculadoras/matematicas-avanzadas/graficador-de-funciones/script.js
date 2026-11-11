/**
 * Graficador de funciones — hasta 3 funciones f(x), con zoom, desplazamiento, valores y ceros aproximados.
 * El analizador de expresiones es propio (no usa eval): números, x, pi, e, + − * / ^, paréntesis y funciones.
 */
(function () {
  // ---------------------------------------------------------------- analizador --
  const FUNCS = {
    sin: Math.sin, sen: Math.sin, cos: Math.cos, tan: Math.tan, tg: Math.tan, asin: Math.asin, acos: Math.acos, atan: Math.atan,
    sinh: Math.sinh, cosh: Math.cosh, tanh: Math.tanh, sqrt: Math.sqrt, raiz: Math.sqrt, cbrt: Math.cbrt, abs: Math.abs,
    ln: Math.log, log: Math.log10, log10: Math.log10, log2: Math.log2, exp: Math.exp, floor: Math.floor, ceil: Math.ceil, round: Math.round, sign: Math.sign,
  };
  const CONSTS = { pi: Math.PI, e: Math.E };

  function tokenize(src) {
    const s = String(src).toLowerCase().replace(/×|·/g, "*").replace(/÷/g, "/").replace(/−/g, "-").replace(/,/g, ".").replace(/\s+/g, "");
    const tokens = [];
    let i = 0;
    while (i < s.length) {
      const rest = s.slice(i);
      let m;
      if ((m = /^(\d+\.?\d*|\.\d+)/.exec(rest))) {
        tokens.push({ t: "num", v: Number(m[0]) });
        i += m[0].length;
      } else if ((m = /^[a-z]+\d*/.exec(rest))) {
        // log2 / log10 llevan dígitos; en el resto, los dígitos son otro número (x2 = x·2)
        const withDigits = m[0], word = /^[a-z]+/.exec(rest)[0];
        const id = withDigits in FUNCS ? withDigits : word;
        tokens.push({ t: "id", v: id });
        i += id.length;
      } else if ("+-*/^()".includes(s[i])) {
        tokens.push({ t: s[i] });
        i++;
      } else {
        throw new Error(`Carácter no válido: "${s[i]}".`);
      }
    }
    // multiplicación implícita: 2x, 2(x+1), (x+1)(x-1), x(x+1), 2sen(x)
    const out = [];
    for (const tok of tokens) {
      const prev = out[out.length - 1];
      const startsValue = tok.t === "num" || tok.t === "id" || tok.t === "(";
      const endsValue = prev && (prev.t === "num" || prev.t === ")" || (prev.t === "id" && (prev.v === "x" || prev.v in CONSTS)));
      if (prev && startsValue && endsValue) out.push({ t: "*" });
      out.push(tok);
    }
    return out;
  }

  function compile(src) {
    const tokens = tokenize(src);
    if (!tokens.length) throw new Error("Escribí una función, por ejemplo x^2 - 4.");
    let pos = 0;
    const peek = () => tokens[pos];
    const eat = (t) => {
      if (peek() && peek().t === t) return tokens[pos++];
      throw new Error(t === ")" ? "Falta cerrar un paréntesis." : `Se esperaba "${t}".`);
    };

    function expr() {
      let left = term();
      while (peek() && (peek().t === "+" || peek().t === "-")) {
        const op = tokens[pos++].t, right = term(), l = left;
        left = op === "+" ? (x) => l(x) + right(x) : (x) => l(x) - right(x);
      }
      return left;
    }
    function term() {
      let left = unary();
      while (peek() && (peek().t === "*" || peek().t === "/")) {
        const op = tokens[pos++].t, right = unary(), l = left;
        left = op === "*" ? (x) => l(x) * right(x) : (x) => l(x) / right(x);
      }
      return left;
    }
    function unary() {
      if (peek() && peek().t === "-") {
        pos++;
        const u = unary();
        return (x) => -u(x);
      }
      if (peek() && peek().t === "+") {
        pos++;
        return unary();
      }
      return power();
    }
    function power() {
      const base = primary();
      if (peek() && peek().t === "^") {
        pos++;
        const exp = unary();
        return (x) => Math.pow(base(x), exp(x));
      }
      return base;
    }
    function primary() {
      const tk = peek();
      if (!tk) throw new Error("La expresión está incompleta.");
      if (tk.t === "num") {
        pos++;
        return () => tk.v;
      }
      if (tk.t === "(") {
        pos++;
        const e = expr();
        eat(")");
        return e;
      }
      if (tk.t === "id") {
        pos++;
        if (tk.v === "x") return (x) => x;
        if (tk.v in CONSTS) return () => CONSTS[tk.v];
        if (tk.v in FUNCS) {
          if (!peek() || peek().t !== "(") throw new Error(`Falta el paréntesis después de ${tk.v}: escribí ${tk.v}(x).`);
          pos++;
          const arg = expr();
          eat(")");
          const fn = FUNCS[tk.v];
          return (x) => fn(arg(x));
        }
        throw new Error(`No conozco "${tk.v}". Funciones disponibles: sen, cos, tan, sqrt, abs, ln, log, exp…`);
      }
      throw new Error(`No se esperaba "${tk.t}" en esa posición.`);
    }

    const f = expr();
    if (pos < tokens.length) throw new Error(`Sobra "${tokens[pos].t === "num" ? tokens[pos].v : tokens[pos].t}" al final de la expresión.`);
    return f;
  }

  // Ceros aproximados en [a, b]: cambios de signo entre muestras + bisección.
  function zeros(f, a, b, samples = 2000) {
    const out = [];
    const step = (b - a) / samples;
    let px = a, py = f(a);
    for (let i = 1; i <= samples && out.length < 12; i++) {
      const cx = a + i * step, cy = f(cx);
      if (Number.isFinite(py) && Number.isFinite(cy)) {
        if (py === 0) out.push(px);
        else if (py * cy < 0) {
          let lo = px, hi = cx, flo = py;
          for (let k = 0; k < 60; k++) {
            const mid = (lo + hi) / 2, fm = f(mid);
            if (flo * fm <= 0) hi = mid;
            else { lo = mid; flo = fm; }
          }
          const r = (lo + hi) / 2;
          if (Math.abs(f(r)) < 1e-6 * Math.max(1, Math.abs(py), Math.abs(cy)) || Math.abs(f(r)) < 1e-3) out.push(r);
        }
      }
      px = cx;
      py = cy;
    }
    return out.filter((r, i) => i === 0 || Math.abs(r - out[i - 1]) > step * 1.5);
  }

  if (typeof module !== "undefined") module.exports = { tokenize, compile, zeros };
  if (typeof document === "undefined" || !document.getElementById("gf-canvas")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const canvas = $("gf-canvas");
  const ctx = canvas.getContext("2d");
  const errorEl = $("err");
  const COLORS = ["#2563eb", "#dc2626", "#16a34a"];
  const view = { x0: -10, x1: 10, y0: -10, y1: 10, autoY: true };
  let fns = [];
  const fmt = (n) => new Intl.NumberFormat("es-AR", { maximumSignificantDigits: 6 }).format(n);

  function cssVar(name, fallback) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim() || fallback;
  }

  function resize() {
    const dpr = window.devicePixelRatio || 1;
    const w = canvas.clientWidth, h = canvas.clientHeight;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    draw();
  }

  function niceStep(range, target) {
    const raw = range / target;
    const mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const n = raw / mag;
    return (n < 1.5 ? 1 : n < 3.5 ? 2 : n < 7.5 ? 5 : 10) * mag;
  }

  function autoRangeY() {
    const ys = [];
    const N = 400;
    fns.forEach((fn) => {
      for (let i = 0; i <= N; i++) {
        const y = fn.f(view.x0 + ((view.x1 - view.x0) * i) / N);
        if (Number.isFinite(y) && Math.abs(y) < 1e6) ys.push(y);
      }
    });
    if (!ys.length) return;
    ys.sort((a, b) => a - b);
    let lo = ys[0], hi = ys[ys.length - 1];
    const p1 = ys[Math.floor(ys.length * 0.02)], p99 = ys[Math.ceil(ys.length * 0.98) - 1];
    if (hi - lo > 40 * Math.max(p99 - p1, 1e-9)) { lo = p1; hi = p99; } // asíntotas: se recortan los extremos
    if (lo === hi) { lo -= 1; hi += 1; }
    const pad = (hi - lo) * 0.12;
    view.y0 = Math.min(lo - pad, 0 - (hi - lo) * 0.02);
    view.y1 = Math.max(hi + pad, 0 + (hi - lo) * 0.02);
  }

  function draw() {
    const W = canvas.clientWidth, H = canvas.clientHeight;
    ctx.clearRect(0, 0, W, H);
    if (view.autoY && fns.length) autoRangeY();
    const sx = (x) => ((x - view.x0) / (view.x1 - view.x0)) * W;
    const sy = (y) => H - ((y - view.y0) / (view.y1 - view.y0)) * H;
    const grid = cssVar("--color-border", "#e2e8f0"), text = cssVar("--color-text-muted", "#64748b"), axis = cssVar("--color-text", "#0f172a");
    ctx.font = "11px 'Roboto Mono', monospace";
    // cuadrícula
    const gx = niceStep(view.x1 - view.x0, 8), gy = niceStep(view.y1 - view.y0, 6);
    ctx.lineWidth = 1;
    ctx.fillStyle = text;
    for (let x = Math.ceil(view.x0 / gx) * gx; x <= view.x1; x += gx) {
      ctx.strokeStyle = grid;
      ctx.beginPath(); ctx.moveTo(sx(x), 0); ctx.lineTo(sx(x), H); ctx.stroke();
      if (Math.abs(x) > gx / 1e3) { ctx.textAlign = "center"; ctx.fillText(fmt(+x.toFixed(10)), sx(x), Math.min(H - 4, Math.max(12, sy(0) + 14))); }
    }
    for (let y = Math.ceil(view.y0 / gy) * gy; y <= view.y1; y += gy) {
      ctx.strokeStyle = grid;
      ctx.beginPath(); ctx.moveTo(0, sy(y)); ctx.lineTo(W, sy(y)); ctx.stroke();
      if (Math.abs(y) > gy / 1e3) { ctx.textAlign = "left"; ctx.fillText(fmt(+y.toFixed(10)), Math.min(W - 40, Math.max(4, sx(0) + 4)), sy(y) - 3); }
    }
    // ejes
    ctx.strokeStyle = axis; ctx.lineWidth = 1.5;
    if (view.y0 < 0 && view.y1 > 0) { ctx.beginPath(); ctx.moveTo(0, sy(0)); ctx.lineTo(W, sy(0)); ctx.stroke(); }
    if (view.x0 < 0 && view.x1 > 0) { ctx.beginPath(); ctx.moveTo(sx(0), 0); ctx.lineTo(sx(0), H); ctx.stroke(); }
    // curvas
    const N = Math.max(300, Math.min(2000, Math.round(W * 2)));
    fns.forEach((fn) => {
      ctx.strokeStyle = COLORS[fn.index]; ctx.lineWidth = 2.2;
      ctx.beginPath();
      let pen = false, prevY = null;
      for (let i = 0; i <= N; i++) {
        const x = view.x0 + ((view.x1 - view.x0) * i) / N, y = fn.f(x);
        const bad = !Number.isFinite(y) || Math.abs(sy(y)) > 1e5;
        const jump = prevY !== null && Number.isFinite(prevY) && Number.isFinite(y) && Math.abs(sy(y) - sy(prevY)) > H * 1.5;
        if (bad || jump) { pen = false; } else if (!pen) { ctx.moveTo(sx(x), sy(y)); pen = true; } else { ctx.lineTo(sx(x), sy(y)); }
        prevY = y;
      }
      ctx.stroke();
    });
  }

  function readFunctions() {
    fns = [];
    for (let i = 1; i <= 3; i++) {
      const el = $("gf-f" + i);
      el.classList.remove("field-error");
      const src = el.value.trim();
      if (!src) continue;
      try {
        fns.push({ index: i - 1, src, f: compile(src) });
      } catch (e) {
        el.classList.add("field-error");
        throw new Error(`Función ${i}: ${e.message}`);
      }
    }
    if (!fns.length) throw new Error("Escribí al menos una función, por ejemplo x^2 - 4.");
  }

  function num(id, label) {
    const v = $(id).value.trim();
    if (v === "") return null;
    const n = Number(v.replace(",", "."));
    if (!Number.isFinite(n)) { $(id).classList.add("field-error"); throw new Error(`"${label}" tiene que ser un número.`); }
    return n;
  }

  function plot() {
    errorEl.classList.add("hidden");
    ["gf-xmin", "gf-xmax", "gf-ymin", "gf-ymax"].forEach((id) => $(id).classList.remove("field-error"));
    try {
      readFunctions();
      const xmin = num("gf-xmin", "x mínimo"), xmax = num("gf-xmax", "x máximo");
      view.x0 = xmin === null ? -10 : xmin;
      view.x1 = xmax === null ? 10 : xmax;
      if (!(view.x1 > view.x0)) throw new Error("x máximo tiene que ser mayor que x mínimo.");
      const ymin = num("gf-ymin", "y mínimo"), ymax = num("gf-ymax", "y máximo");
      view.autoY = ymin === null || ymax === null;
      if (!view.autoY) {
        if (!(ymax > ymin)) throw new Error("y máximo tiene que ser mayor que y mínimo.");
        view.y0 = ymin;
        view.y1 = ymax;
      }
      $("gf-panel").classList.remove("hidden");
      resize(); // el lienzo mide 0 mientras el panel está oculto: se dimensiona recién al mostrarlo
      info();
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
    }
  }

  function syncInputs() {
    $("gf-xmin").value = fmt(+view.x0.toFixed(6));
    $("gf-xmax").value = fmt(+view.x1.toFixed(6));
    if (!view.autoY) {
      $("gf-ymin").value = fmt(+view.y0.toFixed(6));
      $("gf-ymax").value = fmt(+view.y1.toFixed(6));
    }
  }

  function info() {
    const rows = fns.map((fn) => {
      const z = zeros(fn.f, view.x0, view.x1);
      const y0 = fn.f(0);
      return `<li><span style="color:${COLORS[fn.index]}">●</span> <strong class="font-numeric">f${fn.index + 1}(x) = ${fn.src}</strong><br>` +
        `<span>Ceros en este tramo: ${z.length ? z.map((r) => `x ≈ ${fmt(+r.toPrecision(7))}`).join(" · ") : "ninguno visible"}</span>` +
        `${Number.isFinite(y0) && view.x0 <= 0 && view.x1 >= 0 ? `<br><span>Ordenada al origen: f(0) = ${fmt(+y0.toPrecision(7))}</span>` : ""}</li>`;
    });
    $("gf-info").innerHTML = rows.join("");
  }

  function evaluateAt() {
    const out = $("gf-eval-out");
    const v = num("gf-eval", "x");
    if (v === null) { out.textContent = ""; return; }
    out.innerHTML = fns.map((fn) => `f${fn.index + 1}(${fmt(v)}) = <strong>${fmt(+fn.f(v).toPrecision(8))}</strong>`).join(" · ");
  }

  // zoom y desplazamiento
  function zoom(factor, cx = (view.x0 + view.x1) / 2, cy = (view.y0 + view.y1) / 2) {
    view.x0 = cx + (view.x0 - cx) * factor; view.x1 = cx + (view.x1 - cx) * factor;
    if (!view.autoY) { view.y0 = cy + (view.y0 - cy) * factor; view.y1 = cy + (view.y1 - cy) * factor; }
    syncInputs(); draw(); info();
  }
  let drag = null;
  canvas.addEventListener("pointerdown", (e) => { drag = { x: e.clientX, y: e.clientY }; canvas.setPointerCapture(e.pointerId); });
  canvas.addEventListener("pointermove", (e) => {
    const r = canvas.getBoundingClientRect();
    const mx = view.x0 + ((e.clientX - r.left) / r.width) * (view.x1 - view.x0);
    $("gf-cursor").textContent = fns.length ? `x = ${fmt(+mx.toPrecision(5))} → ` + fns.map((fn) => `f${fn.index + 1} = ${fmt(+fn.f(mx).toPrecision(5))}`).join(" · ") : "";
    if (!drag) return;
    const dx = ((e.clientX - drag.x) / r.width) * (view.x1 - view.x0);
    const dy = ((e.clientY - drag.y) / r.height) * (view.y1 - view.y0);
    view.x0 -= dx; view.x1 -= dx;
    if (!view.autoY) { view.y0 += dy; view.y1 += dy; }
    drag = { x: e.clientX, y: e.clientY };
    draw();
  });
  canvas.addEventListener("pointerup", () => { if (drag) { drag = null; syncInputs(); info(); } });
  canvas.addEventListener("wheel", (e) => {
    e.preventDefault();
    const r = canvas.getBoundingClientRect();
    const cx = view.x0 + ((e.clientX - r.left) / r.width) * (view.x1 - view.x0);
    const cy = view.y1 - ((e.clientY - r.top) / r.height) * (view.y1 - view.y0);
    zoom(e.deltaY > 0 ? 1.15 : 1 / 1.15, cx, cy);
  }, { passive: false });

  $("gf-plot").addEventListener("click", plot);
  $("gf-zoom-in").addEventListener("click", () => fns.length && zoom(0.7));
  $("gf-zoom-out").addEventListener("click", () => fns.length && zoom(1 / 0.7));
  $("gf-reset").addEventListener("click", () => { ["gf-xmin", "gf-xmax", "gf-ymin", "gf-ymax"].forEach((id) => ($(id).value = "")); plot(); });
  $("gf-eval").addEventListener("input", evaluateAt);
  document.querySelectorAll("input[id^=gf-f]").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && plot()));
  document.querySelectorAll("[data-fn]").forEach((b) =>
    b.addEventListener("click", () => {
      const [a, bb, c] = b.dataset.fn.split("|");
      $("gf-f1").value = a || ""; $("gf-f2").value = bb || ""; $("gf-f3").value = c || "";
      ["gf-xmin", "gf-xmax", "gf-ymin", "gf-ymax"].forEach((id) => ($(id).value = ""));
      plot();
    })
  );
  $("gf-share").addEventListener("click", async () => {
    const p = new URLSearchParams();
    ["gf-f1", "gf-f2", "gf-f3", "gf-xmin", "gf-xmax", "gf-ymin", "gf-ymax"].forEach((id) => $(id).value.trim() && p.set(id, $(id).value.trim()));
    try { await navigator.clipboard.writeText(location.origin + location.pathname + "?" + p.toString()); $("gf-share").textContent = "¡Enlace copiado!"; } catch { $("gf-share").textContent = "No se pudo copiar"; }
    setTimeout(() => ($("gf-share").textContent = "Copiar enlace"), 1800);
  });
  window.addEventListener("resize", resize);
  new MutationObserver(draw).observe(document.documentElement, { attributes: true, attributeFilter: ["class", "data-theme"] });

  // valores desde el enlace
  new URLSearchParams(location.search).forEach((v, k) => { const el = document.getElementById(k); if (el && /^gf-(f[123]|[xy](min|max))$/.test(k) && v.length < 200) el.value = v; });
  resize();
  if ($("gf-f1").value) plot(); else document.querySelector("[data-fn]").click();
})();
