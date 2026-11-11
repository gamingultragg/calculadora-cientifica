"""
build-batch-7b.py — Lote 7b (motor común): Física (caída libre y tiro oblicuo, trabajo y potencia), Química
(estequiometría y reactivo limitante, balanceo de ecuaciones) e Ingeniería/electrónica (código de colores de
resistencias, divisor de tensión, resistencia para LED). Páginas y guías en un solo script.
Generación de una sola vez: después, el HTML es la fuente de verdad.
"""
from spec_lib import (ENGINE, FORMULA, Lib, S, calc_page, g_formula, g_h2, g_p, g_steps, g_table, g_ul, guide_page, help_blocks,
                      write_guide, write_page)

FIS = dict(cat_slug="fisica", cat_label="Física")
QUI = dict(cat_slug="quimica", cat_label="Química")
ING = dict(cat_slug="ingenieria", cat_label="Ingeniería")


def page(rel, cat, **kw):
    write_page(rel, calc_page(pre_scripts=ENGINE, **cat, **kw))


def G(slug, name, title, desc, og, headline, intro, quick, cta, sections, faqs, related):
    write_guide(slug, guide_page(slug=slug, name=name, page_title=title, desc=desc, og_desc=og, headline=headline, intro=intro, quick=quick,
                                 cta=cta, body_html="\n\n".join(sections), faqs=faqs, related=related))


# ================================================================ caída libre y tiro oblicuo
L = Lib("tr")
page("calculadoras/fisica/caida-libre-y-tiro-oblicuo", FIS,
     slug="caida-libre-y-tiro-oblicuo", name="Calculadora de Caída Libre y Tiro Oblicuo",
     page_title="Calculadora de Caída Libre y Tiro Oblicuo: Tiempo, Alcance y Altura Máxima | Calculadora Científica",
     desc="Calculá el tiempo y la velocidad de una caída libre, o el alcance, la altura máxima y el tiempo de vuelo de un tiro oblicuo según la velocidad inicial y el ángulo. Gratis.",
     og_title="Calculadora de Caída Libre y Tiro Oblicuo",
     og_desc="Tiempo de caída, alcance, altura máxima y tiempo de vuelo. Gratis.",
     schema_desc="Calcula el tiempo y la velocidad de impacto de una caída libre, y el alcance, la altura máxima, el tiempo de vuelo y la velocidad de llegada de un tiro oblicuo, sin rozamiento del aire.",
     intro="Elegí el movimiento: caída libre desde una altura o tiro oblicuo con una velocidad y un ángulo. Obtenés los tiempos, el alcance, la altura máxima y la velocidad de llegada, sin rozamiento del aire.",
     form_html=L.form([
         L.sel("mode", "Movimiento", [("caida", "Caída libre (se suelta desde una altura)"), ("tiro", "Tiro oblicuo (con velocidad y ángulo)")]),
         L.num("height", "Altura de la que cae (m)", "Ej: 20", when="mode=caida"),
         L.num("v0", "Velocidad inicial (m/s)", "Ej: 20", when="mode=tiro"),
         L.num("angle", "Ángulo con la horizontal (°)", "Ej: 45", rule="nonneg", when="mode=tiro"),
         L.num("h0", "Altura inicial (m) — opcional", "0", opt=True, default=0, rule="nonneg", when="mode=tiro"),
         L.num("g", "Gravedad (m/s²)", "9,81", opt=True, default=9.81, value="9,81"),
     ], chips=[("Caída desde 20 m", "mode=caida;height=20;g=9,81"), ("Tiro a 20 m/s y 45°", "mode=tiro;v0=20;angle=45;h0=0;g=9,81"), ("Lanzamiento horizontal desde 20 m", "mode=tiro;v0=10;angle=0;h0=20;g=9,81")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Caída libre", f'<p {FORMULA}>t = √(2·h / g) &nbsp;·&nbsp; v = g·t = √(2·g·h)</p><p>Un cuerpo que cae desde el reposo, sin rozamiento, tarda lo mismo sea cual sea su masa. Desde 20 m tarda 2,02 s y llega a 19,8 m/s (71 km/h).</p>'),
         ("Tiro oblicuo", f'<p {FORMULA}>vₓ = v₀·cos θ &nbsp;·&nbsp; v_y = v₀·sen θ &nbsp;·&nbsp; alcance = vₓ·t</p><p>El movimiento se separa en horizontal (velocidad constante) y vertical (aceleración g hacia abajo). El tiempo de vuelo sale de que la altura final es 0; la altura máxima, de que v_y se anula arriba.</p>'),
         ("Alcance máximo", f'<p {FORMULA}>R = v₀²·sen(2θ) / g (desde el suelo)</p><p>Es máximo con 45°. Dos ángulos complementarios (30° y 60°, por ejemplo) dan el mismo alcance.</p>'),
     ]),
     related=[("/calculadoras/fisica/cinematica-mru-mrua/", "Cinemática (MRU / MRUA)"), ("/calculadoras/fisica/energia-cinetica-y-potencial/", "Energía Cinética y Potencial"),
              ("/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/", "Calculadora Científica Online")],
     guide=("/guias/caida-libre-y-tiro-oblicuo-explicados/", "Caída libre y tiro oblicuo explicados", "Leé la guía completa: las fórmulas, cómo descomponer el movimiento y ejemplos resueltos."),
     faqs=[("¿Cuánto tarda en caer un objeto desde 20 metros?", "t = √(2·20/9,81) = 2,02 s, y llega con una velocidad de 19,8 m/s."),
           ("¿Cómo se calcula el alcance de un tiro oblicuo?", "alcance = v₀·cos θ × tiempo de vuelo. Desde el suelo, R = v₀²·sen(2θ)/g: con 20 m/s y 45°, 40,8 m."),
           ("¿Con qué ángulo se llega más lejos?", "Con 45° (desde el suelo y sin rozamiento)."),
           ("¿Influye la masa en la caída?", "No, sin rozamiento del aire todos los cuerpos caen igual."),
           ("¿Considera la resistencia del aire?", "No: es un modelo ideal. Para objetos livianos o muy rápidos, el aire cambia bastante el resultado.")])

