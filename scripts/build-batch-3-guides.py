"""
build-batch-3-guides.py — Genera las 5 guías del lote 3: fracciones, Pitágoras, aguinaldo,
gases ideales y bases numéricas. Generación de una sola vez; después el HTML es la fuente de verdad.
"""
from pathlib import Path

from page_templates import guide_page

ROOT = Path(__file__).resolve().parent.parent
M = "text-[var(--color-text-muted)]"
S = '<strong class="text-[var(--color-text)]">'


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


# ======================================================== fracciones
body = "\n\n".join([
    h2("1. Qué es una fracción"),
    p("Una fracción a/b expresa a partes de un entero dividido en b partes iguales. El número de arriba es el " + S + "numerador</strong> (cuántas partes tomás) y el de abajo el " + S + "denominador</strong> (en cuántas partes se divide el entero). El denominador nunca puede ser 0."),
    h2("2. Simplificar una fracción"),
    p("Se divide numerador y denominador por su máximo común divisor (MCD). La fracción queda irreducible cuando el MCD es 1."),
    steps(["12/18: MCD(12, 18) = 6", "12 ÷ 6 = 2 y 18 ÷ 6 = 3", "12/18 = 2/3"]),
    h2("3. Sumar y restar"),
    h3("Con el mismo denominador"),
    p("Se suman o restan los numeradores y el denominador queda igual: 3/8 + 2/8 = 5/8."),
    h3("Con distinto denominador"),
    p("Primero hay que buscar un denominador común. Lo más cómodo es usar el MCM de los denominadores."),
    steps(["1/2 + 1/3: MCM(2, 3) = 6", "1/2 = 3/6 y 1/3 = 2/6", "3/6 + 2/6 = 5/6"]),
    p("Con restas es igual: 3/4 − 5/6 → MCM(4, 6) = 12 → 9/12 − 10/12 = " + S + "−1/12</strong>."),
    h2("4. Multiplicar"),
    p("Se multiplican numeradores y denominadores, y después se simplifica. No hace falta denominador común."),
    steps(["2/3 × 9/4 = (2 × 9) / (3 × 4) = 18/12", "MCD(18, 12) = 6", "18/12 = 3/2"]),
    p("Truco: se puede simplificar antes de multiplicar (en forma cruzada). En 2/3 × 9/4, el 3 y el 9 se simplifican por 3, y el 2 y el 4 por 2: queda 1/1 × 3/2 = 3/2."),
    h2("5. Dividir"),
    p("Dividir por una fracción es multiplicar por su inversa (se da vuelta numerador y denominador)."),
    steps(["1/2 ÷ 3/4 = 1/2 × 4/3", "= 4/6", "= 2/3"]),
    h2("6. Números mixtos"),
    p("Un número mixto como 2 1/3 es un entero más una fracción. Para operar conviene pasarlo a fracción impropia: entero × denominador + numerador, sobre el mismo denominador."),
    steps(["2 1/3 = (2 × 3 + 1)/3 = 7/3", "1 3/4 = (1 × 4 + 3)/4 = 7/4", "7/3 + 7/4 = 28/12 + 21/12 = 49/12", "49/12 = 4 1/12  (49 ÷ 12 = 4, resto 1)"]),
    h2("7. Pasar de fracción a decimal"),
    p("Se divide el numerador por el denominador: 7/8 = 0,875. Si el denominador simplificado tiene solo factores 2 y 5, el decimal es exacto (como 3/4 = 0,75); si no, es periódico (como 1/3 = 0,333…)."),
    h2("8. Errores comunes"),
    ul([
        "Sumar numeradores y denominadores entre sí: 1/2 + 1/3 " + S + "no</strong> es 2/5.",
        "Buscar denominador común al multiplicar o dividir (no hace falta).",
        "Olvidar dar vuelta la segunda fracción al dividir.",
        "No simplificar el resultado final.",
    ]),
])
write("como-operar-con-fracciones", guide_page(
    slug="como-operar-con-fracciones", name="Cómo operar con fracciones",
    page_title="Cómo Operar con Fracciones: Suma, Resta, Multiplicación y División | Calculadora Científica",
    desc="Aprendé a sumar, restar, multiplicar, dividir y simplificar fracciones paso a paso, con números mixtos, ejemplos resueltos y los errores más comunes.",
    og_desc="Suma, resta, multiplicación, división y simplificación de fracciones con ejemplos resueltos.",
    headline="Cómo operar con fracciones: suma, resta, multiplicación y división",
    intro="Las fracciones aparecen en recetas, medidas, probabilidades y en toda la matemática posterior. Las cuatro operaciones tienen una regla sencilla cada una: esta guía las resuelve con ejemplos y te muestra los errores más frecuentes.",
    quick="Sumar o restar: denominador común y se operan los numeradores. Multiplicar: arriba por arriba y abajo por abajo. Dividir: multiplicar por la inversa. Siempre simplificar al final.",
    cta=("/calculadoras/matematicas-avanzadas/calculadora-de-fracciones/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cómo se suman fracciones con distinto denominador?", "Se pasan a un denominador común (por ejemplo el MCM) y se suman los numeradores: 1/2 + 1/3 = 3/6 + 2/6 = 5/6."),
          ("¿Cómo se dividen fracciones?", "Se multiplica la primera por la inversa de la segunda: 1/2 ÷ 3/4 = 1/2 × 4/3 = 2/3."),
          ("¿Cómo se simplifica una fracción?", "Se dividen numerador y denominador por su MCD. 12/18 = 2/3 porque MCD(12, 18) = 6."),
          ("¿Cómo se pasa un número mixto a fracción?", "Se multiplica el entero por el denominador y se suma el numerador: 2 1/3 = (2 × 3 + 1)/3 = 7/3.")],
    related=[("/calculadoras/matematicas-avanzadas/calculadora-de-fracciones/", "Calculadora de Fracciones"),
             ("/calculadoras/matematicas-avanzadas/mcd-y-mcm/", "Calculadora de MCD y MCM"),
             ("/guias/como-calcular-mcd-y-mcm/", "Guía: cómo calcular el MCD y el MCM")],
))

