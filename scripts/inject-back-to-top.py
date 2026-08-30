"""
inject-back-to-top.py — Agrega el botón flotante "Volver al inicio" y su
script justo antes de </body> en todas las páginas. Idempotente.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BUTTON = (
    '<button id="back-to-top" type="button" aria-label="Volver al inicio de la página"\n'
    '  class="fixed bottom-6 right-6 z-40 w-11 h-11 rounded-full bg-[var(--color-primary)] '
    'text-white shadow-lg flex items-center justify-center opacity-0 pointer-events-none '
    'translate-y-2 transition-all duration-200 hover:brightness-110">\n'
    '  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">\n'
    '    <path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7"/>\n'
    "  </svg>\n"
    "</button>\n"
    '<script src="/assets/js/back-to-top.js"></script>\n'
)

pages = sorted(ROOT.glob("**/index.html")) + [ROOT / "404.html"]
changed = 0
skipped = 0

for page in pages:
    text = page.read_text(encoding="utf-8")
    if 'id="back-to-top"' in text:
        skipped += 1
        continue
    if "</body>" not in text:
        print(f"AVISO: no se encontró </body> en {page.relative_to(ROOT)}")
        continue

    text = text.replace("</body>", f"{BUTTON}</body>", 1)
    page.write_text(text, encoding="utf-8")
    changed += 1
    print(f"actualizado: {page.relative_to(ROOT)}")

print(f"\n{changed} archivos actualizados, {skipped} ya lo tenían.")
