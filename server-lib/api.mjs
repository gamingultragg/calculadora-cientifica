/**
 * api.mjs — API de cuentas de Calculadora Científica (todo bajo /api/).
 * Pensada para Cloudflare Pages Functions + D1, y testeable en Node con SQLite en memoria.
 *
 *   GET  /api/config              qué está habilitado (Google, mail) y versión de los términos
 *   GET  /api/me                  usuario de la sesión (o null)
 *   POST /api/auth/register       mail + contraseña + aceptación de términos
 *   POST /api/auth/login          mail + contraseña
 *   POST /api/auth/google         ID token de Google (+ aceptación de términos si es cuenta nueva)
 *   POST /api/auth/logout
 *   POST /api/auth/verify         token del mail de verificación
 *   POST /api/auth/resend         reenvía el mail de verificación
 *   POST /api/auth/forgot         pide el mail para restablecer la contraseña
 *   POST /api/auth/reset          nueva contraseña con el token del mail
 *   POST /api/me/accept-terms     acepta una versión nueva de los términos
 *   GET  /api/me/export           descarga todos los datos de la cuenta
 *   POST /api/me/delete           elimina la cuenta y sus datos
 *   GET  /api/sync · PUT /api/sync   datos guardados (favoritas, historial, preferencias)
 */
import { verifyGoogleIdToken } from "./google.mjs";
import {
  ApiError, SESSION_DAYS, TERMS_VERSION, checkPassword, hashPassword, json, normalizeEmail, parseCookies, randomToken, sessionCookie, sha256Hex, verifyPassword,
} from "./util.mjs";

const DAY = 86400000;
const KEY_RE = /^(favs|prefs|sci-history|hist:[a-z0-9\/_-]{1,120})$/;
const MAX_VALUE = 20000;
const MAX_KEYS = 250;

// ------------------------------------------------------------------ helpers --
async function one(db, sql, ...args) {
  return db.prepare(sql).bind(...args).first();
}
async function run(db, sql, ...args) {
  return db.prepare(sql).bind(...args).run();
}
async function all(db, sql, ...args) {
  return (await db.prepare(sql).bind(...args).all()).results || [];
}

async function readBody(request) {
  try {
    const b = await request.json();
    return b && typeof b === "object" ? b : {};
  } catch {
    throw new ApiError(400, "bad_request", "La solicitud no es válida.");
  }
}

async function rateLimit(db, action, who, max, windowSec, now) {
  const k = `${action}:${(await sha256Hex(who)).slice(0, 20)}`;
  const reset = now + windowSec * 1000;
  const row = await one(
    db,
    `INSERT INTO rate_limits(k, n, reset_at) VALUES(?, 1, ?)
     ON CONFLICT(k) DO UPDATE SET n = CASE WHEN rate_limits.reset_at < ? THEN 1 ELSE rate_limits.n + 1 END,
                                  reset_at = CASE WHEN rate_limits.reset_at < ? THEN ? ELSE rate_limits.reset_at END
     RETURNING n`,
    k, reset, now, now, reset
  );
  if (row.n > max) throw new ApiError(429, "rate_limited", "Hiciste demasiados intentos. Esperá unos minutos y probá de nuevo.");
}

function publicUser(u) {
  return {
    id: u.id, email: u.email, name: u.name || null, emailVerified: !!u.email_verified, hasPassword: !!u.password_hash, hasGoogle: !!u.google_sub,
    termsVersion: u.terms_version, termsAcceptedAt: u.terms_accepted_at, needsTerms: u.terms_version !== TERMS_VERSION,
  };
}

async function createSession(db, userId, now) {
  const token = randomToken(32);
  await run(db, "INSERT INTO sessions(token_hash, user_id, created_at, expires_at) VALUES(?,?,?,?)", await sha256Hex(token), userId, now, now + SESSION_DAYS * DAY);
  await run(db, "UPDATE users SET last_login_at = ? WHERE id = ?", now, userId);
  // limpieza oportunista de sesiones y tokens vencidos
  await run(db, "DELETE FROM sessions WHERE expires_at < ?", now);
  await run(db, "DELETE FROM email_tokens WHERE expires_at < ?", now);
  return token;
}

