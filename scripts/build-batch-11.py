"""
build-batch-11.py — Lote 11 (motor común): Matemática (notación científica, potencias y raíces), Estadística (probabilidad
básica), Física (péndulo simple, ley de Coulomb, presión), Hogar y Construcción (escaleras) y Finanzas (meta de ahorro).
Genera las 8 páginas de calculadora; las guías están en build-batch-11-guides.py.
Generación de una sola vez: después, el HTML es la fuente de verdad.
"""
from spec_lib import ENGINE, FORMULA, Lib, calc_page, help_blocks, write_page

MAT = dict(cat_slug="matematicas-avanzadas", cat_label="Matemáticas Avanzadas")
EST = dict(cat_slug="estadistica", cat_label="Estadística")
FIS = dict(cat_slug="fisica", cat_label="Física")
HOG = dict(cat_slug="hogar-y-construccion", cat_label="Hogar y Construcción")
FIN = dict(cat_slug="finanzas", cat_label="Finanzas")


def page(rel, cat, **kw):
    write_page(rel, calc_page(pre_scripts=ENGINE, **cat, **kw))


# ================================================================ notación científica
L = Lib("nc")
page("calculadoras/matematicas-avanzadas/calculadora-de-notacion-cientifica", MAT,
     slug="calculadora-de-notacion-cientifica", name="Calculadora de Notación Científica",
     page_title="Calculadora de Notación Científica: Convertir y Operar (a × 10ⁿ) | Calculadora Científica",
     desc="Pasá un número a notación científica o de ingeniería, convertí a × 10ⁿ a decimal y sumá, restá, multiplicá o dividí números en notación científica. Gratis.",
     og_title="Calculadora de Notación Científica",
     og_desc="Convertí y operá con a × 10ⁿ: científica, ingeniería y decimal. Gratis.",
     schema_desc="Convierte números decimales a notación científica y de ingeniería, pasa de a × 10^n a decimal sin errores de redondeo y realiza sumas, restas, multiplicaciones y divisiones entre números en notación científica.",
     intro="Elegí qué necesitás: convertir un número decimal a notación científica, pasar un número de la forma a × 10ⁿ a decimal, o hacer una operación entre dos números en notación científica. La conversión es exacta: no pierde cifras.",
     form_html=L.form([
         L.sel("mode", "Qué querés hacer", [("sci", "Decimal → notación científica"), ("dec", "Notación científica → decimal"), ("op", "Operar con dos números en notación científica")]),
         L.text("dec", "Número decimal", "Ej: 0,00045 o 602000000000000000000000", when="mode=sci"),
         L.text("man", "Mantisa (a)", "Ej: 6,02", when="mode=dec"),
         L.num("exp", "Exponente (n, entero)", "Ej: 23", rule="any", when="mode=dec"),
         L.text("ma", "Primer número: mantisa", "Ej: 3", when="mode=op"),
         L.num("ea", "Primer número: exponente", "Ej: 8", rule="any", when="mode=op"),
         L.sel("op", "Operación", [("*", "× (multiplicar)"), ("/", "÷ (dividir)"), ("+", "+ (sumar)"), ("-", "− (restar)")], when="mode=op"),
         L.text("mb", "Segundo número: mantisa", "Ej: 2", when="mode=op"),
         L.num("eb", "Segundo número: exponente", "Ej: -3", rule="any", when="mode=op"),
     ], chips=[("0,00045", "mode=sci;dec=0,00045"), ("300.000.000 (velocidad de la luz en m/s)", "mode=sci;dec=300000000"), ("6,02 × 10²³ (número de Avogadro)", "mode=dec;man=6,02;exp=23"),
               ("3 × 10⁸ × 2 × 10⁻³", "mode=op;ma=3;ea=8;op=*;mb=2;eb=-3")],
         note="Con coma o con punto decimal. Un punto seguido de exactamente tres cifras (12.345) se toma como separador de miles."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Forma de la notación científica", f'<p {FORMULA}>N = a × 10ⁿ &nbsp;con&nbsp; 1 ≤ |a| &lt; 10 y n entero</p><p>Se escribe una sola cifra distinta de cero antes de la coma y se multiplica por una potencia de 10. 123.450 = 1,2345 × 10⁵ y 0,00045 = 4,5 × 10⁻⁴.</p>'),
         ("Notación de ingeniería", f'<p {FORMULA}>N = a × 10ⁿ &nbsp;con n múltiplo de 3</p><p>Se usa en electrónica y ciencias aplicadas porque el exponente coincide con los prefijos del SI: 10³ kilo, 10⁶ mega, 10⁻³ mili, 10⁻⁶ micro.</p>'),
         ("Operaciones", f'<p {FORMULA}>(a×10ᵐ)·(b×10ⁿ) = (a·b)×10ᵐ⁺ⁿ &nbsp;·&nbsp; (a×10ᵐ)/(b×10ⁿ) = (a/b)×10ᵐ⁻ⁿ</p><p>Para sumar o restar, los exponentes tienen que ser iguales (o se iguala uno de los números).</p>'),
     ]),
     related=[("/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/", "Calculadora Científica Online"), ("/calculadoras/ingenieria/conversor-de-unidades/", "Conversor de Unidades"),
              ("/calculadoras/matematicas-avanzadas/calculadora-de-logaritmos/", "Calculadora de Logaritmos")],
     guide=("/guias/notacion-cientifica-que-es-y-como-usarla/", "Notación científica: qué es y cómo usarla", "Leé la guía completa: cómo convertir, operar, los prefijos del SI y ejemplos con números muy grandes y muy chicos."),
     faqs=[("¿Cómo se pasa un número a notación científica?", "Se corre la coma hasta que quede una sola cifra distinta de cero a la izquierda y se multiplica por 10 elevado a la cantidad de lugares movidos. 123.450 = 1,2345 × 10⁵."),
           ("¿Cuándo el exponente es negativo?", "Cuando el número es menor que 1: la coma se corre hacia la derecha. 0,00045 = 4,5 × 10⁻⁴."),
           ("¿Cómo se multiplican dos números en notación científica?", "Se multiplican las mantisas y se suman los exponentes: (3 × 10⁸)(2 × 10⁻³) = 6 × 10⁵."),
           ("¿Qué es la notación de ingeniería?", "Es la notación científica con exponente múltiplo de 3, que se corresponde con los prefijos kilo, mega, mili y micro."),
           ("¿Cuánto es el número de Avogadro en decimal?", "6,02 × 10²³ = 602.000.000.000.000.000.000.000 partículas por mol.")])

