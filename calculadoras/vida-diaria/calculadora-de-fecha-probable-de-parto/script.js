/**
 * Fecha probable de parto — regla de Naegele: fecha de última menstruación (FUM) + 280 días (40 semanas), ajustada por la duración del ciclo.
 * Desde la fecha de concepción: + 266 días. Es una estimación: solo una pequeña parte de los bebés nace en la fecha calculada.
 * Las fechas se manejan como "AAAA-MM-DD" y en UTC, para evitar corrimientos por horario de verano.
 */
(function () {
  const MS = 86400000;

  function parseISO(s) {
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(s).trim());
    if (!m) throw new Error("Ingresá una fecha válida.");
    const [y, mo, d] = [Number(m[1]), Number(m[2]), Number(m[3])];
    const t = Date.UTC(y, mo - 1, d);
    const dt = new Date(t);
    if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) throw new Error("La fecha ingresada no existe.");
    return t;
  }
  const toISO = (t) => new Date(t).toISOString().slice(0, 10);
  const addDays = (t, n) => t + n * MS;

  const dueDateFromLMP = (lmpISO, cycleDays = 28) => toISO(addDays(parseISO(lmpISO), 280 + (cycleDays - 28)));
  const dueDateFromConception = (conceptionISO) => toISO(addDays(parseISO(conceptionISO), 266));
  const lmpFromConception = (conceptionISO) => toISO(addDays(parseISO(conceptionISO), -14));
  function gestationalAge(lmpISO, refISO) {
    const days = Math.round((parseISO(refISO) - parseISO(lmpISO)) / MS);
    return { days, weeks: Math.floor(days / 7), rem: ((days % 7) + 7) % 7 };
  }
  const trimester = (weeks) => (weeks < 14 ? 1 : weeks < 28 ? 2 : 3);

  if (typeof module !== "undefined") module.exports = { parseISO, toISO, addDays, dueDateFromLMP, dueDateFromConception, lmpFromConception, gestationalAge, trimester };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("fp-solve")) return;

  const fmtDate = (iso) => new Date(parseISO(iso)).toLocaleDateString("es-AR", { weekday: "long", day: "numeric", month: "long", year: "numeric", timeZone: "UTC" });

  CCSimple.mount({
    prefix: "fp",
    compute(v) {
      const now = new Date();
      const todayISO = toISO(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()));
      const ref = v.ref ? v.ref : todayISO;
      const cycle = v.cycle || 28;
      if (cycle < 21 || cycle > 40) throw new Error('"Duración del ciclo" tiene que estar entre 21 y 40 días.');
      let lmp;
      let due;
      if (v.mode === "conc") {
        lmp = lmpFromConception(v.date);
        due = dueDateFromConception(v.date);
      } else {
        lmp = v.date;
        due = dueDateFromLMP(v.date, cycle);
      }
      const age = gestationalAge(lmp, ref);
      if (age.days < 0) throw new Error("La fecha ingresada es posterior a la fecha de referencia (hoy): revisá los datos.");
      if (age.weeks > 44) throw new Error("Esa fecha es de hace más de 44 semanas: revisá que esté bien cargada.");
      const mark = (w) => fmtDate(toISO(addDays(parseISO(lmp), w * 7)));
      const left = Math.round((parseISO(due) - parseISO(ref)) / MS);
      const lines = [
        `Fecha probable de parto: <strong>${fmtDate(due)}</strong>.`,
        `Edad gestacional al ${fmtDate(ref)}: <strong>${age.weeks} semanas y ${age.rem} día${age.rem === 1 ? "" : "s"}</strong> (${trimester(age.weeks)}.º trimestre).`,
        left >= 0 ? `Faltan ${left} día${left === 1 ? "" : "s"} (unas ${Math.floor(left / 7)} semanas) para la fecha probable.` : `La fecha probable pasó hace ${-left} día${left === -1 ? "" : "s"}.`,
        `Fechas de referencia: semana 12: ${mark(12)} · semana 20: ${mark(20)} · semana 37 (embarazo a término): ${mark(37)}.`,
        "Es una estimación: pocos bebés nacen exactamente en la fecha probable y lo normal es hacerlo entre las semanas 37 y 42. La ecografía y tu obstetra ajustan la fecha.",
      ];
      return { label: "Fecha probable de parto", main: fmtDate(due), lines };
    },
  });
})();
