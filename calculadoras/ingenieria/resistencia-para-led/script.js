/**
 * Resistencia limitadora para un LED — R = (Vfuente − Vf) / I.
 */
(function () {
  const E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2];

  function ledResistor(vs, vf, milliamps) {
    if (!(vs > vf)) throw new Error("La tensión de la fuente tiene que ser mayor que la del LED.");
    const r = (vs - vf) / (milliamps / 1000);
    return { r, power: (vs - vf) * (milliamps / 1000) };
  }

  // Menor valor de la serie E12 que sea mayor o igual a r (más seguro: menos corriente).
  function nextE12(r) {
    const decade = Math.pow(10, Math.floor(Math.log10(r)));
    for (const base of [...E12, 10]) {
      const value = Math.round(base * decade * 100) / 100;
      if (value >= r - 1e-9) return value;
    }
    return r;
  }

  if (typeof module !== "undefined") module.exports = { ledResistor, nextE12 };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("le-solve")) return;

  const fmtR = (ohms, h) => (ohms >= 1e3 ? `${h.fmt(ohms / 1e3, 3)} kΩ` : `${h.fmt(ohms, 1)} Ω`);

  CCSimple.mount({
    prefix: "le",
    compute(v, h) {
      const n = v.leds || 1;
      const r = ledResistor(v.vs, v.vf * n, v.ma);
      const std = nextE12(r.r);
      const realMa = ((v.vs - v.vf * n) / std) * 1000;
      return { label: "Resistencia calculada", main: fmtR(r.r, h), lines: [`Valor comercial recomendado (serie E12, hacia arriba): <strong>${fmtR(std, h)}</strong> → corriente real ≈ ${h.fmt(realMa, 2)} mA.`, `Potencia en la resistencia: ${h.fmt(r.power * 1000, 2)} mW (usá una de ¼ W si es menor a 250 mW).`, `R = (Vs − ${n > 1 ? `${n} × ` : ""}Vf) / I = (${h.fmt(v.vs, 2)} − ${h.fmt(v.vf * n, 2)}) / ${h.fmt(v.ma / 1000, 4)} A`] };
    },
  });
})();
