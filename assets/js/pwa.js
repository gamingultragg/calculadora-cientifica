/**
 * pwa.js — Registra el service worker (funciona sin conexión) y ofrece "Instalar app"
 * cuando el navegador lo permite (Chrome/Edge/Android). En iOS se instala desde Compartir.
 */
(function () {
  if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost" || location.hostname === "127.0.0.1")) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(() => {});
    });
  }

  let deferred = null;
  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferred = e;
    showInstall();
  });
  window.addEventListener("appinstalled", () => {
    deferred = null;
    const b = document.getElementById("cc-install");
    if (b) b.remove();
  });

  function showInstall() {
    if (document.getElementById("cc-install")) return;
    if (window.matchMedia("(display-mode: standalone)").matches) return;
    const footerP = document.querySelector("footer p");
    if (!footerP) return;
    const btn = document.createElement("button");
    btn.id = "cc-install";
    btn.type = "button";
    btn.className = "cc-copy";
    btn.textContent = "Instalar app";
    btn.setAttribute("aria-label", "Instalar Calculadora Científica como aplicación");
    btn.addEventListener("click", async () => {
      if (!deferred) return;
      deferred.prompt();
      try {
        await deferred.userChoice;
      } catch {
        /* ignorado */
      }
      deferred = null;
      btn.remove();
    });
    footerP.parentElement.insertBefore(btn, footerP.nextSibling);
  }
})();
