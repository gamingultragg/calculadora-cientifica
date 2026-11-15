/**
 * Leyes de los gases (cantidad de gas constante) — P₁·V₁ / T₁ = P₂·V₂ / T₂, con T en kelvin.
 * Casos particulares: Boyle (T constante), Charles (P constante) y Gay-Lussac (V constante).
 * La presión y el volumen se simplifican, así que solo hace falta usar la misma unidad en el estado 1 y en el 2.
 */
(function () {
  function toKelvin(t, unit) {
    const k = unit === "C" ? t + 273.15 : t;
    if (!(k > 0)) throw new Error("La temperatura tiene que estar por encima del cero absoluto (−273,15 °C o 0 K).");
    return k;
  }
  const fromKelvin = (k, unit) => (unit === "C" ? k - 273.15 : k);
  const solveP2 = (p1, v1, t1, v2, t2) => (p1 * v1 * t2) / (t1 * v2);
  const solveV2 = (p1, v1, t1, p2, t2) => (p1 * v1 * t2) / (t1 * p2);
  const solveT2 = (p1, v1, t1, p2, v2) => (p2 * v2 * t1) / (p1 * v1);
  const close = (a, b) => Math.abs(a - b) <= 1e-9 * Math.max(Math.abs(a), Math.abs(b), 1);
  function lawName(p1, v1, t1, p2, v2, t2) {
    if (close(t1, t2) && !close(p1, p2)) return "Ley de Boyle (temperatura constante: P·V = constante)";
    if (close(p1, p2) && !close(v1, v2)) return "Ley de Charles (presión constante: V/T = constante)";
    if (close(v1, v2) && !close(p1, p2)) return "Ley de Gay-Lussac (volumen constante: P/T = constante)";
    return "Ley combinada de los gases (cambian las tres magnitudes)";
  }

  if (typeof module !== "undefined") module.exports = { toKelvin, fromKelvin, solveP2, solveV2, solveT2, lawName };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("gl-solve")) return;

  const PU = { atm: "atm", kPa: "kPa", mmHg: "mmHg", bar: "bar", psi: "psi" };
  const VU = { L: "L", mL: "mL", m3: "m³", cm3: "cm³" };

  CCSimple.mount({
    prefix: "gl",
    compute(v, h) {
      const f = (x) => h.fmt(x, 4);
      const pu = PU[v.pu];
      const vu = VU[v.vu];
      const tu = v.tu === "C" ? "°C" : "K";
      const t1 = toKelvin(v.t1, v.tu);
      let p2 = v.p2;
      let v2 = v.v2;
      let t2 = v.t2 !== undefined ? toKelvin(v.t2, v.tu) : undefined;
      let label;
      let main;
      if (v.mode === "p2") {
        p2 = solveP2(v.p1, v.v1, t1, v2, t2);
        label = "Presión final (P₂)";
        main = `${f(p2)} ${pu}`;
      } else if (v.mode === "v2") {
        v2 = solveV2(v.p1, v.v1, t1, p2, t2);
        label = "Volumen final (V₂)";
        main = `${f(v2)} ${vu}`;
      } else {
        t2 = solveT2(v.p1, v.v1, t1, p2, v2);
        if (!(t2 > 0)) throw new Error("La temperatura final da por debajo del cero absoluto: revisá los datos.");
        label = "Temperatura final (T₂)";
        main = `${f(fromKelvin(t2, v.tu))} ${tu}`;
      }
      const lines = [
        `Estado 1: P₁ = ${f(v.p1)} ${pu} · V₁ = ${f(v.v1)} ${vu} · T₁ = ${f(v.t1)} ${tu} (${f(t1)} K).`,
        `Estado 2: P₂ = ${f(p2)} ${pu} · V₂ = ${f(v2)} ${vu} · T₂ = ${f(fromKelvin(t2, v.tu))} ${tu} (${f(t2)} K).`,
        `Se aplica la <strong>${lawName(v.p1, v.v1, t1, p2, v2, t2)}</strong>.`,
        `Comprobación: P₁·V₁/T₁ = ${f((v.p1 * v.v1) / t1)} y P₂·V₂/T₂ = ${f((p2 * v2) / t2)}.`,
      ];
      return { label, main, lines };
    },
  });
})();
