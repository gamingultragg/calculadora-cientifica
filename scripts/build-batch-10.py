"""
build-batch-10.py — Lote 10 (motor común): Matemática (recta y distancia entre puntos, logaritmos), Física (densidad, calor
específico, movimiento circular), Química (leyes de los gases, concentración en ppm) y Vida Diaria (consumo de combustible).
Genera las 8 páginas de calculadora; las guías están en build-batch-10-guides.py.
Generación de una sola vez: después, el HTML es la fuente de verdad.
"""
from spec_lib import ENGINE, FORMULA, Lib, calc_page, help_blocks, write_page

MAT = dict(cat_slug="matematicas-avanzadas", cat_label="Matemáticas Avanzadas")
FIS = dict(cat_slug="fisica", cat_label="Física")
QUI = dict(cat_slug="quimica", cat_label="Química")
VID = dict(cat_slug="vida-diaria", cat_label="Vida Diaria")


def page(rel, cat, **kw):
    write_page(rel, calc_page(pre_scripts=ENGINE, **cat, **kw))


# ================================================================ recta y distancia entre puntos
L = Lib("rc")
page("calculadoras/matematicas-avanzadas/recta-y-distancia-entre-puntos", MAT,
     slug="recta-y-distancia-entre-puntos", name="Calculadora de Recta y Distancia entre Dos Puntos",
     page_title="Calculadora de Pendiente, Ecuación de la Recta y Distancia entre Dos Puntos | Calculadora Científica",
     desc="Ingresá dos puntos y calculá la pendiente, la ecuación de la recta (y = mx + b y forma general), la distancia, el punto medio y el ángulo de inclinación. Gratis.",
     og_title="Calculadora de Recta y Distancia entre Dos Puntos",
     og_desc="Pendiente, ecuación de la recta, distancia y punto medio entre dos puntos. Gratis.",
     schema_desc="Calcula la pendiente, la ecuación de la recta que pasa por dos puntos (forma explícita y general), la distancia entre ellos, el punto medio y el ángulo de inclinación.",
     intro="Ingresá las coordenadas de dos puntos (x₁; y₁) y (x₂; y₂). Obtenés la pendiente, la ecuación de la recta que los une, la distancia entre ellos, el punto medio y el ángulo de inclinación.",
     form_html=L.form([
         L.num("x1", "x₁", "Ej: 1", rule="any"),
         L.num("y1", "y₁", "Ej: 2", rule="any"),
         L.num("x2", "x₂", "Ej: 3", rule="any"),
         L.num("y2", "y₂", "Ej: 6", rule="any"),
     ], chips=[("(1; 2) y (3; 6)", "x1=1;y1=2;x2=3;y2=6"), ("(0; 4) y (2; 0)", "x1=0;y1=4;x2=2;y2=0"), ("Recta vertical", "x1=2;y1=1;x2=2;y2=5"), ("Recta horizontal", "x1=1;y1=3;x2=5;y2=3")],
         note="Podés usar negativos y decimales (con coma o con punto)."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Pendiente y ecuación", f'<p {FORMULA}>m = (y₂ − y₁) / (x₂ − x₁) &nbsp;·&nbsp; y = m·x + b &nbsp;·&nbsp; b = y₁ − m·x₁</p><p>La pendiente indica cuánto sube (o baja) la recta por cada unidad que avanza en x. Si x₂ = x₁ la recta es vertical y la pendiente no está definida: la ecuación es x = constante.</p>'),
         ("Distancia y punto medio", f'<p {FORMULA}>d = √((x₂ − x₁)² + (y₂ − y₁)²) &nbsp;·&nbsp; M = ((x₁ + x₂)/2 ; (y₁ + y₂)/2)</p><p>La distancia sale del teorema de Pitágoras aplicado al triángulo rectángulo que forman los dos puntos.</p>'),
         ("Paralelas y perpendiculares", "<p>Dos rectas son paralelas si tienen la misma pendiente y perpendiculares si el producto de sus pendientes es −1 (la pendiente de una es la inversa cambiada de signo de la otra).</p>"),
     ]),
     related=[("/calculadoras/matematicas-avanzadas/teorema-de-pitagoras/", "Teorema de Pitágoras"), ("/calculadoras/matematicas-avanzadas/graficador-de-funciones/", "Graficador de Funciones"),
              ("/calculadoras/matematicas-avanzadas/sistemas-de-ecuaciones/", "Sistemas de Ecuaciones")],
     guide=("/guias/como-calcular-la-pendiente-y-la-distancia-entre-dos-puntos/", "Cómo calcular la pendiente y la distancia entre dos puntos", "Leé la guía completa: la fórmula de la pendiente, la ecuación de la recta y ejemplos resueltos."),
     faqs=[("¿Cómo se calcula la pendiente entre dos puntos?", "Se divide la diferencia de alturas por la diferencia de posiciones: m = (y₂ − y₁)/(x₂ − x₁). Entre (1; 2) y (3; 6): m = (6 − 2)/(3 − 1) = 2."),
           ("¿Cómo se halla la ecuación de la recta que pasa por dos puntos?", "Se calcula la pendiente m y después la ordenada al origen b = y₁ − m·x₁. Con los puntos (1; 2) y (3; 6): m = 2, b = 0, y la recta es y = 2x."),
           ("¿Cómo se calcula la distancia entre dos puntos?", "Con d = √((x₂ − x₁)² + (y₂ − y₁)²). Entre (1; 2) y (3; 6): √(4 + 16) = √20 ≈ 4,47."),
           ("¿Qué pasa si los dos puntos tienen la misma x?", "La recta es vertical: la pendiente no está definida y la ecuación es x = x₁."),
           ("¿Cómo sé si dos rectas son perpendiculares?", "Si el producto de sus pendientes da −1. La perpendicular a una recta de pendiente 2 tiene pendiente −1/2.")])

