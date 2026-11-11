/**
 * Estequiometría y reactivo limitante. Con la ecuación balanceada, los moles se relacionan por sus coeficientes.
 *   producto: n(B) = n(A) · cB / cA     masa(B) = n(B) · M(B)
 *   limitante: el reactivo con menor n / coeficiente se agota primero.
 */
(function () {
  function product(massA, mA, cA, cB, mB, yieldPct = 100) {
    const nA = massA / mA;
    const nB = (nA * cB) / cA;
    const theoretical = nB * mB;
    return { nA, nB, theoretical, actual: (theoretical * yieldPct) / 100 };
  }

  // reactivos A y B; producto P
  function limiting(a, b, p) {
    const nA = a.mass / a.molar, nB = b.mass / b.molar;
    const extentA = nA / a.coef, extentB = nB / b.coef;
    const aLimits = extentA <= extentB;
    const extent = Math.min(extentA, extentB);
    const nP = extent * p.coef;
    const excess = aLimits ? { name: "B", left: nB - extent * b.coef, molar: b.molar } : { name: "A", left: nA - extent * a.coef, molar: a.molar };
    return { limiting: aLimits ? "A" : "B", nA, nB, extent, nP, massP: nP * p.molar, excessName: excess.name, excessMoles: excess.left, excessMass: excess.left * excess.molar };
  }

  if (typeof module !== "undefined") module.exports = { product, limiting };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("st-solve")) return;

  CCSimple.mount({
    prefix: "st",
    compute(v, h) {
      const f = (x) => h.fmt(x, 4);
      if (v.mode === "producto") {
        const r = product(v.massA, v.mA, v.cA, v.cP, v.mP, v.yield === undefined ? 100 : v.yield);
        return { label: "Masa de producto", main: `${f(r.actual)} g`, lines: [`Moles de A: ${f(r.nA)} mol → moles de producto: <strong>${f(r.nB)} mol</strong>.`, `Masa teórica (100 % de rendimiento): ${f(r.theoretical)} g${v.yield !== undefined && v.yield !== 100 ? ` · con ${f(v.yield)} % de rendimiento: ${f(r.actual)} g` : ""}.`, `Relación estequiométrica: ${v.cA} mol de A producen ${v.cP} mol de producto.`] };
      }
      const r = limiting({ mass: v.massA, molar: v.mA, coef: v.cA }, { mass: v.massB, molar: v.mB, coef: v.cB }, { coef: v.cP, molar: v.mP });
      const lim = r.limiting === "A" ? "A" : "B";
      return { label: "Reactivo limitante", main: `El reactivo ${lim}`, lines: [`Se forman <strong>${f(r.nP)} mol</strong> de producto = <strong>${f(r.massP)} g</strong>.`, `Moles iniciales: A = ${f(r.nA)} mol · B = ${f(r.nB)} mol.`, `Sobra reactivo ${r.excessName}: ${f(r.excessMoles)} mol (${f(r.excessMass)} g).`] };
    },
  });
})();
