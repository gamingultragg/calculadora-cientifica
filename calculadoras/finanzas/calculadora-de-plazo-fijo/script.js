/**
 * Calculadora de Plazo Fijo y conversor de tasas (TNA ↔ TEA).
 * Convención argentina: año de 365 días. Interés = capital × TNA × días / 365.
 * TEA = (1 + TNA × d/365)^(365/d) − 1, con capitalización cada d días.
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

  // tna y tea como decimales (0,40 = 40 %)
  function plazoFijo(capital, tna, dias) {
    const interest = (capital * tna * dias) / 365;
    return { interest, final: capital + interest, periodRate: (tna * dias) / 365 };
  }
  function tnaToTea(tna, dias) {
    return Math.pow(1 + (tna * dias) / 365, 365 / dias) - 1;
  }
  function teaToTna(tea, dias) {
    return ((Math.pow(1 + tea, dias / 365) - 1) * 365) / dias;
  }

  if (typeof module !== "undefined") module.exports = { plazoFijo, tnaToTea, teaToTna };
  if (typeof document === "undefined" || !document.getElementById("pf-mode")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("pf-result-panel");
  const fmtMoney = (n) => "$" + new Intl.NumberFormat("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(Math.round((n + 1e-9) * 100) / 100);
  const fmtPct = (n, d = 2) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: d }).format(Math.round((n * 100 + 1e-12) * 10 ** d) / 10 ** d) + " %";

  const FIELDS = {
    plazo: ["capital", "tna", "dias"],
    "tna-tea": ["tna", "dias"],
    "tea-tna": ["tea", "dias"],
  };
  function sync() {
    const mode = $("pf-mode").value;
    document.querySelectorAll("[data-field]").forEach((el) => el.classList.toggle("hidden", !FIELDS[mode].includes(el.dataset.field)));
    $("pf-dias-label").textContent = mode === "plazo" ? "Plazo (días)" : "Capitalización cada (días)";
    errorEl.classList.add("hidden");
    panel.classList.add("hidden");
  }

  function read(id, label, { allowZero = false } = {}) {
    const el = $(id);
    el.classList.remove("field-error");
    const s = normalizeNumberInput(el.value);
    if (s === "") {
      el.classList.add("field-error");
      throw new Error(`Completá el campo "${label}".`);
    }
    const v = Number(s);
    if (!Number.isFinite(v) || v < 0 || (!allowZero && v === 0)) {
      el.classList.add("field-error");
      throw new Error(`"${label}" tiene que ser un número mayor a 0.`);
    }
    return v;
  }

  function calculate() {
    errorEl.classList.add("hidden");
    try {
      const mode = $("pf-mode").value;
      const dias = read("pf-dias", mode === "plazo" ? "Plazo (días)" : "Capitalización cada (días)");
      let label, main, lines;
      if (mode === "plazo") {
        const C = read("pf-capital", "Capital");
        const tna = read("pf-tna", "TNA") / 100;
        const r = plazoFijo(C, tna, dias);
        const tea = tnaToTea(tna, dias);
        label = "Monto al vencimiento";
        main = fmtMoney(r.final);
        lines = [
          `Interés ganado: <strong>${fmtMoney(r.interest)}</strong> (${fmtPct(r.periodRate)} en ${dias} días)`,
          `TEA equivalente (reinvirtiendo cada ${dias} días): <strong>${fmtPct(tea)}</strong>`,
          `Cuenta: ${fmtMoney(C)} × ${fmtPct(tna)} × ${dias} / 365`,
        ];
      } else if (mode === "tna-tea") {
        const tna = read("pf-tna", "TNA") / 100;
        const tea = tnaToTea(tna, dias);
        label = "TEA (tasa efectiva anual)";
        main = fmtPct(tea);
        lines = [`TEA = (1 + ${fmtPct(tna)} × ${dias}/365)^(365/${dias}) − 1`, `Tasa por período de ${dias} días: ${fmtPct((tna * dias) / 365)}`];
      } else {
        const tea = read("pf-tea", "TEA") / 100;
        const tna = teaToTna(tea, dias);
        label = `TNA equivalente (capitalización cada ${dias} días)`;
        main = fmtPct(tna);
        lines = [`TNA = ((1 + ${fmtPct(tea)})^(${dias}/365) − 1) × 365/${dias}`, `Tasa por período de ${dias} días: ${fmtPct((tna * dias) / 365)}`];
      }
      $("pf-label").textContent = label;
      $("pf-main").textContent = main;
      $("pf-lines").innerHTML = lines.map((l) => `<p>${l}</p>`).join("");
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("pf-mode").addEventListener("change", sync);
  $("pf-solve").addEventListener("click", calculate);
  document.querySelectorAll("input").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && calculate()));
  document.querySelectorAll("[data-example]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const [mode, a, b, c] = btn.dataset.example.split("|");
      $("pf-mode").value = mode;
      sync();
      if (mode === "plazo") {
        $("pf-capital").value = a;
        $("pf-tna").value = b;
        $("pf-dias").value = c;
      } else if (mode === "tna-tea") {
        $("pf-tna").value = a;
        $("pf-dias").value = b;
      } else {
        $("pf-tea").value = a;
        $("pf-dias").value = b;
      }
      calculate();
    })
  );
  sync();
})();
