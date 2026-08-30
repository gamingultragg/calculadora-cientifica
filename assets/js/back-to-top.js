/**
 * back-to-top.js — Botón flotante "volver arriba" (scroll suave al inicio
 * de la página actual), visible apenas se empieza a scrollear. El botón
 * "volver al home" es independiente del scroll: siempre visible (se
 * inyecta ya sin las clases que lo ocultan, ver inject-back-to-home.py).
 */
(function () {
  const topBtn = document.getElementById("back-to-top");
  if (!topBtn) return;

  function toggle() {
    const visible = window.scrollY > 50;
    topBtn.classList.toggle("opacity-0", !visible);
    topBtn.classList.toggle("pointer-events-none", !visible);
    topBtn.classList.toggle("translate-y-2", !visible);
  }

  topBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  window.addEventListener("scroll", toggle, { passive: true });
  toggle();
})();
