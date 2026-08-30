"""
inject-legal-links.py — Agrega los enlaces "Privacidad · Términos" a la
línea de copyright del footer en todas las páginas. Idempotente: si una
página ya los tiene, la salta. No toca privacidad/ ni terminos-de-uso/
(ya los tienen desde que se crearon).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_LINE = "<p>© 2026 Calculadora Científica · Hecho en Argentina 🇦🇷</p>"
NEW_LINE = (
    '<p>© 2026 Calculadora Científica · Hecho en Argentina 🇦🇷 · '
    '<a href="/privacidad/" class="hover:text-[var(--color-primary)]">Privacidad</a> · '
    '<a href="/terminos-de-uso/" class="hover:text-[var(--color-primary)]">Términos</a></p>'
)

pages = sorted(ROOT.glob("**/index.html")) + [ROOT / "404.html"]
changed = 0
skipped = 0

for page in pages:
    text = page.read_text(encoding="utf-8")
    if "Privacidad</a>" in text:
        skipped += 1
        continue
    if OLD_LINE not in text:
        print(f"AVISO: patrón de footer no encontrado en {page.relative_to(ROOT)}")
        continue
    text = text.replace(OLD_LINE, NEW_LINE)
    page.write_text(text, encoding="utf-8")
    changed += 1
    print(f"actualizado: {page.relative_to(ROOT)}")

print(f"\n{changed} archivos actualizados, {skipped} ya tenían el enlace.")
