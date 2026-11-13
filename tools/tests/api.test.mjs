/**
 * Pruebas de la API de cuentas (server-lib/api.mjs) con SQLite en memoria (node:sqlite) en lugar de D1,
 * un Resend simulado y un ID token de Google firmado con una clave RSA generada en la prueba.
 * Uso:  node --test tools/tests/api.test.mjs
 */
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { handle } from "../../server-lib/api.mjs";
import { resetGoogleKeyCache } from "../../server-lib/google.mjs";
import { b64url } from "../../server-lib/util.mjs";

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const MIGRATION = readFileSync(path.join(root, "migrations", "0001_cuentas.sql"), "utf8");
const ORIGIN = "https://www.calculadoracientifica.com.ar";
const CLIENT_ID = "123-test.apps.googleusercontent.com";

function makeDb() {
  const s = new DatabaseSync(":memory:");
  s.exec(MIGRATION);
  return {
    prepare(sql) {
      const st = s.prepare(sql);
      let args = [];
      const o = {
        bind: (...a) => ((args = a), o),
        first: async () => st.get(...args) ?? null,
        all: async () => ({ results: st.all(...args) }),
        run: async () => ({ meta: { changes: st.run(...args).changes } }),
      };
      return o;
    },
  };
}

async function makeGoogle() {
  const pair = await crypto.subtle.generateKey({ name: "RSASSA-PKCS1-v1_5", modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: "SHA-256" }, true, ["sign", "verify"]);
  const jwk = { ...(await crypto.subtle.exportKey("jwk", pair.publicKey)), kid: "k1", alg: "RS256", use: "sig" };
  const enc = (o) => b64url(new TextEncoder().encode(JSON.stringify(o)));
  return {
    jwks: { keys: [jwk] },
    async token(claims = {}, { kid = "k1", signKey = pair.privateKey } = {}) {
      const head = enc({ alg: "RS256", kid, typ: "JWT" });
      const body = enc({ iss: "https://accounts.google.com", aud: CLIENT_ID, sub: "g-1", email: "ana@gmail.com", email_verified: true, name: "Ana", exp: Math.floor(Date.now() / 1000) + 600, ...claims });
      const sig = await crypto.subtle.sign("RSASSA-PKCS1-v1_5", signKey, new TextEncoder().encode(`${head}.${body}`));
      return `${head}.${body}.${b64url(new Uint8Array(sig))}`;
    },
  };
}

async function setup(envOverrides = {}) {
  resetGoogleKeyCache();
  const google = await makeGoogle();
  const mails = [];
  const env = { DB: makeDb(), GOOGLE_CLIENT_ID: CLIENT_ID, RESEND_API_KEY: "re_test", ...envOverrides };
  let clock = Date.parse("2026-11-12T12:00:00Z");
  const deps = {
    iterations: 1000,
    now: () => clock,
    fetch: async (url, init) => {
      if (String(url).includes("googleapis.com")) return new Response(JSON.stringify(google.jwks), { status: 200 });
      if (String(url).includes("resend.com")) {
        mails.push(JSON.parse(init.body));
        return new Response("{}", { status: 200 });
      }
      throw new Error("fetch inesperado " + url);
    },
  };
  let cookie = "";
  const call = async (method, p, body, { origin = ORIGIN, keepCookie = true, ip = "1.1.1.1" } = {}) => {
    const headers = { "Content-Type": "application/json", "CF-Connecting-IP": ip };
    if (origin) headers.Origin = origin;
    if (cookie && keepCookie) headers.Cookie = cookie;
    const res = await handle(new Request(ORIGIN + "/api/" + p, { method, headers, body: body === undefined ? undefined : JSON.stringify(body) }), env, deps);
    const set = res.headers.get("Set-Cookie");
    if (set) cookie = set.startsWith("cc_session=;") || /Max-Age=0/.test(set) ? "" : set.split(";")[0];
    return { status: res.status, body: await res.json().catch(() => null), headers: res.headers };
  };
  const tokenFromMail = (n = mails.length - 1) => /[?&](?:verificar|restablecer)=([A-Za-z0-9_-]+)/.exec(mails[n].text)[1];
  return { env, call, google, mails, tokenFromMail, tick: (ms) => (clock += ms), clearCookie: () => (cookie = "") };
}

test("config: sin base de datos las cuentas están deshabilitadas; con base, informa qué hay", async () => {
  const off = await setup({ DB: undefined });
  assert.deepEqual((await off.call("GET", "config")).body.enabled, false);
  assert.equal((await off.call("POST", "auth/login", { email: "a@b.co", password: "x" })).status, 503);
  const on = await setup();
  const c = (await on.call("GET", "config")).body;
  assert.deepEqual([c.enabled, c.google, c.email], [true, CLIENT_ID, true]);
});

