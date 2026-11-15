"""
register-batch-11.py — Registra el lote 11 en el resto del sitio (idempotente):
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
    dict(id='calculadora-de-notacion-cientifica', title='Notación Científica', cat='matematicas',
         desc='Convertí a × 10ⁿ, notación de ingeniería y decimal, y operá con ellos.',
         kw=['notacion cientifica', 'notacion de ingenieria', 'potencias de 10', 'a por 10 a la n', 'numeros muy grandes', 'prefijos del si', 'mantisa'],
         url='/calculadoras/matematicas-avanzadas/calculadora-de-notacion-cientifica/'),
    dict(id='calculadora-de-potencias-y-raices', title='Potencias y Raíces', cat='matematicas',
         desc='Potencias con cualquier exponente, raíces de cualquier índice y radicales simplificados.',
         kw=['potencias', 'raices', 'raiz cuadrada', 'raiz cubica', 'exponentes', 'radicales', 'simplificar raices', 'elevar'],
         url='/calculadoras/matematicas-avanzadas/calculadora-de-potencias-y-raices/'),
    dict(id='calculadora-de-probabilidad', title='Calculadora de Probabilidad', cat='estadistica',
         desc='Probabilidad simple, eventos independientes y al menos un éxito en n intentos.',
         kw=['probabilidad', 'casos favorables', 'eventos independientes', 'probabilidad de dados', 'monedas', 'al menos uno', 'azar'],
         url='/calculadoras/estadistica/calculadora-de-probabilidad/'),
    dict(id='calculadora-de-pendulo-simple', title='Péndulo Simple', cat='fisica',
         desc='Período, longitud o gravedad de un péndulo: T = 2π√(L/g).',
         kw=['pendulo', 'pendulo simple', 'periodo del pendulo', 'oscilaciones', 'gravedad', 'frecuencia', 't = 2 pi raiz l/g'],
         url='/calculadoras/fisica/calculadora-de-pendulo-simple/'),
    dict(id='calculadora-de-ley-de-coulomb', title='Ley de Coulomb', cat='fisica',
         desc='Fuerza entre cargas, distancia o carga con F = k·q₁·q₂/r².',
         kw=['coulomb', 'ley de coulomb', 'fuerza electrica', 'cargas', 'electrostatica', 'microcoulomb', 'atraccion repulsion'],
         url='/calculadoras/fisica/calculadora-de-ley-de-coulomb/'),
    dict(id='calculadora-de-presion', title='Presión y Presión Hidrostática', cat='fisica',
         desc='P = F/A y presión hidrostática ρ·g·h, en Pa, atm, bar, mmHg y psi.',
         kw=['presion', 'presion hidrostatica', 'pascales', 'atmosferas', 'fuerza sobre area', 'profundidad', 'psi', 'bar'],
         url='/calculadoras/fisica/calculadora-de-presion/'),
    dict(id='calculadora-de-escaleras', title='Escaleras', cat='hogar',
         desc='Escalones, contrahuella, huella y recorrido con la fórmula de Blondel.',
         kw=['escaleras', 'escalones', 'contrahuella', 'huella', 'formula de blondel', 'altura de escalon', 'construccion'],
         url='/calculadoras/hogar-y-construccion/calculadora-de-escaleras/'),
    dict(id='calculadora-de-meta-de-ahorro', title='Meta de Ahorro', cat='finanzas',
         desc='Cuánto ahorrar por mes o en cuántos meses llegás a tu meta, con interés opcional.',
         kw=['ahorro', 'meta de ahorro', 'cuanto ahorrar por mes', 'objetivo de ahorro', 'aporte mensual', 'juntar plata', 'tna'],
         url='/calculadoras/finanzas/calculadora-de-meta-de-ahorro/'),
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
GUIDES = ['notacion-cientifica-que-es-y-como-usarla', 'potencias-y-raices-propiedades-y-ejemplos', 'como-calcular-probabilidades', 'periodo-del-pendulo-simple', 'ley-de-coulomb-explicada', 'presion-y-presion-hidrostatica', 'como-calcular-una-escalera', 'como-calcular-cuanto-ahorrar-para-una-meta']
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
    ('notacion-cientifica-que-es-y-como-usarla', 'Matemáticas Avanzadas', 'Notación científica: qué es y cómo usarla', 'Conversión, operaciones, prefijos del SI y ejemplos con números enormes y diminutos.'),
    ('potencias-y-raices-propiedades-y-ejemplos', 'Matemáticas Avanzadas', 'Potencias y raíces: propiedades y ejemplos', 'Propiedades, exponentes negativos y fraccionarios y radicales simplificados.'),
    ('como-calcular-probabilidades', 'Estadística', 'Cómo calcular probabilidades', 'Eventos simples e independientes y al menos un éxito, con dados, monedas y cartas.'),
    ('periodo-del-pendulo-simple', 'Física', 'Período del péndulo simple', 'La fórmula, de qué depende, cómo medir g y ejemplos resueltos.'),
    ('ley-de-coulomb-explicada', 'Física', 'Ley de Coulomb explicada', 'Fórmula, unidades, atracción y repulsión y ejemplos paso a paso.'),
    ('presion-y-presion-hidrostatica', 'Física', 'Presión y presión hidrostática', 'P = F/A, la presión bajo el agua, unidades y ejemplos.'),
    ('como-calcular-una-escalera', 'Hogar y Construcción', 'Cómo calcular una escalera', 'Escalones, contrahuella, huella y la fórmula de Blondel.'),
    ('como-calcular-cuanto-ahorrar-para-una-meta', 'Finanzas', 'Cómo calcular cuánto ahorrar para una meta', 'Aporte mensual, plazo, interés e inflación con ejemplos.'),
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

