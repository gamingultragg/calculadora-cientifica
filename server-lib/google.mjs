/**
 * google.mjs — Verificación del ID token de "Acceder con Google" (Google Identity Services).
 * No hace falta ningún secreto: el token está firmado (RS256) con claves públicas de Google.
 */
import { b64urlToBytes } from "./util.mjs";

const CERTS_URL = "https://www.googleapis.com/oauth2/v3/certs";
let cache = { keys: null, exp: 0 };

async function getKeys(fetchImpl, now) {
  if (cache.keys && cache.exp > now) return cache.keys;
  const res = await fetchImpl(CERTS_URL);
  if (!res.ok) throw new Error("No se pudieron obtener las claves de Google.");
  const body = await res.json();
  cache = { keys: body.keys || [], exp: now + 60 * 60 * 1000 };
  return cache.keys;
}

export function resetGoogleKeyCache() {
  cache = { keys: null, exp: 0 };
}

/** Devuelve { sub, email, emailVerified, name } o lanza Error si el token no es válido. */
export async function verifyGoogleIdToken(idToken, clientId, { fetchImpl = fetch, now = Date.now() } = {}) {
  const parts = String(idToken || "").split(".");
  if (parts.length !== 3) throw new Error("Token con formato inválido.");
  const header = JSON.parse(new TextDecoder().decode(b64urlToBytes(parts[0])));
  const payload = JSON.parse(new TextDecoder().decode(b64urlToBytes(parts[1])));
  if (header.alg !== "RS256") throw new Error("Algoritmo no admitido.");

  const keys = await getKeys(fetchImpl, now);
  const jwk = keys.find((k) => k.kid === header.kid);
  if (!jwk) throw new Error("Clave de firma desconocida.");
  const key = await crypto.subtle.importKey("jwk", jwk, { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" }, false, ["verify"]);
  const ok = await crypto.subtle.verify("RSASSA-PKCS1-v1_5", key, b64urlToBytes(parts[2]), new TextEncoder().encode(`${parts[0]}.${parts[1]}`));
  if (!ok) throw new Error("Firma inválida.");

  if (!["https://accounts.google.com", "accounts.google.com"].includes(payload.iss)) throw new Error("Emisor inválido.");
  if (payload.aud !== clientId) throw new Error("El token no es para este sitio.");
  if (!(payload.exp * 1000 > now)) throw new Error("El token venció.");
  const verified = payload.email_verified === true || payload.email_verified === "true";
  if (!payload.sub || !payload.email || !verified) throw new Error("La cuenta de Google no tiene un mail verificado.");
  return { sub: String(payload.sub), email: String(payload.email).toLowerCase(), emailVerified: true, name: payload.name ? String(payload.name).slice(0, 120) : null };
}
