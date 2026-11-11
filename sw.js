/* sw.js — GENERADO por scripts/build-sw.py (no editar a mano: editar sw-template.js).
 * Estrategia: precarga del sitio (páginas + CSS + JS) para que funcione sin conexión;
 * red primero con respaldo en caché; tipografías de Google en caché "stale-while-revalidate".
 * No intercepta anuncios, analítica ni nada de otros orígenes (salvo las tipografías). */
const VERSION = "0621cd497c";
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
 "/calculadoras/vida-diaria/",
 "/calculadoras/vida-diaria/calculadora-de-edad-y-fechas/",
 "/calculadoras/vida-diaria/calculadora-de-imc/",
 "/calculadoras/vida-diaria/conversor-de-cocina/",
 "/calculadoras/vida-diaria/calculadora-de-horas-trabajadas/",
 "/calculadoras/vida-diaria/calculadora-de-propina/",
 "/calculadoras/hogar-y-construccion/",
 "/calculadoras/finanzas/cuotas-vs-contado/",
 "/calculadoras/finanzas/calculadora-de-inflacion-acumulada/",
 "/calculadoras/finanzas/calculadora-de-ajuste-de-alquiler/",
 "/calculadoras/finanzas/calculadora-de-margen-y-markup/",
 "/calculadoras/finanzas/descuentos-sucesivos/",
 "/calculadoras/hogar-y-construccion/calculadora-de-ceramicos/",
 "/calculadoras/hogar-y-construccion/calculadora-de-pintura/",
 "/calculadoras/hogar-y-construccion/calculadora-de-ladrillos/",
 "/calculadoras/hogar-y-construccion/calculadora-de-hormigon/",
 "/calculadoras/hogar-y-construccion/calculadora-de-consumo-electrico/",
 "/calculadoras/matematicas-avanzadas/sistemas-de-ecuaciones/",
 "/calculadoras/matematicas-avanzadas/numeros-primos/",
 "/calculadoras/matematicas-avanzadas/progresiones-aritmeticas-y-geometricas/",
 "/calculadoras/matematicas-avanzadas/resolucion-de-triangulos/",
 "/calculadoras/matematicas-avanzadas/conversor-de-numeros-romanos/",
 "/calculadoras/estadistica/distribucion-binomial/",
 "/calculadoras/estadistica/intervalo-de-confianza/",
 "/calculadoras/estadistica/tamano-de-muestra/",
 "/calculadoras/fisica/caida-libre-y-tiro-oblicuo/",
 "/calculadoras/fisica/trabajo-y-potencia/",
 "/calculadoras/quimica/estequiometria-y-reactivo-limitante/",
 "/calculadoras/quimica/balanceo-de-ecuaciones-quimicas/",
 "/calculadoras/ingenieria/codigo-de-colores-de-resistencias/",
 "/calculadoras/ingenieria/divisor-de-tension/",
 "/calculadoras/ingenieria/resistencia-para-led/",
 "/calculadoras/matematicas-avanzadas/graficador-de-funciones/",
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
 "/guias/como-calcular-la-edad-y-los-dias-entre-fechas/",
 "/guias/como-calcular-el-imc/",
 "/guias/equivalencias-de-cocina-tazas-cucharadas-y-gramos/",
 "/guias/como-calcular-horas-trabajadas-y-horas-extra/",
 "/guias/como-calcular-la-propina-y-dividir-la-cuenta/",
 "/guias/cuotas-o-contado-como-saber-cual-conviene/",
 "/guias/como-calcular-la-inflacion-acumulada/",
 "/guias/como-calcular-el-ajuste-de-un-alquiler/",
 "/guias/diferencia-entre-margen-y-markup/",
 "/guias/como-calcular-descuentos-sucesivos/",
 "/guias/cuantos-ceramicos-necesito/",
 "/guias/cuanta-pintura-necesito/",
 "/guias/cuantos-ladrillos-necesito-por-m2/",
 "/guias/como-calcular-el-hormigon-de-una-losa/",
 "/guias/como-calcular-el-consumo-electrico/",
 "/guias/como-resolver-sistemas-de-ecuaciones/",
 "/guias/como-saber-si-un-numero-es-primo/",
 "/guias/progresiones-aritmeticas-y-geometricas/",
 "/guias/teorema-del-seno-y-del-coseno/",
 "/guias/como-leer-y-escribir-numeros-romanos/",
 "/guias/distribucion-binomial-explicada/",
 "/guias/intervalo-de-confianza-explicado/",
 "/guias/como-calcular-el-tamano-de-una-muestra/",
 "/guias/caida-libre-y-tiro-oblicuo-explicados/",
 "/guias/trabajo-y-potencia-mecanica/",
 "/guias/estequiometria-y-reactivo-limitante-paso-a-paso/",
 "/guias/como-balancear-ecuaciones-quimicas/",
 "/guias/como-leer-el-codigo-de-colores-de-resistencias/",
 "/guias/como-funciona-un-divisor-de-tension/",
 "/guias/que-resistencia-poner-a-un-led/",
 "/guias/como-graficar-una-funcion/",
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
 "/assets/js/calc-simple.js",
 "/assets/js/calculators-data.js",
 "/assets/js/category.js",
 "/assets/js/copy-result.js",
 "/assets/js/main.js",
 "/assets/js/pwa.js",
 "/assets/js/theme.js",
 "/calculadoras/estadistica/calculadora-de-promedio-de-notas/script.js",
 "/calculadoras/estadistica/calculadora-estadistica-descriptiva/script.js",
 "/calculadoras/estadistica/distribucion-binomial/script.js",
 "/calculadoras/estadistica/distribucion-normal/script.js",
 "/calculadoras/estadistica/intervalo-de-confianza/script.js",
 "/calculadoras/estadistica/permutaciones-y-combinaciones/script.js",
 "/calculadoras/estadistica/regresion-lineal/script.js",
 "/calculadoras/estadistica/tamano-de-muestra/script.js",
 "/calculadoras/finanzas/amortizacion-prestamos/script.js",
 "/calculadoras/finanzas/calculadora-de-aguinaldo/script.js",
 "/calculadoras/finanzas/calculadora-de-ajuste-de-alquiler/script.js",
 "/calculadoras/finanzas/calculadora-de-inflacion-acumulada/script.js",
 "/calculadoras/finanzas/calculadora-de-interes-simple/script.js",
 "/calculadoras/finanzas/calculadora-de-iva/script.js",
 "/calculadoras/finanzas/calculadora-de-margen-y-markup/script.js",
 "/calculadoras/finanzas/calculadora-de-plazo-fijo/script.js",
 "/calculadoras/finanzas/calculadora-de-porcentajes/script.js",
 "/calculadoras/finanzas/cuotas-vs-contado/script.js",
 "/calculadoras/finanzas/descuentos-sucesivos/script.js",
 "/calculadoras/finanzas/interes-compuesto/script.js",
 "/calculadoras/fisica/caida-libre-y-tiro-oblicuo/script.js",
 "/calculadoras/fisica/cinematica-mru-mrua/script.js",
 "/calculadoras/fisica/energia-cinetica-y-potencial/script.js",
 "/calculadoras/fisica/ley-de-ohm/script.js",
 "/calculadoras/fisica/segunda-ley-de-newton/script.js",
 "/calculadoras/fisica/trabajo-y-potencia/script.js",
 "/calculadoras/hogar-y-construccion/calculadora-de-ceramicos/script.js",
 "/calculadoras/hogar-y-construccion/calculadora-de-consumo-electrico/script.js",
 "/calculadoras/hogar-y-construccion/calculadora-de-hormigon/script.js",
 "/calculadoras/hogar-y-construccion/calculadora-de-ladrillos/script.js",
 "/calculadoras/hogar-y-construccion/calculadora-de-pintura/script.js",
 "/calculadoras/ingenieria/codigo-de-colores-de-resistencias/script.js",
 "/calculadoras/ingenieria/conversor-de-temperatura/script.js",
 "/calculadoras/ingenieria/conversor-de-unidades/script.js",
 "/calculadoras/ingenieria/divisor-de-tension/script.js",
 "/calculadoras/ingenieria/ley-de-hooke/script.js",
 "/calculadoras/ingenieria/resistencia-para-led/script.js",
 "/calculadoras/ingenieria/resistencias-serie-paralelo/script.js",
 "/calculadoras/matematicas-avanzadas/calculadora-basica/script.js",
 "/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/script.js",
 "/calculadoras/matematicas-avanzadas/calculadora-de-areas-y-volumenes/script.js",
 "/calculadoras/matematicas-avanzadas/calculadora-de-fracciones/script.js",
 "/calculadoras/matematicas-avanzadas/calculadora-matrices/script.js",
 "/calculadoras/matematicas-avanzadas/conversor-de-bases-numericas/script.js",
 "/calculadoras/matematicas-avanzadas/conversor-de-numeros-romanos/script.js",
 "/calculadoras/matematicas-avanzadas/ecuaciones-segundo-grado/script.js",
 "/calculadoras/matematicas-avanzadas/graficador-de-funciones/script.js",
 "/calculadoras/matematicas-avanzadas/mcd-y-mcm/script.js",
 "/calculadoras/matematicas-avanzadas/numeros-primos/script.js",
 "/calculadoras/matematicas-avanzadas/progresiones-aritmeticas-y-geometricas/script.js",
 "/calculadoras/matematicas-avanzadas/regla-de-tres/script.js",
 "/calculadoras/matematicas-avanzadas/resolucion-de-triangulos/script.js",
 "/calculadoras/matematicas-avanzadas/sistemas-de-ecuaciones/script.js",
 "/calculadoras/matematicas-avanzadas/teorema-de-pitagoras/script.js",
 "/calculadoras/quimica/balanceo-de-ecuaciones-quimicas/script.js",
 "/calculadoras/quimica/calculadora-de-diluciones/script.js",
 "/calculadoras/quimica/calculadora-de-gases-ideales/script.js",
 "/calculadoras/quimica/calculadora-de-masa-molar/script.js",
 "/calculadoras/quimica/calculadora-de-molaridad/script.js",
 "/calculadoras/quimica/calculadora-de-moles/script.js",
 "/calculadoras/quimica/calculadora-de-ph/script.js",
 "/calculadoras/quimica/estequiometria-y-reactivo-limitante/script.js",
 "/calculadoras/vida-diaria/calculadora-de-edad-y-fechas/script.js",
 "/calculadoras/vida-diaria/calculadora-de-horas-trabajadas/script.js",
 "/calculadoras/vida-diaria/calculadora-de-imc/script.js",
 "/calculadoras/vida-diaria/calculadora-de-propina/script.js",
 "/calculadoras/vida-diaria/conversor-de-cocina/script.js"
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
