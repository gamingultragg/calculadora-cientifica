"""
register-batch-7b.py — Registra el lote 7b en el resto del sitio (idempotente):
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
    dict(id='caida-libre-y-tiro-oblicuo', title='Caída Libre y Tiro Oblicuo', cat='fisica',
         desc='Tiempo de caída, alcance, altura máxima y tiempo de vuelo, sin rozamiento.',
         kw=['caida libre', 'tiro oblicuo', 'tiro parabolico', 'alcance', 'altura maxima', 'proyectil', 'gravedad'],
         url='/calculadoras/fisica/caida-libre-y-tiro-oblicuo/'),
    dict(id='trabajo-y-potencia', title='Trabajo y Potencia', cat='fisica',
         desc='Trabajo en joules y potencia en W, kW, CV y HP.',
         kw=['trabajo', 'potencia', 'joules', 'watts', 'caballos de fuerza', 'hp', 'cv', 'fuerza'],
         url='/calculadoras/fisica/trabajo-y-potencia/'),
    dict(id='estequiometria-y-reactivo-limitante', title='Estequiometría y Reactivo Limitante', cat='quimica',
         desc='Gramos de producto, reactivo limitante, exceso y rendimiento.',
         kw=['estequiometria', 'reactivo limitante', 'rendimiento', 'gramos', 'moles', 'reaccion quimica'],
         url='/calculadoras/quimica/estequiometria-y-reactivo-limitante/'),
    dict(id='balanceo-de-ecuaciones-quimicas', title='Balanceo de Ecuaciones Químicas', cat='quimica',
         desc='Balanceo automático con verificación de átomos.',
         kw=['balanceo', 'balancear ecuaciones', 'ecuaciones quimicas', 'coeficientes', 'reaccion', 'balanceador'],
         url='/calculadoras/quimica/balanceo-de-ecuaciones-quimicas/'),
    dict(id='codigo-de-colores-de-resistencias', title='Código de Colores de Resistencias', cat='ingenieria',
         desc='Valor y tolerancia de resistencias de 4 y 5 bandas.',
         kw=['resistencias', 'codigo de colores', 'bandas', 'ohms', 'tolerancia', 'electronica'],
         url='/calculadoras/ingenieria/codigo-de-colores-de-resistencias/'),
    dict(id='divisor-de-tension', title='Divisor de Tensión', cat='ingenieria',
         desc='Tensión de salida y resistencias de un divisor resistivo.',
         kw=['divisor de tension', 'voltaje', 'resistencias', 'vout', 'electronica', 'divisor resistivo'],
         url='/calculadoras/ingenieria/divisor-de-tension/'),
    dict(id='resistencia-para-led', title='Resistencia para LED', cat='ingenieria',
         desc='Qué resistencia poner a un LED, con valor comercial.',
         kw=['led', 'resistencia para led', 'resistencia limitadora', 'diodo', 'corriente', 'electronica'],
         url='/calculadoras/ingenieria/resistencia-para-led/'),
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
GUIDES = ['caida-libre-y-tiro-oblicuo-explicados', 'trabajo-y-potencia-mecanica', 'estequiometria-y-reactivo-limitante-paso-a-paso', 'como-balancear-ecuaciones-quimicas', 'como-leer-el-codigo-de-colores-de-resistencias', 'como-funciona-un-divisor-de-tension', 'que-resistencia-poner-a-un-led']
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
    ('caida-libre-y-tiro-oblicuo-explicados', 'Física', 'Caída libre y tiro oblicuo explicados', 'Tiempo, alcance, altura máxima y ejemplos resueltos.'),
    ('trabajo-y-potencia-mecanica', 'Física', 'Trabajo y potencia mecánica', 'W = F·d·cos θ, P = W/t y las unidades con ejemplos.'),
    ('estequiometria-y-reactivo-limitante-paso-a-paso', 'Química', 'Estequiometría y reactivo limitante paso a paso', 'De gramos a gramos, limitante y rendimiento.'),
    ('como-balancear-ecuaciones-quimicas', 'Química', 'Cómo balancear ecuaciones químicas', 'Tanteo y método algebraico con ejemplos.'),
    ('como-leer-el-codigo-de-colores-de-resistencias', 'Ingeniería', 'Cómo leer el código de colores de resistencias', 'La tabla completa y ejemplos de 4 y 5 bandas.'),
    ('como-funciona-un-divisor-de-tension', 'Ingeniería', 'Cómo funciona un divisor de tensión', 'Fórmula, ejemplos y limitaciones.'),
    ('que-resistencia-poner-a-un-led', 'Ingeniería', 'Qué resistencia poner a un LED', 'El cálculo, los valores comerciales y varios LED en serie.'),
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