# ================================================================ trabajo y potencia
L = Lib("wp")
page("calculadoras/fisica/trabajo-y-potencia", FIS,
     slug="trabajo-y-potencia", name="Calculadora de Trabajo y Potencia",
     page_title="Calculadora de Trabajo y Potencia: W = F·d·cos θ y P = W/t | Calculadora Científica",
     desc="Calculá el trabajo de una fuerza (W = F·d·cos θ) y la potencia (P = W/t) en joules, watts, kW, CV y HP. Con fórmulas y ejemplos. Gratis.",
     og_title="Calculadora de Trabajo y Potencia",
     og_desc="Trabajo en joules y potencia en W, kW, CV y HP. Gratis.",
     schema_desc="Calcula el trabajo mecánico de una fuerza (W = F·d·cos θ) y la potencia desarrollada (P = W/t), con equivalencias en watts, kilowatts, caballos de vapor y horsepower.",
     intro="Ingresá la fuerza, la distancia y el ángulo entre ambas: obtenés el trabajo en joules. Si agregás el tiempo, calcula también la potencia en watts, kilowatts, CV y HP.",
     form_html=L.form([
         L.num("force", "Fuerza (N)", "Ej: 100"),
         L.num("distance", "Distancia recorrida (m)", "Ej: 5"),
         L.num("angle", "Ángulo entre la fuerza y el desplazamiento (°)", "0", opt=True, default=0, rule="nonneg", value="0", hint="0° si la fuerza empuja en la dirección del movimiento; 90° si es perpendicular (el trabajo es nulo)."),
         L.num("time", "Tiempo empleado (s) — opcional", "Ej: 10", opt=True),
     ], chips=[("100 N durante 5 m en 10 s", "force=100;distance=5;angle=0;time=10"), ("Con ángulo de 60°", "force=100;distance=5;angle=60;time=10"), ("Subir 20 kg a 3 m (196,2 N)", "force=196,2;distance=3;angle=0;time=10")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Trabajo", f'<p {FORMULA}>W = F · d · cos θ</p><p>Se mide en joules (1 J = 1 N·m). Solo trabaja la componente de la fuerza paralela al desplazamiento: con θ = 90° el trabajo es cero (por ejemplo, el peso de un objeto que se mueve en horizontal).</p>'),
         ("Potencia", f'<p {FORMULA}>P = W / t</p><p>Es la rapidez con la que se hace el trabajo: 1 W = 1 J/s. Equivalencias: 1 kW = 1000 W; 1 CV = 735,5 W; 1 HP = 745,7 W.</p>'),
         ("Trabajo negativo", "<p>Si la fuerza apunta contra el movimiento (θ entre 90° y 180°), el trabajo es negativo: la fuerza le saca energía al cuerpo, como el rozamiento al frenar.</p>"),
     ]),
     related=[("/calculadoras/fisica/energia-cinetica-y-potencial/", "Energía Cinética y Potencial"), ("/calculadoras/fisica/segunda-ley-de-newton/", "Segunda Ley de Newton"),
              ("/calculadoras/hogar-y-construccion/calculadora-de-consumo-electrico/", "Calculadora de Consumo Eléctrico")],
     guide=("/guias/trabajo-y-potencia-mecanica/", "Trabajo y potencia mecánica", "Leé la guía completa: las fórmulas, las unidades y ejemplos con joules, watts y caballos de fuerza."),
     faqs=[("¿Cómo se calcula el trabajo?", "W = F·d·cos θ. Con 100 N durante 5 m en la misma dirección: 500 J."),
           ("¿Cómo se calcula la potencia?", "P = W/t: 500 J en 10 s son 50 W."),
           ("¿Cuántos watts tiene un caballo de fuerza?", "1 HP = 745,7 W y 1 CV = 735,5 W."),
           ("¿Cuándo el trabajo es cero?", "Cuando no hay desplazamiento o la fuerza es perpendicular al movimiento (θ = 90°)."),
           ("¿Cómo calculo el trabajo de levantar un objeto?", "La fuerza es el peso (m·g) y la distancia, la altura: levantar 20 kg a 3 m requiere 20 × 9,81 × 3 = 588,6 J.")])

# ================================================================ estequiometría
L = Lib("st")
page("calculadoras/quimica/estequiometria-y-reactivo-limitante", QUI,
     slug="estequiometria-y-reactivo-limitante", name="Calculadora de Estequiometría y Reactivo Limitante",
     page_title="Calculadora de Estequiometría y Reactivo Limitante: Gramos, Moles y Rendimiento | Calculadora Científica",
     desc="Calculá cuántos gramos de producto se obtienen a partir de un reactivo, o cuál es el reactivo limitante y cuánto sobra, con rendimiento porcentual. Gratis y con ejemplos.",
     og_title="Calculadora de Estequiometría y Reactivo Limitante",
     og_desc="Gramos de producto, reactivo limitante y exceso. Gratis.",
     schema_desc="Calcula la masa de producto de una reacción química a partir de la masa de un reactivo y los coeficientes de la ecuación balanceada, o determina el reactivo limitante y el exceso de otro, con rendimiento porcentual.",
     intro="Con la ecuación balanceada, cargá los coeficientes, las masas y las masas molares: obtenés los gramos de producto, o el reactivo limitante y cuánto reactivo sobra.",
     form_html=L.form([
         L.sel("mode", "¿Qué querés calcular?", [("producto", "Masa de producto a partir de un reactivo"), ("limitante", "Reactivo limitante con dos reactivos")]),
         L.num("massA", "Masa del reactivo A (g)", "Ej: 28"),
         L.num("mA", "Masa molar de A (g/mol)", "Ej: 28"),
         L.num("cA", "Coeficiente de A en la ecuación", "Ej: 1", rule="int"),
         L.num("massB", "Masa del reactivo B (g)", "Ej: 10", when="mode=limitante"),
         L.num("mB", "Masa molar de B (g/mol)", "Ej: 2,016", when="mode=limitante"),
         L.num("cB", "Coeficiente de B en la ecuación", "Ej: 3", rule="int", when="mode=limitante"),
         L.num("cP", "Coeficiente del producto", "Ej: 2", rule="int"),
         L.num("mP", "Masa molar del producto (g/mol)", "Ej: 17,03"),
         L.num("yield", "Rendimiento (%) — opcional", "100", opt=True, default=100, rule="nonneg", when="mode=producto"),
     ], chips=[("N₂ + 3 H₂ → 2 NH₃ (desde 28 g de N₂)", "mode=producto;massA=28;mA=28;cA=1;cP=2;mP=17,03;yield=100"), ("Reactivo limitante con 28 g de N₂ y 10 g de H₂", "mode=limitante;massA=28;mA=28;cA=1;massB=10;mB=2,016;cB=3;cP=2;mP=17,03")],
         note="Antes de usar esta calculadora la ecuación tiene que estar balanceada: si no lo está, usá el balanceador de ecuaciones del sitio."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("La relación estequiométrica", f'<p {FORMULA}>n(B) = n(A) · coef(B) / coef(A)</p><p>Los coeficientes de la ecuación balanceada indican la proporción en moles. En N₂ + 3 H₂ → 2 NH₃, 1 mol de N₂ da 2 mol de NH₃.</p>'),
         ("Pasos", "<p>1) Pasar los gramos a moles (masa / masa molar). 2) Usar la relación de coeficientes para hallar los moles del producto. 3) Pasar a gramos (moles × masa molar).</p>"),
         ("Reactivo limitante", "<p>Es el que se agota primero y determina cuánto producto se forma. Se identifica dividiendo los moles de cada reactivo por su coeficiente: el menor cociente corresponde al limitante. El otro queda en exceso.</p>"),
         ("Rendimiento", f'<p {FORMULA}>rendimiento % = masa real / masa teórica × 100</p><p>La masa teórica es la calculada; la real suele ser menor por pérdidas y reacciones secundarias.</p>'),
     ]),
     related=[("/calculadoras/quimica/calculadora-de-moles/", "Calculadora de Moles"), ("/calculadoras/quimica/calculadora-de-masa-molar/", "Calculadora de Masa Molar"),
              ("/calculadoras/quimica/balanceo-de-ecuaciones-quimicas/", "Balanceo de Ecuaciones Químicas")],
     guide=("/guias/estequiometria-y-reactivo-limitante-paso-a-paso/", "Estequiometría y reactivo limitante paso a paso", "Leé la guía completa: de gramos a moles y de moles a gramos, el reactivo limitante y el rendimiento, con ejemplos."),
     faqs=[("¿Cómo se resuelve un problema de estequiometría?", "Gramos del dato → moles (÷ masa molar) → moles de lo que se busca (por la relación de coeficientes) → gramos (× masa molar)."),
           ("¿Qué es el reactivo limitante?", "El que se consume primero y limita la cantidad de producto. Se halla comparando moles/coeficiente de cada reactivo."),
           ("¿Qué pasa con el reactivo en exceso?", "Sobra sin reaccionar: la calculadora indica cuántos moles y gramos."),
           ("¿Qué es el rendimiento de una reacción?", "La relación entre el producto obtenido en la práctica y el teórico, en porcentaje."),
           ("¿Tengo que balancear antes?", "Sí: los coeficientes tienen que ser los de la ecuación balanceada.")])

