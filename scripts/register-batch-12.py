"""
register-batch-12.py — Registra el lote 12 en el resto del sitio (idempotente):
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
    dict(id='calculadora-de-peso-ideal', title='Peso Ideal', cat='vida',
         desc='Tu rango de peso saludable por IMC y el peso ideal con cuatro fórmulas clásicas.',
         kw=['peso ideal', 'peso saludable', 'cuanto debo pesar', 'formula de devine', 'peso segun altura', 'rango de peso', 'imc'],
         url='/calculadoras/vida-diaria/calculadora-de-peso-ideal/'),
    dict(id='calculadora-de-fecha-probable-de-parto', title='Fecha Probable de Parto', cat='vida',
         desc='Fecha probable de parto, semanas de embarazo y trimestre desde la FUM o la concepción.',
         kw=['fecha probable de parto', 'fpp', 'semanas de embarazo', 'embarazo', 'calcular fecha de parto', 'regla de naegele', 'fum'],
         url='/calculadoras/vida-diaria/calculadora-de-fecha-probable-de-parto/'),
    dict(id='calculadora-de-gravitacion-universal', title='Gravitación Universal', cat='fisica',
         desc='Fuerza gravitatoria, gravedad de un planeta y velocidad orbital.',
         kw=['gravitacion universal', 'ley de newton gravitacion', 'fuerza gravitatoria', 'gravedad de la luna', 'velocidad orbital', 'velocidad de escape', 'satelites'],
         url='/calculadoras/fisica/calculadora-de-gravitacion-universal/'),
    dict(id='calculadora-de-ley-de-snell', title='Ley de Snell', cat='fisica',
         desc='Ángulo de refracción, índice de refracción y ángulo crítico de la luz.',
         kw=['ley de snell', 'refraccion', 'indice de refraccion', 'angulo critico', 'reflexion total interna', 'optica', 'luz'],
         url='/calculadoras/fisica/calculadora-de-ley-de-snell/'),
    dict(id='calculadora-de-medias', title='Medias: Aritmética, Geométrica y Armónica', cat='estadistica',
         desc='Las cuatro medias de una lista de números en un solo paso.',
         kw=['media aritmetica', 'media geometrica', 'media armonica', 'media cuadratica', 'promedio', 'crecimiento promedio', 'velocidad media'],
         url='/calculadoras/estadistica/calculadora-de-medias/'),
    dict(id='calculadora-de-error-absoluto-y-relativo', title='Error Absoluto, Relativo y Porcentual', cat='estadistica',
         desc='Errores de una medición e incertidumbre de una serie de mediciones.',
         kw=['error absoluto', 'error relativo', 'error porcentual', 'incertidumbre', 'error estandar', 'laboratorio', 'exactitud y precision'],
         url='/calculadoras/estadistica/calculadora-de-error-absoluto-y-relativo/'),
    dict(id='calculadora-de-propiedades-coligativas', title='Propiedades Coligativas', cat='quimica',
         desc='Descenso crioscópico y ascenso ebulloscópico de una solución.',
         kw=['propiedades coligativas', 'descenso crioscopico', 'ascenso ebulloscopico', 'punto de congelacion', 'punto de ebullicion', 'molalidad', "van't hoff"],
         url='/calculadoras/quimica/calculadora-de-propiedades-coligativas/'),
    dict(id='calculadora-de-pendiente-de-rampa', title='Pendiente de Rampa', cat='hogar',
         desc='Pendiente en % y grados, largo necesario y desnivel de una rampa.',
         kw=['pendiente de rampa', 'rampa', 'pendiente en porcentaje', 'rampa accesible', 'grados a porcentaje', 'largo de rampa', 'construccion'],
         url='/calculadoras/hogar-y-construccion/calculadora-de-pendiente-de-rampa/'),
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
GUIDES = ['como-calcular-el-peso-ideal', 'como-calcular-la-fecha-probable-de-parto', 'ley-de-gravitacion-universal-explicada', 'ley-de-snell-y-refraccion-de-la-luz', 'media-aritmetica-geometrica-y-armonica', 'error-absoluto-relativo-y-porcentual', 'propiedades-coligativas-crioscopia-y-ebulloscopia', 'como-calcular-la-pendiente-de-una-rampa']
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
CARDS = [
    ('como-calcular-el-peso-ideal', 'Vida Diaria', 'Cómo calcular el peso ideal', 'Cuatro fórmulas, el rango por IMC y sus límites, con ejemplos.'),
    ('como-calcular-la-fecha-probable-de-parto', 'Vida Diaria', 'Cómo calcular la fecha probable de parto', 'Regla de Naegele, ajuste por ciclo, semanas y trimestres.'),
    ('ley-de-gravitacion-universal-explicada', 'Física', 'Ley de gravitación universal explicada', 'Fuerza, gravedad de los planetas y órbitas, con ejemplos.'),
    ('ley-de-snell-y-refraccion-de-la-luz', 'Física', 'Ley de Snell y refracción de la luz', 'Índices de refracción, ángulo crítico y reflexión total.'),
    ('media-aritmetica-geometrica-y-armonica', 'Estadística', 'Media aritmética, geométrica y armónica', 'Cuándo usar cada media, con crecimiento, velocidades y precios.'),
    ('error-absoluto-relativo-y-porcentual', 'Estadística', 'Error absoluto, relativo y porcentual', 'Errores de medición, error estándar y exactitud vs. precisión.'),
    ('propiedades-coligativas-crioscopia-y-ebulloscopia', 'Química', 'Propiedades coligativas: crioscopía y ebulloscopía', "ΔT = i·K·m, factor de van't Hoff y ejemplos con sal y anticongelante."),
    ('como-calcular-la-pendiente-de-una-rampa', 'Hogar y Construcción', 'Cómo calcular la pendiente de una rampa', 'Pendiente en % y grados, largo necesario y accesibilidad.'),
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

