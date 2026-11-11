/**
 * Cerámicos y pisos — cuántas piezas y cajas comprar para cubrir un ambiente, con desperdicio por cortes.
 */
(function () {
  function tiles(areaM2, pieceLenCm, pieceWidthCm, wastePct) {
    const pieceArea = (pieceLenCm / 100) * (pieceWidthCm / 100);
    const withWaste = areaM2 * (1 + wastePct / 100);
    const pieces = Math.ceil(withWaste / pieceArea - 1e-9);
    return { pieceArea, withWaste, pieces, buyArea: pieces * pieceArea };
  }

  if (typeof module !== "undefined") module.exports = { tiles };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("ce-solve")) return;

  CCSimple.mount({
    prefix: "ce",
    compute(v, h) {
      const area = v.length * v.width - (v.skip || 0);
      if (area <= 0) throw new Error("La superficie a cubrir tiene que ser mayor a 0 (revisá lo que descontás).");
      const t = tiles(area, v.plen, v.pwid, v.waste);
      const lines = [
        `Superficie a cubrir: <strong>${h.fmt(area, 2)} m²</strong> (${h.fmt(v.length, 2)} × ${h.fmt(v.width, 2)} m${v.skip ? ` − ${h.fmt(v.skip, 2)} m²` : ""}).`,
        `Con ${h.fmt(v.waste, 0)} % de desperdicio: ${h.fmt(t.withWaste, 2)} m² → comprás <strong>${h.fmt(t.buyArea, 2)} m²</strong>.`,
        v.box ? `Cajas: <strong>${Math.ceil(t.pieces / v.box)}</strong> (de ${v.box} piezas; sobran ${Math.ceil(t.pieces / v.box) * v.box - t.pieces} piezas).` : "",
        `Cada pieza de ${h.fmt(v.plen, 1)} × ${h.fmt(v.pwid, 1)} cm cubre ${h.fmt(t.pieceArea, 4)} m².`,
      ];
      return { label: "Piezas a comprar", main: `${h.fmt(t.pieces, 0)} piezas`, lines };
    },
  });
})();
