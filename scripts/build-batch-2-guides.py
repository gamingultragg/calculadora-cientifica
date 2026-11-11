"""
build-batch-2-guides.py — Genera las 4 guías del lote 2: masa molar, promedio de notas,
regla de tres y MCD/MCM (la de interés simple reutiliza interes-simple-vs-compuesto).
Generación de una sola vez; después el HTML es la fuente de verdad.
"""
from pathlib import Path

from page_templates import esc, guide_page

ROOT = Path(__file__).resolve().parent.parent
M = "text-[var(--color-text-muted)]"


def h2(t):
    return f'      <h2 class="font-display font-bold text-xl mt-8 mb-2">{t}</h2>'


def h3(t):
    return f'      <h3 class="font-display font-semibold text-base mt-5 mb-1">{t}</h3>'


def p(t):
    return f'      <p class="{M} leading-relaxed">\n        {t}\n      </p>'


def formula(t):
    return f'      <p class="font-numeric text-center my-3 text-[var(--color-text)]">{t}</p>'


def ol(items):
    li = "\n".join(f"        <li>{i}</li>" for i in items)
    return f'      <ol class="list-decimal list-inside space-y-1 {M}">\n{li}\n      </ol>'


def steps(items):
    li = "\n".join(f"        <li>{i}</li>" for i in items)
    return f'      <ol class="list-decimal list-inside space-y-1 {M} font-numeric">\n{li}\n      </ol>'


def ul(items):
    li = "\n".join(f"        <li>{i}</li>" for i in items)
    return f'      <ul class="list-disc list-inside space-y-1 {M}">\n{li}\n      </ul>'


def table(head, rows):
    th = "".join(f'<th class="px-3 py-2 font-semibold">{c}</th>' for c in head)
    tr = "\n".join(
        '            <tr class="border-t border-[var(--color-border)]">' + "".join(f'<td class="px-3 py-2">{c}</td>' for c in r) + "</tr>"
        for r in rows
    )
    return (f'      <div class="mt-3 overflow-x-auto rounded-xl border border-[var(--color-border)]">\n'
            f'        <table class="w-full text-sm min-w-[360px] font-numeric">\n'
            f'          <thead><tr class="text-left {M}">{th}</tr></thead>\n'
            f'          <tbody class="{M}">\n{tr}\n          </tbody>\n        </table>\n      </div>')


def write(slug, html):
    path = ROOT / "guias" / slug / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("escrito:", path.relative_to(ROOT))


