/* sw.js — GENERADO por scripts/build-sw.py (no editar a mano: editar sw-template.js).
 * Estrategia: precarga del sitio (páginas + CSS + JS) para que funcione sin conexión;
 * red primero con respaldo en caché; tipografías de Google en caché "stale-while-revalidate".
 * No intercepta anuncios, analítica ni nada de otros orígenes (salvo las tipografías). */
const VERSION = "40c7759e94";
const CACHE = "cc-" + VERSION;
const FONTS = "cc-fonts-v1";
const PRECACHE = [
 "/",
 "/calculadoras/matematicas-avanzadas/",
 "/calculadoras/estadistica/",
 "/calculadoras/fisica/",
 "/calculadoras/quimica/",
 "/calculadoras/ingenieria/",
 "/calculadoras/finanzas/",
 "/calculadoras/matematicas-avanzadas/calculadora-basica/",
 "/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/",
 "/calculadoras/matematicas-avanzadas/ecuaciones-segundo-grado/",
 "/calculadoras/matematicas-avanzadas/calculadora-matrices/",
 "/calculadoras/estadistica/calculadora-estadistica-descriptiva/",
 "/calculadoras/fisica/cinematica-mru-mrua/",
 "/calculadoras/quimica/calculadora-de-ph/",
 "/calculadoras/ingenieria/conversor-de-unidades/",
 "/calculadoras/finanzas/interes-compuesto/",
 "/calculadoras/estadistica/permutaciones-y-combinaciones/",
 "/calculadoras/fisica/ley-de-ohm/",
 "/calculadoras/quimica/calculadora-de-molaridad/",
 "/calculadoras/ingenieria/resistencias-serie-paralelo/",
 "/calculadoras/finanzas/amortizacion-prestamos/",
 "/calculadoras/estadistica/distribucion-normal/",
 "/calculadoras/fisica/segunda-ley-de-newton/",
 "/calculadoras/quimica/calculadora-de-diluciones/",
 "/calculadoras/ingenieria/ley-de-hooke/",
 "/calculadoras/finanzas/calculadora-de-porcentajes/",
 "/calculadoras/finanzas/calculadora-de-iva/",
 "/calculadoras/quimica/calculadora-de-masa-molar/",
 "/calculadoras/estadistica/calculadora-de-promedio-de-notas/",
 "/calculadoras/matematicas-avanzadas/regla-de-tres/",
 "/calculadoras/finanzas/calculadora-de-interes-simple/",
 "/calculadoras/matematicas-avanzadas/mcd-y-mcm/",
 "/calculadoras/matematicas-avanzadas/calculadora-de-fracciones/",
 "/calculadoras/matematicas-avanzadas/teorema-de-pitagoras/",
 "/calculadoras/matematicas-avanzadas/conversor-de-bases-numericas/",
 "/calculadoras/finanzas/calculadora-de-aguinaldo/",
 "/calculadoras/quimica/calculadora-de-gases-ideales/",
 "/calculadoras/quimica/calculadora-de-moles/",
 "/calculadoras/finanzas/calculadora-de-plazo-fijo/",
 "/calculadoras/matematicas-avanzadas/calculadora-de-areas-y-volumenes/",
 "/calculadoras/fisica/energia-cinetica-y-potencial/",
 "/calculadoras/estadistica/regresion-lineal/",
 "/calculadoras/ingenieria/conversor-de-temperatura/",
 "/guias/",
 "/guias/orden-de-operaciones-vs-calculo-secuencial/",
 "/guias/como-resolver-ecuaciones-de-segundo-grado/",
 "/guias/determinante-y-matriz-inversa/",
 "/guias/como-calcular-desviacion-estandar/",
 "/guias/ley-de-ohm-explicada/",
 "/guias/como-calcular-ph-y-poh/",
 "/guias/resistencias-serie-vs-paralelo/",
 "/guias/interes-simple-vs-compuesto/",
 "/guias/grados-y-radianes/",
 "/guias/permutaciones-vs-combinaciones/",
 "/guias/formulas-de-mru-y-mrua/",
 "/guias/como-calcular-molaridad/",
 "/guias/conversion-de-unidades-de-presion/",
 "/guias/como-calcular-cuota-de-prestamo/",
 "/guias/puntaje-z-y-curva-normal/",
 "/guias/segunda-ley-de-newton-explicada/",
 "/guias/como-hacer-una-dilucion/",
 "/guias/ley-de-hooke-y-elasticidad/",
 "/guias/como-calcular-porcentajes/",
 "/guias/como-calcular-iva/",
 "/guias/como-calcular-masa-molar/",
 "/guias/como-calcular-promedio-de-notas/",
 "/guias/regla-de-tres-simple-y-compuesta/",
 "/guias/como-calcular-mcd-y-mcm/",
 "/guias/como-operar-con-fracciones/",
 "/guias/teorema-de-pitagoras-explicado/",
 "/guias/como-calcular-el-aguinaldo/",
 "/guias/ley-de-los-gases-ideales/",
 "/guias/como-convertir-binario-decimal-y-hexadecimal/",
 "/guias/como-calcular-moles/",
 "/guias/como-calcular-un-plazo-fijo-tna-y-tea/",
 "/guias/como-calcular-areas-y-volumenes/",
 "/guias/energia-cinetica-y-potencial-explicada/",
 "/guias/regresion-lineal-y-correlacion/",
 "/guias/conversion-de-temperatura-celsius-fahrenheit-kelvin/",
 "/sobre-nosotros/",
 "/privacidad/",
 "/terminos-de-uso/",
 "/404.html",
 "/manifest.webmanifest",
 "/assets/css/styles.css",
 "/assets/css/tailwind.css",
 "/assets/img/apple-touch-icon.png",
 "/assets/img/favicon-32.png",
 "/assets/img/favicon.svg",
 "/assets/img/pwa-192.png",
 "/assets/img/pwa-512.png",
 "/assets/js/ads.js",
 "/assets/js/back-to-top.js",
 "/assets/js/calculators-data.js",
 "/assets/js/category.js",
 "/assets/js/copy-result.js",
 "/assets/js/main.js",
 "/assets/js/pwa.js",
 "/assets/js/theme.js",
 "/calculadoras/estadistica/calculadora-de-promedio-de-notas/script.js",
 "/calculadoras/estadistica/calculadora-estadistica-descriptiva/script.js",
 "/calculadoras/estadistica/distribucion-normal/script.js",
 "/calculadoras/estadistica/permutaciones-y-combinaciones/script.js",
 "/calculadoras/estadistica/regresion-lineal/script.js",
 "/calculadoras/finanzas/amortizacion-prestamos/script.js",
 "/calculadoras/finanzas/calculadora-de-aguinaldo/script.js",
 "/calculadoras/finanzas/calculadora-de-interes-simple/script.js",
 "/calculadoras/finanzas/calculadora-de-iva/script.js",
 "/calculadoras/finanzas/calculadora-de-plazo-fijo/script.js",
 "/calculadoras/finanzas/calculadora-de-porcentajes/script.js",
 "/calculadoras/finanzas/interes-compuesto/script.js",
 "/calculadoras/fisica/cinematica-mru-mrua/script.js",
 "/calculadoras/fisica/energia-cinetica-y-potencial/script.js",
 "/calculadoras/fisica/ley-de-ohm/script.js",
 "/calculadoras/fisica/segunda-ley-de-newton/script.js",
 "/calculadoras/ingenieria/conversor-de-temperatura/script.js",
 "/calculadoras/ingenieria/conversor-de-unidades/script.js",
 "/calculadoras/ingenieria/ley-de-hooke/script.js",
 "/calculadoras/ingenieria/resistencias-serie-paralelo/script.js",
 "/calculadoras/matematicas-avanzadas/calculadora-basica/script.js",
 "/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/script.js",
 "/calculadoras/matematicas-avanzadas/calculadora-de-areas-y-volumenes/script.js",
 "/calculadoras/matematicas-avanzadas/calculadora-de-fracciones/script.js",
 "/calculadoras/matematicas-avanzadas/calculadora-matrices/script.js",
 "/calculadoras/matematicas-avanzadas/conversor-de-bases-numericas/script.js",
 "/calculadoras/matematicas-avanzadas/ecuaciones-segundo-grado/script.js",
 "/calculadoras/matematicas-avanzadas/mcd-y-mcm/script.js",
 "/calculadoras/matematicas-avanzadas/regla-de-tres/script.js",
 "/calculadoras/matematicas-avanzadas/teorema-de-pitagoras/script.js",
 "/calculadoras/quimica/calculadora-de-diluciones/script.js",
 "/calculadoras/quimica/calculadora-de-gases-ideales/script.js",
 "/calculadoras/quimica/calculadora-de-masa-molar/script.js",
 "/calculadoras/quimica/calculadora-de-molaridad/script.js",
 "/calculadoras/quimica/calculadora-de-moles/script.js",
 "/calculadoras/quimica/calculadora-de-ph/script.js"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) =>
      // addAll falla entero si una URL falla: las pedimos una a una y toleramos errores sueltos.
      Promise.all(PRECACHE.map((url) => cache.add(new Request(url, { cache: "reload" })).catch(() => null)))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith("cc-") && k !== CACHE && k !== FONTS).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  if (url.origin === "https://fonts.googleapis.com" || url.origin === "https://fonts.gstatic.com") {
    event.respondWith(
      caches.open(FONTS).then((cache) =>
        cache.match(req).then((hit) => {
          const net = fetch(req).then((res) => { if (res.ok || res.type === "opaque") cache.put(req, res.clone()); return res; }).catch(() => hit);
          return hit || net;
        })
      )
    );
    return;
  }

  if (url.origin !== self.location.origin) return;
  if (url.pathname === "/sw.js") return;

  event.respondWith(
    fetch(req)
      .then((res) => {
        if (res.ok && res.type === "basic") {
          const copy = res.clone();
          caches.open(CACHE).then((cache) => cache.put(req, copy));
        }
        return res;
      })
      .catch(() =>
        caches.match(req, { ignoreSearch: true }).then((hit) => {
          if (hit) return hit;
          if (req.mode === "navigate") return caches.match("/", { ignoreSearch: true });
          return Response.error();
        })
      )
  );
});
