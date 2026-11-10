/** Misma configuración que usaba el CDN en cada <head>, más las rutas a escanear. */
module.exports = {
  darkMode: "class",
  content: [
    "../../**/*.html",
    "../../assets/js/**/*.js",
    "../../calculadoras/**/script.js",
    "!../../**/node_modules/**",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["Roboto Mono", "ui-monospace", "monospace"],
      },
    },
  },
};
