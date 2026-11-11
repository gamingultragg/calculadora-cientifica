"""
build-sw.py — Genera /sw.js a partir de scripts/sw-template.js.
La lista de precarga sale del sitemap (todas las páginas) + los CSS/JS/íconos de assets/.
VERSION = hash del contenido precargado: cualquier cambio en el sitio genera un SW nuevo
y los visitantes reciben la versión actualizada. Correr SIEMPRE al final, antes de commitear.
"""
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.calculadoracientifica.com.ar"

urls = re.findall(r"<loc>" + re.escape(BASE) + r"([^<]*)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
urls = [u for u in urls if u] + ["/404.html", "/manifest.webmanifest"]

for p in sorted((ROOT / "assets").rglob("*")):
    if p.is_file() and p.suffix in {".css", ".js", ".svg"} or p.name in {"pwa-192.png", "pwa-512.png", "apple-touch-icon.png", "favicon-32.png"}:
        urls.append("/" + p.relative_to(ROOT).as_posix())
# los scripts propios de cada calculadora
for p in sorted((ROOT / "calculadoras").rglob("script.js")):
    urls.append("/" + p.relative_to(ROOT).as_posix())
urls = list(dict.fromkeys(urls))


def file_for(u):
    path = u.split("?")[0]
    f = ROOT / path.lstrip("/")
    return f / "index.html" if (f.is_dir() or path.endswith("/") or path == "") else f


h = hashlib.sha256()
for u in urls:
    f = file_for(u)
    if f.exists():
        h.update(u.encode() + f.read_bytes())
    else:
        print("aviso: no existe", u)
version = h.hexdigest()[:10]

tpl = (ROOT / "scripts" / "sw-template.js").read_text(encoding="utf-8")
out = tpl.replace("__VERSION__", version).replace("__PRECACHE__", json.dumps(urls, indent=1))
(ROOT / "sw.js").write_text(out, encoding="utf-8")
print(f"sw.js: {len(urls)} URLs precargadas, versión {version}")
