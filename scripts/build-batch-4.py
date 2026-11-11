"""
build-batch-4.py — Genera las 6 calculadoras del lote 4: moles, plazo fijo (TNA/TEA), áreas y
volúmenes, energía cinética y potencial, regresión lineal y conversor de temperatura.
Los script.js se escriben a mano en cada carpeta; este script solo produce los index.html.
Generación de una sola vez: después, el HTML de cada página es la fuente de verdad.
"""
from pathlib import Path

from page_templates import calc_page

ROOT = Path(__file__).resolve().parent.parent
INPUT = ('class="w-full rounded-xl surface px-3 py-2.5 font-numeric focus:outline-none '
         'focus:ring-2 focus:ring-[var(--color-primary)]"')
SELECT = ('class="w-full rounded-xl surface px-3 py-2.5 focus:outline-none '
          'focus:ring-2 focus:ring-[var(--color-primary)]"')
BTN = 'class="calc-btn calc-btn--op w-full py-2.5"'
LABEL = 'class="block text-sm font-medium mb-1"'
CHIP = ('class="px-3 py-1.5 rounded-full surface text-xs font-semibold font-numeric '
        'hover:shadow-md transition-shadow"')
H3 = 'class="font-semibold text-[var(--color-text)] mb-1"'
FORMULA = 'class="font-numeric text-[var(--color-text)]"'
RESULT_H2 = 'class="font-display font-semibold text-lg mb-3"'
MUTED = "text-[var(--color-text-muted)]"
PRIMARY = "text-[var(--color-primary-link)]"


def field(id_, label, placeholder, extra="", value="", label_id=""):
    v = f' value="{value}"' if value else ""
    lid = f' id="{label_id}"' if label_id else ""
    return (f'        <div{extra}>\n          <label{lid} for="{id_}" {LABEL}>{label}</label>\n'
            f'          <input id="{id_}" type="text" inputmode="decimal" placeholder="{placeholder}"{v} {INPUT} />\n        </div>')


def chips(items):
    return "".join(f'<button type="button" data-example="{v}" {CHIP}>{l}</button>' for l, v in items)


def result_simple(prefix, extra_after=""):
    return f"""        <section id="{prefix}-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>Resultado</h2>
          <p id="{prefix}-label" class="text-sm {MUTED}"></p>
          <p id="{prefix}-main" class="font-numeric text-3xl font-bold {PRIMARY} break-all">—</p>
          <div id="{prefix}-lines" class="mt-3 text-sm {MUTED} space-y-1"></div>{extra_after}
        </section>"""


def write(rel, html):
    path = ROOT / rel / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("escrito:", path.relative_to(ROOT))