# ================================================================ balanceo
L = Lib("bq")
page("calculadoras/quimica/balanceo-de-ecuaciones-quimicas", QUI,
     slug="balanceo-de-ecuaciones-quimicas", name="Balanceador de Ecuaciones Químicas",
     page_title="Balanceador de Ecuaciones Químicas: Balanceo Automático con Verificación | Calculadora Científica",
     desc="Balanceá ecuaciones químicas al instante con el método algebraico: escribí reactivos y productos y obtené los coeficientes, con verificación de átomos. Admite paréntesis e hidratos.",
     og_title="Balanceador de Ecuaciones Químicas",
     og_desc="Escribí la reacción y obtené la ecuación balanceada, con verificación de átomos. Gratis.",
     schema_desc="Balancea ecuaciones químicas automáticamente con el método algebraico (sistema lineal con aritmética exacta), mostrando los coeficientes enteros mínimos y la verificación de átomos de cada elemento.",
     intro="Escribí la reacción con una flecha (H2 + O2 -> H2O) y obtené la ecuación balanceada con los coeficientes enteros más chicos, más la verificación de átomos de cada elemento.",
     form_html=L.form([L.text("equation", "Ecuación química", "Ej: C3H8 + O2 -> CO2 + H2O", hint="Separá las sustancias con +, usá -> o → como flecha y escribí los subíndices como números: Ca(OH)2, Fe2(SO4)3, CuSO4·5H2O.")],
         chips=[("H₂ + O₂ → H₂O", "equation=H2 + O2 -> H2O"), ("Combustión del propano", "equation=C3H8 + O2 -> CO2 + H2O"), ("Oxidación del hierro", "equation=Fe + O2 -> Fe2O3"), ("Neutralización", "equation=Ca(OH)2 + H3PO4 -> Ca3(PO4)2 + H2O"), ("Permanganato", "equation=KMnO4 + HCl -> KCl + MnCl2 + H2O + Cl2")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Ley de conservación de la masa", "<p>En una reacción química no se crean ni se destruyen átomos: de cada elemento tiene que haber la misma cantidad a ambos lados de la flecha. Balancear es elegir los coeficientes que lo logran.</p>"),
         ("Método algebraico", f'<p>Cada sustancia lleva un coeficiente desconocido y cada elemento da una ecuación. Para H₂ + O₂ → H₂O: a·H₂ + b·O₂ = c·H₂O → H: 2a = 2c; O: 2b = c. Con c = 2: a = 2 y b = 1. La calculadora resuelve el sistema con fracciones exactas.</p>'),
         ("Cómo escribir las fórmulas", "<p>Símbolos con mayúscula inicial (Fe, Na, Cl), subíndices como números (H2O) y paréntesis para grupos (Ca(OH)2). Los hidratos se escriben con punto o ·: CuSO4·5H2O. No se admiten cargas iónicas ni estados de agregación.</p>"),
     ]),
     related=[("/calculadoras/quimica/estequiometria-y-reactivo-limitante/", "Estequiometría y Reactivo Limitante"), ("/calculadoras/quimica/calculadora-de-masa-molar/", "Calculadora de Masa Molar"),
              ("/calculadoras/quimica/calculadora-de-moles/", "Calculadora de Moles")],
     guide=("/guias/como-balancear-ecuaciones-quimicas/", "Cómo balancear ecuaciones químicas", "Leé la guía completa: el método por tanteo y el algebraico, con ejemplos resueltos paso a paso."),
     faqs=[("¿Cómo se balancea una ecuación química?", "Se igualan los átomos de cada elemento a ambos lados con coeficientes enteros. Por tanteo o resolviendo un sistema de ecuaciones (método algebraico)."),
           ("¿Cuál es la ecuación balanceada de la combustión del propano?", "C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O."),
           ("¿Para qué sirve balancear?", "Porque los coeficientes dan las proporciones en moles que se usan en estequiometría."),
           ("¿Por qué a veces no se puede balancear?", "Si las fórmulas están mal escritas o una sustancia está en el lado equivocado, no existe solución con coeficientes positivos."),
           ("¿Admite iones o reacciones redox con cargas?", "Esta versión balancea por átomos; las cargas iónicas no están soportadas.")])

# ================================================================ resistencias
COL = [("negro", "Negro", 0), ("marron", "Marrón", 1), ("rojo", "Rojo", 2), ("naranja", "Naranja", 3), ("amarillo", "Amarillo", 4),
       ("verde", "Verde", 5), ("azul", "Azul", 6), ("violeta", "Violeta", 7), ("gris", "Gris", 8), ("blanco", "Blanco", 9)]
