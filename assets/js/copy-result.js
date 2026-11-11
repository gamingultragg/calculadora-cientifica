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

  // Completa los campos a partir de ?id=valor y ejecuta el cálculo. Solo toca campos que ya existen
  // (value/checked): nunca inserta HTML.
  function applyQueryParams() {
    const params = new URLSearchParams(location.search);
    let applied = 0;
    params.forEach((value, id) => {
      if (value.length > 200) return;
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
