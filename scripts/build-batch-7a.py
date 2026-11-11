"""
build-batch-7a.py — Lote 7a (motor común): Matemáticas (sistemas de ecuaciones, números primos, progresiones,
resolución de triángulos, números romanos) y Estadística (binomial, intervalo de confianza, tamaño de muestra).
Generación de una sola vez: después, el HTML de cada página es la fuente de verdad.
"""
from spec_lib import ENGINE, FORMULA, Lib, calc_page, help_blocks, write_page

MAT = dict(cat_slug="matematicas-avanzadas", cat_label="Matemáticas Avanzadas")
EST = dict(cat_slug="estadistica", cat_label="Estadística")


def page(rel, cat, **kw):
    write_page(rel, calc_page(pre_scripts=ENGINE, **cat, **kw))


def grid(cols, *parts):
    return f'        <div class="grid grid-cols-{cols} gap-2">\n' + "\n".join(parts) + "\n        </div>"


# ===================================================== sistemas de ecuaciones
L = Lib("se")
def co(id_, lab, when=None):
    return L.num(id_, lab, "0", rule="any", opt=True, default=0, when=when)
page("calculadoras/matematicas-avanzadas/sistemas-de-ecuaciones", MAT,
     slug="sistemas-de-ecuaciones", name="Calculadora de Sistemas de Ecuaciones 2×2 y 3×3",
     page_title="Calculadora de Sistemas de Ecuaciones Lineales 2×2 y 3×3 (Cramer) | Calculadora Científica",
     desc="Resolvé sistemas de dos o tres ecuaciones lineales con la regla de Cramer: valores de x, y, z, determinante y verificación. Gratis y con el método explicado.",
     og_title="Calculadora de Sistemas de Ecuaciones",
     og_desc="Sistemas lineales 2×2 y 3×3 por la regla de Cramer. Gratis.",
     schema_desc="Resuelve sistemas de ecuaciones lineales de 2×2 y 3×3 con la regla de Cramer, mostrando el determinante, los valores de las incógnitas y la verificación.",
     intro="Ingresá los coeficientes de cada ecuación (los vacíos valen 0) y obtené el valor de x, y (y z) con la regla de Cramer, el determinante del sistema y la verificación del resultado.",
     form_html=L.form([
         L.sel("size", "Tamaño del sistema", [("2", "2 ecuaciones con 2 incógnitas"), ("3", "3 ecuaciones con 3 incógnitas")]),
         grid(4, co("a1", "x"), co("b1", "y"), co("c1", "z", "size=3"), co("d1", "= término indep.")),
         grid(4, co("a2", "x"), co("b2", "y"), co("c2", "z", "size=3"), co("d2", "= término indep.")),
         grid(4, co("a3", "x", "size=3"), co("b3", "y", "size=3"), co("c3", "z", "size=3"), co("d3", "= término indep.", "size=3")),
     ], chips=[("2x + y = 5 · x − y = 1", "size=2;a1=2;b1=1;d1=5;a2=1;b2=-1;d2=1"), ("Sistema 3×3", "size=3;a1=2;b1=1;c1=-1;d1=8;a2=-3;b2=-1;c2=2;d2=-11;a3=-2;b3=1;c3=2;d3=-3")],
         note="Escribí cada ecuación como a·x + b·y + c·z = d. En un sistema 2×2 se usan solo las dos primeras filas."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Regla de Cramer", f'<p {FORMULA}>x = Δₓ / Δ &nbsp;·&nbsp; y = Δᵧ / Δ &nbsp;·&nbsp; z = Δ_z / Δ</p><p>Δ es el determinante de la matriz de coeficientes y Δₓ, Δᵧ, Δ_z son los determinantes que resultan de reemplazar la columna de x, y o z por los términos independientes.</p>'),
         ("Sistema 2×2", f'<p {FORMULA}>Δ = a₁·b₂ − a₂·b₁</p><p>Si Δ ≠ 0 hay una única solución. Si Δ = 0, el sistema es incompatible (sin solución) o compatible indeterminado (infinitas soluciones).</p>'),
         ("Verificación", "<p>Reemplazá los valores obtenidos en cada ecuación: tienen que dar el término independiente. La calculadora lo muestra en el sistema 2×2.</p>"),
     ]),
     related=[("/calculadoras/matematicas-avanzadas/calculadora-matrices/", "Calculadora de Matrices"), ("/calculadoras/matematicas-avanzadas/ecuaciones-segundo-grado/", "Ecuaciones de Segundo Grado"),
              ("/calculadoras/matematicas-avanzadas/regla-de-tres/", "Regla de Tres")],
     guide=("/guias/como-resolver-sistemas-de-ecuaciones/", "Cómo resolver sistemas de ecuaciones", "Leé la guía completa: sustitución, igualación, reducción y regla de Cramer con ejemplos resueltos."),
     faqs=[("¿Cómo se resuelve un sistema de ecuaciones 2×2?", "Con sustitución, igualación, reducción o la regla de Cramer: x = Δₓ/Δ e y = Δᵧ/Δ, con Δ = a₁b₂ − a₂b₁. Para 2x + y = 5 y x − y = 1: Δ = −3, x = 2, y = 1."),
           ("¿Qué pasa si el determinante es 0?", "El sistema no tiene solución única: puede ser incompatible (rectas paralelas) o tener infinitas soluciones (ecuaciones equivalentes)."),
           ("¿Cómo se resuelve un sistema 3×3?", "Con la regla de Cramer (cuatro determinantes de 3×3), el método de Gauss o sustitución sucesiva."),
           ("¿Y si una ecuación no tiene una de las incógnitas?", "Su coeficiente vale 0: dejá el campo vacío."),
           ("¿Sirve para sistemas no lineales?", "No: solo para ecuaciones lineales (sin potencias ni productos de incógnitas).")])