# ================================================================ logaritmos
L = Lib("lo")
page("calculadoras/matematicas-avanzadas/calculadora-de-logaritmos", MAT,
     slug="calculadora-de-logaritmos", name="Calculadora de Logaritmos",
     page_title="Calculadora de Logaritmos: log, ln y Cualquier Base | Calculadora Científica",
     desc="Calculá logaritmos en cualquier base (log₁₀, ln, log₂ y más) y potencias. Muestra la comprobación y los logaritmos decimal, natural y binario del mismo número. Gratis.",
     og_title="Calculadora de Logaritmos",
     og_desc="Logaritmo en cualquier base, ln, log y potencias, con comprobación. Gratis.",
     schema_desc="Calcula el logaritmo de un número en cualquier base (decimal, natural, binario u otra) mediante el cambio de base, y la potencia inversa b elevado a y, con comprobación del resultado.",
     intro="Elegí si querés calcular un logaritmo (¿a qué exponente hay que elevar la base?) o una potencia. Funciona con cualquier base, incluidos el logaritmo decimal (base 10), el natural (base e) y el binario (base 2).",
     form_html=L.form([
         L.sel("mode", "Qué querés calcular", [("log", "Logaritmo: ¿a qué exponente elevo la base?"), ("pot", "Potencia: la base elevada a un exponente")]),
         L.num("base", "Base", "Ej: 10", value="10"),
         L.num("x", "Número", "Ej: 1000", when="mode=log"),
         L.num("y", "Exponente", "Ej: 3", rule="any", when="mode=pot"),
     ], chips=[("log₂(8)", "mode=log;base=2;x=8"), ("log₁₀(1000)", "mode=log;base=10;x=1000"), ("ln(10)", "mode=log;base=2,718281828459045;x=10"), ("log₃(81)", "mode=log;base=3;x=81"), ("2¹⁰", "mode=pot;base=2;y=10")],
         note="Para el logaritmo natural (ln) usá la base e ≈ 2,718281828."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Definición", f'<p {FORMULA}>log_b(x) = y &nbsp;⇔&nbsp; bʸ = x</p><p>El logaritmo en base b de x es el exponente al que hay que elevar b para obtener x. Por ejemplo, log₂(8) = 3 porque 2³ = 8.</p>'),
         ("Cambio de base", f'<p {FORMULA}>log_b(x) = ln(x) / ln(b) = log(x) / log(b)</p><p>Permite calcular cualquier logaritmo con las teclas log o ln de una calculadora común.</p>'),
         ("Propiedades", f'<p {FORMULA}>log(a·b) = log a + log b &nbsp;·&nbsp; log(a/b) = log a − log b &nbsp;·&nbsp; log(aⁿ) = n·log a</p><p>El logaritmo solo existe para números positivos y la base tiene que ser positiva y distinta de 1.</p>'),
     ]),
     related=[("/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/", "Calculadora Científica Online"), ("/calculadoras/matematicas-avanzadas/graficador-de-funciones/", "Graficador de Funciones"),
              ("/calculadoras/quimica/calculadora-de-ph/", "Calculadora de pH")],
     guide=("/guias/logaritmos-que-son-y-como-calcularlos/", "Logaritmos: qué son y cómo calcularlos", "Leé la guía completa: la definición, el cambio de base, las propiedades y ejemplos resueltos."),
     faqs=[("¿Qué es un logaritmo?", "Es el exponente al que hay que elevar una base para obtener un número. log₁₀(1000) = 3 porque 10³ = 1000."),
           ("¿Cómo se calcula un logaritmo en cualquier base?", "Con el cambio de base: log_b(x) = ln(x)/ln(b). Para log₃(81): ln 81 / ln 3 = 4."),
           ("¿Cuál es la diferencia entre log y ln?", "log suele ser el logaritmo decimal (base 10) y ln el natural (base e ≈ 2,718). Se relacionan por ln(x) = 2,3026 · log(x)."),
           ("¿Por qué no existe el logaritmo de 0 ni de un número negativo?", "Porque ninguna potencia de una base positiva da 0 ni un resultado negativo."),
           ("¿Para qué se usan los logaritmos?", "Para trabajar con escalas muy amplias: el pH, los decibeles, la escala de Richter y el interés compuesto, entre otros.")])

