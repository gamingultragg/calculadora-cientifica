"""
build-batch-5.py — Genera las 5 calculadoras del lote 5, que inauguran la categoría "Vida Diaria":
edad y fechas, IMC, conversor de cocina, horas trabajadas y propina/división de cuenta.
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
CAT = dict(cat_slug="vida-diaria", cat_label="Vida Diaria")


def field(id_, label, placeholder="", extra="", value="", type_="text", inputmode="decimal"):
    v = f' value="{value}"' if value else ""
    im = f' inputmode="{inputmode}"' if type_ == "text" else ""
    ph = f' placeholder="{placeholder}"' if placeholder else ""
    return (f'        <div{extra}>\n          <label for="{id_}" {LABEL}>{label}</label>\n'
            f'          <input id="{id_}" type="{type_}"{im}{ph}{v} {INPUT} />\n        </div>')


def with_unit(id_, label, placeholder, unit_id, units, unit_label):
    opts = "".join(f'<option value="{v}">{t}</option>' for v, t in units)
    return f"""          <div>
            <label for="{id_}" {LABEL}>{label}</label>
            <div class="grid grid-cols-[1fr_auto] gap-2">
              <input id="{id_}" type="text" inputmode="decimal" placeholder="{placeholder}" {INPUT} />
              <select id="{unit_id}" aria-label="{unit_label}" {SELECT}>{opts}</select>
            </div>
          </div>"""


def chips(items):
    return "".join(f'<button type="button" data-example="{v}" {CHIP}>{l}</button>' for l, v in items)


def write(rel, html):
    path = ROOT / rel / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("escrito:", path.relative_to(ROOT))


def panel(prefix, extra_inside=""):
    return f"""        <section id="{prefix}-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>Resultado</h2>
          <p id="{prefix}-label" class="text-sm {MUTED}"></p>
          <p id="{prefix}-main" class="font-numeric text-3xl font-bold {PRIMARY} break-words">—</p>{extra_inside}
          <div id="{prefix}-lines" class="mt-3 text-sm {MUTED} space-y-1"></div>
        </section>"""


# ------------------------------------------------------------------ edad y fechas
write("calculadoras/vida-diaria/calculadora-de-edad-y-fechas", calc_page(
    slug="calculadora-de-edad-y-fechas", name="Calculadora de Edad y Fechas", **CAT,
    page_title="Calculadora de Edad y Días entre Fechas | Calculadora Científica",
    desc="Calculá tu edad exacta en años, meses y días, los días entre dos fechas (con días hábiles) o qué fecha será dentro de X días, semanas, meses o años. Gratis y sin registro.",
    og_title="Calculadora de Edad y Fechas",
    og_desc="Edad exacta, días entre fechas y suma de tiempo a una fecha. Gratis.",
    schema_desc="Calcula la edad exacta en años, meses y días, la diferencia entre dos fechas (con días corridos y hábiles) y la fecha resultante de sumar o restar días, semanas, meses o años.",
    intro="Elegí qué necesitás: tu edad exacta y cuántos días faltan para tu próximo cumpleaños, cuánto tiempo pasó entre dos fechas, o qué fecha resulta de sumar o restar días, semanas, meses o años.",
    form_html=f"""        <div class="space-y-4">
          <div>
            <label for="fd-mode" {LABEL}>¿Qué querés calcular?</label>
            <select id="fd-mode" {SELECT}>
              <option value="edad">Edad exacta</option>
              <option value="diff">Días entre dos fechas</option>
              <option value="sumar">Sumar o restar tiempo a una fecha</option>
            </select>
          </div>
{field("fd-birth", "Fecha de nacimiento", extra=' data-mode="edad"', type_="date")}
{field("fd-ref", "Calcular la edad al día (vacío = hoy)", extra=' data-mode="edad"', type_="date")}
{field("fd-a", "Fecha de inicio", extra=' data-mode="diff"', type_="date")}
{field("fd-b", "Fecha de fin", extra=' data-mode="diff"', type_="date")}
{field("fd-base", "Fecha de partida", extra=' data-mode="sumar"', type_="date")}
          <div class="grid grid-cols-3 gap-2" data-mode="sumar">
            <div>
              <label for="fd-op" {LABEL}>Operación</label>
              <select id="fd-op" {SELECT}><option value="sumar">Sumar</option><option value="restar">Restar</option></select>
            </div>
            <div>
              <label for="fd-amount" {LABEL}>Cantidad</label>
              <input id="fd-amount" type="text" inputmode="numeric" placeholder="Ej: 90" {INPUT} />
            </div>
            <div>
              <label for="fd-unit" {LABEL}>Unidad</label>
              <select id="fd-unit" {SELECT}><option value="dias">días</option><option value="semanas">semanas</option><option value="meses">meses</option><option value="anios">años</option></select>
            </div>
          </div>
          <button id="fd-solve" type="button" {BTN}>Calcular</button>
        </div>""",
    result_html=panel("fd"),
    help_html=f"""            <div>
              <h3 {H3}>Cómo se calcula la edad</h3>
              <p>Se cuentan los años y meses completos desde el nacimiento y los días que sobran. Si naciste el 15 de mayo de 1990, al 10 de noviembre de 2026 tenés 36 años, 5 meses y 26 días. El cumpleaños de quienes nacieron un 29 de febrero se festeja el 28 de febrero en los años no bisiestos.</p>
            </div>
            <div>
              <h3 {H3}>Días entre dos fechas</h3>
              <p>Es la resta de las fechas expresada en días corridos (no cuenta el día de inicio). También se muestran los <strong>días hábiles</strong> (de lunes a viernes), que no descuentan feriados porque varían por país y año.</p>
            </div>
            <div>
              <h3 {H3}>Sumar meses y años</h3>
              <p>Al sumar meses el día se conserva, salvo que el mes de destino sea más corto: 31 de enero + 1 mes = 28 de febrero (o 29 en año bisiesto). Sumar semanas y días es exacto.</p>
            </div>
            <div>
              <h3 {H3}>Años bisiestos</h3>
              <p>Son los divisibles por 4, salvo los divisibles por 100 que no lo sean por 400. Así, 2024 y 2000 son bisiestos; 2100 no. La calculadora ya los considera.</p>
            </div>""",
    related=[("/calculadoras/vida-diaria/calculadora-de-horas-trabajadas/", "Calculadora de Horas Trabajadas"),
             ("/calculadoras/finanzas/calculadora-de-plazo-fijo/", "Calculadora de Plazo Fijo y Tasas"),
             ("/calculadoras/finanzas/calculadora-de-interes-simple/", "Interés Simple")],
    guide=("/guias/como-calcular-la-edad-y-los-dias-entre-fechas/", "Cómo calcular la edad y los días entre dos fechas",
           "Leé la guía completa: el método de años, meses y días, los años bisiestos y los errores más comunes."),
    faqs=[("¿Cómo se calcula la edad exacta?",
           "Se restan los años y se ajusta según si ya pasó el cumpleaños; los meses y días sobrantes completan la cuenta. De 15/05/1990 al 10/11/2026: 36 años, 5 meses y 26 días."),
          ("¿Cómo se calculan los días entre dos fechas?",
           "Restando las fechas. Del 1 de enero al 31 de diciembre de 2026 hay 364 días (365 si se cuenta también el último día)."),
          ("¿Qué fecha será dentro de 90 días?",
           "Sumá 90 días a la fecha de partida con la calculadora: desde el 10 de noviembre de 2026, serán 90 días hasta el 8 de febrero de 2027."),
          ("¿Cuenta los feriados?",
           "No: los días hábiles son de lunes a viernes. Los feriados cambian cada año y según el país, así que habría que restarlos a mano."),
          ("¿Qué pasa con quienes nacieron el 29 de febrero?",
           "En los años no bisiestos se toma el 28 de febrero como fecha de cumpleaños para calcular cuántos días faltan.")],
))

# --------------------------------------------------------------------------- IMC
write("calculadoras/vida-diaria/calculadora-de-imc", calc_page(
    slug="calculadora-de-imc", name="Calculadora de IMC (Índice de Masa Corporal)", **CAT,
    page_title="Calculadora de IMC: Índice de Masa Corporal y Peso Saludable | Calculadora Científica",
    desc="Calculá tu índice de masa corporal (IMC) con tu peso y altura, mirá la categoría según la OMS y el rango de peso saludable para tu estatura. En kg, lb, cm, m o pulgadas.",
    og_title="Calculadora de IMC",
    og_desc="Tu índice de masa corporal, la categoría de la OMS y tu rango de peso saludable. Gratis.",
    schema_desc="Calcula el índice de masa corporal (IMC = peso / altura²), indica la categoría según la Organización Mundial de la Salud para adultos y el rango de peso con IMC normal para una altura dada.",
    intro="Ingresá tu peso y tu altura y obtené tu índice de masa corporal (IMC), la categoría según la OMS y el rango de peso que corresponde a un IMC normal para tu estatura.",
    form_html=f"""        <div class="space-y-4">
{with_unit("im-weight", "Peso", "Ej: 70", "im-weight-unit", [("kg", "kg"), ("lb", "lb")], "Unidad de peso")}
{with_unit("im-height", "Altura", "Ej: 175", "im-height-unit", [("cm", "cm"), ("m", "m"), ("in", "pulgadas")], "Unidad de altura")}
          <div class="flex flex-wrap gap-2" aria-label="Ejemplos">{chips([("70 kg · 175 cm", "70|175"), ("55 kg · 160 cm", "55|160"), ("95 kg · 178 cm", "95|178")])}</div>
          <button id="im-solve" type="button" {BTN}>Calcular IMC</button>
          <p class="text-xs {MUTED}">Es un indicador orientativo para adultos. No reemplaza una consulta médica.</p>
        </div>""",
    result_html=panel("im", f'\n          <p id="im-cat" class="mt-1 font-display text-lg font-semibold"></p>').replace(
        '<p id="im-label" class="text-sm text-[var(--color-text-muted)]"></p>', '<p class="text-sm text-[var(--color-text-muted)]">Tu IMC</p>'),
    help_html=f"""            <div>
              <h3 {H3}>La fórmula</h3>
              <p {FORMULA}>IMC = peso (kg) / altura (m)²</p>
              <p>Una persona de 70 kg que mide 1,75 m tiene un IMC de 70 / 3,0625 = 22,9.</p>
            </div>
            <div>
              <h3 {H3}>Categorías de la OMS (adultos)</h3>
              <ul class="list-disc list-inside space-y-1">
                <li>Menos de 18,5: bajo peso</li>
                <li>18,5 a 24,9: peso normal</li>
                <li>25 a 29,9: sobrepeso</li>
                <li>30 a 34,9: obesidad grado I · 35 a 39,9: grado II · 40 o más: grado III</li>
              </ul>
            </div>
            <div>
              <h3 {H3}>Límites del IMC</h3>
              <p>No distingue masa muscular de grasa, no tiene en cuenta la distribución de la grasa ni la edad avanzada, y no se aplica a menores de 18 años, embarazadas ni deportistas de alto rendimiento. Para una evaluación real, consultá con un profesional de la salud.</p>
            </div>""",
    related=[("/calculadoras/vida-diaria/conversor-de-cocina/", "Conversor de Cocina"),
             ("/calculadoras/ingenieria/conversor-de-unidades/", "Conversor de Unidades Técnicas"),
             ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes")],
    guide=("/guias/como-calcular-el-imc/", "Cómo calcular e interpretar el IMC",
           "Leé la guía completa: la fórmula, la tabla de categorías, el rango de peso saludable y las limitaciones del índice."),
    faqs=[("¿Cómo se calcula el IMC?",
           "Dividiendo el peso en kilogramos por la altura en metros al cuadrado. Con 70 kg y 1,75 m: 70 / (1,75 × 1,75) = 22,9."),
          ("¿Qué IMC es normal?",
           "Para adultos, la OMS considera normal un IMC entre 18,5 y 24,9. Menos de 18,5 es bajo peso; de 25 en adelante, sobrepeso; y de 30 en adelante, obesidad."),
          ("¿Cuál es mi peso saludable?",
           "El que da un IMC entre 18,5 y 24,9 para tu altura. Para 1,75 m es de unos 56,7 a 76,3 kg."),
          ("¿El IMC sirve para niños y adolescentes?",
           "No con estas categorías: en menores de 18 años se usan curvas de percentiles según edad y sexo, que interpreta un pediatra."),
          ("¿Por qué el IMC puede engañar a deportistas?",
           "Porque el músculo pesa más que la grasa: una persona muy musculosa puede tener un IMC alto sin exceso de grasa.")],
))

# --------------------------------------------------------------------- cocina
ING = [("agua", "Agua"), ("leche", "Leche"), ("harina", "Harina de trigo"), ("azucar", "Azúcar común"), ("impalpable", "Azúcar impalpable"),
       ("manteca", "Manteca"), ("aceite", "Aceite"), ("miel", "Miel"), ("arroz", "Arroz crudo"), ("avena", "Avena arrollada"),
       ("cacao", "Cacao en polvo"), ("maicena", "Maicena"), ("sal", "Sal fina"), ("ddl", "Dulce de leche"), ("panrallado", "Pan rallado")]
UNITS = [("taza", "tazas"), ("cda", "cucharadas"), ("cdta", "cucharaditas"), ("ml", "ml"), ("l", "litros"), ("g", "gramos"), ("kg", "kg"), ("oz", "onzas")]
write("calculadoras/vida-diaria/conversor-de-cocina", calc_page(
    slug="conversor-de-cocina", name="Conversor de Cocina", **CAT,
    page_title="Conversor de Cocina: Tazas, Cucharadas, Gramos y ml | Calculadora Científica",
    desc="Convertí tazas, cucharadas, cucharaditas, mililitros y gramos de harina, azúcar, manteca y otros ingredientes. Equivalencias de cocina al instante. Gratis.",
    og_title="Conversor de Cocina",
    og_desc="De tazas y cucharadas a gramos y ml, para 15 ingredientes comunes. Gratis.",
    schema_desc="Convierte medidas de cocina entre tazas, cucharadas, cucharaditas, mililitros, litros, gramos, kilogramos y onzas para 15 ingredientes comunes.",
    intro="Escribí una cantidad, elegí la unidad y el ingrediente, y mirá al instante su equivalente en gramos, mililitros, tazas, cucharadas y cucharaditas.",
    form_html=f"""        <div class="space-y-4">
          <div class="grid grid-cols-[1fr_auto] gap-2">
            <div>
              <label for="co-value" {LABEL}>Cantidad</label>
              <input id="co-value" type="text" inputmode="decimal" placeholder="Ej: 1,5" {INPUT} />
            </div>
            <div>
              <label for="co-unit" {LABEL}>Unidad</label>
              <select id="co-unit" {SELECT}>{"".join(f'<option value="{v}">{t}</option>' for v, t in UNITS)}</select>
            </div>
          </div>
          <div>
            <label for="co-ingredient" {LABEL}>Ingrediente</label>
            <select id="co-ingredient" {SELECT}>{"".join(f'<option value="{v}">{t}</option>' for v, t in ING)}</select>
          </div>
          <div>
            <label for="co-cup" {LABEL}>Tamaño de la taza</label>
            <select id="co-cup" {SELECT}><option value="240" selected>240 ml (taza de medir)</option><option value="250">250 ml</option><option value="200">200 ml (taza de té)</option></select>
          </div>
          <div class="flex flex-wrap gap-2" aria-label="Ejemplos">{chips([("1 taza de harina", "1|taza|harina"), ("200 g de azúcar", "200|g|azucar"), ("2 cucharadas de manteca", "2|cda|manteca"), ("500 ml de leche", "500|ml|leche")])}</div>
          <button id="co-solve" type="button" {BTN}>Convertir</button>
        </div>""",
    result_html=f"""        <section id="co-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>Equivalencias</h2>
          <div id="co-rows"></div>
          <p id="co-note" class="mt-3 text-xs {MUTED}"></p>
        </section>""",
    help_html=f"""            <div>
              <h3 {H3}>Medidas de volumen</h3>
              <p>1 cucharadita = 5 ml · 1 cucharada = 15 ml (3 cucharaditas) · 1 taza de medir = 240 ml (16 cucharadas). En muchas recetas argentinas la taza es de 250 ml o de 200 ml (taza de té): por eso se puede elegir el tamaño.</p>
            </div>
            <div>
              <h3 {H3}>De volumen a gramos</h3>
              <p>Los gramos dependen de la densidad del ingrediente: una taza de azúcar (≈ 200 g) pesa mucho más que una de harina (≈ 125 g) o de avena (≈ 90 g). Por eso hay que elegir el ingrediente.</p>
            </div>
            <div>
              <h3 {H3}>Son valores aproximados</h3>
              <p>Cambian según la marca, la humedad, si la harina está tamizada o apelmazada y cómo se llena la medida. En repostería, donde importa la precisión, lo mejor es pesar con balanza.</p>
            </div>""",
    related=[("/calculadoras/ingenieria/conversor-de-temperatura/", "Conversor de Temperatura"),
             ("/calculadoras/ingenieria/conversor-de-unidades/", "Conversor de Unidades Técnicas"),
             ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes")],
    guide=("/guias/equivalencias-de-cocina-tazas-cucharadas-y-gramos/", "Equivalencias de cocina: tazas, cucharadas y gramos",
           "Leé la guía completa: tabla de medidas, gramos por taza de los ingredientes más usados y consejos para medir bien."),
    faqs=[("¿Cuántos gramos tiene una taza de harina?",
           "Alrededor de 125 g (una taza de 240 ml). Si la harina está apelmazada puede llegar a 140 g; tamizada, bajar a 115 g."),
          ("¿Cuántas cucharadas hay en una taza?",
           "16 cucharadas soperas, si la taza es de 240 ml y la cucharada de 15 ml. Con una taza de 250 ml serían unas 16,7."),
          ("¿Cuántos gramos tiene una cucharada de azúcar?",
           "Unos 12,5 g: una cucharada son 15 ml y el azúcar común pesa 0,84 g/ml."),
          ("¿Cuántas cucharaditas tiene una cucharada?",
           "Tres: 1 cucharada = 15 ml y 1 cucharadita = 5 ml."),
          ("¿Por qué los resultados son aproximados?",
           "Porque la densidad de un ingrediente varía con la marca y cómo se llene la medida. Para recetas delicadas, pesá en gramos.")],
))

# ----------------------------------------------------------- horas trabajadas
write("calculadoras/vida-diaria/calculadora-de-horas-trabajadas", calc_page(
    slug="calculadora-de-horas-trabajadas", name="Calculadora de Horas Trabajadas", **CAT,
    page_title="Calculadora de Horas Trabajadas: Entrada, Salida y Horas Extra | Calculadora Científica",
    desc="Calculá las horas trabajadas entre la hora de entrada y de salida (incluso turnos nocturnos), con descanso, días trabajados, horas extra y valor de la hora. Gratis.",
    og_title="Calculadora de Horas Trabajadas",
    og_desc="Horas entre entrada y salida, descanso, horas extra y valor de la hora. Gratis.",
    schema_desc="Calcula las horas trabajadas entre una hora de entrada y una de salida (incluyendo turnos que cruzan la medianoche), descontando el descanso, con horas extra por encima de la jornada normal y el importe estimado.",
    intro="Ingresá la hora de entrada y de salida, el descanso y los días trabajados: obtenés el total de horas en formato horas:minutos y en decimal, las horas extra y, si querés, el importe.",
    form_html=f"""        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-3">
{field("ho-start", "Entrada", value="09:00", type_="time")}
{field("ho-end", "Salida", value="18:00", type_="time")}
          </div>
          <div class="grid grid-cols-2 gap-3">
{field("ho-break", "Descanso (minutos)", "Ej: 60", value="60")}
{field("ho-days", "Días trabajados", "Ej: 5", value="1")}
          </div>
          <details class="rounded-xl border border-[var(--color-border)] p-3">
            <summary class="cursor-pointer text-sm font-semibold min-h-[2rem] flex items-center">Horas extra e importe (opcional)</summary>
            <div class="mt-3 space-y-3">
{field("ho-normal", "Jornada normal por día (horas)", "8", value="8")}
{field("ho-rate", "Valor de la hora ($)", "Ej: 5000")}
{field("ho-surcharge", "Recargo de las horas extra (%)", "50", value="50")}
            </div>
          </details>
          <button id="ho-solve" type="button" {BTN}>Calcular horas</button>
        </div>""",
    result_html=panel("ho").replace('<p id="ho-label" class="text-sm text-[var(--color-text-muted)]"></p>', '<p class="text-sm text-[var(--color-text-muted)]">Total trabajado</p>'),
    help_html=f"""            <div>
              <h3 {H3}>Cómo se calcula</h3>
              <p {FORMULA}>horas = (salida − entrada) − descanso</p>
              <p>Si la salida es menor que la entrada (por ejemplo, de 22:00 a 06:00), se entiende que el turno cruza la medianoche y se suman 24 horas.</p>
            </div>
            <div>
              <h3 {H3}>De horas:minutos a decimal</h3>
              <p>Se divide los minutos por 60: 8:15 son 8,25 horas; 8:30 son 8,5; 8:45 son 8,75. Es el formato que se usa para multiplicar por el valor de la hora.</p>
            </div>
            <div>
              <h3 {H3}>Horas extra</h3>
              <p>Son las que exceden la jornada normal. En Argentina la jornada máxima legal es de 8 horas diarias y 48 semanales, y las horas extra se pagan con un recargo del 50% en días comunes y del 100% los sábados después de las 13, domingos y feriados. Cambiá el porcentaje si tu caso es distinto y verificá tu convenio colectivo.</p>
            </div>""",
    related=[("/calculadoras/vida-diaria/calculadora-de-edad-y-fechas/", "Calculadora de Edad y Fechas"),
             ("/calculadoras/finanzas/calculadora-de-aguinaldo/", "Calculadora de Aguinaldo"),
             ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes")],
    guide=("/guias/como-calcular-horas-trabajadas-y-horas-extra/", "Cómo calcular horas trabajadas y horas extra",
           "Leé la guía completa: turnos nocturnos, conversión a decimal, recargos de horas extra y ejemplos con importes."),
    faqs=[("¿Cómo se calculan las horas trabajadas?",
           "Restando la hora de entrada a la de salida y descontando el descanso. De 09:00 a 18:00 con 60 minutos de descanso son 8 horas."),
          ("¿Cómo se calcula un turno nocturno?",
           "Si la salida es menor que la entrada, se suma un día: de 22:00 a 06:00 son 8 horas."),
          ("¿Cómo paso 8 horas y 45 minutos a decimal?",
           "Dividí los minutos por 60: 45/60 = 0,75, así que son 8,75 horas."),
          ("¿Cómo se pagan las horas extra?",
           "Con un recargo sobre el valor de la hora normal: en Argentina, 50% en días comunes y 100% los sábados después de las 13, domingos y feriados."),
          ("¿Esta calculadora reemplaza al recibo de sueldo?",
           "No: es una estimación. Los conceptos y recargos exactos dependen de tu convenio colectivo y de tu empleador.")],
))

# ----------------------------------------------------------- propina y cuenta
write("calculadoras/vida-diaria/calculadora-de-propina", calc_page(
    slug="calculadora-de-propina", name="Calculadora de Propina y División de la Cuenta", **CAT,
    page_title="Calculadora de Propina y División de la Cuenta | Calculadora Científica",
    desc="Calculá la propina (5%, 10%, 15%…) y dividí la cuenta entre varias personas, con redondeo hacia arriba. Ideal para restaurantes y salidas en grupo. Gratis.",
    og_title="Calculadora de Propina y División de la Cuenta",
    og_desc="Propina, total y cuánto paga cada uno, con redondeo. Gratis.",
    schema_desc="Calcula la propina como porcentaje de la cuenta, el total y cuánto paga cada persona al dividir entre varias, con opción de redondear hacia arriba.",
    intro="Ingresá el total de la cuenta, el porcentaje de propina y cuántas personas son: obtenés la propina, el total y lo que paga cada una, con redondeo opcional.",
    form_html=f"""        <div class="space-y-4">
{field("pr-bill", "Total de la cuenta ($)", "Ej: 25000")}
          <div>
{field("pr-tip", "Propina (%)", "Ej: 10", value="10")}
            <div class="mt-2 flex flex-wrap gap-2" aria-label="Porcentajes frecuentes">{"".join(f'<button type="button" data-tip="{n}" {CHIP}>{n} %</button>' for n in (0, 5, 10, 15, 20))}</div>
          </div>
{field("pr-people", "Cantidad de personas", "Ej: 4", value="2")}
          <div>
            <label for="pr-round" {LABEL}>Redondear lo que paga cada uno hacia arriba</label>
            <select id="pr-round" {SELECT}><option value="0">Sin redondeo</option><option value="10">Al múltiplo de $10</option><option value="100">Al múltiplo de $100</option><option value="1000">Al múltiplo de $1.000</option></select>
          </div>
          <button id="pr-solve" type="button" {BTN}>Calcular</button>
        </div>""",
    result_html=panel("pr").replace('<p id="pr-label" class="text-sm text-[var(--color-text-muted)]"></p>', '<p class="text-sm text-[var(--color-text-muted)]">Cada persona paga</p>'),
    help_html=f"""            <div>
              <h3 {H3}>Cómo se calcula</h3>
              <p {FORMULA}>propina = cuenta × % / 100 &nbsp;·&nbsp; por persona = (cuenta + propina) / personas</p>
              <p>Con una cuenta de $10.000, una propina del 10% y 4 personas: propina $1.000, total $11.000 y $2.750 por persona.</p>
            </div>
            <div>
              <h3 {H3}>Cuánto dejar de propina</h3>
              <p>En Argentina la propina no es obligatoria y la costumbre es dejar alrededor del 10% cuando el servicio fue bueno. No confundir con el "cubierto", que es un cargo del local por el servicio de mesa y está incluido en la cuenta.</p>
            </div>
            <div>
              <h3 {H3}>Redondeo</h3>
              <p>Si dividir da un número raro (como $3.666,67), podés redondear hacia arriba al múltiplo de $10, $100 o $1.000: el excedente se suma a la propina y a todos les queda un monto cómodo para pagar.</p>
            </div>""",
    related=[("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes"),
             ("/calculadoras/finanzas/calculadora-de-iva/", "Calculadora de IVA"),
             ("/calculadoras/matematicas-avanzadas/calculadora-basica/", "Calculadora Básica")],
    guide=("/guias/como-calcular-la-propina-y-dividir-la-cuenta/", "Cómo calcular la propina y dividir la cuenta",
           "Leé la guía completa: cuánto dejar, cómo dividir de forma justa y cómo redondear sin perder la cuenta."),
    faqs=[("¿Cómo se calcula la propina?",
           "Multiplicando la cuenta por el porcentaje y dividiendo por 100. El 10% de $25.000 es $2.500."),
          ("¿Cuánto es la propina habitual en Argentina?",
           "Alrededor del 10% si el servicio fue bueno. No es obligatoria ni está incluida salvo que la cuenta lo indique."),
          ("¿Cómo divido la cuenta entre varias personas?",
           "Sumá la propina al total y dividí por la cantidad de personas: (cuenta + propina) / personas."),
          ("¿Y si cada uno consumió distinto?",
           "Esta calculadora divide en partes iguales. Si los consumos son muy distintos, conviene que cada uno pague lo suyo más una parte proporcional de la propina."),
          ("¿Para qué sirve el redondeo?",
           "Para que cada persona pague un monto redondo; la diferencia que sobra se suma a la propina.")],
))