# ---------------------------------------------------------------------- moles
write("calculadoras/quimica/calculadora-de-moles", calc_page(
    slug="calculadora-de-moles", cat_slug="quimica", cat_label="Química", name="Calculadora de Moles",
    page_title="Calculadora de Moles: Moles de Soluto, a partir de la Masa y de Gases | Calculadora Científica",
    desc="Calculá los moles de una sustancia a partir de su masa y masa molar, de la molaridad y el volumen (moles de soluto), del número de partículas o del volumen de un gas. Gratis.",
    og_title="Calculadora de Moles (moles de soluto y de cualquier sustancia)",
    og_desc="Moles a partir de la masa, la molaridad y el volumen, las partículas o el volumen de gas. Gratis.",
    schema_desc="Calcula la cantidad de sustancia en moles a partir de la masa y la masa molar, de la molaridad y el volumen de solución (moles de soluto), del número de partículas o del volumen de un gas en condiciones normales, y convierte moles a gramos.",
    intro="Elegí de qué dato partís (masa, molaridad y volumen, partículas o volumen de gas) y obtené los moles, con la masa, el número de partículas y el volumen de gas equivalentes. También pasa de moles a gramos.",
    form_html=f"""        <div class="space-y-4">
          <div>
            <label for="mo-mode" {LABEL}>Quiero calcular…</label>
            <select id="mo-mode" {SELECT}>
              <option value="masa">Moles a partir de la masa (n = m / M)</option>
              <option value="molaridad">Moles de soluto a partir de la molaridad y el volumen (n = M × V)</option>
              <option value="particulas">Moles a partir del número de partículas</option>
              <option value="gas">Moles de un gas a partir de su volumen (CNPT)</option>
              <option value="gramos">Gramos a partir de los moles (m = n × M)</option>
            </select>
          </div>
{field("mo-mass", "Masa (g)", "Ej: 49", ' data-field="mass"')}
{field("mo-moles", "Moles (mol)", "Ej: 0,5", ' data-field="moles"')}
{field("mo-molar", "Masa molar (g/mol)", "Ej: 98,08", ' data-field="molar"')}
{field("mo-molarity", "Molaridad (mol/L)", "Ej: 0,1", ' data-field="molarity"')}
          <div data-field="volume">
            <label for="mo-volume" {LABEL}>Volumen de la solución</label>
            <div class="grid grid-cols-[1fr_auto] gap-2">
              <input id="mo-volume" type="text" inputmode="decimal" placeholder="Ej: 250" {INPUT} />
              <select id="mo-volume-unit" aria-label="Unidad de volumen" {SELECT}><option value="ml">mL</option><option value="l">L</option></select>
            </div>
          </div>
{field("mo-particles", "Número de partículas", "Ej: 3,01e23", ' data-field="particles"')}
{field("mo-gasvol", "Volumen del gas (L) a 0 °C y 1 atm", "Ej: 44,8", ' data-field="gasvol"')}
          <div class="flex flex-wrap gap-2" aria-label="Ejemplos">{chips([("49 g de H₂SO₄", "masa|49|98,08"), ("0,1 M en 250 mL", "molaridad|0,1|250"), ("3,01e23 partículas", "particulas|3,01e23"), ("44,8 L de gas", "gas|44,8"), ("0,5 mol → g", "gramos|0,5|98,08")])}</div>
          <button id="mo-solve" type="button" {BTN}>Calcular</button>
          <p class="text-xs {MUTED}">¿No sabés la masa molar? Calculala con la <a class="underline" href="/calculadoras/quimica/calculadora-de-masa-molar/">calculadora de masa molar</a>.</p>
        </div>""",
    result_html=result_simple("mo"),
    help_html=f"""            <div>
              <h3 {H3}>Moles a partir de la masa</h3>
              <p {FORMULA}>n = m / M</p>
              <p>n son los moles, m la masa en gramos y M la masa molar en g/mol (la suma de las masas atómicas de la fórmula).</p>
            </div>
            <div>
              <h3 {H3}>Moles de soluto (molaridad)</h3>
              <p {FORMULA}>n = M × V</p>
              <p>Con la molaridad en mol/L y el volumen de la solución en litros. Una solución 0,1 M en 250 mL contiene 0,1 × 0,25 = 0,025 mol de soluto.</p>
            </div>
            <div>
              <h3 {H3}>Partículas y gases</h3>
              <p {FORMULA}>n = N / Nₐ &nbsp;·&nbsp; n = V / 22,414 L (a 0 °C y 1 atm)</p>
              <p>El número de Avogadro (Nₐ = 6,022 × 10²³) es la cantidad de partículas en un mol. En condiciones normales, un mol de gas ideal ocupa 22,414 L.</p>
            </div>""",
    related=[("/calculadoras/quimica/calculadora-de-molaridad/", "Calculadora de Molaridad"),
             ("/calculadoras/quimica/calculadora-de-masa-molar/", "Calculadora de Masa Molar"),
             ("/calculadoras/quimica/calculadora-de-gases-ideales/", "Calculadora de Gases Ideales")],
    guide=("/guias/como-calcular-moles/", "Cómo calcular los moles de soluto y de cualquier sustancia",
           "Leé la guía completa: las cuatro formas de calcular moles, con ejemplos resueltos y los errores más comunes."),
    faqs=[("¿Cómo se calculan los moles de soluto?",
           "Multiplicando la molaridad por el volumen de la solución en litros: n = M × V. Si tenés 250 mL de una solución 0,1 M, hay 0,1 × 0,25 = 0,025 mol de soluto. Si en cambio tenés la masa del soluto, n = m / M."),
          ("¿Cómo se calculan los moles a partir de los gramos?",
           "Se divide la masa por la masa molar: n = m / M. Con 49 g de H₂SO₄ (98,08 g/mol): 49 / 98,08 = 0,4996 mol."),
          ("¿Cómo se pasa de moles a gramos?",
           "Multiplicando por la masa molar: m = n × M. 0,5 mol de H₂SO₄ son 0,5 × 98,08 = 49,04 g."),
          ("¿Cuántas partículas hay en un mol?",
           "6,022 × 10²³ (el número de Avogadro), ya sean átomos, moléculas o iones."),
          ("¿Cuántos moles hay en un litro de gas?",
           "En condiciones normales (0 °C y 1 atm), un mol ocupa 22,414 L, así que 1 L son 0,0446 mol. A otras presiones o temperaturas se usa la ecuación de los gases ideales.")],
))