# ================================================================ densidad
L = Lib("dn")
MU = [("kg", "kg"), ("g", "g"), ("mg", "mg")]
VU = [("m3", "m³"), ("L", "litros (L)"), ("mL", "mL"), ("cm3", "cm³")]
DU = [("gcm3", "g/cm³ (= kg/L)"), ("kgm3", "kg/m³")]
page("calculadoras/fisica/calculadora-de-densidad", FIS,
     slug="calculadora-de-densidad", name="Calculadora de Densidad, Masa y Volumen",
     page_title="Calculadora de Densidad: ρ = m/V, Masa y Volumen | Calculadora Científica",
     desc="Calculá la densidad, la masa o el volumen de un material con ρ = m/V, en g/cm³, kg/m³, litros y más unidades. Indica si flota o se hunde en agua. Gratis.",
     og_title="Calculadora de Densidad, Masa y Volumen",
     og_desc="Densidad, masa o volumen con conversión de unidades. Gratis.",
     schema_desc="Calcula la densidad de un cuerpo (masa dividida por volumen), o despeja la masa o el volumen, con conversión entre kg, g, mg, m³, L, cm³, g/cm³ y kg/m³, e indica si flota en agua.",
     intro="Elegí qué querés averiguar (densidad, masa o volumen), cargá los otros dos datos con sus unidades y obtenés el resultado convertido a las unidades más usadas. También te dice si el material flota o se hunde en agua.",
     form_html=L.form([
         L.sel("mode", "Qué querés calcular", [("dens", "Densidad (tengo la masa y el volumen)"), ("masa", "Masa (tengo la densidad y el volumen)"), ("vol", "Volumen (tengo la masa y la densidad)")]),
         L.num("m", "Masa", "Ej: 500", when="mode=dens|vol"),
         L.sel("mu", "Unidad de masa", MU, when="mode=dens|vol", value="g"),
         L.num("v", "Volumen", "Ej: 250", when="mode=dens|masa"),
         L.sel("vu", "Unidad de volumen", VU, when="mode=dens|masa", value="cm3"),
         L.num("d", "Densidad", "Ej: 7,87", when="mode=masa|vol"),
         L.sel("du", "Unidad de densidad", DU, when="mode=masa|vol"),
     ], chips=[("500 g en 250 cm³", "mode=dens;m=500;mu=g;v=250;vu=cm3"), ("Masa de 100 cm³ de hierro", "mode=masa;d=7,87;du=gcm3;v=100;vu=cm3"), ("Volumen de 2 kg de aceite", "mode=vol;m=2;mu=kg;d=0,92;du=gcm3")],
         note="Referencias: agua 1 g/cm³ · aluminio 2,70 · hierro 7,87 · cobre 8,96 · oro 19,3 · aceite 0,92."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Fórmula de la densidad", f'<p {FORMULA}>ρ = m / V &nbsp;·&nbsp; m = ρ·V &nbsp;·&nbsp; V = m / ρ</p><p>La densidad es la masa que hay en cada unidad de volumen. En el SI se mide en kg/m³; en el laboratorio se usa g/cm³ (igual a g/mL y a kg/L).</p>'),
         ("Equivalencias", f'<p {FORMULA}>1 g/cm³ = 1 kg/L = 1.000 kg/m³ &nbsp;·&nbsp; 1 L = 1.000 cm³ = 0,001 m³</p><p>El agua tiene una densidad de 1 g/cm³ (1.000 kg/m³): un litro de agua pesa un kilo.</p>'),
         ("Flotar o hundirse", "<p>Un material flota en agua si su densidad es menor que la del agua (1 g/cm³) y se hunde si es mayor. Por eso el aceite (0,92 g/cm³) flota y el hierro (7,87 g/cm³) se hunde.</p>"),
     ]),
     related=[("/calculadoras/ingenieria/conversor-de-unidades/", "Conversor de Unidades"), ("/calculadoras/quimica/calculadora-de-molaridad/", "Calculadora de Molaridad"),
              ("/calculadoras/matematicas-avanzadas/calculadora-de-areas-y-volumenes/", "Áreas y Volúmenes")],
     guide=("/guias/como-calcular-la-densidad/", "Cómo calcular la densidad", "Leé la guía completa: la fórmula, las unidades, una tabla de materiales y ejemplos resueltos."),
     faqs=[("¿Cómo se calcula la densidad?", "Dividiendo la masa por el volumen: ρ = m/V. Un bloque de 500 g que ocupa 250 cm³ tiene una densidad de 2 g/cm³."),
           ("¿Cómo se calcula la masa a partir de la densidad?", "Multiplicando la densidad por el volumen: m = ρ·V. 100 cm³ de hierro (7,87 g/cm³) pesan 787 g."),
           ("¿Cuál es la densidad del agua?", "1 g/cm³, o sea 1.000 kg/m³ (a unos 4 °C). Un litro de agua tiene una masa de 1 kg."),
           ("¿Cómo paso de g/cm³ a kg/m³?", "Multiplicando por 1.000: 2,7 g/cm³ = 2.700 kg/m³."),
           ("¿Cómo sé si un objeto flota?", "Si su densidad media es menor que la del líquido, flota; si es mayor, se hunde.")])