# ============================================================ números primos
L = Lib("np")
page("calculadoras/matematicas-avanzadas/numeros-primos", MAT,
     slug="numeros-primos", name="Calculadora de Números Primos",
     page_title="Calculadora de Números Primos: ¿Es Primo? Factores y Primo Siguiente | Calculadora Científica",
     desc="Verificá si un número es primo, descomponelo en factores primos, contá sus divisores y encontrá el primo siguiente y el anterior. Funciona hasta un billón. Gratis.",
     og_title="Calculadora de Números Primos",
     og_desc="¿Es primo?, factores primos, divisores y primos vecinos. Gratis.",
     schema_desc="Determina si un número es primo, lo descompone en factores primos, calcula su cantidad de divisores y encuentra el primo siguiente y el anterior, para números hasta 10^12.",
     intro="Ingresá un número entero y descubrí si es primo. Si es compuesto, ves su descomposición en factores primos y la cantidad de divisores; además, el primo siguiente y el anterior.",
     form_html=L.form([L.num("n", "Número entero", "Ej: 97", rule="int")], chips=[("97", "n=97"), ("360", "n=360"), ("1001", "n=1001"), ("999999999989", "n=999999999989")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Qué es un número primo", "<p>Es un entero mayor que 1 que solo tiene dos divisores: 1 y él mismo. Los primeros son 2, 3, 5, 7, 11, 13, 17, 19, 23… El 2 es el único primo par; el 1 no es primo ni compuesto.</p>"),
         ("Cómo se verifica", "<p>Basta probar los divisores hasta la raíz cuadrada del número: si ninguno lo divide, es primo. Para 97 alcanza con probar 2, 3, 5 y 7 (porque √97 ≈ 9,8).</p>"),
         ("Factores primos y divisores", f'<p>Todo compuesto se escribe de una sola forma como producto de primos (teorema fundamental de la aritmética): 360 = 2³ × 3² × 5. La cantidad de divisores es el producto de (exponente + 1): (3+1)(2+1)(1+1) = 24.</p>'),
     ]),
     related=[("/calculadoras/matematicas-avanzadas/mcd-y-mcm/", "Calculadora de MCD y MCM"), ("/calculadoras/matematicas-avanzadas/calculadora-de-fracciones/", "Calculadora de Fracciones"),
              ("/calculadoras/matematicas-avanzadas/conversor-de-bases-numericas/", "Conversor de Bases Numéricas")],
     guide=("/guias/como-saber-si-un-numero-es-primo/", "Cómo saber si un número es primo", "Leé la guía completa: criterios de divisibilidad, la prueba hasta la raíz cuadrada y la factorización."),
     faqs=[("¿Cómo sé si un número es primo?", "Probá dividirlo por los primos hasta su raíz cuadrada: si ninguno lo divide exactamente, es primo."),
           ("¿El 1 es primo?", "No: tiene un solo divisor. Por convención no es primo ni compuesto."),
           ("¿Cuál es el único primo par?", "El 2: todos los demás pares son divisibles por 2."),
           ("¿Cuántos divisores tiene un número?", "Se factoriza y se multiplican los (exponentes + 1). 360 = 2³·3²·5 tiene 24 divisores."),
           ("¿Hasta qué número funciona?", "Hasta 1.000.000.000.000 (un billón): el cálculo es instantáneo.")])

