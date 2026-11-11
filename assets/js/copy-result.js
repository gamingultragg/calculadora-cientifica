/**
 * copy-result.js — Acciones sobre el resultado de las calculadoras.
 *  - Paneles de resultado (id terminado en "-result-panel"): se agrega una fila debajo del panel,
 *    visible solo mientras el panel está visible, con: Copiar resultado · Copiar enlace · Imprimir.
 *  - "Copiar enlace" arma una URL con los valores cargados (?capital=100000&tasa=24…); al abrirla,
 *    los campos se completan solos y se calcula (ver applyQueryParams).
 *  - Botones con data-copy-target="<id>": copian el texto de ese elemento (científica y básica).
 */
(function () {
  const LABEL_OK = "¡Copiado!";
  const LABEL_ERR = "No se pudo copiar";

  function clean(text) {
    return text
      .replace(/ /g, " ")
      .split("\n")
      .map((l) => l.replace(/[ \t]+/g, " ").trim())
      .filter((l, i, a) => l || (a[i - 1] && a[i - 1] !== ""))
      .join("\n")
      .trim();
  }

  async function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      try {
        await navigator.clipboard.writeText(text);
        return true;
      } catch {
        /* sigue con el método de respaldo */
      }
    }
    try {
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.cssText = "position:fixed;top:0;left:0;opacity:0";
      document.body.appendChild(ta);
      ta.select();
      const ok = document.execCommand("copy");
      ta.remove();
      return ok;
    } catch {
      return false;
    }
  }

  function wire(btn, getText) {
    const original = btn.textContent;
    let timer;
    btn.addEventListener("click", async () => {
      const text = clean(getText());
      if (!text) return;
      const ok = await copyText(text);
      btn.textContent = ok ? LABEL_OK : LABEL_ERR;
      btn.classList.toggle("cc-copy--ok", ok);
      clearTimeout(timer);
      timer = setTimeout(() => {
        btn.textContent = btn.dataset.copyLabel || original;
        btn.classList.remove("cc-copy--ok");
      }, 1800);
    });
  }

  // Botones declarados en el HTML
  document.querySelectorAll("[data-copy-target]").forEach((btn) => {
    wire(btn, () => {
      const el = document.getElementById(btn.dataset.copyTarget);
      return el ? el.innerText || el.textContent : "";
    });
  });

  // ---- Enlace con los valores cargados --------------------------------------------------
  const FIELD_SELECTOR = "main input[id], main select[id], main textarea[id]";
  const SKIP_TYPES = new Set(["file", "password", "button", "submit", "reset", "hidden"]);

  function shareUrl() {
    const params = new URLSearchParams();
    document.querySelectorAll(FIELD_SELECTOR).forEach((el) => {
      if (SKIP_TYPES.has(el.type)) return;
      if (el.type === "checkbox") {
        if (el.checked) params.set(el.id, "1");
        return;
      }
      const v = String(el.value || "").trim();
      if (v && v.length <= 200) params.set(el.id, v);
    });
    const qs = params.toString();
    return location.origin + location.pathname + (qs ? "?" + qs : "");
  }

  // Completa los campos a partir de pares [id, valor] y ejecuta el cálculo. Solo toca campos que ya
  // existen (value/checked): nunca inserta HTML. Con `reset`, vacía los campos de texto que no vienen.
  function applyParams(entries, { reset = false, maxLen = 200 } = {}) {
    const given = new Map(entries);
    if (reset) {
      document.querySelectorAll(FIELD_SELECTOR).forEach((el) => {
        if (SKIP_TYPES.has(el.type) || el.tagName === "SELECT" || given.has(el.id)) return;
        if (el.type === "checkbox") el.checked = false;
        else if (el.value) el.value = "";
      });
    }
    let applied = 0;
    given.forEach((value, id) => {
      if (String(value).length > maxLen) return;
      const el = document.getElementById(id);
      if (!el || !el.matches(FIELD_SELECTOR) || SKIP_TYPES.has(el.type)) return;
      if (el.type === "checkbox") {
        el.checked = value === "1";
      } else if (el.tagName === "SELECT") {
        if (![...el.options].some((o) => o.value === value)) return;
        el.value = value;
      } else {
        el.value = value;
      }
      el.dispatchEvent(new Event("input", { bubbles: true }));
      el.dispatchEvent(new Event("change", { bubbles: true }));
      applied++;
    });
    if (!applied) return;
    const solve = document.querySelector('main button[id$="-solve"]');
    const form = document.querySelector("main form");
    if (solve) solve.click();
    else if (form && typeof form.requestSubmit === "function") form.requestSubmit();
  }

  function applyQueryParams() {
    applyParams(new URLSearchParams(location.search).entries());
  }

  // ---- Historial local (últimos cálculos de esta calculadora, solo en este navegador) ----------
  // Se omite en las calculadoras con filas dinámicas, donde los campos no se pueden restaurar solos.
  const NO_HISTORY = /(calculadora-de-promedio-de-notas|resistencias-serie-paralelo|calculadora-estadistica-descriptiva|calculadora-matrices|regla-de-tres)/;
  const HIST_MAX = 8;
  const HIST_KEY = "cc-hist:" + location.pathname;

  function collectFields(maxLen = 2000) {
    const o = {};
    document.querySelectorAll(FIELD_SELECTOR).forEach((el) => {
      if (SKIP_TYPES.has(el.type)) return;
      if (el.type === "checkbox") {
        if (el.checked) o[el.id] = "1";
        return;
      }
      const v = String(el.value || "").trim();
      if (v && v.length <= maxLen) o[el.id] = v;
    });
    return o;
  }

  function loadHistory() {
    try {
      const list = JSON.parse(localStorage.getItem(HIST_KEY) || "[]");
      return Array.isArray(list) ? list.filter((e) => e && e.f && typeof e.r === "string").slice(0, HIST_MAX) : [];
    } catch {
      return [];
    }
  }
  function saveHistory(list) {
    try {
      localStorage.setItem(HIST_KEY, JSON.stringify(list));
    } catch {
      /* sin almacenamiento: el historial dura solo mientras la página está abierta */
    }
  }

  function resultSummary(panel) {
    const main = panel.querySelector('[id$="-main"], [id$="-result"], [id$="-cuota"], [id$="-total"]');
    let t = main ? main.textContent : (panel.innerText || "").split("\n").slice(1).join(" ");
    t = t.replace(/\s+/g, " ").trim();
    return t.length > 70 ? t.slice(0, 67) + "…" : t;
  }
  function inputsSummary(fields) {
    const vals = Object.entries(fields)
      .filter(([id]) => document.getElementById(id) && document.getElementById(id).tagName !== "SELECT")
      .map(([, v]) => v.replace(/\s+/g, " "));
    const t = vals.slice(0, 3).join(" · ");
    return t.length > 60 ? t.slice(0, 57) + "…" : t || "(sin datos)";
  }

  function setupHistory(panel, anchor) {
    if (NO_HISTORY.test(location.pathname) || document.querySelector(".cc-hist-box")) return;
    const box = document.createElement("details");
    box.className = "cc-hist-box";
    box.hidden = true;
    const summary = document.createElement("summary");
    const list = document.createElement("ul");
    list.className = "cc-hist-list";
    const clear = document.createElement("button");
    clear.type = "button";
    clear.className = "cc-copy";
    clear.textContent = "Borrar historial";
    box.append(summary, list, clear);
    anchor.insertAdjacentElement("afterend", box);

    function render() {
      const items = loadHistory();
      box.hidden = items.length === 0;
      summary.textContent = `Historial de esta calculadora (${items.length})`;
      list.textContent = "";
      items.forEach((e) => {
        const li = document.createElement("li");
        li.className = "cc-history-item";
        const use = document.createElement("button");
        use.type = "button";
        use.className = "cc-history-expr";
        use.textContent = inputsSummary(e.f);
        use.title = "Volver a cargar estos datos";
        use.addEventListener("click", () => applyParams(Object.entries(e.f), { reset: true, maxLen: 2000 }));
        const res = document.createElement("span");
        res.className = "cc-history-res";
        res.textContent = "→ " + e.r;
        li.append(use, res);
        list.append(li);
      });
    }

    let timer;
    function record() {
      if (panel.classList.contains("hidden")) return;
      const fields = collectFields();
      const r = resultSummary(panel);
      if (!r || !Object.keys(fields).length) return;
      let items = loadHistory();
      const key = JSON.stringify(fields);
      items = items.filter((e) => JSON.stringify(e.f) !== key);
      items.unshift({ f: fields, r, t: Date.now() });
      saveHistory(items.slice(0, HIST_MAX));
      render();
    }
    // Esperamos a que el resultado se "asiente" (las calculadoras en vivo recalculan en cada tecla).
    new MutationObserver(() => {
      clearTimeout(timer);
      timer = setTimeout(record, 1500);
    }).observe(panel, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ["class"] });
    clear.addEventListener("click", () => {
      saveHistory([]);
      render();
    });
    render();
  }

  // ---- Paneles de resultado --------------------------------------------------------------
  function makeButton(label, aria) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "cc-copy";
    btn.dataset.copyLabel = label;
    btn.textContent = label;
    btn.setAttribute("aria-label", aria);
    return btn;
  }

  document.querySelectorAll('[id$="-result-panel"]').forEach((panel) => {
    const row = document.createElement("div");
    row.className = "cc-copy-row";
    const copy = makeButton("Copiar resultado", "Copiar el resultado al portapapeles");
    const link = makeButton("Copiar enlace", "Copiar un enlace a esta calculadora con los valores cargados");
    const print = makeButton("Imprimir", "Imprimir o guardar el resultado como PDF");
    row.append(copy, link, print);
    panel.insertAdjacentElement("afterend", row);
    setupHistory(panel, row);
    wire(copy, () => panel.innerText || panel.textContent);
    wire(link, shareUrl);
    print.addEventListener("click", () => window.print());

    const sync = () => {
      row.hidden = panel.classList.contains("hidden");
    };
    sync();
    new MutationObserver(sync).observe(panel, { attributes: true, attributeFilter: ["class", "hidden"] });
  });

  applyQueryParams();
})();
