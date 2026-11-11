"""
add-category.py — Da de alta una categoría nueva en todo el sitio (idempotente).

Uso:  python scripts/add-category.py KEY SLUG "Etiqueta" COLOR "Descripción"
Ej.:  python scripts/add-category.py hogar hogar-y-construccion "Hogar y Construcción" cyan "Cerámicos, pintura..."

Hace: entrada en CC_CATEGORIES (calculators-data.js), color en main.js / category.js / prerender-cards.py,
botón de filtro en la home y la página de categoría (a partir de la de Finanzas).
Después hay que sumar la categoría en scripts/enrich-categories.py (texto y guías) y correr los
scripts de siempre (register → prerender-cards → enrich-categories → tailwind → build-sw).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
key, slug, label, color, desc = sys.argv[1:6]
BADGE = f"bg-{color}-100 text-{color}-700 dark:bg-{color}-500/15 dark:text-{color}-300"

data = ROOT / "assets/js/calculators-data.js"
t = data.read_text(encoding="utf-8")
if f"  {key}: {{" not in t:
    entry = f'  {key}: {{\n    label: "{label}",\n    color: "{color}",\n    slug: "{slug}",\n    description:\n      "{desc}",\n  }},\n}};\n\nconst CC_CALCULATORS'
    t = t.replace("};\n\nconst CC_CALCULATORS", entry, 1)
    data.write_text(t, encoding="utf-8")
    print("catálogo: categoría agregada")

for f, fmt in [("assets/js/main.js", '    {c}: "{b}",\n'), ("assets/js/category.js", '    {c}: "{b}",\n'), ("scripts/prerender-cards.py", '    "{c}": "{b}",\n')]:
    p = ROOT / f
    s = p.read_text(encoding="utf-8")
    if f"{color}:" in s or f'"{color}"' in s:
        continue
    line = fmt.format(c=color, b=BADGE)
    anchor = re.search(r'^( *)"?teal"?: "[^"]*",\n', s, re.M)
    s = s[: anchor.end()] + line + s[anchor.end():]
    p.write_text(s, encoding="utf-8")
    print(f, "color", color)

h = ROOT / "index.html"
s = h.read_text(encoding="utf-8")
if f'data-category-filter="{key}"' not in s:
    btn = f'      <button data-category-filter="{key}" class="px-4 py-2 rounded-full text-sm font-semibold surface transition-colors">{label}</button>'
    m = list(re.finditer(r'      <button data-category-filter="[a-z]+" class="px-4 py-2 rounded-full text-sm font-semibold surface transition-colors">[^<]*</button>', s))[-1]
    s = s[: m.end()] + "\n" + btn + s[m.end():]
    h.write_text(s, encoding="utf-8")
    print("home: filtro agregado")

out = ROOT / "calculadoras" / slug / "index.html"
if not out.exists():
    src = (ROOT / "calculadoras/finanzas/index.html").read_text(encoding="utf-8")
    d = src.replace("/calculadoras/finanzas/", f"/calculadoras/{slug}/")
    d = d.replace('data-category="finanzas"', f'data-category="{key}"')
    d = d.replace("Calculadoras de Finanzas Online", f"Calculadoras de {label} Online").replace("Calculadoras de Finanzas", f"Calculadoras de {label}")
    d = d.replace('"name": "Finanzas"', f'"name": "{label}"').replace('aria-current="page">Finanzas<', f'aria-current="page">{label}<')
    d = re.sub(r"    <!-- CC-CATEGORY-GUIDES:START -->.*?<!-- CC-CATEGORY-GUIDES:END -->\n", "", d, flags=re.S)
    d = re.sub(r"<!-- CC-PRERENDER:START -->.*?<!-- CC-PRERENDER:END -->", "<!-- CC-PRERENDER:START --><!-- CC-PRERENDER:END -->", d, flags=re.S)
    d = re.sub(r'<meta property="og:description" content="[^"]*" />', f'<meta property="og:description" content="{desc[:110]}" />', d, count=1)
    assert "inanzas" not in d, "quedaron referencias a Finanzas en la plantilla"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(d, encoding="utf-8")
    print("página de categoría creada:", out.relative_to(ROOT))