# ======================================================== Pitágoras
body = "\n\n".join([
    h2("1. El enunciado"),
    p("En un triángulo rectángulo (el que tiene un ángulo de 90°), el cuadrado de la " + S + "hipotenusa</strong> es igual a la suma de los cuadrados de los " + S + "catetos</strong>. La hipotenusa es el lado opuesto al ángulo recto y siempre es el más largo."),
    formula("a² + b² = c²"),
    h2("2. Calcular la hipotenusa"),
    p("Si conocés los dos catetos, sumás sus cuadrados y sacás la raíz:"),
    formula("c = √(a² + b²)"),
    steps(["Catetos: a = 6 y b = 8", "c² = 6² + 8² = 36 + 64 = 100", "c = √100 = 10"]),
    h2("3. Calcular un cateto"),
    p("Si conocés la hipotenusa y un cateto, el otro sale por resta:"),
    formula("a = √(c² − b²)"),
    steps(["Hipotenusa c = 13 y cateto b = 5", "a² = 13² − 5² = 169 − 25 = 144", "a = √144 = 12"]),
    p("Si al restar el resultado es negativo, los datos no forman un triángulo rectángulo: la hipotenusa tiene que ser mayor que el cateto."),
    h2("4. Ternas pitagóricas"),
    p("Son ternas de números enteros que cumplen el teorema. Conviene reconocerlas para resolver rápido:"),
    table(["Catetos", "Hipotenusa", "Comprobación"], [
        ["3 y 4", "5", "9 + 16 = 25"],
        ["5 y 12", "13", "25 + 144 = 169"],
        ["8 y 15", "17", "64 + 225 = 289"],
        ["7 y 24", "25", "49 + 576 = 625"],
    ]),
    p("Cualquier múltiplo de una terna también lo es: 6-8-10, 9-12-15, 30-40-50. Los albañiles usan la 3-4-5 (o 30-40-50 cm) para marcar un ángulo recto en una obra."),
    h2("5. Un ejemplo de la vida real"),
    p("Una escalera de 5 m se apoya contra una pared con el pie a 1,4 m de la base. ¿A qué altura llega?"),
    steps(["La escalera es la hipotenusa: c = 5 m. La distancia al pie es un cateto: b = 1,4 m.", "a² = 5² − 1,4² = 25 − 1,96 = 23,04", "a = √23,04 = 4,8 m"]),
    h2("6. Otros datos del triángulo rectángulo"),
    ul([
        S + "Área</strong> = a × b / 2 (los catetos son base y altura).",
        S + "Perímetro</strong> = a + b + c.",
        S + "Altura sobre la hipotenusa</strong> = a × b / c.",
        S + "Ángulos agudos:</strong> el opuesto al cateto a mide arctan(a/b), y el otro es su complemento hasta 90°.",
    ]),
    h2("7. Errores comunes"),
    ul([
        "Usar el teorema en un triángulo que no es rectángulo.",
        "Sumar los lados sin elevarlos al cuadrado: 3 + 4 no es 5 en el teorema, lo que vale es 3² + 4² = 5².",
        "Restar al revés al despejar un cateto (siempre se resta del cuadrado de la hipotenusa).",
    ]),
])
write("teorema-de-pitagoras-explicado", guide_page(
    slug="teorema-de-pitagoras-explicado", name="El teorema de Pitágoras explicado",
    page_title="Teorema de Pitágoras Explicado: Fórmula, Ejemplos y Ternas | Calculadora Científica",
    desc="Qué dice el teorema de Pitágoras, cómo calcular la hipotenusa y los catetos paso a paso, ternas pitagóricas y un ejemplo de la vida real, con errores comunes.",
    og_desc="La fórmula del teorema de Pitágoras con ejemplos resueltos, ternas y aplicaciones.",
    headline="El teorema de Pitágoras explicado paso a paso",
    intro="Es uno de los resultados más usados de la geometría: sirve para medir distancias, comprobar ángulos rectos y resolver problemas de construcción. Esta guía te muestra la fórmula, cómo despejar cada lado y cómo reconocerlo en un problema.",
    quick="a² + b² = c², con c la hipotenusa. Hipotenusa: c = √(a² + b²). Cateto: a = √(c² − b²). Solo vale en triángulos rectángulos.",
    cta=("/calculadoras/matematicas-avanzadas/teorema-de-pitagoras/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cuál es la fórmula del teorema de Pitágoras?", "a² + b² = c², donde a y b son los catetos y c la hipotenusa del triángulo rectángulo."),
          ("¿Cómo se calcula un cateto?", "Se resta: a = √(c² − b²). Con hipotenusa 13 y cateto 5, el otro cateto es √(169 − 25) = 12."),
          ("¿Qué es una terna pitagórica?", "Tres números enteros que cumplen a² + b² = c², como 3-4-5 o 5-12-13."),
          ("¿El teorema sirve para cualquier triángulo?", "No, solo para triángulos rectángulos. Para otros se usan los teoremas del seno y del coseno.")],
    related=[("/calculadoras/matematicas-avanzadas/teorema-de-pitagoras/", "Calculadora del Teorema de Pitágoras"),
             ("/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/", "Calculadora Científica Online"),
             ("/guias/grados-y-radianes/", "Guía: grados y radianes")],
))

