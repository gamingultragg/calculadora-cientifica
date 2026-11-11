/**
 * Pintura — litros necesarios para las paredes (y el techo) de una habitación, según manos y rendimiento.
 */
(function () {
  function paintArea(length, width, height, openings, ceiling) {
    const walls = 2 * (length + width) * height - openings;
    const ceilingArea = ceiling ? length * width : 0;
    return { walls, ceilingArea, total: walls + ceilingArea };
  }
  const liters = (area, coats, yieldM2PerL) => (area * coats) / yieldM2PerL;

  // Combinación de latas (4, 10 y 20 L) que cubre los litros con el menor sobrante.
  function cans(neededL) {
    let best = null;
    for (let c20 = 0; c20 <= Math.ceil(neededL / 20); c20++) {
      for (let c10 = 0; c10 <= Math.ceil(neededL / 10); c10++) {
        const rest = neededL - c20 * 20 - c10 * 10;
        const c4 = rest > 0 ? Math.ceil(rest / 4 - 1e-9) : 0;
        const total = c20 * 20 + c10 * 10 + c4 * 4;
        const count = c20 + c10 + c4;
        if (!best || total < best.total || (total === best.total && count < best.count)) best = { c20, c10, c4, total, count };
      }
    }
    return best;
  }

  if (typeof module !== "undefined") module.exports = { paintArea, liters, cans };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("pi-solve")) return;

  CCSimple.mount({
    prefix: "pi",
    compute(v, h) {
      const a = paintArea(v.length, v.width, v.height, v.openings || 0, v.ceiling === "si");
      if (a.walls <= 0) throw new Error("Las aberturas descontadas son mayores que la superficie de las paredes.");
      const L = liters(a.total, v.coats, v.yield);
      const c = cans(L);
      const parts = [c.c20 && `${c.c20} × 20 L`, c.c10 && `${c.c10} × 10 L`, c.c4 && `${c.c4} × 4 L`].filter(Boolean).join(" + ");
      const lines = [
        `Superficie a pintar: <strong>${h.fmt(a.total, 2)} m²</strong> (paredes ${h.fmt(a.walls, 2)} m²${a.ceilingArea ? ` + techo ${h.fmt(a.ceilingArea, 2)} m²` : ""}).`,
        `${v.coats} ${v.coats === 1 ? "mano" : "manos"} con un rendimiento de ${h.fmt(v.yield, 1)} m²/L → ${h.fmt(L, 2)} litros.`,
        `Latas sugeridas: <strong>${parts}</strong> (${c.total} L en total).`,
      ];
      return { label: "Pintura necesaria", main: `${h.fmt(L, 1)} litros`, lines };
    },
  });
})();
