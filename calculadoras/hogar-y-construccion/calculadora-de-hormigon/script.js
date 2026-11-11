/**
 * Hormigón — volumen de una losa/platea o de columnas, y materiales aproximados por m³.
 * Las dosificaciones son orientativas (por m³ de hormigón elaborado en obra): el cálculo estructural
 * y la dosificación real los define un profesional.
 */
(function () {
  const DOSAGE = {
    H13: { name: "H-13", cement: 280, sand: 0.55, stone: 0.8, water: 190 },
    H17: { name: "H-17", cement: 330, sand: 0.52, stone: 0.8, water: 185 },
    H21: { name: "H-21", cement: 380, sand: 0.5, stone: 0.78, water: 185 },
  };
  const volumeSlab = (lenM, widthM, thicknessCm) => lenM * widthM * (thicknessCm / 100);
  const volumeColumns = (sideACm, sideBCm, heightM, qty) => (sideACm / 100) * (sideBCm / 100) * heightM * qty;
  const materials = (m3, key) => {
    const d = DOSAGE[key];
    return { cementKg: d.cement * m3, bags: Math.ceil((d.cement * m3) / 50 - 1e-9), sand: d.sand * m3, stone: d.stone * m3, water: d.water * m3 };
  };

  if (typeof module !== "undefined") module.exports = { DOSAGE, volumeSlab, volumeColumns, materials };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("hm-solve")) return;

  CCSimple.mount({
    prefix: "hm",
    compute(v, h) {
      const base = v.shape === "losa" ? volumeSlab(v.length, v.width, v.thickness) : volumeColumns(v.sa, v.sb, v.height, v.qty);
      const total = base * (1 + (v.waste || 0) / 100);
      const m = materials(total, v.grade);
      const lines = [
        `Volumen calculado: ${h.fmt(base, 3)} m³ + ${h.fmt(v.waste || 0, 0)} % de desperdicio = <strong>${h.fmt(total, 2)} m³</strong>.`,
        `Para ${DOSAGE[v.grade].name}: cemento <strong>${h.fmt(m.cementKg, 0)} kg (${m.bags} bolsas de 50 kg)</strong>.`,
        `Arena: <strong>${h.fmt(m.sand, 2)} m³</strong> · Piedra partida: <strong>${h.fmt(m.stone, 2)} m³</strong> · Agua: ${h.fmt(m.water, 0)} litros.`,
        `Si lo pedís elaborado, pedí ${h.fmt(Math.ceil(total * 10) / 10, 1)} m³.`,
      ];
      return { label: "Volumen de hormigón", main: `${h.fmt(total, 2)} m³`, lines };
    },
  });
})();
