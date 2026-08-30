/**
 * theme.js — Toggle de modo oscuro/claro compartido por toda la plataforma.
 * Se auto-ejecuta apenas se carga (antes de pintar el body) para evitar
 * parpadeo (FOUC) cuando el usuario ya eligió modo oscuro.
 */
(function initTheme() {
  const STORAGE_KEY = "cc-theme";

  function applyTheme(theme) {
    document.documentElement.classList.toggle("dark", theme === "dark");
  }

  function getPreferredTheme() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === "dark" || stored === "light") return stored;
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  // Aplicar de inmediato (este script se incluye con <script> normal, no
  // defer, justo antes de cerrar <head>, para que corra antes del primer paint).
  applyTheme(getPreferredTheme());

  window.ccToggleTheme = function ccToggleTheme() {
    const isDark = document.documentElement.classList.contains("dark");
    const next = isDark ? "light" : "dark";
    applyTheme(next);
    localStorage.setItem(STORAGE_KEY, next);
    document.querySelectorAll("[data-theme-icon]").forEach((el) => {
      el.textContent = next === "dark" ? "☀️" : "🌙";
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    const isDark = document.documentElement.classList.contains("dark");
    document.querySelectorAll("[data-theme-icon]").forEach((el) => {
      el.textContent = isDark ? "☀️" : "🌙";
    });
    document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
      btn.addEventListener("click", window.ccToggleTheme);
    });
  });
})();
