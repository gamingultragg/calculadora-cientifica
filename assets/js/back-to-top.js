/**
 * back-to-top.js — Botón flotante para volver al inicio de la página.
 * Aparece recién después de scrollear una pantalla hacia abajo, y hace
 * scroll suave al hacer clic.
 */
(function () {
  const btn = document.getElementById("back-to-top");
  if (!btn) return;

  function toggle() {
    const visible = window.scrollY > 400;
    btn.classList.toggle("opacity-0", !visible);
    btn.classList.toggle("pointer-events-none", !visible);
    btn.classList.toggle("translate-y-2", !visible);
  }

  btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  window.addEventListener("scroll", toggle, { passive: true });
  toggle();
})();
