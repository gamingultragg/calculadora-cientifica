/**
 * Sistemas de ecuaciones lineales 2×2 y 3×3 — regla de Cramer.
 */
(function () {
  const EPS = 1e-12;
  const det2 = (a, b, c, d) => a * d - b * c;
  const det3 = (m) =>
    m[0][0] * det2(m[1][1], m[1][2], m[2][1], m[2][2]) -
    m[0][1] * det2(m[1][0], m[1][2], m[2][0], m[2][2]) +
    m[0][2] * det2(m[1][0], m[1][1], m[2][0], m[2][1]);

  // a1 x + b1 y = d1 ; a2 x + b2 y = d2
  function solve2(a1, b1, d1, a2, b2, d2) {
    const det = det2(a1, b1, a2, b2);
    if (Math.abs(det) < EPS) return { det: 0 };
    return { det, x: det2(d1, b1, d2, b2) / det, y: det2(a1, d1, a2, d2) / det };
  }

  // matriz A (3×3) y vector d
  function solve3(A, d) {
    const det = det3(A);
    if (Math.abs(det) < EPS) return { det: 0 };
    const rep = (col) => A.map((row, i) => row.map((v, j) => (j === col ? d[i] : v)));
    return { det, x: det3(rep(0)) / det, y: det3(rep(1)) / det, z: det3(rep(2)) / det };
  }

  if (typeof module !== "undefined") module.exports = { det2, det3, solve2, solve3 };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("se-solve")) return;

  CCSimple.mount({
    prefix: "se",
    compute(v, h) {
      const f = (n) => h.fmt(n, 6);
      if (v.size === "2") {
        const r = solve2(v.a1, v.b1, v.d1, v.a2, v.b2, v.d2);
        if (r.det === 0) throw new Error("El sistema no tiene solución única (determinante 0): las ecuaciones son incompatibles o dependientes.");
        return {
          label: "Solución", main: `x = ${f(r.x)} · y = ${f(r.y)}`,
          lines: [`Determinante del sistema: <strong>${f(r.det)}</strong>`, `Regla de Cramer: x = Δx/Δ = ${f(det2(v.d1, v.b1, v.d2, v.b2))}/${f(r.det)}, y = Δy/Δ = ${f(det2(v.a1, v.d1, v.a2, v.d2))}/${f(r.det)}`,
            `Verificación: ${f(v.a1 * r.x + v.b1 * r.y)} = ${f(v.d1)} y ${f(v.a2 * r.x + v.b2 * r.y)} = ${f(v.d2)}`],
        };
      }
      const A = [[v.a1, v.b1, v.c1], [v.a2, v.b2, v.c2], [v.a3, v.b3, v.c3]];
      const r = solve3(A, [v.d1, v.d2, v.d3]);
      if (r.det === 0) throw new Error("El sistema no tiene solución única (determinante 0): las ecuaciones son incompatibles o dependientes.");
      return {
        label: "Solución", main: `x = ${f(r.x)} · y = ${f(r.y)} · z = ${f(r.z)}`,
        lines: [`Determinante del sistema: <strong>${f(r.det)}</strong>`, "Se resolvió con la regla de Cramer: cada incógnita es el cociente entre un determinante (con su columna reemplazada por los términos independientes) y el determinante del sistema."],
      };
    },
  });
})();