# ======================================================== aguinaldo
body = "\n\n".join([
    h2("1. Qué es el aguinaldo"),
    p("El aguinaldo o Sueldo Anual Complementario (SAC) es un pago que reciben los trabajadores en relación de dependencia en Argentina dos veces por año. Corresponde a un semestre de trabajo: de enero a junio (primera cuota) y de julio a diciembre (segunda cuota)."),
    h2("2. La fórmula"),
    formula("SAC = 50 % de la mejor remuneración mensual del semestre"),
    p("Se toma la " + S + "mejor</strong> remuneración mensual, normal y habitual, devengada en el semestre: no el promedio ni, necesariamente, el último sueldo. Si en abril cobraste más que en junio, vale la de abril."),
    steps(["Mejor sueldo del semestre: $1.000.000", "SAC = 1.000.000 × 50% = $500.000 (bruto)"]),
    h2("3. Si no trabajaste todo el semestre"),
    p("El aguinaldo se paga proporcional al tiempo trabajado. Por meses, equivale a 1/12 del mejor sueldo por cada mes:"),
    formula("SAC proporcional = (mejor sueldo ÷ 2) × meses trabajados ÷ 6"),
    steps(["Mejor sueldo: $1.200.000; trabajaste 3 meses", "(1.200.000 ÷ 2) × 3 ÷ 6 = 600.000 × 0,5 = $300.000"]),
    p("Por días se usa un semestre de 180 días: (mejor sueldo ÷ 2) × días trabajados ÷ 180. Con un mejor sueldo de $900.000 y 45 días: 450.000 × 45 ÷ 180 = $112.500."),
    h2("4. Cuánto se descuenta"),
    p("Sobre el aguinaldo se aplican los mismos aportes que sobre el sueldo: jubilación (11 %), ley 19.032 (3 %) y obra social (3 %), que suman un 17 %. Si te corresponde, también se descuenta el impuesto a las ganancias."),
    steps(["SAC bruto: $500.000", "Descuentos 17 %: $85.000", "Neto estimado: $415.000"]),
    h2("5. Cuándo se cobra"),
    p("La ley fija como fechas de pago el 30 de junio y el 18 de diciembre, con hasta 4 días hábiles de plazo para depositarlo."),
    h2("6. Qué entra en la mejor remuneración"),
    ul([
        "El sueldo básico y los adicionales habituales (antigüedad, presentismo, comisiones habituales, horas extra regulares).",
        "No suelen entrar los conceptos extraordinarios o no habituales. Si tenés dudas, mirá tu convenio colectivo o preguntale a tu empleador o sindicato.",
    ]),
    h2("7. Errores comunes"),
    ul([
        "Calcularlo sobre el promedio de los seis meses en vez de sobre el mejor sueldo.",
        "Olvidar los descuentos y creer que el aguinaldo bruto es lo que se cobra.",
        "No proporcionar cuando se ingresó o se salió a mitad de semestre.",
    ]),
    p("Esta guía y la calculadora son una referencia general. Cada convenio puede tener particularidades: ante cualquier diferencia, valen tu recibo de sueldo y la ley vigente."),
])
write("como-calcular-el-aguinaldo", guide_page(
    slug="como-calcular-el-aguinaldo", name="Cómo calcular el aguinaldo",
    page_title="Cómo Calcular el Aguinaldo (SAC) en Argentina: Fórmula y Ejemplos | Calculadora Científica",
    desc="Cómo se calcula el aguinaldo en Argentina: el 50% de la mejor remuneración del semestre, cálculo proporcional, descuentos y fechas de pago, con ejemplos resueltos.",
    og_desc="Aguinaldo (SAC): fórmula, proporcional, descuentos y fechas de pago con ejemplos.",
    headline="Cómo calcular el aguinaldo (SAC) en Argentina",
    intro="Dos veces por año llega el aguinaldo, pero no siempre es claro cuánto te corresponde. La cuenta es simple una vez que sabés cuál es el sueldo que se toma y cómo se proporciona. Acá está explicada con ejemplos.",
    quick="Aguinaldo = 50 % de la mejor remuneración mensual del semestre. Si no trabajaste todo el semestre, se proporciona (1/12 del mejor sueldo por mes trabajado). Se descuenta un 17 % de aportes.",
    cta=("/calculadoras/finanzas/calculadora-de-aguinaldo/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cómo se calcula el aguinaldo?", "Es el 50% de la mejor remuneración mensual del semestre. Con un mejor sueldo de $1.000.000, el aguinaldo bruto es $500.000."),
          ("¿Cómo se calcula el aguinaldo proporcional?", "Por cada mes trabajado corresponde 1/12 del mejor sueldo; por días, la mitad del mejor sueldo dividida por 180 y multiplicada por los días trabajados."),
          ("¿Cuándo se paga el aguinaldo?", "El 30 de junio y el 18 de diciembre, con hasta 4 días hábiles de plazo."),
          ("¿Cuánto se descuenta del aguinaldo?", "Los aportes del 17% (jubilación, ley 19.032 y obra social) y, si corresponde, ganancias.")],
    related=[("/calculadoras/finanzas/calculadora-de-aguinaldo/", "Calculadora de Aguinaldo"),
             ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes"),
             ("/guias/como-calcular-porcentajes/", "Guía: cómo calcular porcentajes")],
))

