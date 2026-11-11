/**
 * Calculadora de Energía Cinética y Potencial gravitatoria.
 *   Ec = ½ · m · v²        Ep = m · g · h        (SI: kg, m/s, m, J)
 * Se puede despejar la energía, la masa o la velocidad (cinética) / la altura (potencial).
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

  const kinetic = (m, v) => 0.5 * m * v * v;
  const massFromKinetic = (E, v) => {
    if (!(v > 0)) throw new Error("La velocidad tiene que ser mayor a 0 para despejar la masa.");
    return (2 * E) / (v * v);
  };
  const speedFromKinetic = (E, m) => {
    if (!(m > 0)) throw new Error("La masa tiene que ser mayor a 0.");
    return Math.sqrt((2 * E) / m);
  };
  const potential = (m, g, h) => m * g * h;
  const massFromPotential = (E, g, h) => {
    if (!(g > 0 && h > 0)) throw new Error("La gravedad y la altura tienen que ser mayores a 0 para despejar la masa.");
    return E / (g * h);
  };
  const heightFromPotential = (E, m, g) => {
    if (!(m > 0 && g > 0)) throw new Error("La masa y la gravedad tienen que ser mayores a 0 para despejar la altura.");
    return E / (m * g);
  };

  if (typeof module !== "undefined")
    module.exports = { kinetic, massFromKinetic, speedFromKinetic, potential, massFromPotential, heightFromPotential };
  if (typeof document === "undefined" || !document.getElementById("en-type")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("en-result-panel");
  const fmt = (n, d = 4) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: d }).format(Number(n.toPrecision(7)));

  // data-field: m (masa), v (velocidad), g (gravedad), h (altura), E (energía)
  const FIELDS = {
    "cinetica|energia": ["m", "v"], "cinetica|masa": ["E", "v"], "cinetica|variable": ["E", "m"],
    "potencial|energia": ["m", "g", "h"], "potencial|masa": ["E", "g", "h"], "potencial|variable": ["E", "m", "g"],
  };
  function sync() {
    const type = $("en-type").value, target = $("en-target").value;
    $("en-target-var").textContent = type === "cinetica" ? "Velocidad" : "Altura";
    const show = FIELDS[`${type}|${target}`];
    document.querySelectorAll("[data-field]").forEach((el) => el.classList.toggle("hidden", !show.includes(el.dataset.field)));
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
  const speedInMs = () => read("en-v", "Velocidad", { allowZero: true }) / ($("en-v-unit").value === "kmh" ? 3.6 : 1);

  function energyLines(E) {
    return `<p>Equivale a ${fmt(E / 1000)} kJ · ${fmt(E / 4184)} kcal · ${fmt(E / 3.6e6, 6)} kWh.</p>`;
  }

  function calculate() {
    errorEl.classList.add("hidden");
    try {
      const type = $("en-type").value, target = $("en-target").value;
      let label, main, lines;
      if (type === "cinetica") {
        if (target === "energia") {
          const m = read("en-m", "Masa"), v = speedInMs();
          const E = kinetic(m, v);
          label = "Energía cinética";
          main = `${fmt(E)} J`;
          lines = [`<p>Ec = ½ · m · v² = ½ × ${fmt(m)} kg × (${fmt(v)} m/s)²</p>`, energyLines(E)];
        } else if (target === "masa") {
          const E = read("en-E", "Energía"), v = speedInMs();
          const m = massFromKinetic(E, v);
          label = "Masa";
          main = `${fmt(m)} kg`;
          lines = [`<p>m = 2·Ec / v² = 2 × ${fmt(E)} J / (${fmt(v)} m/s)²</p>`];
        } else {
          const E = read("en-E", "Energía"), m = read("en-m", "Masa");
          const v = speedFromKinetic(E, m);
          label = "Velocidad";
          main = `${fmt(v)} m/s`;
          lines = [`<p>v = √(2·Ec / m) = √(2 × ${fmt(E)} J / ${fmt(m)} kg)</p>`, `<p>Equivale a ${fmt(v * 3.6)} km/h.</p>`];
        }
      } else if (target === "energia") {
        const m = read("en-m", "Masa"), g = read("en-g", "Gravedad"), h = read("en-h", "Altura", { allowZero: true });
        const E = potential(m, g, h);
        label = "Energía potencial gravitatoria";
        main = `${fmt(E)} J`;
        lines = [`<p>Ep = m · g · h = ${fmt(m)} kg × ${fmt(g)} m/s² × ${fmt(h)} m</p>`, energyLines(E)];
      } else if (target === "masa") {
        const E = read("en-E", "Energía"), g = read("en-g", "Gravedad"), h = read("en-h", "Altura");
        const m = massFromPotential(E, g, h);
        label = "Masa";
        main = `${fmt(m)} kg`;
        lines = [`<p>m = Ep / (g · h) = ${fmt(E)} J / (${fmt(g)} × ${fmt(h)})</p>`];
      } else {
        const E = read("en-E", "Energía"), m = read("en-m", "Masa"), g = read("en-g", "Gravedad");
        const h = heightFromPotential(E, m, g);
        label = "Altura";
        main = `${fmt(h)} m`;
        lines = [`<p>h = Ep / (m · g) = ${fmt(E)} J / (${fmt(m)} kg × ${fmt(g)} m/s²)</p>`];
      }
      $("en-label").textContent = label;
      $("en-main").textContent = main;
      $("en-lines").innerHTML = lines.join("");
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("en-type").addEventListener("change", sync);
  $("en-target").addEventListener("change", sync);
  $("en-solve").addEventListener("click", calculate);
  document.querySelectorAll("input").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && calculate()));
  document.querySelectorAll("[data-example]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const [type, target, ...vals] = btn.dataset.example.split("|");
      $("en-type").value = type;
      $("en-target").value = target;
      sync();
      const ids = FIELDS[`${type}|${target}`].map((k) => "en-" + k);
      ids.forEach((id, i) => ($(id).value = vals[i] || ""));
      calculate();
    })
  );
  sync();
})();