# ============================================================ progresiones
L = Lib("pg")
page("calculadoras/matematicas-avanzadas/progresiones-aritmeticas-y-geometricas", MAT,
     slug="progresiones-aritmeticas-y-geometricas", name="Calculadora de Progresiones Aritméticas y Geométricas",
     page_title="Calculadora de Progresiones Aritméticas y Geométricas: Término n y Suma | Calculadora Científica",
     desc="Calculá el término n-ésimo y la suma de los primeros n términos de una progresión aritmética o geométrica, y la suma infinita cuando converge. Gratis y con fórmulas.",
     og_title="Calculadora de Progresiones Aritméticas y Geométricas",
     og_desc="Término n-ésimo, suma de n términos y suma infinita. Gratis.",
     schema_desc="Calcula el término n-ésimo y la suma de los primeros n términos de progresiones aritméticas y geométricas, y la suma de infinitos términos de una progresión geométrica convergente.",
     intro="Elegí el tipo de progresión, ingresá el primer término, la diferencia o la razón y la cantidad de términos: obtenés el término n-ésimo, la suma y, en las geométricas con |r| < 1, la suma infinita.",
     form_html=L.form([
         L.sel("mode", "Tipo de progresión", [("ar", "Aritmética (se suma una diferencia)"), ("geo", "Geométrica (se multiplica por una razón)")]),
         L.num("a1", "Primer término (a₁)", "Ej: 3", rule="any"),
         L.num("d", "Diferencia (d)", "Ej: 4", rule="any", when="mode=ar"),
         L.num("r", "Razón (r)", "Ej: 2", rule="any", when="mode=geo"),
         L.num("n", "Cantidad de términos (n)", "Ej: 10", rule="int"),
     ], chips=[("Aritmética 3, 7, 11… (10 términos)", "mode=ar;a1=3;d=4;n=10"), ("Geométrica 2, 6, 18… (5 términos)", "mode=geo;a1=2;r=3;n=5"), ("Geométrica 1, ½, ¼… (10 términos)", "mode=geo;a1=1;r=0,5;n=10")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Progresión aritmética", f'<p {FORMULA}>aₙ = a₁ + (n − 1)·d &nbsp;·&nbsp; Sₙ = n·(a₁ + aₙ) / 2</p><p>Cada término se obtiene sumando una diferencia constante d. Ejemplo: 3, 7, 11, 15… tiene d = 4.</p>'),
         ("Progresión geométrica", f'<p {FORMULA}>aₙ = a₁·r^(n−1) &nbsp;·&nbsp; Sₙ = a₁·(rⁿ − 1) / (r − 1)</p><p>Cada término se obtiene multiplicando por una razón constante r. Ejemplo: 2, 6, 18, 54… tiene r = 3. Si r = 1, la suma es n·a₁.</p>'),
         ("Suma infinita", f'<p {FORMULA}>S∞ = a₁ / (1 − r), con |r| &lt; 1</p><p>Si la razón está entre −1 y 1, los términos se achican y la suma de infinitos términos converge. Con a₁ = 1 y r = ½, S∞ = 2.</p>'),
     ]),
     related=[("/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/", "Calculadora Científica Online"), ("/calculadoras/finanzas/interes-compuesto/", "Interés Compuesto"),
              ("/calculadoras/matematicas-avanzadas/regla-de-tres/", "Regla de Tres")],
     guide=("/guias/progresiones-aritmeticas-y-geometricas/", "Progresiones aritméticas y geométricas", "Leé la guía completa: las fórmulas, cómo distinguirlas, la suma infinita y ejemplos resueltos."),
     faqs=[("¿Cómo se calcula el término n de una progresión aritmética?", "aₙ = a₁ + (n − 1)·d. Para 3, 7, 11…: el décimo término es 3 + 9 × 4 = 39."),
           ("¿Cómo se suman los términos de una progresión aritmética?", "Sₙ = n·(a₁ + aₙ)/2. Los diez primeros de 3, 7, 11… suman 10 × (3 + 39) / 2 = 210."),
           ("¿Cómo se calcula el término n de una progresión geométrica?", "aₙ = a₁·r^(n−1). Para 2, 6, 18…: el quinto término es 2 × 3⁴ = 162."),
           ("¿Cuándo converge la suma de una progresión geométrica?", "Cuando |r| < 1: S∞ = a₁/(1 − r). Con a₁ = 1 y r = 1/2 da 2."),
           ("¿Cómo distingo si es aritmética o geométrica?", "Si la diferencia entre términos consecutivos es constante, es aritmética; si lo es el cociente, es geométrica.")])