# ================================================================ potencias y raíces
L = Lib("pr")
page("calculadoras/matematicas-avanzadas/calculadora-de-potencias-y-raices", MAT,
     slug="calculadora-de-potencias-y-raices", name="Calculadora de Potencias y Raíces",
     page_title="Calculadora de Potencias y Raíces: Raíz Cuadrada, Cúbica y Simplificación | Calculadora Científica",
     desc="Calculá potencias con cualquier exponente (negativo o fraccionario) y raíces de cualquier índice. Simplifica radicales (√72 = 6√2) y detecta raíces exactas. Gratis.",
     og_title="Calculadora de Potencias y Raíces",
     og_desc="Potencias, raíces de cualquier índice y simplificación de radicales. Gratis.",
     schema_desc="Calcula potencias con exponentes enteros, negativos y fraccionarios, raíces cuadradas, cúbicas y de cualquier índice, detecta potencias perfectas y simplifica radicales factorizando el radicando.",
     intro="Elegí si querés una potencia (aⁿ) o una raíz de cualquier índice. Además del resultado, te muestra la comprobación y, en las raíces, el radical simplificado (por ejemplo √72 = 6√2) o si la raíz es exacta.",
     form_html=L.form([
         L.sel("mode", "Qué querés calcular", [("pot", "Potencia: base elevada a un exponente"), ("raiz", "Raíz de cualquier índice")]),
         L.num("a", "Número (base o radicando)", "Ej: 72", rule="any"),
         L.num("n", "Exponente", "Ej: 3 (puede ser negativo o decimal)", rule="any", when="mode=pot"),
         L.num("k", "Índice de la raíz", "2 = cuadrada, 3 = cúbica", rule="int", when="mode=raiz", value="2"),
     ], chips=[("2¹⁰", "mode=pot;a=2;n=10"), ("5⁻²", "mode=pot;a=5;n=-2"), ("√72", "mode=raiz;a=72;k=2"), ("∛54", "mode=raiz;a=54;k=3"), ("√2", "mode=raiz;a=2;k=2"), ("∛(−27)", "mode=raiz;a=-27;k=3")],
         note="Las raíces de índice par de números negativos no existen en los números reales."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Potencias", f'<p {FORMULA}>aⁿ = a·a·…·a (n veces) &nbsp;·&nbsp; a⁻ⁿ = 1/aⁿ &nbsp;·&nbsp; a⁰ = 1 &nbsp;·&nbsp; a^(p/q) = ᵠ√(aᵖ)</p><p>Un exponente negativo da la inversa y uno fraccionario equivale a una raíz.</p>'),
         ("Raíces", f'<p {FORMULA}>ⁿ√x = y &nbsp;⇔&nbsp; yⁿ = x &nbsp;·&nbsp; ⁿ√x = x^(1/n)</p><p>La raíz cuadrada de 49 es 7 porque 7² = 49. La raíz cúbica de −27 es −3 porque (−3)³ = −27.</p>'),
         ("Simplificar radicales", f'<p {FORMULA}>ⁿ√(kⁿ·m) = k·ⁿ√m</p><p>Se factoriza el radicando y se sacan de la raíz los factores que se repiten n veces: √72 = √(2²·3²·2) = 6√2.</p>'),
     ]),
     related=[("/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/", "Calculadora Científica Online"), ("/calculadoras/matematicas-avanzadas/teorema-de-pitagoras/", "Teorema de Pitágoras"),
              ("/calculadoras/matematicas-avanzadas/numeros-primos/", "Números Primos y Factorización")],
     guide=("/guias/potencias-y-raices-propiedades-y-ejemplos/", "Potencias y raíces: propiedades y ejemplos", "Leé la guía completa: las propiedades, los exponentes negativos y fraccionarios y cómo simplificar radicales."),
     faqs=[("¿Cómo se calcula una potencia con exponente negativo?", "Es la inversa de la potencia con exponente positivo: 5⁻² = 1/5² = 1/25 = 0,04."),
           ("¿Cómo se simplifica una raíz cuadrada?", "Se factoriza el número y se sacan los factores repetidos: √72 = √(2³·3²) = 2·3·√2 = 6√2."),
           ("¿Qué es la raíz cúbica de un número negativo?", "Existe y es negativa: ∛(−27) = −3, porque (−3)³ = −27."),
           ("¿Por qué no existe la raíz cuadrada de un número negativo?", "Porque ningún número real elevado al cuadrado da un resultado negativo."),
           ("¿Cómo se calcula una raíz de cualquier índice?", "Elevando el número a 1/n: ⁴√16 = 16^(1/4) = 2.")])

