/**
 * Calculadora de Gases Ideales — PV = nRT.
 * Todo se convierte a atm, L, mol y K (R = 0,082057 L·atm/(mol·K)) y el resultado se
 * expresa en la unidad elegida para ese campo.
 */
(function () {
  const R = 0.082057366; // L·atm / (mol·K)

  function normalizeNumberInput(value) {
    let str = String(value).trim();
    if (str.includes(",")) {
      str = str.replace(/\./g, "").replace(",", ".");
    } else if (/^-?[1-9]\d{0,2}(\.\d{3})+$/.test(str)) {
      str = str.replace(/\./g, "");
    }
    return str;
  }

  // factor a atm, litros
  const P_TO_ATM = { atm: 1, kpa: 1 / 101.325, mmhg: 1 / 760, bar: 1 / 1.01325 };
  const V_TO_L = { l: 1, ml: 0.001, m3: 1000 };
  const toKelvin = (t, unit) => (unit === "c" ? t + 273.15 : t);
  const fromKelvin = (k, unit) => (unit === "c" ? k - 273.15 : k);

  // atm, L, mol, K
  const pressure = (n, V, T) => (n * R * T) / V;
  const volume = (n, P, T) => (n * R * T) / P;
  const moles = (P, V, T) => (P * V) / (R * T);
  const temperature = (P, V, n) => (P * V) / (n * R);

  if (typeof module !== "undefined") module.exports = { R, P_TO_ATM, V_TO_L, toKelvin, fromKelvin, pressure, volume, moles, temperature };
  if (typeof document === "undefined" || !document.getElementById("gi-target")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("gi-result-panel");
  const fmt = (n, d = 4) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: d, useGrouping: true }).format(Number(n.toPrecision(6)));
  const UNIT_LABEL = { atm: "atm", kpa: "kPa", mmhg: "mmHg", bar: "bar", l: "L", ml: "mL", m3: "m³", k: "K", c: "°C" };

  // Cada magnitud (P, V, n, T) es una fila. La que se calcula pierde su campo numérico
  // pero conserva el selector de unidad (es la unidad en que se muestra el resultado).
  function sync() {
    const t = $("gi-target").value;
    document.querySelectorAll("[data-row]").forEach((row) => {
      const isTarget = row.dataset.row === t;
      row.classList.toggle("hidden", isTarget && t === "n");
      const input = row.querySelector("[data-input]");
      if (input) input.classList.toggle("hidden", isTarget);
      const label = row.querySelector("label");
      label.textContent = isTarget ? label.dataset.result : label.dataset.base;
    });
    errorEl.classList.add("hidden");
    panel.classList.add("hidden");
  }

  function read(id, label, { allowNegative = false } = {}) {
    const el = $(id);
    el.classList.remove("field-error");
    const s = normalizeNumberInput(el.value);
    if (s === "") {
      el.classList.add("field-error");
      throw new Error(`Completá el campo "${label}".`);
    }
    const v = Number(s);
    if (!Number.isFinite(v) || (!allowNegative && v <= 0)) {
      el.classList.add("field-error");
      throw new Error(`"${label}" tiene que ser un número mayor a 0.`);
    }
    return v;
  }

  function calculate() {
    errorEl.classList.add("hidden");
    try {
      const t = $("gi-target").value;
      const pu = $("gi-p-unit").value, vu = $("gi-v-unit").value, tu = $("gi-t-unit").value;
      const get = {
        P: () => read("gi-p", "Presión") * P_TO_ATM[pu],
        V: () => read("gi-v", "Volumen") * V_TO_L[vu],
        n: () => read("gi-n", "Moles"),
        T: () => {
          const k = toKelvin(read("gi-t", "Temperatura", { allowNegative: true }), tu);
          if (k <= 0) {
            $("gi-t").classList.add("field-error");
            throw new Error("La temperatura tiene que ser mayor al cero absoluto (0 K = −273,15 °C).");
          }
          return k;
        },
      };

      let label, value, unit, extra = "";
      if (t === "P") {
        const atm = pressure(get.n(), get.V(), get.T());
        label = "Presión";
        value = atm / P_TO_ATM[pu];
        unit = UNIT_LABEL[pu];
        extra = `Equivale a ${fmt(atm)} atm · ${fmt(atm * 101.325)} kPa · ${fmt(atm * 760)} mmHg · ${fmt(atm * 1.01325)} bar.`;
      } else if (t === "V") {
        const L = volume(get.n(), get.P(), get.T());
        label = "Volumen";
        value = L / V_TO_L[vu];
        unit = UNIT_LABEL[vu];
        extra = `Equivale a ${fmt(L)} L · ${fmt(L * 1000)} mL · ${fmt(L / 1000, 6)} m³.`;
      } else if (t === "n") {
        const mol = moles(get.P(), get.V(), get.T());
        label = "Cantidad de sustancia";
        value = mol;
        unit = "mol";
        extra = `Con ${fmt(mol * 6.02214076e23, 3)} partículas (número de Avogadro).`;
      } else {
        const K = temperature(get.P(), get.V(), get.n());
        label = "Temperatura";
        value = fromKelvin(K, tu);
        unit = UNIT_LABEL[tu];
        extra = `Equivale a ${fmt(K)} K · ${fmt(K - 273.15)} °C.`;
      }
      $("gi-label").textContent = label;
      $("gi-main").textContent = `${fmt(value)} ${unit}`;
      $("gi-lines").innerHTML = `<p>${extra}</p><p>PV = nRT con R = 0,082057 L·atm/(mol·K).</p>`;
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("gi-target").addEventListener("change", sync);
  $("gi-solve").addEventListener("click", calculate);
  document.querySelectorAll("input").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && calculate()));
  document.querySelectorAll("[data-example]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const [t, p, v, n, temp] = btn.dataset.example.split("|");
      $("gi-target").value = t;
      $("gi-p-unit").value = "atm";
      $("gi-v-unit").value = "l";
      $("gi-t-unit").value = "c";
      $("gi-p").value = p;
      $("gi-v").value = v;
      $("gi-n").value = n;
      $("gi-t").value = temp;
      sync();
      calculate();
    })
  );
  sync();
})();
