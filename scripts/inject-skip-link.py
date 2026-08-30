"""
inject-skip-link.py — Agrega un enlace "Saltar al contenido" (visible solo
al enfocarlo con teclado) justo después de <body>, y un id="main-content"
al <main> de la página, para que usuarios de teclado/lectores de pantalla
puedan saltar el header sin tener que tabular por toda la navegación.
Idempotente.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_LINK = (
    '<a href="#main-content" '
    'class="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 '
    'focus:px-4 focus:py-2 focus:rounded-lg focus:bg-[var(--color-primary)] '
    'focus:text-white focus:text-sm focus:font-semibold">Saltar al contenido</a>'
)

BODY_RE = re.compile(r'(<body[^>]*>)')
MAIN_RE = re.compile(r'<main(?![^>]*\bid=)([^>]*)>')

pages = sorted(ROOT.glob("**/index.html")) + [ROOT / "404.html"]
changed = 0
skipped = 0

for page in pages:
    text = page.read_text(encoding="utf-8")
    if "Saltar al contenido" in text:
        skipped += 1
        continue
    if not BODY_RE.search(text) or "<main" not in text:
        print(f"AVISO: no se encontró <body> o <main> en {page.relative_to(ROOT)}")
        continue

    text = BODY_RE.sub(lambda m: m.group(1) + "\n  " + SKIP_LINK, text, count=1)
    text = MAIN_RE.sub(lambda m: f'<main id="main-content"{m.group(1)}>', text, count=1)

    page.write_text(text, encoding="utf-8")
    changed += 1
    print(f"actualizado: {page.relative_to(ROOT)}")

print(f"\n{changed} archivos actualizados, {skipped} ya lo tenían.")