# ============================================================ triángulos
L = Lib("tg")
page("calculadoras/matematicas-avanzadas/resolucion-de-triangulos", MAT,
     slug="resolucion-de-triangulos", name="Calculadora de Resolución de Triángulos",
     page_title="Calculadora de Triángulos: Teorema del Seno y del Coseno | Calculadora Científica",
     desc="Resolvé cualquier triángulo conociendo tres lados, dos lados y el ángulo comprendido, o dos ángulos y un lado: lados, ángulos, área y perímetro con los teoremas del coseno y del seno.",
     og_title="Calculadora de Resolución de Triángulos",
     og_desc="Lados, ángulos, área y perímetro con los teoremas del coseno y del seno. Gratis.",
     schema_desc="Resuelve triángulos cualesquiera (tres lados, dos lados y el ángulo comprendido, o dos ángulos y el lado comprendido) con los teoremas del coseno y del seno, calculando lados, ángulos, área y perímetro.",
     intro="Elegí qué datos conocés del triángulo: tres lados, dos lados y el ángulo entre ellos, o dos ángulos y el lado entre ellos. Obtenés todos los lados y ángulos, el área, el perímetro y el tipo de triángulo.",
     form_html=L.form([
         L.sel("mode", "Datos conocidos", [("sss", "Tres lados (a, b, c)"), ("sas", "Dos lados y el ángulo comprendido (a, b, C)"), ("asa", "Dos ángulos y el lado comprendido (A, B, c)")]),
         L.num("a", "Lado a", "Ej: 5", when="mode=sss|sas"),
         L.num("b", "Lado b", "Ej: 7", when="mode=sss|sas"),
         L.num("c", "Lado c", "Ej: 9", when="mode=sss|asa", hint="En el caso de dos ángulos, es el lado comprendido entre A y B."),
         L.num("C", "Ángulo C (grados)", "Ej: 60", when="mode=sas"),
         L.num("A", "Ángulo A (grados)", "Ej: 40", when="mode=asa"),
         L.num("B", "Ángulo B (grados)", "Ej: 60", when="mode=asa"),
     ], chips=[("Lados 3, 4 y 5", "mode=sss;a=3;b=4;c=5"), ("Lados 5 y 7 con ángulo de 60°", "mode=sas;a=5;b=7;C=60"), ("Ángulos 40° y 60° con lado 10", "mode=asa;A=40;B=60;c=10")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Teorema del coseno", f'<p {FORMULA}>c² = a² + b² − 2·a·b·cos(C)</p><p>Generaliza Pitágoras a cualquier triángulo. Con tres lados se despeja cada ángulo: cos(A) = (b² + c² − a²) / (2·b·c).</p>'),
         ("Teorema del seno", f'<p {FORMULA}>a / sen(A) = b / sen(B) = c / sen(C)</p><p>Relaciona cada lado con el seno de su ángulo opuesto. Sirve cuando se conocen dos ángulos y un lado.</p>'),
         ("Área", f'<p {FORMULA}>Área = √(s·(s−a)·(s−b)·(s−c)), con s = (a+b+c)/2</p><p>Fórmula de Herón. La suma de los ángulos interiores siempre es 180°.</p>'),
     ]),
     related=[("/calculadoras/matematicas-avanzadas/teorema-de-pitagoras/", "Teorema de Pitágoras"), ("/calculadoras/matematicas-avanzadas/calculadora-de-areas-y-volumenes/", "Áreas y Volúmenes"),
              ("/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/", "Calculadora Científica Online")],
     guide=("/guias/teorema-del-seno-y-del-coseno/", "Teorema del seno y del coseno", "Leé la guía completa: cuándo usar cada teorema, con ejemplos resueltos de triángulos cualesquiera."),
     faqs=[("¿Cómo se resuelve un triángulo con tres lados?", "Con el teorema del coseno se obtiene cada ángulo: cos(A) = (b² + c² − a²)/(2bc). Con lados 3, 4 y 5 el ángulo C es 90°."),
           ("¿Cuándo uso el teorema del seno?", "Cuando conocés dos ángulos y un lado (o dos lados y un ángulo opuesto a uno de ellos)."),
           ("¿Cuándo uso el teorema del coseno?", "Cuando conocés tres lados, o dos lados y el ángulo comprendido entre ellos."),
           ("¿Cuánto suman los ángulos de un triángulo?", "180°. Por eso, conocidos dos, el tercero es 180° − A − B."),
           ("¿Cómo calculo el área sin la altura?", "Con la fórmula de Herón a partir de los tres lados, o con ½·a·b·sen(C).")])

