"""
swap-floating-buttons.py — Invierte las posiciones verticales de los
botones flotantes: "back-to-home" pasa a bottom-6 (abajo del todo) y
"back-to-top" pasa a bottom-20 (arriba del otro). Idempotente (detecta
si ya están intercambiados y no vuelve a tocar).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TOP_OLD = 'id="back-to-top" type="button" aria-label="Volver al inicio de la página"\n  class="fixed bottom-6 right-6'
TOP_NEW = 'id="back-to-top" type="button" aria-label="Volver al inicio de la página"\n  class="fixed bottom-20 right-6'

HOME_OLD = 'id="back-to-home" aria-label="Ir al inicio del sitio"\n  class="fixed bottom-20 right-6'
HOME_NEW = 'id="back-to-home" aria-label="Ir al inicio del sitio"\n  class="fixed bottom-6 right-6'

pages = sorted(ROOT.glob("**/index.html")) + [ROOT / "404.html"]
changed = 0

for page in pages:
    text = page.read_text(encoding="utf-8")
    original = text
    text = text.replace(TOP_OLD, TOP_NEW)
    text = text.replace(HOME_OLD, HOME_NEW)
    if text != original:
        page.write_text(text, encoding="utf-8")
        changed += 1
        print(f"actualizado: {page.relative_to(ROOT)}")

print(f"\n{changed} archivos actualizados.")
