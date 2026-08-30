"""
fix-mobile-button-position.py — Mueve los botones flotantes a la
izquierda en mobile/tablet (donde el layout de las calculadoras es a una
sola columna y los botones +/- del teclado quedan pegados al borde
derecho, chocando con los flotantes), y los vuelve a la derecha recién
en pantallas grandes (lg: 1024px+, donde el layout pasa a dos columnas y
el borde derecho queda libre). Idempotente.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    ("fixed bottom-20 right-6 z-40", "fixed bottom-20 left-4 right-auto lg:left-auto lg:right-6 z-40"),
    ("fixed bottom-6 right-6 z-40", "fixed bottom-6 left-4 right-auto lg:left-auto lg:right-6 z-40"),
]

pages = sorted(ROOT.glob("**/index.html")) + [ROOT / "404.html"]
changed = 0

for page in pages:
    text = page.read_text(encoding="utf-8")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != original:
        page.write_text(text, encoding="utf-8")
        changed += 1
        print(f"actualizado: {page.relative_to(ROOT)}")

print(f"\n{changed} archivos actualizados.")
