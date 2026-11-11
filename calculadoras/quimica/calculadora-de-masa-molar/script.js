/**
 * Calculadora de Masa Molar — interpreta una fórmula química (H2SO4, Ca(OH)2,
 * CuSO4·5H2O…), suma las masas atómicas y muestra el desglose por elemento, la
 * composición porcentual y la conversión masa ↔ moles.
 *
 * Masas atómicas estándar (IUPAC, valores convencionales redondeados).
 */
(function () {
  const ATOMIC = {
    H: 1.008, He: 4.0026, Li: 6.94, Be: 9.0122, B: 10.81, C: 12.011, N: 14.007, O: 15.999,
    F: 18.998, Ne: 20.18, Na: 22.99, Mg: 24.305, Al: 26.982, Si: 28.085, P: 30.974, S: 32.065,
    Cl: 35.45, Ar: 39.95, K: 39.098, Ca: 40.078, Sc: 44.956, Ti: 47.867, V: 50.942, Cr: 51.996,
    Mn: 54.938, Fe: 55.845, Co: 58.933, Ni: 58.693, Cu: 63.546, Zn: 65.38, Ga: 69.723,
    Ge: 72.63, As: 74.922, Se: 78.971, Br: 79.904, Kr: 83.798, Rb: 85.468, Sr: 87.62, Y: 88.906,
    Zr: 91.224, Nb: 92.906, Mo: 95.95, Ru: 101.07, Rh: 102.91, Pd: 106.42, Ag: 107.87,
    Cd: 112.41, In: 114.82, Sn: 118.71, Sb: 121.76, Te: 127.6, I: 126.9, Xe: 131.29, Cs: 132.91,
    Ba: 137.33, La: 138.91, Ce: 140.12, Pr: 140.91, Nd: 144.24, Sm: 150.36, Eu: 151.96,
    Gd: 157.25, Tb: 158.93, Dy: 162.5, Ho: 164.93, Er: 167.26, Tm: 168.93, Yb: 173.05,
    Lu: 174.97, Hf: 178.49, Ta: 180.95, W: 183.84, Re: 186.21, Os: 190.23, Ir: 192.22,
    Pt: 195.08, Au: 196.97, Hg: 200.59, Tl: 204.38, Pb: 207.2, Bi: 208.98, Th: 232.04, U: 238.03,
  };

  function normalizeNumberInput(value) {
    let str = String(value).trim();
    if (str.includes(",")) {
      str = str.replace(/\./g, "").replace(",", ".");
    } else if (/^-?[1-9]\d{0,2}(\.\d{3})+$/.test(str)) {
      str = str.replace(/\./g, "");
    }
    return str;
  }

  function addInto(target, source, times) {
    source.forEach((count, sym) => target.set(sym, (target.get(sym) || 0) + count * times));
  }

  // Interpreta un grupo sin hidratos: elementos, números y paréntesis/corchetes.
  function parseGroup(s) {
    let i = 0;
    const stack = [new Map()];
    function readInt() {
      let j = i;
      while (j < s.length && /\d/.test(s[j])) j++;
      const n = j > i ? parseInt(s.slice(i, j), 10) : 1;
      i = j;
      return n;
    }
    while (i < s.length) {
      const ch = s[i];
      if (ch === "(" || ch === "[") {
        stack.push(new Map());
        i++;
      } else if (ch === ")" || ch === "]") {
        if (stack.length < 2) throw new Error("Hay un paréntesis de cierre sin su apertura.");
        i++;
        const times = readInt();
        const inner = stack.pop();
        addInto(stack[stack.length - 1], inner, times);
      } else if (/[A-Z]/.test(ch)) {
        let sym = ch;
        i++;
        if (i < s.length && /[a-z]/.test(s[i])) {
          sym += s[i];
          i++;
        }
        if (!(sym in ATOMIC)) {
          throw new Error(
            `No reconozco el elemento "${sym}". Revisá las mayúsculas y minúsculas (por ejemplo Co es cobalto y CO es carbono + oxígeno).`
          );
        }
        const count = readInt();
        addInto(stack[stack.length - 1], new Map([[sym, 1]]), count);
      } else if (/[a-z]/.test(ch)) {
        throw new Error(`Los símbolos empiezan con mayúscula (H2O, no h2o). Revisá "${ch}".`);
      } else if (/\d/.test(ch)) {
        throw new Error("Hay un número suelto sin elemento delante (los subíndices van después del símbolo).");
      } else {
        throw new Error(`Carácter no válido en la fórmula: "${ch}".`);
      }
    }
    if (stack.length > 1) throw new Error("Falta cerrar un paréntesis.");
    return stack[0];
  }

  function parseFormula(input) {
    const s = String(input)
      .trim()
      .replace(/[₀-₉]/g, (d) => String(d.charCodeAt(0) - 0x2080))
      .replace(/\s+/g, "");
    if (!s) throw new Error("Escribí una fórmula, por ejemplo H2SO4.");
    // Hidratos: CuSO4·5H2O (también con . o *; el punto solo separa si sigue un coeficiente o elemento).
    const parts = s.split(/[·•*]|\.(?=\d*[A-Z(\[])/);
    const total = new Map();
    parts.forEach((part) => {
      if (!part) throw new Error("Hay un separador de hidrato sin fórmula al lado.");
      const m = part.match(/^(\d+)(.+)$/);
      const coef = m ? parseInt(m[1], 10) : 1;
      addInto(total, parseGroup(m ? m[2] : part), coef);
    });
    return total;
  }

  const round = (n, d) => Math.round((n + 1e-9) * 10 ** d) / 10 ** d;

  function molarMass(input) {
    const counts = parseFormula(input);
    let total = 0;
    counts.forEach((count, sym) => (total += count * ATOMIC[sym]));
    const rows = [];
    counts.forEach((count, sym) => {
      const subtotal = count * ATOMIC[sym];
      rows.push({ symbol: sym, count, mass: ATOMIC[sym], subtotal, percent: (subtotal / total) * 100 });
    });
    return { total, rows };
  }

  if (typeof module !== "undefined") module.exports = { molarMass, parseFormula, ATOMIC };
  if (typeof document === "undefined" || !document.getElementById("mm-formula")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("mm-result-panel");
  const fmt2 = (n) => new Intl.NumberFormat("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(round(n, 2));
  const fmt = (n, max = 4) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: max }).format(round(n, max));

  function showError(msg) {
    errorEl.textContent = msg;
    errorEl.classList.remove("hidden");
    panel.classList.add("hidden");
  }

  function readOptional(id, label) {
    const raw = normalizeNumberInput($(id).value);
    if (raw === "") return null;
    const v = Number(raw);
    if (!Number.isFinite(v) || v < 0) throw new Error(`"${label}" tiene que ser un número mayor o igual a 0.`);
    return v;
  }

  function calculate() {
    errorEl.classList.add("hidden");
    $("mm-formula").classList.remove("field-error");
    try {
      const { total, rows } = molarMass($("mm-formula").value);
      const grams = readOptional("mm-grams", "Masa de la muestra");
      const moles = readOptional("mm-moles", "Moles");

      $("mm-total").textContent = `${fmt2(total)} g/mol`;
      $("mm-formula-shown").textContent = $("mm-formula").value.trim();
      $("mm-rows").innerHTML = rows
        .map(
          (r) => `<tr class="border-t border-[var(--color-border)]">
            <td class="px-3 py-2 font-semibold">${r.symbol}</td>
            <td class="px-3 py-2">${r.count}</td>
            <td class="px-3 py-2">${fmt(r.mass, 3)}</td>
            <td class="px-3 py-2">${fmt(r.subtotal, 3)}</td>
            <td class="px-3 py-2">${fmt(r.percent, 2)} %</td></tr>`
        )
        .join("");

      const conv = [];
      if (grams !== null) conv.push(`${fmt(grams)} g equivalen a <strong>${fmt(grams / total, 6)} mol</strong>.`);
      if (moles !== null) conv.push(`${fmt(moles)} mol equivalen a <strong>${fmt(moles * total, 4)} g</strong>.`);
      const convEl = $("mm-conv");
      convEl.innerHTML = conv.map((c) => `<p>${c}</p>`).join("");
      convEl.classList.toggle("hidden", conv.length === 0);
      panel.classList.remove("hidden");
    } catch (err) {
      $("mm-formula").classList.add("field-error");
      showError(err.message);
    }
  }

  $("mm-solve").addEventListener("click", calculate);
  document.querySelectorAll("[data-example]").forEach((btn) =>
    btn.addEventListener("click", () => {
      $("mm-formula").value = btn.dataset.example;
      calculate();
    })
  );
  ["mm-formula", "mm-grams", "mm-moles"].forEach((id) =>
    $(id).addEventListener("keydown", (e) => {
      if (e.key === "Enter") calculate();
    })
  );
})();
