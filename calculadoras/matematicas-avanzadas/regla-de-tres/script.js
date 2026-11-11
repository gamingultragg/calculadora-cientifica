/**
 * Regla de Tres — simple directa, simple inversa y compuesta.
 *   directa:  a es a b como c es a x   =>  x = b·c / a
 *   inversa:  a es a b como c es a x   =>  x = a·b / c
 *   compuesta: R2 = R1 · Π (v2/v1)^(±1)  (+1 si la relación es directa, −1 si es inversa)
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

  function simple(kind, a, b, c) {
    if (a === 0) throw new Error("El primer valor (A) no puede ser 0.");
    if (kind === "inversa" && c === 0) throw new Error("El tercer valor (C) no puede ser 0 en una regla inversa.");
    return kind === "directa" ? (b * c) / a : (a * b) / c;
  }

  // factors: [{ v1, v2, dir: "directa" | "inversa" }]
  function compound(r1, factors) {
    if (!factors.length) throw new Error("Cargá al menos un dato con sus dos valores.");
    let r = r1;
    factors.forEach((f, i) => {
      if (f.v1 === 0) throw new Error(`En el dato ${i + 1}, el primer valor no puede ser 0.`);
      if (f.dir === "inversa" && f.v2 === 0) throw new Error(`En el dato ${i + 1}, el segundo valor no puede ser 0 si la relación es inversa.`);
      r = f.dir === "directa" ? (r * f.v2) / f.v1 : (r * f.v1) / f.v2;
    });
    return r;
  }

  if (typeof module !== "undefined") module.exports = { simple, compound };
  if (typeof document === "undefined" || !document.getElementById("rt-panel-directa")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("rt-result-panel");
  const fmt = (n) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: 6 }).format(Math.round((n + 1e-12) * 1e6) / 1e6);
  const tabs = document.querySelectorAll(".rt-tab-btn");
  const panels = { directa: $("rt-panel-directa"), inversa: $("rt-panel-inversa"), compuesta: $("rt-panel-compuesta") };

  function setTab(tab) {
    tabs.forEach((b) => {
      const on = b.dataset.tab === tab;
      b.classList.toggle("bg-[var(--color-primary)]", on);
      b.classList.toggle("text-white", on);
    });
    Object.entries(panels).forEach(([k, el]) => el.classList.toggle("hidden", k !== tab));
    errorEl.classList.add("hidden");
    panel.classList.add("hidden");
  }
  tabs.forEach((b) => b.addEventListener("click", () => setTab(b.dataset.tab)));

  function num(id, label) {
    const el = $(id);
    el.classList.remove("field-error");
    const s = normalizeNumberInput(el.value);
    if (s === "") {
      el.classList.add("field-error");
      throw new Error(`Completá el campo "${label}".`);
    }
    const v = Number(s);
    if (!Number.isFinite(v)) {
      el.classList.add("field-error");
      throw new Error(`"${label}" tiene que ser un número válido.`);
    }
    return v;
  }

  function show(result, detail, steps) {
    $("rt-result").textContent = fmt(result);
    $("rt-detail").textContent = detail;
    $("rt-steps").innerHTML = steps.map((s) => `<li>${s}</li>`).join("");
    panel.classList.remove("hidden");
  }

  function run(fn) {
    errorEl.classList.add("hidden");
    try {
      fn();
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  ["directa", "inversa"].forEach((kind) => {
    $(`rt-${kind}-solve`).addEventListener("click", () =>
      run(() => {
        const a = num(`${kind}-a`, "A");
        const b = num(`${kind}-b`, "B");
        const c = num(`${kind}-c`, "C");
        const x = simple(kind, a, b, c);
        const formula = kind === "directa" ? `x = (B × C) / A = (${fmt(b)} × ${fmt(c)}) / ${fmt(a)}` : `x = (A × B) / C = (${fmt(a)} × ${fmt(b)}) / ${fmt(c)}`;
        show(x, `Regla de tres simple ${kind}.`, [
          `${fmt(a)} corresponde a ${fmt(b)}, y ${fmt(c)} corresponde a x.`,
          formula,
          `x = ${fmt(x)}`,
        ]);
      })
    );
  });

  $("rt-compuesta-solve").addEventListener("click", () =>
    run(() => {
      const r1 = num("comp-r1", "Resultado conocido");
      const factors = [];
      [1, 2, 3].forEach((i) => {
        const a = $(`comp-${i}-v1`).value.trim();
        const b = $(`comp-${i}-v2`).value.trim();
        if (a === "" && b === "") {
          if (i < 3) throw new Error(`Completá los dos valores del dato ${i}.`);
          return;
        }
        factors.push({ v1: num(`comp-${i}-v1`, `Dato ${i}, valor inicial`), v2: num(`comp-${i}-v2`, `Dato ${i}, valor nuevo`), dir: $(`comp-${i}-dir`).value });
      });
      const x = compound(r1, factors);
      const steps = [`Partimos del resultado conocido: ${fmt(r1)}.`];
      factors.forEach((f, i) =>
        steps.push(
          f.dir === "directa"
            ? `Dato ${i + 1} (directa): × (${fmt(f.v2)} / ${fmt(f.v1)})`
            : `Dato ${i + 1} (inversa): × (${fmt(f.v1)} / ${fmt(f.v2)})`
        )
      );
      steps.push(`Resultado: x = ${fmt(x)}`);
      show(x, "Regla de tres compuesta.", steps);
    })
  );

  setTab("directa");
})();
