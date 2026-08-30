"""
group-guias-by-category.py — Reordena las tarjetas de /guias/index.html
(hand-authored, no data-driven como el dashboard) para que queden
agrupadas por categoría, en el mismo orden que CC_CATEGORIES, en vez del
orden cronológico en que se fueron escribiendo las guías.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "guias" / "index.html"

CATEGORY_ORDER = [
    "Matemáticas Avanzadas",
    "Estadística",
    "Física",
    "Química",
    "Ingeniería",
    "Finanzas",
]

CARD_RE = re.compile(
    r'      <a href="[^"]*"\n        class="surface[^\n]*">\n.*?\n      </a>',
    re.DOTALL,
)
BADGE_RE = re.compile(r'<span class="badge[^"]*">([^<]+)</span>')

text = PAGE.read_text(encoding="utf-8")
cards = CARD_RE.findall(text)
print(f"Tarjetas encontradas: {len(cards)}")

if len(cards) != 18:
    print("AVISO: se esperaban 18 tarjetas, revisar antes de continuar.")

def category_index(card):
    m = BADGE_RE.search(card)
    label = m.group(1) if m else ""
    return CATEGORY_ORDER.index(label) if label in CATEGORY_ORDER else len(CATEGORY_ORDER)

sorted_cards = sorted(cards, key=category_index)

# Reemplazar el bloque completo de tarjetas por la versión reordenada,
# separadas por línea en blanco (mismo formato que el original).
old_block = "\n\n".join(cards)
new_block = "\n\n".join(sorted_cards)

if old_block not in text:
    print("ERROR: no se pudo ubicar el bloque original exacto en el archivo. Nada se modificó.")
else:
    text = text.replace(old_block, new_block, 1)
    PAGE.write_text(text, encoding="utf-8")
    print("guias/index.html reordenado por categoría.")
