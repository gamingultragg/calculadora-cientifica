/**
 * _middleware.js — Redirección 301 del subdominio pages.dev al dominio
 * definitivo (.com.ar), para consolidar todo el tráfico y el SEO bajo un
 * único dominio canónico.
 *
 * Cloudflare Pages sirve el mismo proyecto en varios hosts a la vez
 * (calculadora-cientifica.pages.dev, calculadoracientifica.com.ar y
 * www.calculadoracientifica.com.ar). Sin este middleware, los tres
 * responden 200 con contenido idéntico — lo cual es exactamente lo que
 * necesita evitarse antes de usar la herramienta "Cambio de dirección"
 * de Google Search Console (pide redirecciones 301 reales del sitio
 * viejo al nuevo).
 *
 * Solo actúa sobre el host pages.dev; el resto de los hosts pasan sin
 * modificar (context.next()).
 */
const OLD_HOST = "calculadora-cientifica.pages.dev";
const NEW_HOST = "www.calculadoracientifica.com.ar";

export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.hostname === OLD_HOST) {
    url.hostname = NEW_HOST;
    url.protocol = "https:";
    return Response.redirect(url.toString(), 301);
  }

  return context.next();
}