DIG = [(k, f"{n} ({d})") for k, n, d in COL]
MUL = [(k, f"{n} (×{'1' + '0' * d if d else '1'})".replace("×1" + "0" * 9, "×1.000.000.000")) for k, n, d in COL] + [("dorado", "Dorado (×0,1)"), ("plateado", "Plateado (×0,01)")]
TOLS = [("marron", "Marrón (±1 %)"), ("rojo", "Rojo (±2 %)"), ("verde", "Verde (±0,5 %)"), ("azul", "Azul (±0,25 %)"), ("violeta", "Violeta (±0,1 %)"), ("gris", "Gris (±0,05 %)"), ("dorado", "Dorado (±5 %)"), ("plateado", "Plateado (±10 %)")]
L = Lib("rc")
page("calculadoras/ingenieria/codigo-de-colores-de-resistencias", ING,
     slug="codigo-de-colores-de-resistencias", name="Calculadora del Código de Colores de Resistencias",
     page_title="Código de Colores de Resistencias: Calculadora de 4 y 5 Bandas | Calculadora Científica",
     desc="Leé el valor de una resistencia por sus bandas de colores (4 o 5 bandas): resistencia en ohms, tolerancia y rango real. Con la tabla del código de colores. Gratis.",
     og_title="Calculadora del Código de Colores de Resistencias",
     og_desc="Valor y tolerancia de una resistencia por sus bandas de colores. Gratis.",
     schema_desc="Calcula el valor en ohms, la tolerancia y el rango real de una resistencia eléctrica a partir de los colores de sus bandas (4 o 5 bandas).",
     intro="Elegí la cantidad de bandas y el color de cada una: obtenés el valor de la resistencia en ohms, kilohms o megohms, su tolerancia y el rango en el que puede estar su valor real.",
     form_html=L.form([
         L.sel("bands", "Cantidad de bandas", [("4", "4 bandas"), ("5", "5 bandas")]),
         L.sel("b1", "1.ª banda (primera cifra)", DIG[1:], value="marron"),
         L.sel("b2", "2.ª banda (segunda cifra)", DIG),
         L.sel("b3", "3.ª banda (tercera cifra)", DIG, when="bands=5"),
         L.sel("mult", "Banda del multiplicador", MUL, value="rojo"),
         L.sel("tol", "Banda de tolerancia", TOLS, value="dorado"),
     ], chips=[("Marrón-negro-rojo-dorado (1 kΩ)", "bands=4;b1=marron;b2=negro;mult=rojo;tol=dorado"), ("Amarillo-violeta-naranja-dorado (47 kΩ)", "bands=4;b1=amarillo;b2=violeta;mult=naranja;tol=dorado"), ("Rojo-rojo-negro-marrón-marrón (2,2 kΩ)", "bands=5;b1=rojo;b2=rojo;b3=negro;mult=marron;tol=marron")],
         note="Leé las bandas desde el extremo donde están más juntas; la de tolerancia (dorada o plateada en las de 4 bandas) queda sola, algo separada."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Cómo se lee", "<p>En una resistencia de 4 bandas, las dos primeras son cifras, la tercera es el multiplicador (potencia de 10) y la cuarta la tolerancia. En las de 5 bandas hay tres cifras. El valor es (cifras) × multiplicador.</p>"),
         ("Tabla de colores", "<p>Negro 0 · Marrón 1 · Rojo 2 · Naranja 3 · Amarillo 4 · Verde 5 · Azul 6 · Violeta 7 · Gris 8 · Blanco 9. Como multiplicador, además: dorado ×0,1 y plateado ×0,01.</p>"),
         ("Tolerancia", "<p>Marrón ±1 % · Rojo ±2 % · Verde ±0,5 % · Azul ±0,25 % · Violeta ±0,1 % · Gris ±0,05 % · Dorado ±5 % · Plateado ±10 %. Una resistencia de 1 kΩ ±5 % puede valer entre 950 Ω y 1050 Ω.</p>"),
     ]),
     related=[("/calculadoras/ingenieria/resistencias-serie-paralelo/", "Resistencias en Serie y Paralelo"), ("/calculadoras/fisica/ley-de-ohm/", "Ley de Ohm"),
              ("/calculadoras/ingenieria/resistencia-para-led/", "Resistencia para LED")],
     guide=("/guias/como-leer-el-codigo-de-colores-de-resistencias/", "Cómo leer el código de colores de resistencias", "Leé la guía completa: la tabla de colores, cómo leer 4 y 5 bandas y ejemplos resueltos."),
     faqs=[("¿Cómo se lee una resistencia de 4 bandas?", "Primera y segunda banda: cifras; tercera: multiplicador; cuarta: tolerancia. Marrón-negro-rojo-dorado = 10 × 100 = 1 kΩ ±5 %."),
           ("¿Cuál es el sentido de lectura?", "Desde el extremo con las bandas más juntas; la banda de tolerancia suele estar separada y ser dorada o plateada."),
           ("¿Cómo se lee una de 5 bandas?", "Tres cifras, el multiplicador y la tolerancia: rojo-rojo-negro-marrón-marrón = 220 × 10 = 2,2 kΩ ±1 %."),
           ("¿Qué significa la tolerancia?", "El margen en el que puede variar el valor real: ±5 % en una de 1 kΩ es de 950 a 1050 Ω."),
           ("¿Cómo recuerdo los colores?", "Siguen el orden del arcoíris con negro y marrón al principio, y gris y blanco al final: 0 a 9.")])

# ================================================================ divisor de tensión
L = Lib("dv")
page("calculadoras/ingenieria/divisor-de-tension", ING,
     slug="divisor-de-tension", name="Calculadora de Divisor de Tensión",
     page_title="Calculadora de Divisor de Tensión: Vout y Resistencia R2 | Calculadora Científica",
     desc="Calculá la tensión de salida de un divisor de tensión resistivo (Vout = Vin·R2/(R1+R2)) o la resistencia R2 necesaria para una tensión deseada. Con corriente y potencia. Gratis.",
     og_title="Calculadora de Divisor de Tensión",
     og_desc="Tensión de salida y resistencias de un divisor de tensión. Gratis.",
     schema_desc="Calcula la tensión de salida de un divisor de tensión resistivo a partir de Vin, R1 y R2, o la resistencia R2 necesaria para obtener una tensión de salida deseada, con la corriente y la potencia del divisor.",
     intro="Elegí si querés la tensión de salida de un divisor de dos resistencias o la resistencia R2 que necesitás para una tensión deseada. También calcula la corriente y la potencia.",
     form_html=L.form([
         L.sel("mode", "¿Qué querés calcular?", [("vout", "Tensión de salida (Vout)"), ("r2", "Resistencia R2 para una Vout deseada")]),
         L.sel("unit", "Unidad de las resistencias", [("ohm", "Ω"), ("k", "kΩ"), ("m", "MΩ")], value="k"),
         L.num("vin", "Tensión de entrada Vin (V)", "Ej: 12"),
         L.num("r1", "Resistencia R1", "Ej: 1"),
         L.num("r2", "Resistencia R2", "Ej: 2", when="mode=vout"),
         L.num("vout", "Tensión de salida deseada (V)", "Ej: 3,3", when="mode=r2"),
     ], chips=[("12 V, R1 = 1 kΩ, R2 = 2 kΩ", "mode=vout;unit=k;vin=12;r1=1;r2=2"), ("De 5 V a 3,3 V con R1 = 1 kΩ", "mode=r2;unit=k;vin=5;r1=1;vout=3,3")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("La fórmula", f'<p {FORMULA}>Vout = Vin · R2 / (R1 + R2)</p><p>Dos resistencias en serie reparten la tensión de entrada en proporción a sus valores: R2 es la que está "del lado" de la salida. Con R1 = 1 kΩ y R2 = 2 kΩ, Vout es los 2/3 de Vin.</p>'),
         ("Despejando R2", f'<p {FORMULA}>R2 = Vout · R1 / (Vin − Vout)</p>'),
         ("Limitaciones", "<p>La fórmula supone que no hay carga conectada a la salida. Si la carga consume corriente, Vout baja: para que el divisor sea estable, la resistencia de carga tiene que ser mucho mayor que R2. Un divisor no sirve para alimentar cargas de potencia.</p>"),
     ]),
     related=[("/calculadoras/fisica/ley-de-ohm/", "Ley de Ohm"), ("/calculadoras/ingenieria/resistencias-serie-paralelo/", "Resistencias en Serie y Paralelo"),
              ("/calculadoras/ingenieria/codigo-de-colores-de-resistencias/", "Código de Colores de Resistencias")],
     guide=("/guias/como-funciona-un-divisor-de-tension/", "Cómo funciona un divisor de tensión", "Leé la guía completa: la fórmula, ejemplos con valores reales y sus limitaciones."),
     faqs=[("¿Cómo se calcula un divisor de tensión?", "Vout = Vin·R2/(R1 + R2). Con 12 V, 1 kΩ y 2 kΩ: 8 V."),
           ("¿Cómo elijo R2 para una tensión deseada?", "R2 = Vout·R1/(Vin − Vout). Para 3,3 V desde 5 V con R1 = 1 kΩ: 1,94 kΩ (usá el valor comercial más cercano)."),
           ("¿Sirve para alimentar un circuito?", "Solo cargas de muy baja corriente: la carga modifica la tensión de salida."),
           ("¿Qué valores de resistencias conviene usar?", "Valores que dejen pasar una corriente baja pero mucho mayor que la que consume la carga: de 1 kΩ a 100 kΩ según el caso."),
           ("¿Qué corriente circula por el divisor?", "I = Vin / (R1 + R2).")])

