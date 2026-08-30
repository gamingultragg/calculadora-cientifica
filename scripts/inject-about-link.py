"""
inject-about-link.py — Agrega el enlace "Sobre Nosotros" a la línea de
copyright del footer en todas las páginas. Idempotente: si una página ya
lo tiene, la salta. No toca sobre-nosotros/index.html (ya lo tiene desde
que se creó).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_LINE = (
    '<p>© 2026 Calculadora Científica · Hecho en Argentina 🇦🇷 · '
    '<a href="/privacidad/" class="hover:text-[var(--color-primary-link)]">Privacidad</a> · '
    '<a href="/terminos-de-uso/" class="hover:text-[var(--color-primary-link)]">Términos</a></p>'
)
NEW_LINE = (
    '<p>© 2026 Calculadora Científica · Hecho en Argentina 🇦🇷 · '
    '<a href="/sobre-nosotros/" class="hover:text-[var(--color-primary-link)]">Sobre Nosotros</a> · '
    '<a href="/privacidad/" class="hover:text-[var(--color-primary-link)]">Privacidad</a> · '
    '<a href="/terminos-de-uso/" class="hover:text-[var(--color-primary-link)]">Términos</a></p>'
)

pages = sorted(ROOT.glob("**/index.html")) + [ROOT / "404.html"]
changed = 0
skipped = 0

for page in pages:
    if "sobre-nosotros" in str(page.relative_to(ROOT)).replace("\\", "/"):
        skipped += 1
        continue
    text = page.read_text(encoding="utf-8")
    if "Sobre Nosotros</a>" in text:
        skipped += 1
        continue
    if OLD_LINE not in text:
        print(f"AVISO: patrón de footer no encontrado en {page.relative_to(ROOT)}")
        continue
    text = text.replace(OLD_LINE, NEW_LINE)
    page.write_text(text, encoding="utf-8")
    changed += 1
    print(f"actualizado: {page.relative_to(ROOT)}")

print(f"\n{changed} archivos actualizados, {skipped} ya tenían el enlace o son sobre-nosotros/.")