# ============================================================ masa molar
body = "\n\n".join([
    h2("1. Qué es la masa molar"),
    p("La masa molar es la masa de <strong class=\"text-[var(--color-text)]\">un mol</strong> de una sustancia, es decir, de 6,022 × 10²³ unidades (átomos, moléculas o fórmulas). Se mide en gramos por mol (g/mol) y se obtiene sumando las masas atómicas de todos los átomos de la fórmula."),
    h2("2. Cómo calcularla, paso a paso"),
    ol([
        "Escribí la fórmula y contá cuántos átomos hay de cada elemento (los subíndices; si no hay, es 1).",
        "Buscá la masa atómica de cada elemento en la tabla periódica.",
        "Multiplicá la cantidad de átomos de cada elemento por su masa atómica.",
        "Sumá todos los resultados. El total, en g/mol, es la masa molar.",
    ]),
    formula("M = Σ (átomos de cada elemento × su masa atómica)"),
    h2("3. Ejemplos resueltos"),
    h3("Ácido sulfúrico, H₂SO₄"),
    steps(["H: 2 × 1,008 = 2,016", "S: 1 × 32,065 = 32,065", "O: 4 × 15,999 = 63,996", "M = 2,016 + 32,065 + 63,996 = 98,08 g/mol"]),
    h3("Hidróxido de calcio, Ca(OH)₂ — con paréntesis"),
    p("El subíndice de afuera multiplica todo lo que está dentro del paréntesis: hay 1 Ca, 2 O y 2 H."),
    steps(["Ca: 1 × 40,078 = 40,078", "O: 2 × 15,999 = 31,998", "H: 2 × 1,008 = 2,016", "M = 40,078 + 31,998 + 2,016 = 74,09 g/mol"]),
    h3("Sulfato de aluminio, Al₂(SO₄)₃"),
    p("Dentro del paréntesis hay 1 S y 4 O, y el 3 de afuera lo multiplica: 3 S y 12 O."),
    steps(["Al: 2 × 26,982 = 53,964", "S: 3 × 32,065 = 96,195", "O: 12 × 15,999 = 191,988", "M = 53,964 + 96,195 + 191,988 = 342,15 g/mol"]),
    h3("Sulfato de cobre pentahidratado, CuSO₄·5H₂O — con agua de hidratación"),
    p("La masa molar de la sal anhidra se suma a 5 veces la del agua (H₂O = 18,015 g/mol)."),
    steps(["CuSO₄: 63,546 + 32,065 + 4 × 15,999 = 159,607", "5 H₂O: 5 × 18,015 = 90,075", "M = 159,607 + 90,075 = 249,68 g/mol"]),
    h2("4. Masa molar, masa molecular y peso fórmula"),
    p("En la práctica se usan casi como sinónimos y dan el mismo número, pero no son lo mismo: la <strong class=\"text-[var(--color-text)]\">masa molar</strong> se expresa en g/mol, mientras que la <strong class=\"text-[var(--color-text)]\">masa molecular relativa</strong> es adimensional. Para compuestos iónicos como el NaCl, que no forman moléculas, se habla de masa fórmula."),
    h2("5. Para qué se usa: pasar de gramos a moles"),
    formula("n = masa / masa molar"),
    p("Ejemplo: ¿cuántos moles son 49 g de H₂SO₄? n = 49 / 98,08 ≈ 0,5 mol. Con los moles podés calcular la molaridad de una solución (mirá <a class=\"text-[var(--color-primary-link)] hover:underline\" href=\"/guias/como-calcular-molaridad/\">cómo calcular la molaridad</a>) o hacer cálculos de estequiometría."),
    h2("6. Errores comunes"),
    ul([
        "Olvidar multiplicar el contenido del paréntesis por el subíndice de afuera.",
        "Confundir mayúsculas y minúsculas: <span class=\"font-numeric\">Co</span> es cobalto y <span class=\"font-numeric\">CO</span> es carbono más oxígeno.",
        "Usar el número atómico (Z) en lugar de la masa atómica.",
        "Olvidar el agua de hidratación en las sales hidratadas.",
    ]),
])
write("como-calcular-masa-molar", guide_page(
    slug="como-calcular-masa-molar", name="Cómo calcular la masa molar",
    page_title="Cómo Calcular la Masa Molar de un Compuesto Paso a Paso | Calculadora Científica",
    desc="Cómo calcular la masa molar de un compuesto: contar átomos, multiplicar por la masa atómica y sumar. Ejemplos con paréntesis e hidratos, y cómo pasar de gramos a moles.",
    og_desc="Contá los átomos, multiplicá por la masa atómica y sumá: ejemplos con paréntesis e hidratos.",
    headline="Cómo calcular la masa molar de un compuesto paso a paso",
    intro="La masa molar es el dato que conecta los gramos que pesás en el laboratorio con los moles que usás en las cuentas. Esta guía muestra cómo calcularla desde la fórmula, con ejemplos que incluyen paréntesis y sales hidratadas.",
    quick="Contá los átomos de cada elemento, multiplicá por su masa atómica y sumá todo. Por ejemplo, H₂O = 2 × 1,008 + 15,999 = 18,02 g/mol.",
    cta=("/calculadoras/quimica/calculadora-de-masa-molar/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cómo se calcula la masa molar?", "Se cuentan los átomos de cada elemento de la fórmula, se multiplica cada cantidad por su masa atómica en g/mol y se suman los resultados."),
          ("¿Cómo se calcula la masa molar con paréntesis?", "El subíndice de afuera multiplica todos los átomos de adentro. En Ca(OH)₂ hay 1 Ca, 2 O y 2 H."),
          ("¿Cómo paso de gramos a moles?", "Dividiendo la masa en gramos por la masa molar: n = masa / masa molar."),
          ("¿Se incluye el agua en las sales hidratadas?", "Sí: la masa molar del hidrato incluye la del agua de hidratación multiplicada por su coeficiente (CuSO₄·5H₂O suma 5 × 18,015 a la sal anhidra).")],
    related=[("/calculadoras/quimica/calculadora-de-masa-molar/", "Calculadora de Masa Molar"),
             ("/calculadoras/quimica/calculadora-de-molaridad/", "Calculadora de Molaridad"),
             ("/guias/como-calcular-molaridad/", "Guía: cómo calcular la molaridad")],
))

