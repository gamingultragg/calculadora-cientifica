/**
 * Conversor de Cocina — tazas, cucharadas, cucharaditas, ml y gramos de ingredientes comunes.
 * Los gramos por volumen son valores aproximados (varían con la marca, la humedad y cómo se llena la medida).
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

  // Densidad aproximada en g/ml.
  const INGREDIENTS = {
    agua: { name: "Agua", density: 1.0 },
    leche: { name: "Leche", density: 1.03 },
    harina: { name: "Harina de trigo", density: 0.53 },
    azucar: { name: "Azúcar común", density: 0.84 },
    impalpable: { name: "Azúcar impalpable", density: 0.5 },
    manteca: { name: "Manteca", density: 0.95 },
    aceite: { name: "Aceite", density: 0.92 },
    miel: { name: "Miel", density: 1.42 },
    arroz: { name: "Arroz crudo", density: 0.77 },
    avena: { name: "Avena arrollada", density: 0.37 },
    cacao: { name: "Cacao en polvo", density: 0.42 },
    maicena: { name: "Maicena", density: 0.54 },
    sal: { name: "Sal fina", density: 1.2 },
    ddl: { name: "Dulce de leche", density: 1.3 },
    panrallado: { name: "Pan rallado", density: 0.48 },
  };

  // Unidades de volumen en ml; "taza" depende del tamaño elegido.
  const VOLUME_UNITS = { ml: 1, l: 1000, cdta: 5, cda: 15, taza: null };
  const MASS_UNITS = { g: 1, kg: 1000, oz: 28.3495 };

  function toMl(value, unit, cupMl, density) {
    if (unit in MASS_UNITS) return (value * MASS_UNITS[unit]) / density;
    if (unit === "taza") return value * cupMl;
    return value * VOLUME_UNITS[unit];
  }

  function allUnits(ml, cupMl, density) {
    return {
      ml,
      l: ml / 1000,
      cdta: ml / 5,
      cda: ml / 15,
      taza: ml / cupMl,
      g: ml * density,
      kg: (ml * density) / 1000,
      oz: (ml * density) / MASS_UNITS.oz,
    };
  }

  if (typeof module !== "undefined") module.exports = { INGREDIENTS, VOLUME_UNITS, MASS_UNITS, toMl, allUnits };
  if (typeof document === "undefined" || !document.getElementById("co-value")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("co-result-panel");
  const fmt = (n) => {
    const d = n >= 100 ? 0 : n >= 10 ? 1 : 2;
    return new Intl.NumberFormat("es-AR", { maximumFractionDigits: d }).format(Math.round(n * 10 ** d) / 10 ** d);
  };
  const ROWS = [
    ["g", "Gramos (g)"], ["kg", "Kilogramos (kg)"], ["oz", "Onzas (oz)"],
    ["ml", "Mililitros (ml)"], ["l", "Litros (l)"], ["taza", "Tazas"], ["cda", "Cucharadas"], ["cdta", "Cucharaditas"],
  ];

  function calculate() {
    errorEl.classList.add("hidden");
    const el = $("co-value");
    el.classList.remove("field-error");
    try {
      const s = normalizeNumberInput(el.value);
      if (s === "") {
        el.classList.add("field-error");
        throw new Error("Ingresá una cantidad.");
      }
      const v = Number(s);
      if (!Number.isFinite(v) || v <= 0) {
        el.classList.add("field-error");
        throw new Error("La cantidad tiene que ser un número mayor a 0.");
      }
      const unit = $("co-unit").value;
      const cup = Number($("co-cup").value);
      const ing = INGREDIENTS[$("co-ingredient").value];
      const ml = toMl(v, unit, cup, ing.density);
      const all = allUnits(ml, cup, ing.density);
      $("co-rows").innerHTML = ROWS.map(([k, label]) => {
        const mark = k === unit ? " (origen)" : "";
        return `<div class="flex items-baseline justify-between gap-4 border-b border-[var(--color-border)] py-2 last:border-0"><span class="text-sm text-[var(--color-text-muted)]">${label}${mark}</span><span class="font-numeric text-lg font-bold">${fmt(all[k])}</span></div>`;
      }).join("");
      $("co-note").textContent = `Con ${ing.name.toLowerCase()} (≈ ${fmt(ing.density * 1000)} g por litro) y una taza de ${cup} ml. Los gramos son aproximados.`;
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("co-solve").addEventListener("click", calculate);
  ["co-unit", "co-cup", "co-ingredient"].forEach((id) => $(id).addEventListener("change", () => $("co-value").value && calculate()));
  $("co-value").addEventListener("input", () => $("co-value").value && calculate());
  document.querySelectorAll("[data-example]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const [v, unit, ing] = btn.dataset.example.split("|");
      $("co-value").value = v;
      $("co-unit").value = unit;
      $("co-ingredient").value = ing;
      calculate();
    })
  );
})();
