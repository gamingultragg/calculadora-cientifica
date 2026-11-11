/**
 * copy-result.js — Botón "Copiar resultado" para todas las calculadoras.
 *  - Paneles de resultado (id terminado en "-result-panel"): se agrega un botón debajo del panel,
 *    visible solo mientras el panel está visible, que copia el texto del panel.
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

  // Paneles de resultado
  document.querySelectorAll('[id$="-result-panel"]').forEach((panel) => {
    const row = document.createElement("div");
    row.className = "cc-copy-row";
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "cc-copy";
    btn.dataset.copyLabel = "Copiar resultado";
    btn.textContent = "Copiar resultado";
    btn.setAttribute("aria-label", "Copiar el resultado al portapapeles");
    row.appendChild(btn);
    panel.insertAdjacentElement("afterend", row);
    wire(btn, () => panel.innerText || panel.textContent);

    const sync = () => {
      row.hidden = panel.classList.contains("hidden");
    };
    sync();
    new MutationObserver(sync).observe(panel, { attributes: true, attributeFilter: ["class", "hidden"] });
  });
})();