# ============================================================ promedio de notas
body = "\n\n".join([
    h2("1. Promedio simple"),
    formula("promedio = (n₁ + n₂ + … + nₖ) / k"),
    p("Se suman todas las notas y se divide por la cantidad de notas. Ejemplo: sacaste 7, 8 y 6 → (7 + 8 + 6) / 3 = 21 / 3 = <strong class=\"text-[var(--color-text)]\">7</strong>. Se usa cuando todas las notas valen lo mismo."),
    h2("2. Promedio ponderado"),
    formula("promedio = Σ (nota × peso) / Σ pesos"),
    p("Cuando las notas no valen lo mismo (un final pesa más que un trabajo práctico), cada nota se multiplica por su peso. Ejemplo con tres instancias:"),
    table(["Instancia", "Nota", "Peso", "Nota × peso"],
          [["Parcial", "7", "30%", "210"], ["Trabajo práctico", "9", "20%", "180"], ["Final", "6", "50%", "300"], ["<strong>Total</strong>", "", "<strong>100%</strong>", "<strong>690</strong>"]]),
    p("Promedio = 690 / 100 = <strong class=\"text-[var(--color-text)]\">6,9</strong>. Fijate que el promedio simple de esas notas sería 7,33: la nota baja del final pesa más y arrastra el resultado."),
    h2("3. ¿Qué nota necesito para llegar a un promedio?"),
    p("Si te falta una nota, se despeja de la fórmula del promedio."),
    h3("Sin pesos"),
    p("Tenés 7 y 8, y querés terminar con 8 de promedio en 3 notas: 8 × 3 = 24 puntos en total, ya tenés 15, necesitás <strong class=\"text-[var(--color-text)]\">9</strong>."),
    h3("Con pesos"),
    formula("nota necesaria = (objetivo × 100 − Σ nota × peso) / peso restante"),
    p("Tenés 6 con peso 30% y 8 con peso 30%, y el final vale 40%. Para llegar a 7: (7 × 100 − (6 × 30 + 8 × 30)) / 40 = (700 − 420) / 40 = <strong class=\"text-[var(--color-text)]\">7</strong>."),
    h2("4. Errores comunes"),
    ul([
        "<strong class=\"text-[var(--color-text)]\">Promediar promedios.</strong> El promedio de dos promedios solo es correcto si cada uno sale de la misma cantidad de notas; si no, hay que ponderar.",
        "Confundir el peso con la nota: el 30% es cuánto vale la instancia, no la nota que sacaste.",
        "Olvidar que los pesos tienen que sumar 100% (o dividir por la suma real).",
        "Dar por hecho el redondeo: cada institución define si redondea y cómo, y qué promedio mínimo exige para aprobar.",
    ]),
])
write("como-calcular-promedio-de-notas", guide_page(
    slug="como-calcular-promedio-de-notas", name="Cómo calcular el promedio de notas",
    page_title="Cómo Calcular el Promedio de Notas: Simple y Ponderado | Calculadora Científica",
    desc="Cómo calcular el promedio de notas, simple y ponderado, con ejemplos resueltos, y cómo saber qué nota necesitás en el próximo examen para llegar al promedio que querés.",
    og_desc="Promedio simple, promedio ponderado y qué nota necesitás para llegar a tu objetivo.",
    headline="Cómo calcular el promedio de notas: simple y ponderado",
    intro="Calcular el promedio parece simple, hasta que las notas tienen pesos distintos o te falta un examen. Esta guía muestra los dos tipos de promedio y cómo averiguar qué nota necesitás para llegar al que querés.",
    quick="Promedio simple: sumá las notas y dividí por la cantidad. Promedio ponderado: multiplicá cada nota por su peso, sumá y dividí por la suma de los pesos.",
    cta=("/calculadoras/estadistica/calculadora-de-promedio-de-notas/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cómo se calcula el promedio de notas?", "Se suman todas las notas y se divide por la cantidad. Con 7, 8 y 6 el promedio es 7."),
          ("¿Cómo se calcula el promedio ponderado?", "Se multiplica cada nota por su peso, se suman los productos y se divide por la suma de los pesos."),
          ("¿Qué nota necesito para llegar a cierto promedio?", "Se despeja de la fórmula: multiplicás el promedio objetivo por el total de notas (o por el peso total), restás lo acumulado y dividís por el peso de la nota que falta."),
          ("¿Se pueden promediar promedios?", "Solo si cada promedio sale de la misma cantidad de notas. Si no, hay que ponderar cada promedio por su cantidad de notas o por su peso.")],
    related=[("/calculadoras/estadistica/calculadora-de-promedio-de-notas/", "Calculadora de Promedio de Notas"),
             ("/calculadoras/estadistica/calculadora-estadistica-descriptiva/", "Estadística Descriptiva"),
             ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes")],
))