# ----------------------------------------------------------------- plazo fijo
write("calculadoras/finanzas/calculadora-de-plazo-fijo", calc_page(
    slug="calculadora-de-plazo-fijo", cat_slug="finanzas", cat_label="Finanzas", name="Calculadora de Plazo Fijo y Tasas (TNA y TEA)",
    page_title="Calculadora de Plazo Fijo: Interés, TNA y TEA | Calculadora Científica",
    desc="Calculá cuánto ganás con un plazo fijo según la TNA y los días, y convertí tasas entre TNA y TEA. Con año de 365 días, como lo hacen los bancos en Argentina. Gratis.",
    og_title="Calculadora de Plazo Fijo, TNA y TEA",
    og_desc="Interés de un plazo fijo y conversión entre TNA y TEA, con año de 365 días. Gratis.",
    schema_desc="Calcula el interés y el monto final de un plazo fijo a partir de la TNA y los días, y convierte entre tasa nominal anual (TNA) y tasa efectiva anual (TEA) con año de 365 días.",
    intro="Ingresá el capital, la TNA y los días y calculá el interés y el monto de un plazo fijo, con la TEA equivalente. También convierte entre TNA y TEA con la capitalización que elijas.",
    form_html=f"""        <div class="space-y-4">
          <div>
            <label for="pf-mode" {LABEL}>¿Qué querés calcular?</label>
            <select id="pf-mode" {SELECT}>
              <option value="plazo">Interés y monto de un plazo fijo</option>
              <option value="tna-tea">De TNA a TEA</option>
              <option value="tea-tna">De TEA a TNA</option>
            </select>
          </div>
{field("pf-capital", "Capital ($)", "Ej: 1000000", ' data-field="capital"')}
{field("pf-tna", "TNA — tasa nominal anual (%)", "Ej: 40", ' data-field="tna"')}
{field("pf-tea", "TEA — tasa efectiva anual (%)", "Ej: 50", ' data-field="tea"')}
{field("pf-dias", "Plazo (días)", "Ej: 30", ' data-field="dias"', value="30", label_id="pf-dias-label")}
          <div class="flex flex-wrap gap-2" aria-label="Ejemplos">{chips([("$1.000.000 al 40 % a 30 días", "plazo|1000000|40|30"), ("TNA 40 % → TEA", "tna-tea|40|30"), ("TEA 50 % → TNA", "tea-tna|50|30")])}</div>
          <button id="pf-solve" type="button" {BTN}>Calcular</button>
        </div>""",
    result_html=result_simple("pf"),
    help_html=f"""            <div>
              <h3 {H3}>Interés de un plazo fijo</h3>
              <p {FORMULA}>Interés = Capital × TNA × días / 365</p>
              <p>En Argentina los bancos usan el año de 365 días. Con $1.000.000 al 40 % TNA a 30 días: 1.000.000 × 0,40 × 30 / 365 = $32.876,71.</p>
            </div>
            <div>
              <h3 {H3}>TNA y TEA</h3>
              <p>La <strong>TNA</strong> (tasa nominal anual) es la tasa "de cartel": no incluye reinversión. La <strong>TEA</strong> (tasa efectiva anual) sí: es lo que rendiría el capital en un año si reinvertís el interés cada vez que vence el plazo.</p>
              <p {FORMULA}>TEA = (1 + TNA × d/365)^(365/d) − 1</p>
            </div>
            <div>
              <h3 {H3}>De TEA a TNA</h3>
              <p {FORMULA}>TNA = ((1 + TEA)^(d/365) − 1) × 365/d</p>
              <p>d son los días de cada período de capitalización (30 para plazos fijos mensuales). La TEA siempre es mayor o igual que la TNA.</p>
            </div>""",
    related=[("/calculadoras/finanzas/interes-compuesto/", "Interés Compuesto"),
             ("/calculadoras/finanzas/calculadora-de-interes-simple/", "Interés Simple"),
             ("/calculadoras/finanzas/amortizacion-prestamos/", "Amortización de Préstamos")],
    guide=("/guias/como-calcular-un-plazo-fijo-tna-y-tea/", "Cómo calcular un plazo fijo: TNA y TEA",
           "Leé la guía completa: la fórmula del interés, la diferencia entre TNA y TEA y cómo comparar tasas."),
    faqs=[("¿Cómo se calcula el interés de un plazo fijo?",
           "Con Capital × TNA × días / 365. Con $1.000.000, una TNA del 40 % y 30 días, el interés es $32.876,71 y el monto final $1.032.876,71."),
          ("¿Qué diferencia hay entre TNA y TEA?",
           "La TNA no considera la reinversión de los intereses; la TEA sí. Una TNA del 40 % con capitalización cada 30 días equivale a una TEA de 48,23 %."),
          ("¿Cómo se pasa de TNA a TEA?",
           "TEA = (1 + TNA × d/365)^(365/d) − 1, donde d es el plazo en días. Para 40 % y 30 días: (1 + 0,40 × 30/365)^(365/30) − 1 = 0,4823."),
          ("¿Por qué se usa 365 días?",
           "Es la convención de los bancos argentinos para tasas anuales: se prorratea el año en 365 días, aunque el plazo fijo dure 30, 60 o 90 días."),
          ("¿Esta calculadora descuenta impuestos o inflación?",
           "No: calcula el interés bruto nominal. La ganancia real depende de la inflación del período, que se compara aparte.")],
))

