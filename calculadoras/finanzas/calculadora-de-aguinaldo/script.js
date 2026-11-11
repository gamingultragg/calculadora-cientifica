/**
 * Calculadora de Aguinaldo (SAC) — Argentina.
 * Criterio: 50 % de la mejor remuneración mensual del semestre. Si no se trabajó el semestre
 * completo, se proporciona: meses / 6 (equivale a mejor sueldo / 12 por mes trabajado) o
 * días / 180. Es una estimación de referencia: el convenio colectivo puede fijar otro criterio.
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

  // fraction: proporción del semestre trabajado (0 a 1).
  function sacFraction(unit, amount) {
    if (unit === "completo") return 1;
    const f = unit === "meses" ? amount / 6 : amount / 180;
    return Math.min(f, 1);
  }

  function aguinaldo(bestSalary, fraction, deductionPct) {
    const full = bestSalary / 2;
    const gross = full * fraction;
    const deductions = gross * (deductionPct / 100);
    return { full, gross, deductions, net: gross - deductions };
  }

  if (typeof module !== "undefined") module.exports = { aguinaldo, sacFraction };
  if (typeof document === "undefined" || !document.getElementById("sa-salary")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("sa-result-panel");
  const fmtMoney = (n) => "$" + new Intl.NumberFormat("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(Math.round((n + 1e-9) * 100) / 100);
  const fmt = (n, d = 2) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: d }).format(n);

  function read(id, label, { min = 0, allowZero = false } = {}) {
    const el = $(id);
    el.classList.remove("field-error");
    const s = normalizeNumberInput(el.value);
    if (s === "") {
      el.classList.add("field-error");
      throw new Error(`Completá el campo "${label}".`);
    }
    const v = Number(s);
    if (!Number.isFinite(v) || v < min || (!allowZero && v === 0)) {
      el.classList.add("field-error");
      throw new Error(`"${label}" tiene que ser un número ${allowZero ? "mayor o igual a 0" : "mayor a 0"}.`);
    }
    return v;
  }

  function syncPart() {
    const partial = $("sa-time").value !== "completo";
    $("sa-part-wrap").classList.toggle("hidden", !partial);
    $("sa-part-label").textContent = $("sa-time").value === "meses" ? "Meses trabajados en el semestre (máx. 6)" : "Días trabajados en el semestre (máx. 180)";
    errorEl.classList.add("hidden");
    panel.classList.add("hidden");
  }

  function calculate() {
    errorEl.classList.add("hidden");
    try {
      const best = read("sa-salary", "Mejor remuneración mensual");
      const unit = $("sa-time").value;
      const amount = unit === "completo" ? 0 : read("sa-part", "Tiempo trabajado");
      const ded = read("sa-deductions", "Descuentos", { allowZero: true });
      if (ded >= 100) {
        $("sa-deductions").classList.add("field-error");
        throw new Error('"Descuentos" tiene que ser menor a 100.');
      }
      const frac = sacFraction(unit, amount);
      const r = aguinaldo(best, frac, ded);
      $("sa-main").textContent = fmtMoney(r.gross);
      $("sa-lines").innerHTML = [
        `<p>Neto estimado (con ${fmt(ded)}% de descuentos): <strong>${fmtMoney(r.net)}</strong> · Descuentos: ${fmtMoney(r.deductions)}</p>`,
        `<p>Aguinaldo completo del semestre (50% de ${fmtMoney(best)}): ${fmtMoney(r.full)}</p>`,
        frac < 1 ? `<p>Proporcional: ${fmt(frac * 100)}% del semestre (${unit === "meses" ? `${fmt(amount)} de 6 meses` : `${fmt(amount)} de 180 días`}).</p>` : "",
      ].join("");
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("sa-time").addEventListener("change", syncPart);
  $("sa-solve").addEventListener("click", calculate);
  document.querySelectorAll("input").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && calculate()));
  syncPart();
})();
