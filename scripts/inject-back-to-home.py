"""
inject-back-to-home.py — Agrega el botón flotante "Ir al inicio del sitio"
(navega a /) justo arriba del botón "Volver arriba" ya existente, en todas
las páginas excepto la propia home (sería redundante ahí). Idempotente.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HOME_BUTTON = (
    '<a href="/" id="back-to-home" aria-label="Ir al inicio del sitio"\n'
    '  class="fixed bottom-20 right-6 z-40 w-11 h-11 rounded-full surface shadow-lg '
    'flex items-center justify-center opacity-0 pointer-events-none translate-y-2 '
    'transition-all duration-200 hover:shadow-xl">\n'
    '  <svg class="w-5 h-5 text-[var(--color-text)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">\n'
    '    <path stroke-linecap="round" stroke-linejoin="round" d="M3 9.5L12 3l9 6.5M5 9.5V20a1 1 0 001 1h4v-6h4v6h4a1 1 0 001-1V9.5"/>\n'
    "  </svg>\n"
    "</a>\n"
)

ANCHOR = '<button id="back-to-top"'

pages = [p for p in sorted(ROOT.glob("**/index.html")) if p != ROOT / "index.html"]
pages.append(ROOT / "404.html")

changed = 0
skipped = 0

for page in pages:
    text = page.read_text(encoding="utf-8")
    if 'id="back-to-home"' in text:
        skipped += 1
        continue
    if ANCHOR not in text:
        print(f"AVISO: no se encontró el botón back-to-top en {page.relative_to(ROOT)}")
        continue

    text = text.replace(ANCHOR, HOME_BUTTON + ANCHOR, 1)
    page.write_text(text, encoding="utf-8")
    changed += 1
    print(f"actualizado: {page.relative_to(ROOT)}")

print(f"\n{changed} archivos actualizados, {skipped} ya lo tenían.")
