/**
 * Conversor de Unidades Técnicas — longitud, masa, presión, caudal y torque.
 * Cada categoría define un factor de conversión hacia una unidad base;
 * convertir A→B es: valor × factor[A] / factor[B].
 */
(function () {
  // Convierte un input numérico en formato es-AR ("15.000" con punto de
  // miles, "1.234,56" con punto de miles y coma decimal, o un número
  // simple como "9.8") al formato que entiende Number(). Un punto seguido
  // de 1, 2 o más de 3 dígitos se interpreta como separador decimal (no
  // de miles), evitando falsos positivos como "3.14" o "0.5".
  function normalizeNumberInput(value) {
    let str = String(value).trim();
    if (str.includes(",")) {
      str = str.replace(/\./g, "").replace(",", ".");
    } else if (/^-?[1-9]\d{0,2}(\.\d{3})+$/.test(str)) {
      str = str.replace(/\./g, "");
    }
    return str;
  }

  const CATEGORIES = {
    longitud: {
      label: "Longitud",
      base: "m",
      units: {
        m: { label: "Metros (m)", factor: 1 },
        km: { label: "Kilómetros (km)", factor: 1000 },
        cm: { label: "Centímetros (cm)", factor: 0.01 },
        mm: { label: "Milímetros (mm)", factor: 0.001 },
        in: { label: "Pulgadas (in)", factor: 0.0254 },
        ft: { label: "Pies (ft)", factor: 0.3048 },
        yd: { label: "Yardas (yd)", factor: 0.9144 },
        mi: { label: "Millas (mi)", factor: 1609.344 },
      },
    },
    masa: {
      label: "Masa",
      base: "kg",
      units: {
        kg: { label: "Kilogramos (kg)", factor: 1 },
        g: { label: "Gramos (g)", factor: 0.001 },
        mg: { label: "Miligramos (mg)", factor: 0.000001 },
        ton: { label: "Toneladas métricas (t)", factor: 1000 },
        lb: { label: "Libras (lb)", factor: 0.45359237 },
        oz: { label: "Onzas (oz)", factor: 0.028349523 },
      },
    },
    presion: {
      label: "Presión",
      base: "Pa",
      units: {
        Pa: { label: "Pascales (Pa)", factor: 1 },
        kPa: { label: "Kilopascales (kPa)", factor: 1000 },
        MPa: { label: "Megapascales (MPa)", factor: 1000000 },
        bar: { label: "Bar", factor: 100000 },
        atm: { label: "Atmósferas (atm)", factor: 101325 },
        psi: { label: "PSI (lbf/in²)", factor: 6894.757 },
        mmHg: { label: "Milímetros de mercurio (mmHg)", factor: 133.322 },
      },
    },
    caudal: {
      label: "Caudal",
      base: "m3s",
      units: {
        m3s: { label: "Metros cúbicos/segundo (m³/s)", factor: 1 },
        m3h: { label: "Metros cúbicos/hora (m³/h)", factor: 1 / 3600 },
        ls: { label: "Litros/segundo (L/s)", factor: 0.001 },
        lmin: { label: "Litros/minuto (L/min)", factor: 0.001 / 60 },
        galmin: { label: "Galones US/minuto (gal/min)", factor: 0.0000630902 },
      },
    },
    torque: {
      label: "Torque",
      base: "Nm",
      units: {
        Nm: { label: "Newton·metro (N·m)", factor: 1 },
        kgfm: { label: "Kilogramo-fuerza·metro (kgf·m)", factor: 9.80665 },
        lbfft: { label: "Libra-fuerza·pie (lbf·ft)", factor: 1.35582 },
        lbfin: { label: "Libra-fuerza·pulgada (lbf·in)", factor: 0.112985 },
      },
    },
  };

  const categorySelect = document.getElementById("cv-category");
  const fromSelect = document.getElementById("cv-from");
  const toSelect = document.getElementById("cv-to");
  const valueInput = document.getElementById("cv-value");
  const swapBtn = document.getElementById("cv-swap");
  const errorEl = document.getElementById("cv-error");
  const resultEl = document.getElementById("cv-result");

  Object.entries(CATEGORIES).forEach(([key, cat]) => {
    const opt = document.createElement("option");
    opt.value = key;
    opt.textContent = cat.label;
    categorySelect.appendChild(opt);
  });

  function populateUnitSelects() {
    const cat = CATEGORIES[categorySelect.value];
    [fromSelect, toSelect].forEach((select) => (select.innerHTML = ""));
    Object.entries(cat.units).forEach(([unitKey, unit]) => {
      [fromSelect, toSelect].forEach((select) => {
        const opt = document.createElement("option");
        opt.value = unitKey;
        opt.textContent = unit.label;
        select.appendChild(opt);
      });
    });
    const keys = Object.keys(cat.units);
    fromSelect.value = keys[0];
    toSelect.value = keys[1] || keys[0];
  }

  function showError(message) {
    errorEl.textContent = message;
    errorEl.classList.remove("hidden");
    resultEl.textContent = "—";
  }
  function clearError() {
    errorEl.classList.add("hidden");
    errorEl.textContent = "";
  }

  const fmt = (n) =>
    new Intl.NumberFormat("es-AR", { maximumFractionDigits: 8 }).format(
      Object.is(n, -0) ? 0 : Math.round(n * 1e10) / 1e10
    );

  function convert() {
    clearError();
    const raw = normalizeNumberInput(valueInput.value);
    if (raw === "") {
      resultEl.textContent = "—";
      return;
    }
    const value = Number(raw);
    if (!Number.isFinite(value)) {
      showError("El valor ingresado no es un número válido.");
      return;
    }

    const cat = CATEGORIES[categorySelect.value];
    const fromUnit = cat.units[fromSelect.value];
    const toUnit = cat.units[toSelect.value];
    const result = (value * fromUnit.factor) / toUnit.factor;

    resultEl.textContent = `${fmt(value)} ${fromSelect.options[fromSelect.selectedIndex].text.match(/\(([^)]+)\)/)?.[1] ?? ""} = ${fmt(result)} ${toSelect.options[toSelect.selectedIndex].text.match(/\(([^)]+)\)/)?.[1] ?? ""}`;
  }

  categorySelect.addEventListener("change", () => {
    populateUnitSelects();
    convert();
  });
  fromSelect.addEventListener("change", convert);
  toSelect.addEventListener("change", convert);
  valueInput.addEventListener("input", convert);
  swapBtn.addEventListener("click", () => {
    const tmp = fromSelect.value;
    fromSelect.value = toSelect.value;
    toSelect.value = tmp;
    convert();
  });

  populateUnitSelects();
  valueInput.value = "1";
  convert();
})();
