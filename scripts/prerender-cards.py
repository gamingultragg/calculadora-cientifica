"""
prerender-cards.py — Pre-renderiza en el HTML las tarjetas de calculadoras
que antes solo dibujaba JavaScript (home y landing pages de categoría).

Por qué: Google descubre y pondera mejor los enlaces que están en el HTML
inicial que los que aparecen recién después de ejecutar JS. Con las tarjetas
estáticas, la home y cada categoría enlazan directo a todas las calculadoras.

La fuente única de verdad sigue siendo assets/js/calculators-data.js. El JS
(main.js / category.js) sigue funcionando igual: al cargar redibuja las mismas
tarjetas (búsqueda y filtros), así que no hay salto visual.

Idempotente: reemplaza el contenido entre los marcadores
<!-- CC-PRERENDER:START --> y <!-- CC-PRERENDER:END -->. Volver a correrlo después
de tocar calculators-data.js deja todo sincronizado.

Uso:
    python scripts/prerender-cards.py
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START = "<!-- CC-PRERENDER:START -->"
END = "<!-- CC-PRERENDER:END -->"

COLORS = {
    "blue": "bg-blue-100 text-blue-700 dark:bg-blue-500/15 dark:text-blue-300",
    "violet": "bg-violet-100 text-violet-700 dark:bg-violet-500/15 dark:text-violet-300",
    "orange": "bg-orange-100 text-orange-700 dark:bg-orange-500/15 dark:text-orange-300",
    "green": "bg-green-100 text-green-700 dark:bg-green-500/15 dark:text-green-300",
    "amber": "bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300",
    "teal": "bg-teal-100 text-teal-700 dark:bg-teal-500/15 dark:text-teal-300",
    "cyan": "bg-cyan-100 text-cyan-700 dark:bg-cyan-500/15 dark:text-cyan-300",
    "pink": "bg-pink-100 text-pink-700 dark:bg-pink-500/15 dark:text-pink-300",
}
ARROW = (
    '<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">'
    '<path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>'
)
CARD_CLASS = "surface block rounded-2xl p-5 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-150"


def load_data():
    js = (ROOT / "assets" / "js" / "calculators-data.js").read_text(encoding="utf-8")
    node_code = (
        "const vm=require('vm');const s=require('fs').readFileSync(0,'utf8');"
        "const ctx={};vm.runInNewContext(s+';this.C=CC_CATEGORIES;this.L=CC_CALCULATORS;',ctx);"
        "process.stdout.write(JSON.stringify({c:ctx.C,l:ctx.L}));"
    )
    out = subprocess.run(["node", "-e", node_code], input=js, capture_output=True, text=True, encoding="utf-8", check=True)
    data = json.loads(out.stdout)
    return data["c"], data["l"]


def card(calc, cats, home):
    cat = cats[calc["category"]]
    badge = f'<span class="badge {COLORS[cat["color"]]}">{cat["label"]}</span>'
    if home:
        badge = f'<div class="flex items-start justify-between gap-3">{badge}</div>'
    return (
        f'<a href="{calc["url"]}" class="{CARD_CLASS}">'
        f"{badge}"
        f'<h3 class="mt-3 font-display font-semibold text-lg text-[var(--color-text)]">{calc["title"]}</h3>'
        f'<p class="mt-1.5 text-sm text-[var(--color-text-muted)] leading-relaxed">{calc["description"]}</p>'
        f'<span class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-[var(--color-primary-link)]">'
        f"Abrir calculadora {ARROW}</span></a>"
    )


def inject(text, grid_id, cards_html):
    """Pone cards_html dentro del <div id=grid_id ...>...</div> (entre marcadores)."""
    block = f"{START}{cards_html}{END}"
    if START in text:
        return re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block, text, count=1, flags=re.S)
    pattern = re.compile(r'(<div id="%s"[^>]*>)(\s*)(</div>)' % re.escape(grid_id))
    new, n = pattern.subn(lambda m: m.group(1) + block + m.group(3), text, count=1)
    if n == 0:
        raise RuntimeError(f"No se encontró el contenedor #{grid_id}")
    return new


def main():
    cats, calcs = load_data()
    live = [c for c in calcs if c.get("status") == "live"]
    order = list(cats.keys())

    # Home: todas, agrupadas por categoría (igual que main.js).
    home_calcs = sorted(live, key=lambda c: order.index(c["category"]))
    home_path = ROOT / "index.html"
    text = home_path.read_text(encoding="utf-8")
    text = inject(text, "calc-grid", "".join(card(c, cats, True) for c in home_calcs))
    n = len(home_calcs)
    text = re.sub(
        r'(<span id="calc-result-count"[^>]*>)[^<]*(</span>)',
        lambda m: f'{m.group(1)}{n} {"resultado" if n == 1 else "resultados"}{m.group(2)}',
        text,
        count=1,
    )
    home_path.write_text(text, encoding="utf-8")
    print(f"home: {n} tarjetas")

    # Landing pages de categoría.
    for page in sorted((ROOT / "calculadoras").glob("*/index.html")):
        html = page.read_text(encoding="utf-8")
        m = re.search(r'<body[^>]*data-category="(\w+)"', html)
        if not m or 'id="cat-grid"' not in html:
            continue
        key = m.group(1)
        mine = [c for c in live if c["category"] == key]
        html = inject(html, "cat-grid", "".join(card(c, cats, False) for c in mine))
        page.write_text(html, encoding="utf-8")
        print(f"{page.parent.name}: {len(mine)} tarjetas")


if __name__ == "__main__":
    main()
