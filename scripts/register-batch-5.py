"""
register-batch-5.py — Registra el lote 5 (categoría Vida Diaria) en el resto del sitio (idempotente):
  - assets/js/calculators-data.js  (catálogo: home, categorías y buscador)
  - sitemap.xml                    (página de categoría + 5 calculadoras + 5 guías)
  - guias/index.html e index.html  (tarjetas de las 5 guías nuevas)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.calculadoracientifica.com.ar"

# ------------------------------------------------------------------ catálogo
CALCS = [
    dict(id="calculadora-de-edad-y-fechas", title="Calculadora de Edad y Fechas", cat="vida",
         desc="Edad exacta, días entre dos fechas (con días hábiles) y qué fecha será dentro de X tiempo.",
         kw=["edad", "fechas", "dias entre fechas", "cumpleanos", "fecha de nacimiento", "dias habiles", "sumar dias", "calendario"],
         url="/calculadoras/vida-diaria/calculadora-de-edad-y-fechas/"),
    dict(id="calculadora-de-imc", title="Calculadora de IMC", cat="vida",
         desc="Índice de masa corporal, categoría de la OMS y rango de peso saludable para tu altura.",
         kw=["imc", "indice de masa corporal", "peso", "altura", "peso ideal", "peso saludable", "obesidad", "bajo peso"],
         url="/calculadoras/vida-diaria/calculadora-de-imc/"),
    dict(id="conversor-de-cocina", title="Conversor de Cocina", cat="vida",
         desc="Tazas, cucharadas, cucharaditas, ml y gramos de 15 ingredientes comunes.",
         kw=["cocina", "tazas", "cucharadas", "gramos", "harina", "azucar", "equivalencias", "receta", "medidas"],
         url="/calculadoras/vida-diaria/conversor-de-cocina/"),
    dict(id="calculadora-de-horas-trabajadas", title="Calculadora de Horas Trabajadas", cat="vida",
         desc="Horas entre entrada y salida, descanso, turnos nocturnos, horas extra y valor de la hora.",
         kw=["horas trabajadas", "horas extra", "entrada", "salida", "turno nocturno", "jornada", "sueldo por hora", "fichaje"],
         url="/calculadoras/vida-diaria/calculadora-de-horas-trabajadas/"),
    dict(id="calculadora-de-propina", title="Calculadora de Propina y División de la Cuenta", cat="vida",
         desc="Propina, total y cuánto paga cada persona, con redondeo hacia arriba.",
         kw=["propina", "dividir la cuenta", "restaurante", "cuenta", "personas", "10%", "cubierto"],
         url="/calculadoras/vida-diaria/calculadora-de-propina/"),
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
GUIDES = ["como-calcular-la-edad-y-los-dias-entre-fechas", "como-calcular-el-imc", "equivalencias-de-cocina-tazas-cucharadas-y-gramos", "como-calcular-horas-trabajadas-y-horas-extra", "como-calcular-la-propina-y-dividir-la-cuenta"]
sm = ROOT / "sitemap.xml"
s = sm.read_text(encoding="utf-8")


def url_block(path, prio, freq="monthly"):
    return f"  <url>\n    <loc>{BASE}{path}</loc>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>\n"


n = 0
CATEGORY_URL = "/calculadoras/vida-diaria/"
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
}
CARDS = [
    ("como-calcular-la-edad-y-los-dias-entre-fechas", "Vida Diaria", "Cómo calcular la edad y los días entre dos fechas", "Años, meses y días exactos, años bisiestos y suma de tiempo a una fecha."),
    ("como-calcular-el-imc", "Vida Diaria", "Cómo calcular e interpretar el IMC", "Fórmula, categorías de la OMS, rango de peso saludable y limitaciones."),
    ("equivalencias-de-cocina-tazas-cucharadas-y-gramos", "Vida Diaria", "Equivalencias de cocina: tazas, cucharadas y gramos", "Tabla de medidas y gramos por taza de los ingredientes más usados."),
    ("como-calcular-horas-trabajadas-y-horas-extra", "Vida Diaria", "Cómo calcular horas trabajadas y horas extra", "Turnos nocturnos, decimales y recargos del 50 % y 100 %."),
    ("como-calcular-la-propina-y-dividir-la-cuenta", "Vida Diaria", "Cómo calcular la propina y dividir la cuenta", "Cuánto dejar, cómo dividir y cómo redondear sin perder la cuenta."),
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
        if not blocks:  # categoría nueva: va a continuación de la última tarjeta de guía
            blocks = list(BLOCK_RE.finditer(html))
        assert blocks, f"no hay tarjetas en {rel}"
        last = blocks[-1]
        html = html[: last.end()] + "\n" + card(slug, label, title, text_, tag) + html[last.end():]
        count += 1
    path.write_text(html, encoding="utf-8")
    print(f"{rel}: {count} tarjetas nuevas")

