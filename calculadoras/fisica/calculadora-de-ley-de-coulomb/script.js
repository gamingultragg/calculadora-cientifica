/**
 * Ley de Coulomb — F = k·q₁·q₂ / r², con k = 8,9875517923 × 10⁹ N·m²/C².
 * Fuerza positiva = repulsiva (cargas del mismo signo); negativa = atractiva (signos opuestos).
 */
(function () {
  const K = 8.9875517923e9;
  const CHARGE = { C: 1, mC: 1e-3, uC: 1e-6, nC: 1e-9, pC: 1e-12 };
  const DIST = { m: 1, cm: 1e-2, mm: 1e-3 };

  const force = (q1, q2, r) => (K * q1 * q2) / (r * r);
  const distance = (F, q1, q2) => Math.sqrt((K * Math.abs(q1 * q2)) / Math.abs(F));
  const charge2 = (F, q1, r) => (Math.abs(F) * r * r) / (K * Math.abs(q1));

  if (typeof module !== "undefined") module.exports = { K, CHARGE, DIST, force, distance, charge2 };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("cl-solve")) return;

  // Número legible: decimales normales o notación científica cuando es muy grande o muy chico.
  const show = (h, n, d = 4) => {
    if (n === 0) return "0";
    return Math.abs(n) >= 1e6 || Math.abs(n) < 1e-3 ? n.toExponential(4).replace(".", ",").replace("e+", " × 10^").replace("e-", " × 10^−") : h.fmt(n, d);
  };

  CCSimple.mount({
    prefix: "cl",
    compute(v, h) {
      const q1 = v.q1 * CHARGE[v.q1u];
      if (q1 === 0) throw new Error('"Carga 1" no puede ser 0.');
      if (v.mode === "f") {
        const q2 = v.q2 * CHARGE[v.q2u];
        if (q2 === 0) throw new Error('"Carga 2" no puede ser 0.');
        const r = v.r * DIST[v.ru];
        const F = force(q1, q2, r);
        const kind = F > 0 ? "<strong>repulsiva</strong> (cargas del mismo signo: se alejan)" : "<strong>atractiva</strong> (cargas de signo opuesto: se acercan)";
        return {
          label: "Fuerza eléctrica",
          main: `${show(h, Math.abs(F))} N`,
          lines: [`F = k·q₁·q₂ / r² = ${show(h, K)} × ${show(h, q1)} × ${show(h, q2)} / ${show(h, r)}² = ${show(h, Math.abs(F))} N.`, `La fuerza es ${kind}.`, "Cada carga recibe una fuerza de igual intensidad y sentido contrario sobre la otra (tercera ley de Newton)."],
        };
      }
      if (v.mode === "r") {
        const q2 = v.q2 * CHARGE[v.q2u];
        if (q2 === 0) throw new Error('"Carga 2" no puede ser 0.');
        const r = distance(v.F, q1, q2);
        return { label: "Distancia entre las cargas", main: `${show(h, r)} m`, lines: [`r = √(k·|q₁·q₂| / F) = √(${show(h, K)} × ${show(h, Math.abs(q1 * q2))} / ${show(h, v.F)}) = ${show(h, r)} m = ${show(h, r * 100)} cm.`] };
      }
      const r = v.r * DIST[v.ru];
      const q2 = charge2(v.F, q1, r);
      return { label: "Carga 2 (valor absoluto)", main: `${show(h, q2)} C`, lines: [`|q₂| = F·r² / (k·|q₁|) = ${show(h, q2)} C = ${show(h, q2 * 1e6)} µC.`, "El signo de q₂ se deduce de si la fuerza es atractiva (opuesto a q₁) o repulsiva (igual a q₁)."] };
    },
  });
})();