# ============================================================ regla de tres
body = "\n\n".join([
    h2("1. Qué es la regla de tres"),
    p("Es un método para resolver problemas de <strong class=\"text-[var(--color-text)]\">proporcionalidad</strong>: conocés tres valores de dos magnitudes relacionadas y querés hallar el cuarto. Según cómo se relacionen las magnitudes, puede ser directa o inversa."),
    h2("2. Regla de tres simple directa"),
    p("Las dos magnitudes crecen o decrecen juntas: si una se duplica, la otra también."),
    formula("A → B &nbsp;&nbsp; C → x &nbsp;&nbsp;⇒&nbsp;&nbsp; x = (B × C) / A"),
    p("Ejemplo: 3 kg de manzanas cuestan $12. ¿Cuánto cuestan 5 kg? x = (12 × 5) / 3 = <strong class=\"text-[var(--color-text)]\">$20</strong>."),
    h2("3. Regla de tres simple inversa"),
    p("Cuando una magnitud aumenta, la otra disminuye en la misma proporción."),
    formula("A → B &nbsp;&nbsp; C → x &nbsp;&nbsp;⇒&nbsp;&nbsp; x = (A × B) / C"),
    p("Ejemplo: 3 obreros tardan 12 días en terminar una obra. ¿Cuántos días tardan 4 obreros? x = (3 × 12) / 4 = <strong class=\"text-[var(--color-text)]\">9 días</strong>. Más obreros, menos días."),
    h2("4. ¿Directa o inversa? El truco del doble"),
    p("Preguntate qué pasa con el resultado si duplicás el dato: si <strong class=\"text-[var(--color-text)]\">también se duplica</strong>, es directa (kilos y precio, distancia y tiempo a velocidad constante). Si <strong class=\"text-[var(--color-text)]\">se reduce a la mitad</strong>, es inversa (obreros y días de trabajo, velocidad y tiempo para recorrer una distancia fija)."),
    h2("5. Regla de tres compuesta"),
    p("Relaciona más de dos magnitudes. Se parte del resultado conocido y se multiplica por el cociente de cada dato que cambia: <span class=\"font-numeric\">(nuevo / inicial)</span> si la relación con el resultado es directa y <span class=\"font-numeric\">(inicial / nuevo)</span> si es inversa."),
    h3("Ejemplo con dos relaciones directas"),
    p("5 obreros trabajando 10 días construyen 200 m de pared. ¿Cuántos metros construyen 8 obreros en 5 días? Más obreros, más metros (directa); menos días, menos metros (directa)."),
    steps(["x = 200 × (8 / 5) × (5 / 10)", "x = 200 × 1,6 × 0,5 = 160 m"]),
    h3("Ejemplo con dos relaciones inversas"),
    p("4 obreros que trabajan 6 horas por día terminan una obra en 15 días. ¿Cuántos días tardan 6 obreros trabajando 5 horas por día? Pasar de 4 a 6 obreros hace que tarden menos días (inversa), y pasar de 6 a 5 horas por día hace que tarden más días (también inversa). En las dos relaciones el cociente va invertido: valor inicial sobre valor nuevo."),
    steps(["x = 15 × (4 / 6) × (6 / 5)", "x = 15 × 0,6667 × 1,2 = 12 días"]),
    h2("6. Errores comunes"),
    ul([
        "Resolver siempre como directa sin preguntarse si la relación es inversa.",
        "Mezclar unidades (horas con minutos, metros con kilómetros) antes de calcular.",
        "En la compuesta, invertir mal el cociente de un dato: conviene escribir cada relación por separado antes de multiplicar.",
        "Aplicar regla de tres a magnitudes que no son proporcionales (por ejemplo, la edad y la altura).",
    ]),
])
write("regla-de-tres-simple-y-compuesta", guide_page(
    slug="regla-de-tres-simple-y-compuesta", name="Regla de tres simple y compuesta",
    page_title="Regla de Tres Simple y Compuesta: Directa e Inversa con Ejemplos | Calculadora Científica",
    desc="Cómo resolver la regla de tres simple directa, simple inversa y compuesta, cómo saber cuál usar y ejemplos resueltos paso a paso.",
    og_desc="Directa, inversa y compuesta: cómo distinguirlas y resolverlas con ejemplos.",
    headline="Regla de tres simple y compuesta: cómo resolverla con ejemplos",
    intro="La regla de tres resuelve casi cualquier problema de proporciones: recetas, precios, velocidades, obreros y días. Lo difícil no es la cuenta, sino decidir si la relación es directa o inversa. Esta guía te da el método.",
    quick="Directa: x = (B × C) / A. Inversa: x = (A × B) / C. Para saber cuál usar, duplicá un dato: si el resultado también se duplica, es directa; si se reduce a la mitad, es inversa.",
    cta=("/calculadoras/matematicas-avanzadas/regla-de-tres/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cómo se resuelve una regla de tres simple?", "Directa: x = (B × C) / A. Inversa: x = (A × B) / C, donde A corresponde a B y C corresponde a x."),
          ("¿Cómo se sabe si es directa o inversa?", "Si al aumentar una magnitud la otra aumenta en la misma proporción, es directa; si disminuye, es inversa."),
          ("¿Cómo se resuelve una regla de tres compuesta?", "Se parte del resultado conocido y se multiplica por el cociente de cada dato que cambia, invertido cuando la relación es inversa."),
          ("¿Se puede usar la regla de tres con porcentajes?", "Sí: el 100% corresponde al total y el porcentaje buscado al valor que querés hallar, lo que resuelve cuánto es el X% de un número.")],
    related=[("/calculadoras/matematicas-avanzadas/regla-de-tres/", "Calculadora de Regla de Tres"),
             ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes"),
             ("/guias/como-calcular-porcentajes/", "Guía: cómo calcular porcentajes")],
))