# ======================================================== gases ideales
body = "\n\n".join([
    h2("1. La ecuación"),
    formula("P · V = n · R · T"),
    ul([
        S + "P:</strong> presión del gas (atm, kPa, mmHg, bar…).",
        S + "V:</strong> volumen que ocupa (litros, m³…).",
        S + "n:</strong> cantidad de gas, en moles.",
        S + "R:</strong> constante de los gases ideales.",
        S + "T:</strong> temperatura absoluta, en kelvin.",
    ]),
    h2("2. Qué valor de R usar"),
    table(["Unidades de P y V", "R"], [
        ["atm y L", "0,082057 L·atm/(mol·K)"],
        ["Pa y m³ (SI)", "8,314 J/(mol·K)"],
        ["mmHg y L", "62,364 L·mmHg/(mol·K)"],
        ["kPa y L", "8,314 L·kPa/(mol·K)"],
    ]),
    p("Lo más importante es que las unidades de P y V coincidan con las de R. La calculadora convierte todo a atm y litros por vos."),
    h2("3. La temperatura siempre en kelvin"),
    formula("T (K) = T (°C) + 273,15"),
    p("Usar °C en la fórmula es el error más común. 25 °C son 298,15 K."),
    h2("4. Ejemplos resueltos"),
    h3("Volumen de un mol en condiciones normales"),
    steps(["n = 1 mol, T = 0 °C = 273,15 K, P = 1 atm", "V = nRT / P = 1 × 0,082057 × 273,15 / 1", "V = 22,414 L"]),
    h3("Presión de un gas encerrado"),
    steps(["2 mol en un recipiente de 10 L a 27 °C (300,15 K)", "P = nRT / V = 2 × 0,082057 × 300,15 / 10", "P = 4,93 atm"]),
    h3("Moles a partir de P, V y T"),
    steps(["10 L a 2 atm y 25 °C (298,15 K)", "n = PV / RT = (2 × 10) / (0,082057 × 298,15)", "n = 20 / 24,465 = 0,817 mol"]),
    h2("5. Las leyes particulares"),
    p("De PV = nRT salen las leyes clásicas cuando se mantienen constantes algunas magnitudes:"),
    ul([
        S + "Boyle</strong> (T y n constantes): P₁V₁ = P₂V₂.",
        S + "Charles</strong> (P y n constantes): V₁/T₁ = V₂/T₂.",
        S + "Gay-Lussac</strong> (V y n constantes): P₁/T₁ = P₂/T₂.",
        S + "Ley combinada</strong>: P₁V₁/T₁ = P₂V₂/T₂.",
    ]),
    h2("6. Equivalencias de presión"),
    p("1 atm = 101,325 kPa = 760 mmHg = 1,01325 bar. Si necesitás otras unidades, el conversor de unidades técnicas del sitio las pasa."),
    h2("7. Cuándo falla el modelo"),
    p("El gas ideal supone partículas sin volumen y sin atracción entre sí. A presiones muy altas o temperaturas muy bajas esas suposiciones dejan de valer y se usan modelos como el de Van der Waals."),
])
write("ley-de-los-gases-ideales", guide_page(
    slug="ley-de-los-gases-ideales", name="La ley de los gases ideales",
    page_title="Ley de los Gases Ideales (PV = nRT): Fórmula, R y Ejemplos | Calculadora Científica",
    desc="La ecuación de los gases ideales PV = nRT explicada: qué valor de R usar, por qué la temperatura va en kelvin, ejemplos resueltos y las leyes de Boyle, Charles y Gay-Lussac.",
    og_desc="PV = nRT explicada con ejemplos resueltos, la constante R y las leyes de los gases.",
    headline="La ley de los gases ideales: PV = nRT con ejemplos",
    intro="La ecuación de los gases ideales relaciona presión, volumen, cantidad de gas y temperatura en una sola fórmula. Con ella se resuelve casi cualquier problema de gases en química general. Acá se explica con ejemplos y los errores a evitar.",
    quick="PV = nRT. Con P en atm, V en litros y T en kelvin, R = 0,082057 L·atm/(mol·K). Un mol a 0 °C y 1 atm ocupa 22,414 L.",
    cta=("/calculadoras/quimica/calculadora-de-gases-ideales/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Qué significa PV = nRT?", "Que el producto de la presión por el volumen de un gas es proporcional a los moles y a la temperatura absoluta, con la constante R como factor."),
          ("¿Qué valor tiene R?", "0,082057 L·atm/(mol·K), o 8,314 J/(mol·K) en unidades del sistema internacional."),
          ("¿Por qué se usa kelvin?", "Porque la ecuación depende de la temperatura absoluta, que parte del cero absoluto. Se pasa de °C a K sumando 273,15."),
          ("¿Cuánto ocupa un mol de gas?", "22,414 L a 0 °C y 1 atm (condiciones normales de presión y temperatura).")],
    related=[("/calculadoras/quimica/calculadora-de-gases-ideales/", "Calculadora de Gases Ideales"),
             ("/calculadoras/quimica/calculadora-de-molaridad/", "Calculadora de Molaridad"),
             ("/guias/conversion-de-unidades-de-presion/", "Guía: conversión de unidades de presión")],
))