# ================================================================ calor específico
L = Lib("ce")
page("calculadoras/fisica/calculadora-de-calor-especifico", FIS,
     slug="calculadora-de-calor-especifico", name="Calculadora de Calor Específico y Calorimetría",
     page_title="Calculadora de Calor Específico: Q = m·c·ΔT (Calorimetría) | Calculadora Científica",
     desc="Calculá el calor intercambiado, el calor específico, la masa o la variación de temperatura con Q = m·c·ΔT. Resultado en joules, kJ y calorías. Gratis.",
     og_title="Calculadora de Calor Específico y Calorimetría",
     og_desc="Q = m·c·ΔT: calor, calor específico, masa o variación de temperatura. Gratis.",
     schema_desc="Resuelve la ecuación fundamental de la calorimetría Q = m·c·ΔT despejando el calor intercambiado, el calor específico, la masa o la variación de temperatura, con resultados en J, kJ, cal y kcal.",
     intro="Elegí la incógnita de Q = m·c·ΔT, cargá los otros tres datos y obtenés el resultado con el calor expresado en joules, kilojoules, calorías y kilocalorías. Incluye una tabla de calores específicos de materiales comunes.",
     form_html=L.form([
         L.sel("mode", "Qué querés calcular", [("q", "Calor intercambiado Q"), ("c", "Calor específico c"), ("m", "Masa m"), ("dt", "Variación de temperatura ΔT")]),
         L.num("q", "Calor Q (J) — positivo si lo absorbe, negativo si lo cede", "Ej: 251160", rule="any", when="mode=c|m|dt"),
         L.num("m", "Masa m (g)", "Ej: 1000", when="mode=q|c|dt"),
         L.num("c", "Calor específico c (J/g·°C)", "Ej: 4,186", when="mode=q|m|dt", hint="Agua 4,186 · hielo 2,09 · vapor 2,01 · aluminio 0,897 · hierro 0,449 · cobre 0,385 · plomo 0,129"),
         L.num("dT", "Variación de temperatura ΔT (°C) — final menos inicial", "Ej: 60", rule="any", when="mode=q|c|m"),
     ], chips=[("1 kg de agua, +60 °C", "mode=q;m=1000;c=4,186;dT=60"), ("500 g de aluminio, +80 °C", "mode=q;m=500;c=0,897;dT=80"), ("200 g de cobre que se enfría 50 °C", "mode=q;m=200;c=0,385;dT=-50"), ("¿Qué material es? (c)", "mode=c;q=3850;m=200;dT=50")],
         note="Valores para sustancias sin cambio de estado. 1 cal = 4,184 J."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Ecuación de la calorimetría", f'<p {FORMULA}>Q = m · c · ΔT</p><p>El calor necesario para cambiar la temperatura de un cuerpo es proporcional a su masa, a su calor específico y a la variación de temperatura. Si Q es positivo el cuerpo absorbe calor y se calienta; si es negativo, lo cede y se enfría.</p>'),
         ("Calor específico", f'<p {FORMULA}>c = Q / (m · ΔT)</p><p>Es la energía que hace falta para subir 1 °C la temperatura de 1 g de una sustancia. El agua tiene un calor específico alto (4,186 J/g·°C): tarda mucho en calentarse y en enfriarse.</p>'),
         ("Unidades", f'<p {FORMULA}>1 cal = 4,184 J &nbsp;·&nbsp; 1 kcal = 4.184 J &nbsp;·&nbsp; 1 °C de variación = 1 K de variación</p><p>Con la masa en gramos, c va en J/(g·°C); con la masa en kilogramos, en J/(kg·°C) (4.186 para el agua).</p>'),
     ]),
     related=[("/calculadoras/fisica/trabajo-y-potencia/", "Trabajo y Potencia"), ("/calculadoras/fisica/energia-cinetica-y-potencial/", "Energía Cinética y Potencial"),
              ("/calculadoras/ingenieria/conversor-de-temperatura/", "Conversor de Temperatura")],
     guide=("/guias/calor-especifico-y-calorimetria/", "Calor específico y calorimetría", "Leé la guía completa: la fórmula, una tabla de materiales y ejemplos resueltos de calentamiento y mezclas."),
     faqs=[("¿Cómo se calcula el calor necesario para calentar agua?", "Con Q = m·c·ΔT. Para calentar 1 kg de agua de 20 °C a 80 °C: 1000 g × 4,186 J/g·°C × 60 °C = 251.160 J (unas 60 kcal)."),
           ("¿Qué es el calor específico?", "La cantidad de energía que absorbe 1 g de una sustancia para subir 1 °C su temperatura. Cada material tiene el suyo."),
           ("¿Por qué el agua tarda tanto en calentarse?", "Porque su calor específico es muy alto (4,186 J/g·°C), unas 10 veces el del hierro o el cobre."),
           ("¿La fórmula sirve si hay cambio de estado?", "No: durante la fusión o la ebullición la temperatura no cambia y se usa el calor latente (Q = m·L)."),
           ("¿Cómo paso de joules a calorías?", "Dividiendo por 4,184: 251.160 J ÷ 4,184 ≈ 60.029 cal.")])