# ================================================================ LED
L = Lib("le")
page("calculadoras/ingenieria/resistencia-para-led", ING,
     slug="resistencia-para-led", name="Calculadora de Resistencia para LED",
     page_title="Calculadora de Resistencia para LED: Qué Resistencia Usar | Calculadora Científica",
     desc="Calculá la resistencia limitadora para un LED según la tensión de la fuente, la caída del LED y la corriente: valor exacto, valor comercial E12 y potencia. Gratis.",
     og_title="Calculadora de Resistencia para LED",
     og_desc="Qué resistencia poner a un LED, con valor comercial. Gratis.",
     schema_desc="Calcula la resistencia limitadora de corriente para uno o varios LED en serie a partir de la tensión de la fuente, la caída de tensión del LED y la corriente deseada, con el valor comercial de la serie E12 y la potencia disipada.",
     intro="Ingresá la tensión de tu fuente, la caída de tensión del LED y la corriente que querés que circule: obtenés el valor de la resistencia, el valor comercial más cercano y la potencia que disipa.",
     form_html=L.form([
         L.num("vs", "Tensión de la fuente (V)", "Ej: 5"),
         L.num("vf", "Caída de tensión del LED, Vf (V)", "2", value="2", hint="Rojo ≈ 1,8–2,2 V · verde ≈ 2,0–3,0 V · azul y blanco ≈ 3,0–3,4 V."),
         L.num("ma", "Corriente deseada (mA)", "20", value="20", hint="20 mA es la corriente típica de un LED común; con 10 mA brilla menos y dura más."),
         L.num("leds", "LED en serie", "1", opt=True, default=1, rule="int", value="1"),
     ], chips=[("5 V y LED rojo", "vs=5;vf=2;ma=20;leds=1"), ("3,3 V y LED rojo a 10 mA", "vs=3,3;vf=2;ma=10;leds=1"), ("9 V y LED rojo", "vs=9;vf=2;ma=20;leds=1")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("La fórmula", f'<p {FORMULA}>R = (Vfuente − Vf) / I</p><p>El LED no limita la corriente por sí mismo: sin resistencia se quema. La resistencia absorbe la diferencia entre la tensión de la fuente y la del LED. Con 5 V, un LED de 2 V y 20 mA: R = 3 / 0,02 = 150 Ω.</p>'),
         ("Valor comercial", "<p>Las resistencias se fabrican en valores normalizados (serie E12: 100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820…). Se elige el valor igual o inmediatamente mayor, que da un poco menos de corriente y es más seguro para el LED.</p>"),
         ("Potencia", f'<p {FORMULA}>P = (Vfuente − Vf) · I</p><p>Con 3 V y 20 mA son 60 mW, muy por debajo de los ¼ W (250 mW) de una resistencia común.</p>'),
         ("Varios LED en serie", "<p>Se suman las caídas de tensión de todos los LED. La fuente tiene que ser mayor que esa suma.</p>"),
     ]),
     related=[("/calculadoras/fisica/ley-de-ohm/", "Ley de Ohm"), ("/calculadoras/ingenieria/codigo-de-colores-de-resistencias/", "Código de Colores de Resistencias"),
              ("/calculadoras/ingenieria/divisor-de-tension/", "Divisor de Tensión")],
     guide=("/guias/que-resistencia-poner-a-un-led/", "Qué resistencia poner a un LED", "Leé la guía completa: el cálculo, los valores comerciales y cómo conectar varios LED."),
     faqs=[("¿Qué resistencia necesita un LED con 5 V?", "Para un LED rojo (2 V) a 20 mA: (5 − 2)/0,02 = 150 Ω."),
           ("¿Qué pasa si no pongo resistencia?", "Circula demasiada corriente y el LED se quema en poco tiempo."),
           ("¿Qué corriente es segura para un LED?", "La mayoría de los LED comunes soportan 20 mA como máximo; 10 a 15 mA da buen brillo con margen."),
           ("¿Puedo usar un valor mayor al calculado?", "Sí: el LED brillará un poco menos pero estará más protegido. Evitá un valor menor."),
           ("¿Qué potencia debe tener la resistencia?", "P = (Vfuente − Vf)·I; en la mayoría de los casos alcanza con ¼ W.")])

# ================================================================ GUÍAS
G("caida-libre-y-tiro-oblicuo-explicados", "Caída libre y tiro oblicuo explicados",
  "Caída Libre y Tiro Oblicuo: Fórmulas, Alcance y Ejemplos | Calculadora Científica",
  "Fórmulas de caída libre y tiro oblicuo: tiempo, velocidad de impacto, alcance, altura máxima y tiempo de vuelo, cómo descomponer el movimiento y ejemplos resueltos.",
  "Caída libre y tiro oblicuo con fórmulas y ejemplos resueltos.",
  "Caída libre y tiro oblicuo explicados con ejemplos",
  "Soltar una piedra o patear una pelota parecen movimientos distintos, pero se describen con la misma idea: la gravedad actúa solo en vertical. Con eso se resuelve cuánto tarda, hasta dónde llega y qué tan alto sube.",
  "Caída libre: t = √(2h/g) y v = g·t. Tiro oblicuo: se separa en un movimiento horizontal uniforme y uno vertical con aceleración g.",
  ("/calculadoras/fisica/caida-libre-y-tiro-oblicuo/", "Abrir calculadora"),
  [g_h2("1. Caída libre"), g_p("Un cuerpo que se suelta desde el reposo cae con aceleración constante g = 9,81 m/s² (sin rozamiento del aire). La masa no influye."),
   g_formula("h = ½·g·t² &nbsp;→&nbsp; t = √(2h/g) &nbsp;·&nbsp; v = g·t"),
   g_steps(["Un objeto cae desde 20 m", "t = √(2 × 20 / 9,81) = 2,02 s", "v = 9,81 × 2,02 = 19,8 m/s ≈ 71 km/h"]),
   g_h2("2. Tiro oblicuo: dos movimientos en uno"), g_p("Con velocidad inicial v₀ y ángulo θ: la componente horizontal vₓ = v₀·cos θ es constante; la vertical v_y = v₀·sen θ cambia con g."),
   g_h2("3. Ejemplo: 20 m/s a 45° desde el suelo"),
   g_steps(["vₓ = v_y = 20 × cos 45° = 14,14 m/s", "Tiempo hasta el punto más alto: 14,14 / 9,81 = 1,44 s → tiempo total 2,88 s", "Alcance = 14,14 × 2,88 = 40,8 m", "Altura máxima = 14,14² / (2 × 9,81) = 10,2 m"]),
   g_h2("4. El ángulo del alcance máximo"), g_formula("R = v₀² · sen(2θ) / g"), g_p("Es máximo con θ = 45°. Los ángulos complementarios (30° y 60°) dan el mismo alcance, aunque con distinta altura y tiempo de vuelo."),
   g_h2("5. Lanzamiento horizontal desde una altura"), g_steps(["Se lanza a 10 m/s horizontalmente desde 20 m", "Cae como en caída libre: t = 2,02 s", "Alcance = 10 × 2,02 = 20,2 m"]),
   g_h2("6. Lo que el modelo ignora"), g_ul(["La resistencia del aire: en la realidad, el alcance es menor, sobre todo en objetos livianos.", "La rotación de la Tierra y el cambio de g con la altura, irrelevantes a estas escalas."])],
  [("¿Cuánto tarda en caer un objeto desde 20 m?", "2,02 s."), ("¿Con qué ángulo se llega más lejos?", "Con 45°."), ("¿Influye la masa?", "No, sin rozamiento todos los cuerpos caen igual."), ("¿Cómo se calcula el alcance?", "vₓ × tiempo de vuelo; desde el suelo, v₀²·sen(2θ)/g.")],
  [("/calculadoras/fisica/caida-libre-y-tiro-oblicuo/", "Calculadora de Caída Libre y Tiro Oblicuo"), ("/calculadoras/fisica/cinematica-mru-mrua/", "Cinemática (MRU / MRUA)"), ("/guias/formulas-de-mru-y-mrua/", "Guía: fórmulas de MRU y MRUA")])

