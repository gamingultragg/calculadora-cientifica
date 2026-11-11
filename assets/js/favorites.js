/**
 * favorites.js — "Mis calculadoras favoritas", guardadas solo en este navegador (localStorage "cc-favs").
 *  - En cada calculadora: botón ☆/★ junto al título para guardarla o quitarla.
 *  - En la home: bloque "Tus favoritas" arriba de la grilla, con acceso directo y botón para quitar.
 */
(function () {
  const KEY = "cc-favs";
  const MAX = 12;
  const CALC_PATH = /^\/calculadoras\/[^/]+\/[^/]+\/$/;

  function load() {
    try {
      const v = JSON.parse(localStorage.getItem(KEY) || "[]");
      return Array.isArray(v) ? v.filter((x) => x && typeof x.u === "string" && typeof x.t === "string").slice(0, MAX) : [];
    } catch {
      return [];
    }
  }
  function save(list) {
    try {
      localStorage.setItem(KEY, JSON.stringify(list.slice(0, MAX)));
    } catch {
      /* sin almacenamiento: no se guardan favoritas */
    }
  }

  // ---- página de una calculadora ----
  if (CALC_PATH.test(location.pathname)) {
    const h1 = document.querySelector("main h1");
    if (!h1) return;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "cc-copy mt-3";
    const render = () => {
      const on = load().some((x) => x.u === location.pathname);
      btn.textContent = on ? "★ En tus favoritas" : "☆ Guardar en favoritas";
      btn.setAttribute("aria-pressed", String(on));
    };
    btn.addEventListener("click", () => {
      let list = load();
      if (list.some((x) => x.u === location.pathname)) list = list.filter((x) => x.u !== location.pathname);
      else list.unshift({ u: location.pathname, t: h1.textContent.trim() });
      save(list);
      render();
    });
    render();
    h1.insertAdjacentElement("afterend", btn);
    return;
  }

  // ---- home ----
  const main = document.getElementById("calculadoras");
  if (location.pathname !== "/" || !main) return;
  const box = document.createElement("section");
  box.id = "cc-favs";
  box.className = "mb-8";
  box.hidden = true;
  main.insertBefore(box, main.firstChild);

  function render() {
    const list = load();
    box.hidden = list.length === 0;
    box.textContent = "";
    if (!list.length) return;
    const h = document.createElement("h2");
    h.className = "font-display font-bold text-xl mb-3";
    h.textContent = "Tus favoritas";
    const ul = document.createElement("ul");
    ul.className = "flex flex-wrap gap-2";
    list.forEach((f) => {
      const li = document.createElement("li");
      li.className = "surface rounded-full pl-4 pr-1 py-1 flex items-center gap-1 shadow-sm";
      const a = document.createElement("a");
      a.href = f.u;
      a.className = "text-sm font-semibold hover:underline text-[var(--color-primary-link)]";
      a.textContent = "★ " + f.t;
      const x = document.createElement("button");
      x.type = "button";
      x.className = "cc-fav-x";
      x.setAttribute("aria-label", `Quitar ${f.t} de favoritas`);
      x.textContent = "×";
      x.addEventListener("click", () => {
        save(load().filter((y) => y.u !== f.u));
        render();
      });
      li.append(a, x);
      ul.append(li);
    });
    box.append(h, ul);
  }
  render();
})();
