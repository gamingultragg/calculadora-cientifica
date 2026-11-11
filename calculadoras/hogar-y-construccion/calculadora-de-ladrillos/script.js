/**
 * Ladrillos para una pared — unidades por m² a partir de las medidas de la cara colocada y la junta.
 *   unidades por m² = 10.000 / ((largo + junta) × (alto + junta))   (medidas en cm)
 */
(function () {
  const perM2 = (lenCm, heightCm, jointCm) => 10000 / ((lenCm + jointCm) * (heightCm + jointCm));
  const bricks = (areaM2, lenCm, heightCm, jointCm, wastePct) => {
    const base = areaM2 * perM2(lenCm, heightCm, jointCm);
    return { perM2: perM2(lenCm, heightCm, jointCm), base, total: Math.ceil(base * (1 + wastePct / 100) - 1e-9) };
  };

  if (typeof module !== "undefined") module.exports = { perM2, bricks };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("la-solve")) return;

  CCSimple.mount({
    prefix: "la",
    compute(v, h) {
      const area = v.mode === "medidas" ? v.wlen * v.wheight - (v.openings || 0) : v.area;
      if (!(area > 0)) throw new Error("La superficie de pared tiene que ser mayor a 0.");
      const [l, a] = String(v.brick).split("x").map(Number);
      const r = bricks(area, l, a, v.joint, v.waste);
      const lines = [
        `Superficie de pared: <strong>${h.fmt(area, 2)} m²</strong>.`,
        `Con el ladrillo de ${h.fmt(l, 1)} × ${h.fmt(a, 1)} cm y juntas de ${h.fmt(v.joint, 1)} cm entran <strong>${h.fmt(r.perM2, 1)} unidades por m²</strong>.`,
        `${h.fmt(r.base, 0)} unidades + ${h.fmt(v.waste, 0)} % de desperdicio por roturas y cortes = ${h.fmt(r.total, 0)}.`,
      ];
      return { label: "Ladrillos a comprar", main: `${h.fmt(r.total, 0)} unidades`, lines };
    },
  });
})();