# ================================================================ movimiento circular
L = Lib("mc")
page("calculadoras/fisica/calculadora-de-movimiento-circular", FIS,
     slug="calculadora-de-movimiento-circular", name="Calculadora de Movimiento Circular Uniforme",
     page_title="Calculadora de Movimiento Circular Uniforme (MCU): Período, Frecuencia y Velocidad | Calculadora Científica",
     desc="Calculá el período, la frecuencia, las rpm, la velocidad angular y lineal y la aceleración centrípeta de un movimiento circular uniforme a partir del radio y un dato. Gratis.",
     og_title="Calculadora de Movimiento Circular Uniforme",
     og_desc="Período, frecuencia, rpm, velocidad angular y lineal y aceleración centrípeta. Gratis.",
     schema_desc="Calcula todas las magnitudes del movimiento circular uniforme (período, frecuencia, rpm, velocidad angular, velocidad lineal y aceleración centrípeta) a partir del radio y de un dato conocido.",
     intro="Ingresá el radio de la circunferencia y un dato del movimiento (período, frecuencia, rpm, velocidad lineal o velocidad angular). Obtenés todas las demás magnitudes y la aceleración centrípeta.",
     form_html=L.form([
         L.num("r", "Radio r (m)", "Ej: 0,5"),
         L.sel("mode", "Dato que conocés", [("T", "Período T (s por vuelta)"), ("f", "Frecuencia f (Hz = vueltas por segundo)"), ("rpm", "Revoluciones por minuto (rpm)"), ("v", "Velocidad lineal v (m/s)"), ("w", "Velocidad angular ω (rad/s)")]),
         L.num("T", "Período T (s)", "Ej: 2", when="mode=T"),
         L.num("f", "Frecuencia f (Hz)", "Ej: 0,5", when="mode=f"),
         L.num("rpm", "Revoluciones por minuto", "Ej: 120", when="mode=rpm"),
         L.num("v", "Velocidad lineal v (m/s)", "Ej: 20", when="mode=v"),
         L.num("w", "Velocidad angular ω (rad/s)", "Ej: 3,14", when="mode=w"),
     ], chips=[("r = 0,5 m, T = 2 s", "r=0,5;mode=T;T=2"), ("Rueda de 30 cm a 120 rpm", "r=0,3;mode=rpm;rpm=120"), ("Auto en una curva de 50 m a 20 m/s", "r=50;mode=v;v=20")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Magnitudes del MCU", f'<p {FORMULA}>T = 1/f &nbsp;·&nbsp; ω = 2π/T = 2πf &nbsp;·&nbsp; v = ω·r</p><p>El período es el tiempo de una vuelta; la frecuencia, la cantidad de vueltas por segundo; la velocidad angular, el ángulo (en radianes) que se recorre por segundo; y la lineal, la rapidez a lo largo de la circunferencia.</p>'),
         ("Aceleración centrípeta", f'<p {FORMULA}>a = v² / r = ω² · r</p><p>Aunque la rapidez sea constante, la dirección cambia todo el tiempo: por eso hay una aceleración dirigida hacia el centro. La fuerza centrípeta es F = m·a.</p>'),
         ("Conversión de rpm", f'<p {FORMULA}>1 rpm = 1/60 Hz = 0,1047 rad/s</p><p>120 rpm equivalen a 2 vueltas por segundo (2 Hz).</p>'),
     ]),
     related=[("/calculadoras/fisica/segunda-ley-de-newton/", "Segunda Ley de Newton"), ("/calculadoras/fisica/cinematica-mru-mrua/", "Cinemática (MRU / MRUA)"),
              ("/calculadoras/matematicas-avanzadas/resolucion-de-triangulos/", "Resolución de Triángulos")],
     guide=("/guias/movimiento-circular-uniforme-explicado/", "Movimiento circular uniforme explicado", "Leé la guía completa: período, frecuencia, velocidad angular y lineal, aceleración centrípeta y ejemplos."),
     faqs=[("¿Qué es el movimiento circular uniforme?", "Es el de un objeto que recorre una circunferencia con rapidez constante. Aunque la rapidez no cambie, la dirección sí, por eso hay aceleración."),
           ("¿Cómo se calcula la velocidad lineal?", "v = ω·r, o también v = 2π·r/T. Una rueda de 0,3 m de radio a 120 rpm tiene ω = 12,57 rad/s y v ≈ 3,77 m/s (13,6 km/h)."),
           ("¿Qué es la aceleración centrípeta?", "La aceleración dirigida al centro que mantiene al cuerpo en la circunferencia: a = v²/r. Un auto a 20 m/s en una curva de 50 m tiene a = 8 m/s²."),
           ("¿Cómo paso de rpm a rad/s?", "Multiplicando por 2π y dividiendo por 60: 120 rpm = 12,57 rad/s."),
           ("¿Cuál es la diferencia entre período y frecuencia?", "Son inversos: el período es el tiempo de una vuelta (T) y la frecuencia, las vueltas por segundo (f = 1/T).")])