# ---------------------------------------------------------- áreas y volúmenes
SHAPES_OPTS = [
    ("cuadrado", "Cuadrado"), ("rectangulo", "Rectángulo"), ("triangulo", "Triángulo (base y altura)"),
    ("triangulo-lados", "Triángulo (tres lados)"), ("circulo", "Círculo"), ("trapecio", "Trapecio"),
    ("rombo", "Rombo"), ("paralelogramo", "Paralelogramo"), ("cubo", "Cubo"), ("prisma", "Prisma rectangular"),
    ("cilindro", "Cilindro"), ("cono", "Cono"), ("esfera", "Esfera"), ("piramide", "Pirámide de base cuadrada"),
]
shape_options = "".join(f'<option value="{v}">{t}</option>' for v, t in SHAPES_OPTS)
dims = "\n".join(
    f"""          <div id="av-wrap-{i}"{' class="hidden"' if i else ''}>
            <label id="av-label-{i}" for="av-f{i}" {LABEL}>Dato {i + 1}</label>
            <input id="av-f{i}" type="text" inputmode="decimal" placeholder="Ej: {['5', '3', '4'][i]}" {INPUT} />
          </div>""" for i in range(3))
write("calculadoras/matematicas-avanzadas/calculadora-de-areas-y-volumenes", calc_page(
    slug="calculadora-de-areas-y-volumenes", cat_slug="matematicas-avanzadas", cat_label="Matemáticas Avanzadas",
    name="Calculadora de Áreas, Perímetros y Volúmenes",
    page_title="Calculadora de Áreas y Volúmenes: Figuras Planas y Cuerpos Geométricos | Calculadora Científica",
    desc="Calculá el área y el perímetro de cuadrados, rectángulos, triángulos, círculos y más, y el volumen y la superficie de cubos, cilindros, conos, esferas y pirámides. Con fórmulas. Gratis.",
    og_title="Calculadora de Áreas, Perímetros y Volúmenes",
    og_desc="Área, perímetro, volumen y superficie de 14 figuras geométricas, con sus fórmulas.",
    schema_desc="Calcula el área y el perímetro de figuras planas (cuadrado, rectángulo, triángulo, círculo, trapecio, rombo, paralelogramo) y el volumen y la superficie de cuerpos geométricos (cubo, prisma, cilindro, cono, esfera, pirámide).",
    intro="Elegí la figura, ingresá sus medidas y obtené el área y el perímetro (figuras planas) o el volumen y la superficie (cuerpos), con la fórmula usada en cada caso.",
    form_html=f"""        <div class="space-y-4">
          <div>
            <label for="av-shape" {LABEL}>Figura</label>
            <select id="av-shape" {SELECT}>{shape_options}</select>
          </div>
{dims}
          <div>
            <label for="av-unit" {LABEL}>Unidad de longitud</label>
            <select id="av-unit" {SELECT}><option value="cm">cm</option><option value="m">m</option><option value="mm">mm</option><option value="km">km</option><option value="pulg">pulgadas</option></select>
          </div>
          <div class="flex flex-wrap gap-2" aria-label="Ejemplos">{chips([("círculo r = 5", "circulo|5"), ("rectángulo 3 × 4", "rectangulo|3|4"), ("cilindro r = 2, h = 10", "cilindro|2|10"), ("esfera r = 3", "esfera|3"), ("cono r = 3, h = 4", "cono|3|4")])}</div>
          <button id="av-solve" type="button" {BTN}>Calcular</button>
        </div>""",
    result_html=result_simple("av"),
    help_html=f"""            <div>
              <h3 {H3}>Figuras planas</h3>
              <p {FORMULA}>Cuadrado: A = l² · Rectángulo: A = b·h · Triángulo: A = b·h/2 · Círculo: A = π·r²</p>
              <p {FORMULA}>Trapecio: A = (B + b)·h/2 · Rombo: A = D·d/2 · Paralelogramo: A = b·h</p>
              <p>El perímetro es la suma de los lados; en el círculo se llama circunferencia: 2·π·r.</p>
            </div>
            <div>
              <h3 {H3}>Triángulo con tres lados (Herón)</h3>
              <p {FORMULA}>s = (a + b + c) / 2 &nbsp;·&nbsp; A = √(s·(s−a)·(s−b)·(s−c))</p>
              <p>Sirve cuando no conocés la altura. Los lados tienen que cumplir la desigualdad triangular.</p>
            </div>
            <div>
              <h3 {H3}>Cuerpos geométricos</h3>
              <p {FORMULA}>Cubo: V = a³ · Prisma: V = a·b·c · Cilindro: V = π·r²·h · Cono: V = π·r²·h/3</p>
              <p {FORMULA}>Esfera: V = 4/3·π·r³ · Pirámide: V = (área de la base × h)/3</p>
              <p>La superficie es la suma de las áreas de todas las caras. Las áreas están en unidades cuadradas (cm²) y los volúmenes en cúbicas (cm³).</p>
            </div>""",
    related=[("/calculadoras/matematicas-avanzadas/teorema-de-pitagoras/", "Teorema de Pitágoras"),
             ("/calculadoras/ingenieria/conversor-de-unidades/", "Conversor de Unidades Técnicas"),
             ("/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/", "Calculadora Científica Online")],
    guide=("/guias/como-calcular-areas-y-volumenes/", "Cómo calcular áreas y volúmenes",
           "Leé la guía completa: todas las fórmulas de áreas y volúmenes con ejemplos resueltos y la diferencia entre área, superficie y volumen."),
    faqs=[("¿Cómo se calcula el área de un círculo?",
           "Con A = π·r². Un círculo de radio 5 cm tiene un área de 3,1416 × 25 = 78,54 cm²."),
          ("¿Cuál es la diferencia entre área y volumen?",
           "El área mide una superficie (cm², m²); el volumen mide el espacio que ocupa un cuerpo (cm³, m³)."),
          ("¿Cómo se calcula el volumen de un cilindro?",
           "V = π·r²·h: el área de la base por la altura. Con r = 2 y h = 10: 3,1416 × 4 × 10 = 125,66."),
          ("¿Cómo se calcula el área de un triángulo sin la altura?",
           "Con la fórmula de Herón: se calcula el semiperímetro s = (a + b + c)/2 y el área es √(s·(s−a)·(s−b)·(s−c)). Para 3, 4 y 5 da 6."),
          ("¿En qué unidades da el resultado?",
           "En la unidad que elijas, al cuadrado para áreas (cm²) y al cubo para volúmenes (cm³).")],
))