# ============================================================ romanos
L = Lib("nr")
page("calculadoras/matematicas-avanzadas/conversor-de-numeros-romanos", MAT,
     slug="conversor-de-numeros-romanos", name="Conversor de Números Romanos",
     page_title="Conversor de Números Romanos: de Arábigos a Romanos y al Revés | Calculadora Científica",
     desc="Convertí números arábigos a romanos (1 a 3999) y números romanos a arábigos, con la descomposición paso a paso y la validación de errores. Gratis.",
     og_title="Conversor de Números Romanos",
     og_desc="De arábigos a romanos y de romanos a arábigos, con el desarrollo. Gratis.",
     schema_desc="Convierte números arábigos (1 a 3999) a números romanos y números romanos a arábigos, con la descomposición paso a paso y validación de la escritura.",
     intro="Escribí un número (2024) o un número romano (MMXXIV) y obtené la conversión al otro sistema, con la descomposición paso a paso. Detecta automáticamente en qué sistema escribiste.",
     form_html=L.form([L.text("value", "Número arábigo o romano", "Ej: 2024 o MMXXIV")], chips=[("2024", "value=2024"), ("MCMXCIV", "value=MCMXCIV"), ("49", "value=49"), ("3999", "value=3999")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Las letras", "<p>I = 1 · V = 5 · X = 10 · L = 50 · C = 100 · D = 500 · M = 1000.</p>"),
         ("Reglas de escritura", "<p>Las letras se suman de mayor a menor (XVI = 16). Una letra menor delante de una mayor se resta (IV = 4, IX = 9, XL = 40, XC = 90, CD = 400, CM = 900). I, X, C y M se repiten hasta tres veces seguidas; V, L y D no se repiten.</p>"),
         ("Límite", "<p>El sistema estándar llega hasta 3999 (MMMCMXCIX): para números mayores se usaba una barra sobre la letra, que multiplica por mil.</p>"),
     ]),
     related=[("/calculadoras/matematicas-avanzadas/conversor-de-bases-numericas/", "Conversor de Bases Numéricas"), ("/calculadoras/matematicas-avanzadas/numeros-primos/", "Números Primos"),
              ("/calculadoras/matematicas-avanzadas/calculadora-basica/", "Calculadora Básica")],
     guide=("/guias/como-leer-y-escribir-numeros-romanos/", "Cómo leer y escribir números romanos", "Leé la guía completa: las letras, las reglas de suma y resta y ejemplos para convertir cualquier número."),
     faqs=[("¿Cómo se escribe 2024 en números romanos?", "MMXXIV: MM (2000) + XX (20) + IV (4)."),
           ("¿Cómo se convierte un número romano a arábigo?", "Se suman los valores de las letras, restando los de las que están delante de una mayor. MCMXCIV = 1000 + 900 + 90 + 4 = 1994."),
           ("¿Cuál es el número romano más grande?", "En el sistema estándar, 3999 (MMMCMXCIX)."),
           ("¿Por qué IIII no es válido?", "La regla estándar pide escribir 4 como IV (aunque algunos relojes usan IIII por tradición)."),
           ("¿Existe el cero en números romanos?", "No: los romanos no tenían símbolo para el cero.")])

