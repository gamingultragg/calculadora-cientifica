/**
 * Meta de ahorro — cuánto aportar por mes (o cuántos meses hacen falta) para llegar a un monto, con tasa opcional.
 * Aportes al final de cada mes y capitalización mensual (i = TNA / 12):
 *   VF = P·(1 + i)ⁿ + A·((1 + i)ⁿ − 1) / i
 */
(function () {
  const futureValue = (P, A, i, n) => (i === 0 ? P + A * n : P * Math.pow(1 + i, n) + (A * (Math.pow(1 + i, n) - 1)) / i);

  function contribution(goal, P, i, n) {
    if (P >= goal) throw new Error("Con el capital inicial ya alcanzás la meta: no hace falta ahorrar más.");
    if (i === 0) return (goal - P) / n;
    const growth = Math.pow(1 + i, n);
    const A = ((goal - P * growth) * i) / (growth - 1);
    if (A <= 0) throw new Error("Con el capital inicial y el interés ya alcanzás la meta en ese plazo: no hace falta aportar.");
    return A;
  }

  // Meses (puede ser fraccionario) para llegar a la meta aportando A por mes.
  function months(goal, P, A, i) {
    if (P >= goal) throw new Error("Con el capital inicial ya alcanzás la meta: no hace falta ahorrar más.");
    if (i === 0) return (goal - P) / A;
    return Math.log((goal * i + A) / (P * i + A)) / Math.log(1 + i);
  }

  if (typeof module !== "undefined") module.exports = { futureValue, contribution, months };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("ma-solve")) return;

  const span = (h, m) => {
    const total = Math.ceil(m - 1e-9);
    const y = Math.floor(total / 12);
    const mm = total % 12;
    return total + " meses" + (y > 0 ? ` (${y} año${y === 1 ? "" : "s"}${mm ? ` y ${mm} mes${mm === 1 ? "" : "es"}` : ""})` : "");
  };

  CCSimple.mount({
    prefix: "ma",
    compute(v, h) {
      const i = (v.tna || 0) / 100 / 12;
      const P = v.initial || 0;
      if (v.mode === "aporte") {
        if (v.months > 1200) throw new Error('"Plazo" no puede superar los 1.200 meses (100 años).');
        const A = contribution(v.goal, P, i, v.months);
        const contributed = A * v.months;
        const interest = v.goal - P - contributed;
        return {
          label: "Aporte mensual necesario",
          main: h.money(A),
          lines: [
            `Para llegar a ${h.money(v.goal)} en ${span(h, v.months)} tenés que ahorrar <strong>${h.money(A)} por mes</strong>.`,
            `Total que ponés de tu bolsillo: ${h.money(contributed + P)}${P > 0 ? ` (incluye el capital inicial de ${h.money(P)})` : ""}.`,
            i > 0 ? `Interés ganado: ${h.money(interest)} (TNA ${h.fmt(v.tna, 2)} %, capitalización mensual).` : "Sin interés: es la meta dividida por la cantidad de meses.",
            "No considera la inflación: en un contexto inflacionario, el monto de la meta pierde poder de compra con el tiempo.",
          ],
        };
      }
      if (P >= v.goal) throw new Error("Con el capital inicial ya alcanzás la meta: no hace falta ahorrar más.");
      const m = months(v.goal, P, v.amount, i);
      if (!Number.isFinite(m) || m > 1200) throw new Error("Con ese aporte la meta tarda más de 100 años: probá con un aporte mayor.");
      const n = Math.ceil(m - 1e-9);
      return {
        label: "Tiempo para llegar a la meta",
        main: span(h, m),
        lines: [
          `Aportando ${h.money(v.amount)} por mes, llegás a ${h.money(v.goal)} en <strong>${span(h, m)}</strong>.`,
          `Total aportado: ${h.money(v.amount * n + P)}${i > 0 ? ` · Interés ganado: ${h.money(futureValue(P, v.amount, i, n) - P - v.amount * n)}.` : "."}`,
          "No considera la inflación ni impuestos.",
        ],
      };
    },
  });
})();
