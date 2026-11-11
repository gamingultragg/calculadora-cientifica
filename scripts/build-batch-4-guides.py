"""
build-batch-4-guides.py — Genera las 6 guías del lote 4: moles, plazo fijo (TNA/TEA), áreas y
volúmenes, energía, regresión lineal y temperatura. Generación de una sola vez.
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


# ============================================================ moles
body = "\n\n".join([
    h2("1. Qué es un mol"),
    p("Un mol es la cantidad de sustancia que contiene 6,022 × 10²³ partículas (átomos, moléculas, iones…), el " + S + "número de Avogadro</strong>. Se usa para contar partículas pesándolas: la masa de un mol de una sustancia es su masa molar, en g/mol."),
    h2("2. Moles a partir de la masa"),
    formula("n = m / M"),
    p("n son los moles, m la masa en gramos y M la masa molar (la suma de las masas atómicas de la fórmula; si no la tenés, calculala primero)."),
    steps(["¿Cuántos moles son 49 g de H₂SO₄?", "M(H₂SO₄) = 2 × 1,008 + 32,06 + 4 × 16,00 = 98,08 g/mol", "n = 49 / 98,08 = 0,4996 mol"]),
    h2("3. Moles de soluto a partir de la molaridad"),
    p("La molaridad es la cantidad de moles de soluto por litro de solución. Despejando:"),
    formula("n = M × V (V en litros)"),
    steps(["¿Cuántos moles de soluto hay en 2 L de HCl 0,1 M?", "n = 0,1 mol/L × 2 L = 0,2 mol"]),
    p("Cuidado con las unidades: si el volumen está en mL, hay que dividirlo por 1000. En 250 mL de NaCl 0,5 M: n = 0,5 × 0,25 = 0,125 mol, que equivalen a 0,125 × 58,44 = 7,3 g de sal."),
    h2("4. Moles a partir del número de partículas"),
    formula("n = N / Nₐ"),
    steps(["3,01 × 10²³ moléculas de agua", "n = 3,01 × 10²³ / 6,022 × 10²³ = 0,5 mol"]),
    h2("5. Moles de un gas a partir de su volumen"),
    p("En condiciones normales (0 °C y 1 atm), un mol de gas ideal ocupa 22,414 L:"),
    steps(["44,8 L de un gas a 0 °C y 1 atm", "n = 44,8 / 22,414 = 2 mol"]),
    p("A otras presiones o temperaturas se usa la ecuación de los gases ideales: n = PV / RT."),
    h2("6. De moles a gramos y viceversa"),
    table(["Quiero…", "Fórmula", "Ejemplo"], [
        ["Moles desde gramos", "n = m / M", "49 g / 98,08 = 0,4996 mol"],
        ["Gramos desde moles", "m = n × M", "0,5 mol × 98,08 = 49,04 g"],
        ["Moles desde molaridad", "n = M × V", "0,1 M × 0,25 L = 0,025 mol"],
        ["Partículas desde moles", "N = n × Nₐ", "0,5 × 6,022 × 10²³ = 3,01 × 10²³"],
    ]),
    h2("7. Errores comunes"),
    ul([
        "Usar el volumen en mL sin pasarlo a litros al multiplicar por la molaridad.",
        "Confundir la masa molar de la molécula con la del átomo (O₂ pesa 32 g/mol, no 16).",
        "Usar el volumen del solvente en vez del volumen de la solución.",
        "Aplicar 22,414 L/mol cuando el gas no está a 0 °C y 1 atm.",
    ]),
])
write("como-calcular-moles", guide_page(
    slug="como-calcular-moles", name="Cómo calcular los moles",
    page_title="Cómo Calcular los Moles de Soluto y de Cualquier Sustancia: Fórmulas y Ejemplos | Calculadora Científica",
    desc="Cómo calcular los moles a partir de la masa, de la molaridad y el volumen (moles de soluto), del número de partículas o del volumen de un gas, con ejemplos resueltos paso a paso.",
    og_desc="Las cuatro formas de calcular moles, con ejemplos resueltos y errores comunes.",
    headline="Cómo calcular los moles de soluto y de cualquier sustancia",
    intro="Casi todos los problemas de química pasan por calcular moles. Según el dato que tengas (masa, molaridad y volumen, partículas o volumen de gas), cambia la fórmula. Esta guía las reúne con un ejemplo de cada una.",
    quick="Con la masa: n = m / M. Con la molaridad (moles de soluto): n = M × V, con V en litros. Con partículas: n = N / 6,022 × 10²³. Con un gas a 0 °C y 1 atm: n = V / 22,414.",
    cta=("/calculadoras/quimica/calculadora-de-moles/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cómo se calculan los moles de soluto?", "Multiplicando la molaridad por el volumen de la solución en litros (n = M × V), o dividiendo la masa de soluto por su masa molar (n = m / M)."),
          ("¿Cómo se calculan los moles a partir de los gramos?", "Dividiendo la masa por la masa molar: n = m / M. 49 g de H₂SO₄ son 49 / 98,08 = 0,4996 mol."),
          ("¿Cuántas partículas hay en un mol?", "6,022 × 10²³, el número de Avogadro."),
          ("¿Cuántos moles hay en 22,4 litros de gas?", "Un mol, si el gas está a 0 °C y 1 atm (condiciones normales).")],
    related=[("/calculadoras/quimica/calculadora-de-moles/", "Calculadora de Moles"),
             ("/calculadoras/quimica/calculadora-de-molaridad/", "Calculadora de Molaridad"),
             ("/guias/como-calcular-molaridad/", "Guía: cómo calcular la molaridad")],
))

# ============================================================ plazo fijo
body = "\n\n".join([
    h2("1. Cómo funciona un plazo fijo"),
    p("Depositás un capital en un banco por un plazo (por ejemplo, 30 días) y al vencimiento recibís el capital más un interés. El banco informa una " + S + "TNA</strong> (tasa nominal anual) y el interés de tu plazo se prorratea según los días."),
    h2("2. La fórmula del interés"),
    formula("Interés = Capital × TNA × días / 365"),
    p("Se usa el año de 365 días. Por ejemplo, $1.000.000 a 30 días con una TNA del 40 %:"),
    steps(["Interés = 1.000.000 × 0,40 × 30 / 365", "Interés = $32.876,71", "Monto final = $1.032.876,71"]),
    p("El rendimiento del período es 3,29 %: es la tasa mensual de ese plazo."),
    h2("3. TNA vs TEA"),
    p("La " + S + "TNA</strong> no incluye la reinversión de los intereses. La " + S + "TEA</strong> (tasa efectiva anual) muestra cuánto rendiría el capital en un año si, cada vez que vence el plazo, reinvertís capital e interés en otro plazo igual."),
    formula("TEA = (1 + TNA × d/365)^(365/d) − 1"),
    steps(["TNA = 40 %, plazos de 30 días", "TEA = (1 + 0,40 × 30/365)^(365/30) − 1", "TEA = 1,0329^12,17 − 1 = 48,23 %"]),
    p("Cuanto más corto es el plazo de reinversión, más alta es la TEA para una misma TNA. Con plazos de 90 días la TEA de una TNA del 40 % baja a 46,45 %."),
    h2("4. De TEA a TNA"),
    formula("TNA = ((1 + TEA)^(d/365) − 1) × 365/d"),
    p("Con una TEA del 50 % y plazos de 30 días: TNA = ((1,5)^(30/365) − 1) × 365/30 = 41,23 %. Sirve para comparar una oferta expresada en TEA con otra expresada en TNA."),
    h2("5. Cómo comparar con la inflación"),
    p("El interés de un plazo fijo es nominal. Para saber si ganaste poder de compra, compará el rendimiento del período con la inflación del mismo período: si el plazo rindió 3,29 % en un mes y la inflación fue de 2,5 %, el rendimiento real es positivo (aprox. 0,8 %); si fue de 4 %, es negativo."),
    h2("6. Errores comunes"),
    ul([
        "Dividir la TNA por 12 en lugar de prorratear por días (30/365 no es 1/12).",
        "Comparar una TNA con una TEA como si fueran lo mismo.",
        "Olvidar que el interés es bruto: no considera impuestos ni inflación.",
    ]),
])
write("como-calcular-un-plazo-fijo-tna-y-tea", guide_page(
    slug="como-calcular-un-plazo-fijo-tna-y-tea", name="Cómo calcular un plazo fijo: TNA y TEA",
    page_title="Cómo Calcular un Plazo Fijo: Fórmula, TNA y TEA con Ejemplos | Calculadora Científica",
    desc="Cómo calcular el interés de un plazo fijo con la TNA y los días, qué diferencia hay entre TNA y TEA y cómo convertirlas, con ejemplos resueltos y la comparación con la inflación.",
    og_desc="Interés de un plazo fijo, TNA vs TEA y cómo convertirlas, con ejemplos.",
    headline="Cómo calcular un plazo fijo: fórmula, TNA y TEA",
    intro="Antes de elegir dónde poner tu plata conviene saber cuánto vas a ganar y cómo comparar tasas que vienen expresadas distinto. Esta guía explica la cuenta del interés, la diferencia entre TNA y TEA y cómo pasar de una a otra.",
    quick="Interés = capital × TNA × días / 365. La TEA incluye la reinversión: TEA = (1 + TNA × d/365)^(365/d) − 1. Con una TNA del 40 % a 30 días, el rendimiento es 3,29 % y la TEA 48,23 %.",
    cta=("/calculadoras/finanzas/calculadora-de-plazo-fijo/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cómo se calcula el interés de un plazo fijo?", "Capital × TNA × días / 365. Con $1.000.000, TNA 40 % y 30 días: $32.876,71."),
          ("¿Qué diferencia hay entre TNA y TEA?", "La TNA no considera la reinversión de intereses; la TEA sí, por eso es mayor."),
          ("¿Cómo se pasa de TNA a TEA?", "TEA = (1 + TNA × d/365)^(365/d) − 1, con d los días del plazo."),
          ("¿Por qué se divide por 365?", "Es la convención de los bancos argentinos para prorratear una tasa anual por días.")],
    related=[("/calculadoras/finanzas/calculadora-de-plazo-fijo/", "Calculadora de Plazo Fijo y Tasas"),
             ("/calculadoras/finanzas/interes-compuesto/", "Interés Compuesto"),
             ("/guias/interes-simple-vs-compuesto/", "Guía: interés simple vs compuesto")],
))

# ============================================================ áreas y volúmenes
body = "\n\n".join([
    h2("1. Área, perímetro y volumen"),
    ul([
        S + "Perímetro:</strong> la longitud del contorno de una figura plana (cm, m).",
        S + "Área:</strong> la superficie que ocupa una figura plana (cm², m²).",
        S + "Volumen:</strong> el espacio que ocupa un cuerpo (cm³, m³, litros).",
    ]),
    h2("2. Fórmulas de figuras planas"),
    table(["Figura", "Área", "Perímetro"], [
        ["Cuadrado (lado l)", "l²", "4l"],
        ["Rectángulo (b, h)", "b · h", "2(b + h)"],
        ["Triángulo (b, h)", "b · h / 2", "a + b + c"],
        ["Círculo (r)", "π · r²", "2 · π · r"],
        ["Trapecio (B, b, h)", "(B + b) · h / 2", "suma de los lados"],
        ["Rombo (D, d)", "D · d / 2", "4 · lado"],
        ["Paralelogramo (b, h)", "b · h", "2(b + lado)"],
    ]),
    p("Cuando no conocés la altura de un triángulo pero sí sus tres lados, se usa la fórmula de Herón: con s = (a + b + c)/2, el área es √(s·(s−a)·(s−b)·(s−c)). Para 3, 4 y 5: s = 6 y área = √(6·3·2·1) = 6."),
    h2("3. Fórmulas de cuerpos"),
    table(["Cuerpo", "Volumen", "Superficie total"], [
        ["Cubo (arista a)", "a³", "6a²"],
        ["Prisma (a, b, c)", "a · b · c", "2(ab + bc + ac)"],
        ["Cilindro (r, h)", "π · r² · h", "2πr(r + h)"],
        ["Cono (r, h)", "π · r² · h / 3", "πr(r + g), con g = √(r² + h²)"],
        ["Esfera (r)", "4/3 · π · r³", "4πr²"],
        ["Pirámide cuadrada (a, h)", "a² · h / 3", "a² + 2a · apotema"],
    ]),
    h2("4. Ejemplos resueltos"),
    h3("Un terreno rectangular"),
    steps(["12 m de frente por 25 m de fondo", "Área = 12 × 25 = 300 m²", "Perímetro = 2 × (12 + 25) = 74 m de alambrado"]),
    h3("Una lata cilíndrica"),
    steps(["Radio 4 cm y altura 12 cm", "V = π × 4² × 12 = 603,19 cm³ (≈ 0,6 litros)"]),
    h3("Un cono"),
    steps(["Radio 3 y altura 4", "Generatriz g = √(3² + 4²) = 5", "V = π × 9 × 4 / 3 = 37,70", "Superficie lateral = π × 3 × 5 = 47,12"]),
    h2("5. Equivalencias útiles"),
    table(["Unidad", "Equivalencia"], [
        ["1 m²", "10.000 cm²"],
        ["1 m³", "1.000 litros"],
        ["1 litro", "1.000 cm³"],
        ["1 hectárea", "10.000 m²"],
    ]),
    h2("6. Errores comunes"),
    ul([
        "Mezclar unidades (metros con centímetros) en la misma cuenta.",
        "Olvidar que las áreas son cuadradas y los volúmenes cúbicos: al pasar de m² a cm² se multiplica por 10.000, no por 100.",
        "Usar el diámetro en lugar del radio en las fórmulas del círculo y la esfera.",
        "Confundir la altura del cono con la generatriz.",
    ]),
])
write("como-calcular-areas-y-volumenes", guide_page(
    slug="como-calcular-areas-y-volumenes", name="Cómo calcular áreas y volúmenes",
    page_title="Cómo Calcular Áreas y Volúmenes: Fórmulas de Figuras y Cuerpos | Calculadora Científica",
    desc="Todas las fórmulas de áreas, perímetros, volúmenes y superficies de figuras planas y cuerpos geométricos, con ejemplos resueltos, equivalencias de unidades y errores comunes.",
    og_desc="Fórmulas de áreas y volúmenes con ejemplos resueltos y equivalencias de unidades.",
    headline="Cómo calcular áreas y volúmenes: fórmulas y ejemplos",
    intro="Área, perímetro, volumen: tres medidas distintas que se confunden con facilidad. Acá están las fórmulas de las figuras más usadas, ejemplos con números y las equivalencias de unidades para no equivocarte.",
    quick="Área de un rectángulo: b·h; de un círculo: π·r²; de un triángulo: b·h/2. Volumen de un cilindro: π·r²·h; de una esfera: 4/3·π·r³; de un cono: π·r²·h/3.",
    cta=("/calculadoras/matematicas-avanzadas/calculadora-de-areas-y-volumenes/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cuál es la fórmula del área del círculo?", "A = π·r². Con radio 5: 78,54 unidades cuadradas."),
          ("¿Cómo se calcula el volumen de un cilindro?", "V = π·r²·h, el área de la base por la altura."),
          ("¿Cuántos litros hay en un metro cúbico?", "1.000 litros."),
          ("¿Qué diferencia hay entre área y perímetro?", "El perímetro mide el contorno (una longitud) y el área mide la superficie que encierra.")],
    related=[("/calculadoras/matematicas-avanzadas/calculadora-de-areas-y-volumenes/", "Calculadora de Áreas y Volúmenes"),
             ("/calculadoras/matematicas-avanzadas/teorema-de-pitagoras/", "Teorema de Pitágoras"),
             ("/guias/teorema-de-pitagoras-explicado/", "Guía: el teorema de Pitágoras")],
))

# ============================================================ energía
body = "\n\n".join([
    h2("1. Energía cinética"),
    p("Es la energía que tiene un cuerpo por estar en movimiento."),
    formula("Ec = ½ · m · v²"),
    steps(["Un auto de 1000 kg que va a 20 m/s (72 km/h)", "Ec = 0,5 × 1000 × 20² = 200.000 J = 200 kJ"]),
    p("Como la velocidad está al cuadrado, " + S + "duplicarla cuadruplica la energía</strong>: a 40 m/s (144 km/h) el mismo auto tiene 800.000 J. Por eso la distancia de frenado crece tanto con la velocidad."),
    h2("2. Energía potencial gravitatoria"),
    p("Es la energía almacenada por estar a cierta altura sobre un nivel de referencia."),
    formula("Ep = m · g · h"),
    steps(["Una persona de 70 kg a 10 m de altura", "Ep = 70 × 9,81 × 10 = 6.867 J"]),
    h2("3. Conservación de la energía mecánica"),
    p("Sin rozamiento, la suma de energía cinética y potencial se mantiene constante. Un objeto que cae transforma energía potencial en cinética. Con esto se calcula la velocidad de impacto sin usar el tiempo:"),
    formula("m · g · h = ½ · m · v²  →  v = √(2 · g · h)"),
    steps(["Un objeto cae desde 5 m", "v = √(2 × 9,81 × 5) = √98,1 = 9,90 m/s (≈ 35,7 km/h)"]),
    p("Fijate que la masa se simplifica: en el vacío, todos los cuerpos caen igual."),
    h2("4. Unidades y equivalencias"),
    table(["Unidad", "Equivalencia en joules"], [
        ["1 kJ", "1.000 J"],
        ["1 kcal", "4.184 J"],
        ["1 kWh", "3.600.000 J"],
        ["1 cal", "4,184 J"],
    ]),
    p("Los 200.000 J del auto equivalen a 47,8 kcal. La velocidad en km/h se pasa a m/s dividiendo por 3,6."),
    h2("5. Errores comunes"),
    ul([
        "Usar la velocidad en km/h sin pasarla a m/s: el resultado no sale en joules.",
        "Olvidar el cuadrado de la velocidad o el ½.",
        "Medir la altura desde un punto equivocado: la energía potencial depende del nivel de referencia que elijas.",
    ]),
])
write("energia-cinetica-y-potencial-explicada", guide_page(
    slug="energia-cinetica-y-potencial-explicada", name="Energía cinética y potencial explicadas",
    page_title="Energía Cinética y Potencial: Fórmulas, Diferencias y Ejemplos | Calculadora Científica",
    desc="Qué son la energía cinética (½mv²) y la potencial gravitatoria (mgh), cómo calcularlas, la conservación de la energía mecánica y ejemplos resueltos con unidades.",
    og_desc="Energía cinética y potencial: fórmulas, conservación de la energía y ejemplos.",
    headline="Energía cinética y potencial: fórmulas y ejemplos resueltos",
    intro="Las dos formas básicas de energía mecánica son la del movimiento y la de la altura. Con dos fórmulas cortas se resuelven desde problemas de colegio hasta el cálculo de la velocidad de caída de un objeto.",
    quick="Ec = ½·m·v² (movimiento) y Ep = m·g·h (altura), en joules con kg, m/s y m. Sin rozamiento, Ec + Ep se conserva: un objeto que cae desde h llega con v = √(2·g·h).",
    cta=("/calculadoras/fisica/energia-cinetica-y-potencial/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cuál es la fórmula de la energía cinética?", "Ec = ½·m·v², con la masa en kg y la velocidad en m/s; da joules."),
          ("¿Cuál es la fórmula de la energía potencial?", "Ep = m·g·h, con g = 9,81 m/s²."),
          ("¿Qué es la energía mecánica?", "La suma de la energía cinética y la potencial. Se conserva si no hay rozamiento."),
          ("¿Cómo se pasa de joules a kilocalorías?", "Dividiendo por 4.184: 200.000 J son 47,8 kcal.")],
    related=[("/calculadoras/fisica/energia-cinetica-y-potencial/", "Calculadora de Energía Cinética y Potencial"),
             ("/calculadoras/fisica/segunda-ley-de-newton/", "Segunda Ley de Newton"),
             ("/guias/formulas-de-mru-y-mrua/", "Guía: fórmulas de MRU y MRUA")],
))

# ============================================================ regresión lineal
body = "\n\n".join([
    h2("1. Qué hace la regresión lineal"),
    p("Dado un conjunto de pares (x, y), busca la recta y = a + b·x que mejor se ajusta a los puntos. Se usa para describir la relación entre dos variables y para hacer predicciones. \"Mejor\" significa que minimiza la suma de los cuadrados de los errores verticales (" + S + "mínimos cuadrados</strong>)."),
    h2("2. Las fórmulas"),
    formula("b = (n·Σxy − Σx·Σy) / (n·Σx² − (Σx)²)"),
    formula("a = ȳ − b · x̄"),
    p("b es la pendiente (cuánto cambia y por cada unidad de x) y a es la ordenada al origen (el valor de y cuando x = 0)."),
    h2("3. Ejemplo resuelto"),
    p("Datos: (1, 2), (2, 3), (3, 5), (4, 4), (5, 6)."),
    table(["x", "y", "x·y", "x²", "y²"], [
        ["1", "2", "2", "1", "4"], ["2", "3", "6", "4", "9"], ["3", "5", "15", "9", "25"],
        ["4", "4", "16", "16", "16"], ["5", "6", "30", "25", "36"], ["Σ = 15", "Σ = 20", "Σ = 69", "Σ = 55", "Σ = 90"],
    ]),
    steps([
        "b = (5 × 69 − 15 × 20) / (5 × 55 − 15²) = (345 − 300) / (275 − 225) = 45 / 50 = 0,9",
        "x̄ = 3 e ȳ = 4 → a = 4 − 0,9 × 3 = 1,3",
        "Recta: y = 1,3 + 0,9·x",
        "Predicción para x = 6: y = 1,3 + 0,9 × 6 = 6,7",
    ]),
    h2("4. Coeficiente de correlación r"),
    formula("r = (n·Σxy − Σx·Σy) / √[(n·Σx² − (Σx)²)(n·Σy² − (Σy)²)]"),
    p("Con los datos anteriores: r = 45 / √(50 × 50) = 0,9. Va de −1 a 1. Una guía orientativa para el valor absoluto: menos de 0,2 casi nula; de 0,2 a 0,4 débil; de 0,4 a 0,7 moderada; de 0,7 a 0,9 fuerte; más de 0,9 muy fuerte."),
    h2("5. R²: cuánto explica la recta"),
    p("R² = r² = 0,81: la recta explica el 81 % de la variación de y; el 19 % restante depende de otros factores o del azar."),
    h2("6. Errores comunes"),
    ul([
        "Extrapolar muy lejos del rango de datos.",
        "Interpretar correlación como causalidad.",
        "Ajustar una recta a datos que claramente siguen una curva: conviene mirar el gráfico antes.",
        "Dejarse engañar por un solo dato extremo (outlier), que puede cambiar mucho la pendiente.",
    ]),
])
write("regresion-lineal-y-correlacion", guide_page(
    slug="regresion-lineal-y-correlacion", name="Regresión lineal y correlación",
    page_title="Regresión Lineal y Correlación: Cómo Calcular la Recta, r y R² | Calculadora Científica",
    desc="Cómo calcular la recta de regresión por mínimos cuadrados, el coeficiente de correlación r y R², con un ejemplo resuelto paso a paso, interpretación y errores comunes.",
    og_desc="Recta de regresión, r y R² con ejemplo resuelto paso a paso.",
    headline="Regresión lineal y correlación: cómo calcularlas e interpretarlas",
    intro="La regresión lineal es una de las herramientas estadísticas más usadas: describe cuánto cambia una variable cuando cambia otra y permite predecir. Esta guía la resuelve a mano con un ejemplo y te enseña a leer r y R².",
    quick="Pendiente b = (n·Σxy − Σx·Σy) / (n·Σx² − (Σx)²); ordenada a = ȳ − b·x̄; recta y = a + b·x. r va de −1 a 1 y R² = r² es la proporción de variación explicada.",
    cta=("/calculadoras/estadistica/regresion-lineal/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cómo se calcula la recta de regresión?", "Con la pendiente b = (n·Σxy − Σx·Σy)/(n·Σx² − (Σx)²) y la ordenada a = ȳ − b·x̄."),
          ("¿Qué significa r = 0,9?", "Una correlación lineal positiva muy fuerte: cuando x aumenta, y tiende a aumentar casi en línea recta."),
          ("¿Qué indica R²?", "La proporción de la variación de y que explica la recta. R² = 0,81 es un 81 %."),
          ("¿Correlación es causalidad?", "No: que dos variables se muevan juntas no prueba que una cause la otra.")],
    related=[("/calculadoras/estadistica/regresion-lineal/", "Calculadora de Regresión Lineal"),
             ("/calculadoras/estadistica/calculadora-estadistica-descriptiva/", "Estadística Descriptiva"),
             ("/guias/como-calcular-desviacion-estandar/", "Guía: cómo calcular la desviación estándar")],
))

# ============================================================ temperatura
body = "\n\n".join([
    h2("1. Las cuatro escalas"),
    ul([
        S + "Celsius (°C):</strong> el agua se congela a 0 °C y hierve a 100 °C. La usa casi todo el mundo.",
        S + "Fahrenheit (°F):</strong> el agua se congela a 32 °F y hierve a 212 °F. La usan Estados Unidos y algunos países más.",
        S + "Kelvin (K):</strong> escala absoluta del sistema internacional; parte del cero absoluto.",
        S + "Rankine (°R):</strong> escala absoluta con grados del tamaño de los Fahrenheit.",
    ]),
    h2("2. Las fórmulas"),
    table(["De → A", "Fórmula"], [
        ["°C → °F", "°F = °C × 9/5 + 32"],
        ["°F → °C", "°C = (°F − 32) × 5/9"],
        ["°C → K", "K = °C + 273,15"],
        ["K → °C", "°C = K − 273,15"],
        ["°F → °R", "°R = °F + 459,67"],
    ]),
    h2("3. Ejemplos"),
    steps(["25 °C → °F: 25 × 9/5 + 32 = 77 °F", "98,6 °F → °C: (98,6 − 32) × 5/9 = 37 °C", "300 K → °C: 300 − 273,15 = 26,85 °C", "−40 °C → °F: −40 × 9/5 + 32 = −40 °F (único punto donde coinciden)"]),
    h2("4. Tabla de referencia"),
    table(["Situación", "°C", "°F", "K"], [
        ["Agua se congela", "0", "32", "273,15"],
        ["Día templado", "20", "68", "293,15"],
        ["Cuerpo humano", "37", "98,6", "310,15"],
        ["Agua hierve", "100", "212", "373,15"],
        ["Cero absoluto", "−273,15", "−459,67", "0"],
    ]),
    h2("5. Un truco para estimar de cabeza"),
    p("Para pasar de Celsius a Fahrenheit en forma aproximada, duplicá y sumá 30: 25 °C → 25 × 2 + 30 = 80 °F (el valor exacto es 77 °F). Para volver, restá 30 y dividí por 2. Sirve para temperaturas del clima, no para cálculos científicos."),
    h2("6. Errores comunes"),
    ul([
        "Olvidar restar 32 antes de multiplicar al pasar de Fahrenheit a Celsius.",
        "Usar °C en fórmulas de física que piden temperatura absoluta (como la ley de los gases ideales): hay que pasarla a kelvin.",
        "Escribir \"grados Kelvin\": el nombre correcto es kelvin, sin la palabra \"grados\".",
    ]),
])
write("conversion-de-temperatura-celsius-fahrenheit-kelvin", guide_page(
    slug="conversion-de-temperatura-celsius-fahrenheit-kelvin", name="Cómo convertir entre Celsius, Fahrenheit y Kelvin",
    page_title="Conversión de Temperatura: Celsius, Fahrenheit y Kelvin con Fórmulas | Calculadora Científica",
    desc="Fórmulas para convertir entre grados Celsius, Fahrenheit, Kelvin y Rankine, con ejemplos resueltos, tabla de referencia y un truco para estimar de cabeza.",
    og_desc="Fórmulas de conversión de temperatura con ejemplos y tabla de referencia.",
    headline="Cómo convertir entre Celsius, Fahrenheit y Kelvin",
    intro="Pasar de una escala de temperatura a otra es una cuenta de una línea, pero es fácil equivocarse con el orden de las operaciones. Acá están las fórmulas, ejemplos y una tabla de referencia para controlar tus resultados.",
    quick="°F = °C × 9/5 + 32; °C = (°F − 32) × 5/9; K = °C + 273,15. El agua hierve a 100 °C = 212 °F = 373,15 K.",
    cta=("/calculadoras/ingenieria/conversor-de-temperatura/", "Abrir conversor"),
    body_html=body,
    faqs=[("¿Cómo se pasa de Celsius a Fahrenheit?", "°F = °C × 9/5 + 32. 100 °C son 212 °F."),
          ("¿Cómo se pasa de Fahrenheit a Celsius?", "°C = (°F − 32) × 5/9. 98,6 °F son 37 °C."),
          ("¿Cómo se pasa de Celsius a Kelvin?", "Sumando 273,15: 25 °C son 298,15 K."),
          ("¿En qué temperatura coinciden Celsius y Fahrenheit?", "En −40: −40 °C = −40 °F.")],
    related=[("/calculadoras/ingenieria/conversor-de-temperatura/", "Conversor de Temperatura"),
             ("/calculadoras/ingenieria/conversor-de-unidades/", "Conversor de Unidades Técnicas"),
             ("/guias/ley-de-los-gases-ideales/", "Guía: la ley de los gases ideales")],
))