# ----------------------------------------------------------------- energía
write("calculadoras/fisica/energia-cinetica-y-potencial", calc_page(
    slug="energia-cinetica-y-potencial", cat_slug="fisica", cat_label="Física", name="Calculadora de Energía Cinética y Potencial",
    page_title="Calculadora de Energía Cinética y Potencial: Ec = ½mv² y Ep = mgh | Calculadora Científica",
    desc="Calculá la energía cinética (½·m·v²) y la energía potencial gravitatoria (m·g·h), o despejá la masa, la velocidad o la altura. Con equivalencias en kJ, kcal y kWh. Gratis.",
    og_title="Calculadora de Energía Cinética y Potencial",
    og_desc="Ec = ½·m·v² y Ep = m·g·h, con despeje de masa, velocidad o altura. Gratis.",
    schema_desc="Calcula la energía cinética (Ec = ½mv²) y la energía potencial gravitatoria (Ep = mgh), y permite despejar la masa, la velocidad o la altura.",
    intro="Elegí el tipo de energía, qué querés calcular y completá los datos. Obtenés el resultado en joules, con su equivalente en kilojoules, kilocalorías y kWh.",
    form_html=f"""        <div class="space-y-4">
          <div>
            <label for="en-type" {LABEL}>Tipo de energía</label>
            <select id="en-type" {SELECT}>
              <option value="cinetica">Cinética (Ec = ½·m·v²)</option>
              <option value="potencial">Potencial gravitatoria (Ep = m·g·h)</option>
            </select>
          </div>
          <div>
            <label for="en-target" {LABEL}>¿Qué querés calcular?</label>
            <select id="en-target" {SELECT}>
              <option value="energia">Energía</option>
              <option value="masa">Masa</option>
              <option id="en-target-var" value="variable">Velocidad</option>
            </select>
          </div>
{field("en-E", "Energía (J)", "Ej: 200000", ' data-field="E"')}
{field("en-m", "Masa (kg)", "Ej: 1000", ' data-field="m"')}
          <div data-field="v">
            <label for="en-v" {LABEL}>Velocidad</label>
            <div class="grid grid-cols-[1fr_auto] gap-2">
              <input id="en-v" type="text" inputmode="decimal" placeholder="Ej: 20" {INPUT} />
              <select id="en-v-unit" aria-label="Unidad de velocidad" {SELECT}><option value="ms">m/s</option><option value="kmh">km/h</option></select>
            </div>
          </div>
{field("en-g", "Gravedad g (m/s²)", "9,81", ' data-field="g"', value="9,81")}
{field("en-h", "Altura (m)", "Ej: 10", ' data-field="h"')}
          <div class="flex flex-wrap gap-2" aria-label="Ejemplos">{chips([("auto de 1000 kg a 20 m/s", "cinetica|energia|1000|20"), ("70 kg a 10 m de altura", "potencial|energia|70|9,81|10"), ("velocidad con Ec = 200000 J, 1000 kg", "cinetica|variable|200000|1000")])}</div>
          <button id="en-solve" type="button" {BTN}>Calcular</button>
        </div>""",
    result_html=result_simple("en"),
    help_html=f"""            <div>
              <h3 {H3}>Energía cinética</h3>
              <p {FORMULA}>Ec = ½ · m · v²</p>
              <p>Es la energía que tiene un cuerpo por estar en movimiento. Depende del <strong>cuadrado</strong> de la velocidad: al duplicar la velocidad, la energía se cuadruplica.</p>
            </div>
            <div>
              <h3 {H3}>Energía potencial gravitatoria</h3>
              <p {FORMULA}>Ep = m · g · h</p>
              <p>Es la energía almacenada por la altura h sobre un nivel de referencia, con g = 9,81 m/s² cerca de la superficie terrestre.</p>
            </div>
            <div>
              <h3 {H3}>Unidades</h3>
              <p>La energía se mide en joules (J): 1 J = 1 kg·m²/s². Además, 1 kcal = 4184 J y 1 kWh = 3,6 × 10⁶ J. Para la velocidad: 1 m/s = 3,6 km/h.</p>
            </div>
            <div>
              <h3 {H3}>Conservación de la energía mecánica</h3>
              <p {FORMULA}>Em = Ec + Ep = constante (sin rozamiento)</p>
              <p>Un objeto que cae pierde energía potencial y gana la misma cantidad de energía cinética.</p>
            </div>""",
    related=[("/calculadoras/fisica/segunda-ley-de-newton/", "Segunda Ley de Newton"),
             ("/calculadoras/fisica/cinematica-mru-mrua/", "Cinemática (MRU / MRUA)"),
             ("/calculadoras/fisica/ley-de-ohm/", "Ley de Ohm")],
    guide=("/guias/energia-cinetica-y-potencial-explicada/", "Energía cinética y potencial explicadas",
           "Leé la guía completa: las dos fórmulas, la conservación de la energía mecánica y ejemplos resueltos."),
    faqs=[("¿Cómo se calcula la energía cinética?",
           "Con Ec = ½·m·v². Un auto de 1000 kg a 20 m/s tiene Ec = 0,5 × 1000 × 400 = 200.000 J (200 kJ)."),
          ("¿Cómo se calcula la energía potencial?",
           "Con Ep = m·g·h. Una persona de 70 kg a 10 m de altura tiene Ep = 70 × 9,81 × 10 = 6867 J."),
          ("¿Por qué la velocidad está al cuadrado?",
           "Porque la energía necesaria para llevar un cuerpo hasta una velocidad crece con el cuadrado de esa velocidad: a doble velocidad, cuádruple energía (y distancia de frenado)."),
          ("¿Qué unidad tiene la energía?",
           "El joule (J). Para otras magnitudes se usan el kilojoule (1000 J), la kilocaloría (4184 J) y el kWh (3,6 millones de J)."),
          ("¿Qué pasa con la energía de un objeto que cae?",
           "La energía potencial se convierte en cinética: sin rozamiento, la suma de ambas (energía mecánica) se mantiene constante.")],
))