G("trabajo-y-potencia-mecanica", "Trabajo y potencia mecánica",
  "Trabajo y Potencia en Física: Fórmulas, Unidades y Ejemplos | Calculadora Científica",
  "Qué son el trabajo y la potencia mecánica, sus fórmulas (W = F·d·cos θ y P = W/t), las unidades (joule, watt, CV, HP) y ejemplos resueltos, incluido el trabajo negativo.",
  "Trabajo y potencia: fórmulas, unidades y ejemplos.",
  "Trabajo y potencia mecánica: fórmulas y ejemplos",
  "En física, \"trabajo\" no es esfuerzo: es la energía que una fuerza transfiere al mover algo. Y la potencia dice con qué rapidez se hace ese trabajo.",
  "W = F·d·cos θ (joules) y P = W/t (watts). 1 CV = 735,5 W y 1 HP = 745,7 W.",
  ("/calculadoras/fisica/trabajo-y-potencia/", "Abrir calculadora"),
  [g_h2("1. Trabajo"), g_formula("W = F · d · cos θ"), g_p("θ es el ángulo entre la fuerza y el desplazamiento. Se mide en joules (1 J = 1 N·m)."),
   g_steps(["Empujar con 100 N durante 5 m en la misma dirección: W = 100 × 5 × cos 0° = 500 J", "Con la fuerza a 60° del movimiento: 100 × 5 × cos 60° = 250 J", "Fuerza perpendicular (90°): W = 0"]),
   g_h2("2. Trabajo negativo"), g_p("Si la fuerza va contra el movimiento (θ = 180°), cos θ = −1 y el trabajo es negativo: la fuerza le quita energía al cuerpo, como el rozamiento al frenar."),
   g_h2("3. Potencia"), g_formula("P = W / t"), g_p("Se mide en watts (1 W = 1 J/s). Hacer 500 J de trabajo en 10 s equivale a 50 W."),
   g_table(["Unidad", "Equivale a"], [["1 kW", "1000 W"], ["1 CV (caballo de vapor)", "735,5 W"], ["1 HP (horsepower)", "745,7 W"]]),
   g_h2("4. Ejemplo: levantar una carga"), g_steps(["Subir 20 kg una altura de 3 m: F = m·g = 20 × 9,81 = 196,2 N", "W = 196,2 × 3 = 588,6 J", "Si se hace en 10 s: P = 58,9 W"]),
   g_h2("5. Relación con la energía"), g_p("El trabajo total sobre un cuerpo es igual a la variación de su energía cinética (teorema del trabajo y la energía). Por eso frenar un auto de gran velocidad exige mucho trabajo del freno."),
   g_h2("6. Errores comunes"), g_ul(["Confundir trabajo con esfuerzo: sostener una caja quieta no realiza trabajo físico.", "Usar la distancia total en lugar de la componente en la dirección de la fuerza.", "Mezclar CV y HP, que no son iguales."])],
  [("¿Cómo se calcula el trabajo?", "W = F·d·cos θ."), ("¿Cuál es la unidad de potencia?", "El watt (J/s). También se usan el kW, el CV y el HP."), ("¿Cuándo es cero el trabajo?", "Cuando no hay desplazamiento o la fuerza es perpendicular."), ("¿Cuántos watts es un HP?", "745,7 W.")],
  [("/calculadoras/fisica/trabajo-y-potencia/", "Calculadora de Trabajo y Potencia"), ("/calculadoras/fisica/energia-cinetica-y-potencial/", "Energía Cinética y Potencial"), ("/guias/energia-cinetica-y-potencial-explicada/", "Guía: energía cinética y potencial")])

G("estequiometria-y-reactivo-limitante-paso-a-paso", "Estequiometría y reactivo limitante paso a paso",
  "Estequiometría y Reactivo Limitante: Método Paso a Paso con Ejemplos | Calculadora Científica",
  "Cómo resolver problemas de estequiometría: de gramos a moles y de moles a gramos con la relación de coeficientes, cómo hallar el reactivo limitante y el exceso, y el rendimiento.",
  "Estequiometría, reactivo limitante y rendimiento con ejemplos.",
  "Estequiometría y reactivo limitante paso a paso",
  "La estequiometría calcula cuánto reacciona y cuánto se forma en una reacción química. Siempre sigue los mismos tres pasos, y cuando hay dos reactivos aparece el concepto de reactivo limitante.",
  "Gramos → moles (÷ masa molar) → moles de lo buscado (× coeficiente buscado / coeficiente del dato) → gramos (× masa molar).",
  ("/calculadoras/quimica/estequiometria-y-reactivo-limitante/", "Abrir calculadora"),
  [g_h2("1. La ecuación balanceada"), g_p("Los coeficientes son proporciones en moles. En N₂ + 3 H₂ → 2 NH₃, 1 mol de N₂ reacciona con 3 mol de H₂ y forma 2 mol de NH₃."),
   g_h2("2. De gramos a gramos"), g_steps(["¿Cuántos gramos de NH₃ se obtienen con 28 g de N₂? (M del N₂ = 28 g/mol)", "Moles de N₂: 28 / 28 = 1 mol", "Moles de NH₃: 1 × 2 / 1 = 2 mol", "Masa de NH₃: 2 × 17,03 = 34,06 g"]),
   g_h2("3. Reactivo limitante"), g_p("Si hay dos reactivos, el que se agota primero limita la reacción. Se compara moles / coeficiente de cada uno: el menor es el limitante."),
   g_steps(["Tenemos 28 g de N₂ (1 mol) y 10 g de H₂ (4,96 mol)", "N₂: 1 / 1 = 1 · H₂: 4,96 / 3 = 1,65", "El menor es el N₂: es el limitante", "Se forman 2 mol de NH₃ (34,06 g) y sobran 4,96 − 3 = 1,96 mol de H₂ (3,95 g)"]),
   g_h2("4. Rendimiento"), g_formula("rendimiento % = masa real / masa teórica × 100"), g_p("Si el cálculo da 34,06 g y en el laboratorio se obtienen 25 g, el rendimiento es 73,4 %. A partir del rendimiento se puede calcular la masa real esperada."),
   g_h2("5. Errores comunes"), g_ul(["Usar una ecuación sin balancear.", "Comparar gramos en vez de moles para hallar el limitante.", "Olvidar el coeficiente del producto al pasar de moles de reactivo a moles de producto."])],
  [("¿Cómo se resuelve un problema de estequiometría?", "Gramos del dato → moles → relación de coeficientes → moles del buscado → gramos."), ("¿Qué es el reactivo limitante?", "El que se agota primero y determina el producto máximo."), ("¿Cómo se halla?", "Dividiendo los moles de cada reactivo por su coeficiente: el menor es el limitante."), ("¿Qué es el rendimiento?", "El porcentaje que se obtiene realmente frente al valor teórico.")],
  [("/calculadoras/quimica/estequiometria-y-reactivo-limitante/", "Calculadora de Estequiometría"), ("/calculadoras/quimica/balanceo-de-ecuaciones-quimicas/", "Balanceador de Ecuaciones"), ("/guias/como-calcular-moles/", "Guía: cómo calcular moles")])