# ================================================================ probabilidad
L = Lib("pb")
page("calculadoras/estadistica/calculadora-de-probabilidad", EST,
     slug="calculadora-de-probabilidad", name="Calculadora de Probabilidad",
     page_title="Calculadora de Probabilidad: Casos Favorables, Eventos Independientes y Al Menos Uno | Calculadora Científica",
     desc="Calculá la probabilidad de un evento (favorables/posibles), de dos eventos independientes (A y B, A o B, ninguno) y de que ocurra al menos un éxito en n intentos. Gratis.",
     og_title="Calculadora de Probabilidad",
     og_desc="Probabilidad simple, eventos independientes y al menos uno en n intentos. Gratis.",
     schema_desc="Calcula la probabilidad de un evento como casos favorables sobre casos posibles, la probabilidad de la intersección y la unión de dos eventos independientes, y la probabilidad de al menos un éxito en n intentos repetidos.",
     intro="Elegí el tipo de problema: la probabilidad de un evento a partir de los casos favorables y posibles, la de dos eventos independientes (que ocurran los dos, alguno o ninguno) o la de que algo pase al menos una vez en varios intentos.",
     form_html=L.form([
         L.sel("mode", "Tipo de problema", [("simple", "Un evento: casos favorables y posibles"), ("dos", "Dos eventos independientes A y B"), ("rep", "Al menos un éxito en n intentos")]),
         L.num("fav", "Casos favorables", "Ej: 1", rule="nonneg", when="mode=simple"),
         L.num("tot", "Casos posibles", "Ej: 6", when="mode=simple"),
         L.num("pa", "Probabilidad de A (%)", "Ej: 50", rule="nonneg", when="mode=dos"),
         L.num("pb", "Probabilidad de B (%)", "Ej: 30", rule="nonneg", when="mode=dos"),
         L.num("p", "Probabilidad de éxito en cada intento (%)", "Ej: 50", rule="nonneg", when="mode=rep"),
         L.num("n", "Cantidad de intentos", "Ej: 3", rule="int", when="mode=rep"),
     ], chips=[("Sacar un 6 con un dado", "mode=simple;fav=1;tot=6"), ("Sacar un as de un mazo de 52", "mode=simple;fav=4;tot=52"), ("A = 50 % y B = 30 %", "mode=dos;pa=50;pb=30"), ("Al menos una cara en 3 tiros de moneda", "mode=rep;p=50;n=3"),
               ("Al menos un 6 en 4 tiros de dado", "mode=rep;p=16,6667;n=4")],
         note="Los eventos independientes son los que no se influyen entre sí (por ejemplo, tiros distintos de una moneda)."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Probabilidad de un evento", f'<p {FORMULA}>P(A) = casos favorables / casos posibles</p><p>Vale cuando todos los casos son igualmente probables. Va de 0 (imposible) a 1 (seguro) o, en porcentaje, de 0 % a 100 %. La probabilidad de que no ocurra es 1 − P(A).</p>'),
         ("Dos eventos independientes", f'<p {FORMULA}>P(A y B) = P(A)·P(B) &nbsp;·&nbsp; P(A o B) = P(A) + P(B) − P(A)·P(B)</p><p>Hay que restar P(A y B) en la unión para no contar dos veces los casos en que pasan ambos.</p>'),
         ("Al menos uno en n intentos", f'<p {FORMULA}>P(al menos uno) = 1 − (1 − p)ⁿ</p><p>Es más simple calcular la probabilidad de que no ocurra ninguna vez, (1 − p)ⁿ, y restarla de 1.</p>'),
     ]),
     related=[("/calculadoras/estadistica/distribucion-binomial/", "Distribución Binomial"), ("/calculadoras/estadistica/permutaciones-y-combinaciones/", "Permutaciones y Combinaciones"),
              ("/calculadoras/estadistica/distribucion-normal/", "Distribución Normal")],
     guide=("/guias/como-calcular-probabilidades/", "Cómo calcular probabilidades", "Leé la guía completa: casos favorables, eventos independientes, el complemento y ejemplos con dados, monedas y cartas."),
     faqs=[("¿Cómo se calcula la probabilidad de un evento?", "Dividiendo los casos favorables por los casos posibles. Sacar un 6 con un dado: 1/6 ≈ 16,67 %."),
           ("¿Cuál es la probabilidad de que ocurran dos eventos independientes?", "Se multiplican: si A tiene 50 % y B 30 %, la probabilidad de que ocurran los dos es 0,5 × 0,3 = 15 %."),
           ("¿Cómo se calcula la probabilidad de al menos un éxito?", "Con 1 − (1 − p)ⁿ. Al menos una cara en 3 tiros de moneda: 1 − 0,5³ = 87,5 %."),
           ("¿Qué es el complemento de un evento?", "Es que no ocurra: P(no A) = 1 − P(A)."),
           ("¿Qué diferencia hay entre eventos independientes y excluyentes?", "Independientes: uno no influye en el otro. Excluyentes: no pueden ocurrir a la vez (por ejemplo, sacar par e impar en un mismo tiro).")])

