/**
 * account.js — Cuentas de usuario (opcionales): ingreso con Google o con mail y contraseña, aceptación de los
 * términos, y sincronización de favoritas, historial y preferencias entre dispositivos.
 *
 * Si la API de cuentas no está habilitada (/api/config → enabled:false o no responde), este script no hace nada
 * y el sitio funciona exactamente igual que sin él.
 */
(function () {
  "use strict";

  const SYNC_RELOAD_FLAG = "cc-sync-reloaded";
  const META_KEY = "cc-sync-meta";
  const rawSet = Storage.prototype.setItem;
  const rawRemove = Storage.prototype.removeItem;
  let cfg = null;
  let me = null;
  let pendingGoogle = null; // credencial de Google a la espera de que se acepten los términos

  // ------------------------------------------------------------------ utilidades --
  async function api(method, path, body) {
    try {
      const res = await fetch("/api/" + path, {
        method,
        credentials: "same-origin",
        headers: body ? { "Content-Type": "application/json" } : {},
        body: body ? JSON.stringify(body) : undefined,
      });
      let data = {};
      try { data = await res.json(); } catch { /* sin cuerpo */ }
      return { ok: res.ok, status: res.status, data };
    } catch {
      return { ok: false, status: 0, data: { error: "network", message: "No hay conexión. Probá de nuevo." } };
    }
  }

  function el(tag, attrs = {}, ...children) {
    const node = document.createElement(tag);
    Object.entries(attrs).forEach(([k, v]) => {
      if (k === "class") node.className = v;
      else if (k === "text") node.textContent = v;
      else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
      else if (v === true) node.setAttribute(k, "");
      else if (v !== false && v != null) node.setAttribute(k, v);
    });
    children.flat().forEach((c) => c != null && node.append(c));
    return node;
  }

  function toast(message, kind = "info") {
    let box = document.getElementById("cc-toast");
    if (!box) {
      box = el("div", { id: "cc-toast", class: "cc-toast", role: "status", "aria-live": "polite" });
      document.body.append(box);
    }
    box.textContent = message;
    box.dataset.kind = kind;
    box.hidden = false;
    clearTimeout(toast.t);
    toast.t = setTimeout(() => (box.hidden = true), 9000);
  }

  // ------------------------------------------------------------ sincronización --
  const toRemote = (k) => (k === "cc-favs" ? "favs" : k === "cc-theme" ? "prefs" : k === "cc-sci-history" ? "sci-history" : k.startsWith("cc-hist:") ? "hist:" + k.slice(8).toLowerCase() : null);
  const toLocal = (r) => (r === "favs" ? "cc-favs" : r === "prefs" ? "cc-theme" : r === "sci-history" ? "cc-sci-history" : r.startsWith("hist:") ? "cc-hist:" + r.slice(5) : null);
  const parse = (v) => { try { return JSON.parse(v); } catch { return null; } };
  const loadMeta = () => parse(localStorage.getItem(META_KEY)) || {};
  const saveMeta = (m) => rawSet.call(localStorage, META_KEY, JSON.stringify(m));

  function union(a, b, keyOf, sortBy, cap) {
    const seen = new Set();
    const out = [];
    [...(Array.isArray(a) ? a : []), ...(Array.isArray(b) ? b : [])].forEach((x) => {
      const k = x && keyOf(x);
      if (k && !seen.has(k)) { seen.add(k); out.push(x); }
    });
    if (sortBy) out.sort(sortBy);
    return JSON.stringify(out.slice(0, cap));
  }

  function mergeValue(rk, lv, rv, lt, rt) {
    if (lv == null) return rv;
    if (rv == null) return lv;
    if (lv === rv) return lv;
    if (rk === "favs") return union(parse(lv), parse(rv), (x) => x.u, null, 12);
    if (rk.startsWith("hist:")) return union(parse(lv), parse(rv), (x) => JSON.stringify(x.f), (a, b) => (b.t || 0) - (a.t || 0), 8);
    if (rk === "sci-history") return union(parse(lv), parse(rv), (x) => x.expr + "|" + x.raw, null, 30);
    return (lt || 0) >= (rt || 0) ? lv : rv; // preferencias: gana la más reciente
  }

  async function push(data) {
    const keys = Object.keys(data);
    for (let i = 0; i < keys.length; i += 50) {
      const chunk = Object.fromEntries(keys.slice(i, i + 50).map((k) => [k, data[k]]));
      await api("PUT", "sync", { data: chunk });
    }
  }

  async function pull() {
    const r = await api("GET", "sync");
    if (!r.ok) return;
    const remote = r.data.data || {};
    const meta = loadMeta();
    const local = {};
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      const rk = toRemote(k);
      if (rk) local[rk] = localStorage.getItem(k);
    }
    const toPush = {};
    let changed = false;
    new Set([...Object.keys(local), ...Object.keys(remote)]).forEach((rk) => {
      const lk = toLocal(rk);
      if (!lk) return;
      const lv = local[rk] ?? null;
      const rv = remote[rk] ? remote[rk].v : null;
      const merged = mergeValue(rk, lv, rv, meta[rk], remote[rk] && remote[rk].t);
      if (merged == null) return;
      if (merged !== lv) { rawSet.call(localStorage, lk, merged); changed = true; }
      if (merged !== rv) toPush[rk] = { v: merged, t: Date.now() };
    });
    if (Object.keys(toPush).length) await push(toPush);
    if (changed && !sessionStorage.getItem(SYNC_RELOAD_FLAG)) {
      sessionStorage.setItem(SYNC_RELOAD_FLAG, "1");
      location.reload(); // se vuelve a dibujar la página con los datos sincronizados
    }
  }

  const dirty = new Set();
  let timer = null;
  function flush() {
    if (!me || !me.emailVerified || !dirty.size) return;
    const data = {};
    dirty.forEach((rk) => {
      const v = localStorage.getItem(toLocal(rk));
      if (v != null) data[rk] = { v, t: loadMeta()[rk] || Date.now() };
    });
    dirty.clear();
    if (Object.keys(data).length) push(data);
  }
  function markDirty(localKey) {
    const rk = toRemote(localKey);
    if (!rk || !me || !me.emailVerified) return;
    const meta = loadMeta();
    meta[rk] = Date.now();
    saveMeta(meta);
    dirty.add(rk);
    clearTimeout(timer);
    timer = setTimeout(flush, 2500);
  }
  Storage.prototype.setItem = function (k, v) {
    rawSet.call(this, k, v);
    if (this === window.localStorage) markDirty(k);
  };
  Storage.prototype.removeItem = function (k) {
    rawRemove.call(this, k);
  };
  document.addEventListener("visibilitychange", () => document.visibilityState === "hidden" && flush());

  function clearSyncedLocal() {
    const rm = [];
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k === "cc-favs" || k === "cc-sci-history" || k === META_KEY || (k && k.startsWith("cc-hist:"))) rm.push(k);
    }
    rm.forEach((k) => rawRemove.call(localStorage, k));
    sessionStorage.removeItem(SYNC_RELOAD_FLAG);
  }

  // ------------------------------------------------------------------ encabezado --
  function mountHeader() {
    const toggle = document.querySelector("[data-theme-toggle]");
    if (!toggle || document.getElementById("cc-account-slot")) return;
    const slot = el("div", { id: "cc-account-slot", class: "flex items-center gap-2" });
    toggle.parentElement.insertBefore(slot, toggle);
    slot.append(toggle);
    renderHeader();
  }
  function renderHeader() {
    const slot = document.getElementById("cc-account-slot");
    if (!slot) return;
    slot.querySelectorAll(".cc-acc-btn").forEach((n) => n.remove());
    const toggle = slot.querySelector("[data-theme-toggle]");
    if (me) {
      const label = (me.name || me.email).split(/[ @]/)[0].slice(0, 14);
      const a = el("a", { href: "/cuenta/", class: "cc-acc-btn", "aria-label": "Mi cuenta" }, el("span", { class: "cc-acc-avatar", text: (me.name || me.email)[0].toUpperCase() }), el("span", { class: "cc-acc-label", text: label }));
      if (!me.emailVerified || me.needsTerms) a.append(el("span", { class: "cc-acc-dot", title: me.needsTerms ? "Aceptá los términos actualizados" : "Falta confirmar tu mail" }));
      slot.insertBefore(a, toggle);
    } else {
      slot.insertBefore(el("button", { type: "button", class: "cc-acc-btn", onclick: () => openAuth("login") }, el("span", { text: "Ingresar" })), toggle);
    }
  }

  // ---------------------------------------------------------------------- Google --
  let googleLoading = null;
  function loadGoogle() {
    if (googleLoading) return googleLoading;
    googleLoading = new Promise((resolve, reject) => {
      if (window.google && google.accounts && google.accounts.id) return resolve();
      const s = el("script", { src: "https://accounts.google.com/gsi/client", async: true });
      s.onload = resolve;
      s.onerror = reject;
      document.head.append(s);
    });
    return googleLoading;
  }

  // ------------------------------------------------------------------ modal de ingreso --
  let dialog = null;
  let mode = "login";

  function buildDialog() {
    const termsLinks = [el("a", { href: "/terminos-de-uso/", target: "_blank", rel: "noopener", text: "Términos de Uso" }), " y la ", el("a", { href: "/privacidad/", target: "_blank", rel: "noopener", text: "Política de Privacidad" })];
    dialog = el("dialog", { id: "cc-auth", class: "cc-modal", "aria-labelledby": "cc-auth-title" },
      el("button", { type: "button", class: "cc-modal-x", "aria-label": "Cerrar", text: "×", onclick: () => dialog.close() }),
      el("h2", { id: "cc-auth-title", class: "cc-modal-title", text: "Ingresá a tu cuenta" }),
      el("p", { class: "cc-modal-sub", text: "Es opcional. Sirve para guardar tus favoritas, tu historial de cálculos y tus preferencias, y verlos en todos tus dispositivos." }),
      el("div", { class: "cc-tabs", role: "tablist" },
        el("button", { type: "button", role: "tab", "data-tab": "login", "aria-selected": "true", text: "Ingresar", onclick: () => setMode("login") }),
        el("button", { type: "button", role: "tab", "data-tab": "register", "aria-selected": "false", text: "Crear cuenta", onclick: () => setMode("register") })),
      el("div", { id: "cc-google-wrap", class: "cc-google-wrap" }, el("div", { id: "cc-google-btn" }), el("button", { type: "button", id: "cc-google-lock", class: "cc-google-lock", hidden: true, "aria-label": "Aceptá los términos para continuar con Google", onclick: () => showMsg("Para crear la cuenta, primero marcá que aceptás los términos.", true) })),
      // Términos y mensajes van fuera del formulario: tienen que verse aunque el ingreso con mail esté apagado (solo Google).
      el("div", { id: "cc-terms-row", class: "cc-terms", hidden: true },
        el("label", { class: "cc-check" }, el("input", { id: "cc-terms", type: "checkbox", onchange: updateGoogleLock }), el("span", {}, "Acepto los ", termsLinks))),
      el("p", { id: "cc-msg", class: "cc-msg", role: "alert", "aria-live": "polite" }),
      el("p", { id: "cc-or", class: "cc-or", text: "o con tu mail" }),
      el("form", { id: "cc-form", novalidate: true, onsubmit: onSubmit },
        el("label", { class: "cc-field" }, "Mail", el("input", { id: "cc-email", type: "email", autocomplete: "email", required: true, inputmode: "email" })),
        el("label", { class: "cc-field" }, "Contraseña", el("input", { id: "cc-pass", type: "password", autocomplete: "current-password", required: true, minlength: "8" })),
        el("p", { id: "cc-pass-hint", class: "cc-hint", text: "Mínimo 8 caracteres.", hidden: true }),
        el("button", { id: "cc-submit", type: "submit", class: "calc-btn calc-btn--op w-full py-2.5", text: "Ingresar" }),
        el("button", { id: "cc-forgot", type: "button", class: "cc-link", text: "Olvidé mi contraseña", onclick: onForgot })));
    dialog.addEventListener("click", (e) => e.target === dialog && dialog.close());
    document.body.append(dialog);
  }

  function showMsg(text, isError = false) {
    const m = document.getElementById("cc-msg");
    m.textContent = text;
    m.dataset.kind = isError ? "error" : "ok";
  }

  function updateGoogleLock() {
    const lock = document.getElementById("cc-google-lock");
    lock.hidden = !(mode === "register" && !document.getElementById("cc-terms").checked);
  }

  function setMode(next) {
    mode = next;
    dialog.querySelectorAll("[data-tab]").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.tab === mode)));
    const reg = mode === "register";
    document.getElementById("cc-terms-row").hidden = !reg;
    document.getElementById("cc-pass-hint").hidden = !reg;
    document.getElementById("cc-forgot").hidden = reg;
    document.getElementById("cc-submit").textContent = reg ? "Crear cuenta" : "Ingresar";
    document.getElementById("cc-pass").autocomplete = reg ? "new-password" : "current-password";
    document.getElementById("cc-auth-title").textContent = reg ? "Creá tu cuenta" : "Ingresá a tu cuenta";
    showMsg("");
    updateGoogleLock();
  }

  async function openAuth(initialMode = "login") {
    if (!cfg) return;
    if (!dialog) buildDialog();
    const emailOn = cfg.email;
    document.getElementById("cc-form").hidden = !emailOn;
    document.getElementById("cc-or").hidden = !emailOn || !cfg.google;
    dialog.querySelector(".cc-tabs").hidden = !emailOn;
    document.getElementById("cc-google-wrap").hidden = !cfg.google;
    setMode(initialMode);
    if (!dialog.open) dialog.showModal();
    if (cfg.google && !document.getElementById("cc-google-btn").childElementCount) {
      try {
        await loadGoogle();
        google.accounts.id.initialize({ client_id: cfg.google, callback: onGoogle, auto_select: false });
        google.accounts.id.renderButton(document.getElementById("cc-google-btn"), { theme: "outline", size: "large", text: "continue_with", shape: "pill", locale: "es-419", width: 280 });
      } catch {
        document.getElementById("cc-google-wrap").hidden = true;
        showMsg("No se pudo cargar el ingreso con Google. Probá con tu mail o más tarde.", true);
      }
    }
  }

  async function onGoogle(resp, acceptOverride) {
    const accept = acceptOverride === true || (document.getElementById("cc-terms") && document.getElementById("cc-terms").checked && mode === "register");
    const r = await api("POST", "auth/google", { credential: resp.credential, acceptTerms: accept });
    if (r.ok) return afterLogin(r.data.user);
    if (r.data.error === "terms_required") {
      pendingGoogle = resp;
      setMode("register");
      showMsg("Es tu primera vez con esta cuenta de Google. Marcá que aceptás los términos y tocá \"Continuar con Google\".", true);
      showContinue();
      return;
    }
    showMsg(r.data.message || "No pudimos ingresar con Google.", true);
  }

  function showContinue() {
    let b = document.getElementById("cc-google-continue");
    if (!b) {
      b = el("button", { id: "cc-google-continue", type: "button", class: "calc-btn calc-btn--op w-full py-2.5 mt-2", text: "Continuar con Google", onclick: () => {
        if (!document.getElementById("cc-terms").checked) return showMsg("Marcá que aceptás los términos para continuar.", true);
        onGoogle(pendingGoogle, true);
      } });
      document.getElementById("cc-google-wrap").append(b);
    }
    b.hidden = false;
    document.getElementById("cc-google-lock").hidden = true;
  }

  async function onSubmit(e) {
    e.preventDefault();
    const email = document.getElementById("cc-email").value.trim();
    const password = document.getElementById("cc-pass").value;
    if (!email || !password) return showMsg("Completá el mail y la contraseña.", true);
    const btn = document.getElementById("cc-submit");
    btn.disabled = true;
    try {
      if (mode === "register") {
        if (!document.getElementById("cc-terms").checked) return showMsg("Para crear la cuenta tenés que aceptar los Términos de Uso y la Política de Privacidad.", true);
        const r = await api("POST", "auth/register", { email, password, acceptTerms: true });
        if (!r.ok) return showMsg(r.data.message || "No pudimos crear la cuenta.", true);
        afterLogin(r.data.user, `Te enviamos un mail a ${email} para confirmar tu dirección. Cuando lo confirmes, tus datos se guardan en la cuenta.`);
      } else {
        const r = await api("POST", "auth/login", { email, password });
        if (!r.ok) return showMsg(r.data.message || "No pudimos ingresar.", true);
        afterLogin(r.data.user);
      }
    } finally {
      btn.disabled = false;
    }
  }

  async function onForgot() {
    const email = document.getElementById("cc-email").value.trim();
    if (!email) return showMsg("Escribí tu mail arriba y volvé a tocar \"Olvidé mi contraseña\".", true);
    const r = await api("POST", "auth/forgot", { email });
    showMsg(r.data.message || "Si ese mail tiene una cuenta con contraseña, te enviamos un enlace.", !r.ok);
  }

  function afterLogin(user, message) {
    me = user;
    if (dialog && dialog.open) dialog.close();
    renderHeader();
    if (message) toast(message);
    if (me.needsTerms) return askTerms();
    if (me.emailVerified) pull();
    else if (document.location.pathname === "/cuenta/") renderCuenta();
  }

  // -------------------------------------------------------------- términos nuevos --
  function askTerms() {
    const d = el("dialog", { class: "cc-modal", "aria-labelledby": "cc-terms-title" },
      el("h2", { id: "cc-terms-title", class: "cc-modal-title", text: "Actualizamos los términos" }),
      el("p", { class: "cc-modal-sub" }, "Para seguir usando tu cuenta, leé y aceptá los ", el("a", { href: "/terminos-de-uso/", target: "_blank", rel: "noopener", text: "Términos de Uso" }), " y la ", el("a", { href: "/privacidad/", target: "_blank", rel: "noopener", text: "Política de Privacidad" }), " actualizados."),
      el("label", { class: "cc-check" }, el("input", { id: "cc-terms2", type: "checkbox" }), el("span", { text: "Los leí y los acepto." })),
      el("p", { id: "cc-msg2", class: "cc-msg", role: "alert" }),
      el("div", { class: "cc-row" },
        el("button", { type: "button", class: "calc-btn calc-btn--op py-2.5 px-4", text: "Aceptar", onclick: async () => {
          if (!d.querySelector("#cc-terms2").checked) return (d.querySelector("#cc-msg2").textContent = "Marcá la casilla para continuar.");
          const r = await api("POST", "me/accept-terms", { accept: true });
          if (r.ok) { me = r.data.user; d.close(); renderHeader(); if (me.emailVerified) pull(); } else d.querySelector("#cc-msg2").textContent = r.data.message || "No se pudo guardar.";
        } }),
        el("button", { type: "button", class: "cc-link", text: "Cerrar sesión", onclick: () => doLogout() })));
    d.addEventListener("cancel", (e) => e.preventDefault());
    document.body.append(d);
    d.showModal();
  }

  async function doLogout() {
    await api("POST", "auth/logout", {});
    clearSyncedLocal();
    location.href = "/";
  }

  // ---------------------------------------------------------------- página /cuenta/ --
  async function renderCuenta() {
    const box = document.getElementById("cc-cuenta");
    if (!box) return;
    box.textContent = "";
    if (!me) {
      box.append(el("p", { class: "cc-modal-sub", text: "Ingresá para ver y administrar tu cuenta." }), el("button", { type: "button", class: "calc-btn calc-btn--op py-2.5 px-4", text: "Ingresar o crear cuenta", onclick: () => openAuth("login") }));
      return;
    }
    const kv = (k, v) => el("div", { class: "cc-kv" }, el("dt", { text: k }), el("dd", { text: v }));
    const provider = [me.hasGoogle && "Google", me.hasPassword && "Mail y contraseña"].filter(Boolean).join(" + ");
    const list = el("dl", { class: "cc-dl" }, kv("Mail", me.email), me.name ? kv("Nombre", me.name) : null, kv("Ingreso con", provider || "—"), kv("Términos aceptados", `versión ${me.termsVersion} · ${new Date(me.termsAcceptedAt).toLocaleDateString("es-AR")}`));
    box.append(list);

    if (!me.emailVerified) {
      const msg = el("p", { class: "cc-msg", "data-kind": "error", text: "Todavía no confirmaste tu mail. Hasta que lo hagas no se guardan tus datos en la cuenta." });
      const b = el("button", { type: "button", class: "cc-copy", text: "Reenviar mail de confirmación", onclick: async () => {
        const r = await api("POST", "auth/resend", {});
        msg.textContent = r.ok ? "Listo: te enviamos un mail nuevo. Revisá también la carpeta de spam." : r.data.message || "No se pudo enviar.";
      } });
      box.append(el("div", { class: "mt-4" }, msg, b));
    } else {
      const r = await api("GET", "sync");
      const data = (r.data && r.data.data) || {};
      const favs = (parse((data.favs || {}).v) || []).length;
      const hists = Object.keys(data).filter((k) => k.startsWith("hist:")).length;
      const sci = (parse((data["sci-history"] || {}).v) || []).length;
      box.append(el("h2", { class: "cc-h2", text: "Lo que guardamos en tu cuenta" }), el("ul", { class: "cc-ul" },
        el("li", { text: `${favs} calculadora${favs === 1 ? "" : "s"} favorita${favs === 1 ? "" : "s"}` }),
        el("li", { text: `Historial de ${hists} calculadora${hists === 1 ? "" : "s"}${sci ? ` y ${sci} cálculo${sci === 1 ? "" : "s"} de la calculadora científica` : ""}` }),
        el("li", { text: "Preferencia de tema (claro u oscuro)" })));
    }

    box.append(el("div", { class: "cc-row mt-6" },
      el("a", { href: "/api/me/export", class: "cc-copy", download: "mis-datos-calculadora-cientifica.json", text: "Descargar mis datos" }),
      el("button", { type: "button", class: "cc-copy", text: "Cerrar sesión", onclick: doLogout })));

    const input = el("input", { type: "text", class: "cc-input", placeholder: "Escribí ELIMINAR", "aria-label": "Confirmación para eliminar la cuenta", autocomplete: "off" });
    const dmsg = el("p", { class: "cc-msg", role: "alert" });
    box.append(el("section", { class: "cc-danger" }, el("h2", { class: "cc-h2", text: "Eliminar mi cuenta" }),
      el("p", { class: "cc-modal-sub", text: "Se borran al instante tu cuenta y todo lo que guardaste. No se puede deshacer." }), input,
      el("button", { type: "button", class: "cc-danger-btn", text: "Eliminar definitivamente", onclick: async () => {
        const r = await api("POST", "me/delete", { confirm: input.value.trim() });
        if (!r.ok) { dmsg.textContent = r.data.message || "No se pudo eliminar."; dmsg.dataset.kind = "error"; return; }
        clearSyncedLocal();
        location.href = "/?cuenta-eliminada=1";
      } }), dmsg));
  }

  async function handleCuentaLinks() {
    const box = document.getElementById("cc-cuenta");
    const params = new URLSearchParams(location.search);
    const verify = params.get("verificar"), reset = params.get("restablecer");
    if (verify) {
      history.replaceState(null, "", "/cuenta/");
      const r = await api("POST", "auth/verify", { token: verify });
      toast(r.ok ? "¡Mail confirmado! Ya se guardan tus datos en la cuenta." : r.data.message || "No se pudo confirmar el mail.", r.ok ? "info" : "error");
      if (r.ok && me) { me.emailVerified = true; renderHeader(); pull(); }
      else if (r.ok) { const m = await api("GET", "me"); me = m.data.user; renderHeader(); }
    } else if (reset && box) {
      history.replaceState(null, "", "/cuenta/");
      box.textContent = "";
      const pass = el("input", { type: "password", class: "cc-input", autocomplete: "new-password", minlength: "8", "aria-label": "Nueva contraseña", placeholder: "Nueva contraseña (mínimo 8 caracteres)" });
      const msg = el("p", { class: "cc-msg", role: "alert" });
      box.append(el("h2", { class: "cc-h2", text: "Elegí una contraseña nueva" }), pass, el("button", { type: "button", class: "calc-btn calc-btn--op py-2.5 px-4 mt-3", text: "Guardar contraseña", onclick: async () => {
        const r = await api("POST", "auth/reset", { token: reset, password: pass.value });
        msg.dataset.kind = r.ok ? "ok" : "error";
        msg.textContent = r.ok ? "Listo: tu contraseña cambió. Ya podés ingresar." : r.data.message || "No se pudo cambiar.";
        if (r.ok) setTimeout(() => openAuth("login"), 800);
      } }), msg);
      return true;
    }
    return false;
  }

  // -------------------------------------------------------------------------- inicio --
  (async function init() {
    const c = await api("GET", "config");
    // cuentas no habilitadas, o sin ningún método de ingreso configurado: el sitio sigue como siempre
    if (!c.ok || !c.data.enabled || (!c.data.google && !c.data.email)) return;
    cfg = c.data;
    const m = await api("GET", "me");
    me = (m.data && m.data.user) || null;
    mountHeader();
    if (location.pathname === "/cuenta/") {
      if (await handleCuentaLinks()) return;
      renderCuenta();
    }
    if (me && me.needsTerms) askTerms();
    else if (me && me.emailVerified) pull();
    if (new URLSearchParams(location.search).get("cuenta-eliminada")) toast("Tu cuenta y tus datos fueron eliminados.");
  })();
})();
