"""
register-batch-2.py — Registra el lote 2 en el resto del sitio (idempotente):
  - assets/js/calculators-data.js  (catálogo: home, categorías y buscador)
  - sitemap.xml                    (5 calculadoras + 4 guías)
  - guias/index.html e index.html  (tarjetas de las 4 guías nuevas, en su categoría)
  - guias/interes-simple-vs-compuesto: enlace a la calculadora de interés simple
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.calculadoracientifica.com.ar"

# ------------------------------------------------------------------ catálogo
CALCS = [
    dict(id="calculadora-de-masa-molar", title="Calculadora de Masa Molar", cat="quimica",
         desc="Masa molar de cualquier fórmula (H₂SO₄, Ca(OH)₂, hidratos), con desglose y % en masa.",
         kw=["masa molar", "peso molecular", "formula quimica", "gramos por mol", "composicion porcentual", "moles"],
         url="/calculadoras/quimica/calculadora-de-masa-molar/"),
    dict(id="calculadora-de-promedio-de-notas", title="Calculadora de Promedio de Notas", cat="estadistica",
         desc="Promedio simple o ponderado, y qué nota necesitás para llegar a tu objetivo.",
         kw=["promedio", "notas", "ponderado", "calificaciones", "aprobar", "parcial", "final"],
         url="/calculadoras/estadistica/calculadora-de-promedio-de-notas/"),
    dict(id="regla-de-tres", title="Regla de Tres", cat="matematicas",
         desc="Regla de tres simple directa, inversa y compuesta, con el desarrollo paso a paso.",
         kw=["regla de tres", "proporcion", "proporcionalidad", "directa", "inversa", "compuesta"],
         url="/calculadoras/matematicas-avanzadas/regla-de-tres/"),
    dict(id="calculadora-de-interes-simple", title="Interés Simple", cat="finanzas",
         desc="Interés, monto, capital, tasa o tiempo con I = C·i·t, en años, meses o días.",
         kw=["interes simple", "capital", "tasa", "monto", "plazo fijo", "prestamo", "interes"],
         url="/calculadoras/finanzas/calculadora-de-interes-simple/"),
    dict(id="mcd-y-mcm", title="MCD y MCM", cat="matematicas",
         desc="Máximo común divisor y mínimo común múltiplo, con factores primos y Euclides.",
         kw=["mcd", "mcm", "maximo comun divisor", "minimo comun multiplo", "divisores", "multiplos", "euclides", "factores primos"],
         url="/calculadoras/matematicas-avanzadas/mcd-y-mcm/"),
]

data = ROOT / "assets" / "js" / "calculators-data.js"
text = data.read_text(encoding="utf-8")
added = 0
for c in CALCS:
    if f'id: "{c["id"]}"' in text:
        continue
    kw = ", ".join(f'"{k}"' for k in c["kw"])
    block = (
        f'  {{\n    id: "{c["id"]}",\n    title: "{c["title"]}",\n    description: "{c["desc"]}",\n'
        f'    category: "{c["cat"]}",\n    keywords: [{kw}],\n    url: "{c["url"]}",\n    status: "live",\n  }},\n'
    )
    text = text.rstrip()
    assert text.endswith("];"), "formato inesperado en calculators-data.js"
    text = text[:-2] + block + "];\n"
    added += 1
data.write_text(text, encoding="utf-8")
print(f"calculators-data.js: {added} entradas nuevas")

# ------------------------------------------------------------------- sitemap
GUIDES = ["como-calcular-masa-molar", "como-calcular-promedio-de-notas", "regla-de-tres-simple-y-compuesta", "como-calcular-mcd-y-mcm"]
sm = ROOT / "sitemap.xml"
s = sm.read_text(encoding="utf-8")


def url_block(path, prio, freq="monthly"):
    return f"  <url>\n    <loc>{BASE}{path}</loc>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>\n"


n = 0
new_calcs = "".join(url_block(c["url"], "0.9") for c in CALCS if c["url"] not in s)
if new_calcs:
    s = s.replace("\n  <!-- Guías -->", "\n" + new_calcs.rstrip("\n") + "\n\n  <!-- Guías -->", 1)
    n += new_calcs.count("<url>")
new_guides = "".join(url_block(f"/guias/{g}/", "0.7") for g in GUIDES if f"/guias/{g}/" not in s)
if new_guides:
    s = s.replace("\n  <!-- Institucional -->", "\n" + new_guides.rstrip("\n") + "\n\n  <!-- Institucional -->", 1)
    n += new_guides.count("<url>")
sm.write_text(s, encoding="utf-8")
print(f"sitemap.xml: {n} URLs nuevas")

# ------------------------------------------------------------ tarjetas de guías
BADGE = {
    "Matemáticas Avanzadas": "bg-blue-100 text-blue-700 dark:bg-blue-500/15 dark:text-blue-300",
    "Estadística": "bg-violet-100 text-violet-700 dark:bg-violet-500/15 dark:text-violet-300",
    "Química": "bg-green-100 text-green-700 dark:bg-green-500/15 dark:text-green-300",
    "Finanzas": "bg-teal-100 text-teal-700 dark:bg-teal-500/15 dark:text-teal-300",
}
CARDS = [
    ("como-calcular-masa-molar", "Química", "Cómo calcular la masa molar", "Sumar masas atómicas paso a paso, con paréntesis e hidratos."),
    ("como-calcular-promedio-de-notas", "Estadística", "Cómo calcular el promedio de notas", "Promedio simple, ponderado y qué nota necesitás para tu objetivo."),
    ("regla-de-tres-simple-y-compuesta", "Matemáticas Avanzadas", "Regla de tres simple y compuesta", "Directa, inversa y compuesta, con el truco para distinguirlas."),
    ("como-calcular-mcd-y-mcm", "Matemáticas Avanzadas", "Cómo calcular el MCD y el MCM", "Factores primos y Euclides, con ejemplos y para qué sirven."),
]
ARROW = ('<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">'
         '<path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>')
BLOCK_RE = re.compile(r'      <a href="/guias/[^"]+/"\n.*?</a>\n', re.S)


def card(slug, label, title, text_, tag):
    return (
        f'      <a href="/guias/{slug}/"\n'
        f'        class="surface block rounded-2xl p-5 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-150">\n'
        f'        <span class="badge {BADGE[label]}">{label}</span>\n'
        f'        <{tag} class="mt-3 font-display font-semibold text-lg text-[var(--color-text)]">{title}</{tag}>\n'
        f'        <p class="mt-1.5 text-sm text-[var(--color-text-muted)] leading-relaxed">{text_}</p>\n'
        f'        <span class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-[var(--color-primary-link)]">\n'
        f'          Leer guía\n          {ARROW}\n        </span>\n      </a>\n'
    )


for rel, tag in [("guias/index.html", "h2"), ("index.html", "h3")]:
    path = ROOT / rel
    html = path.read_text(encoding="utf-8")
    count = 0
    for slug, label, title, text_ in CARDS:
        if f'href="/guias/{slug}/"' in html:
            continue
        blocks = [m for m in BLOCK_RE.finditer(html) if f'class="badge {BADGE[label]}">{label}<' in m.group(0)]
        assert blocks, f"no hay tarjetas de {label} en {rel}"
        last = blocks[-1]
        html = html[: last.end()] + "\n" + card(slug, label, title, text_, tag) + html[last.end():]
        count += 1
    path.write_text(html, encoding="utf-8")
    print(f"{rel}: {count} tarjetas nuevas")

# ------------------------------------------- enlace en la guía de interés simple
g = ROOT / "guias" / "interes-simple-vs-compuesto" / "index.html"
gt = g.read_text(encoding="utf-8")
link = '        <li><a class="text-[var(--color-primary-link)] hover:underline" href="/calculadoras/finanzas/calculadora-de-interes-simple/">Interés Simple</a></li>\n'
if "calculadora-de-interes-simple" not in gt:
    anchor = '        <li><a class="text-[var(--color-primary-link)] hover:underline" href="/calculadoras/finanzas/interes-compuesto/">Interés Compuesto</a></li>\n'
    assert anchor in gt
    gt = gt.replace(anchor, link + anchor, 1)
    g.write_text(gt, encoding="utf-8")
    print("guía interes-simple-vs-compuesto: enlace agregado")