# ================================================================ péndulo simple
L = Lib("pd")
page("calculadoras/fisica/calculadora-de-pendulo-simple", FIS,
     slug="calculadora-de-pendulo-simple", name="Calculadora de Péndulo Simple",
     page_title="Calculadora de Péndulo Simple: Período, Longitud y Gravedad (T = 2π√(L/g)) | Calculadora Científica",
     desc="Calculá el período, la frecuencia, la longitud o la gravedad de un péndulo simple con T = 2π√(L/g), con corrección por amplitud. Gratis y con fórmulas.",
     og_title="Calculadora de Péndulo Simple",
     og_desc="Período, longitud y gravedad de un péndulo: T = 2π√(L/g). Gratis.",
     schema_desc="Calcula el período y la frecuencia de un péndulo simple a partir de su longitud, despeja la longitud o la aceleración de la gravedad, y aplica una corrección por amplitud para ángulos grandes.",
     intro="Elegí qué querés averiguar: el período a partir de la longitud, la longitud necesaria para un período dado o la gravedad medida con un péndulo. Podés agregar la amplitud inicial para corregir el período en oscilaciones grandes.",
     form_html=L.form([
         L.sel("mode", "Qué querés calcular", [("T", "Período T (conozco la longitud)"), ("L", "Longitud L (conozco el período)"), ("g", "Gravedad g (conozco longitud y período)")]),
         L.num("L", "Longitud del hilo L (m)", "Ej: 1", when="mode=T|g"),
         L.num("T", "Período T (s)", "Ej: 2", when="mode=L|g"),
         L.num("g", "Gravedad g (m/s²)", "9,81", opt=True, default=9.81, value="9,81", when="mode=T|L"),
         L.num("angle", "Amplitud inicial (°) — opcional", "Ej: 30", opt=True, default=0, rule="nonneg", when="mode=T"),
     ], chips=[("Péndulo de 1 m", "mode=T;L=1;g=9,81;angle=0"), ("Con amplitud de 30°", "mode=T;L=1;g=9,81;angle=30"), ("¿Qué largo tiene un péndulo de 2 s?", "mode=L;T=2;g=9,81"), ("Medir g: L = 1 m y T = 2,007 s", "mode=g;L=1;T=2,007")],
         note="La fórmula es válida para oscilaciones pequeñas (menos de unos 15°)."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Período del péndulo", f'<p {FORMULA}>T = 2π·√(L / g)</p><p>Depende solo de la longitud y de la gravedad: no de la masa ni (para ángulos chicos) de la amplitud. Un péndulo de 1 m tiene un período de unos 2 s.</p>'),
         ("Despejes", f'<p {FORMULA}>L = g·T² / (4π²) &nbsp;·&nbsp; g = 4π²·L / T²</p><p>Con un hilo y una masa se puede medir la gravedad: se mide la longitud, se cronometran varias oscilaciones y se despeja g.</p>'),
         ("Corrección por amplitud", f'<p {FORMULA}>T ≈ T₀·(1 + θ₀²/16 + 11·θ₀⁴/3072) &nbsp;(θ₀ en radianes)</p><p>Con 30° de amplitud el período real es un 1,7 % mayor que el de la fórmula simple.</p>'),
     ]),
     related=[("/calculadoras/fisica/calculadora-de-movimiento-circular/", "Movimiento Circular Uniforme"), ("/calculadoras/fisica/energia-cinetica-y-potencial/", "Energía Cinética y Potencial"),
              ("/calculadoras/fisica/caida-libre-y-tiro-oblicuo/", "Caída Libre y Tiro Oblicuo")],
     guide=("/guias/periodo-del-pendulo-simple/", "Período del péndulo simple", "Leé la guía completa: la fórmula, de qué depende el período, cómo medir g y ejemplos resueltos."),
     faqs=[("¿Cómo se calcula el período de un péndulo?", "Con T = 2π·√(L/g). Para L = 1 m y g = 9,81 m/s²: T = 2π·√(0,102) ≈ 2,01 s."),
           ("¿De qué depende el período de un péndulo?", "De la longitud y de la gravedad. No depende de la masa, y para ángulos chicos tampoco de la amplitud."),
           ("¿Qué longitud tiene un péndulo de 2 segundos?", "L = g·T²/(4π²) ≈ 0,994 m: cerca de un metro."),
           ("¿Cómo se mide la gravedad con un péndulo?", "Se mide la longitud y el período (cronometrando varias oscilaciones y dividiendo) y se despeja g = 4π²·L/T²."),
           ("¿Hasta qué ángulo vale la fórmula?", "Para amplitudes de hasta unos 15° el error es menor al 0,5 %. Más allá conviene aplicar la corrección por amplitud.")])

