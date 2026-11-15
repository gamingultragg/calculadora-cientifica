"""
register-batch-10.py — Registra el lote 10 en el resto del sitio (idempotente):
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
    dict(id='recta-y-distancia-entre-puntos', title='Recta y Distancia entre Dos Puntos', cat='matematicas',
         desc='Pendiente, ecuación de la recta, distancia y punto medio entre dos puntos.',
         kw=['recta', 'pendiente', 'ecuacion de la recta', 'distancia entre dos puntos', 'punto medio', 'geometria analitica', 'y = mx + b'],
         url='/calculadoras/matematicas-avanzadas/recta-y-distancia-entre-puntos/'),
    dict(id='calculadora-de-logaritmos', title='Calculadora de Logaritmos', cat='matematicas',
         desc='Logaritmo en cualquier base, ln, log y potencias, con comprobación.',
         kw=['logaritmos', 'logaritmo', 'log', 'ln', 'logaritmo natural', 'cambio de base', 'log base 2', 'exponentes'],
         url='/calculadoras/matematicas-avanzadas/calculadora-de-logaritmos/'),
    dict(id='calculadora-de-densidad', title='Densidad, Masa y Volumen', cat='fisica',
         desc='Densidad, masa o volumen con conversión de unidades y flotación en agua.',
         kw=['densidad', 'masa', 'volumen', 'g/cm3', 'kg/m3', 'flota', 'rho', 'densidad del agua'],
         url='/calculadoras/fisica/calculadora-de-densidad/'),
    dict(id='calculadora-de-calor-especifico', title='Calor Específico y Calorimetría', cat='fisica',
         desc='Q = m·c·ΔT: calor, calor específico, masa o variación de temperatura.',
         kw=['calor especifico', 'calorimetria', 'q = mc delta t', 'joules', 'calorias', 'calentar agua', 'equilibrio termico'],
         url='/calculadoras/fisica/calculadora-de-calor-especifico/'),
    dict(id='calculadora-de-movimiento-circular', title='Movimiento Circular Uniforme', cat='fisica',
         desc='Período, frecuencia, rpm, velocidad angular y lineal y aceleración centrípeta.',
         kw=['movimiento circular', 'mcu', 'periodo', 'frecuencia', 'velocidad angular', 'aceleracion centripeta', 'rpm', 'radianes por segundo'],
         url='/calculadoras/fisica/calculadora-de-movimiento-circular/'),
    dict(id='leyes-de-los-gases', title='Leyes de los Gases', cat='quimica',
         desc='Boyle, Charles, Gay-Lussac y ley combinada: presión, volumen o temperatura final.',
         kw=['leyes de los gases', 'boyle', 'charles', 'gay-lussac', 'ley combinada', 'presion volumen temperatura', 'gases'],
         url='/calculadoras/quimica/leyes-de-los-gases/'),
    dict(id='calculadora-de-concentracion-ppm', title='Concentración: ppm y Porcentaje', cat='quimica',
         desc='ppm, mg/L, g/L y % m/v: conversiones y cuánto soluto necesitás.',
         kw=['ppm', 'partes por millon', 'mg/l', 'concentracion', 'porcentaje masa volumen', '% m/v', 'cloro pileta'],
         url='/calculadoras/quimica/calculadora-de-concentracion-ppm/'),
    dict(id='calculadora-de-consumo-de-combustible', title='Consumo de Combustible', cat='vida',
         desc='Rendimiento en km/L y L/100 km, costo del viaje y autonomía del tanque.',
         kw=['consumo de combustible', 'km por litro', 'litros cada 100 km', 'nafta', 'costo de un viaje', 'autonomia', 'rendimiento del auto'],
         url='/calculadoras/vida-diaria/calculadora-de-consumo-de-combustible/'),
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
GUIDES = ['como-calcular-la-pendiente-y-la-distancia-entre-dos-puntos', 'logaritmos-que-son-y-como-calcularlos', 'como-calcular-la-densidad', 'calor-especifico-y-calorimetria', 'movimiento-circular-uniforme-explicado', 'leyes-de-boyle-charles-y-gay-lussac', 'como-calcular-ppm-y-porcentaje-de-concentracion', 'como-calcular-el-consumo-de-combustible-de-un-auto']
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
    ('como-calcular-la-pendiente-y-la-distancia-entre-dos-puntos', 'Matemáticas Avanzadas', 'Cómo calcular la pendiente y la distancia entre dos puntos', 'Pendiente, ecuación de la recta, distancia y punto medio con ejemplos.'),
    ('logaritmos-que-son-y-como-calcularlos', 'Matemáticas Avanzadas', 'Logaritmos: qué son y cómo calcularlos', 'Definición, propiedades, cambio de base y ecuaciones exponenciales.'),
    ('como-calcular-la-densidad', 'Física', 'Cómo calcular la densidad', 'ρ = m/V, unidades, tabla de materiales y ejemplos resueltos.'),
    ('calor-especifico-y-calorimetria', 'Física', 'Calor específico y calorimetría', 'Q = m·c·ΔT con ejemplos de calentamiento y mezclas.'),
    ('movimiento-circular-uniforme-explicado', 'Física', 'Movimiento circular uniforme explicado', 'Período, frecuencia, velocidades y aceleración centrípeta.'),
    ('leyes-de-boyle-charles-y-gay-lussac', 'Química', 'Leyes de Boyle, Charles y Gay-Lussac', 'Cada ley, la ley combinada y por qué se usa kelvin.'),
    ('como-calcular-ppm-y-porcentaje-de-concentracion', 'Química', 'Cómo calcular ppm y porcentaje de concentración', 'ppm, mg/L, g/L y % m/v con ejemplos de cloro y agua salada.'),
    ('como-calcular-el-consumo-de-combustible-de-un-auto', 'Vida Diaria', 'Cómo calcular el consumo de combustible de un auto', 'km/L, L/100 km, costo de un viaje y autonomía.'),
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