G("como-balancear-ecuaciones-quimicas", "Cómo balancear ecuaciones químicas",
  "Cómo Balancear Ecuaciones Químicas: Tanteo y Método Algebraico | Calculadora Científica",
  "Cómo balancear ecuaciones químicas por tanteo y por el método algebraico, con ejemplos resueltos paso a paso (propano, hierro, neutralización) y errores comunes.",
  "Balanceo de ecuaciones químicas: tanteo y método algebraico.",
  "Cómo balancear ecuaciones químicas paso a paso",
  "Balancear una ecuación es hacer que haya los mismos átomos de cada elemento a los dos lados de la flecha. Hay dos métodos: el tanteo, para casos simples, y el algebraico, que funciona siempre.",
  "Los átomos de cada elemento deben ser iguales en reactivos y productos. Método algebraico: un coeficiente por sustancia y una ecuación por elemento.",
  ("/calculadoras/quimica/balanceo-de-ecuaciones-quimicas/", "Abrir calculadora"),
  [g_h2("1. Por qué hay que balancear"), g_p("La materia no se crea ni se destruye. Si en una reacción entran 4 átomos de H, tienen que salir 4. Los coeficientes (los números delante de las fórmulas) lo garantizan; los subíndices nunca se cambian."),
   g_h2("2. Método de tanteo: propano"), g_steps(["C₃H₈ + O₂ → CO₂ + H₂O", "Balanceamos C: 3 CO₂ → C₃H₈ + O₂ → 3 CO₂ + H₂O", "Balanceamos H: 4 H₂O → C₃H₈ + O₂ → 3 CO₂ + 4 H₂O", "Balanceamos O: hay 6 + 4 = 10 átomos → 5 O₂", "C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O"]),
   g_h2("3. Método algebraico: agua"), g_steps(["a·H₂ + b·O₂ → c·H₂O", "H: 2a = 2c → a = c", "O: 2b = c", "Con c = 2: a = 2, b = 1", "2 H₂ + O₂ → 2 H₂O"]),
   g_h2("4. Con paréntesis: neutralización"), g_p("Ca(OH)₂ + H₃PO₄ → Ca₃(PO₄)₂ + H₂O se balancea como 3 Ca(OH)₂ + 2 H₃PO₄ → Ca₃(PO₄)₂ + 6 H₂O. Los paréntesis multiplican todo lo que contienen: Ca(OH)₂ tiene 1 Ca, 2 O y 2 H."),
   g_h2("5. Oxidación del hierro"), g_p("4 Fe + 3 O₂ → 2 Fe₂O₃: a la izquierda 4 Fe y 6 O; a la derecha, 2 × 2 = 4 Fe y 2 × 3 = 6 O."),
   g_h2("6. Errores comunes"), g_ul(["Cambiar subíndices en vez de coeficientes (H₂O₂ no es H₂O).", "Olvidar multiplicar el coeficiente por los subíndices al contar átomos.", "Dejar coeficientes con fracciones: se multiplican todos para obtener enteros."])],
  [("¿Cómo se balancea una ecuación química?", "Igualando los átomos de cada elemento con coeficientes enteros, por tanteo o con un sistema de ecuaciones."), ("¿Cómo queda la combustión del propano?", "C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O."), ("¿Se pueden cambiar los subíndices?", "No: cambian la sustancia. Solo se cambian los coeficientes."), ("¿Para qué sirve balancear?", "Los coeficientes son las proporciones en moles para los cálculos estequiométricos.")],
  [("/calculadoras/quimica/balanceo-de-ecuaciones-quimicas/", "Balanceador de Ecuaciones Químicas"), ("/calculadoras/quimica/estequiometria-y-reactivo-limitante/", "Estequiometría y Reactivo Limitante"), ("/guias/estequiometria-y-reactivo-limitante-paso-a-paso/", "Guía: estequiometría")])

G("como-leer-el-codigo-de-colores-de-resistencias", "Cómo leer el código de colores de resistencias",
  "Código de Colores de Resistencias: Tabla y Cómo Leer 4 y 5 Bandas | Calculadora Científica",
  "Cómo leer el código de colores de las resistencias de 4 y 5 bandas, con la tabla completa de colores, multiplicadores y tolerancias, y ejemplos resueltos.",
  "Tabla del código de colores y ejemplos de lectura de resistencias.",
  "Cómo leer el código de colores de resistencias",
  "Las resistencias son tan chicas que su valor se indica con bandas de colores. Con una tabla y una regla de lectura se obtiene el valor de cualquiera de 4 o 5 bandas.",
  "4 bandas: cifra, cifra, multiplicador, tolerancia. 5 bandas: cifra, cifra, cifra, multiplicador, tolerancia. Marrón-negro-rojo-dorado = 1 kΩ ±5 %.",
  ("/calculadoras/ingenieria/codigo-de-colores-de-resistencias/", "Abrir calculadora"),
  [g_h2("1. La tabla"), g_table(["Color", "Cifra", "Multiplicador", "Tolerancia"], [["Negro", "0", "×1", "—"], ["Marrón", "1", "×10", "±1 %"], ["Rojo", "2", "×100", "±2 %"], ["Naranja", "3", "×1 k", "—"], ["Amarillo", "4", "×10 k", "—"], ["Verde", "5", "×100 k", "±0,5 %"], ["Azul", "6", "×1 M", "±0,25 %"], ["Violeta", "7", "×10 M", "±0,1 %"], ["Gris", "8", "×100 M", "±0,05 %"], ["Blanco", "9", "×1 G", "—"], ["Dorado", "—", "×0,1", "±5 %"], ["Plateado", "—", "×0,01", "±10 %"]]),
   g_h2("2. Cómo se lee"), g_ul(["Se empieza por el extremo donde las bandas están más juntas.", "La banda de tolerancia (dorada o plateada en las de 4 bandas) queda separada, al final.", "El valor es (cifras) × multiplicador."]),
   g_h2("3. Ejemplos de 4 bandas"), g_steps(["Marrón-negro-rojo-dorado → 1, 0, ×100, ±5 % → 1.000 Ω = 1 kΩ ±5 %", "Amarillo-violeta-naranja-dorado → 4, 7, ×1 k → 47 kΩ ±5 %"]),
   g_h2("4. Ejemplo de 5 bandas"), g_steps(["Rojo-rojo-negro-marrón-marrón → 2, 2, 0, ×10, ±1 %", "220 × 10 = 2.200 Ω = 2,2 kΩ ±1 %"]),
   g_h2("5. La tolerancia"), g_p("Una resistencia de 1 kΩ con ±5 % puede valer entre 950 Ω y 1050 Ω. En aplicaciones de precisión se usan las de 1 % o menos (5 bandas)."),
   g_h2("6. Medirla para confirmar"), g_p("Con un multímetro en modo ohmímetro, con la resistencia fuera del circuito, se confirma el valor. Los colores pueden confundirse (marrón y rojo, naranja y rojo) con poca luz.")],
  [("¿Cómo se lee una resistencia de 4 bandas?", "Dos cifras, un multiplicador y la tolerancia."), ("¿Qué valor tiene marrón-negro-rojo-dorado?", "1 kΩ ±5 %."), ("¿Qué significa la banda dorada?", "Como última banda, una tolerancia de ±5 %; como multiplicador, ×0,1."), ("¿Cómo sé por dónde empezar?", "Por el extremo con las bandas más juntas; la de tolerancia suele estar separada.")],
  [("/calculadoras/ingenieria/codigo-de-colores-de-resistencias/", "Código de Colores de Resistencias"), ("/calculadoras/ingenieria/resistencias-serie-paralelo/", "Resistencias en Serie y Paralelo"), ("/guias/resistencias-serie-vs-paralelo/", "Guía: resistencias en serie vs paralelo")])