# ============================================================ binomial
L = Lib("bi")
page("calculadoras/estadistica/distribucion-binomial", EST,
     slug="distribucion-binomial", name="Calculadora de Distribución Binomial",
     page_title="Calculadora de Distribución Binomial: P(X = k), Acumulada, Media y Varianza | Calculadora Científica",
     desc="Calculá probabilidades de la distribución binomial: P(X = k), P(X ≤ k), P(X ≥ k), media, varianza y desvío estándar a partir de n y la probabilidad de éxito. Gratis.",
     og_title="Calculadora de Distribución Binomial",
     og_desc="Probabilidad exacta y acumulada, media y desvío de una binomial. Gratis.",
     schema_desc="Calcula la probabilidad exacta y acumulada de una distribución binomial (P(X=k), P(X≤k), P(X≥k)), junto con la media, la varianza y el desvío estándar, para n de hasta 5000 ensayos.",
     intro="Ingresá la cantidad de ensayos, la probabilidad de éxito de cada uno y cuántos éxitos te interesan: obtenés la probabilidad exacta, las acumuladas, la media y el desvío estándar.",
     form_html=L.form([
         L.num("n", "Cantidad de ensayos (n)", "Ej: 10", rule="int"),
         L.num("p", "Probabilidad de éxito en cada ensayo (%)", "Ej: 50", rule="nonneg"),
         L.num("k", "Cantidad de éxitos (k)", "Ej: 5", rule="nonneg"),
     ], chips=[("10 monedas, 5 caras", "n=10;p=50;k=5"), ("20 ensayos al 30 %, 6 éxitos", "n=20;p=30;k=6"), ("Examen de 10 preguntas con 4 opciones, 7 aciertos al azar", "n=10;p=25;k=7")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("La fórmula", f'<p {FORMULA}>P(X = k) = C(n, k) · p<sup>k</sup> · (1 − p)<sup>n − k</sup></p><p>Es la probabilidad de obtener exactamente k éxitos en n ensayos independientes, cada uno con probabilidad de éxito p. C(n, k) es el número combinatorio.</p>'),
         ("Cuándo se usa", "<p>Cuando hay una cantidad fija de ensayos, cada uno con solo dos resultados (éxito o fracaso), la misma probabilidad en todos y ensayos independientes: lanzar monedas, aciertos al azar en un examen, piezas defectuosas en una muestra.</p>"),
         ("Media y desvío", f'<p {FORMULA}>media = n·p &nbsp;·&nbsp; varianza = n·p·(1 − p) &nbsp;·&nbsp; desvío = √(n·p·(1 − p))</p>'),
     ]),
     related=[("/calculadoras/estadistica/permutaciones-y-combinaciones/", "Permutaciones y Combinaciones"), ("/calculadoras/estadistica/distribucion-normal/", "Distribución Normal"),
              ("/calculadoras/estadistica/tamano-de-muestra/", "Tamaño de Muestra")],
     guide=("/guias/distribucion-binomial-explicada/", "La distribución binomial explicada", "Leé la guía completa: cuándo usarla, la fórmula, ejemplos resueltos y cómo leer las probabilidades acumuladas."),
     faqs=[("¿Cómo se calcula la probabilidad binomial?", "P(X = k) = C(n, k)·p^k·(1 − p)^(n−k). Con 10 monedas, la probabilidad de 5 caras es 252 × 0,5¹⁰ = 24,6 %."),
           ("¿Qué significa P(X ≤ k)?", "La probabilidad acumulada: de obtener k éxitos o menos. Es la suma de las probabilidades exactas de 0 a k."),
           ("¿Cuál es la media de una binomial?", "n·p. Con 20 ensayos al 30 %, se esperan 6 éxitos."),
           ("¿Cuándo no se puede usar la binomial?", "Si los ensayos no son independientes o la probabilidad cambia (por ejemplo, extraer sin reposición de una población chica)."),
           ("¿Cuál es el límite de ensayos?", "Hasta 5.000, con cálculo por logaritmos para evitar errores de redondeo.")])