test("registro con mail: exige términos, verifica el mail, y la sesión funciona", async () => {
  const t = await setup();
  assert.equal((await t.call("POST", "auth/register", { email: "ana@mail.com", password: "clave-larga-1" })).body.error, "terms_required");
  assert.equal((await t.call("POST", "auth/register", { email: "ana@mail.com", password: "corta", acceptTerms: true })).body.error, "password_short");
  assert.equal((await t.call("POST", "auth/register", { email: "no-es-mail", password: "clave-larga-1", acceptTerms: true })).body.error, "email_invalid");
  const r = await t.call("POST", "auth/register", { email: "Ana@Mail.com", password: "clave-larga-1", acceptTerms: true });
  assert.equal(r.status, 200);
  assert.equal(r.body.user.email, "ana@mail.com");
  assert.equal(r.body.user.emailVerified, false);
  assert.match(r.headers.get("Set-Cookie"), /HttpOnly; Secure; SameSite=Lax/);
  assert.equal(t.mails.length, 1);
  assert.equal(t.mails[0].to[0], "ana@mail.com");
  assert.equal((await t.call("GET", "me")).body.user.email, "ana@mail.com");
  // sin verificar no se puede sincronizar
  assert.equal((await t.call("GET", "sync")).status, 403);
  assert.equal((await t.call("POST", "auth/verify", { token: "inventado" })).body.error, "token_invalid");
  assert.equal((await t.call("POST", "auth/verify", { token: t.tokenFromMail() })).status, 200);
  assert.equal((await t.call("POST", "auth/verify", { token: t.tokenFromMail() })).status, 400); // un solo uso
  assert.equal((await t.call("GET", "me")).body.user.emailVerified, true);
  assert.equal((await t.call("GET", "sync")).status, 200);
  // mail repetido
  assert.equal((await t.call("POST", "auth/register", { email: "ana@mail.com", password: "otra-clave-9", acceptTerms: true }, { ip: "2.2.2.2" })).body.error, "email_taken");
});

test("el registro con mail se deshabilita si no hay servicio de mail", async () => {
  const t = await setup({ RESEND_API_KEY: undefined });
  assert.equal((await t.call("POST", "auth/register", { email: "ana@mail.com", password: "clave-larga-1", acceptTerms: true })).body.error, "email_disabled");
});

test("login: credenciales, cierre de sesión y límite de intentos", async () => {
  const t = await setup();
  await t.call("POST", "auth/register", { email: "ana@mail.com", password: "clave-larga-1", acceptTerms: true });
  await t.call("POST", "auth/logout", {});
  assert.equal((await t.call("GET", "me")).body.user, null);
  assert.equal((await t.call("POST", "auth/login", { email: "ana@mail.com", password: "mala-clave-1" })).status, 401);
  assert.equal((await t.call("POST", "auth/login", { email: "nadie@mail.com", password: "clave-larga-1" })).status, 401);
  assert.equal((await t.call("POST", "auth/login", { email: "ana@mail.com", password: "clave-larga-1" })).status, 200);
  assert.equal((await t.call("GET", "me")).body.user.email, "ana@mail.com");
  // fuerza bruta sobre un mismo mail: se bloquea aunque cambie la IP
  let last;
  for (let i = 0; i < 10; i++) last = await t.call("POST", "auth/login", { email: "ana@mail.com", password: "mala-clave-1" }, { ip: "9.9.9." + i });
  assert.equal(last.status, 429);
});

test("protección CSRF: sin Origin del propio sitio no se aceptan modificaciones", async () => {
  const t = await setup();
  assert.equal((await t.call("POST", "auth/logout", {}, { origin: null })).status, 403);
  assert.equal((await t.call("POST", "auth/logout", {}, { origin: "https://sitio-malo.com" })).status, 403);
  assert.equal((await t.call("POST", "auth/logout", {})).status, 200);
});

test("Google: cuenta nueva pide términos; después entra; token falso o ajeno se rechaza", async () => {
  const t = await setup();
  const ok = await t.google.token();
  assert.equal((await t.call("POST", "auth/google", { credential: ok })).body.error, "terms_required");
  const r = await t.call("POST", "auth/google", { credential: ok, acceptTerms: true });
  assert.equal(r.status, 200);
  assert.equal(r.body.user.email, "ana@gmail.com");
  assert.equal(r.body.user.emailVerified, true);
  assert.equal(r.body.user.hasGoogle, true);
  t.clearCookie();
  assert.equal((await t.call("POST", "auth/google", { credential: ok })).status, 200); // ya no pide términos
  assert.equal((await t.call("POST", "auth/google", { credential: await t.google.token({ aud: "otro-sitio" }) })).status, 401);
  assert.equal((await t.call("POST", "auth/google", { credential: await t.google.token({ exp: 1 }) })).status, 401);
  assert.equal((await t.call("POST", "auth/google", { credential: await t.google.token({ email_verified: false }) })).status, 401);
  assert.equal((await t.call("POST", "auth/google", { credential: await t.google.token({}, { kid: "desconocida" }) })).status, 401);
  const other = await crypto.subtle.generateKey({ name: "RSASSA-PKCS1-v1_5", modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: "SHA-256" }, true, ["sign", "verify"]);
  assert.equal((await t.call("POST", "auth/google", { credential: await t.google.token({}, { signKey: other.privateKey }) })).status, 401); // firma ajena
});