# ================================================================ leyes de los gases
L = Lib("gl")
PU = [("atm", "atm"), ("kPa", "kPa"), ("mmHg", "mmHg"), ("bar", "bar"), ("psi", "psi")]
GV = [("L", "litros (L)"), ("mL", "mL"), ("m3", "m³"), ("cm3", "cm³")]
page("calculadoras/quimica/leyes-de-los-gases", QUI,
     slug="leyes-de-los-gases", name="Calculadora de las Leyes de los Gases: Boyle, Charles y Gay-Lussac",
     page_title="Calculadora de Leyes de los Gases: Boyle, Charles y Gay-Lussac | Calculadora Científica",
     desc="Calculá la presión, el volumen o la temperatura final de un gas con la ley combinada P₁V₁/T₁ = P₂V₂/T₂. Detecta si aplica Boyle, Charles o Gay-Lussac. Gratis.",
     og_title="Calculadora de Leyes de los Gases",
     og_desc="Boyle, Charles, Gay-Lussac y ley combinada: P, V o T final. Gratis.",
     schema_desc="Resuelve la ley combinada de los gases (P1·V1/T1 = P2·V2/T2) para hallar la presión, el volumen o la temperatura final, e identifica si corresponde la ley de Boyle, de Charles o de Gay-Lussac.",
     intro="Cargá el estado inicial del gas (presión, volumen y temperatura) y los datos conocidos del estado final: la calculadora despeja la incógnita y te dice si se trata de la ley de Boyle, de Charles, de Gay-Lussac o de la ley combinada.",
     form_html=L.form([
         L.sel("mode", "Qué querés calcular", [("p2", "Presión final P₂"), ("v2", "Volumen final V₂"), ("t2", "Temperatura final T₂")]),
         L.sel("pu", "Unidad de presión", PU),
         L.sel("vu", "Unidad de volumen", GV),
         L.sel("tu", "Unidad de temperatura", [("C", "grados Celsius (°C)"), ("K", "kelvin (K)")]),
         L.num("p1", "Presión inicial P₁", "Ej: 1"),
         L.num("v1", "Volumen inicial V₁", "Ej: 10"),
         L.num("t1", "Temperatura inicial T₁", "Ej: 25", rule="any"),
         L.num("p2", "Presión final P₂", "Ej: 2", when="mode=v2|t2"),
         L.num("v2", "Volumen final V₂", "Ej: 5", when="mode=p2|t2"),
         L.num("t2", "Temperatura final T₂", "Ej: 25", rule="any", when="mode=p2|v2"),
     ], chips=[("Boyle: se comprime de 10 L a 5 L", "mode=p2;pu=atm;vu=L;tu=C;p1=1;v1=10;t1=25;v2=5;t2=25"), ("Charles: un globo se calienta de 20 a 80 °C", "mode=v2;pu=atm;vu=L;tu=C;p1=1;v1=2;t1=20;p2=1;t2=80"), ("Gay-Lussac: un envase rígido pasa de 20 a 100 °C", "mode=p2;pu=atm;vu=L;tu=C;p1=2;v1=5;t1=20;v2=5;t2=100")],
         note="Cantidad de gas constante. La temperatura se pasa a kelvin automáticamente. Usá la misma unidad de presión y de volumen en los dos estados."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Ley combinada", f'<p {FORMULA}>P₁·V₁ / T₁ = P₂·V₂ / T₂</p><p>Relaciona los tres estados del gas cuando la cantidad de materia no cambia. La temperatura tiene que estar en kelvin (K = °C + 273,15).</p>'),
         ("Casos particulares", f'<p {FORMULA}>Boyle (T constante): P₁V₁ = P₂V₂ &nbsp;·&nbsp; Charles (P constante): V₁/T₁ = V₂/T₂ &nbsp;·&nbsp; Gay-Lussac (V constante): P₁/T₁ = P₂/T₂</p><p>Cada una sale de la ley combinada al mantener una variable fija.</p>'),
         ("Diferencia con la ecuación de los gases ideales", "<p>Acá se compara el mismo gas en dos estados distintos, sin necesidad de conocer la cantidad de moles. Si querés calcular con moles (PV = nRT), usá la calculadora de gases ideales.</p>"),
     ]),
     related=[("/calculadoras/quimica/calculadora-de-gases-ideales/", "Gases Ideales (PV = nRT)"), ("/calculadoras/ingenieria/conversor-de-temperatura/", "Conversor de Temperatura"),
              ("/calculadoras/quimica/calculadora-de-moles/", "Calculadora de Moles")],
     guide=("/guias/leyes-de-boyle-charles-y-gay-lussac/", "Leyes de Boyle, Charles y Gay-Lussac", "Leé la guía completa: cada ley, cuándo se usa, la ley combinada y ejemplos resueltos."),
     faqs=[("¿Qué dice la ley de Boyle?", "A temperatura constante, la presión y el volumen de un gas son inversamente proporcionales: P₁V₁ = P₂V₂. Si el volumen se reduce a la mitad, la presión se duplica."),
           ("¿Qué dice la ley de Charles?", "A presión constante, el volumen es proporcional a la temperatura absoluta: V₁/T₁ = V₂/T₂. Un globo de 2 L a 20 °C pasa a unos 2,41 L a 80 °C."),
           ("¿Qué dice la ley de Gay-Lussac?", "A volumen constante, la presión es proporcional a la temperatura absoluta: P₁/T₁ = P₂/T₂. Un envase rígido con 2 atm a 20 °C llega a unas 2,55 atm a 100 °C."),
           ("¿Por qué hay que usar kelvin?", "Porque las proporcionalidades valen con la temperatura absoluta. Con grados Celsius los resultados serían incorrectos."),
           ("¿Cuándo se usa la ley combinada?", "Cuando cambian dos o tres magnitudes a la vez y la cantidad de gas es constante.")])