# ============================================================ intervalo de confianza
L = Lib("ic")
page("calculadoras/estadistica/intervalo-de-confianza", EST,
     slug="intervalo-de-confianza", name="Calculadora de Intervalo de Confianza para la Media",
     page_title="Calculadora de Intervalo de Confianza para la Media (z y t) | Calculadora Científica",
     desc="Calculá el intervalo de confianza para la media al 90, 95 o 99 % con la distribución normal o t de Student, el margen de error y su interpretación. Gratis.",
     og_title="Calculadora de Intervalo de Confianza",
     og_desc="Intervalo de confianza de la media con z o t de Student. Gratis.",
     schema_desc="Calcula el intervalo de confianza para la media de una población a partir de la media muestral, el desvío estándar y el tamaño de la muestra, usando la distribución normal o la t de Student según corresponda.",
     intro="Ingresá la media de tu muestra, el desvío estándar, el tamaño de la muestra y el nivel de confianza: obtenés el margen de error y el intervalo donde estará la media verdadera de la población.",
     form_html=L.form([
         L.num("mean", "Media de la muestra (x̄)", "Ej: 50", rule="any"),
         L.num("sd", "Desvío estándar", "Ej: 10"),
         L.num("n", "Tamaño de la muestra (n)", "Ej: 25", rule="int"),
         L.sel("level", "Nivel de confianza", [("90", "90 %"), ("95", "95 %"), ("99", "99 %")], value="95"),
         L.sel("sdtype", "El desvío estándar es…", [("muestral", "Muestral (de tus datos)"), ("poblacional", "Poblacional (conocido)")]),
     ], chips=[("n = 25, media 50, desvío 10", "mean=50;sd=10;n=25;level=95;sdtype=muestral"), ("n = 100, media 50, desvío 10", "mean=50;sd=10;n=100;level=95;sdtype=muestral")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("La fórmula", f'<p {FORMULA}>x̄ ± c · s/√n</p><p>x̄ es la media muestral, s el desvío, n el tamaño y c el valor crítico: z si el desvío poblacional es conocido o la muestra es grande (n &gt; 30), y t de Student con n − 1 grados de libertad si el desvío es muestral y n ≤ 30.</p>'),
         ("Valores críticos z", "<p>90 % → 1,645 · 95 % → 1,960 · 99 % → 2,576.</p>"),
         ("Cómo se interpreta", "<p>Un intervalo del 95 % significa que, si repetiras el muestreo muchas veces, el 95 % de los intervalos construidos así contendrían a la media verdadera. No es la probabilidad de que la media esté dentro de este intervalo en particular.</p>"),
     ]),
     related=[("/calculadoras/estadistica/tamano-de-muestra/", "Tamaño de Muestra"), ("/calculadoras/estadistica/calculadora-estadistica-descriptiva/", "Estadística Descriptiva"),
              ("/calculadoras/estadistica/distribucion-normal/", "Distribución Normal")],
     guide=("/guias/intervalo-de-confianza-explicado/", "El intervalo de confianza explicado", "Leé la guía completa: la fórmula, z vs t de Student, cómo interpretarlo y un ejemplo resuelto."),
     faqs=[("¿Cómo se calcula el intervalo de confianza de la media?", "x̄ ± c·s/√n. Con media 50, desvío 10, n = 100 y 95 %: 50 ± 1,96 × 1 = [48,04 ; 51,96]."),
           ("¿Cuándo uso t de Student y cuándo z?", "z cuando el desvío poblacional es conocido o n > 30; t cuando solo tenés el desvío de la muestra y n ≤ 30."),
           ("¿Qué significa un nivel de confianza del 95 %?", "Que el método usado captura la media verdadera en el 95 % de las muestras posibles."),
           ("¿Cómo achico el intervalo?", "Aumentando el tamaño de la muestra o bajando el nivel de confianza."),
           ("¿Qué es el margen de error?", "La mitad del ancho del intervalo: c·s/√n.")])

