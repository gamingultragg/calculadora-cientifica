"""
register-batch-3.py — Registra el lote 3 en el resto del sitio (idempotente):
  - assets/js/calculators-data.js  (catálogo: home, categorías y buscador)
  - sitemap.xml                    (5 calculadoras + 5 guías)
  - guias/index.html e index.html  (tarjetas de las 5 guías nuevas, en su categoría)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.calculadoracientifica.com.ar"

# ------------------------------------------------------------------ catálogo
CALCS = [
    dict(id="calculadora-de-fracciones", title="Calculadora de Fracciones", cat="matematicas",
         desc="Suma, resta, multiplica, divide y simplifica fracciones, con números mixtos y paso a paso.",
         kw=["fracciones", "sumar fracciones", "simplificar", "numero mixto", "denominador comun", "dividir fracciones"],
         url="/calculadoras/matematicas-avanzadas/calculadora-de-fracciones/"),
    dict(id="teorema-de-pitagoras", title="Teorema de Pitágoras", cat="matematicas",
         desc="Hipotenusa o cateto de un triángulo rectángulo, con área, perímetro y ángulos.",
         kw=["pitagoras", "hipotenusa", "cateto", "triangulo rectangulo", "teorema", "terna pitagorica"],
         url="/calculadoras/matematicas-avanzadas/teorema-de-pitagoras/"),
    dict(id="conversor-de-bases-numericas", title="Conversor de Bases Numéricas", cat="matematicas",
         desc="Binario, octal, decimal, hexadecimal y cualquier base de 2 a 36, con el desarrollo paso a paso.",
         kw=["binario", "hexadecimal", "octal", "decimal", "bases numericas", "conversor", "sistema numerico"],
         url="/calculadoras/matematicas-avanzadas/conversor-de-bases-numericas/"),
    dict(id="calculadora-de-aguinaldo", title="Calculadora de Aguinaldo (SAC)", cat="finanzas",
         desc="Aguinaldo bruto, neto y proporcional en Argentina, a partir de tu mejor sueldo del semestre.",
         kw=["aguinaldo", "sac", "sueldo anual complementario", "sueldo", "proporcional", "argentina", "mejor remuneracion"],
         url="/calculadoras/finanzas/calculadora-de-aguinaldo/"),
    dict(id="calculadora-de-gases-ideales", title="Calculadora de Gases Ideales", cat="quimica",
         desc="Presión, volumen, moles o temperatura con la ecuación PV = nRT, con conversión de unidades.",
         kw=["gases ideales", "pv=nrt", "presion", "volumen", "moles", "temperatura", "ley de los gases", "constante r"],
         url="/calculadoras/quimica/calculadora-de-gases-ideales/"),
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
GUIDES = ["como-operar-con-fracciones", "teorema-de-pitagoras-explicado", "como-calcular-el-aguinaldo", "ley-de-los-gases-ideales", "como-convertir-binario-decimal-y-hexadecimal"]
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
    ("como-operar-con-fracciones", "Matemáticas Avanzadas", "Cómo operar con fracciones", "Suma, resta, multiplicación, división y simplificación con ejemplos."),
    ("teorema-de-pitagoras-explicado", "Matemáticas Avanzadas", "El teorema de Pitágoras explicado", "Hipotenusa, catetos, ternas pitagóricas y ejemplos de la vida real."),
    ("como-convertir-binario-decimal-y-hexadecimal", "Matemáticas Avanzadas", "Cómo convertir entre binario, decimal y hexadecimal", "Divisiones sucesivas, suma de potencias y tabla de equivalencias."),
    ("como-calcular-el-aguinaldo", "Finanzas", "Cómo calcular el aguinaldo (SAC)", "El 50% de la mejor remuneración, proporcional, descuentos y fechas de pago."),
    ("ley-de-los-gases-ideales", "Química", "La ley de los gases ideales", "PV = nRT, la constante R, ejemplos resueltos y las leyes de Boyle y Charles."),
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