# ================================================================ ley de Coulomb
L = Lib("cl")
QU = [("uC", "µC (microcoulomb)"), ("nC", "nC (nanocoulomb)"), ("mC", "mC (milicoulomb)"), ("pC", "pC (picocoulomb)"), ("C", "C (coulomb)")]
RU = [("m", "metros (m)"), ("cm", "centímetros (cm)"), ("mm", "milímetros (mm)")]
page("calculadoras/fisica/calculadora-de-ley-de-coulomb", FIS,
     slug="calculadora-de-ley-de-coulomb", name="Calculadora de la Ley de Coulomb",
     page_title="Calculadora de la Ley de Coulomb: Fuerza entre Cargas (F = k·q₁·q₂/r²) | Calculadora Científica",
     desc="Calculá la fuerza eléctrica entre dos cargas, la distancia o una de las cargas con la ley de Coulomb. Indica si es atractiva o repulsiva. Gratis y con fórmulas.",
     og_title="Calculadora de la Ley de Coulomb",
     og_desc="Fuerza entre cargas, distancia o carga con F = k·q₁·q₂/r². Gratis.",
     schema_desc="Calcula la fuerza eléctrica entre dos cargas puntuales con la ley de Coulomb, despeja la distancia o una de las cargas, e indica si la interacción es atractiva o repulsiva según los signos.",
     intro="Elegí la incógnita de la ley de Coulomb (fuerza, distancia o carga), cargá los datos con sus unidades (µC, nC, cm, mm…) y obtenés el resultado. Con los signos de las cargas te dice si la fuerza es atractiva o repulsiva.",
     form_html=L.form([
         L.sel("mode", "Qué querés calcular", [("f", "Fuerza F entre las cargas"), ("r", "Distancia r entre las cargas"), ("q", "Carga q₂ (valor absoluto)")]),
         L.num("q1", "Carga q₁ (con su signo)", "Ej: 1", rule="any"),
         L.sel("q1u", "Unidad de q₁", QU),
         L.num("q2", "Carga q₂ (con su signo)", "Ej: -1", rule="any", when="mode=f|r"),
         L.sel("q2u", "Unidad de q₂", QU, when="mode=f|r"),
         L.num("r", "Distancia r", "Ej: 10", when="mode=f|q"),
         L.sel("ru", "Unidad de la distancia", RU, when="mode=f|q", value="cm"),
         L.num("F", "Fuerza F (N)", "Ej: 5", when="mode=r|q"),
     ], chips=[("1 µC y 1 µC a 10 cm", "mode=f;q1=1;q1u=uC;q2=1;q2u=uC;r=10;ru=cm"), ("+2 µC y −3 µC a 5 cm", "mode=f;q1=2;q1u=uC;q2=-3;q2u=uC;r=5;ru=cm"), ("Electrón y protón del hidrógeno", "mode=f;q1=1,602e-19;q1u=C;q2=-1,602e-19;q2u=C;r=5,29e-11;ru=m"),
               ("¿A qué distancia hay 5 N?", "mode=r;q1=2;q1u=uC;q2=3;q2u=uC;F=5")],
         note="Cargas puntuales en el vacío (o en el aire). Signo igual: repulsión. Signo distinto: atracción."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Ley de Coulomb", f'<p {FORMULA}>F = k·q₁·q₂ / r² &nbsp; con &nbsp; k = 8,99 × 10⁹ N·m²/C²</p><p>La fuerza entre dos cargas puntuales es proporcional al producto de las cargas e inversamente proporcional al cuadrado de la distancia: al duplicar la distancia, la fuerza se reduce a la cuarta parte.</p>'),
         ("Atracción y repulsión", "<p>Cargas del mismo signo se repelen y de signo opuesto se atraen. Las dos fuerzas tienen igual intensidad y sentido contrario (tercera ley de Newton).</p>"),
         ("Unidades de carga", f'<p {FORMULA}>1 µC = 10⁻⁶ C &nbsp;·&nbsp; 1 nC = 10⁻⁹ C &nbsp;·&nbsp; carga del electrón: 1,602 × 10⁻¹⁹ C</p><p>El coulomb es una unidad enorme: en la práctica se usan submúltiplos.</p>'),
     ]),
     related=[("/calculadoras/fisica/ley-de-ohm/", "Ley de Ohm"), ("/calculadoras/fisica/segunda-ley-de-newton/", "Segunda Ley de Newton"),
              ("/calculadoras/matematicas-avanzadas/calculadora-de-notacion-cientifica/", "Notación Científica")],
     guide=("/guias/ley-de-coulomb-explicada/", "Ley de Coulomb explicada", "Leé la guía completa: la fórmula, las unidades, atracción y repulsión y ejemplos resueltos."),
     faqs=[("¿Qué dice la ley de Coulomb?", "Que la fuerza entre dos cargas puntuales es proporcional al producto de las cargas e inversamente proporcional al cuadrado de la distancia: F = k·q₁·q₂/r²."),
           ("¿Cuánto vale la constante k?", "k = 8,99 × 10⁹ N·m²/C² en el vacío."),
           ("¿Cómo sé si la fuerza es atractiva o repulsiva?", "Si las cargas tienen el mismo signo se repelen; si tienen signos opuestos se atraen."),
           ("¿Qué pasa con la fuerza si duplico la distancia?", "Se reduce a la cuarta parte, porque depende de 1/r²."),
           ("¿Cuál es la fuerza entre un electrón y un protón en el hidrógeno?", "Unos 8,2 × 10⁻⁸ N, atractiva, con una distancia de 5,29 × 10⁻¹¹ m.")])

