/**
 * util.mjs — Utilidades del backend de cuentas (funcionan en Cloudflare Workers y en Node ≥ 20).
 */
export const TERMS_VERSION = "2026-11-12"; // cambiar al modificar Términos o Privacidad: se vuelve a pedir la aceptación
export const SESSION_DAYS = 30;
export const PBKDF2_ITERATIONS = 100000; // máximo permitido por WebCrypto en Cloudflare Workers

const enc = new TextEncoder();

export function b64url(bytes) {
  let s = "";
  bytes.forEach((b) => (s += String.fromCharCode(b)));
  return btoa(s).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
export function b64urlToBytes(str) {
  const s = str.replace(/-/g, "+").replace(/_/g, "/") + "=".repeat((4 - (str.length % 4)) % 4);
  const bin = atob(s);
  return Uint8Array.from(bin, (c) => c.charCodeAt(0));
}

export function randomToken(bytes = 32) {
  return b64url(crypto.getRandomValues(new Uint8Array(bytes)));
}

export async function sha256Hex(text) {
  const buf = await crypto.subtle.digest("SHA-256", enc.encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a[i] ^ b[i];
  return diff === 0;
}

async function derive(password, salt, iterations) {
  const key = await crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt, iterations }, key, 256);
  return new Uint8Array(bits);
}

/** Devuelve "pbkdf2$iteraciones$sal$hash" (sal y hash en base64url). */
export async function hashPassword(password, iterations = PBKDF2_ITERATIONS) {
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const hash = await derive(password, salt, iterations);
  return `pbkdf2$${iterations}$${b64url(salt)}$${b64url(hash)}`;
}

export async function verifyPassword(password, stored) {
  const [scheme, it, salt, hash] = String(stored || "").split("$");
  if (scheme !== "pbkdf2" || !it || !salt || !hash) return false;
  const derived = await derive(password, b64urlToBytes(salt), Number(it));
  return timingSafeEqual(derived, b64urlToBytes(hash));
}

export function json(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...headers },
  });
}

export class ApiError extends Error {
  constructor(status, code, message) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

export function parseCookies(header) {
  const out = {};
  String(header || "")
    .split(/;\s*/)
    .forEach((part) => {
      const i = part.indexOf("=");
      if (i > 0) out[part.slice(0, i)] = decodeURIComponent(part.slice(i + 1));
    });
  return out;
}

export function sessionCookie(token, maxAgeSeconds) {
  return `cc_session=${token}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${maxAgeSeconds}`;
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
export function normalizeEmail(value) {
  const e = String(value || "").trim().toLowerCase();
  if (!EMAIL_RE.test(e) || e.length > 254) throw new ApiError(400, "email_invalid", "Escribí un mail válido.");
  return e;
}

export function checkPassword(password, email) {
  const p = String(password || "");
  if (p.length < 8) throw new ApiError(400, "password_short", "La contraseña tiene que tener al menos 8 caracteres.");
  if (p.length > 200) throw new ApiError(400, "password_long", "La contraseña es demasiado larga.");
  if (email && p.toLowerCase() === email) throw new ApiError(400, "password_weak", "La contraseña no puede ser igual al mail.");
  return p;
}
