/**
 * Divisor de tensión — Vout = Vin · R2 / (R1 + R2).
 */
(function () {
  const vout = (vin, r1, r2) => (vin * r2) / (r1 + r2);
  function r2For(vin, vo, r1) {
    if (!(vo < vin)) throw new Error("La tensión de salida tiene que ser menor que la de entrada.");
    return (vo * r1) / (vin - vo);
  }
  const UNIT = { ohm: 1, k: 1e3, m: 1e6 };

  if (typeof module !== "undefined") module.exports = { vout, r2For };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("dv-solve")) return;

  const fmtR = (ohms, h) => (ohms >= 1e6 ? `${h.fmt(ohms / 1e6, 4)} MΩ` : ohms >= 1e3 ? `${h.fmt(ohms / 1e3, 4)} kΩ` : `${h.fmt(ohms, 4)} Ω`);

  CCSimple.mount({
    prefix: "dv",
    compute(v, h) {
      const u = UNIT[v.unit];
      const r1 = v.r1 * u;
      if (v.mode === "vout") {
        const r2 = v.r2 * u;
        const vo = vout(v.vin, r1, r2);
        const i = v.vin / (r1 + r2);
        return { label: "Tensión de salida", main: `${h.fmt(vo, 4)} V`, lines: [`Corriente por el divisor: <strong>${h.fmt(i * 1000, 4)} mA</strong> · Potencia total: ${h.fmt(v.vin * i * 1000, 4)} mW.`, `Caída en R1: ${h.fmt(v.vin - vo, 4)} V · en R2: ${h.fmt(vo, 4)} V.`, `Vout = Vin × R2 / (R1 + R2) = ${h.fmt(v.vin, 3)} × ${fmtR(r2, h)} / (${fmtR(r1, h)} + ${fmtR(r2, h)})`] };
      }
      const r2 = r2For(v.vin, v.vout, r1);
      return { label: "Resistencia R2 necesaria", main: fmtR(r2, h), lines: [`Para obtener ${h.fmt(v.vout, 3)} V a partir de ${h.fmt(v.vin, 3)} V con R1 = ${fmtR(r1, h)}.`, `Corriente: ${h.fmt((v.vin / (r1 + r2)) * 1000, 4)} mA.`, "Usá el valor comercial más cercano (serie E12 o E24) y verificá la tensión resultante."] };
    },
  });
})();