async function sessionUser(request, db, now) {
  const token = parseCookies(request.headers.get("Cookie")).cc_session;
  if (!token) return null;
  return one(
    db,
    `SELECT u.* FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token_hash = ? AND s.expires_at > ?`,
    await sha256Hex(token), now
  );
}

async function requireUser(request, db, now) {
  const u = await sessionUser(request, db, now);
  if (!u) throw new ApiError(401, "unauthenticated", "Tenés que iniciar sesión.");
  return u;
}

function withSession(user, token, extra = {}) {
  return json({ user: publicUser(user), ...extra }, 200, { "Set-Cookie": sessionCookie(token, SESSION_DAYS * 86400) });
}

async function sendMail(env, deps, { to, subject, text }) {
  if (env.DEV_MAIL_LOG === "1") {
    console.log(`[MAIL de desarrollo] a ${to} — ${subject}
${text}`); // solo en pruebas locales: nunca se define en producción
    return;
  }
  const res = await (deps.fetch || fetch)("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: env.MAIL_FROM || "Calculadora Científica <contacto@calculadoracientifica.com.ar>",
      to: [to], subject, text,
      html: `<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.5;color:#0f172a">${text.split("\n").map((l) => `<p>${l.replace(/(https?:\/\/\S+)/g, '<a href="$1">$1</a>')}</p>`).join("")}</div>`,
    }),
  });
  if (!res.ok) throw new ApiError(502, "mail_failed", "No pudimos enviar el mail. Probá de nuevo en unos minutos.");
}

async function issueEmailToken(db, userId, kind, hours, now) {
  const token = randomToken(32);
  await run(db, "DELETE FROM email_tokens WHERE user_id = ? AND kind = ?", userId, kind);
  await run(db, "INSERT INTO email_tokens(token_hash, user_id, kind, expires_at) VALUES(?,?,?,?)", await sha256Hex(token), userId, kind, now + hours * 3600000);
  return token;
}

async function sendVerification(env, deps, db, user, siteUrl, now) {
  const token = await issueEmailToken(db, user.id, "verify", 24, now);
  await sendMail(env, deps, {
    to: user.email, subject: "Confirmá tu mail — Calculadora Científica",
    text: `Hola${user.name ? " " + user.name : ""}:\n\nPara activar tu cuenta de Calculadora Científica confirmá tu mail con este enlace (vale 24 horas):\n${siteUrl}/cuenta/?verificar=${token}\n\nSi no creaste una cuenta, ignorá este mensaje.`,
  });
}