# --------------------------------------------------------- regresión lineal
write("calculadoras/estadistica/regresion-lineal", calc_page(
    slug="regresion-lineal", cat_slug="estadistica", cat_label="Estadística", name="Calculadora de Regresión Lineal",
    page_title="Calculadora de Regresión Lineal: Recta, Pendiente y Correlación | Calculadora Científica",
    desc="Calculá la recta de regresión lineal por mínimos cuadrados (y = a + bx), el coeficiente de correlación r y R² a partir de tus datos, y hacé predicciones. Gratis.",
    og_title="Calculadora de Regresión Lineal",
    og_desc="Recta de regresión, pendiente, correlación r y R² a partir de pares de datos.",
    schema_desc="Calcula la recta de regresión lineal por mínimos cuadrados, el coeficiente de correlación de Pearson r, el coeficiente de determinación R² y predicciones a partir de pares de datos (x, y).",
    intro="Pegá tus pares de datos (uno por línea, x e y separados por un espacio) y obtené la recta de regresión, la pendiente, la ordenada al origen, el coeficiente de correlación r y R², con una predicción opcional.",
    form_html=f"""        <div class="space-y-4">
          <div>
            <label for="rl-data" {LABEL}>Datos (un par x y por línea)</label>
            <textarea id="rl-data" rows="8" spellcheck="false" placeholder="1 2&#10;2 3&#10;3 5&#10;4 4&#10;5 6" class="w-full rounded-xl surface px-3 py-2.5 font-numeric focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]"></textarea>
          </div>
{field("rl-predict", "Predecir y para x = (opcional)", "Ej: 6")}
          <div class="flex flex-wrap gap-2" aria-label="Ejemplos"><button type="button" data-example="1 2;2 3;3 5;4 4;5 6" data-predict="6" {CHIP}>Ejemplo: 5 puntos</button><button type="button" data-example="1 2;2 4;3 6;4 8" {CHIP}>Relación perfecta</button><button type="button" data-example="1 8;2 6;3 5;4 3;5 1" data-predict="6" {CHIP}>Correlación negativa</button></div>
          <button id="rl-solve" type="button" {BTN}>Calcular regresión</button>
        </div>""",
    result_html=result_simple("rl").replace('<p id="rl-label" class="text-sm text-[var(--color-text-muted)]"></p>', '<p class="text-sm text-[var(--color-text-muted)]">Recta de regresión</p>'),
    help_html=f"""            <div>
              <h3 {H3}>Mínimos cuadrados</h3>
              <p {FORMULA}>b = (n·Σxy − Σx·Σy) / (n·Σx² − (Σx)²) &nbsp;·&nbsp; a = ȳ − b·x̄</p>
              <p>Es la recta y = a + b·x que minimiza la suma de los cuadrados de las distancias verticales a los puntos. b es la pendiente y a la ordenada al origen.</p>
            </div>
            <div>
              <h3 {H3}>Coeficiente de correlación r</h3>
              <p {FORMULA}>r = (n·Σxy − Σx·Σy) / √[(n·Σx² − (Σx)²)(n·Σy² − (Σy)²)]</p>
              <p>Va de −1 a 1: cerca de 1 hay relación lineal positiva fuerte, cerca de −1 negativa fuerte y cerca de 0 no hay relación lineal.</p>
            </div>
            <div>
              <h3 {H3}>R² (coeficiente de determinación)</h3>
              <p>Es r² y se interpreta como la proporción de la variación de y que explica la recta. R² = 0,81 significa que x explica el 81 % de la variación de y.</p>
            </div>
            <div>
              <h3 {H3}>Cuidado con extrapolar</h3>
              <p>Las predicciones son confiables dentro del rango de tus datos. Fuera de ese rango, y ante una correlación baja, pueden alejarse mucho de la realidad. Correlación no implica causalidad.</p>
            </div>""",
    related=[("/calculadoras/estadistica/calculadora-estadistica-descriptiva/", "Estadística Descriptiva"),
             ("/calculadoras/estadistica/distribucion-normal/", "Distribución Normal (Puntaje Z)"),
             ("/calculadoras/estadistica/calculadora-de-promedio-de-notas/", "Calculadora de Promedio de Notas")],
    guide=("/guias/regresion-lineal-y-correlacion/", "Regresión lineal y correlación, explicadas",
           "Leé la guía completa: cómo se obtiene la recta, cómo interpretar r y R² y los errores más comunes."),
    faqs=[("¿Qué es la regresión lineal?",
           "Es un método para ajustar la recta y = a + b·x que mejor describe la relación entre dos variables, minimizando la suma de los errores al cuadrado (mínimos cuadrados)."),
          ("¿Cómo se interpreta el coeficiente de correlación r?",
           "Mide la fuerza y el sentido de la relación lineal: entre −1 y 1. Cerca de ±1, relación fuerte; cerca de 0, casi nula. El signo indica si y crece (+) o decrece (−) cuando crece x."),
          ("¿Qué significa R²?",
           "Es el cuadrado de r e indica qué proporción de la variación de y queda explicada por la recta. Con R² = 0,81, el 81 %."),
          ("¿Cuántos datos hacen falta?",
           "Mínimo dos pares, pero con pocos puntos el resultado es poco confiable. Cuantos más datos y más representativos, mejor."),
          ("¿Correlación significa causalidad?",
           "No. Que dos variables se muevan juntas no prueba que una cause a la otra: pueden depender de un tercer factor o coincidir por azar.")],
))