test("Google sobre un mail registrado y sin verificar: toma la cuenta y descarta la contraseña del impostor", async () => {
  const t = await setup();
  await t.call("POST", "auth/register", { email: "ana@gmail.com", password: "clave-del-impostor", acceptTerms: true });
  t.clearCookie();
  const r = await t.call("POST", "auth/google", { credential: await t.google.token() });
  assert.equal(r.status, 200);
  assert.equal(r.body.user.hasPassword, false);
  assert.equal(r.body.user.emailVerified, true);
  t.clearCookie();
  assert.equal((await t.call("POST", "auth/login", { email: "ana@gmail.com", password: "clave-del-impostor" })).status, 401);
});

test("restablecer contraseña: vale una vez, cierra las sesiones y no revela si el mail existe", async () => {
  const t = await setup();
  await t.call("POST", "auth/register", { email: "ana@mail.com", password: "clave-larga-1", acceptTerms: true });
  const before = t.mails.length;
  assert.equal((await t.call("POST", "auth/forgot", { email: "nadie@mail.com" })).status, 200);
  assert.equal(t.mails.length, before); // no se envió nada
  assert.equal((await t.call("POST", "auth/forgot", { email: "ana@mail.com" })).status, 200);
  const token = t.tokenFromMail();
  assert.equal((await t.call("POST", "auth/reset", { token, password: "corta" })).status, 400);
  assert.equal((await t.call("POST", "auth/reset", { token, password: "clave-nueva-77" })).status, 200);
  assert.equal((await t.call("POST", "auth/reset", { token, password: "clave-nueva-88" })).status, 400);
  assert.equal((await t.call("GET", "me")).body.user, null); // sesión cerrada
  assert.equal((await t.call("POST", "auth/login", { email: "ana@mail.com", password: "clave-nueva-77" })).status, 200);
  const stale = await t.call("POST", "auth/reset", { token: "x".repeat(40), password: "clave-nueva-99" });
  assert.equal(stale.status, 400);
});

test("sincronización: valida claves, gana el dato más nuevo y respeta límites", async () => {
  const t = await setup();
  await t.call("POST", "auth/google", { credential: await t.google.token(), acceptTerms: true });
  const now = Date.parse("2026-11-12T12:00:00Z");
  const put = await t.call("PUT", "sync", { data: { favs: { v: '[{"u":"/a/","t":"A"}]', t: now }, "hist:/calculadoras/x/y/": { v: "[1]", t: now }, "clave-no-permitida": { v: "x", t: now }, prefs: { v: "x".repeat(30000), t: now } } });
  assert.deepEqual(Object.keys(put.body.data).sort(), ["favs", "hist:/calculadoras/x/y/"]);
  // un dato más viejo no pisa al más nuevo
  const old = await t.call("PUT", "sync", { data: { favs: { v: "[]", t: now - 5000 } } });
  assert.equal(old.body.data.favs.v, '[{"u":"/a/","t":"A"}]');
  const newer = await t.call("PUT", "sync", { data: { favs: { v: "[]", t: now + 1000 } } });
  assert.equal(newer.body.data.favs.v, "[]");
  assert.equal((await t.call("GET", "sync")).body.data["hist:/calculadoras/x/y/"].v, "[1]");
  // sin sesión no hay acceso
  t.clearCookie();
  assert.equal((await t.call("GET", "sync")).status, 401);
});

test("exportar y eliminar la cuenta borra todo", async () => {
  const t = await setup();
  await t.call("POST", "auth/google", { credential: await t.google.token(), acceptTerms: true });
  await t.call("PUT", "sync", { data: { favs: { v: "[1]", t: Date.parse("2026-11-12T12:00:00Z") } } });
  const ex = await t.call("GET", "me/export");
  assert.equal(ex.body.user.email, "ana@gmail.com");
  assert.equal(ex.body.acceptances[0].via, "google");
  assert.equal(ex.body.data.favs.value, "[1]");
  assert.equal((await t.call("POST", "me/delete", { confirm: "no" })).status, 400);
  assert.equal((await t.call("POST", "me/delete", { confirm: "ELIMINAR" })).status, 200);
  assert.equal((await t.call("GET", "me")).body.user, null);
  for (const tbl of ["users", "user_data", "sessions", "terms_acceptances"]) {
    const n = await t.env.DB.prepare(`SELECT COUNT(*) AS n FROM ${tbl}`).bind().first();
    assert.equal(n.n, 0, tbl);
  }
});

test("nueva versión de los términos: se detecta y se reacepta", async () => {
  const t = await setup();
  await t.call("POST", "auth/google", { credential: await t.google.token(), acceptTerms: true });
  await t.env.DB.prepare("UPDATE users SET terms_version = '2020-01-01'").bind().run();
  assert.equal((await t.call("GET", "me")).body.user.needsTerms, true);
  assert.equal((await t.call("POST", "me/accept-terms", { accept: false })).status, 400);
  assert.equal((await t.call("POST", "me/accept-terms", { accept: true })).body.user.needsTerms, false);
});
