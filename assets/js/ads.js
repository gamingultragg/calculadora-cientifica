/**
 * ads.js — Ubicaciones de anuncios de Google AdSense.
 *
 * Cada página tiene contenedores <aside class="cc-ad" data-ad="..."> (calc, guide,
 * home, cat) que arrancan ocultos y sin ocupar espacio. Este script los muestra solo
 * si ENABLED es true y su tipo tiene un ID de unidad en SLOTS; si no, el sitio se ve
 * exactamente igual que sin anuncios.
 *
 * Unidades creadas en AdSense (display, adaptables) el 2026-11-10: calculadoras,
 * guias, home y categorias. Los anuncios automáticos del sitio ya están
 * DESACTIVADOS en AdSense (Anuncios > Por sitio).
 *
 * PARA ACTIVAR: poner ENABLED = true cuando AdSense > Sitios muestre el sitio como
 * "Listo" (hoy figura "Preparando": todavía no sirve anuncios, y encenderlos antes
 * dejaría cajas vacías con la etiqueta "Publicidad"). Si un anuncio no se llena,
 * el contenedor se oculta solo.
 *
 * Carga diferida: el anuncio se pide recién cuando el contenedor está por entrar en
 * pantalla (400 px antes), así no compite con la carga inicial de la página.
 */
(function () {
  const ENABLED = false;
  const CLIENT = "ca-pub-7274131858034505";
  const SLOTS = {
    calc: "8844192446", // calculadoras: columna derecha, debajo de la ayuda
    guide: "4200359527", // guías: al final del artículo
    home: "5593332249", // home: entre las calculadoras y las guías
    cat: "4144519200", // páginas de categoría: debajo de la grilla
  };

  if (!ENABLED) return;
  const nodes = document.querySelectorAll(".cc-ad[data-ad]");
  if (!nodes.length) return;

  function mount(node, slot) {
    const holder = node.querySelector(".cc-ad-slot");
    if (!holder || holder.firstChild) return;
    const ins = document.createElement("ins");
    ins.className = "adsbygoogle";
    ins.style.display = "block";
    ins.setAttribute("data-ad-client", CLIENT);
    ins.setAttribute("data-ad-slot", slot);
    ins.setAttribute("data-ad-format", "auto");
    ins.setAttribute("data-full-width-responsive", "true");
    holder.appendChild(ins);
    // Si AdSense no tiene anuncio para llenar el espacio, marca el <ins> como
    // data-ad-status="unfilled": ocultamos todo el contenedor (etiqueta y altura).
    if ("MutationObserver" in window) {
      new MutationObserver(() => {
        if (ins.getAttribute("data-ad-status") === "unfilled") node.hidden = true;
      }).observe(ins, { attributes: true, attributeFilter: ["data-ad-status"] });
    }
    try {
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    } catch (e) {
      /* si el script de AdSense no cargó (bloqueador), el espacio queda vacío */
    }
  }

  nodes.forEach((node) => {
    const slot = SLOTS[node.dataset.ad];
    if (!slot) return;
    node.hidden = false;
    if (!("IntersectionObserver" in window)) {
      mount(node, slot);
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          io.disconnect();
          mount(node, slot);
        });
      },
      { rootMargin: "400px 0px" }
    );
    io.observe(node);
  });
})();