# ============================================================ tamaño de muestra
L = Lib("tm")
page("calculadoras/estadistica/tamano-de-muestra", EST,
     slug="tamano-de-muestra", name="Calculadora de Tamaño de Muestra",
     page_title="Calculadora de Tamaño de Muestra: Nivel de Confianza y Margen de Error | Calculadora Científica",
     desc="Calculá cuántas personas hay que encuestar para estimar una proporción con el nivel de confianza y el margen de error que elijas, con corrección por población finita. Gratis.",
     og_title="Calculadora de Tamaño de Muestra",
     og_desc="Cuántas personas encuestar según confianza y margen de error. Gratis.",
     schema_desc="Calcula el tamaño de muestra necesario para estimar una proporción con un nivel de confianza y un margen de error dados, con corrección opcional por población finita.",
     intro="Elegí el nivel de confianza y el margen de error que aceptás y obtené cuántas personas tenés que encuestar. Si conocés el tamaño de la población, la calculadora corrige el resultado.",
     form_html=L.form([
         L.sel("level", "Nivel de confianza", [("90", "90 %"), ("95", "95 %"), ("99", "99 %")], value="95"),
         L.num("error", "Margen de error (%)", "Ej: 5"),
         L.num("p", "Proporción esperada (%)", "50", opt=True, default=50, rule="nonneg", value="50", hint="Si no la conocés, dejá 50 %: es el caso más exigente."),
         L.num("population", "Tamaño de la población — opcional", "Ej: 2000", opt=True, rule="int"),
     ], chips=[("95 %, error 5 %", "level=95;error=5;p=50;population="), ("95 %, error 5 %, población de 1.000", "level=95;error=5;p=50;population=1000"), ("99 %, error 3 %", "level=99;error=3;p=50;population=")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("La fórmula", f'<p {FORMULA}>n₀ = z² · p · (1 − p) / e²</p><p>z es el valor crítico del nivel de confianza (1,96 para 95 %), p la proporción esperada y e el margen de error. Con p = 50 %, z = 1,96 y e = 5 %: n₀ = 385.</p>'),
         ("Población finita", f'<p {FORMULA}>n = n₀ / (1 + (n₀ − 1) / N)</p><p>Si la población N es chica, la muestra necesaria baja: con N = 1.000 y los datos anteriores, n = 278.</p>'),
         ("Qué es cada dato", "<p>El <strong>margen de error</strong> es cuánto puede alejarse tu estimación del valor real; el <strong>nivel de confianza</strong>, qué tan seguro querés estar de que el valor real cae dentro de ese margen.</p>"),
     ]),
     related=[("/calculadoras/estadistica/intervalo-de-confianza/", "Intervalo de Confianza"), ("/calculadoras/estadistica/calculadora-estadistica-descriptiva/", "Estadística Descriptiva"),
              ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes")],
     guide=("/guias/como-calcular-el-tamano-de-una-muestra/", "Cómo calcular el tamaño de una muestra", "Leé la guía completa: la fórmula, la corrección por población finita y cómo elegir el margen de error."),
     faqs=[("¿Cómo se calcula el tamaño de la muestra?", "n = z²·p·(1 − p)/e². Con 95 % de confianza, p = 50 % y error 5 %: 385 personas."),
           ("¿Qué proporción uso si no la conozco?", "50 %: es la que maximiza p·(1 − p) y da la muestra más grande, o sea, la opción segura."),
           ("¿Influye el tamaño de la población?", "Solo si la población es chica: se aplica la corrección por población finita. Para poblaciones grandes, casi no cambia."),
           ("¿Cómo reduzco el tamaño de la muestra?", "Aceptando un margen de error mayor o un nivel de confianza menor."),
           ("¿Sirve para estimar medias?", "Esta calculadora es para proporciones. Para medias se usa n = (z·σ/e)².")])
