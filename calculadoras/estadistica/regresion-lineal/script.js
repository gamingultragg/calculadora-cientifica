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
