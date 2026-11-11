/**
 * Calculadora de Edad y Fechas — diferencia entre dos fechas, edad exacta y sumar/restar tiempo.
 * Todo el cálculo se hace en UTC con fechas de calendario (sin horas), así que no hay saltos por
 * cambios de horario. Las fechas llegan como "AAAA-MM-DD" (input type="date").
 */
(function () {
  const DAY_MS = 86400000;
  const WEEKDAYS = ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"];
  const MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];

  const daysInMonth = (y, m) => new Date(Date.UTC(y, m, 0)).getUTCDate(); // m: 1-12
  const utc = (d) => Date.UTC(d.y, d.m - 1, d.d);

  function parseISO(s) {
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(s).trim());
    if (!m) throw new Error("Elegí una fecha válida.");
    const d = { y: Number(m[1]), m: Number(m[2]), d: Number(m[3]) };
    if (d.m < 1 || d.m > 12 || d.d < 1 || d.d > daysInMonth(d.y, d.m)) throw new Error("La fecha no existe en el calendario.");
    return d;
  }
  const fromUTC = (ms) => {
    const t = new Date(ms);
    return { y: t.getUTCFullYear(), m: t.getUTCMonth() + 1, d: t.getUTCDate() };
  };
  const weekdayName = (d) => WEEKDAYS[new Date(utc(d)).getUTCDay()];
  const fmtDate = (d) => `${String(d.d).padStart(2, "0")}/${String(d.m).padStart(2, "0")}/${d.y}`;
  const longDate = (d) => `${weekdayName(d)} ${d.d} de ${MONTHS[d.m - 1]} de ${d.y}`;

  // Suma meses a una fecha recortando al fin de mes (31/1 + 1 mes = 28/2 o 29/2).
  function addMonths(date, n) {
    const idx = date.y * 12 + (date.m - 1) + n;
    const y = Math.floor(idx / 12), m = (idx % 12) + 1;
    return { y, m, d: Math.min(date.d, daysInMonth(y, m)) };
  }

  // Diferencia de calendario entre a y b (a <= b): años, meses y días completos. Se suman meses enteros
  // a "a" (con recorte a fin de mes) mientras no se pase de "b"; lo que sobra son días.
  function calendarDiff(a, b) {
    let months = (b.y - a.y) * 12 + (b.m - a.m);
    let anchor = addMonths(a, months);
    if (utc(anchor) > utc(b)) {
      months--;
      anchor = addMonths(a, months);
    }
    const days = Math.round((utc(b) - utc(anchor)) / DAY_MS);
    return { years: Math.floor(months / 12), months: months % 12, days };
  }

  // Días de lunes a viernes desde a (inclusive) hasta b (exclusive).
  function countWeekdays(a, b) {
    let count = 0;
    const total = Math.round((utc(b) - utc(a)) / DAY_MS);
    for (let i = 0; i < total; i++) {
      const wd = new Date(utc(a) + i * DAY_MS).getUTCDay();
      if (wd !== 0 && wd !== 6) count++;
    }
    return count;
  }

  function dateDiff(a, b) {
    let swapped = false;
    if (utc(a) > utc(b)) {
      [a, b] = [b, a];
      swapped = true;
    }
    const totalDays = Math.round((utc(b) - utc(a)) / DAY_MS);
    return { ...calendarDiff(a, b), totalDays, weeks: Math.floor(totalDays / 7), restDays: totalDays % 7, weekdays: countWeekdays(a, b), swapped, from: a, to: b };
  }

  // Edad exacta y próximo cumpleaños (el 29/2 se festeja el 28/2 en los años no bisiestos).
  function ageInfo(birth, ref) {
    if (utc(birth) > utc(ref)) throw new Error("La fecha de nacimiento no puede ser posterior a la fecha de referencia.");
    const diff = calendarDiff(birth, ref);
    const totalDays = Math.round((utc(ref) - utc(birth)) / DAY_MS);
    const birthdayIn = (year) => ({ y: year, m: birth.m, d: Math.min(birth.d, daysInMonth(year, birth.m)) });
    let next = birthdayIn(ref.y);
    if (utc(next) < utc(ref)) next = birthdayIn(ref.y + 1);
    const daysToBirthday = Math.round((utc(next) - utc(ref)) / DAY_MS);
    return { ...diff, totalDays, months_total: diff.years * 12 + diff.months, nextBirthday: next, daysToBirthday, turning: next.y - birth.y };
  }

  // Suma n unidades ("dias", "semanas", "meses", "anios"); n puede ser negativo. Los meses se recortan al fin de mes.
  function addToDate(date, n, unit) {
    if (unit === "dias") return fromUTC(utc(date) + n * DAY_MS);
    if (unit === "semanas") return fromUTC(utc(date) + n * 7 * DAY_MS);
    return addMonths(date, unit === "anios" ? n * 12 : n);
  }

  if (typeof module !== "undefined") module.exports = { parseISO, daysInMonth, calendarDiff, countWeekdays, dateDiff, ageInfo, addToDate, weekdayName, fmtDate, longDate };
  if (typeof document === "undefined" || !document.getElementById("fd-mode")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("fd-result-panel");
  const nf = (n) => new Intl.NumberFormat("es-AR").format(n);
  const plural = (n, s, p) => `${nf(n)} ${n === 1 ? s : p}`;
  const ymd = (r) => `${plural(r.years, "año", "años")}, ${plural(r.months, "mes", "meses")} y ${plural(r.days, "día", "días")}`;

  const today = () => {
    const t = new Date();
    return { y: t.getFullYear(), m: t.getMonth() + 1, d: t.getDate() };
  };
  const iso = (d) => `${d.y}-${String(d.m).padStart(2, "0")}-${String(d.d).padStart(2, "0")}`;

  function sync() {
    const mode = $("fd-mode").value;
    document.querySelectorAll("[data-mode]").forEach((el) => el.classList.toggle("hidden", !el.dataset.mode.split(" ").includes(mode)));
    errorEl.classList.add("hidden");
    panel.classList.add("hidden");
  }

  function readDate(id, label) {
    const el = $(id);
    el.classList.remove("field-error");
    try {
      return parseISO(el.value);
    } catch (e) {
      el.classList.add("field-error");
      throw new Error(`${label}: ${e.message.toLowerCase().replace(/\.$/, "")}.`);
    }
  }

  function show(label, main, lines) {
    $("fd-label").textContent = label;
    $("fd-main").textContent = main;
    $("fd-lines").innerHTML = lines.map((l) => `<p>${l}</p>`).join("");
    panel.classList.remove("hidden");
  }

  function calculate() {
    errorEl.classList.add("hidden");
    try {
      const mode = $("fd-mode").value;
      if (mode === "diff") {
        const a = readDate("fd-a", "Fecha de inicio"), b = readDate("fd-b", "Fecha de fin");
        const r = dateDiff(a, b);
        show("Tiempo entre las dos fechas", ymd(r), [
          `Total: <strong>${plural(r.totalDays, "día", "días")}</strong> (${plural(r.weeks, "semana", "semanas")} y ${plural(r.restDays, "día", "días")})`,
          `Días hábiles (lunes a viernes, sin feriados): <strong>${nf(r.weekdays)}</strong>`,
          `Del ${longDate(r.from)} al ${longDate(r.to)}.`,
          r.swapped ? "Las fechas estaban invertidas: se ordenaron de la más antigua a la más reciente." : "",
        ].filter(Boolean));
      } else if (mode === "edad") {
        const birth = readDate("fd-birth", "Fecha de nacimiento");
        const ref = $("fd-ref").value ? readDate("fd-ref", "Fecha de referencia") : today();
        const r = ageInfo(birth, ref);
        show("Edad", plural(r.years, "año", "años"), [
          `Exacta: <strong>${ymd(r)}</strong>`,
          `Días vividos: <strong>${nf(r.totalDays)}</strong> · Meses cumplidos: ${nf(r.months_total)}`,
          r.daysToBirthday === 0
            ? `¡Hoy es su cumpleaños número ${r.turning}!`
            : `Próximo cumpleaños (${r.turning} años): ${longDate(r.nextBirthday)}, en <strong>${plural(r.daysToBirthday, "día", "días")}</strong>.`,
          `Referencia: ${fmtDate(ref)}.`,
        ]);
      } else {
        const base = readDate("fd-base", "Fecha de partida");
        const amountEl = $("fd-amount");
        amountEl.classList.remove("field-error");
        const n = Number(String(amountEl.value).replace(",", "."));
        if (!Number.isInteger(n) || n < 0 || n > 100000) {
          amountEl.classList.add("field-error");
          throw new Error("La cantidad tiene que ser un número entero entre 0 y 100.000.");
        }
        const sign = $("fd-op").value === "restar" ? -1 : 1;
        const unit = $("fd-unit").value;
        const res = addToDate(base, sign * n, unit);
        const unitLabel = { dias: "días", semanas: "semanas", meses: "meses", anios: "años" }[unit];
        show("Fecha resultante", fmtDate(res), [
          `<strong>${longDate(res)}</strong>`,
          `${fmtDate(base)} ${sign > 0 ? "+" : "−"} ${nf(n)} ${unitLabel}.`,
        ]);
      }
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  // valores iniciales útiles (hoy), sin pisar lo que venga de un enlace
  ["fd-a", "fd-b", "fd-base"].forEach((id) => {
    if (!$(id).value) $(id).value = iso(today());
  });

  $("fd-mode").addEventListener("change", sync);
  $("fd-solve").addEventListener("click", calculate);
  document.querySelectorAll("input").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && calculate()));
  sync();
})();
