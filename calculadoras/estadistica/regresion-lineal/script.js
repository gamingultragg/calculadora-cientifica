/**
 * Calculadora de Regresión Lineal (mínimos cuadrados) y correlación de Pearson.
 *   y = a + b·x     b = (nΣxy − ΣxΣy) / (nΣx² − (Σx)²)     a = ȳ − b·x̄
 * Los datos se pegan como pares "x y" (uno por línea; separador: espacio, tabulación o punto y coma).
 */
(function () {
  function toNumber(token) {
    let s = token.trim();
    if (s.includes(",") && !s.includes(".")) s = s.replace(",", ".");
    else if (s.includes(",")) s = s.replace(/\./g, "").replace(",", ".");
    const v = Number(s);
    if (s === "" || !Number.isFinite(v)) throw new Error(`"${token}" no es un número válido.`);
    return v;
  }

  function parsePairs(text) {
    const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
    const xs = [], ys = [];
    lines.forEach((line, i) => {
      const parts = line.split(/[\s;]+/).filter(Boolean);
      if (parts.length !== 2) throw new Error(`La línea ${i + 1} ("${line}") tiene que tener exactamente dos valores: x e y.`);
      xs.push(toNumber(parts[0]));
      ys.push(toNumber(parts[1]));
    });
    if (xs.length < 2) throw new Error("Ingresá al menos dos pares de datos.");
    return { xs, ys };
  }

  function regress(xs, ys) {
    const n = xs.length;
    const sx = xs.reduce((a, b) => a + b, 0);
    const sy = ys.reduce((a, b) => a + b, 0);
    const sxx = xs.reduce((a, x) => a + x * x, 0);
    const syy = ys.reduce((a, y) => a + y * y, 0);
    const sxy = xs.reduce((a, x, i) => a + x * ys[i], 0);
    const denom = n * sxx - sx * sx;
    if (Math.abs(denom) < 1e-12) throw new Error("Todos los valores de x son iguales: no se puede ajustar una recta (la pendiente no está definida).");
    const slope = (n * sxy - sx * sy) / denom;
    const intercept = (sy - slope * sx) / n;
    const rDen = Math.sqrt(denom * (n * syy - sy * sy));
    const r = rDen === 0 ? (slope === 0 ? 0 : NaN) : (n * sxy - sx * sy) / rDen;
    return { n, slope, intercept, r, r2: r * r, meanX: sx / n, meanY: sy / n };
  }

  if (typeof module !== "undefined") module.exports = { parsePairs, regress };
  if (typeof document === "undefined" || !document.getElementById("rl-data")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("rl-result-panel");
  const fmt = (n, d = 6) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: d }).format(Number(n.toPrecision(7)));

  function strength(r) {
    const a = Math.abs(r);
    const f = a >= 0.9 ? "muy fuerte" : a >= 0.7 ? "fuerte" : a >= 0.4 ? "moderada" : a >= 0.2 ? "débil" : "muy débil o nula";
    return `${f}${r > 0 ? ", positiva" : r < 0 ? ", negativa" : ""}`;
  }

  // Gráfico de dispersión con la recta ajustada (canvas, sin dependencias).
  function drawChart(xs, ys, r) {
    const canvas = $("rl-canvas");
    if (!canvas) return;
    const dpr = window.devicePixelRatio || 1;
    const W = canvas.clientWidth, H = canvas.clientHeight;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    const ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    const css = (n, d) => getComputedStyle(document.documentElement).getPropertyValue(n).trim() || d;
    const grid = css("--color-border", "#e2e8f0"), text = css("--color-text-muted", "#64748b");
    const pad = { l: 44, r: 12, t: 12, b: 28 };
    const span = (a) => { const lo = Math.min(...a), hi = Math.max(...a); const d = (hi - lo) || Math.abs(hi) || 1; return [lo - d * 0.08, hi + d * 0.08]; };
    const [x0, x1] = span(xs), [y0, y1] = span(ys.concat([r.intercept + r.slope * Math.min(...xs), r.intercept + r.slope * Math.max(...xs)]));
    const px = (x) => pad.l + ((x - x0) / (x1 - x0)) * (W - pad.l - pad.r);
    const py = (y) => H - pad.b - ((y - y0) / (y1 - y0)) * (H - pad.t - pad.b);
    ctx.font = "11px 'Roboto Mono', monospace";
    ctx.fillStyle = text;
    ctx.strokeStyle = grid;
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const gx = x0 + ((x1 - x0) * i) / 4, gy = y0 + ((y1 - y0) * i) / 4;
      ctx.beginPath(); ctx.moveTo(px(gx), pad.t); ctx.lineTo(px(gx), H - pad.b); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(pad.l, py(gy)); ctx.lineTo(W - pad.r, py(gy)); ctx.stroke();
      ctx.textAlign = "center"; ctx.fillText(fmt(gx, 3), px(gx), H - 10);
      ctx.textAlign = "right"; ctx.fillText(fmt(gy, 3), pad.l - 5, py(gy) + 4);
    }
    // recta de regresión
    const lx0 = Math.min(...xs), lx1 = Math.max(...xs);
    ctx.strokeStyle = "#dc2626"; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(px(lx0), py(r.intercept + r.slope * lx0)); ctx.lineTo(px(lx1), py(r.intercept + r.slope * lx1)); ctx.stroke();
    // puntos
    ctx.fillStyle = "#2563eb";
    xs.forEach((x, i) => { ctx.beginPath(); ctx.arc(px(x), py(ys[i]), 4, 0, Math.PI * 2); ctx.fill(); });
  }

  function calculate() {
    errorEl.classList.add("hidden");
    $("rl-data").classList.remove("field-error");
    try {
      let data;
      try {
        data = parsePairs($("rl-data").value);
      } catch (e) {
        $("rl-data").classList.add("field-error");
        throw e;
      }
      const r = regress(data.xs, data.ys);
      const sign = r.intercept < 0 ? "−" : "+";
      $("rl-main").textContent = `y = ${fmt(r.slope)}·x ${sign} ${fmt(Math.abs(r.intercept))}`;
      const lines = [
        `<p>Pendiente (b): <strong>${fmt(r.slope)}</strong> · Ordenada al origen (a): <strong>${fmt(r.intercept)}</strong></p>`,
        `<p>Coeficiente de correlación r: <strong>${Number.isNaN(r.r) ? "no definido" : fmt(r.r)}</strong> · R²: <strong>${Number.isNaN(r.r) ? "—" : fmt(r.r2)}</strong>${Number.isNaN(r.r) ? "" : ` (correlación ${strength(r.r)})`}</p>`,
        `<p>Datos: ${r.n} pares · media de x = ${fmt(r.meanX)} · media de y = ${fmt(r.meanY)}</p>`,
      ];
      const pxRaw = $("rl-predict").value.trim();
      if (pxRaw) {
        try {
          const px = toNumber(pxRaw);
          lines.push(`<p>Predicción: para x = ${fmt(px)} → <strong>y ≈ ${fmt(r.intercept + r.slope * px)}</strong></p>`);
        } catch (e) {
          $("rl-predict").classList.add("field-error");
          throw e;
        }
      }
      $("rl-lines").innerHTML = lines.join("");
      panel.classList.remove("hidden");
      drawChart(data.xs, data.ys, r);
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("rl-solve").addEventListener("click", calculate);
  document.querySelectorAll("[data-example]").forEach((btn) =>
    btn.addEventListener("click", () => {
      $("rl-data").value = btn.dataset.example.replace(/;/g, "\n");
      $("rl-predict").value = btn.dataset.predict || "";
      calculate();
    })
  );
})();
