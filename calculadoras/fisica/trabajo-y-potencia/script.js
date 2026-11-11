/**
 * Trabajo y potencia — W = F·d·cos(θ) y P = W/t. 1 CV = 735,5 W y 1 HP = 745,7 W.
 */
(function () {
  const work = (force, distance, angleDeg) => force * distance * Math.cos((angleDeg * Math.PI) / 180);
  const power = (workJ, timeS) => workJ / timeS;

  if (typeof module !== "undefined") module.exports = { work, power };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("wp-solve")) return;

  CCSimple.mount({
    prefix: "wp",
    compute(v, h) {
      const f = (x) => h.fmt(x, 4);
      if ((v.angle || 0) > 180) throw new Error('"Ángulo" tiene que estar entre 0° y 180°.');
      const W = work(v.force, v.distance, v.angle || 0);
      const lines = [`W = F·d·cos θ = ${f(v.force)} N × ${f(v.distance)} m × cos ${f(v.angle || 0)}° = <strong>${f(W)} J</strong> (${f(W / 1000)} kJ).`];
      if (v.time) {
        const P = power(W, v.time);
        lines.push(`Potencia: P = W/t = ${f(W)} / ${f(v.time)} = <strong>${f(P)} W</strong> = ${f(P / 1000)} kW = ${f(P / 735.5)} CV = ${f(P / 745.7)} HP.`);
      }
      if (W < 0) lines.push("El trabajo es negativo: la fuerza se opone al desplazamiento (por ejemplo, el rozamiento).");
      return { label: "Trabajo realizado", main: `${f(W)} J`, lines };
    },
  });
})();