// --------------------------------------------------------------------- rutas --
export async function handle(request, env, deps = {}) {
  const now = (deps.now || Date.now)();
  const url = new URL(request.url);
  const path = url.pathname.replace(/^\/api\/?/, "").replace(/\/+$/, "");
  const method = request.method.toUpperCase();
  const db = env.DB;
  const site = (env.SITE_URL || url.origin).replace(/\/+$/, "");

  try {
    if (path === "config" && method === "GET") {
      return json({ enabled: !!db, google: (db && env.GOOGLE_CLIENT_ID) || null, email: !!(db && env.RESEND_API_KEY), termsVersion: TERMS_VERSION });
    }
    if (!db) throw new ApiError(503, "disabled", "Las cuentas todavía no están habilitadas.");

    // Protección CSRF: las solicitudes que modifican datos tienen que venir de nuestro propio sitio.
    if (method !== "GET" && method !== "HEAD") {
      const origin = request.headers.get("Origin");
      if (!origin || new URL(origin).host !== url.host) throw new ApiError(403, "bad_origin", "Solicitud no permitida.");
    }
    const ip = request.headers.get("CF-Connecting-IP") || "local";

    if (path === "me" && method === "GET") {
      const u = await sessionUser(request, db, now);
      return json({ user: u ? publicUser(u) : null });
    }

    if (path === "auth/register" && method === "POST") {
      if (!env.RESEND_API_KEY) throw new ApiError(503, "email_disabled", "El registro con mail no está disponible por ahora: podés ingresar con Google.");
      await rateLimit(db, "register", ip, 5, 3600, now);
      const b = await readBody(request);
      const email = normalizeEmail(b.email);
      const password = checkPassword(b.password, email);
      if (b.acceptTerms !== true) throw new ApiError(400, "terms_required", "Para crear la cuenta tenés que aceptar los Términos de Uso y la Política de Privacidad.");
      if (await one(db, "SELECT id FROM users WHERE email = ?", email)) throw new ApiError(409, "email_taken", "Ya existe una cuenta con ese mail. Ingresá o restablecé la contraseña.");
      const id = randomToken(16);
      await run(db, "INSERT INTO users(id, email, email_verified, password_hash, terms_version, terms_accepted_at, created_at) VALUES(?,?,0,?,?,?,?)", id, email, await hashPassword(password, deps.iterations), TERMS_VERSION, now, now);
      await run(db, "INSERT INTO terms_acceptances(user_id, version, accepted_at, via) VALUES(?,?,?,?)", id, TERMS_VERSION, now, "password");
      const user = await one(db, "SELECT * FROM users WHERE id = ?", id);
      await sendVerification(env, deps, db, user, site, now);
      return withSession(user, await createSession(db, id, now), { message: "Te enviamos un mail para confirmar tu dirección." });
    }

    if (path === "auth/login" && method === "POST") {
      const b = await readBody(request);
      const email = normalizeEmail(b.email);
      await rateLimit(db, "login-ip", ip, 15, 600, now);
      await rateLimit(db, "login-mail", email, 8, 600, now);
      const u = await one(db, "SELECT * FROM users WHERE email = ?", email);
      const dummy = "pbkdf2$100000$AAAAAAAAAAAAAAAAAAAAAA$AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
      const ok = await verifyPassword(String(b.password || ""), u && u.password_hash ? u.password_hash : dummy);
      if (!u || !u.password_hash || !ok) throw new ApiError(401, "bad_credentials", "Mail o contraseña incorrectos. Si te registraste con Google, usá el botón de Google.");
      return withSession(u, await createSession(db, u.id, now));
    }

    if (path === "auth/google" && method === "POST") {
      if (!env.GOOGLE_CLIENT_ID) throw new ApiError(503, "google_disabled", "El ingreso con Google no está disponible por ahora.");
      await rateLimit(db, "google", ip, 30, 600, now);
      const b = await readBody(request);
      let g;
      try {
        g = await verifyGoogleIdToken(b.credential, env.GOOGLE_CLIENT_ID, { fetchImpl: deps.fetch || fetch, now });
      } catch {
        throw new ApiError(401, "google_invalid", "No pudimos validar tu cuenta de Google. Probá de nuevo.");
      }
      let u = await one(db, "SELECT * FROM users WHERE google_sub = ?", g.sub);
      if (!u) {
        u = await one(db, "SELECT * FROM users WHERE email = ?", g.email);
        if (u) {
          // Cuenta existente con el mismo mail: Google ya verificó el mail. Si la cuenta de mail nunca se verificó,
          // se descarta su contraseña (evita que alguien que se registró con el mail de otra persona conserve el acceso).
          await run(db, "UPDATE users SET google_sub = ?, email_verified = 1, name = COALESCE(name, ?), password_hash = CASE WHEN email_verified = 0 THEN NULL ELSE password_hash END WHERE id = ?", g.sub, g.name, u.id);
        } else {
          if (b.acceptTerms !== true) throw new ApiError(409, "terms_required", "Para crear la cuenta tenés que aceptar los Términos de Uso y la Política de Privacidad.");
          const id = randomToken(16);
          await run(db, "INSERT INTO users(id, email, email_verified, google_sub, name, terms_version, terms_accepted_at, created_at) VALUES(?,?,1,?,?,?,?,?)", id, g.email, g.sub, g.name, TERMS_VERSION, now, now);
          await run(db, "INSERT INTO terms_acceptances(user_id, version, accepted_at, via) VALUES(?,?,?,?)", id, TERMS_VERSION, now, "google");
          u = { id };
        }
      }
      const user = await one(db, "SELECT * FROM users WHERE id = ?", u.id);
      return withSession(user, await createSession(db, user.id, now));
    }

    if (path === "auth/logout" && method === "POST") {
      const token = parseCookies(request.headers.get("Cookie")).cc_session;
      if (token) await run(db, "DELETE FROM sessions WHERE token_hash = ?", await sha256Hex(token));
      return json({ ok: true }, 200, { "Set-Cookie": sessionCookie("", 0) });
    }

    if (path === "auth/verify" && method === "POST") {
      await rateLimit(db, "verify", ip, 20, 600, now);
      const b = await readBody(request);
      const row = await one(db, "SELECT * FROM email_tokens WHERE token_hash = ? AND kind = 'verify' AND expires_at > ?", await sha256Hex(String(b.token || "")), now);
      if (!row) throw new ApiError(400, "token_invalid", "El enlace venció o ya se usó. Pedí uno nuevo desde tu cuenta.");
      await run(db, "UPDATE users SET email_verified = 1 WHERE id = ?", row.user_id);
      await run(db, "DELETE FROM email_tokens WHERE token_hash = ?", row.token_hash);
      return json({ ok: true });
    }

    if (path === "auth/resend" && method === "POST") {
      const u = await requireUser(request, db, now);
      if (u.email_verified) return json({ ok: true });
      if (!env.RESEND_API_KEY) throw new ApiError(503, "email_disabled", "El envío de mails no está disponible por ahora.");
      await rateLimit(db, "resend", u.id, 3, 3600, now);
      await sendVerification(env, deps, db, u, site, now);
      return json({ ok: true });
    }

    if (path === "auth/forgot" && method === "POST") {
      if (!env.RESEND_API_KEY) throw new ApiError(503, "email_disabled", "El envío de mails no está disponible por ahora.");
      await rateLimit(db, "forgot", ip, 5, 3600, now);
      const b = await readBody(request);
      const email = normalizeEmail(b.email);
      await rateLimit(db, "forgot-mail", email, 3, 3600, now);
      const u = await one(db, "SELECT * FROM users WHERE email = ?", email);
      if (u && u.password_hash) {
        const token = await issueEmailToken(db, u.id, "reset", 1, now);
        await sendMail(env, deps, { to: email, subject: "Restablecé tu contraseña — Calculadora Científica", text: `Hola:\n\nPara elegir una contraseña nueva entrá a este enlace (vale 1 hora):\n${site}/cuenta/?restablecer=${token}\n\nSi no lo pediste, ignorá este mensaje: tu contraseña no cambia.` });
      }
      return json({ ok: true, message: "Si ese mail tiene una cuenta con contraseña, te enviamos un enlace para restablecerla." });
    }

    if (path === "auth/reset" && method === "POST") {
      await rateLimit(db, "reset", ip, 10, 600, now);
      const b = await readBody(request);
      const row = await one(db, "SELECT * FROM email_tokens WHERE token_hash = ? AND kind = 'reset' AND expires_at > ?", await sha256Hex(String(b.token || "")), now);
      if (!row) throw new ApiError(400, "token_invalid", "El enlace venció o ya se usó. Pedí uno nuevo.");
      const u = await one(db, "SELECT * FROM users WHERE id = ?", row.user_id);
      const password = checkPassword(b.password, u.email);
      await run(db, "UPDATE users SET password_hash = ?, email_verified = 1 WHERE id = ?", await hashPassword(password, deps.iterations), u.id);
      await run(db, "DELETE FROM sessions WHERE user_id = ?", u.id);
      await run(db, "DELETE FROM email_tokens WHERE user_id = ?", u.id);
      return json({ ok: true });
    }

    if (path === "me/accept-terms" && method === "POST") {
      const u = await requireUser(request, db, now);
      const b = await readBody(request);
      if (b.accept !== true) throw new ApiError(400, "terms_required", "Para seguir usando tu cuenta tenés que aceptar los términos actualizados.");
      await run(db, "UPDATE users SET terms_version = ?, terms_accepted_at = ? WHERE id = ?", TERMS_VERSION, now, u.id);
      await run(db, "INSERT INTO terms_acceptances(user_id, version, accepted_at, via) VALUES(?,?,?,?)", u.id, TERMS_VERSION, now, "reaceptacion");
      return json({ user: publicUser(await one(db, "SELECT * FROM users WHERE id = ?", u.id)) });
    }

    if (path === "me/export" && method === "GET") {
      const u = await requireUser(request, db, now);
      const data = await all(db, "SELECT key, value, updated_at FROM user_data WHERE user_id = ?", u.id);
      const acceptances = await all(db, "SELECT version, accepted_at, via FROM terms_acceptances WHERE user_id = ?", u.id);
      return json({ user: { email: u.email, name: u.name, createdAt: u.created_at, emailVerified: !!u.email_verified }, acceptances, data: Object.fromEntries(data.map((d) => [d.key, { value: d.value, updatedAt: d.updated_at }])) }, 200, { "Content-Disposition": 'attachment; filename="mis-datos-calculadora-cientifica.json"' });
    }

    if (path === "me/delete" && method === "POST") {
      const u = await requireUser(request, db, now);
      const b = await readBody(request);
      if (b.confirm !== "ELIMINAR") throw new ApiError(400, "confirm_required", 'Para eliminar la cuenta escribí "ELIMINAR".');
      for (const t of ["user_data", "sessions", "email_tokens", "terms_acceptances"]) await run(db, `DELETE FROM ${t} WHERE user_id = ?`, u.id);
      await run(db, "DELETE FROM users WHERE id = ?", u.id);
      return json({ ok: true }, 200, { "Set-Cookie": sessionCookie("", 0) });
    }

    if (path === "sync" && method === "GET") {
      const u = await requireUser(request, db, now);
      if (!u.email_verified) throw new ApiError(403, "unverified", "Confirmá tu mail para guardar tus datos en la cuenta.");
      const rows = await all(db, "SELECT key, value, updated_at FROM user_data WHERE user_id = ?", u.id);
      return json({ data: Object.fromEntries(rows.map((r) => [r.key, { v: r.value, t: r.updated_at }])) });
    }

    if (path === "sync" && method === "PUT") {
      const u = await requireUser(request, db, now);
      if (!u.email_verified) throw new ApiError(403, "unverified", "Confirmá tu mail para guardar tus datos en la cuenta.");
      await rateLimit(db, "sync", u.id, 120, 600, now);
      const b = await readBody(request);
      const entries = Object.entries(b.data && typeof b.data === "object" ? b.data : {});
      if (entries.length > 60) throw new ApiError(400, "too_many", "Demasiados datos en una sola solicitud.");
      const existing = await all(db, "SELECT key FROM user_data WHERE user_id = ?", u.id);
      const known = new Set(existing.map((r) => r.key));
      for (const [key, item] of entries) {
        if (!KEY_RE.test(key) || !item || typeof item.v !== "string" || item.v.length > MAX_VALUE || !Number.isFinite(item.t)) continue;
        if (!known.has(key) && known.size >= MAX_KEYS) continue;
        known.add(key);
        await run(
          db,
          `INSERT INTO user_data(user_id, key, value, updated_at) VALUES(?,?,?,?)
           ON CONFLICT(user_id, key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at WHERE excluded.updated_at >= user_data.updated_at`,
          u.id, key, item.v, Math.min(item.t, now + 60000)
        );
      }
      const rows = await all(db, "SELECT key, value, updated_at FROM user_data WHERE user_id = ?", u.id);
      return json({ data: Object.fromEntries(rows.map((r) => [r.key, { v: r.value, t: r.updated_at }])) });
    }

    throw new ApiError(404, "not_found", "No encontrado.");
  } catch (err) {
    if (err instanceof ApiError) return json({ error: err.code, message: err.message }, err.status);
    console.error("api error", err && err.stack ? err.stack : err);
    return json({ error: "server_error", message: "Ocurrió un error inesperado. Probá de nuevo en unos minutos." }, 500);
  }
}
