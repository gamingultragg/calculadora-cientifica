/**
 * Calculadora del Teorema de Pitágoras — a² + b² = c² (triángulo rectángulo).
 * Dados dos lados calcula el tercero, más área, perímetro, altura sobre la hipotenusa y ángulos.
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

  const toDeg = (rad) => (rad * 180) / Math.PI;

  // a, b catetos; c hipotenusa.
  const hypotenuse = (a, b) => Math.hypot(a, b);
  function leg(c, other) {
    if (c <= other) throw new Error("La hipotenusa tiene que ser mayor que el cateto: es el lado más largo del triángulo.");
    return Math.sqrt(c * c - other * other);
  }

  function solve(target, x, y) {
    let a, b, c;
    if (target === "c") {
      a = x;
      b = y;
      c = hypotenuse(a, b);
    } else if (target === "a") {
      c = x;
      b = y;
      a = leg(c, b);
    } else {
      c = x;
      a = y;
      b = leg(c, a);
    }
    return {
      a, b, c,
      area: (a * b) / 2,
      perimeter: a + b + c,
      height: (a * b) / c, // altura sobre la hipotenusa
      angleA: toDeg(Math.atan2(a, b)), // opuesto al cateto a
      angleB: toDeg(Math.atan2(b, a)),
    };
  }

  if (typeof module !== "undefined") module.exports = { solve, hypotenuse, leg };
  if (typeof document === "undefined" || !document.getElementById("pt-target")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("pt-result-panel");
  const fmt = (n, d = 4) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: d }).format(Math.round((n + 1e-12) * 10 ** d) / 10 ** d);

  // Qué dos datos se piden según el lado a calcular.
  const INPUTS = {
    c: [["pt-x", "Cateto a"], ["pt-y", "Cateto b"]],
    a: [["pt-x", "Hipotenusa c"], ["pt-y", "Cateto b"]],
    b: [["pt-x", "Hipotenusa c"], ["pt-y", "Cateto a"]],
  };
  function syncLabels() {
    const t = $("pt-target").value;
    INPUTS[t].forEach(([id, label]) => ($(id + "-label").textContent = label));
    errorEl.classList.add("hidden");
    panel.classList.add("hidden");
  }

  function read(id, label) {
    const el = $(id);
    el.classList.remove("field-error");
    const s = normalizeNumberInput(el.value);
    if (s === "") {
      el.classList.add("field-error");
      throw new Error(`Completá el campo "${label}".`);
    }
    const v = Number(s);
    if (!Number.isFinite(v) || v <= 0) {
      el.classList.add("field-error");
      throw new Error(`"${label}" tiene que ser un número mayor a 0.`);
    }
    return v;
  }

  function calculate() {
    errorEl.classList.add("hidden");
    try {
      const t = $("pt-target").value;
      const [[idX, lx], [idY, ly]] = INPUTS[t];
      const x = read(idX, lx), y = read(idY, ly);
      const r = solve(t, x, y);
      const name = { c: "Hipotenusa c", a: "Cateto a", b: "Cateto b" }[t];
      const main = { c: r.c, a: r.a, b: r.b }[t];
      const formula =
        t === "c"
          ? `c = √(a² + b²) = √(${fmt(x)}² + ${fmt(y)}²) = √${fmt(x * x + y * y)}`
          : `${t} = √(c² − ${t === "a" ? "b" : "a"}²) = √(${fmt(x)}² − ${fmt(y)}²) = √${fmt(x * x - y * y)}`;
      $("pt-label").textContent = name;
      $("pt-main").textContent = fmt(main, 6);
      $("pt-lines").innerHTML = [
        `<p>${formula}</p>`,
        `<p>Catetos: a = <strong>${fmt(r.a)}</strong> y b = <strong>${fmt(r.b)}</strong> · Hipotenusa: c = <strong>${fmt(r.c)}</strong></p>`,
        `<p>Área: <strong>${fmt(r.area)}</strong> · Perímetro: <strong>${fmt(r.perimeter)}</strong> · Altura sobre la hipotenusa: <strong>${fmt(r.height)}</strong></p>`,
        `<p>Ángulos agudos: <strong>${fmt(r.angleA, 2)}°</strong> (opuesto a <em>a</em>) y <strong>${fmt(r.angleB, 2)}°</strong> (opuesto a <em>b</em>), más el ángulo recto de 90°.</p>`,
      ].join("");
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("pt-target").addEventListener("change", syncLabels);
  $("pt-solve").addEventListener("click", calculate);
  document.querySelectorAll("input").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && calculate()));
  document.querySelectorAll("[data-example]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const [t, x, y] = btn.dataset.example.split("|");
      $("pt-target").value = t;
      syncLabels();
      $("pt-x").value = x;
      $("pt-y").value = y;
      calculate();
    })
  );
  syncLabels();
})();
