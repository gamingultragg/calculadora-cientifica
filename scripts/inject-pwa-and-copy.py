"""
inject-pwa-and-copy.py — Agrega a TODAS las páginas (idempotente):
  - <head>: <link rel="manifest"> y <meta name="theme-color">
  - antes de </body>: assets/js/pwa.js (service worker + "Instalar app")
  - en las páginas con panel de resultado o botón data-copy-target: assets/js/copy-result.js
Correr después de cualquier generador de páginas; luego scripts/build-sw.py.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEAD_ANCHOR = '<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png" />'
HEAD_ADD = '\n<link rel="manifest" href="/manifest.webmanifest" />\n<meta name="theme-color" content="#2563eb" />'
PWA = '<script src="/assets/js/pwa.js" defer></script>'
COPY = '<script src="/assets/js/copy-result.js" defer></script>'
FAVS = '<script src="/assets/js/favorites.js" defer></script>'
ACCOUNT = '<script src="/assets/js/account.js" defer></script>'

changed = 0
for f in sorted(ROOT.rglob("*.html")):
    rel = f.relative_to(ROOT).as_posix()
    if rel.startswith(("tools/", "functions/", "node_modules/")) or rel.startswith("google"):
        continue
    s = f.read_text(encoding="utf-8")
    if "</body>" not in s:
        continue
    o = s
    if "manifest.webmanifest" not in s and HEAD_ANCHOR in s:
        s = s.replace(HEAD_ANCHOR, HEAD_ANCHOR + HEAD_ADD, 1)
    needs_copy = 'id$=' in s or "-result-panel" in s or "data-copy-target" in s
    add = ""
    if PWA not in s:
        add += PWA + "\n"
    if needs_copy and COPY not in s:
        add += COPY + "\n"
    # favoritas: home y páginas de calculadoras (calculadoras/<categoria>/<slug>/index.html)
    if FAVS not in s and (rel == "index.html" or (rel.startswith("calculadoras/") and rel.count("/") == 3)):
        add += FAVS + "\n"
    if ACCOUNT not in s and rel not in ("404.html",):
        add += ACCOUNT + "\n"
    if add:
        s = s.replace("</body>", add + "</body>", 1)
    if s != o:
        f.write_text(s, encoding="utf-8")
        changed += 1
print(f"{changed} páginas actualizadas")
