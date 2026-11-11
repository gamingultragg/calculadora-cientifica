"""
register-batch-4.py — Registra el lote 4 en el resto del sitio (idempotente):
  - assets/js/calculators-data.js  (catálogo: home, categorías y buscador)
  - sitemap.xml                    (6 calculadoras + 6 guías)
  - guias/index.html e index.html  (tarjetas de las 6 guías nuevas, en su categoría)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.calculadoracientifica.com.ar"

# ------------------------------------------------------------------ catálogo
CALCS = [
    dict(id="calculadora-de-moles", title="Calculadora de Moles", cat="quimica",
         desc="Moles a partir de la masa, la molaridad y el volumen, las partículas o el volumen de un gas.",
         kw=["moles", "moles de soluto", "calcular moles", "mol", "numero de avogadro", "gramos a moles", "soluto"],
         url="/calculadoras/quimica/calculadora-de-moles/"),
    dict(id="calculadora-de-plazo-fijo", title="Calculadora de Plazo Fijo y Tasas (TNA y TEA)", cat="finanzas",
         desc="Interés y monto de un plazo fijo, y conversión entre TNA y TEA con año de 365 días.",
         kw=["plazo fijo", "tna", "tea", "tasa nominal", "tasa efectiva", "rendimiento", "interes", "banco", "inversion"],
         url="/calculadoras/finanzas/calculadora-de-plazo-fijo/"),
    dict(id="calculadora-de-areas-y-volumenes", title="Calculadora de Áreas, Perímetros y Volúmenes", cat="matematicas",
         desc="Área, perímetro, volumen y superficie de 14 figuras geométricas, con sus fórmulas.",
         kw=["area", "volumen", "perimetro", "circulo", "cilindro", "esfera", "cono", "geometria", "triangulo", "rectangulo"],
         url="/calculadoras/matematicas-avanzadas/calculadora-de-areas-y-volumenes/"),
    dict(id="energia-cinetica-y-potencial", title="Energía Cinética y Potencial", cat="fisica",
         desc="Ec = ½·m·v² y Ep = m·g·h, con despeje de masa, velocidad o altura.",
         kw=["energia cinetica", "energia potencial", "joules", "energia mecanica", "velocidad", "altura", "masa"],
         url="/calculadoras/fisica/energia-cinetica-y-potencial/"),
    dict(id="regresion-lineal", title="Regresión Lineal", cat="estadistica",
         desc="Recta de regresión, pendiente, correlación r y R² a partir de pares de datos.",
         kw=["regresion lineal", "correlacion", "minimos cuadrados", "pendiente", "recta", "r2", "prediccion"],
         url="/calculadoras/estadistica/regresion-lineal/"),
    dict(id="conversor-de-temperatura", title="Conversor de Temperatura", cat="ingenieria",
         desc="Celsius, Fahrenheit, Kelvin y Rankine al instante, con sus fórmulas.",
         kw=["temperatura", "celsius", "fahrenheit", "kelvin", "grados", "conversor", "rankine"],
         url="/calculadoras/ingenieria/conversor-de-temperatura/"),
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
GUIDES = ["como-calcular-moles", "como-calcular-un-plazo-fijo-tna-y-tea", "como-calcular-areas-y-volumenes", "energia-cinetica-y-potencial-explicada", "regresion-lineal-y-correlacion", "conversion-de-temperatura-celsius-fahrenheit-kelvin"]
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
    "Física": "bg-orange-100 text-orange-700 dark:bg-orange-500/15 dark:text-orange-300",
    "Ingeniería": "bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300",
}
CARDS = [
    ("como-calcular-moles", "Química", "Cómo calcular los moles de soluto y de cualquier sustancia", "Las cuatro formas de calcular moles, con ejemplos resueltos."),
    ("como-calcular-un-plazo-fijo-tna-y-tea", "Finanzas", "Cómo calcular un plazo fijo: TNA y TEA", "Fórmula del interés, TNA vs TEA y cómo compararlas con la inflación."),
    ("como-calcular-areas-y-volumenes", "Matemáticas Avanzadas", "Cómo calcular áreas y volúmenes", "Fórmulas de figuras planas y cuerpos, con ejemplos y equivalencias."),
    ("energia-cinetica-y-potencial-explicada", "Física", "Energía cinética y potencial explicadas", "Ec = ½mv², Ep = mgh y la conservación de la energía mecánica."),
    ("regresion-lineal-y-correlacion", "Estadística", "Regresión lineal y correlación", "Recta de regresión, r y R² con un ejemplo resuelto paso a paso."),
    ("conversion-de-temperatura-celsius-fahrenheit-kelvin", "Ingeniería", "Cómo convertir entre Celsius, Fahrenheit y Kelvin", "Fórmulas de conversión, tabla de referencia y un truco para estimar."),
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