# ================================================================ concentración ppm
L = Lib("cn")
page("calculadoras/quimica/calculadora-de-concentracion-ppm", QUI,
     slug="calculadora-de-concentracion-ppm", name="Calculadora de Concentración: ppm, mg/L y Porcentaje",
     page_title="Calculadora de ppm: Concentración en mg/L, g/L y Porcentaje | Calculadora Científica",
     desc="Calculá la concentración de una solución en ppm (mg/L), g/L y % m/v, convertí ppm a porcentaje o hallá cuánto soluto agregar para una ppm objetivo. Gratis.",
     og_title="Calculadora de ppm y Concentración",
     og_desc="ppm, mg/L, g/L y % m/v: conversiones y cuánto soluto necesitás. Gratis.",
     schema_desc="Calcula la concentración de una solución diluida en partes por millón (ppm, mg/L), g/L y porcentaje masa/volumen, convierte entre estas unidades y calcula la masa de soluto necesaria para una concentración objetivo.",
     intro="Elegí qué necesitás: calcular la concentración a partir del soluto y el volumen, convertir una cantidad en ppm a otras unidades, o saber cuánto soluto agregar para lograr una concentración en ppm. Pensada para soluciones diluidas en agua.",
     form_html=L.form([
         L.sel("mode", "Qué necesitás", [("conc", "Calcular la concentración (tengo soluto y volumen)"), ("ppm", "Convertir ppm a otras unidades"), ("masa", "Calcular cuánto soluto agregar (tengo la ppm objetivo)")]),
         L.num("s", "Cantidad de soluto", "Ej: 5", when="mode=conc"),
         L.sel("su", "Unidad del soluto", [("mg", "mg"), ("g", "g"), ("kg", "kg")], when="mode=conc", value="g"),
         L.num("p", "Concentración (ppm)", "Ej: 50", when="mode=ppm|masa"),
         L.num("vol", "Volumen de la solución", "Ej: 2", when="mode=conc|masa"),
         L.sel("vu", "Unidad del volumen", [("L", "litros (L)"), ("mL", "mL")], when="mode=conc|masa"),
     ], chips=[("5 g en 2 L", "mode=conc;s=5;su=g;vol=2;vu=L"), ("1.000 ppm", "mode=ppm;p=1000"), ("50 ppm en 20 L", "mode=masa;p=50;vol=20;vu=L")],
         note="En agua diluida, 1 ppm = 1 mg/L = 1 µg/mL. Para soluciones concentradas o con otra densidad, usá molaridad."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Qué es una ppm", f'<p {FORMULA}>1 ppm = 1 mg de soluto / 1 L de solución = 1 mg/kg</p><p>"Partes por millón": una parte de soluto cada millón de partes de solución. En agua diluida (1 L ≈ 1 kg) equivale a miligramos por litro.</p>'),
         ("Conversiones", f'<p {FORMULA}>1 % m/v = 10 g/L = 10.000 ppm &nbsp;·&nbsp; 1 g/L = 1.000 ppm &nbsp;·&nbsp; 1.000 ppm = 0,1 %</p><p>El porcentaje masa/volumen indica los gramos de soluto cada 100 mL de solución.</p>'),
         ("Soluto necesario", f'<p {FORMULA}>masa (mg) = ppm × volumen (L)</p><p>Para preparar 20 L con 50 ppm hacen falta 50 × 20 = 1.000 mg = 1 g de soluto.</p>'),
     ]),
     related=[("/calculadoras/quimica/calculadora-de-molaridad/", "Calculadora de Molaridad"), ("/calculadoras/quimica/calculadora-de-diluciones/", "Calculadora de Diluciones"),
              ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes")],
     guide=("/guias/como-calcular-ppm-y-porcentaje-de-concentracion/", "Cómo calcular ppm y porcentaje de concentración", "Leé la guía completa: qué es una ppm, equivalencias con mg/L y % m/v y ejemplos resueltos."),
     faqs=[("¿Qué significa ppm?", "Partes por millón. En una solución diluida en agua, 1 ppm equivale a 1 mg de soluto por litro de solución."),
           ("¿Cómo paso de ppm a porcentaje?", "Dividiendo por 10.000: 1.000 ppm = 0,1 %. A la inversa, 1 % = 10.000 ppm."),
           ("¿Cómo calculo cuántos mg necesito para una ppm determinada?", "Multiplicando la ppm por los litros: para 50 ppm en 20 L hacen falta 1.000 mg (1 g)."),
           ("¿Cuántas ppm tiene una solución de 5 g en 2 L?", "5 g = 5.000 mg; 5.000 mg ÷ 2 L = 2.500 ppm, o sea 0,25 % m/v."),
           ("¿Es lo mismo ppm que mg/L?", "Solo en soluciones diluidas en agua, donde 1 L pesa aproximadamente 1 kg.")])

