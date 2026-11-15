/**
 * Escaleras — cantidad de escalones, contrahuella (alzada) y huella (pisada) con la fórmula de Blondel: 2·c + h ≈ 63 cm.
 * Una escalera de n escalones tiene n contrahuellas y n − 1 huellas (el piso superior hace de último peldaño).
 */
(function () {
  function stairs(heightCm, targetRiserCm, treadCm) {
    const n = Math.max(2, Math.round(heightCm / targetRiserCm)); // contrahuellas
    const riser = heightCm / n;
    const tread = treadCm !== undefined ? treadCm : 63 - 2 * riser;
    const run = (n - 1) * tread;
    return { n, riser, tread, run, blondel: 2 * riser + tread, angle: (Math.atan2(riser, tread) * 180) / Math.PI, stringer: Math.hypot(heightCm, run) };
  }

  if (typeof module !== "undefined") module.exports = { stairs };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("es-solve")) return;

  CCSimple.mount({
    prefix: "es",
    compute(v, h) {
      const f = (x, d = 1) => h.fmt(x, d);
      const H = v.unit === "m" ? v.height * 100 : v.height;
      if (H < 30 || H > 1000) throw new Error('"Altura a salvar" parece fuera de rango: revisá el valor y la unidad.');
      const target = v.riser;
      if (target < 10 || target > 25) throw new Error('"Contrahuella deseada" tiene que estar entre 10 y 25 cm (lo habitual es 17 a 18).');
      if (v.tread !== undefined && (v.tread < 15 || v.tread > 50)) throw new Error('"Huella" tiene que estar entre 15 y 50 cm (lo habitual es 25 a 30).');
      const r = stairs(H, target, v.tread);
      const okRiser = r.riser >= 15 && r.riser <= 20;
      const okTread = r.tread >= 23;
      const okBlondel = r.blondel >= 60 && r.blondel <= 64;
      const lines = [
        `<strong>${r.n} contrahuellas</strong> (alturas de escalón) y ${r.n - 1} huellas (pisadas).`,
        `Contrahuella: ${f(r.riser, 2)} cm · Huella: ${f(r.tread, 1)} cm.`,
        `Recorrido horizontal: ${f(r.run / 100, 2)} m · Largo de la rampa inclinada: ${f(r.stringer / 100, 2)} m · Inclinación: ${f(r.angle)}°.`,
        `Comodidad (Blondel): 2 × ${f(r.riser, 2)} + ${f(r.tread)} = ${f(r.blondel)} cm. ${okBlondel ? "Está en el rango cómodo (60 a 64 cm)." : "Está fuera del rango cómodo (60 a 64 cm): ajustá la huella o la altura de escalón."}`,
        !okRiser ? "La contrahuella queda fuera de lo habitual (15 a 20 cm)." : null,
        !okTread ? "La huella es muy corta: menos de 23 cm resulta incómodo e inseguro." : null,
        "Verificá la normativa de edificación de tu zona: fija medidas máximas y mínimas.",
      ];
      return { label: "Cantidad de escalones", main: `${r.n} escalones`, lines };
    },
  });
})();
