/**
 * Cuotas vs contado — cuánto interés real tiene comprar en cuotas.
 * Tasa implícita: el valor presente de las cuotas (vencidas, iguales) iguala al precio de contado.
 *   precio = cuota × (1 − (1 + i)^−n) / i      → se despeja i por bisección.
 */
(function () {
  const presentValue = (payment, n, i) => (Math.abs(i) < 1e-12 ? payment * n : (payment * (1 - Math.pow(1 + i, -n))) / i);

  // Tasa periódica (mensual) implícita; negativa si se paga menos que el contado.
  function implicitRate(cash, payment, n) {
    if (!(cash > 0 && payment > 0 && n >= 1)) throw new Error("Los datos tienen que ser mayores a 0.");
    if (payment * n < cash * 0.5) throw new Error("Las cuotas suman menos de la mitad del precio de contado: revisá los datos.");
    let lo = -0.9, hi = 10;
    if (presentValue(payment, n, lo) < cash) throw new Error("Las cuotas son demasiado bajas para ese precio de contado.");
    if (presentValue(payment, n, hi) > cash) throw new Error("La tasa implícita es mayor al 1000 % mensual: revisá los datos.");
    for (let k = 0; k < 200; k++) {
      const mid = (lo + hi) / 2;
      if (presentValue(payment, n, mid) > cash) lo = mid;
      else hi = mid;
    }
    return (lo + hi) / 2;
  }

  if (typeof module !== "undefined") module.exports = { presentValue, implicitRate };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("cv-solve")) return;

  CCSimple.mount({
    prefix: "cv",
    compute(v, h) {
      const total = v.payment * v.n;
      const surcharge = total / v.cash - 1;
      const i = implicitRate(v.cash, v.payment, v.n);
      const tea = Math.pow(1 + i, 12) - 1;
      const lines = [
        `Total en cuotas: <strong>${h.money(total)}</strong> (${v.n} × ${h.money(v.payment)}) · Diferencia con el contado: <strong>${h.money(total - v.cash)}</strong>`,
        `Recargo total sobre el contado: <strong>${h.pct(surcharge)}</strong>`,
        `Tasa mensual implícita (TEM): <strong>${h.pct(i)}</strong> · TNA: ${h.pct(i * 12)} · TEA: ${h.pct(tea)}`,
        `Cuota sin interés sería ${h.money(v.cash / v.n)}.`,
      ];
      if (v.infl !== undefined && v.infl > 0) {
        const m = v.infl / 100;
        const pv = presentValue(v.payment, v.n, m);
        const diff = v.cash - pv;
        lines.push(
          diff > 0
            ? `Con una inflación de ${h.pct(m)} mensual, las cuotas valen hoy ${h.money(pv)}: pagar en cuotas te <strong>ahorra ${h.money(diff)}</strong> en valor de hoy (si lo que no pagás al contado lo invertís al ritmo de la inflación).`
            : `Con una inflación de ${h.pct(m)} mensual, las cuotas valen hoy ${h.money(pv)}: pagar de contado te <strong>ahorra ${h.money(-diff)}</strong> en valor de hoy.`
        );
      }
      return { label: "Tasa mensual implícita", main: h.pct(i), lines };
    },
  });
})();
