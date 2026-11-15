/**
 * Errores de medición — error absoluto, relativo y porcentual respecto de un valor de referencia, e incertidumbre de una serie
 * de mediciones (promedio, desvío estándar muestral y error estándar de la media).
 *   E = |medido − real|   ·   e = E / |real|   ·   e % = e × 100   ·   error estándar = s / √n
 */
(function () {
  function normalizeNumber(value) {
    let str = String(value).trim();
    if (str.includes(",")) str = str.replace(/\./g, "").replace(",", ".");
    else if (/^-?[1-9]\d{0,2}(\.\d{3})+$/.test(str)) str = str.replace(/\./g, "");
    return str;
  }
  function parseList(text) {
    const tokens = String(text).replace(/,\s+/g, " ").split(/[\s;]+/).filter(Boolean);
    const out = tokens.map((t) => Number(normalizeNumber(t.replace(/,$/, ""))));
    if (out.length < 2) throw new Error("Ingresá al menos dos mediciones.");
    if (out.length > 1000) throw new Error("Ingresá hasta 1.000 mediciones.");
    if (out.some((n) => !Number.isFinite(n))) throw new Error("Hay un valor que no es un número válido. Separá los números con espacios o punto y coma.");
    return out;
  }

  function singleError(real, measured) {
    if (real === 0) throw new Error("El valor real no puede ser 0 para calcular el error relativo.");
    const absolute = Math.abs(measured - real);
    return { absolute, relative: absolute / Math.abs(real), percent: (absolute / Math.abs(real)) * 100, signed: measured - real };
  }

  function series(list) {
    const n = list.length;
    const mean = list.reduce((s, x) => s + x, 0) / n;
    const s = Math.sqrt(list.reduce((acc, x) => acc + (x - mean) * (x - mean), 0) / (n - 1));
    return { n, mean, s, sem: s / Math.sqrt(n), min: Math.min(...list), max: Math.max(...list) };
  }

  if (typeof module !== "undefined") module.exports = { parseList, singleError, series };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("er-solve")) return;

  CCSimple.mount({
    prefix: "er",
    compute(v, h) {
      const f = (x, d = 6) => h.fmt(x, d);
      if (v.mode === "uno") {
        const e = singleError(v.real, v.meas);
        return {
          label: "Error porcentual",
          main: `${f(e.percent, 4)} %`,
          lines: [
            `Error absoluto: |${f(v.meas)} − ${f(v.real)}| = <strong>${f(e.absolute)}</strong>.`,
            `Error relativo: ${f(e.absolute)} / ${f(Math.abs(v.real))} = <strong>${f(e.relative)}</strong>.`,
            `Error porcentual: <strong>${f(e.percent, 4)} %</strong>.`,
            e.signed > 0 ? "La medición quedó por encima del valor real (error por exceso)." : e.signed < 0 ? "La medición quedó por debajo del valor real (error por defecto)." : "La medición coincide con el valor real.",
          ],
        };
      }
      const list = parseList(v.list);
      const s = series(list);
      const rel = s.mean !== 0 ? (s.sem / Math.abs(s.mean)) * 100 : null;
      return {
        label: "Resultado de la medición",
        main: `${f(s.mean)} ± ${f(s.sem)}`,
        lines: [
          `Cantidad de mediciones: ${s.n} · mínimo ${f(s.min)} · máximo ${f(s.max)}.`,
          `Promedio: <strong>${f(s.mean)}</strong>.`,
          `Desvío estándar muestral: ${f(s.s)} (qué tanto se dispersan las mediciones).`,
          `Error estándar de la media: s / √n = <strong>${f(s.sem)}</strong>.`,
          rel !== null ? `Error relativo del promedio: ${f(rel, 4)} %.` : null,
          `Se informa como: ${f(s.mean)} ± ${f(s.sem)}.`,
        ],
      };
    },
  });
})();
