"""
build-batch-5-guides.py — Genera las 5 guías del lote 5 (Vida Diaria): edad y fechas, IMC,
equivalencias de cocina, horas trabajadas y propina. Generación de una sola vez.
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


# ============================================================ edad y fechas
body = "\n\n".join([
    h2("1. Cómo se calcula la edad"),
    p("La edad exacta se expresa en años, meses y días completos. El método es contar cuántos meses enteros pasaron desde el nacimiento y ver cuántos días sobran."),
    steps(["Nacimiento: 15/05/1990. Hoy: 10/11/2026.", "Años cumplidos: 2026 − 1990 = 36 (el 15/05/2026 ya pasó).", "Meses desde el último cumpleaños: del 15/05 al 15/10 → 5 meses.", "Días desde el 15/10 al 10/11 → 26 días.", "Edad: " + "36 años, 5 meses y 26 días."]),
    h2("2. Días entre dos fechas"),
    p("Se restan las fechas como días corridos. Del 1 de enero al 31 de diciembre de 2026 hay 364 días de diferencia (el año tiene 365: la cuenta no incluye el día de inicio). Si querés contar ambos extremos, sumá 1."),
    p("Para pasar a semanas, dividí por 7: 364 días son 52 semanas exactas. Para los " + S + "días hábiles</strong> se cuentan solo de lunes a viernes; los feriados hay que restarlos aparte porque cambian cada año."),
    h2("3. Sumar o restar tiempo a una fecha"),
    ul([
        S + "Días y semanas:</strong> la cuenta es exacta. 10/11/2026 + 90 días = 08/02/2027.",
        S + "Meses y años:</strong> se mantiene el día, salvo que el mes de llegada sea más corto: 31/01 + 1 mes = 28/02 (29/02 en año bisiesto).",
    ]),
    h2("4. Años bisiestos"),
    p("Un año es bisiesto si es divisible por 4, salvo que lo sea por 100 y no por 400. Entonces 2024 y 2000 son bisiestos, pero 1900 y 2100 no. Febrero tiene 29 días en esos años, lo que afecta cualquier cuenta que lo atraviese."),
    h3("El cumpleaños del 29 de febrero"),
    p("Quienes nacieron un 29 de febrero festejan el 28 de febrero (o el 1 de marzo, según la costumbre) en los años no bisiestos. Una calculadora tiene que elegir una de las dos; la nuestra usa el 28/02."),
    h2("5. Errores comunes"),
    ul([
        "Restar los años sin fijarse si ya pasó el cumpleaños de este año.",
        "Suponer que todos los meses tienen 30 días: la diferencia entre meses se arma con el calendario real.",
        "Olvidar que sumar un mes a un día 29, 30 o 31 puede caer en un mes más corto.",
        "Contar los días hábiles sin restar los feriados del período.",
    ]),
])
write("como-calcular-la-edad-y-los-dias-entre-fechas", guide_page(
    slug="como-calcular-la-edad-y-los-dias-entre-fechas", name="Cómo calcular la edad y los días entre fechas",
    page_title="Cómo Calcular la Edad y los Días entre Dos Fechas: Método y Ejemplos | Calculadora Científica",
    desc="Cómo calcular la edad exacta en años, meses y días, los días entre dos fechas y qué fecha será dentro de X tiempo, con años bisiestos, días hábiles y ejemplos resueltos.",
    og_desc="Edad exacta, días entre fechas, años bisiestos y suma de tiempo, con ejemplos.",
    headline="Cómo calcular la edad y los días entre dos fechas",
    intro="Parece sencillo hasta que aparecen los meses de distinto largo y los años bisiestos. Esta guía explica el método para calcular una edad exacta, la diferencia entre dos fechas y la fecha que resulta de sumar tiempo.",
    quick="Edad: años y meses completos desde el nacimiento más los días que sobran. Días entre fechas: se restan como días corridos. Al sumar meses, si el mes de llegada es más corto, se recorta al último día (31/01 + 1 mes = 28/02).",
    cta=("/calculadoras/vida-diaria/calculadora-de-edad-y-fechas/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cómo se calcula la edad exacta?", "Se cuentan los años y meses completos desde el nacimiento y se suman los días restantes. De 15/05/1990 al 10/11/2026: 36 años, 5 meses y 26 días."),
          ("¿Cuántos días hay entre dos fechas?", "Se restan las fechas. Del 1 de enero al 31 de diciembre de 2026 hay 364 días de diferencia."),
          ("¿Qué es un año bisiesto?", "El divisible por 4, salvo los divisibles por 100 que no lo sean por 400. Tiene 366 días."),
          ("¿Qué fecha será dentro de 90 días?", "Sumás 90 días a la fecha de partida. Desde el 10/11/2026 es el 08/02/2027.")],
    related=[("/calculadoras/vida-diaria/calculadora-de-edad-y-fechas/", "Calculadora de Edad y Fechas"),
             ("/calculadoras/vida-diaria/calculadora-de-horas-trabajadas/", "Calculadora de Horas Trabajadas"),
             ("/calculadoras/finanzas/calculadora-de-interes-simple/", "Interés Simple")],
))

# ============================================================ IMC
body = "\n\n".join([
    h2("1. Qué es el IMC"),
    p("El índice de masa corporal relaciona el peso con la altura. Se usa para clasificar de forma rápida el estado nutricional de adultos y orientar si el peso está dentro de un rango habitual."),
    formula("IMC = peso (kg) / altura (m)²"),
    steps(["Peso: 70 kg. Altura: 1,75 m.", "Altura al cuadrado: 1,75 × 1,75 = 3,0625", "IMC = 70 / 3,0625 = 22,9 → peso normal"]),
    p("Si tenés el peso en libras, multiplicá por 0,4536 para pasarlo a kilos; si la altura está en centímetros, dividila por 100."),
    h2("2. Categorías de la OMS"),
    table(["IMC", "Categoría"], [
        ["Menos de 18,5", "Bajo peso"],
        ["18,5 a 24,9", "Peso normal"],
        ["25 a 29,9", "Sobrepeso"],
        ["30 a 34,9", "Obesidad grado I"],
        ["35 a 39,9", "Obesidad grado II"],
        ["40 o más", "Obesidad grado III"],
    ]),
    h2("3. Tu rango de peso saludable"),
    p("Despejando el peso de la fórmula, el rango con IMC entre 18,5 y 24,9 es: " + S + "18,5 × altura² hasta 24,9 × altura²</strong>."),
    steps(["Altura 1,75 m → altura² = 3,0625", "Mínimo: 18,5 × 3,0625 = 56,7 kg", "Máximo: 24,9 × 3,0625 = 76,3 kg"]),
    h2("4. Limitaciones"),
    ul([
        "No distingue entre masa muscular y grasa: una persona muy musculosa puede tener un IMC alto sin exceso de grasa.",
        "No indica dónde se acumula la grasa (la abdominal es la que más riesgo conlleva).",
        "No se aplica a menores de 18 años (se usan curvas de percentiles), embarazadas ni a adultos mayores con las mismas categorías.",
        "Es un dato de orientación: no es un diagnóstico.",
    ]),
    p("Para una evaluación real, el profesional de la salud considera además la circunferencia de cintura, la composición corporal, los antecedentes y los estudios de laboratorio."),
])
write("como-calcular-el-imc", guide_page(
    slug="como-calcular-el-imc", name="Cómo calcular el IMC",
    page_title="Cómo Calcular el IMC (Índice de Masa Corporal): Fórmula y Tabla | Calculadora Científica",
    desc="Cómo se calcula el índice de masa corporal con la fórmula peso/altura², las categorías de la OMS, cómo obtener tu rango de peso saludable y las limitaciones del IMC.",
    og_desc="IMC: fórmula, categorías de la OMS, rango de peso saludable y limitaciones.",
    headline="Cómo calcular e interpretar el IMC",
    intro="El IMC es el indicador más usado para orientar si el peso es adecuado para la altura. Esta guía muestra la fórmula, la tabla de categorías de la OMS, cómo sacar tu rango saludable y por qué conviene no tomarlo como un diagnóstico.",
    quick="IMC = peso (kg) / altura (m)². Entre 18,5 y 24,9 se considera peso normal para un adulto. Con 70 kg y 1,75 m el IMC es 22,9.",
    cta=("/calculadoras/vida-diaria/calculadora-de-imc/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cómo se calcula el IMC?", "Dividiendo el peso en kilos por la altura en metros al cuadrado."),
          ("¿Qué IMC se considera normal?", "Entre 18,5 y 24,9 para adultos, según la OMS."),
          ("¿Cómo saco mi peso saludable?", "Multiplicando 18,5 y 24,9 por tu altura al cuadrado. Para 1,75 m: de 56,7 a 76,3 kg."),
          ("¿El IMC es un diagnóstico?", "No: es un indicador orientativo con límites importantes. Consultá siempre con un profesional de la salud.")],
    related=[("/calculadoras/vida-diaria/calculadora-de-imc/", "Calculadora de IMC"),
             ("/calculadoras/vida-diaria/conversor-de-cocina/", "Conversor de Cocina"),
             ("/guias/como-calcular-porcentajes/", "Guía: cómo calcular porcentajes")],
))

# ============================================================ cocina
body = "\n\n".join([
    h2("1. Medidas básicas de volumen"),
    table(["Medida", "Equivale a"], [
        ["1 cucharadita", "5 ml"],
        ["1 cucharada", "15 ml = 3 cucharaditas"],
        ["1 taza de medir", "240 ml = 16 cucharadas"],
        ["1 taza de té", "≈ 200 ml"],
        ["1 litro", "1.000 ml ≈ 4 tazas"],
    ]),
    p("En las recetas argentinas la taza suele ser de 250 ml; si una receta no aclara, conviene fijarse de qué tamaño es la que usa su autor."),
    h2("2. Cuántos gramos pesa una taza"),
    p("El peso de una taza depende del ingrediente (de su densidad). Valores aproximados para una taza de 240 ml:"),
    table(["Ingrediente", "Gramos por taza"], [
        ["Agua", "240 g"], ["Leche", "245 g"], ["Harina de trigo", "125 g"], ["Azúcar común", "200 g"],
        ["Azúcar impalpable", "120 g"], ["Manteca", "230 g"], ["Aceite", "220 g"], ["Miel", "340 g"],
        ["Arroz crudo", "185 g"], ["Avena arrollada", "90 g"], ["Cacao en polvo", "100 g"], ["Maicena", "130 g"],
        ["Sal fina", "290 g"], ["Dulce de leche", "310 g"], ["Pan rallado", "115 g"],
    ]),
    h2("3. Ejemplos"),
    steps(["200 g de azúcar → 1 taza de 240 ml (≈ 238 ml)", "2 cucharadas de manteca → 30 ml → ≈ 28 g", "1 taza de harina → 125 g (≈ 16 cucharadas)"]),
    h2("4. Por qué son aproximados"),
    ul([
        "La harina pesa distinto si está tamizada, suelta o apelmazada (de 115 a 140 g por taza).",
        "Las marcas tienen granulometría y humedad diferentes.",
        "Una medida \"al ras\" o \"colmada\" puede variar un 20 % o más.",
    ]),
    h2("5. Consejos para medir bien"),
    ul([
        "Para repostería, pesá en gramos con una balanza: es mucho más exacto.",
        "Usá medidores estándar y nivelá al ras con un cuchillo.",
        "Los líquidos se miden en una jarra graduada a la altura de los ojos.",
        "Las cucharas de café o de té de la vajilla no son medidas: usá cucharas dosificadoras.",
    ]),
])
write("equivalencias-de-cocina-tazas-cucharadas-y-gramos", guide_page(
    slug="equivalencias-de-cocina-tazas-cucharadas-y-gramos", name="Equivalencias de cocina",
    page_title="Equivalencias de Cocina: Tazas, Cucharadas y Gramos (Tabla) | Calculadora Científica",
    desc="Tabla de equivalencias de cocina: cuántos ml tiene una taza, una cucharada y una cucharadita, y cuántos gramos pesa una taza de harina, azúcar, manteca, arroz y más.",
    og_desc="Tabla de tazas, cucharadas y gramos para los ingredientes más usados.",
    headline="Equivalencias de cocina: tazas, cucharadas y gramos",
    intro="Muchas recetas usan tazas y cucharadas, otras gramos. Esta guía reúne las equivalencias que más se usan, incluida una tabla de cuántos gramos pesa una taza de cada ingrediente, y explica por qué son siempre aproximadas.",
    quick="1 cucharadita = 5 ml, 1 cucharada = 15 ml, 1 taza = 240 ml (16 cucharadas). Una taza de harina pesa ≈ 125 g; de azúcar, ≈ 200 g; de manteca, ≈ 230 g.",
    cta=("/calculadoras/vida-diaria/conversor-de-cocina/", "Abrir conversor"),
    body_html=body,
    faqs=[("¿Cuántos ml tiene una taza?", "240 ml la taza de medir; en muchas recetas argentinas se usan 250 ml o 200 ml (taza de té)."),
          ("¿Cuántos gramos tiene una taza de harina?", "Alrededor de 125 g."),
          ("¿Cuántas cucharadas tiene una taza?", "16 cucharadas, con una taza de 240 ml y cucharadas de 15 ml."),
          ("¿Cuántas cucharaditas tiene una cucharada?", "Tres.")],
    related=[("/calculadoras/vida-diaria/conversor-de-cocina/", "Conversor de Cocina"),
             ("/calculadoras/ingenieria/conversor-de-temperatura/", "Conversor de Temperatura"),
             ("/guias/conversion-de-temperatura-celsius-fahrenheit-kelvin/", "Guía: conversión de temperatura")],
))

# ============================================================ horas trabajadas
body = "\n\n".join([
    h2("1. Horas entre la entrada y la salida"),
    formula("horas trabajadas = (salida − entrada) − descanso"),
    steps(["Entrada 09:00, salida 18:00 → 9 horas", "Descanso de 60 minutos → 9:00 − 1:00 = 8 horas"]),
    h2("2. Turnos que cruzan la medianoche"),
    p("Si la salida es menor que la entrada, el turno termina al día siguiente: se suman 24 horas a la salida. De 22:00 a 06:00: (06:00 + 24:00) − 22:00 = 8 horas."),
    h2("3. De horas:minutos a decimal"),
    p("Para multiplicar por un valor de la hora hace falta el tiempo en decimal: se divide los minutos por 60."),
    table(["Horas:minutos", "Decimal"], [["8:15", "8,25"], ["8:30", "8,50"], ["8:45", "8,75"], ["7:10", "7,17"], ["7:20", "7,33"]]),
    h2("4. Horas extra"),
    p("Son las que exceden la jornada normal. En Argentina la jornada máxima es de 8 horas diarias y 48 semanales, y la ley prevé un recargo del " + S + "50 %</strong> sobre la hora normal en días comunes y del " + S + "100 %</strong> en sábados después de las 13, domingos y feriados. Verificá siempre tu convenio colectivo, que puede mejorar esos valores."),
    steps(["5 días de 10 horas, valor de la hora $1.000", "Horas normales: 5 × 8 = 40 h → 40 × 1.000 = $40.000", "Horas extra: 5 × 2 = 10 h → 10 × 1.000 × 1,5 = $15.000", "Total: $55.000"]),
    h2("5. Valor de la hora de un sueldo mensual"),
    p("Para mensualizados, un criterio habitual es dividir el sueldo por 200 (jornada de 48 horas semanales). Es una referencia: tu convenio puede fijar otro divisor."),
    h2("6. Errores comunes"),
    ul([
        "Multiplicar el valor de la hora por horas:minutos sin pasarlas a decimal (8:30 no es 8,30).",
        "Olvidar descontar el descanso no remunerado.",
        "No considerar que el turno cruza la medianoche.",
        "Aplicar el recargo del 50 % a horas que corresponden al 100 %.",
    ]),
])
write("como-calcular-horas-trabajadas-y-horas-extra", guide_page(
    slug="como-calcular-horas-trabajadas-y-horas-extra", name="Cómo calcular horas trabajadas y horas extra",
    page_title="Cómo Calcular las Horas Trabajadas y las Horas Extra | Calculadora Científica",
    desc="Cómo calcular las horas trabajadas entre entrada y salida (incluso turnos nocturnos), pasarlas a decimal y calcular las horas extra con recargo del 50% o 100%, con ejemplos.",
    og_desc="Horas trabajadas, turnos nocturnos, decimal y horas extra con recargo, con ejemplos.",
    headline="Cómo calcular horas trabajadas y horas extra",
    intro="Saber cuántas horas trabajaste y cuánto corresponde pagar por ellas exige tres cuentas: la diferencia entre la entrada y la salida, el pasaje a decimal y el recargo de las horas extra. Acá están con ejemplos.",
    quick="Horas = (salida − entrada) − descanso, sumando 24 h si el turno cruza la medianoche. Para pagar, pasá los minutos a decimal (÷ 60). Las horas extra llevan un recargo del 50 % o del 100 % según el día.",
    cta=("/calculadoras/vida-diaria/calculadora-de-horas-trabajadas/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cómo se calculan las horas trabajadas?", "Restando la entrada a la salida y descontando el descanso: de 09:00 a 18:00 con 60 min de descanso son 8 horas."),
          ("¿Cómo se pasa de horas y minutos a decimal?", "Dividiendo los minutos por 60: 8:45 son 8,75 horas."),
          ("¿Cuánto se paga la hora extra?", "El valor de la hora normal más un recargo: 50 % en días comunes y 100 % los sábados desde las 13, domingos y feriados."),
          ("¿Cómo calculo el valor de la hora de un sueldo mensual?", "Un criterio habitual es dividir el sueldo por 200; tu convenio puede indicar otro divisor.")],
    related=[("/calculadoras/vida-diaria/calculadora-de-horas-trabajadas/", "Calculadora de Horas Trabajadas"),
             ("/calculadoras/finanzas/calculadora-de-aguinaldo/", "Calculadora de Aguinaldo"),
             ("/guias/como-calcular-el-aguinaldo/", "Guía: cómo calcular el aguinaldo")],
))

# ============================================================ propina
body = "\n\n".join([
    h2("1. Calcular la propina"),
    formula("propina = cuenta × porcentaje / 100"),
    steps(["Cuenta: $25.000. Propina del 10 %", "25.000 × 10 / 100 = $2.500", "Total: 25.000 + 2.500 = $27.500"]),
    p("Atajo mental para el 10 %: movés la coma un lugar a la izquierda ($25.000 → $2.500). El 5 % es la mitad de eso; el 15 %, el 10 % más la mitad del 10 %."),
    h2("2. Cuánto dejar"),
    p("En Argentina la propina no es obligatoria: la costumbre es dejar alrededor del 10 % cuando el servicio fue bueno. No hay que confundirla con el " + S + "cubierto</strong>, un cargo del local por el servicio de mesa que ya viene incluido en la cuenta."),
    h2("3. Dividir la cuenta en partes iguales"),
    formula("por persona = (cuenta + propina) / personas"),
    steps(["Cuenta $10.000, propina 10 % = $1.000, total $11.000", "4 personas → 11.000 / 4 = $2.750 por persona"]),
    h2("4. Redondeo"),
    p("A veces la división da centavos: $11.000 entre 3 personas son $3.666,67. Redondeando hacia arriba al múltiplo de $100, cada uno paga $3.700 y se juntan $11.100: los $100 de diferencia se suman a la propina."),
    h2("5. Cuando cada uno consumió distinto"),
    p("Dividir en partes iguales es justo cuando los consumos son parecidos. Si no, lo más equitativo es que cada uno pague lo suyo y sume una parte proporcional de la propina: su consumo × (1 + porcentaje de propina)."),
    steps(["Ana consumió $6.000 y Beto $14.000, propina 10 %", "Ana: 6.000 × 1,10 = $6.600", "Beto: 14.000 × 1,10 = $15.400"]),
    h2("6. Errores comunes"),
    ul([
        "Calcular la propina sobre un total que ya incluye cubierto o propina sugerida.",
        "Olvidar sumar la propina antes de dividir.",
        "Redondear hacia abajo y quedarse corto con el total de la cuenta.",
    ]),
])
write("como-calcular-la-propina-y-dividir-la-cuenta", guide_page(
    slug="como-calcular-la-propina-y-dividir-la-cuenta", name="Cómo calcular la propina y dividir la cuenta",
    page_title="Cómo Calcular la Propina y Dividir la Cuenta entre Varios | Calculadora Científica",
    desc="Cómo calcular la propina (10%, 15%…), cuánto es habitual dejar en Argentina, cómo dividir la cuenta entre varias personas y cómo redondear, con ejemplos resueltos.",
    og_desc="Propina, división de la cuenta y redondeo con ejemplos.",
    headline="Cómo calcular la propina y dividir la cuenta",
    intro="Al final de una comida en grupo siempre aparece la cuenta: cuánto dejar de propina y cuánto paga cada uno. Acá está la cuenta paso a paso, con un atajo mental y la forma más justa de dividir cuando se consumió distinto.",
    quick="Propina = cuenta × % / 100. Por persona = (cuenta + propina) / personas. El 10 % se saca moviendo la coma un lugar a la izquierda.",
    cta=("/calculadoras/vida-diaria/calculadora-de-propina/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cómo se calcula la propina?", "Multiplicando la cuenta por el porcentaje y dividiendo por 100: el 10 % de $25.000 es $2.500."),
          ("¿Cuánto se deja de propina en Argentina?", "Alrededor del 10 % si el servicio fue bueno; no es obligatoria."),
          ("¿Cómo se divide la cuenta entre varias personas?", "Se suma la propina al total y se divide por la cantidad de personas."),
          ("¿Y si cada uno consumió distinto?", "Cada uno paga lo suyo más su parte proporcional de la propina.")],
    related=[("/calculadoras/vida-diaria/calculadora-de-propina/", "Calculadora de Propina y División de la Cuenta"),
             ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes"),
             ("/guias/como-calcular-porcentajes/", "Guía: cómo calcular porcentajes")],
))
