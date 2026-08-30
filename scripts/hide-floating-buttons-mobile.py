"""
hide-floating-buttons-mobile.py — Oculta por completo los botones
flotantes (back-to-top / back-to-home) por debajo del breakpoint lg
(1024px). El usuario los encontró molestos en mobile incluso ya
reposicionados a la izquierda; en desktop se mantienen como estaban.
Idempotente.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    (
        'class="fixed bottom-20 left-4 right-auto lg:left-auto lg:right-6 z-40 w-11 h-11 rounded-full bg-[var(--color-primary)] text-white shadow-lg flex items-center justify-center opacity-0 pointer-events-none translate-y-2 transition-all duration-200 hover:brightness-110">',
        'class="fixed bottom-20 right-6 z-40 w-11 h-11 rounded-full bg-[var(--color-primary)] text-white shadow-lg hidden lg:flex items-center justify-center opacity-0 pointer-events-none translate-y-2 transition-all duration-200 hover:brightness-110">',
    ),
    (
        'class="fixed bottom-6 left-4 right-auto lg:left-auto lg:right-6 z-40 w-11 h-11 rounded-full surface shadow-lg flex items-center justify-center transition-all duration-200 hover:shadow-xl">',
        'class="fixed bottom-6 right-6 z-40 w-11 h-11 rounded-full surface shadow-lg hidden lg:flex items-center justify-center transition-all duration-200 hover:shadow-xl">',
    ),
    (
        # Variante de la home: back-to-top solo, en bottom-6 (no hay back-to-home ahí).
        'class="fixed bottom-6 left-4 right-auto lg:left-auto lg:right-6 z-40 w-11 h-11 rounded-full bg-[var(--color-primary)] text-white shadow-lg flex items-center justify-center opacity-0 pointer-events-none translate-y-2 transition-all duration-200 hover:brightness-110">',
        'class="fixed bottom-6 right-6 z-40 w-11 h-11 rounded-full bg-[var(--color-primary)] text-white shadow-lg hidden lg:flex items-center justify-center opacity-0 pointer-events-none translate-y-2 transition-all duration-200 hover:brightness-110">',
    ),
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