# ---------------------------------------------------------------- temperatura
write("calculadoras/ingenieria/conversor-de-temperatura", calc_page(
    slug="conversor-de-temperatura", cat_slug="ingenieria", cat_label="Ingeniería", name="Conversor de Temperatura",
    page_title="Conversor de Temperatura: Celsius, Fahrenheit, Kelvin y Rankine | Calculadora Científica",
    desc="Convertí temperaturas entre grados Celsius, Fahrenheit, Kelvin y Rankine al instante, con las fórmulas de conversión. Gratis y sin registro.",
    og_title="Conversor de Temperatura",
    og_desc="Celsius, Fahrenheit, Kelvin y Rankine al instante, con sus fórmulas.",
    schema_desc="Convierte temperaturas entre las escalas Celsius, Fahrenheit, Kelvin y Rankine, con las fórmulas de conversión.",
    intro="Escribí una temperatura, elegí su escala y mirá al instante su equivalente en Celsius, Fahrenheit, Kelvin y Rankine.",
    form_html=f"""        <div class="space-y-4">
{field("tp-value", "Temperatura", "Ej: 100")}
          <div>
            <label for="tp-from" {LABEL}>Escala</label>
            <select id="tp-from" {SELECT}>
              <option value="c">Celsius (°C)</option>
              <option value="f">Fahrenheit (°F)</option>
              <option value="k">Kelvin (K)</option>
              <option value="r">Rankine (°R)</option>
            </select>
          </div>
          <div class="flex flex-wrap gap-2" aria-label="Ejemplos">{chips([("100 °C", "100|c"), ("32 °F", "32|f"), ("0 K", "0|k"), ("−40 °C", "-40|c"), ("37 °C", "37|c")])}</div>
          <button id="tp-solve" type="button" {BTN}>Convertir</button>
        </div>""",
    result_html=f"""        <section id="tp-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>Resultado</h2>
          <div id="tp-rows"></div>
        </section>""",
    help_html=f"""            <div>
              <h3 {H3}>Fórmulas de conversión</h3>
              <p {FORMULA}>°F = °C × 9/5 + 32 &nbsp;·&nbsp; °C = (°F − 32) × 5/9</p>
              <p {FORMULA}>K = °C + 273,15 &nbsp;·&nbsp; °R = °F + 459,67</p>
            </div>
            <div>
              <h3 {H3}>Puntos de referencia</h3>
              <p>El agua se congela a 0 °C (32 °F, 273,15 K) y hierve a 100 °C (212 °F, 373,15 K) al nivel del mar. La temperatura corporal normal es de unos 37 °C (98,6 °F). Los −40 °C y los −40 °F son la misma temperatura.</p>
            </div>
            <div>
              <h3 {H3}>Escalas absolutas</h3>
              <p>Kelvin y Rankine parten del cero absoluto (la menor temperatura posible: 0 K = −273,15 °C = −459,67 °F). Se usan en física y química, por ejemplo en la ley de los gases ideales.</p>
            </div>""",
    related=[("/calculadoras/ingenieria/conversor-de-unidades/", "Conversor de Unidades Técnicas"),
             ("/calculadoras/quimica/calculadora-de-gases-ideales/", "Calculadora de Gases Ideales"),
             ("/calculadoras/fisica/cinematica-mru-mrua/", "Cinemática (MRU / MRUA)")],
    guide=("/guias/conversion-de-temperatura-celsius-fahrenheit-kelvin/", "Cómo convertir entre Celsius, Fahrenheit y Kelvin",
           "Leé la guía completa: las fórmulas, trucos para estimar de cabeza y ejemplos resueltos."),
    faqs=[("¿Cómo se pasa de Celsius a Fahrenheit?",
           "Multiplicando por 9/5 y sumando 32: °F = °C × 9/5 + 32. 100 °C son 100 × 1,8 + 32 = 212 °F."),
          ("¿Cómo se pasa de Fahrenheit a Celsius?",
           "Restando 32 y multiplicando por 5/9: °C = (°F − 32) × 5/9. 98,6 °F son 66,6 × 5/9 = 37 °C."),
          ("¿Cómo se pasa de Celsius a Kelvin?",
           "Sumando 273,15: K = °C + 273,15. 25 °C son 298,15 K."),
          ("¿Cuál es el cero absoluto?",
           "0 K, es decir −273,15 °C o −459,67 °F: la temperatura más baja posible, donde cesa el movimiento térmico de las partículas."),
          ("¿En qué temperatura coinciden Celsius y Fahrenheit?",
           "En −40: −40 °C equivalen a −40 °F.")],
))