# ============================================================ MCD y MCM
body = "\n\n".join([
    h2("1. Qué son el MCD y el MCM"),
    ul([
        "<strong class=\"text-[var(--color-text)]\">MCD (máximo común divisor):</strong> el mayor número que divide a todos los números dados. MCD(12, 18) = 6.",
        "<strong class=\"text-[var(--color-text)]\">MCM (mínimo común múltiplo):</strong> el menor número positivo que es múltiplo de todos. MCM(12, 18) = 36.",
    ]),
    h2("2. Método 1: factores primos"),
    p("Se descompone cada número en factores primos. Ejemplo con 360 y 84:"),
    steps(["360 = 2³ × 3² × 5", "84 = 2² × 3 × 7"]),
    p("<strong class=\"text-[var(--color-text)]\">MCD</strong>: factores comunes con el <em>menor</em> exponente → 2² × 3 = <strong class=\"text-[var(--color-text)]\">12</strong>."),
    p("<strong class=\"text-[var(--color-text)]\">MCM</strong>: todos los factores con el <em>mayor</em> exponente → 2³ × 3² × 5 × 7 = <strong class=\"text-[var(--color-text)]\">2.520</strong>."),
    h2("3. Método 2: algoritmo de Euclides (para el MCD)"),
    p("Se divide el mayor por el menor y se repite con el divisor y el resto, hasta que el resto sea 0. El último resto distinto de 0 es el MCD. Es el método más rápido con números grandes."),
    steps(["360 = 84 × 4 + 24", "84 = 24 × 3 + 12", "24 = 12 × 2 + 0  →  MCD = 12"]),
    h2("4. Atajo: del MCD al MCM"),
    formula("MCD(a, b) × MCM(a, b) = a × b"),
    p("Con el MCD ya calculado, el MCM de dos números sale de la fórmula: MCM(360, 84) = 360 × 84 / 12 = 30.240 / 12 = 2.520. Con tres o más números, el atajo no se aplica directo: se calcula de a pares o con factores primos."),
    h3("Ejemplo con tres números: 48, 180 y 24"),
    steps(["48 = 2⁴ × 3", "180 = 2² × 3² × 5", "24 = 2³ × 3", "MCD = 2² × 3 = 12", "MCM = 2⁴ × 3² × 5 = 720"]),
    h2("5. Para qué sirven"),
    ul([
        "<strong class=\"text-[var(--color-text)]\">Simplificar fracciones</strong> (MCD): 180/48 → se divide arriba y abajo por 12 → 15/4.",
        "<strong class=\"text-[var(--color-text)]\">Sumar fracciones</strong> (MCM): 1/12 + 1/18 → denominador común 36 → 3/36 + 2/36 = 5/36.",
        "<strong class=\"text-[var(--color-text)]\">Problemas de coincidencia</strong> (MCM): si un colectivo pasa cada 12 minutos y otro cada 18, vuelven a coincidir cada 36 minutos.",
        "<strong class=\"text-[var(--color-text)]\">Repartir en grupos iguales</strong> (MCD): 48 chicos y 180 libros se pueden repartir en 12 grupos iguales, cada uno con 4 chicos y 15 libros.",
    ]),
    h2("6. Errores comunes"),
    ul([
        "Confundir MCD con MCM: el MCD nunca es mayor que el menor de los números, y el MCM nunca es menor que el mayor.",
        "Tomar el exponente mayor para el MCD o el menor para el MCM (es al revés).",
        "Olvidar los factores que no son comunes al calcular el MCM.",
    ]),
])
write("como-calcular-mcd-y-mcm", guide_page(
    slug="como-calcular-mcd-y-mcm", name="Cómo calcular el MCD y el MCM",
    page_title="Cómo Calcular el MCD y el MCM: Factores Primos y Euclides | Calculadora Científica",
    desc="Cómo calcular el máximo común divisor y el mínimo común múltiplo con factores primos y con el algoritmo de Euclides, con ejemplos resueltos y sus usos con fracciones.",
    og_desc="MCD y MCM con factores primos y Euclides, ejemplos resueltos y para qué sirven.",
    headline="Cómo calcular el MCD y el MCM con ejemplos",
    intro="El máximo común divisor y el mínimo común múltiplo aparecen cada vez que simplificás o sumás fracciones y en los problemas de coincidencia. Hay tres formas de calcularlos; esta guía las compara con el mismo ejemplo.",
    quick="MCD: factores primos comunes con el menor exponente. MCM: todos los factores primos con el mayor exponente. Atajo para dos números: MCM = (a × b) / MCD.",
    cta=("/calculadoras/matematicas-avanzadas/mcd-y-mcm/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cómo se calcula el MCD?", "Con factores primos (los comunes con el menor exponente) o con el algoritmo de Euclides: se divide el mayor por el menor y se repite con el resto hasta llegar a 0; el último resto distinto de 0 es el MCD."),
          ("¿Cómo se calcula el MCM?", "Con factores primos (todos, con el mayor exponente) o como (a × b) / MCD para dos números."),
          ("¿Para qué sirve el MCD?", "Para simplificar fracciones y repartir cosas en la mayor cantidad posible de grupos iguales."),
          ("¿Para qué sirve el MCM?", "Para sumar y restar fracciones con distinto denominador y para resolver problemas de coincidencia de eventos periódicos.")],
    related=[("/calculadoras/matematicas-avanzadas/mcd-y-mcm/", "Calculadora de MCD y MCM"),
             ("/calculadoras/matematicas-avanzadas/regla-de-tres/", "Calculadora de Regla de Tres"),
             ("/calculadoras/matematicas-avanzadas/calculadora-basica/", "Calculadora Básica")],
))
