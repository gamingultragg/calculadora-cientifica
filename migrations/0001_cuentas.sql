-- Cuentas de usuario de Calculadora Científica (Cloudflare D1 / SQLite).
-- Se aplica una sola vez:  npx wrangler d1 execute calculadora --remote --file=migrations/0001_cuentas.sql

CREATE TABLE IF NOT EXISTS users (
  id                 TEXT PRIMARY KEY,
  email              TEXT NOT NULL UNIQUE,          -- siempre en minúsculas
  email_verified     INTEGER NOT NULL DEFAULT 0,
  password_hash      TEXT,                          -- pbkdf2$iteraciones$sal$hash (NULL si solo usa Google)
  google_sub         TEXT UNIQUE,                   -- identificador estable de la cuenta de Google
  name               TEXT,
  terms_version      TEXT NOT NULL,
  terms_accepted_at  INTEGER NOT NULL,              -- ms desde epoch
  created_at         INTEGER NOT NULL,
  last_login_at      INTEGER
);

-- Constancia de cada aceptación de los términos (versión + momento).
CREATE TABLE IF NOT EXISTS terms_acceptances (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  version     TEXT NOT NULL,
  accepted_at INTEGER NOT NULL,
  via         TEXT NOT NULL                          -- 'password' | 'google'
);

-- Sesiones: se guarda solo el hash del token (la cookie lleva el token).
CREATE TABLE IF NOT EXISTS sessions (
  token_hash TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at INTEGER NOT NULL,
  expires_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);

-- Tokens de un solo uso para verificar el mail o restablecer la contraseña (también hasheados).
CREATE TABLE IF NOT EXISTS email_tokens (
  token_hash TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  kind       TEXT NOT NULL,                          -- 'verify' | 'reset'
  expires_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_email_tokens_user ON email_tokens(user_id);

-- Datos que la persona guarda en su cuenta (favoritas, historial, preferencias): clave → JSON.
CREATE TABLE IF NOT EXISTS user_data (
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  key        TEXT NOT NULL,
  value      TEXT NOT NULL,
  updated_at INTEGER NOT NULL,
  PRIMARY KEY (user_id, key)
);

-- Límite de intentos por acción y origen (ventana deslizante simple).
CREATE TABLE IF NOT EXISTS rate_limits (
  k        TEXT PRIMARY KEY,
  n        INTEGER NOT NULL,
  reset_at INTEGER NOT NULL
);
