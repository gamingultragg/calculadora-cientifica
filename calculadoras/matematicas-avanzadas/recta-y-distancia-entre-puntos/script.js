/**
 * Recta y distancia entre dos puntos — pendiente, ecuación, distancia, punto medio y ángulo de inclinación.
 *   m = (y₂ − y₁)/(x₂ − x₁)   ·   d = √((x₂ − x₁)² + (y₂ − y₁)²)   ·   M = ((x₁ + x₂)/2, (y₁ + y₂)/2)
 * Forma general: A·x + B·y + C = 0 con A = y₂ − y₁, B = x₁ − x₂, C = x₂·y₁ − x₁·y₂.
 */
(function () {
  function line(x1, y1, x2, y2) {
    const dx = x2 - x1;
    const dy = y2 - y1;
    if (dx === 0 && dy === 0) throw new Error("Los dos puntos son iguales: no definen una recta. Cambiá alguno de los valores.");
    const vertical = dx === 0;
    const slope = vertical ? null : dy / dx;
    let incl = (Math.atan2(dy, dx) * 180) / Math.PI; // ángulo de la recta con el eje x, entre 0° y 180°
    if (incl < 0) incl += 180;
    if (incl >= 180) incl -= 180;
    return {
      dx,
      dy,
      vertical,
      slope,
      b: vertical ? null : y1 - slope * x1,
      distance: Math.hypot(dx, dy),
      mid: [(x1 + x2) / 2, (y1 + y2) / 2],
      incl,
      A: dy,
      B: -dx,
      C: x2 * y1 - x1 * y2,
    };
  }

  if (typeof module !== "undefined") module.exports = { line };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("rc-solve")) return;

  CCSimple.mount({
    prefix: "rc",
    compute(v, h) {
      const f = (x) => h.fmt(Object.is(x, -0) ? 0 : x, 4).replace("-", "−");
      const r = line(v.x1, v.y1, v.x2, v.y2);
      const sign = (n) => (n < 0 ? "−" : "+");
      let eq;
      if (r.vertical) eq = `x = ${f(v.x1)}`;
      else if (r.slope === 0) eq = `y = ${f(r.b)}`;
      else {
        const m = Math.abs(r.slope) === 1 ? "" : f(Math.abs(r.slope));
        eq = `y = ${r.slope < 0 ? "−" : ""}${m}x` + (Math.abs(r.b) < 1e-12 ? "" : ` ${sign(r.b)} ${f(Math.abs(r.b))}`);
      }
      const terms = [[r.A, "x"], [r.B, "y"], [r.C, ""]].filter(([n]) => Math.abs(n) >= 1e-12);
      const general = terms.map(([n, s], i) => (i === 0 ? (n < 0 ? "−" : "") : n < 0 ? " − " : " + ") + f(Math.abs(n)) + s).join("") + " = 0";
      const lines = [
        r.vertical
          ? "Pendiente: <strong>indefinida</strong> (recta vertical, x₂ = x₁)."
          : `Pendiente: m = (${f(v.y2)} − ${f(v.y1)}) / (${f(v.x2)} − ${f(v.x1)}) = <strong>${f(r.slope)}</strong>.`,
        r.vertical ? null : `Ordenada al origen: b = ${f(r.b)} (la recta corta al eje y en el punto (0; ${f(r.b)})).`,
        `Forma general: ${general}`,
        `Distancia entre los puntos: d = √(${f(r.dx)}² + ${f(r.dy)}²) = <strong>${f(r.distance)}</strong>.`,
        `Punto medio: M = (${f(r.mid[0])}; ${f(r.mid[1])}).`,
        `Ángulo de inclinación: ${f(r.incl)}° respecto del eje x.`,
        r.vertical
          ? "Una recta paralela es otra vertical; una perpendicular es horizontal (pendiente 0)."
          : r.slope === 0
            ? "Una recta perpendicular es vertical (pendiente indefinida)."
            : `Una recta paralela tiene pendiente ${f(r.slope)}; una perpendicular, ${f(-1 / r.slope)}.`,
      ];
      return { label: "Ecuación de la recta", main: eq, lines };
    },
  });
})();
