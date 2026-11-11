/**
 * Conversor de Temperatura — Celsius, Fahrenheit, Kelvin y Rankine.
 * Se pasa todo a Kelvin y de ahí a cada escala.
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

  const toKelvin = { c: (t) => t + 273.15, f: (t) => ((t - 32) * 5) / 9 + 273.15, k: (t) => t, r: (t) => (t * 5) / 9 };
  const fromKelvin = { c: (k) => k - 273.15, f: (k) => ((k - 273.15) * 9) / 5 + 32, k: (k) => k, r: (k) => (k * 9) / 5 };

  function convert(value, from) {
    const k = toKelvin[from](value);
    if (k < -1e-9) throw new Error("Esa temperatura está por debajo del cero absoluto (0 K = −273,15 °C = −459,67 °F).");
    return { c: fromKelvin.c(k), f: fromKelvin.f(k), k, r: fromKelvin.r(k) };
  }

  if (typeof module !== "undefined") module.exports = { convert };
  if (typeof document === "undefined" || !document.getElementById("tp-value")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("tp-result-panel");
  const fmt = (n) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: 4 }).format(Math.round((n + 1e-12) * 1e4) / 1e4);
  const NAMES = { c: ["Celsius", "°C"], f: ["Fahrenheit", "°F"], k: ["Kelvin", "K"], r: ["Rankine", "°R"] };

  function calculate() {
    errorEl.classList.add("hidden");
    const el = $("tp-value");
    el.classList.remove("field-error");
    try {
      const s = normalizeNumberInput(el.value);
      if (s === "") {
        el.classList.add("field-error");
        throw new Error("Ingresá una temperatura.");
      }
      const v = Number(s);
      if (!Number.isFinite(v)) {
        el.classList.add("field-error");
        throw new Error("Ingresá un número válido.");
      }
      const from = $("tp-from").value;
      const r = convert(v, from);
      $("tp-rows").innerHTML = Object.keys(NAMES)
        .map((k) => {
          const mark = k === from ? " (origen)" : "";
          return `<div class="flex items-baseline justify-between gap-4 border-b border-[var(--color-border)] py-2 last:border-0"><span class="text-sm text-[var(--color-text-muted)]">${NAMES[k][0]}${mark}</span><span class="font-numeric text-lg font-bold">${fmt(r[k])} ${NAMES[k][1]}</span></div>`;
        })
        .join("");
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("tp-solve").addEventListener("click", calculate);
  $("tp-from").addEventListener("change", () => $("tp-value").value && calculate());
  $("tp-value").addEventListener("input", () => $("tp-value").value && calculate());
  document.querySelectorAll("input").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && calculate()));
  document.querySelectorAll("[data-example]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const [v, from] = btn.dataset.example.split("|");
      $("tp-from").value = from;
      $("tp-value").value = v;
      calculate();
    })
  );
})();
