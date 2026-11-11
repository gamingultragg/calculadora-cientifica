"""
enrich-categories.py — Actualiza las 6 páginas de categoría (idempotente):
  - texto de introducción y meta description acordes al catálogo actual
  - bloque "Guías de <categoría>" con enlaces internos a todas las guías del tema
  - descripción de cada categoría en assets/js/calculators-data.js
Se corre después de sumar calculadoras o guías nuevas (editar GUIDES abajo).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATS = {
    "matematicas-avanzadas": dict(
        key="matematicas", label="Matemáticas Avanzadas",
        desc="Calculadora científica y básica, ecuaciones de segundo grado, matrices, fracciones, regla de tres, MCD y MCM, teorema de Pitágoras, bases numéricas y áreas y volúmenes, con desarrollo paso a paso.",
        meta="Calculadoras de matemática online y gratis: científica, fracciones, ecuaciones, matrices, regla de tres, MCD y MCM, Pitágoras, bases numéricas y áreas y volúmenes.",
        text="Resolvé desde una cuenta simple hasta un sistema de álgebra lineal. Cada calculadora muestra el desarrollo paso a paso y viene con una guía que explica el método, para que no solo obtengas el resultado sino que entiendas cómo se llega a él.",
        guides=["como-operar-con-fracciones", "regla-de-tres-simple-y-compuesta", "como-calcular-mcd-y-mcm", "teorema-de-pitagoras-explicado",
                "como-calcular-areas-y-volumenes", "como-convertir-binario-decimal-y-hexadecimal", "como-resolver-ecuaciones-de-segundo-grado",
                "determinante-y-matriz-inversa", "grados-y-radianes", "orden-de-operaciones-vs-calculo-secuencial"]),
    "estadistica": dict(
        key="estadistica", label="Estadística",
        desc="Estadística descriptiva, promedio de notas, distribución normal, permutaciones y combinaciones y regresión lineal, para cátedras, tesis e informes.",
        meta="Calculadoras de estadística online y gratis: estadística descriptiva, promedio de notas, distribución normal, combinatoria y regresión lineal.",
        text="Herramientas para analizar datos y resolver problemas de probabilidad y combinatoria: media, mediana, desvío estándar, puntaje Z, permutaciones, combinaciones y la recta de regresión con su correlación.",
        guides=["como-calcular-desviacion-estandar", "puntaje-z-y-curva-normal", "permutaciones-vs-combinaciones", "como-calcular-promedio-de-notas", "regresion-lineal-y-correlacion"]),
    "fisica": dict(
        key="fisica", label="Física",
        desc="Cinemática (MRU y MRUA), segunda ley de Newton, ley de Ohm y energía cinética y potencial, con fórmulas explicadas.",
        meta="Calculadoras de física online y gratis: cinemática MRU y MRUA, leyes de Newton y Ohm, energía cinética y potencial, con fórmulas.",
        text="Calculadoras para los temas centrales de física general: movimiento, fuerza, electricidad y energía. Todas despejan la incógnita que necesites y muestran la fórmula que usan.",
        guides=["formulas-de-mru-y-mrua", "segunda-ley-de-newton-explicada", "ley-de-ohm-explicada", "energia-cinetica-y-potencial-explicada"]),
    "quimica": dict(
        key="quimica", label="Química",
        desc="pH y pOH, molaridad, diluciones, masa molar, moles y gases ideales para química general y analítica.",
        meta="Calculadoras de química online y gratis: pH y pOH, molaridad, diluciones, masa molar, moles y gases ideales, con fórmulas y paso a paso.",
        text="Todo lo que se usa en las prácticas de química general: concentración de soluciones, masa molar de una fórmula, cantidad de sustancia en moles y la ecuación de los gases ideales.",
        guides=["como-calcular-molaridad", "como-calcular-moles", "como-calcular-masa-molar", "como-calcular-ph-y-poh", "como-hacer-una-dilucion", "ley-de-los-gases-ideales"]),
    "ingenieria": dict(
        key="ingenieria", label="Ingeniería",
        desc="Conversión de unidades técnicas y de temperatura, ley de Hooke y resistencias en serie y paralelo.",
        meta="Calculadoras de ingeniería online y gratis: conversor de unidades técnicas y de temperatura, ley de Hooke y resistencias en serie y paralelo.",
        text="Herramientas de uso diario en taller, obra y laboratorio: conversión de presión, caudal, torque y temperatura, cálculo de elasticidad de un resorte y resistencia equivalente de un circuito.",
        guides=["conversion-de-unidades-de-presion", "conversion-de-temperatura-celsius-fahrenheit-kelvin", "ley-de-hooke-y-elasticidad", "resistencias-serie-vs-paralelo"]),
    "finanzas": dict(
        key="finanzas", label="Finanzas",
        desc="Interés simple y compuesto, préstamos con sistema francés, plazo fijo, IVA, porcentajes y aguinaldo.",
        meta="Calculadoras financieras online y gratis para Argentina: interés simple y compuesto, préstamos (sistema francés), plazo fijo, IVA, porcentajes y aguinaldo.",
        text="Calculá cuánto rinde un plazo fijo, cuánto pagás de cuota, cuánto es el IVA o el aguinaldo que te corresponde. Las calculadoras usan las convenciones argentinas (año de 365 días, alícuotas de IVA vigentes) y explican cada fórmula.",
        guides=["como-calcular-un-plazo-fijo-tna-y-tea", "como-calcular-cuota-de-prestamo", "interes-simple-vs-compuesto", "como-calcular-el-aguinaldo", "como-calcular-iva", "como-calcular-porcentajes"]),
}


def guide_title(slug):
    s = (ROOT / "guias" / slug / "index.html").read_text(encoding="utf-8")
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip()


LINK = "text-[var(--color-primary-link)] hover:underline"
for slug, c in CATS.items():
    path = ROOT / "calculadoras" / slug / "index.html"
    html = path.read_text(encoding="utf-8")

    # intro (primer <p> después del h1)
    html = re.sub(r'(<h1 class="[^"]*">[^<]*</h1>\s*<p class="[^"]*">\s*)(.*?)(\s*</p>)',
                  lambda m: m.group(1) + c["desc"] + m.group(3), html, count=1, flags=re.S)
    html = re.sub(r'<meta name="description" content="[^"]*" />', f'<meta name="description" content="{c["meta"]}" />', html, count=1)

    items = "\n".join(f'        <li><a class="{LINK}" href="/guias/{g}/">{guide_title(g)}</a></li>' for g in c["guides"])
    block = f"""    <!-- CC-CATEGORY-GUIDES:START -->
    <section class="mt-10 surface rounded-2xl p-5 shadow-sm">
      <h2 class="font-display font-semibold text-lg mb-2">Guías de {c["label"]}</h2>
      <p class="text-sm text-[var(--color-text-muted)] mb-3">{c["text"]}</p>
      <ul class="grid sm:grid-cols-2 gap-x-6 gap-y-2 text-sm list-disc list-inside">
{items}
      </ul>
    </section>
    <!-- CC-CATEGORY-GUIDES:END -->
"""
    if "CC-CATEGORY-GUIDES:START" in html:
        html = re.sub(r"    <!-- CC-CATEGORY-GUIDES:START -->.*?<!-- CC-CATEGORY-GUIDES:END -->\n", block, html, flags=re.S)
    else:
        html = html.replace('    <aside class="cc-ad" data-ad="cat"', block + '    <aside class="cc-ad" data-ad="cat"', 1)
    path.write_text(html, encoding="utf-8")
    print("categoría:", slug, f"({len(c['guides'])} guías)")

# descripciones en calculators-data.js
data = ROOT / "assets" / "js" / "calculators-data.js"
t = data.read_text(encoding="utf-8")
for slug, c in CATS.items():
    pat = re.compile(r'(slug: "' + re.escape(slug) + r'",\s*description:\s*)"[^"]*"', re.S)
    t, n = pat.subn(lambda m: m.group(1) + '"' + c["desc"].replace('"', '\\"') + '"', t, count=1)
    assert n == 1, slug
data.write_text(t, encoding="utf-8")
print("calculators-data.js: descripciones actualizadas")
