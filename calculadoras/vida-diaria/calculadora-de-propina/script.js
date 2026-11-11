/**
 * Calculadora de Propina y División de la Cuenta — propina en %, personas y redondeo hacia arriba.
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

  // roundTo: 0 = sin redondeo; si no, cada persona paga el múltiplo de roundTo inmediato hacia arriba.
  function split(bill, tipPct, people, roundTo = 0) {
    if (!(people >= 1) || !Number.isInteger(people)) throw new Error("La cantidad de personas tiene que ser un entero de 1 o más.");
    const tip = (bill * tipPct) / 100;
    const total = bill + tip;
    let perPerson = total / people;
    if (roundTo > 0) perPerson = Math.ceil(perPerson / roundTo - 1e-9) * roundTo;
    const collected = perPerson * people;
    return { tip, total, perPerson, collected, extra: collected - total };
  }

  if (typeof module !== "undefined") module.exports = { split };
  if (typeof document === "undefined" || !document.getElementById("pr-bill")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("pr-result-panel");
  const money = (n) => "$" + new Intl.NumberFormat("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(Math.round((n + 1e-9) * 100) / 100);

  function num(id, label, { positive = true, def = null } = {}) {
    const el = $(id);
    el.classList.remove("field-error");
    const s = normalizeNumberInput(el.value);
    if (s === "") {
      if (def !== null) return def;
      el.classList.add("field-error");
      throw new Error(`Completá el campo "${label}".`);
    }
    const v = Number(s);
    if (!Number.isFinite(v) || v < 0 || (positive && v === 0)) {
      el.classList.add("field-error");
      throw new Error(`"${label}" tiene que ser un número ${positive ? "mayor a 0" : "mayor o igual a 0"}.`);
    }
    return v;
  }

  function calculate() {
    errorEl.classList.add("hidden");
    try {
      const bill = num("pr-bill", "Total de la cuenta");
      const pct = num("pr-tip", "Propina (%)", { positive: false, def: 0 });
      const people = num("pr-people", "Personas", { def: 1 });
      const roundTo = Number($("pr-round").value);
      let r;
      try {
        r = split(bill, pct, people, roundTo);
      } catch (e) {
        $("pr-people").classList.add("field-error");
        throw e;
      }
      $("pr-main").textContent = money(r.perPerson);
      $("pr-lines").innerHTML = [
        `<p>Propina (${new Intl.NumberFormat("es-AR").format(pct)}%): <strong>${money(r.tip)}</strong> · Total con propina: <strong>${money(r.total)}</strong></p>`,
        `<p>Cuenta ${money(bill)} + propina ${money(r.tip)}, dividido entre ${people} ${people === 1 ? "persona" : "personas"}.</p>`,
        roundTo > 0 && r.extra > 0.005 ? `<p>Con el redondeo se junta ${money(r.collected)}: ${money(r.extra)} más que el total, que suma a la propina.</p>` : "",
      ].filter(Boolean).join("");
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("pr-solve").addEventListener("click", calculate);
  $("pr-round").addEventListener("change", () => $("pr-bill").value && calculate());
  document.querySelectorAll("input").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && calculate()));
  document.querySelectorAll("[data-tip]").forEach((btn) =>
    btn.addEventListener("click", () => {
      $("pr-tip").value = btn.dataset.tip;
      if ($("pr-bill").value) calculate();
    })
  );
})();