# ======================================================== bases numéricas
body = "\n\n".join([
    h2("1. Qué es una base"),
    p("Un sistema de numeración posicional usa una cantidad fija de símbolos, la " + S + "base</strong>. En decimal (base 10) se usan los dígitos 0 a 9; en binario (base 2), 0 y 1; en octal (base 8), 0 a 7; y en hexadecimal (base 16), 0 a 9 y las letras A a F. Cada posición vale una potencia de la base."),
    table(["Decimal", "Binario", "Octal", "Hexadecimal"], [
        ["0", "0000", "0", "0"], ["1", "0001", "1", "1"], ["2", "0010", "2", "2"], ["3", "0011", "3", "3"],
        ["4", "0100", "4", "4"], ["5", "0101", "5", "5"], ["6", "0110", "6", "6"], ["7", "0111", "7", "7"],
        ["8", "1000", "10", "8"], ["9", "1001", "11", "9"], ["10", "1010", "12", "A"], ["11", "1011", "13", "B"],
        ["12", "1100", "14", "C"], ["13", "1101", "15", "D"], ["14", "1110", "16", "E"], ["15", "1111", "17", "F"],
    ]),
    h2("2. De decimal a otra base: divisiones sucesivas"),
    p("Se divide el número por la base, se anota el resto y se repite con el cociente hasta llegar a 0. Los restos, leídos " + S + "de abajo hacia arriba</strong>, son el resultado."),
    steps(["13 ÷ 2 = 6, resto 1", "6 ÷ 2 = 3, resto 0", "3 ÷ 2 = 1, resto 1", "1 ÷ 2 = 0, resto 1", "Leyendo de abajo hacia arriba: 13 = 1101₂"]),
    p("Para hexadecimal se divide por 16. Ejemplo con 2024: 2024 ÷ 16 = 126 resto 8; 126 ÷ 16 = 7 resto 14 (E); 7 ÷ 16 = 0 resto 7 → 2024 = " + S + "7E8</strong>₁₆."),
    h2("3. De otra base a decimal: suma de potencias"),
    p("Cada dígito se multiplica por la base elevada a su posición (empezando en 0 por la derecha) y se suma."),
    steps(["1101₂ = 1·2³ + 1·2² + 0·2¹ + 1·2⁰ = 8 + 4 + 0 + 1 = 13", "7E8₁₆ = 7·16² + 14·16 + 8 = 1792 + 224 + 8 = 2024"]),
    h2("4. Binario ↔ hexadecimal y octal, sin pasar por decimal"),
    p("Como 16 = 2⁴, cada dígito hexadecimal equivale a 4 bits; como 8 = 2³, cada dígito octal equivale a 3 bits. Se agrupa y se traduce:"),
    steps(["11111101000₂ → se agrupa de a 4 desde la derecha: 0111 | 1110 | 1000", "0111 = 7, 1110 = E, 1000 = 8 → 7E8₁₆", "Agrupando de a 3: 011 | 111 | 101 | 000 → 3750₈"]),
    h2("5. El caso del 255"),
    p("255 en binario es 11111111 (ocho unos), en octal 377 y en hexadecimal FF. Es el mayor valor que entra en un byte, y por eso aparece en colores (#FF0000 es rojo puro) y en direcciones de red."),
    h2("6. Errores comunes"),
    ul([
        "Leer los restos de arriba hacia abajo en lugar de al revés.",
        "Empezar a contar las posiciones en 1 en vez de en 0.",
        "Usar un dígito que no existe en la base (un 2 en binario, un 8 en octal).",
        "Confundir las letras hexadecimales: A = 10, B = 11, C = 12, D = 13, E = 14, F = 15.",
    ]),
])
write("como-convertir-binario-decimal-y-hexadecimal", guide_page(
    slug="como-convertir-binario-decimal-y-hexadecimal", name="Cómo convertir entre binario, decimal y hexadecimal",
    page_title="Cómo Convertir Binario, Decimal y Hexadecimal: Métodos y Ejemplos | Calculadora Científica",
    desc="Cómo pasar números entre binario, decimal, octal y hexadecimal con divisiones sucesivas y suma de potencias, con tabla de equivalencias y ejemplos resueltos paso a paso.",
    og_desc="Conversión entre bases numéricas con ejemplos, tabla de equivalencias y los errores a evitar.",
    headline="Cómo convertir entre binario, decimal y hexadecimal",
    intro="Pasar un número de una base a otra se reduce a dos métodos: dividir sucesivamente por la base o sumar potencias. Con una tabla de 16 equivalencias y un truco para binario y hexadecimal, tenés todo lo necesario.",
    quick="Decimal → otra base: dividir por la base y leer los restos de abajo hacia arriba. Otra base → decimal: sumar cada dígito × base elevada a su posición. Binario ↔ hexadecimal: agrupar de a 4 bits.",
    cta=("/calculadoras/matematicas-avanzadas/conversor-de-bases-numericas/", "Abrir conversor"),
    body_html=body,
    faqs=[("¿Cómo se pasa de decimal a binario?", "Dividiendo por 2 hasta llegar a 0 y leyendo los restos de abajo hacia arriba: 13 = 1101."),
          ("¿Cómo se pasa de binario a decimal?", "Sumando cada bit multiplicado por 2 elevado a su posición: 1101₂ = 8 + 4 + 0 + 1 = 13."),
          ("¿Cómo se pasa de binario a hexadecimal?", "Agrupando los bits de a 4 desde la derecha y traduciendo cada grupo a un dígito hexadecimal."),
          ("¿Qué valores representan las letras A-F?", "A = 10, B = 11, C = 12, D = 13, E = 14 y F = 15.")],
    related=[("/calculadoras/matematicas-avanzadas/conversor-de-bases-numericas/", "Conversor de Bases Numéricas"),
             ("/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/", "Calculadora Científica Online"),
             ("/calculadoras/matematicas-avanzadas/mcd-y-mcm/", "Calculadora de MCD y MCM")],
))
