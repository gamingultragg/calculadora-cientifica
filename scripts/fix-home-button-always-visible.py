"""
fix-home-button-always-visible.py — Saca las clases que ocultan el botón
"back-to-home" hasta scrollear (opacity-0, pointer-events-none,
translate-y-2), para que quede siempre visible. El botón "back-to-top"
no se toca: sigue apareciendo recién al scrollear. Idempotente.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD = (
    'id="back-to-home" aria-label="Ir al inicio del sitio"\n'
    '  class="fixed bottom-20 right-6 z-40 w-11 h-11 rounded-full surface shadow-lg '
    'flex items-center justify-center opacity-0 pointer-events-none translate-y-2 '
    'transition-all duration-200 hover:shadow-xl">'
)
NEW = (
    'id="back-to-home" aria-label="Ir al inicio del sitio"\n'
    '  class="fixed bottom-20 right-6 z-40 w-11 h-11 rounded-full surface shadow-lg '
    'flex items-center justify-center transition-all duration-200 hover:shadow-xl">'
)

pages = [p for p in sorted(ROOT.glob("**/index.html")) if p != ROOT / "index.html"]
pages.append(ROOT / "404.html")

changed = 0
skipped = 0

for page in pages:
    text = page.read_text(encoding="utf-8")
    if OLD not in text:
        if 'id="back-to-home"' in text and "opacity-0" not in text.split('id="back-to-home"')[1][:300]:
            skipped += 1  # ya estaba arreglado
        continue
    text = text.replace(OLD, NEW, 1)
    page.write_text(text, encoding="utf-8")
    changed += 1
    print(f"actualizado: {page.relative_to(ROOT)}")

print(f"\n{changed} archivos actualizados, {skipped} ya estaban bien.")
