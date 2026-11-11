/**
 * Caída libre y tiro oblicuo (sin rozamiento del aire).
 *   caída libre desde h:   t = √(2h/g)    v = g·t
 *   tiro oblicuo:          y(t) = h₀ + v₀·sen(θ)·t − ½·g·t²     x(t) = v₀·cos(θ)·t
 */
(function () {
  function freeFall(height, g) {
    const t = Math.sqrt((2 * height) / g);
    return { time: t, speed: g * t };
  }

  function projectile(v0, angleDeg, h0, g) {
    const th = (angleDeg * Math.PI) / 180;
    const vx = v0 * Math.cos(th), vy = v0 * Math.sin(th);
    const time = (vy + Math.sqrt(vy * vy + 2 * g * h0)) / g;
    const maxHeight = h0 + (vy > 0 ? (vy * vy) / (2 * g) : 0);
    const impactVy = vy - g * time;
    return { vx, vy, time, range: vx * time, maxHeight, impactSpeed: Math.hypot(vx, impactVy), timeToTop: vy > 0 ? vy / g : 0 };
  }

  if (typeof module !== "undefined") module.exports = { freeFall, projectile };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("tr-solve")) return;

  CCSimple.mount({
    prefix: "tr",
    compute(v, h) {
      const g = v.g || 9.81;
      const f = (x) => h.fmt(x, 3);
      if (v.mode === "caida") {
        const r = freeFall(v.height, g);
        return { label: "Tiempo de caída", main: `${f(r.time)} s`, lines: [`Velocidad al llegar al suelo: <strong>${f(r.speed)} m/s</strong> (${f(r.speed * 3.6)} km/h).`, `t = √(2·h/g) = √(2 × ${f(v.height)} / ${f(g)}) · v = g·t`] };
      }
      if (v.angle > 90) throw new Error('"Ángulo" tiene que estar entre 0° y 90°.');
      const r = projectile(v.v0, v.angle, v.h0 || 0, g);
      return { label: "Alcance horizontal", main: `${f(r.range)} m`, lines: [`Altura máxima: <strong>${f(r.maxHeight)} m</strong> (a los ${f(r.timeToTop)} s).`, `Tiempo total en el aire: <strong>${f(r.time)} s</strong>.`, `Velocidad al llegar al suelo: ${f(r.impactSpeed)} m/s.`, `Componentes iniciales: vₓ = ${f(r.vx)} m/s, v_y = ${f(r.vy)} m/s.`] };
    },
  });
})();