# ================================================================ presión
L = Lib("ps")
page("calculadoras/fisica/calculadora-de-presion", FIS,
     slug="calculadora-de-presion", name="Calculadora de Presión y Presión Hidrostática",
     page_title="Calculadora de Presión: P = F/A y Presión Hidrostática (ρ·g·h) | Calculadora Científica",
     desc="Calculá la presión como fuerza sobre superficie o la presión hidrostática de un líquido a cierta profundidad, con conversión a Pa, kPa, atm, bar, mmHg y psi. Gratis.",
     og_title="Calculadora de Presión",
     og_desc="P = F/A y presión hidrostática ρ·g·h, en Pa, atm, bar, mmHg y psi. Gratis.",
     schema_desc="Calcula la presión ejercida por una fuerza sobre una superficie (P = F/A) y la presión hidrostática de una columna de líquido (P = ρ·g·h), con presión absoluta y conversión a Pa, kPa, atm, bar, mmHg y psi.",
     intro="Elegí si querés la presión que ejerce una fuerza sobre una superficie o la que hace un líquido a cierta profundidad. El resultado se muestra en pascales y en atmósferas, bar, mmHg y psi; en el caso del líquido, también la presión absoluta.",
     form_html=L.form([
         L.sel("mode", "Qué querés calcular", [("sol", "Presión de una fuerza sobre una superficie (P = F/A)"), ("hid", "Presión hidrostática de un líquido (P = ρ·g·h)")]),
         L.num("F", "Fuerza F (N)", "Ej: 100", when="mode=sol"),
         L.num("A", "Superficie A", "Ej: 0,5", when="mode=sol"),
         L.sel("Au", "Unidad de la superficie", [("m2", "m²"), ("cm2", "cm²"), ("mm2", "mm²")], when="mode=sol"),
         L.num("rho", "Densidad del líquido ρ (kg/m³)", "Ej: 1000", when="mode=hid", hint="Agua dulce 1.000 · agua de mar 1.025 · aceite 920 · mercurio 13.550"),
         L.num("h", "Profundidad h (m)", "Ej: 10", when="mode=hid"),
         L.num("g", "Gravedad g (m/s²)", "9,81", opt=True, default=9.81, value="9,81", when="mode=hid"),
     ], chips=[("100 N sobre 0,5 m²", "mode=sol;F=100;A=0,5;Au=m2"), ("Un tacón: 600 N sobre 1 cm²", "mode=sol;F=600;A=1;Au=cm2"), ("10 m bajo el agua", "mode=hid;rho=1000;h=10;g=9,81"), ("30 m en el mar", "mode=hid;rho=1025;h=30;g=9,81")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Presión de una fuerza", f'<p {FORMULA}>P = F / A &nbsp;·&nbsp; 1 Pa = 1 N/m²</p><p>La misma fuerza produce más presión cuanto menor es la superficie: por eso un cuchillo afilado corta y un tacón aguja marca el piso.</p>'),
         ("Presión hidrostática", f'<p {FORMULA}>P = ρ · g · h</p><p>Aumenta con la profundidad y con la densidad del líquido, y no depende de la forma del recipiente. En el agua, la presión sube aproximadamente 1 atm cada 10 metros.</p>'),
         ("Equivalencias", f'<p {FORMULA}>1 atm = 101.325 Pa = 1,01325 bar = 760 mmHg = 14,696 psi</p><p>La presión absoluta suma la atmosférica a la presión del líquido (presión manométrica).</p>'),
     ]),
     related=[("/calculadoras/fisica/calculadora-de-densidad/", "Calculadora de Densidad"), ("/calculadoras/ingenieria/conversor-de-unidades/", "Conversor de Unidades"),
              ("/calculadoras/quimica/leyes-de-los-gases/", "Leyes de los Gases")],
     guide=("/guias/presion-y-presion-hidrostatica/", "Presión y presión hidrostática", "Leé la guía completa: P = F/A, la presión de los líquidos, las unidades y ejemplos resueltos."),
     faqs=[("¿Cómo se calcula la presión?", "Dividiendo la fuerza por la superficie: P = F/A. 100 N sobre 0,5 m² dan 200 Pa."),
           ("¿Cómo se calcula la presión hidrostática?", "P = ρ·g·h. A 10 m de profundidad en agua: 1.000 × 9,81 × 10 = 98.100 Pa, casi 1 atm."),
           ("¿Cuánto aumenta la presión por cada 10 metros bajo el agua?", "Aproximadamente 1 atmósfera. A 10 m de profundidad la presión absoluta es de unas 2 atm."),
           ("¿Cuál es la diferencia entre presión absoluta y manométrica?", "La manométrica es la que genera el líquido (ρ·g·h); la absoluta le suma la presión atmosférica (101.325 Pa)."),
           ("¿Cómo paso de pascales a atmósferas?", "Dividiendo por 101.325: 98.100 Pa ≈ 0,968 atm.")])

