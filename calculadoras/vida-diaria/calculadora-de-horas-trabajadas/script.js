/**
 * Calculadora de Horas Trabajadas — entre una hora de entrada y una de salida (aunque cruce la
 * medianoche), con descanso, varios días, horas extra y valor de la hora.
 */
(function () {
  function normalizeNumberInput(value) {
    let str = String(value).trim();
    if (str.includes(",")) {
      str = str.replace(/\./g, "").replace(",", ".");
    } else if (/^-?[1-9]\d{0,2}(\.\d{3})+$/.test(str)) {
      str = str.replace(/\./g, "");
    }
    return str;
  }

  function parseTime(s) {
    const m = /^(\d{1,2}):(\d{2})$/.exec(String(s).trim());
    if (!m) throw new Error("Ingresá la hora con el formato HH:MM.");
    const h = Number(m[1]), min = Number(m[2]);
    if (h > 23 || min > 59) throw new Error("La hora tiene que estar entre 00:00 y 23:59.");
    return h * 60 + min;
  }

  // Minutos trabajados en un día: si la salida es menor o igual a la entrada, se asume que cruza la medianoche.
  function workedMinutes(startMin, endMin, breakMin) {
    let total = endMin - startMin;
    if (total <= 0) total += 24 * 60;
    total -= breakMin;
    if (total < 0) throw new Error("El descanso es mayor que el tiempo entre la entrada y la salida.");
    return total;
  }

  const hhmm = (minutes) => `${Math.floor(minutes / 60)}:${String(Math.round(minutes % 60)).padStart(2, "0")}`;

  // normalHours: jornada normal diaria; rate: valor de la hora ($); surchargePct: recargo de las extras (%).
  function summarize({ perDayMin, days, normalHours = 8, rate = 0, surchargePct = 50 }) {
    const normalMin = normalHours * 60;
    const regularPerDay = Math.min(perDayMin, normalMin);
    const extraPerDay = Math.max(0, perDayMin - normalMin);
    const totalMin = perDayMin * days;
    const regularMin = regularPerDay * days;
    const extraMin = extraPerDay * days;
    const pay = (regularMin / 60) * rate + (extraMin / 60) * rate * (1 + surchargePct / 100);
    return { totalMin, regularMin, extraMin, totalDecimal: totalMin / 60, pay };
  }

  if (typeof module !== "undefined") module.exports = { parseTime, workedMinutes, hhmm, summarize };
  if (typeof document === "undefined" || !document.getElementById("ho-start")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("ho-result-panel");
  const fmt = (n, d = 2) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: d }).format(Math.round(n * 10 ** d) / 10 ** d);
  const money = (n) => "$" + new Intl.NumberFormat("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(Math.round(n * 100) / 100);

  function num(id, label, { min = 0, allowEmpty = false, def = 0 } = {}) {
    const el = $(id);
    el.classList.remove("field-error");
    const s = normalizeNumberInput(el.value);
    if (s === "") {
      if (allowEmpty) return def;
      el.classList.add("field-error");
      throw new Error(`Completá el campo "${label}".`);
    }
    const v = Number(s);
    if (!Number.isFinite(v) || v < min) {
      el.classList.add("field-error");
      throw new Error(`"${label}" tiene que ser un número mayor o igual a ${min}.`);
    }
    return v;
  }

  function calculate() {
    errorEl.classList.add("hidden");
    ["ho-start", "ho-end"].forEach((id) => $(id).classList.remove("field-error"));
    try {
      let start, end;
      try { start = parseTime($("ho-start").value); } catch (e) { $("ho-start").classList.add("field-error"); throw new Error("Hora de entrada: " + e.message.toLowerCase()); }
      try { end = parseTime($("ho-end").value); } catch (e) { $("ho-end").classList.add("field-error"); throw new Error("Hora de salida: " + e.message.toLowerCase()); }
      const brk = num("ho-break", "Descanso (minutos)", { allowEmpty: true });
      const days = num("ho-days", "Días trabajados", { min: 1, allowEmpty: true, def: 1 });
      const normal = num("ho-normal", "Jornada normal (horas)", { min: 1, allowEmpty: true, def: 8 });
      const rate = num("ho-rate", "Valor de la hora", { allowEmpty: true });
      const sur = num("ho-surcharge", "Recargo de las horas extra (%)", { allowEmpty: true, def: 50 });
      const perDay = workedMinutes(start, end, brk);
      const r = summarize({ perDayMin: perDay, days, normalHours: normal, rate, surchargePct: sur });
      const overnight = end <= start;
      $("ho-main").textContent = `${hhmm(r.totalMin)} h`;
      const lines = [
        `<p>En decimal: <strong>${fmt(r.totalDecimal)} horas</strong>${days > 1 ? ` (${hhmm(perDay)} h por día × ${fmt(days)} días)` : ""}.</p>`,
        overnight ? "<p>La salida es menor que la entrada: se calculó como un turno que cruza la medianoche.</p>" : "",
        r.extraMin > 0 ? `<p>Horas normales: ${hhmm(r.regularMin)} h · Horas extra: <strong>${hhmm(r.extraMin)} h</strong> (más de ${fmt(normal)} h por día).</p>` : `<p>No hay horas extra (jornada normal de ${fmt(normal)} h).</p>`,
        rate > 0 ? `<p>Importe estimado: <strong>${money(r.pay)}</strong> (extras con ${fmt(sur)}% de recargo).</p>` : "",
      ].filter(Boolean);
      $("ho-lines").innerHTML = lines.join("");
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("ho-solve").addEventListener("click", calculate);
  document.querySelectorAll("input").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && calculate()));
})();
