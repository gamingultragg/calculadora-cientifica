/**
 * calc-simple.js — Motor común para calculadoras de tipo "campos → resultado".
 *
 * El HTML (generado por scripts/spec_lib.py) declara los campos con atributos de datos y este motor
 * lee, valida y muestra el resultado. Cada calculadora solo aporta `compute(valores, helpers)`.
 *
 * Contrato del HTML (prefijo p):
 *   <div id="p-w-ID" data-when="modo=a|b">   envoltorio del campo (data-when: visible solo con esos valores)
 *   <input id="p-ID" data-kind="num" data-label="..." data-rule="pos|nonneg|any|int" data-opt data-def="…">
 *   <select id="p-ID" data-kind="sel"> · <input/textarea id="p-ID" data-kind="text" data-label="...">
 *   <button id="p-solve">, <section id="p-result-panel">, #p-label, #p-main, #p-lines, #p-extra (opcional)
 *   chips: <button data-ex="campo=valor;campo=valor">
 */
(function (root) {
  function normalizeNumberInput(value) {
    let str = String(value).trim();
    if (str.includes(",")) {
      str = str.replace(/\./g, "").replace(",", ".");
    } else if (/^-?[1-9]\d{0,2}(\.\d{3})+$/.test(str)) {
      str = str.replace(/\./g, "");
    }
    return str;
  }

  const nf = (d) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: d });
  const helpers = {
    // número con hasta d decimales (redondeo estable)
    fmt: (n, d = 2) => nf(d).format(Math.round((n + Number.EPSILON * Math.sign(n)) * 10 ** d) / 10 ** d),
    money: (n) => "$" + new Intl.NumberFormat("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(Math.round((n + 1e-9) * 100) / 100),
    pct: (n, d = 2) => nf(d).format(Math.round((n * 100 + 1e-12) * 10 ** d) / 10 ** d) + " %",
    int: (n) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: 0 }).format(Math.ceil(n - 1e-9)),
  };

  function mount(cfg) {
    const p = cfg.prefix;
    const $ = (id) => document.getElementById(`${p}-${id}`);
    const errorEl = document.getElementById("err");
    const panel = $("result-panel");
    const fields = [...document.querySelectorAll(`[id^="${p}-"][data-kind]`)].map((el) => ({ el, id: el.id.slice(p.length + 1), kind: el.dataset.kind }));

    function visible(f) {
      const wrap = $("w-" + f.id);
      return !wrap || !wrap.classList.contains("hidden");
    }

    function syncWhen() {
      const vals = {};
      fields.forEach((f) => (vals[f.id] = f.el.value));
      document.querySelectorAll(`[id^="${p}-w-"][data-when]`).forEach((wrap) => {
        const [key, list] = wrap.dataset.when.split("=");
        wrap.classList.toggle("hidden", !list.split("|").includes(String(vals[key])));
      });
    }

    function readValues() {
      const v = {};
      fields.forEach((f) => {
        f.el.classList.remove("field-error");
        if (!visible(f)) return;
        const raw = f.el.value;
        const label = f.el.dataset.label || f.id;
        if (f.kind === "sel") {
          v[f.id] = raw;
          return;
        }
        if (f.kind === "text") {
          if (String(raw).trim() === "" && f.el.dataset.opt === undefined) {
            f.el.classList.add("field-error");
            throw new Error(`Completá el campo "${label}".`);
          }
          v[f.id] = String(raw).trim();
          return;
        }
        const s = normalizeNumberInput(raw);
        if (s === "") {
          if (f.el.dataset.opt !== undefined) {
            v[f.id] = f.el.dataset.def !== undefined ? Number(f.el.dataset.def) : undefined;
            return;
          }
          f.el.classList.add("field-error");
          throw new Error(`Completá el campo "${label}".`);
        }
        const n = Number(s);
        const rule = f.el.dataset.rule || "pos";
        const bad =
          !Number.isFinite(n) ||
          (rule === "pos" && n <= 0) ||
          (rule === "nonneg" && n < 0) ||
          (rule === "int" && (!Number.isInteger(n) || n < 1));
        if (bad) {
          f.el.classList.add("field-error");
          const msg = { pos: "mayor a 0", nonneg: "mayor o igual a 0", int: "entero de 1 o más", any: "válido" }[rule];
          throw new Error(`"${label}" tiene que ser un número ${msg}.`);
        }
        v[f.id] = n;
      });
      return v;
    }

    function calculate() {
      errorEl.classList.add("hidden");
      try {
        const r = cfg.compute(readValues(), helpers);
        const label = $("label");
        if (label && r.label !== undefined) label.textContent = r.label;
        $("main").textContent = r.main;
        $("lines").innerHTML = (r.lines || []).filter(Boolean).map((l) => `<p>${l}</p>`).join("");
        const extra = $("extra");
        if (extra) extra.innerHTML = r.extra || "";
        panel.classList.remove("hidden");
      } catch (err) {
        errorEl.textContent = err.message;
        errorEl.classList.remove("hidden");
        panel.classList.add("hidden");
      }
    }

    fields.forEach((f) => {
      if (f.kind === "sel") f.el.addEventListener("change", () => {
        syncWhen();
        errorEl.classList.add("hidden");
        panel.classList.add("hidden");
      });
      if (f.el.tagName !== "TEXTAREA") f.el.addEventListener("keydown", (e) => e.key === "Enter" && calculate());
    });
    $("solve").addEventListener("click", calculate);
    document.querySelectorAll("[data-ex]").forEach((btn) =>
      btn.addEventListener("click", () => {
        btn.dataset.ex.split(";").forEach((pair) => {
          const i = pair.indexOf("=");
          const f = fields.find((x) => x.id === pair.slice(0, i));
          if (f) f.el.value = pair.slice(i + 1);
        });
        syncWhen();
        calculate();
      })
    );
    syncWhen();
  }

  const api = { mount, helpers, normalizeNumberInput };
  root.CCSimple = api;
  if (typeof module !== "undefined") module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
