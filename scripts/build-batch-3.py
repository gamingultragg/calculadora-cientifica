"""
build-batch-3.py — Genera las 5 calculadoras del lote 3: fracciones, teorema de Pitágoras,
aguinaldo (SAC), gases ideales y conversor de bases numéricas. Los script.js se escriben a mano
en cada carpeta; este script solo produce los index.html con scripts/page_templates.py.

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


def field(id_, label, placeholder, extra="", value=""):
    v = f' value="{value}"' if value else ""
    return (f'        <div{extra}>\n          <label for="{id_}" {LABEL}>{label}</label>\n'
            f'          <input id="{id_}" type="text" inputmode="decimal" placeholder="{placeholder}"{v} {INPUT} />\n        </div>')


def chips(items):
    """items: [(etiqueta, valor del data-example)]"""
    return "".join(f'<button type="button" data-example="{v}" {CHIP}>{l}</button>' for l, v in items)


def write(rel, html):
    path = ROOT / rel / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("escrito:", path.relative_to(ROOT))


# ------------------------------------------------------------------- fracciones
write("calculadoras/matematicas-avanzadas/calculadora-de-fracciones", calc_page(
    slug="calculadora-de-fracciones", cat_slug="matematicas-avanzadas", cat_label="Matemáticas Avanzadas",
    name="Calculadora de Fracciones",
    page_title="Calculadora de Fracciones: Sumar, Restar, Multiplicar y Simplificar | Calculadora Científica",
    desc="Sumá, restá, multiplicá y dividí fracciones con el desarrollo paso a paso, y simplificá cualquier fracción. Acepta números mixtos y decimales. Gratis y sin registro.",
    og_title="Calculadora de Fracciones",
    og_desc="Suma, resta, multiplicación, división y simplificación de fracciones, con el desarrollo paso a paso.",
    schema_desc="Opera con fracciones (suma, resta, multiplicación, división) y las simplifica, con resultado como fracción irreducible, número mixto y decimal, y el desarrollo paso a paso.",
    intro="Escribí dos fracciones, elegí la operación y obtené el resultado simplificado, como número mixto y en decimal, con el desarrollo paso a paso. También simplifica una sola fracción.",
    form_html=f"""        <div class="space-y-4">
          <div>
            <label for="fr-a" {LABEL}>Primera fracción</label>
            <input id="fr-a" type="text" autocomplete="off" spellcheck="false" placeholder="Ej: 3/4 o 1 1/2" {INPUT} />
          </div>
          <div>
            <label for="fr-op" {LABEL}>Operación</label>
            <select id="fr-op" {SELECT}>
              <option value="add">Sumar (+)</option>
              <option value="sub">Restar (−)</option>
              <option value="mul">Multiplicar (×)</option>
              <option value="div">Dividir (÷)</option>
              <option value="simp">Solo simplificar la primera</option>
            </select>
          </div>
          <div id="fr-b-wrap">
            <label for="fr-b" {LABEL}>Segunda fracción</label>
            <input id="fr-b" type="text" autocomplete="off" spellcheck="false" placeholder="Ej: 5/6" {INPUT} />
          </div>
          <div class="flex flex-wrap gap-2" aria-label="Ejemplos">{chips([("1/2 + 1/3", "1/2|add|1/3"), ("3/4 − 5/6", "3/4|sub|5/6"), ("2/3 × 9/4", "2/3|mul|9/4"), ("1 1/2 ÷ 3/4", "1 1/2|div|3/4"), ("simplificar 12/18", "12/18|simp|")])}</div>
          <button id="fr-solve" type="button" {BTN}>Calcular</button>
        </div>""",
    result_html=f"""        <section id="fr-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>Resultado</h2>
          <p id="fr-main" class="font-numeric text-3xl font-bold {PRIMARY} break-all">—</p>
          <div id="fr-lines" class="mt-2 text-sm {MUTED} space-y-1"></div>
          <div id="fr-steps" class="mt-4 text-sm {MUTED}"></div>
        </section>""",
    help_html=f"""            <div>
              <h3 {H3}>Cómo escribir las fracciones</h3>
              <p>Usá <span class="font-numeric">3/4</span> para una fracción, <span class="font-numeric">1 1/2</span> para un número mixto (un entero, un espacio y la fracción), <span class="font-numeric">7</span> para un entero y <span class="font-numeric">0,75</span> para un decimal. Los negativos llevan el signo adelante: <span class="font-numeric">-2/5</span>.</p>
            </div>
            <div>
              <h3 {H3}>Suma y resta</h3>
              <p {FORMULA}>a/b ± c/d = (a·d ± c·b) / (b·d)</p>
              <p>Se buscan fracciones equivalentes con un denominador común (lo mejor es el MCM de los denominadores) y se suman o restan los numeradores.</p>
            </div>
            <div>
              <h3 {H3}>Multiplicación y división</h3>
              <p {FORMULA}>a/b × c/d = (a·c) / (b·d) &nbsp;·&nbsp; a/b ÷ c/d = (a·d) / (b·c)</p>
              <p>Para dividir se multiplica por la inversa de la segunda fracción. No hace falta denominador común.</p>
            </div>
            <div>
              <h3 {H3}>Simplificar</h3>
              <p>Se divide numerador y denominador por su máximo común divisor (MCD). La fracción queda irreducible cuando el MCD es 1.</p>
            </div>""",
    related=[("/calculadoras/matematicas-avanzadas/mcd-y-mcm/", "Calculadora de MCD y MCM"),
             ("/calculadoras/matematicas-avanzadas/regla-de-tres/", "Calculadora de Regla de Tres"),
             ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes")],
    guide=("/guias/como-operar-con-fracciones/", "Cómo operar con fracciones",
           "Leé la guía completa: suma, resta, multiplicación, división y simplificación con ejemplos resueltos."),
    faqs=[("¿Cómo se suman fracciones con distinto denominador?",
           "Se llevan a un denominador común y se suman los numeradores. Para 1/2 + 1/3, el MCM de 2 y 3 es 6: 1/2 = 3/6 y 1/3 = 2/6, entonces la suma es 5/6."),
          ("¿Cómo se multiplican fracciones?",
           "Se multiplican los numeradores entre sí y los denominadores entre sí: 2/3 × 9/4 = 18/12, que simplificado es 3/2."),
          ("¿Cómo se dividen fracciones?",
           "Se multiplica la primera por la inversa de la segunda: 1/2 ÷ 3/4 = 1/2 × 4/3 = 4/6 = 2/3."),
          ("¿Cómo se simplifica una fracción?",
           "Se divide numerador y denominador por su máximo común divisor. En 12/18 el MCD es 6, así que 12/18 = 2/3."),
          ("¿Cómo paso un número mixto a fracción?",
           "Se multiplica el entero por el denominador y se suma el numerador: 1 1/2 = (1 × 2 + 1)/2 = 3/2. La calculadora acepta números mixtos directamente.")],
))

# ------------------------------------------------------------------- Pitágoras
write("calculadoras/matematicas-avanzadas/teorema-de-pitagoras", calc_page(
    slug="teorema-de-pitagoras", cat_slug="matematicas-avanzadas", cat_label="Matemáticas Avanzadas",
    name="Calculadora del Teorema de Pitágoras",
    page_title="Calculadora del Teorema de Pitágoras: Hipotenusa y Catetos | Calculadora Científica",
    desc="Calculá la hipotenusa o un cateto de un triángulo rectángulo con el teorema de Pitágoras, más área, perímetro, altura y ángulos. Gratis y con la fórmula explicada.",
    og_title="Calculadora del Teorema de Pitágoras",
    og_desc="Hipotenusa o cateto de un triángulo rectángulo, con área, perímetro y ángulos. Gratis.",
    schema_desc="Calcula la hipotenusa o un cateto de un triángulo rectángulo con el teorema de Pitágoras, junto con el área, el perímetro, la altura sobre la hipotenusa y los ángulos agudos.",
    intro="Ingresá dos lados de un triángulo rectángulo y obtené el tercero con el teorema de Pitágoras (a² + b² = c²). Además calcula el área, el perímetro, la altura sobre la hipotenusa y los ángulos.",
    form_html=f"""        <div class="space-y-4">
          <div>
            <label for="pt-target" {LABEL}>¿Qué lado querés calcular?</label>
            <select id="pt-target" {SELECT}>
              <option value="c">Hipotenusa (c)</option>
              <option value="a">Cateto a</option>
              <option value="b">Cateto b</option>
            </select>
          </div>
          <div>
            <label id="pt-x-label" for="pt-x" {LABEL}>Cateto a</label>
            <input id="pt-x" type="text" inputmode="decimal" placeholder="Ej: 3" {INPUT} />
          </div>
          <div>
            <label id="pt-y-label" for="pt-y" {LABEL}>Cateto b</label>
            <input id="pt-y" type="text" inputmode="decimal" placeholder="Ej: 4" {INPUT} />
          </div>
          <div class="flex flex-wrap gap-2" aria-label="Ejemplos">{chips([("catetos 3 y 4", "c|3|4"), ("hipotenusa 13, cateto 5", "a|13|5"), ("hipotenusa 10, cateto 6", "b|10|6")])}</div>
          <button id="pt-solve" type="button" {BTN}>Calcular</button>
        </div>""",
    result_html=f"""        <section id="pt-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>Resultado</h2>
          <p id="pt-label" class="text-sm {MUTED}"></p>
          <p id="pt-main" class="font-numeric text-3xl font-bold {PRIMARY}">—</p>
          <div id="pt-lines" class="mt-3 text-sm {MUTED} space-y-1"></div>
        </section>""",
    help_html=f"""            <div>
              <h3 {H3}>El teorema de Pitágoras</h3>
              <p {FORMULA}>a² + b² = c²</p>
              <p>En un triángulo rectángulo, el cuadrado de la hipotenusa (c, el lado opuesto al ángulo recto y el más largo) es igual a la suma de los cuadrados de los catetos (a y b).</p>
            </div>
            <div>
              <h3 {H3}>Despejando</h3>
              <p {FORMULA}>c = √(a² + b²) &nbsp;·&nbsp; a = √(c² − b²) &nbsp;·&nbsp; b = √(c² − a²)</p>
              <p>Para un cateto se resta; por eso la hipotenusa siempre tiene que ser mayor que el cateto que conocés.</p>
            </div>
            <div>
              <h3 {H3}>Otros datos del triángulo</h3>
              <p {FORMULA}>Área = a·b / 2 &nbsp;·&nbsp; Perímetro = a + b + c &nbsp;·&nbsp; h = a·b / c</p>
              <p>Los ángulos agudos salen con la tangente: el ángulo opuesto a <em>a</em> es arctan(a/b) y el opuesto a <em>b</em> es arctan(b/a). Suman 90°.</p>
            </div>
            <div>
              <h3 {H3}>Ternas pitagóricas</h3>
              <p>Son tres números enteros que cumplen el teorema: 3-4-5, 5-12-13, 8-15-17, 7-24-25. Cualquier múltiplo también sirve (6-8-10, 9-12-15…).</p>
            </div>""",
    related=[("/calculadoras/matematicas-avanzadas/ecuaciones-segundo-grado/", "Ecuaciones de Segundo Grado"),
             ("/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/", "Calculadora Científica Online"),
             ("/calculadoras/fisica/cinematica-mru-mrua/", "Cinemática (MRU / MRUA)")],
    guide=("/guias/teorema-de-pitagoras-explicado/", "El teorema de Pitágoras explicado",
           "Leé la guía completa: la fórmula, cómo despejar cada lado, ternas pitagóricas y ejemplos de la vida real."),
    faqs=[("¿Cómo se calcula la hipotenusa?",
           "Con c = √(a² + b²): se elevan los catetos al cuadrado, se suman y se calcula la raíz cuadrada. Con catetos de 3 y 4: √(9 + 16) = √25 = 5."),
          ("¿Cómo se calcula un cateto?",
           "Se resta: a = √(c² − b²). Con hipotenusa 13 y cateto 5: √(169 − 25) = √144 = 12."),
          ("¿Se puede usar con cualquier triángulo?",
           "No: el teorema de Pitágoras vale solo para triángulos rectángulos, los que tienen un ángulo de 90°. Para otros triángulos se usan el teorema del coseno o del seno."),
          ("¿Por qué la hipotenusa tiene que ser el lado más largo?",
           "Porque c² = a² + b² es mayor que a² y que b² por separado. Si al despejar un cateto la resta da negativa, los datos no corresponden a un triángulo rectángulo."),
          ("¿Qué es una terna pitagórica?",
           "Es un conjunto de tres números enteros que cumplen a² + b² = c², como 3, 4 y 5 (9 + 16 = 25) o 5, 12 y 13 (25 + 144 = 169).")],
))

# -------------------------------------------------------------------- aguinaldo
write("calculadoras/finanzas/calculadora-de-aguinaldo", calc_page(
    slug="calculadora-de-aguinaldo", cat_slug="finanzas", cat_label="Finanzas", name="Calculadora de Aguinaldo (SAC)",
    page_title="Calculadora de Aguinaldo (SAC) Argentina: Bruto, Neto y Proporcional | Calculadora Científica",
    desc="Calculá tu aguinaldo (sueldo anual complementario) en Argentina: el 50% de la mejor remuneración del semestre, proporcional si no trabajaste todo el período, con el neto estimado.",
    og_title="Calculadora de Aguinaldo (SAC) Argentina",
    og_desc="Aguinaldo bruto, neto y proporcional a partir de tu mejor sueldo del semestre. Gratis.",
    schema_desc="Estima el aguinaldo (sueldo anual complementario) de un trabajador en relación de dependencia en Argentina: el 50% de la mejor remuneración mensual del semestre, proporcional al tiempo trabajado, con el neto estimado.",
    intro="Ingresá tu mejor sueldo mensual del semestre y calculá el aguinaldo (SAC) que te corresponde en Argentina, completo o proporcional al tiempo trabajado, con el neto estimado después de descuentos.",
    form_html=f"""        <div class="space-y-4">
{field("sa-salary", "Mejor remuneración mensual del semestre ($)", "Ej: 1200000")}
          <div>
            <label for="sa-time" {LABEL}>¿Cuánto trabajaste en el semestre?</label>
            <select id="sa-time" {SELECT}>
              <option value="completo">Todo el semestre</option>
              <option value="meses">Parte del semestre (en meses)</option>
              <option value="dias">Parte del semestre (en días)</option>
            </select>
          </div>
          <div id="sa-part-wrap" class="hidden">
            <label id="sa-part-label" for="sa-part" {LABEL}>Meses trabajados en el semestre (máx. 6)</label>
            <input id="sa-part" type="text" inputmode="decimal" placeholder="Ej: 3" {INPUT} />
          </div>
{field("sa-deductions", "Descuentos estimados (%)", "Ej: 17", value="17")}
          <button id="sa-solve" type="button" {BTN}>Calcular aguinaldo</button>
          <p class="text-xs {MUTED}">Es una estimación de referencia. El convenio colectivo de tu actividad o tu recibo de sueldo pueden aplicar otro criterio: ante dudas, consultá con tu empleador o tu sindicato.</p>
        </div>""",
    result_html=f"""        <section id="sa-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>Resultado</h2>
          <p class="text-sm {MUTED}">Aguinaldo bruto</p>
          <p id="sa-main" class="font-numeric text-3xl font-bold {PRIMARY}">—</p>
          <div id="sa-lines" class="mt-3 text-sm {MUTED} space-y-1"></div>
        </section>""",
    help_html=f"""            <div>
              <h3 {H3}>Cómo se calcula el aguinaldo</h3>
              <p {FORMULA}>SAC = 50 % × mejor remuneración mensual del semestre</p>
              <p>El semestre va del 1.° de enero al 30 de junio y del 1.° de julio al 31 de diciembre. Se toma la <strong>mejor</strong> remuneración mensual, normal y habitual, devengada en ese período (no el promedio ni el último sueldo, salvo que sea el mejor).</p>
            </div>
            <div>
              <h3 {H3}>Si no trabajaste todo el semestre</h3>
              <p {FORMULA}>SAC proporcional = (mejor sueldo / 2) × meses trabajados / 6</p>
              <p>También se puede expresar por días: (mejor sueldo / 2) × días trabajados / 180. Es lo mismo que sumar 1/12 del mejor sueldo por cada mes trabajado.</p>
            </div>
            <div>
              <h3 {H3}>Descuentos</h3>
              <p>Sobre el aguinaldo se descuentan los mismos aportes que sobre el sueldo (jubilación, PAMI y obra social, que suman habitualmente un 17%). Podés cambiar el porcentaje si tu recibo indica otro. El impuesto a las ganancias, si te corresponde, no está incluido.</p>
            </div>
            <div>
              <h3 {H3}>Fechas de pago</h3>
              <p>La ley establece el 30 de junio y el 18 de diciembre, con hasta 4 días hábiles de plazo para depositarlo.</p>
            </div>""",
    related=[("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes"),
             ("/calculadoras/finanzas/calculadora-de-iva/", "Calculadora de IVA"),
             ("/calculadoras/finanzas/calculadora-de-interes-simple/", "Interés Simple")],
    guide=("/guias/como-calcular-el-aguinaldo/", "Cómo calcular el aguinaldo",
           "Leé la guía completa: mejor remuneración, proporcional, descuentos y fechas de pago, con ejemplos."),
    faqs=[("¿Cómo se calcula el aguinaldo?",
           "Es el 50% de la mejor remuneración mensual del semestre. Con un mejor sueldo de $1.000.000, el aguinaldo completo es $500.000 bruto."),
          ("¿Qué pasa si no trabajé todo el semestre?",
           "Se paga proporcional: por cada mes trabajado corresponde 1/12 del mejor sueldo (o, por días, 1/180 de la mitad del mejor sueldo por día). Con 3 meses y un mejor sueldo de $1.200.000: 1.200.000 / 12 × 3 = $300.000."),
          ("¿Cuándo se cobra el aguinaldo?",
           "En dos cuotas anuales: la primera vence el 30 de junio y la segunda el 18 de diciembre, con 4 días hábiles de plazo para depositarlas."),
          ("¿Cuánto se descuenta del aguinaldo?",
           "Los aportes habituales de la relación de dependencia (jubilación 11%, ley 19.032 3% y obra social 3%, en total 17%), y el impuesto a las ganancias si corresponde. En la calculadora podés ajustar el porcentaje."),
          ("¿Cuál es la mejor remuneración del semestre?",
           "Es el mayor sueldo mensual normal y habitual que cobraste entre enero y junio (primer aguinaldo) o entre julio y diciembre (segundo), incluyendo adicionales habituales como el presentismo.")],
))

# ---------------------------------------------------------------- gases ideales
def gas_row(key, base, result, input_id, placeholder, unit_id=None, units=()):
    unit = ""
    if unit_id:
        opts = "".join(f'<option value="{v}">{t}</option>' for v, t in units)
        unit = f'\n            <select id="{unit_id}" aria-label="Unidad de {base.lower()}" {SELECT}>{opts}</select>'
    cols = "grid-cols-[1fr_auto]" if unit_id else "grid-cols-1"
    return f"""          <div data-row="{key}">
            <label for="{input_id}" data-base="{base}" data-result="{result}" {LABEL}>{base}</label>
            <div class="grid {cols} gap-2">
              <input id="{input_id}" data-input type="text" inputmode="decimal" placeholder="{placeholder}" {INPUT} />{unit}
            </div>
          </div>"""


write("calculadoras/quimica/calculadora-de-gases-ideales", calc_page(
    slug="calculadora-de-gases-ideales", cat_slug="quimica", cat_label="Química", name="Calculadora de Gases Ideales",
    page_title="Calculadora de Gases Ideales: PV = nRT (Presión, Volumen, Moles, Temperatura) | Calculadora Científica",
    desc="Despejá la presión, el volumen, los moles o la temperatura con la ecuación de los gases ideales PV = nRT. Con atm, kPa, mmHg, bar, litros y °C o K. Gratis.",
    og_title="Calculadora de Gases Ideales (PV = nRT)",
    og_desc="Presión, volumen, moles o temperatura con la ley de los gases ideales. Gratis.",
    schema_desc="Calcula la presión, el volumen, la cantidad de sustancia o la temperatura de un gas ideal con la ecuación PV = nRT, con conversión de unidades (atm, kPa, mmHg, bar, L, mL, m³, K, °C).",
    intro="Elegí qué querés calcular, completá los otros tres datos con las unidades que prefieras y obtené el resultado con la ecuación de los gases ideales PV = nRT.",
    form_html=f"""        <div class="space-y-4">
          <div>
            <label for="gi-target" {LABEL}>¿Qué querés calcular?</label>
            <select id="gi-target" {SELECT}>
              <option value="P">Presión (P)</option>
              <option value="V">Volumen (V)</option>
              <option value="n">Moles (n)</option>
              <option value="T">Temperatura (T)</option>
            </select>
          </div>
{gas_row("P", "Presión", "Unidad de la presión (resultado)", "gi-p", "Ej: 1", "gi-p-unit", [("atm", "atm"), ("kpa", "kPa"), ("mmhg", "mmHg"), ("bar", "bar")])}
{gas_row("V", "Volumen", "Unidad del volumen (resultado)", "gi-v", "Ej: 22,4", "gi-v-unit", [("l", "L"), ("ml", "mL"), ("m3", "m³")])}
{gas_row("n", "Moles (n)", "Moles (n)", "gi-n", "Ej: 1")}
{gas_row("T", "Temperatura", "Unidad de la temperatura (resultado)", "gi-t", "Ej: 25", "gi-t-unit", [("c", "°C"), ("k", "K")])}
          <div class="flex flex-wrap gap-2" aria-label="Ejemplos">{chips([("1 mol a 0 °C y 1 atm → V", "V|1||1|0"), ("2 mol en 10 L a 27 °C → P", "P||10|2|27"), ("1 atm, 22,4 L → moles a 0 °C", "n|1|22,4||0")])}</div>
          <button id="gi-solve" type="button" {BTN}>Calcular</button>
        </div>""",
    result_html=f"""        <section id="gi-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>Resultado</h2>
          <p id="gi-label" class="text-sm {MUTED}"></p>
          <p id="gi-main" class="font-numeric text-3xl font-bold {PRIMARY}">—</p>
          <div id="gi-lines" class="mt-2 text-sm {MUTED} space-y-1"></div>
        </section>""",
    help_html=f"""            <div>
              <h3 {H3}>Ecuación de los gases ideales</h3>
              <p {FORMULA}>P · V = n · R · T</p>
              <p>P es la presión, V el volumen, n la cantidad de gas en moles, R la constante de los gases y T la temperatura <strong>absoluta</strong> (en kelvin).</p>
            </div>
            <div>
              <h3 {H3}>La constante R</h3>
              <p {FORMULA}>R = 0,082057 L·atm/(mol·K) = 8,314 J/(mol·K)</p>
              <p>La calculadora convierte todo a atm, litros y kelvin antes de operar, y te devuelve el resultado en la unidad que elegiste.</p>
            </div>
            <div>
              <h3 {H3}>Temperatura en kelvin</h3>
              <p {FORMULA}>T(K) = T(°C) + 273,15</p>
              <p>En la ecuación siempre se usa kelvin: usar °C da resultados incorrectos. La calculadora hace la conversión sola si elegís °C.</p>
            </div>
            <div>
              <h3 {H3}>Condiciones normales (CNPT)</h3>
              <p>A 0 °C (273,15 K) y 1 atm, un mol de gas ideal ocupa 22,414 L. Es un buen dato para controlar tus cuentas.</p>
            </div>""",
    related=[("/calculadoras/quimica/calculadora-de-molaridad/", "Calculadora de Molaridad"),
             ("/calculadoras/quimica/calculadora-de-masa-molar/", "Calculadora de Masa Molar"),
             ("/calculadoras/ingenieria/conversor-de-unidades/", "Conversor de Unidades Técnicas")],
    guide=("/guias/ley-de-los-gases-ideales/", "La ley de los gases ideales",
           "Leé la guía completa: la ecuación PV = nRT, cómo elegir la R correcta y ejemplos resueltos paso a paso."),
    faqs=[("¿Qué es la ecuación de los gases ideales?",
           "Es la relación PV = nRT entre presión, volumen, cantidad de gas (en moles) y temperatura absoluta. Describe bien a la mayoría de los gases a presiones bajas y temperaturas altas."),
          ("¿Por qué hay que usar kelvin?",
           "Porque la ecuación es proporcional a la temperatura absoluta, que parte del cero absoluto (0 K). Con grados Celsius, 0 °C no es \"ausencia de energía\" y los resultados salen mal."),
          ("¿Qué valor de R uso?",
           "Depende de las unidades: 0,082057 L·atm/(mol·K) si la presión está en atm y el volumen en litros, o 8,314 J/(mol·K) en unidades del sistema internacional (Pa y m³). La calculadora usa la primera y convierte por vos."),
          ("¿Cuánto ocupa un mol de gas?",
           "A 0 °C y 1 atm (condiciones normales), 22,414 litros. A 25 °C y 1 atm son unos 24,46 litros."),
          ("¿Cuándo deja de valer el modelo de gas ideal?",
           "A presiones muy altas o temperaturas muy bajas, cuando las moléculas ocupan un volumen apreciable y se atraen entre sí. Ahí se usan modelos como el de Van der Waals.")],
))

# ----------------------------------------------------------- bases numéricas
write("calculadoras/matematicas-avanzadas/conversor-de-bases-numericas", calc_page(
    slug="conversor-de-bases-numericas", cat_slug="matematicas-avanzadas", cat_label="Matemáticas Avanzadas",
    name="Conversor de Bases Numéricas",
    page_title="Conversor de Bases Numéricas: Binario, Decimal, Octal y Hexadecimal | Calculadora Científica",
    desc="Convertí números entre binario, octal, decimal, hexadecimal y cualquier base de 2 a 36, con el desarrollo paso a paso por divisiones sucesivas. Gratis y sin límite de tamaño.",
    og_title="Conversor de Bases Numéricas",
    og_desc="Binario, octal, decimal, hexadecimal y cualquier base de 2 a 36, con el desarrollo paso a paso.",
    schema_desc="Convierte números enteros entre binario, octal, decimal, hexadecimal y cualquier base de 2 a 36, con el desarrollo por divisiones sucesivas y soporte para números muy grandes.",
    intro="Escribí un número en cualquier base y obtené su equivalente en binario, octal, decimal y hexadecimal (y en otra base de 2 a 36 si querés), con el desarrollo de las divisiones sucesivas.",
    form_html=f"""        <div class="space-y-4">
          <div>
            <label for="bn-input" {LABEL}>Número</label>
            <input id="bn-input" type="text" autocomplete="off" spellcheck="false" placeholder="Ej: 255 o FF" {INPUT} />
          </div>
          <div>
            <label for="bn-from" {LABEL}>Está escrito en base…</label>
            <select id="bn-from" {SELECT}>
              <option value="10">10 — Decimal</option>
              <option value="2">2 — Binario</option>
              <option value="8">8 — Octal</option>
              <option value="16">16 — Hexadecimal</option>
              <option value="custom">Otra base (2 a 36)</option>
            </select>
          </div>
          <div id="bn-from-custom-wrap" class="hidden">
            <label for="bn-from-custom" {LABEL}>Base de origen (2 a 36)</label>
            <input id="bn-from-custom" type="number" min="2" max="36" step="1" value="5" {INPUT} />
          </div>
          <div>
            <label for="bn-to-custom" {LABEL}>Convertir también a otra base (opcional)</label>
            <input id="bn-to-custom" type="number" min="2" max="36" step="1" placeholder="Ej: 5" {INPUT} />
          </div>
          <div class="flex flex-wrap gap-2" aria-label="Ejemplos">{chips([("255 (dec)", "255|10"), ("1010 (bin)", "1010|2"), ("FF (hex)", "ff|16"), ("777 (oct)", "777|8")])}</div>
          <button id="bn-solve" type="button" {BTN}>Convertir</button>
        </div>""",
    result_html=f"""        <section id="bn-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>Resultado</h2>
          <div id="bn-rows"></div>
          <div id="bn-steps" class="mt-4 text-sm {MUTED}"></div>
        </section>""",
    help_html=f"""            <div>
              <h3 {H3}>Qué es una base numérica</h3>
              <p>Es la cantidad de símbolos que usa un sistema para escribir números. Decimal usa 10 (0-9), binario usa 2 (0 y 1), octal usa 8 (0-7) y hexadecimal usa 16 (0-9 y A-F, donde A = 10 … F = 15).</p>
            </div>
            <div>
              <h3 {H3}>De decimal a otra base</h3>
              <p>Se divide el número por la base una y otra vez, anotando los restos, hasta llegar a 0. Los restos leídos <strong>de abajo hacia arriba</strong> forman el número. Ejemplo: 13 ÷ 2 = 6 resto 1; 6 ÷ 2 = 3 resto 0; 3 ÷ 2 = 1 resto 1; 1 ÷ 2 = 0 resto 1 → 1101.</p>
            </div>
            <div>
              <h3 {H3}>De otra base a decimal</h3>
              <p {FORMULA}>1101₂ = 1·2³ + 1·2² + 0·2¹ + 1·2⁰ = 13</p>
              <p>Cada dígito se multiplica por la base elevada a su posición (empezando en 0 por la derecha) y se suma.</p>
            </div>
            <div>
              <h3 {H3}>Binario ↔ hexadecimal</h3>
              <p>Cada dígito hexadecimal equivale a 4 bits: 1111 0000₂ = F0₁₆. Por eso el hexadecimal se usa tanto en informática: es una forma corta de escribir binario.</p>
            </div>""",
    related=[("/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/", "Calculadora Científica Online"),
             ("/calculadoras/matematicas-avanzadas/mcd-y-mcm/", "Calculadora de MCD y MCM"),
             ("/calculadoras/matematicas-avanzadas/calculadora-basica/", "Calculadora Básica")],
    guide=("/guias/como-convertir-binario-decimal-y-hexadecimal/", "Cómo convertir entre binario, decimal y hexadecimal",
           "Leé la guía completa: métodos paso a paso, tablas de equivalencias y ejemplos para pasar de una base a otra."),
    faqs=[("¿Cómo se pasa de decimal a binario?",
           "Se divide por 2 sucesivamente anotando los restos, hasta llegar a 0, y se leen los restos de abajo hacia arriba. 13 → 1101."),
          ("¿Cómo se pasa de binario a decimal?",
           "Se multiplica cada bit por 2 elevado a su posición (de derecha a izquierda, desde 0) y se suma. 1101₂ = 8 + 4 + 0 + 1 = 13."),
          ("¿Qué significan las letras A-F en hexadecimal?",
           "Son los dígitos 10 a 15: A = 10, B = 11, C = 12, D = 13, E = 14 y F = 15. Con ellos el sistema completa los 16 símbolos que necesita."),
          ("¿Cuál es el binario de 255?",
           "11111111 (ocho unos) y en hexadecimal FF. Es el mayor valor que entra en un byte."),
          ("¿Puedo convertir números negativos o muy grandes?",
           "Sí: se acepta el signo menos y la calculadora usa aritmética de precisión arbitraria, sin perder dígitos. Solo trabaja con números enteros.")],
))
