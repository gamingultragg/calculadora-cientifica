/**
 * ads.js — Ubicaciones de anuncios de Google AdSense.
 *
 * Cada página tiene contenedores <aside class="cc-ad" data-ad="..."> (calc, guide,
 * home, cat) que arrancan ocultos y sin ocupar espacio. Este script solo muestra un
 * contenedor si su tipo tiene un ID de unidad de anuncio (data-ad-slot) cargado en
 * SLOTS: mientras estén vacíos, el sitio se ve exactamente igual que sin anuncios.
 *
 * Cómo activarlos:
 *   1. En AdSense: Anuncios > Por unidad de anuncio > Anuncios de display
 *      (responsive). Crear una unidad por tipo y copiar su "data-ad-slot" (10 dígitos).
 *   2. Pegar cada ID abajo en SLOTS.
 *   3. En AdSense: Anuncios > Por sitio > Editar > apagar "Anuncios automáticos"
 *      (si no, Google sigue inyectando anuncios por su cuenta).
 *
 * Carga diferida: el anuncio se pide recién cuando el contenedor está por entrar en
 * pantalla (400 px antes), así no compite con la carga inicial de la página.
 */
(function () {
  const CLIENT = "ca-pub-7274131858034505";
  const SLOTS = {
    calc: "", // calculadoras: columna derecha, debajo de la ayuda
    guide: "", // guías: al final del artículo
    home: "", // home: entre las calculadoras y las guías
    cat: "", // páginas de categoría: debajo de la grilla
  };

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
