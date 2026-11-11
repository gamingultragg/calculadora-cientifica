"""
register-batch-6.py — Registra el lote 6 (Finanzas + categoría Hogar y Construcción) en el resto del sitio (idempotente):
  - assets/js/calculators-data.js  (catálogo: home, categorías y buscador)
  - sitemap.xml                    (página de categoría + 10 calculadoras + 10 guías)
  - guias/index.html e index.html  (tarjetas de las 10 guías nuevas)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.calculadoracientifica.com.ar"

# ------------------------------------------------------------------ catálogo
CALCS = [
    dict(id="cuotas-vs-contado", title="Cuotas vs Contado", cat="finanzas",
         desc="Tasa real de comprar en cuotas (TEM, TNA, TEA) y si conviene más que el contado.",
         kw=['cuotas', 'contado', 'tasa de interes', 'financiacion', 'recargo', 'tarjeta', 'cuotas sin interes', 'tem'],
         url="/calculadoras/finanzas/cuotas-vs-contado/"),
    dict(id="calculadora-de-inflacion-acumulada", title="Calculadora de Inflación Acumulada", cat="finanzas",
         desc="Inflación acumulada, promedio mensual y anualizada a partir de los datos mensuales.",
         kw=['inflacion', 'inflacion acumulada', 'indec', 'precios', 'poder adquisitivo', 'anualizada'],
         url="/calculadoras/finanzas/calculadora-de-inflacion-acumulada/"),
    dict(id="calculadora-de-ajuste-de-alquiler", title="Calculadora de Ajuste de Alquiler", cat="finanzas",
         desc="Nuevo valor del alquiler por índice (ICL, IPC, CER) o por porcentaje de aumento.",
         kw=['alquiler', 'ajuste de alquiler', 'icl', 'ipc', 'contrato', 'aumento', 'actualizacion'],
         url="/calculadoras/finanzas/calculadora-de-ajuste-de-alquiler/"),
    dict(id="calculadora-de-margen-y-markup", title="Calculadora de Margen y Markup", cat="finanzas",
         desc="Precio de venta, margen y markup a partir del costo, con IVA.",
         kw=['margen', 'markup', 'precio de venta', 'ganancia', 'costo', 'comercio', 'rentabilidad'],
         url="/calculadoras/finanzas/calculadora-de-margen-y-markup/"),
    dict(id="descuentos-sucesivos", title="Calculadora de Descuentos Sucesivos", cat="finanzas",
         desc="Precio final y descuento total de varios descuentos encadenados.",
         kw=['descuento', 'descuentos sucesivos', 'promocion', 'cupon', 'precio final', 'porcentaje'],
         url="/calculadoras/finanzas/descuentos-sucesivos/"),
    dict(id="calculadora-de-ceramicos", title="Calculadora de Cerámicos y Pisos", cat="hogar",
         desc="Cuántas piezas y cajas comprar según el ambiente y la pieza, con desperdicio.",
         kw=['ceramicos', 'pisos', 'porcelanato', 'revestimiento', 'piezas', 'cajas', 'metros cuadrados', 'obra'],
         url="/calculadoras/hogar-y-construccion/calculadora-de-ceramicos/"),
    dict(id="calculadora-de-pintura", title="Calculadora de Pintura", cat="hogar",
         desc="Litros de pintura y latas para paredes y techo de una habitación.",
         kw=['pintura', 'litros', 'paredes', 'techo', 'latex', 'manos', 'rendimiento', 'habitacion'],
         url="/calculadoras/hogar-y-construccion/calculadora-de-pintura/"),
    dict(id="calculadora-de-ladrillos", title="Calculadora de Ladrillos", cat="hogar",
         desc="Cantidad de ladrillos por m² y para tu pared, con junta y desperdicio.",
         kw=['ladrillos', 'pared', 'muro', 'bloques', 'mamposteria', 'obra', 'por metro cuadrado'],
         url="/calculadoras/hogar-y-construccion/calculadora-de-ladrillos/"),
    dict(id="calculadora-de-hormigon", title="Calculadora de Hormigón", cat="hogar",
         desc="Volumen de hormigón y materiales aproximados para losas y columnas.",
         kw=['hormigon', 'concreto', 'losa', 'platea', 'columnas', 'cemento', 'arena', 'piedra', 'm3'],
         url="/calculadoras/hogar-y-construccion/calculadora-de-hormigon/"),
    dict(id="calculadora-de-consumo-electrico", title="Calculadora de Consumo Eléctrico", cat="hogar",
         desc="kWh y costo mensual de cualquier artefacto según su potencia y horas de uso.",
         kw=['consumo electrico', 'kwh', 'watts', 'factura de luz', 'artefacto', 'costo', 'aire acondicionado'],
         url="/calculadoras/hogar-y-construccion/calculadora-de-consumo-electrico/"),
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
GUIDES = ['cuotas-o-contado-como-saber-cual-conviene', 'como-calcular-la-inflacion-acumulada', 'como-calcular-el-ajuste-de-un-alquiler', 'diferencia-entre-margen-y-markup', 'como-calcular-descuentos-sucesivos', 'cuantos-ceramicos-necesito', 'cuanta-pintura-necesito', 'cuantos-ladrillos-necesito-por-m2', 'como-calcular-el-hormigon-de-una-losa', 'como-calcular-el-consumo-electrico']
sm = ROOT / "sitemap.xml"
s = sm.read_text(encoding="utf-8")


def url_block(path, prio, freq="monthly"):
    return f"  <url>\n    <loc>{BASE}{path}</loc>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>\n"


n = 0
CATEGORY_URL = "/calculadoras/hogar-y-construccion/"
new_calcs = ("" if CATEGORY_URL in s else url_block(CATEGORY_URL, "0.8")) + "".join(url_block(c["url"], "0.9") for c in CALCS if c["url"] not in s)
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
    "Vida Diaria": "bg-pink-100 text-pink-700 dark:bg-pink-500/15 dark:text-pink-300",
    "Hogar y Construcción": "bg-cyan-100 text-cyan-700 dark:bg-cyan-500/15 dark:text-cyan-300",
}
CARDS = [('cuotas-o-contado-como-saber-cual-conviene', 'Finanzas', 'Cuotas o contado: cómo saber cuál conviene', 'La tasa real de las cuotas y cuándo conviene financiar frente al contado.'),
    ('como-calcular-la-inflacion-acumulada', 'Finanzas', 'Cómo calcular la inflación acumulada', 'Por qué los porcentajes se componen, cómo anualizar y actualizar un monto.'),
    ('como-calcular-el-ajuste-de-un-alquiler', 'Finanzas', 'Cómo calcular el ajuste de un alquiler', 'Ajuste por índice y por porcentaje, con ejemplos y qué revisar del contrato.'),
    ('diferencia-entre-margen-y-markup', 'Finanzas', 'Diferencia entre margen y markup', 'Las dos fórmulas, la tabla de equivalencias y cómo fijar el precio.'),
    ('como-calcular-descuentos-sucesivos', 'Finanzas', 'Cómo calcular descuentos sucesivos', 'Por qué 20 % + 10 % no es 30 % y cómo sacar el descuento total real.'),
    ('cuantos-ceramicos-necesito', 'Hogar y Construcción', 'Cuántos cerámicos necesito', 'Piezas, cajas y desperdicio para cubrir un ambiente.'),
    ('cuanta-pintura-necesito', 'Hogar y Construcción', 'Cuánta pintura necesito', 'Litros, manos y latas para paredes y techo.'),
    ('cuantos-ladrillos-necesito-por-m2', 'Hogar y Construcción', 'Cuántos ladrillos necesito por m² de pared', 'La fórmula y una tabla con los ladrillos más usados.'),
    ('como-calcular-el-hormigon-de-una-losa', 'Hogar y Construcción', 'Cómo calcular el hormigón de una losa', 'Volumen y materiales aproximados para losas y columnas.'),
    ('como-calcular-el-consumo-electrico', 'Hogar y Construcción', 'Cómo calcular el consumo eléctrico de un artefacto', 'De watts a kWh y cuánto cuesta cada artefacto.')]
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
        if not blocks:  # categoría nueva: va a continuación de la última tarjeta de guía
            blocks = list(BLOCK_RE.finditer(html))
        assert blocks, f"no hay tarjetas en {rel}"
        last = blocks[-1]
        html = html[: last.end()] + "\n" + card(slug, label, title, text_, tag) + html[last.end():]
        count += 1
    path.write_text(html, encoding="utf-8")
    print(f"{rel}: {count} tarjetas nuevas")

