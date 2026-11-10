"""
replace-tailwind-cdn.py — Reemplaza el Tailwind Play CDN por el CSS compilado
(assets/css/tailwind.css, generado con tools/tailwind).

Quita de cada <head>:
    <script src="https://cdn.tailwindcss.com"></script>
    <script> tailwind.config = {...}; </script>
y agrega, justo después de styles.css:
    <link rel="stylesheet" href="/assets/css/tailwind.css" />

El orden importa: el CDN inyectaba su <style> al final del <head> (después de
styles.css), así que el CSS compilado va después de styles.css para conservar
la misma cascada.

Idempotente: las páginas que ya tienen el <link> se saltan.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = '<link rel="stylesheet" href="/assets/css/tailwind.css" />'
STYLES = '<link rel="stylesheet" href="/assets/css/styles.css" />'
CDN_BLOCK = re.compile(
    r'[ \t]*<script src="https://cdn\.tailwindcss\.com"></script>\s*<script>\s*tailwind\.config.*?</script>[ \t]*\r?\n',
    re.S,
)

pages = sorted(ROOT.glob("**/*.html"))
changed = skipped = 0
for page in pages:
    if "node_modules" in page.parts:
        continue
    text = page.read_text(encoding="utf-8")
    if "cdn.tailwindcss.com" not in text:
        skipped += 1
        continue
    if STYLES not in text:
        print(f"AVISO: sin styles.css en {page.relative_to(ROOT)}")
        continue
    new, n = CDN_BLOCK.subn("", text, count=1)
    if n != 1:
        print(f"AVISO: bloque del CDN no encontrado en {page.relative_to(ROOT)}")
        continue
    new = new.replace(STYLES, STYLES + "\n" + LINK, 1)
    page.write_text(new, encoding="utf-8")
    changed += 1

print(f"{changed} páginas actualizadas, {skipped} sin CDN (saltadas).")
