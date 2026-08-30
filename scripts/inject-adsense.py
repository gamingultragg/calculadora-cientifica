"""
inject-adsense.py — Agrega el script de verificación/carga de Google
AdSense al <head> de todas las páginas. Idempotente: si una página ya lo
tiene, la salta.

No carga anuncios por sí solo (la cuenta todavía puede estar en revisión)
— es el mismo script que usa AdSense tanto para verificar la propiedad
del sitio como, una vez aprobada la cuenta, para servir anuncios.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ADSENSE_CLIENT = "ca-pub-7274131858034505"
SNIPPET = (
    f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'
    f'?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>\n'
)
ANCHOR = '<script src="https://cdn.tailwindcss.com"></script>'

pages = sorted(ROOT.glob("**/index.html")) + [ROOT / "404.html"]
changed = 0
skipped = 0

for page in pages:
    text = page.read_text(encoding="utf-8")
    if ADSENSE_CLIENT in text:
        skipped += 1
        continue
    if ANCHOR not in text:
        print(f"AVISO: ancla no encontrada en {page.relative_to(ROOT)}")
        continue
    text = text.replace(ANCHOR, SNIPPET + ANCHOR, 1)
    page.write_text(text, encoding="utf-8")
    changed += 1
    print(f"actualizado: {page.relative_to(ROOT)}")

print(f"\n{changed} archivos actualizados, {skipped} ya tenían el snippet.")