G("como-funciona-un-divisor-de-tension", "Cómo funciona un divisor de tensión",
  "Divisor de Tensión: Fórmula, Ejemplos y Limitaciones | Calculadora Científica",
  "Qué es un divisor de tensión resistivo, la fórmula Vout = Vin·R2/(R1+R2), cómo elegir las resistencias para una tensión deseada, ejemplos resueltos y por qué no sirve para alimentar cargas.",
  "Divisor de tensión: fórmula, ejemplos y limitaciones.",
  "Cómo funciona un divisor de tensión",
  "Un divisor de tensión son dos resistencias en serie que \"reparten\" una tensión. Se usa para adaptar niveles (5 V a 3,3 V), leer sensores y polarizar circuitos.",
  "Vout = Vin · R2 / (R1 + R2). Para una Vout deseada: R2 = Vout · R1 / (Vin − Vout).",
  ("/calculadoras/ingenieria/divisor-de-tension/", "Abrir calculadora"),
  [g_h2("1. La idea"), g_p("Por dos resistencias en serie circula la misma corriente I = Vin / (R1 + R2). La tensión en cada una es I × su resistencia, así que la tensión se reparte en proporción a las resistencias. La salida se toma sobre R2."),
   g_formula("Vout = Vin · R2 / (R1 + R2)"),
   g_h2("2. Ejemplo directo"), g_steps(["Vin = 12 V, R1 = 1 kΩ y R2 = 2 kΩ", "Vout = 12 × 2000 / 3000 = 8 V", "Corriente: 12 / 3000 = 4 mA"]),
   g_h2("3. Elegir R2 para una tensión deseada"), g_steps(["Pasar de 5 V a 3,3 V con R1 = 1 kΩ", "R2 = 3,3 × 1000 / (5 − 3,3) = 1.941 Ω", "Se usa el valor comercial cercano (1,8 kΩ o 2 kΩ) y se verifica la salida"]),
   g_h2("4. Limitaciones"), g_ul(["La fórmula supone que la salida no alimenta nada. Una carga en paralelo con R2 baja la tensión.", "Para que el efecto de la carga sea despreciable, su resistencia debe ser al menos diez veces mayor que R2.", "El divisor disipa potencia siempre, aunque no haya carga.", "No sirve para alimentar circuitos que consumen corriente: para eso se usa un regulador."]),
   g_h2("5. Usos típicos"), g_ul(["Adaptar señales de 5 V a 3,3 V.", "Leer sensores resistivos (termistores, LDR) con un conversor analógico-digital.", "Polarizar transistores y amplificadores.", "Medir tensiones altas con un instrumento de rango chico."])],
  [("¿Cómo se calcula un divisor de tensión?", "Vout = Vin·R2/(R1 + R2)."), ("¿Cómo elijo las resistencias?", "Fijá R1 y calculá R2 = Vout·R1/(Vin − Vout); usá el valor comercial más cercano."), ("¿Puedo alimentar un circuito con un divisor?", "Solo si consume muy poca corriente."), ("¿Qué corriente circula?", "I = Vin/(R1 + R2).")],
  [("/calculadoras/ingenieria/divisor-de-tension/", "Calculadora de Divisor de Tensión"), ("/calculadoras/fisica/ley-de-ohm/", "Ley de Ohm"), ("/guias/ley-de-ohm-explicada/", "Guía: la ley de Ohm")])

G("que-resistencia-poner-a-un-led", "Qué resistencia poner a un LED",
  "Qué Resistencia Poner a un LED: Cálculo y Valores Comerciales | Calculadora Científica",
  "Cómo calcular la resistencia limitadora de un LED a partir de la tensión de la fuente, la caída del LED y la corriente, qué valor comercial elegir y cómo conectar varios LED.",
  "Resistencia para LED: fórmula, valores comerciales y ejemplos.",
  "Qué resistencia poner a un LED",
  "Un LED conectado directo a una fuente se quema: necesita una resistencia que limite la corriente. El cálculo es una resta y una división.",
  "R = (Vfuente − Vf) / I. Con 5 V, un LED rojo (2 V) y 20 mA: 150 Ω.",
  ("/calculadoras/ingenieria/resistencia-para-led/", "Abrir calculadora"),
  [g_h2("1. La fórmula"), g_formula("R = (V<sub>fuente</sub> − V<sub>f</sub>) / I"),
   g_steps(["Fuente de 5 V, LED rojo (Vf = 2 V), corriente de 20 mA", "R = (5 − 2) / 0,02 = 150 Ω", "Potencia: 3 V × 0,02 A = 60 mW (alcanza una de ¼ W)"]),
   g_h2("2. La caída de tensión (Vf) según el color"), g_table(["Color", "Vf aproximada"], [["Rojo", "1,8 – 2,2 V"], ["Amarillo / naranja", "2,0 – 2,2 V"], ["Verde", "2,0 – 3,0 V"], ["Azul / blanco", "3,0 – 3,4 V"]]),
   g_h2("3. Valores comerciales"), g_p("Las resistencias se venden en valores normalizados (serie E12: 100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820 y sus múltiplos de 10). Se elige el valor igual o mayor al calculado: da un poco menos de corriente y protege el LED."),
   g_steps(["3,3 V con LED rojo a 10 mA: R = 1,3 / 0,01 = 130 Ω → se usa 150 Ω", "9 V con LED rojo a 20 mA: R = 7 / 0,02 = 350 Ω → se usa 390 Ω"]),
   g_h2("4. Varios LED en serie"), g_p("Se suman las caídas de tensión: con 3 LED rojos (6 V) y una fuente de 12 V a 20 mA, R = (12 − 6)/0,02 = 300 Ω. La fuente debe superar la suma de las caídas."),
   g_h2("5. Corriente y brillo"), g_p("La mayoría de los LED comunes admiten hasta 20 mA. Con 10 a 15 mA brillan bien y duran más. Un valor de resistencia mayor al calculado solo reduce el brillo; uno menor puede quemar el LED."),
   g_h2("6. Errores comunes"), g_ul(["Conectar el LED sin resistencia.", "Usar la tensión de la fuente completa en la fórmula, sin restar la del LED.", "Poner varios LED en paralelo con una sola resistencia: no se reparten bien la corriente."])],
  [("¿Qué resistencia necesita un LED con 5 V?", "150 Ω para un LED rojo a 20 mA."), ("¿Qué pasa si no pongo resistencia?", "El LED se quema."), ("¿Qué corriente le doy a un LED?", "Entre 10 y 20 mA para los comunes."), ("¿Puedo usar una resistencia mayor?", "Sí, el LED brilla algo menos pero está más protegido.")],
  [("/calculadoras/ingenieria/resistencia-para-led/", "Calculadora de Resistencia para LED"), ("/calculadoras/ingenieria/codigo-de-colores-de-resistencias/", "Código de Colores de Resistencias"), ("/guias/ley-de-ohm-explicada/", "Guía: la ley de Ohm")])
