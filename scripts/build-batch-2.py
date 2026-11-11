"""
build-batch-2.py — Genera las 5 calculadoras del lote 2 (masa molar, promedio de notas,
regla de tres, interés simple, MCD y MCM). Los script.js de cada una se escriben a mano
en su carpeta; este script solo produce los index.html con scripts/page_templates.py.

Es una generación de una sola vez: después de generar, el HTML de cada página es la
fuente de verdad (se edita directo). Se deja en el repo como referencia de cómo armar
una página nueva.
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


def field(id_, label, placeholder, extra=""):
    return (f'        <div{extra}>\n          <label for="{id_}" {LABEL}>{label}</label>\n'
            f'          <input id="{id_}" type="text" inputmode="decimal" placeholder="{placeholder}" {INPUT} />\n        </div>')


def write(rel, html):
    path = ROOT / rel / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("escrito:", path.relative_to(ROOT))


# ------------------------------------------------------------------ masa molar
chips = "".join(f'<button type="button" data-example="{f}" {CHIP}>{f}</button>' for f in
                ["H2O", "NaCl", "H2SO4", "Ca(OH)2", "C6H12O6", "CuSO4·5H2O"])
write("calculadoras/quimica/calculadora-de-masa-molar", calc_page(
    slug="calculadora-de-masa-molar", cat_slug="quimica", cat_label="Química", name="Calculadora de Masa Molar",
    page_title="Calculadora de Masa Molar Online: Fórmula y Composición | Calculadora Científica",
    desc="Calculá la masa molar de cualquier compuesto escribiendo su fórmula (H2SO4, Ca(OH)2, CuSO4·5H2O): desglose por elemento, composición porcentual y conversión masa-moles.",
    og_title="Calculadora de Masa Molar Online",
    og_desc="Escribí la fórmula y obtené la masa molar, el desglose por elemento y el % en masa. Gratis.",
    schema_desc="Calcula la masa molar de un compuesto a partir de su fórmula química, con el desglose por elemento, la composición porcentual y la conversión entre masa y moles.",
    intro="Escribí la fórmula química de un compuesto y obtené su masa molar en g/mol, con el aporte de cada elemento y el porcentaje en masa. Acepta paréntesis y sales hidratadas.",
    form_html=f"""        <div class="space-y-4">
          <div>
            <label for="mm-formula" {LABEL}>Fórmula química</label>
            <input id="mm-formula" type="text" autocomplete="off" spellcheck="false" placeholder="Ej: H2SO4 o Ca(OH)2" {INPUT} />
            <div class="mt-2 flex flex-wrap gap-2" aria-label="Ejemplos">{chips}</div>
          </div>
{field("mm-grams", "Masa de la muestra (g) — opcional", "Ej: 49")}
{field("mm-moles", "Moles — opcional", "Ej: 0,5")}
          <button id="mm-solve" type="button" {BTN}>Calcular masa molar</button>
        </div>""",
    result_html=f"""        <section id="mm-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>Masa molar</h2>
          <p class="text-sm {MUTED}">Fórmula: <span id="mm-formula-shown" {FORMULA}></span></p>
          <p id="mm-total" class="font-numeric text-3xl font-bold {PRIMARY} mt-1">—</p>
          <div class="mt-4 overflow-x-auto rounded-xl border border-[var(--color-border)]">
            <table class="w-full text-sm min-w-[380px] font-numeric">
              <thead>
                <tr class="text-left {MUTED}">
                  <th class="px-3 py-2 font-semibold">Elemento</th>
                  <th class="px-3 py-2 font-semibold">Átomos</th>
                  <th class="px-3 py-2 font-semibold">Masa atómica</th>
                  <th class="px-3 py-2 font-semibold">Aporte (g/mol)</th>
                  <th class="px-3 py-2 font-semibold">% en masa</th>
                </tr>
              </thead>
              <tbody id="mm-rows" class="{MUTED}"></tbody>
            </table>
          </div>
          <div id="mm-conv" class="hidden mt-4 text-sm space-y-1"></div>
        </section>""",
    help_html=f"""            <div>
              <h3 {H3}>Masa molar</h3>
              <p {FORMULA}>M = Σ (átomos de cada elemento × su masa atómica)</p>
              <p>Se expresa en g/mol. Ejemplo: H₂O = 2 × 1,008 + 15,999 = 18,02 g/mol.</p>
            </div>
            <div>
              <h3 {H3}>Escribir la fórmula</h3>
              <p>Usá mayúscula al empezar cada símbolo y minúscula para la segunda letra (<span {FORMULA}>Co</span> es cobalto, <span {FORMULA}>CO</span> es carbono y oxígeno). Los subíndices se escriben como números normales y se aceptan paréntesis y corchetes: <span {FORMULA}>Al2(SO4)3</span>. Para hidratos usá un punto medio, un punto o un asterisco: <span {FORMULA}>CuSO4·5H2O</span>.</p>
            </div>
            <div>
              <h3 {H3}>De masa a moles</h3>
              <p {FORMULA}>n = masa / masa molar &nbsp;·&nbsp; masa = n × masa molar</p>
            </div>
            <div>
              <h3 {H3}>Masas atómicas</h3>
              <p>Se usan los valores estándar de la IUPAC redondeados (H 1,008; C 12,011; O 15,999; S 32,065; Cl 35,45…). Distintos libros redondean algunos elementos de forma diferente, así que el último decimal puede variar.</p>
            </div>""",
    related=[("/calculadoras/quimica/calculadora-de-molaridad/", "Calculadora de Molaridad"),
             ("/calculadoras/quimica/calculadora-de-diluciones/", "Calculadora de Diluciones"),
             ("/calculadoras/quimica/calculadora-de-ph/", "Calculadora de pH y pOH")],
    guide=("/guias/como-calcular-masa-molar/", "Cómo calcular la masa molar",
           "Leé la guía completa: cómo sumar las masas atómicas paso a paso, con ejemplos de compuestos con paréntesis e hidratos."),
    faqs=[("¿Cómo se calcula la masa molar de un compuesto?",
           "Se cuenta cuántos átomos hay de cada elemento en la fórmula, se multiplica cada cantidad por la masa atómica del elemento (en g/mol) y se suman los resultados. Por ejemplo, H₂O = 2 × 1,008 + 15,999 = 18,02 g/mol."),
          ("¿Cómo se calcula la masa molar de un compuesto con paréntesis?",
           "Se multiplica todo lo que está dentro del paréntesis por el subíndice de afuera. En Ca(OH)₂ hay 1 Ca, 2 O y 2 H: 40,078 + 2 × 15,999 + 2 × 1,008 = 74,09 g/mol."),
          ("¿Cuál es la diferencia entre masa molar y masa molecular?",
           "Numéricamente coinciden, pero las unidades son distintas: la masa molar se mide en g/mol (masa de un mol de sustancia) y la masa molecular relativa es adimensional (masa de una molécula comparada con 1/12 del carbono-12)."),
          ("¿Para qué sirve la masa molar?",
           "Para convertir entre gramos y moles (n = masa / masa molar), y de ahí calcular molaridad, preparar soluciones o hacer cálculos estequiométricos.")],
))

# --------------------------------------------------------------- promedio notas
write("calculadoras/estadistica/calculadora-de-promedio-de-notas", calc_page(
    slug="calculadora-de-promedio-de-notas", cat_slug="estadistica", cat_label="Estadística",
    name="Calculadora de Promedio de Notas",
    page_title="Calculadora de Promedio de Notas: Simple y Ponderado | Calculadora Científica",
    desc="Calculá tu promedio de notas, simple o ponderado (cada nota con su peso), y descubrí qué nota necesitás en el próximo examen para llegar al promedio que querés. Gratis.",
    og_title="Calculadora de Promedio de Notas",
    og_desc="Promedio simple o ponderado y qué nota necesitás para llegar a tu objetivo. Gratis.",
    schema_desc="Calcula el promedio simple o ponderado de una lista de notas y la nota que hace falta sacar para llegar a un promedio objetivo.",
    intro="Cargá tus notas y obtené el promedio. Si cada nota tiene un peso distinto (parciales, trabajos prácticos, final), activá el modo ponderado. También te calcula qué nota necesitás para llegar al promedio que querés.",
    form_html=f"""        <div class="space-y-4">
          <label class="flex items-center gap-2 text-sm font-medium">
            <input id="pn-weighted" type="checkbox" class="w-4 h-4" />
            Cada nota tiene un peso distinto (promedio ponderado)
          </label>
          <div id="pn-rows" class="space-y-2"></div>
          <button id="pn-add" type="button" class="text-sm font-semibold {PRIMARY} hover:underline">+ Agregar otra nota</button>

          <div class="pt-3 border-t border-[var(--color-border)] space-y-3">
            <p class="text-sm font-semibold">¿Qué nota necesito? <span class="font-normal {MUTED}">(opcional)</span></p>
{field("pn-target", "Promedio que querés lograr", "Ej: 7")}
            <div id="pn-remaining-wrap" class="hidden">
              <label for="pn-remaining" {LABEL}>Peso de la nota que falta (%)</label>
              <input id="pn-remaining" type="text" inputmode="decimal" placeholder="Ej: 40" {INPUT} />
            </div>
{field("pn-max", "Nota máxima de tu escala — opcional", "Ej: 10")}
          </div>
          <button id="pn-solve" type="button" {BTN}>Calcular promedio</button>
        </div>""",
    result_html=f"""        <section id="pn-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>Resultado</h2>
          <p class="text-sm {MUTED}">Tu promedio</p>
          <p id="pn-average" class="font-numeric text-4xl font-bold {PRIMARY}">—</p>
          <p id="pn-detail" class="mt-2 text-sm {MUTED}"></p>
          <p id="pn-need" class="hidden mt-4 rounded-xl surface p-3 text-sm"></p>
        </section>""",
    help_html=f"""            <div>
              <h3 {H3}>Promedio simple</h3>
              <p {FORMULA}>promedio = (n₁ + n₂ + … + nₖ) / k</p>
              <p>Se suman todas las notas y se divide por la cantidad. Ejemplo: 7, 8 y 6 → 21 / 3 = 7.</p>
            </div>
            <div>
              <h3 {H3}>Promedio ponderado</h3>
              <p {FORMULA}>promedio = Σ (nota × peso) / Σ pesos</p>
              <p>Cada nota se multiplica por su peso. Ejemplo: 8 con peso 40% y 6 con peso 60% → (8 × 40 + 6 × 60) / 100 = 6,8.</p>
            </div>
            <div>
              <h3 {H3}>¿Qué nota necesito?</h3>
              <p {FORMULA}>nota necesaria = (objetivo × (Σ pesos + peso restante) − Σ nota × peso) / peso restante</p>
              <p>Si no usás pesos, la nota que falta cuenta igual que las demás. Cada institución define cómo redondea y qué promedio mínimo exige: usá este resultado como referencia.</p>
            </div>""",
    related=[("/calculadoras/estadistica/calculadora-estadistica-descriptiva/", "Estadística Descriptiva"),
             ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes"),
             ("/calculadoras/matematicas-avanzadas/calculadora-basica/", "Calculadora Básica")],
    guide=("/guias/como-calcular-promedio-de-notas/", "Cómo calcular el promedio de notas",
           "Leé la guía completa: promedio simple, promedio ponderado, y cómo saber qué nota necesitás para aprobar o llegar a tu objetivo."),
    faqs=[("¿Cómo se calcula el promedio de notas?",
           "Se suman todas las notas y se divide por la cantidad de notas. Con 7, 8 y 6: (7 + 8 + 6) / 3 = 7."),
          ("¿Cómo se calcula un promedio ponderado?",
           "Se multiplica cada nota por su peso, se suman esos productos y se divide por la suma de los pesos. Con 8 (peso 40%) y 6 (peso 60%): (8 × 40 + 6 × 60) / 100 = 6,8."),
          ("¿Cómo sé qué nota necesito para llegar a un promedio?",
           "Se despeja la nota que falta: multiplicás el promedio objetivo por la cantidad total de notas (o por el peso total), restás lo que ya acumulaste y dividís por el peso de la nota que falta."),
          ("¿Qué pasa si los pesos no suman 100%?",
           "El promedio ponderado se calcula igual, dividiendo por la suma real de los pesos. La calculadora te avisa cuando no llegan a 100% para que revises si falta alguna nota.")],
))

# ---------------------------------------------------------------- regla de tres
tabs = "".join(
    f'<button type="button" data-tab="{k}" class="rt-tab-btn px-4 py-2 rounded-full text-sm font-semibold">{v}</button>'
    for k, v in [("directa", "Simple directa"), ("inversa", "Simple inversa"), ("compuesta", "Compuesta")])


def comp_row(i, optional=False):
    tag = " — opcional" if optional else ""
    return f"""          <div class="space-y-2">
            <p class="text-sm font-semibold">Dato {i}{tag}</p>
            <div class="grid grid-cols-2 gap-2">
              <input id="comp-{i}-v1" type="text" inputmode="decimal" placeholder="Valor inicial" aria-label="Dato {i}, valor inicial" {INPUT} />
              <input id="comp-{i}-v2" type="text" inputmode="decimal" placeholder="Valor nuevo" aria-label="Dato {i}, valor nuevo" {INPUT} />
            </div>
            <select id="comp-{i}-dir" aria-label="Relación del dato {i}" {SELECT}>
              <option value="directa">Relación directa (si aumenta, el resultado aumenta)</option>
              <option value="inversa">Relación inversa (si aumenta, el resultado disminuye)</option>
            </select>
          </div>"""


def simple_panel(kind, hint):
    return f"""        <div id="rt-panel-{kind}" class="space-y-4">
          <p class="text-sm {MUTED}">{hint}</p>
{field(f"{kind}-a", "A", "Ej: 3")}
{field(f"{kind}-b", "B", "Ej: 12")}
{field(f"{kind}-c", "C", "Ej: 5")}
          <button id="rt-{kind}-solve" type="button" {BTN}>Calcular x</button>
        </div>"""


write("calculadoras/matematicas-avanzadas/regla-de-tres", calc_page(
    slug="regla-de-tres", cat_slug="matematicas-avanzadas", cat_label="Matemáticas Avanzadas", name="Calculadora de Regla de Tres",
    page_title="Calculadora de Regla de Tres: Simple, Inversa y Compuesta | Calculadora Científica",
    desc="Resolvé regla de tres simple directa, simple inversa y compuesta con el desarrollo paso a paso. Gratis y sin registro.",
    og_title="Calculadora de Regla de Tres",
    og_desc="Regla de tres simple directa, inversa y compuesta, con el desarrollo paso a paso. Gratis.",
    schema_desc="Resuelve problemas de regla de tres simple (directa e inversa) y compuesta, mostrando los pasos del cálculo.",
    intro="Resolvé problemas de proporcionalidad: regla de tres simple directa, simple inversa y compuesta, con el desarrollo paso a paso.",
    top_html=f'\n    <div class="mt-6 inline-flex flex-wrap rounded-full surface p-1 gap-1">{tabs}</div>\n',
    form_html=(simple_panel("directa", "Si <strong>A</strong> corresponde a <strong>B</strong>, ¿a cuánto corresponde <strong>C</strong>? Es directa cuando al aumentar una cantidad, aumenta la otra.")
               + "\n" + simple_panel("inversa", "Si <strong>A</strong> corresponde a <strong>B</strong>, ¿a cuánto corresponde <strong>C</strong>? Es inversa cuando al aumentar una cantidad, la otra disminuye (por ejemplo, obreros y días de trabajo).")
               + f"""
        <div id="rt-panel-compuesta" class="space-y-4">
          <p class="text-sm {MUTED}">Cargá el resultado conocido y, para cada dato que cambia, su valor inicial, su valor nuevo y si la relación con el resultado es directa o inversa.</p>
{field("comp-r1", "Resultado conocido", "Ej: 200")}
{comp_row(1)}
{comp_row(2)}
{comp_row(3, True)}
          <button id="rt-compuesta-solve" type="button" {BTN}>Calcular x</button>
        </div>"""),
    result_html=f"""        <section id="rt-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>Resultado</h2>
          <p id="rt-result" class="font-numeric text-3xl font-bold {PRIMARY}">—</p>
          <p id="rt-detail" class="mt-1 text-sm {MUTED}"></p>
          <ol id="rt-steps" class="mt-3 space-y-1 text-sm font-numeric list-decimal list-inside"></ol>
        </section>""",
    help_html=f"""            <div>
              <h3 {H3}>Regla de tres simple directa</h3>
              <p {FORMULA}>x = (B × C) / A</p>
              <p>Las dos cantidades crecen o decrecen juntas. Ejemplo: 3 kg cuestan $12; 5 kg cuestan x → x = (12 × 5) / 3 = $20.</p>
            </div>
            <div>
              <h3 {H3}>Regla de tres simple inversa</h3>
              <p {FORMULA}>x = (A × B) / C</p>
              <p>Cuando una cantidad aumenta, la otra disminuye. Ejemplo: 3 obreros tardan 12 días; 4 obreros tardan x → x = (3 × 12) / 4 = 9 días.</p>
            </div>
            <div>
              <h3 {H3}>Regla de tres compuesta</h3>
              <p {FORMULA}>x = R × (v₂/v₁) para cada dato directo, y × (v₁/v₂) para cada dato inverso</p>
              <p>Se parte del resultado conocido y se multiplica por el cociente de cada dato que cambia. Ejemplo: 5 obreros en 10 días hacen 200 m; 8 obreros en 5 días hacen 200 × (8/5) × (5/10) = 160 m.</p>
            </div>
            <div>
              <h3 {H3}>¿Directa o inversa?</h3>
              <p>Preguntate: si una cantidad se duplica, ¿la otra también se duplica (directa) o se reduce a la mitad (inversa)?</p>
            </div>""",
    related=[("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes"),
             ("/calculadoras/matematicas-avanzadas/calculadora-basica/", "Calculadora Básica"),
             ("/calculadoras/matematicas-avanzadas/mcd-y-mcm/", "Calculadora de MCD y MCM")],
    guide=("/guias/regla-de-tres-simple-y-compuesta/", "Regla de tres simple y compuesta",
           "Leé la guía completa: cómo distinguir una relación directa de una inversa y cómo resolver cada tipo, con ejemplos."),
    faqs=[("¿Cómo se resuelve una regla de tres simple directa?",
           "Se multiplican en cruz los dos valores conocidos de distinta fila y se divide por el que queda: si A corresponde a B y C corresponde a x, entonces x = (B × C) / A."),
          ("¿Cómo se resuelve una regla de tres inversa?",
           "Se multiplican los valores de la misma fila y se divide por el otro dato: si A corresponde a B y C corresponde a x en proporción inversa, entonces x = (A × B) / C."),
          ("¿Cómo se sabe si es directa o inversa?",
           "Si al aumentar una cantidad la otra también aumenta en la misma proporción, es directa (kilos y precio). Si al aumentar una la otra disminuye, es inversa (obreros y días de trabajo, velocidad y tiempo)."),
          ("¿Qué es la regla de tres compuesta?",
           "Es la que relaciona más de dos magnitudes. Se parte del resultado conocido y se multiplica por el cociente de cada dato que cambia, invirtiéndolo cuando la relación con el resultado es inversa.")],
))

# ---------------------------------------------------------------- interés simple
write("calculadoras/finanzas/calculadora-de-interes-simple", calc_page(
    slug="calculadora-de-interes-simple", cat_slug="finanzas", cat_label="Finanzas", name="Calculadora de Interés Simple",
    page_title="Calculadora de Interés Simple: Capital, Tasa y Tiempo | Calculadora Científica",
    desc="Calculá el interés simple y el monto final, o despejá el capital, la tasa o el tiempo. Con tasa anual, mensual o diaria y tiempo en años, meses o días. Gratis.",
    og_title="Calculadora de Interés Simple",
    og_desc="Interés, monto, capital, tasa o tiempo con la fórmula I = C × i × t. Gratis.",
    schema_desc="Calcula el interés simple (I = C·i·t), el monto final, y permite despejar el capital, la tasa de interés o el tiempo.",
    intro="Calculá el interés simple y el monto final de un capital, o despejá el capital, la tasa o el tiempo a partir de los demás datos. La tasa puede ser anual, mensual o diaria, y el tiempo en años, meses o días.",
    form_html=f"""        <div class="space-y-4">
          <div>
            <label for="is-target" {LABEL}>¿Qué querés calcular?</label>
            <select id="is-target" {SELECT}>
              <option value="interes">Interés y monto final</option>
              <option value="capital">Capital inicial</option>
              <option value="tasa">Tasa de interés</option>
              <option value="tiempo">Tiempo</option>
            </select>
          </div>
{field("is-capital", "Capital ($)", "Ej: 100000", ' data-field="capital"')}
{field("is-interes", "Interés ganado ($)", "Ej: 12000", ' data-field="interes"')}
          <div data-field="tasa">
            <label for="is-tasa" {LABEL}>Tasa de interés (%)</label>
            <div class="grid grid-cols-[1fr_auto] gap-2">
              <input id="is-tasa" type="text" inputmode="decimal" placeholder="Ej: 24" {INPUT} />
              <select id="is-rate-period" aria-label="Período de la tasa" {SELECT}>
                <option value="anual">anual</option>
                <option value="mensual">mensual</option>
                <option value="diaria">diaria</option>
              </select>
            </div>
          </div>
          <div data-field="tiempo">
            <label for="is-tiempo" {LABEL}>Tiempo</label>
            <div class="grid grid-cols-[1fr_auto] gap-2">
              <input id="is-tiempo" type="text" inputmode="decimal" placeholder="Ej: 6" {INPUT} />
              <select id="is-time-unit" aria-label="Unidad de tiempo" {SELECT}>
                <option value="meses">meses</option>
                <option value="anios">años</option>
                <option value="dias">días</option>
              </select>
            </div>
          </div>
          <button id="is-solve" type="button" {BTN}>Calcular</button>
        </div>""",
    result_html=f"""        <section id="is-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>Resultado</h2>
          <p id="is-label" class="text-sm {MUTED}"></p>
          <p id="is-main" class="font-numeric text-3xl font-bold {PRIMARY}">—</p>
          <div id="is-lines" class="mt-2 text-sm {MUTED} space-y-1"></div>
        </section>""",
    help_html=f"""            <div>
              <h3 {H3}>Interés simple</h3>
              <p {FORMULA}>I = C × i × t &nbsp;·&nbsp; M = C + I = C × (1 + i × t)</p>
              <p>I es el interés, C el capital inicial, i la tasa (en la misma unidad de tiempo que t) y M el monto final. En el interés simple el interés se calcula siempre sobre el capital inicial: no se capitaliza.</p>
            </div>
            <div>
              <h3 {H3}>Despejando</h3>
              <p {FORMULA}>C = I / (i × t) &nbsp;·&nbsp; i = I / (C × t) &nbsp;·&nbsp; t = I / (C × i)</p>
            </div>
            <div>
              <h3 {H3}>Unidades</h3>
              <p>La calculadora pasa tasa y tiempo a años para operar (12 meses o 365 días por año) y te muestra el resultado en la unidad que elegiste. Una tasa mensual del 2% equivale a una tasa anual del 24% en interés simple.</p>
            </div>""",
    related=[("/calculadoras/finanzas/interes-compuesto/", "Interés Compuesto"),
             ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes"),
             ("/calculadoras/finanzas/amortizacion-prestamos/", "Amortización de Préstamos")],
    guide=("/guias/interes-simple-vs-compuesto/", "Interés simple vs interés compuesto",
           "Leé la guía completa: en qué se diferencian los dos tipos de interés y cuándo conviene cada uno, con un ejemplo comparativo."),
    faqs=[("¿Cómo se calcula el interés simple?",
           "Con la fórmula I = C × i × t: capital por tasa por tiempo, con la tasa y el tiempo en la misma unidad. Con $100.000 al 24% anual durante 6 meses: 100.000 × 0,24 × 0,5 = $12.000."),
          ("¿Cómo se calcula el monto final con interés simple?",
           "Se suma el interés al capital: M = C + I = C × (1 + i × t). Con el ejemplo anterior, el monto final es $112.000."),
          ("¿Cómo se pasa una tasa mensual a anual en interés simple?",
           "Se multiplica por 12. Una tasa mensual del 2% equivale a una anual del 24%. En interés compuesto no alcanza con multiplicar, porque los intereses se capitalizan."),
          ("¿Qué diferencia hay entre interés simple y compuesto?",
           "En el simple, el interés se calcula siempre sobre el capital inicial. En el compuesto, los intereses ganados se suman al capital y generan nuevos intereses, por eso crece más rápido a largo plazo.")],
))

# ------------------------------------------------------------------- MCD y MCM
chips2 = "".join(f'<button type="button" data-example="{v}" {CHIP}>{v}</button>' for v in ["12 18", "48 180 24", "17 5", "360 84"])
write("calculadoras/matematicas-avanzadas/mcd-y-mcm", calc_page(
    slug="mcd-y-mcm", cat_slug="matematicas-avanzadas", cat_label="Matemáticas Avanzadas", name="Calculadora de MCD y MCM",
    page_title="Calculadora de MCD y MCM: Máximo Común Divisor y Mínimo Común Múltiplo | Calculadora Científica",
    desc="Calculá el MCD y el MCM de dos o más números con la descomposición en factores primos y el algoritmo de Euclides paso a paso. Gratis y sin registro.",
    og_title="Calculadora de MCD y MCM",
    og_desc="Máximo común divisor y mínimo común múltiplo con el desarrollo paso a paso. Gratis.",
    schema_desc="Calcula el máximo común divisor (MCD) y el mínimo común múltiplo (MCM) de 2 a 10 números enteros, con la descomposición en factores primos y el algoritmo de Euclides.",
    intro="Ingresá dos o más números enteros y obtené el máximo común divisor (MCD) y el mínimo común múltiplo (MCM), con la descomposición en factores primos y el algoritmo de Euclides paso a paso.",
    form_html=f"""        <div class="space-y-4">
          <div>
            <label for="md-input" {LABEL}>Números (separados por espacios o comas)</label>
            <input id="md-input" type="text" inputmode="numeric" autocomplete="off" placeholder="Ej: 48 180 24" {INPUT} />
            <div class="mt-2 flex flex-wrap gap-2" aria-label="Ejemplos">{chips2}</div>
          </div>
          <button id="md-solve" type="button" {BTN}>Calcular MCD y MCM</button>
        </div>""",
    result_html=f"""        <section id="md-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>Resultado</h2>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm {MUTED}">MCD</p>
              <p id="md-gcd" class="font-numeric text-3xl font-bold {PRIMARY} break-all">—</p>
            </div>
            <div>
              <p class="text-sm {MUTED}">MCM</p>
              <p id="md-lcm" class="font-numeric text-3xl font-bold {PRIMARY} break-all">—</p>
            </div>
          </div>
          <div id="md-steps" class="mt-4 text-sm {MUTED}"></div>
        </section>""",
    help_html=f"""            <div>
              <h3 {H3}>MCD: máximo común divisor</h3>
              <p>Es el mayor número que divide a todos los números a la vez. Con factores primos: se toman los factores comunes con el <strong>menor</strong> exponente. Ejemplo: 12 = 2² × 3 y 18 = 2 × 3² → MCD = 2 × 3 = 6.</p>
            </div>
            <div>
              <h3 {H3}>MCM: mínimo común múltiplo</h3>
              <p>Es el menor número positivo que es múltiplo de todos. Con factores primos: se toman todos los factores, comunes y no comunes, con el <strong>mayor</strong> exponente. Ejemplo: 12 y 18 → 2² × 3² = 36.</p>
            </div>
            <div>
              <h3 {H3}>Relación entre ambos</h3>
              <p {FORMULA}>MCD(a, b) × MCM(a, b) = a × b</p>
              <p>Con esa fórmula, el MCM de dos números se calcula como (a × b) / MCD.</p>
            </div>
            <div>
              <h3 {H3}>Algoritmo de Euclides</h3>
              <p>Se divide el mayor por el menor y se repite con el divisor y el resto, hasta que el resto sea 0. El último resto distinto de 0 es el MCD.</p>
            </div>""",
    related=[("/calculadoras/matematicas-avanzadas/regla-de-tres/", "Calculadora de Regla de Tres"),
             ("/calculadoras/matematicas-avanzadas/calculadora-basica/", "Calculadora Básica"),
             ("/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/", "Calculadora Científica Online")],
    guide=("/guias/como-calcular-mcd-y-mcm/", "Cómo calcular el MCD y el MCM",
           "Leé la guía completa: factores primos, algoritmo de Euclides y cuándo usar cada uno, con ejemplos resueltos."),
    faqs=[("¿Cómo se calcula el MCD de dos números?",
           "Podés usar factores primos (se toman los comunes con el menor exponente) o el algoritmo de Euclides (se divide el mayor por el menor y se repite con el resto hasta llegar a 0; el último resto distinto de 0 es el MCD). Para 48 y 18: 48 = 18 × 2 + 12, 18 = 12 × 1 + 6, 12 = 6 × 2 + 0, así que MCD = 6."),
          ("¿Cómo se calcula el MCM?",
           "Con factores primos se toman todos los factores con el mayor exponente. También se puede calcular como el producto de los dos números dividido por su MCD: MCM(12, 18) = 12 × 18 / 6 = 36."),
          ("¿Para qué sirven el MCD y el MCM?",
           "El MCD sirve para simplificar fracciones y repartir en grupos iguales; el MCM, para sumar fracciones con distinto denominador y para problemas de coincidencia (cada cuánto tiempo se vuelven a encontrar dos eventos periódicos)."),
          ("¿Qué pasa si los números son primos entre sí?",
           "Si no tienen ningún factor primo en común, su MCD es 1 y su MCM es simplemente el producto de ambos. Por ejemplo, 17 y 5: MCD = 1, MCM = 85.")],
))