# ================================================================ escaleras
L = Lib("es")
page("calculadoras/hogar-y-construccion/calculadora-de-escaleras", HOG,
     slug="calculadora-de-escaleras", name="Calculadora de Escaleras: Escalones, Contrahuella y Huella",
     page_title="Calculadora de Escaleras: Cantidad de Escalones, Altura y Huella (Fórmula de Blondel) | Calculadora Científica",
     desc="Calculá cuántos escalones necesita una escalera, la altura de cada contrahuella, la huella y el recorrido con la fórmula de Blondel. Verifica la comodidad. Gratis.",
     og_title="Calculadora de Escaleras",
     og_desc="Escalones, contrahuella, huella y recorrido con la fórmula de Blondel. Gratis.",
     schema_desc="Calcula la cantidad de escalones de una escalera, la altura de la contrahuella, la profundidad de la huella con la fórmula de Blondel (2c + h = 63 cm), el recorrido horizontal, la inclinación y verifica la comodidad.",
     intro="Ingresá la altura que tiene que salvar la escalera (de piso a piso) y la altura de escalón que preferís. Obtenés la cantidad de escalones, la contrahuella exacta, la huella según la fórmula de Blondel, el recorrido horizontal y si la escalera es cómoda.",
     form_html=L.form([
         L.num("height", "Altura a salvar (de piso a piso)", "Ej: 2,70", when=None),
         L.sel("unit", "Unidad de la altura", [("m", "metros (m)"), ("cm", "centímetros (cm)")]),
         L.num("riser", "Contrahuella deseada (cm)", "17,5", opt=True, default=17.5, value="17,5", hint="Es la altura de cada escalón. Lo habitual es de 17 a 18 cm."),
         L.num("tread", "Huella (cm) — opcional", "Vacío = se calcula con Blondel", opt=True, rule="pos", hint="Es la profundidad de la pisada. Si la dejás vacía, se calcula como 63 − 2 × contrahuella."),
     ], chips=[("Piso a piso de 2,70 m", "height=2,7;unit=m;riser=17,5;tread="), ("2,80 m con escalones de 17 cm", "height=2,8;unit=m;riser=17;tread="), ("Entrepiso de 1,50 m", "height=1,5;unit=m;riser=17,5;tread="), ("2,70 m con huella de 30 cm", "height=2,7;unit=m;riser=17,5;tread=30")],
         note="Verificá siempre la normativa de edificación de tu zona."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Contrahuella y huella", "<p>La contrahuella (o alzada) es la altura de cada escalón; la huella (o pisada), su profundidad. En una escalera de n escalones hay n contrahuellas y n − 1 huellas, porque el piso superior hace de último peldaño.</p>"),
         ("Fórmula de Blondel", f'<p {FORMULA}>2·c + h = 63 cm (entre 60 y 64)</p><p>Relaciona la altura del escalón con la profundidad de la pisada para que el paso sea cómodo: con una contrahuella de 18 cm, la huella ideal es de 27 cm.</p>'),
         ("Cantidad de escalones", f'<p {FORMULA}>n = altura / contrahuella (redondeado) &nbsp;·&nbsp; c real = altura / n</p><p>Se redondea a un número entero de escalones y se recalcula la contrahuella para que todos sean iguales.</p>'),
     ]),
     related=[("/calculadoras/hogar-y-construccion/calculadora-de-hormigon/", "Calculadora de Hormigón"), ("/calculadoras/matematicas-avanzadas/teorema-de-pitagoras/", "Teorema de Pitágoras"),
              ("/calculadoras/hogar-y-construccion/calculadora-de-ceramicos/", "Calculadora de Cerámicos")],
     guide=("/guias/como-calcular-una-escalera/", "Cómo calcular una escalera", "Leé la guía completa: contrahuella, huella, la fórmula de Blondel y un ejemplo resuelto paso a paso."),
     faqs=[("¿Cuántos escalones necesita una escalera de 2,70 m?", "Con una contrahuella de unos 17,5 cm, 15 escalones: 270 / 15 = 18 cm cada uno."),
           ("¿Qué es la fórmula de Blondel?", "2 × contrahuella + huella = 63 cm (entre 60 y 64). Asegura una relación cómoda entre la altura y la profundidad del escalón."),
           ("¿Cuál es la altura ideal de un escalón?", "Entre 17 y 18 cm. Menos de 15 cm o más de 20 cm resultan incómodos."),
           ("¿Cuánto espacio horizontal ocupa una escalera?", "(n − 1) × huella. Con 15 escalones y huella de 27 cm: 14 × 27 = 3,78 m."),
           ("¿Por qué hay un escalón menos de huellas que de contrahuellas?", "Porque el último peldaño es el propio piso superior.")])

