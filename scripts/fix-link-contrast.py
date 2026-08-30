"""
fix-link-contrast.py — Redirige los usos de "text-[var(--color-primary)]"
(incluye "hover:text-[var(--color-primary)]", que contiene el mismo
substring) al nuevo token "--color-primary-link", que en modo oscuro es
más claro para mantener 4.5:1 de contraste WCAG AA sobre tarjetas.

No toca "bg-[var(--color-primary)]" ni "focus:ring-[var(--color-primary)]"
(esos usos están bien como están: los botones necesitan el azul más
saturado para que el texto blanco encima tenga suficiente contraste, y
los anillos de foco solo requieren 3:1, que ya cumplen).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD = "text-[var(--color-primary)]"
NEW = "text-[var(--color-primary-link)]"

pages = sorted(ROOT.glob("**/*.html"))
changed = 0
total_replacements = 0

for page in pages:
    text = page.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count == 0:
        continue
    text = text.replace(OLD, NEW)
    page.write_text(text, encoding="utf-8")
    changed += 1
    total_replacements += count
    print(f"{page.relative_to(ROOT)}: {count} reemplazo(s)")

print(f"\n{changed} archivos actualizados, {total_replacements} reemplazos en total.")