# ================================================================ consumo de combustible
L = Lib("cf")
page("calculadoras/vida-diaria/calculadora-de-consumo-de-combustible", VID,
     slug="calculadora-de-consumo-de-combustible", name="Calculadora de Consumo de Combustible y Costo del Viaje",
     page_title="Calculadora de Consumo de Combustible: km/L, L/100 km y Costo de Viaje | Calculadora Científica",
     desc="Calculá el rendimiento de tu auto (km/L y litros cada 100 km), cuántos litros y cuánto cuesta un viaje, y la autonomía del tanque. Gratis y sin registro.",
     og_title="Calculadora de Consumo de Combustible",
     og_desc="Rendimiento en km/L y L/100 km, costo del viaje y autonomía del tanque. Gratis.",
     schema_desc="Calcula el consumo de combustible de un vehículo (km por litro y litros cada 100 km), los litros y el costo de un viaje según el precio del litro, y la autonomía de un tanque.",
     intro="Elegí qué querés saber: el rendimiento de tu auto a partir de lo que recorriste y cargaste, cuánto combustible y plata necesita un viaje, o hasta dónde llegás con un tanque. Todo con el precio del litro que ingreses.",
     form_html=L.form([
         L.sel("mode", "Qué querés calcular", [("consumo", "Mi rendimiento (km/L y L cada 100 km)"), ("viaje", "Litros y costo de un viaje"), ("autonomia", "Autonomía del tanque")]),
         L.num("km", "Kilómetros recorridos", "Ej: 450", when="mode=consumo|viaje"),
         L.num("lit", "Litros cargados", "Ej: 36", when="mode=consumo"),
         L.num("cons", "Consumo (litros cada 100 km)", "Ej: 8", when="mode=viaje|autonomia", hint="Ciudad suele ser más alto que ruta. Si no lo sabés, calculalo en la primera opción."),
         L.num("tank", "Litros en el tanque", "Ej: 50", when="mode=autonomia"),
         L.num("price", "Precio del litro ($) — opcional", "Ej: 1500", opt=True, rule="nonneg"),
     ], chips=[("450 km con 36 L", "mode=consumo;km=450;lit=36;price=1500"), ("Viaje de 300 km a 8 L/100 km", "mode=viaje;km=300;cons=8;price=1500"), ("Tanque de 50 L a 8 L/100 km", "mode=autonomia;tank=50;cons=8;price=1500")],
         note="El consumo real varía con el estilo de manejo, la velocidad, la carga y el tránsito."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Rendimiento y consumo", f'<p {FORMULA}>km/L = kilómetros ÷ litros &nbsp;·&nbsp; L/100 km = 100 ÷ (km/L)</p><p>Son dos formas de decir lo mismo: 12,5 km/L equivalen a 8 litros cada 100 km. A menor L/100 km, más económico es el auto.</p>'),
         ("Costo de un viaje", f'<p {FORMULA}>litros = km × (L/100 km) ÷ 100 &nbsp;·&nbsp; costo = litros × precio del litro</p><p>Para 300 km a 8 L/100 km se necesitan 24 litros; a $1.500 el litro, $36.000.</p>'),
         ("Autonomía", f'<p {FORMULA}>km = litros ÷ (L/100 km) × 100</p><p>Un tanque de 50 litros con un consumo de 8 L/100 km alcanza para unos 625 km.</p>'),
     ]),
     related=[("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes"), ("/calculadoras/vida-diaria/calculadora-de-propina/", "Propina y División de la Cuenta"),
              ("/calculadoras/ingenieria/conversor-de-unidades/", "Conversor de Unidades")],
     guide=("/guias/como-calcular-el-consumo-de-combustible-de-un-auto/", "Cómo calcular el consumo de combustible de un auto", "Leé la guía completa: km/L, L/100 km, costo de un viaje y cómo medir tu consumo real."),
     faqs=[("¿Cómo se calcula el consumo de combustible de un auto?", "Llená el tanque, reiniciá el cuentakilómetros parcial, manejá y volvé a llenar: los litros que entraron son lo que gastaste. Consumo = litros ÷ km × 100."),
           ("¿Cómo paso de km/L a L/100 km?", "Dividiendo 100 por el rendimiento: 12,5 km/L = 100 ÷ 12,5 = 8 L/100 km."),
           ("¿Cuánto cuesta un viaje de 300 km?", "Con 8 L/100 km se gastan 24 litros; multiplicalos por el precio del litro. A $1.500, son $36.000."),
           ("¿Cuántos kilómetros hago con un tanque lleno?", "Dividí los litros del tanque por el consumo y multiplicá por 100: 50 L a 8 L/100 km son 625 km."),
           ("¿Por qué mi consumo real es mayor que el del fabricante?", "Porque las cifras oficiales se miden en condiciones ideales; el tránsito, el aire acondicionado, la carga y la velocidad aumentan el gasto.")])