# ================================================================ meta de ahorro
L = Lib("ma")
page("calculadoras/finanzas/calculadora-de-meta-de-ahorro", FIN,
     slug="calculadora-de-meta-de-ahorro", name="Calculadora de Meta de Ahorro",
     page_title="Calculadora de Meta de Ahorro: Cuánto Ahorrar por Mes para Llegar a un Objetivo | Calculadora Científica",
     desc="Calculá cuánto tenés que ahorrar por mes para llegar a una meta en cierto plazo, o en cuántos meses la alcanzás con un aporte dado, con interés opcional. Gratis.",
     og_title="Calculadora de Meta de Ahorro",
     og_desc="Aporte mensual necesario o tiempo para llegar a tu meta, con interés opcional. Gratis.",
     schema_desc="Calcula el aporte mensual necesario para alcanzar una meta de ahorro en un plazo dado, o el tiempo que se tarda en llegar a ella con un aporte fijo, con capital inicial y tasa nominal anual opcionales.",
     intro="Ingresá cuánto querés juntar y elegí qué necesitás: el aporte mensual para llegar en cierto plazo, o cuántos meses tardás aportando un monto fijo. Podés sumar un capital inicial y una tasa de interés (TNA).",
     form_html=L.form([
         L.sel("mode", "Qué querés calcular", [("aporte", "Cuánto ahorrar por mes (tengo el plazo)"), ("tiempo", "En cuántos meses llego (tengo el aporte)")]),
         L.num("goal", "Meta de ahorro ($)", "Ej: 1200000"),
         L.num("initial", "Capital inicial ($) — opcional", "0", opt=True, default=0, rule="nonneg"),
         L.num("tna", "Tasa nominal anual TNA (%) — opcional", "0", opt=True, default=0, rule="nonneg", hint="Capitalización mensual. Dejala en 0 si guardás el dinero sin interés."),
         L.num("months", "Plazo (meses)", "Ej: 12", rule="int", when="mode=aporte"),
         L.num("amount", "Aporte mensual ($)", "Ej: 50000", when="mode=tiempo"),
     ], chips=[("$1.200.000 en 12 meses, sin interés", "mode=aporte;goal=1200000;initial=0;tna=0;months=12"), ("Lo mismo con TNA del 40 %", "mode=aporte;goal=1200000;initial=0;tna=40;months=12"), ("Aportando $50.000 por mes, ¿cuándo llego a $2.000.000?", "mode=tiempo;goal=2000000;initial=0;tna=0;amount=50000"),
               ("Con $300.000 iniciales", "mode=tiempo;goal=2000000;initial=300000;tna=0;amount=50000")],
         note="Los aportes se hacen al final de cada mes. No considera inflación ni impuestos."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Sin interés", f'<p {FORMULA}>aporte = (meta − capital inicial) / meses</p><p>Es la cuenta más simple: se reparte lo que falta en partes iguales. Para $1.200.000 en 12 meses: $100.000 por mes.</p>'),
         ("Con interés", f'<p {FORMULA}>Meta = P·(1 + i)ⁿ + A·((1 + i)ⁿ − 1) / i &nbsp;con&nbsp; i = TNA / 12</p><p>Los aportes generan intereses, así que hace falta ahorrar menos que sin interés. Se despeja el aporte A o la cantidad de meses n.</p>'),
         ("Importante", "<p>Si la inflación es mayor que la tasa que obtenés, el dinero ahorrado pierde poder de compra: conviene calcular la meta en pesos de hoy y actualizarla periódicamente.</p>"),
     ]),
     related=[("/calculadoras/finanzas/interes-compuesto/", "Interés Compuesto"), ("/calculadoras/finanzas/calculadora-de-plazo-fijo/", "Plazo Fijo (TNA y TEA)"),
              ("/calculadoras/finanzas/calculadora-de-inflacion-acumulada/", "Inflación Acumulada")],
     guide=("/guias/como-calcular-cuanto-ahorrar-para-una-meta/", "Cómo calcular cuánto ahorrar para una meta", "Leé la guía completa: el aporte mensual, el efecto del interés, la inflación y ejemplos resueltos."),
     faqs=[("¿Cómo calculo cuánto tengo que ahorrar por mes?", "Sin interés, dividí lo que te falta por los meses: $1.200.000 en 12 meses son $100.000 por mes. Con interés, el aporte es menor."),
           ("¿En cuántos meses llego a mi meta?", "Sin interés, meta ÷ aporte. Con $50.000 por mes, $2.000.000 se juntan en 40 meses."),
           ("¿Cómo influye el interés?", "Los intereses suman al ahorro, por lo que hace falta aportar menos. Cuanto más largo el plazo, mayor el efecto."),
           ("¿Y la inflación?", "Si los precios suben más que tu tasa, la meta en pesos nominales deja de alcanzar. Conviene revisar y actualizar el objetivo cada tanto."),
           ("¿Los aportes se hacen al inicio o al final del mes?", "Esta calculadora supone aportes al final de cada mes (anualidad vencida).")])
