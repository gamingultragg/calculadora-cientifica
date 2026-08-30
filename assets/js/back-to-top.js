/**
 * back-to-top.js — Botones flotantes: "volver arriba" (scroll suave al
 * inicio de la página actual) y "volver al home" (navega a /, ausente en
 * la propia home). Ambos aparecen apenas se empieza a scrollear.
 */
(function () {
  const topBtn = document.getElementById("back-to-top");
  const homeBtn = document.getElementById("back-to-home");
  if (!topBtn && !homeBtn) return;

  function toggle(btn) {
    if (!btn) return;
    const visible = window.scrollY > 50;
    btn.classList.toggle("opacity-0", !visible);
    btn.classList.toggle("pointer-events-none", !visible);
    btn.classList.toggle("translate-y-2", !visible);
  }

  if (topBtn) {
    topBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  window.addEventListener(
    "scroll",
    () => {
      toggle(topBtn);
      toggle(homeBtn);
    },
    { passive: true }
  );
  toggle(topBtn);
  toggle(homeBtn);
})();
