/**
 * Pendiente de una rampa — pendiente en %, ángulo y largo de la rampa a partir del desnivel y la longitud horizontal, o el largo necesario
 * para salvar una altura con una pendiente dada.   pendiente % = desnivel / longitud horizontal × 100
 */
(function () {
  function slope(rise, run) {
    return { pct: (rise / run) * 100, deg: (Math.atan2(rise, run) * 180) / Math.PI, length: Math.hypot(rise, run) };
  }
  const runFor = (rise, pct) => rise / (pct / 100);
  const riseFor = (run, pct) => run * (pct / 100);
  function describe(pct) {
    if (pct <= 5) return "suave: cómoda para casi todo el mundo";
    if (pct <= 8) return "moderada: es el valor máximo habitual en rampas accesibles de tramos largos";
    if (pct <= 12) return "pronunciada: normalmente solo se admite en tramos cortos";
    return "muy pronunciada: no apta para sillas de ruedas, carritos ni personas con movilidad reducida";
  }

  if (typeof module !== "undefined") module.exports = { slope, runFor, riseFor, describe };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("rp-solve")) return;

  CCSimple.mount({
    prefix: "rp",
    compute(v, h) {
      const f = (x, d = 2) => h.fmt(x, d);
      const u = v.unit; // "m" o "cm"
      const k = u === "cm" ? 0.01 : 1; // a metros
      let rise;
      let run;
      let label;
      let main;
      if (v.mode === "pend") {
        rise = v.rise * k;
        run = v.run * k;
        label = "Pendiente de la rampa";
        main = `${f(slope(rise, run).pct)} %`;
      } else if (v.mode === "largo") {
        rise = v.rise * k;
        run = runFor(rise, v.pct);
        label = "Longitud horizontal necesaria";
        main = `${f(run)} m`;
      } else {
        run = v.run * k;
        rise = riseFor(run, v.pct);
        label = "Desnivel que se salva";
        main = `${f(rise)} m`;
      }
      const s = slope(rise, run);
      const lines = [
        `Desnivel: ${f(rise)} m · Longitud horizontal: ${f(run)} m · Largo de la rampa (inclinado): ${f(s.length)} m.`,
        `Pendiente: <strong>${f(s.pct)} %</strong> = ${f(s.deg)}° de inclinación.`,
        `Es una pendiente ${describe(s.pct)}.`,
        "Las normas de accesibilidad suelen fijar máximos de entre el 6 % y el 12 % según el largo del tramo, y exigen descansos y pasamanos: verificá la normativa de tu zona.",
      ];
      return { label, main, lines };
    },
  });
})();
