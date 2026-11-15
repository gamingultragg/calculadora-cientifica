"""
build-batch-12.py — Lote 12 (motor común): Vida Diaria (peso ideal, fecha probable de parto), Física (gravitación universal, ley de Snell),
Estadística (medias, errores de medición), Química (propiedades coligativas) y Hogar y Construcción (pendiente de rampa).
Genera las 8 páginas de calculadora; las guías están en build-batch-12-guides.py.
Generación de una sola vez: después, el HTML es la fuente de verdad.
"""
from spec_lib import ENGINE, FORMULA, INPUT, LABEL, Lib, calc_page, esc, help_blocks, write_page

VID = dict(cat_slug="vida-diaria", cat_label="Vida Diaria")
FIS = dict(cat_slug="fisica", cat_label="Física")
EST = dict(cat_slug="estadistica", cat_label="Estadística")
QUI = dict(cat_slug="quimica", cat_label="Química")
HOG = dict(cat_slug="hogar-y-construccion", cat_label="Hogar y Construcción")


def page(rel, cat, **kw):
    write_page(rel, calc_page(pre_scripts=ENGINE, **cat, **kw))


def date_field(L, id_, label, when=None, opt=False, value=""):
    """Campo de fecha (input type=date) para el motor común: se lee como texto 'AAAA-MM-DD' (vacío si es opcional)."""
    o = " data-opt" if opt else ""
    v = f' value="{value}"' if value else ""
    inner = (f'          <label for="{L.p}-{id_}" {LABEL}>{label}</label>\n'
             f'          <input id="{L.p}-{id_}" type="date" data-kind="text" data-label="{esc(label)}"{o}{v} {INPUT} />')
    return L._wrap(id_, inner, when)


# ================================================================ peso ideal
L = Lib("pi")
page("calculadoras/vida-diaria/calculadora-de-peso-ideal", VID,
     slug="calculadora-de-peso-ideal", name="Calculadora de Peso Ideal",
     page_title="Calculadora de Peso Ideal: Fórmulas de Devine, Robinson, Miller y Hamwi | Calculadora Científica",
     desc="Calculá tu peso ideal según tu altura y sexo con las fórmulas de Devine, Robinson, Miller y Hamwi, y tu rango de peso saludable según el IMC (18,5 a 24,9). Gratis.",
     og_title="Calculadora de Peso Ideal",
     og_desc="Peso ideal con 4 fórmulas y rango saludable por IMC. Gratis.",
     schema_desc="Calcula el peso ideal de un adulto según su altura y sexo con las fórmulas de Devine, Robinson, Miller y Hamwi, y el rango de peso saludable correspondiente a un índice de masa corporal entre 18,5 y 24,9.",
     intro="Ingresá tu sexo, edad y altura: obtenés tu rango de peso saludable según el IMC y el peso ideal que dan cuatro fórmulas clásicas (Devine, Robinson, Miller y Hamwi). Es una orientación general para adultos, no un diagnóstico.",
     form_html=L.form([
         L.sel("sex", "Sexo", [("mujer", "Mujer"), ("hombre", "Hombre")]),
         L.num("age", "Edad (años)", "Ej: 30", rule="int"),
         L.num("height", "Altura (cm)", "Ej: 170"),
     ], chips=[("Hombre de 175 cm", "sex=hombre;age=30;height=175"), ("Mujer de 165 cm", "sex=mujer;age=30;height=165"), ("Mujer de 158 cm", "sex=mujer;age=40;height=158")],
         note="Para adultos de 18 años o más. No reemplaza la consulta con un médico o nutricionista."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Rango saludable según el IMC", f'<p {FORMULA}>peso = IMC × altura² (con la altura en metros) &nbsp;·&nbsp; IMC saludable: 18,5 a 24,9</p><p>Es el criterio más usado hoy: en lugar de un único número, da un rango. Para 1,75 m va de 56,7 a 76,3 kg.</p>'),
         ("Fórmulas clásicas", f'<p {FORMULA}>Devine (hombres): 50 + 2,3 × (pulgadas − 60) &nbsp;·&nbsp; Devine (mujeres): 45,5 + 2,3 × (pulgadas − 60)</p><p>Robinson, Miller y Hamwi usan la misma idea, con otros coeficientes. Todas parten de los 60 pulgadas (152,4 cm) y suman un peso por cada pulgada de más.</p>'),
         ("Limitaciones", "<p>No distinguen entre músculo y grasa, ni consideran la contextura, la edad, el embarazo o enfermedades. Un deportista con mucha masa muscular puede estar fuera del rango y estar sano. Consultá con un profesional antes de cambiar tu alimentación.</p>"),
     ]),
     related=[("/calculadoras/vida-diaria/calculadora-de-imc/", "Calculadora de IMC"), ("/calculadoras/vida-diaria/calculadora-de-calorias-y-metabolismo-basal/", "Calorías y Metabolismo Basal"),
              ("/calculadoras/ingenieria/conversor-de-unidades/", "Conversor de Unidades")],
     guide=("/guias/como-calcular-el-peso-ideal/", "Cómo calcular el peso ideal", "Leé la guía completa: las cuatro fórmulas, el rango por IMC, ejemplos y sus límites."),
     faqs=[("¿Cómo se calcula el peso ideal?", "Con fórmulas que dependen de la altura y el sexo (Devine, Robinson, Miller, Hamwi) o con el rango de IMC saludable (18,5 a 24,9). Para un hombre de 175 cm, el rango es de 56,7 a 76,3 kg."),
           ("¿Cuál es la fórmula de Devine?", "Para hombres, 50 kg + 2,3 kg por cada pulgada de altura sobre 60 pulgadas (152,4 cm); para mujeres, 45,5 kg + 2,3 kg por pulgada."),
           ("¿Por qué las fórmulas dan resultados distintos?", "Porque cada una se desarrolló con poblaciones y criterios diferentes. Por eso conviene mirar el rango y no un único número."),
           ("¿El peso ideal es el mismo para todos?", "No: depende de la contextura, la masa muscular, la edad y la salud. Es solo una referencia."),
           ("¿Sirve para menores de 18 años?", "No. En niños y adolescentes se usan curvas de crecimiento que interpreta el pediatra.")])

# ================================================================ fecha probable de parto
L = Lib("fp")
page("calculadoras/vida-diaria/calculadora-de-fecha-probable-de-parto", VID,
     slug="calculadora-de-fecha-probable-de-parto", name="Calculadora de Fecha Probable de Parto",
     page_title="Calculadora de Fecha Probable de Parto y Semanas de Embarazo (Regla de Naegele) | Calculadora Científica",
     desc="Calculá la fecha probable de parto y las semanas de embarazo a partir de la fecha de última menstruación o de concepción, con el trimestre y fechas de referencia. Gratis.",
     og_title="Calculadora de Fecha Probable de Parto",
     og_desc="Fecha probable de parto, semanas de embarazo y trimestre. Gratis.",
     schema_desc="Calcula la fecha probable de parto con la regla de Naegele a partir de la fecha de última menstruación (con ajuste por duración del ciclo) o de la fecha de concepción, y la edad gestacional en semanas y días con el trimestre.",
     intro="Ingresá la fecha de tu última menstruación (o la de concepción) y obtenés la fecha probable de parto, cuántas semanas de embarazo tenés hoy, en qué trimestre estás y fechas de referencia. Es una estimación: tu obstetra la confirma con la ecografía.",
     form_html=L.form([
         L.sel("mode", "Qué fecha conocés", [("lmp", "Fecha de la última menstruación (FUM)"), ("conc", "Fecha de concepción")]),
         date_field(L, "date", "Fecha"),
         L.num("cycle", "Duración de tu ciclo (días)", "28", opt=True, default=28, rule="int", value="28", when="mode=lmp"),
         date_field(L, "ref", "Calcular a la fecha (si lo dejás vacío, es hoy)", opt=True),
     ], chips=[("FUM del 1/3/2026, calculado al 10/5/2026", "mode=lmp;date=2026-03-01;cycle=28;ref=2026-05-10"), ("Ciclo de 32 días", "mode=lmp;date=2026-03-01;cycle=32;ref=2026-05-10"), ("Concepción el 15/3/2026", "mode=conc;date=2026-03-15;ref=2026-06-01")],
         note="Es una estimación orientativa y no reemplaza el control médico."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Regla de Naegele", f'<p {FORMULA}>FPP = FUM + 280 días (40 semanas) &nbsp;·&nbsp; con un ciclo distinto de 28 días: + (ciclo − 28) días</p><p>El embarazo se cuenta desde el primer día de la última menstruación, unas dos semanas antes de la concepción. Si se conoce la concepción: FPP = concepción + 266 días.</p>'),
         ("Edad gestacional y trimestres", "<p>Se expresa en semanas y días desde la FUM. Primer trimestre: hasta la semana 13 y 6 días; segundo: de la 14 a la 27; tercero: desde la 28. Un embarazo a término va de la semana 37 a la 41 y 6 días.</p>"),
         ("Qué tan exacta es", "<p>Solo una minoría de los bebés nace en la fecha probable; lo normal es entre las semanas 37 y 42. La ecografía del primer trimestre es el método más preciso para datar el embarazo, y tu obstetra puede ajustar la fecha.</p>"),
     ]),
     related=[("/calculadoras/vida-diaria/calculadora-de-edad-y-fechas/", "Edad y Fechas"), ("/calculadoras/vida-diaria/calculadora-de-imc/", "Calculadora de IMC"),
              ("/calculadoras/vida-diaria/calculadora-de-peso-ideal/", "Calculadora de Peso Ideal")],
     guide=("/guias/como-calcular-la-fecha-probable-de-parto/", "Cómo calcular la fecha probable de parto", "Leé la guía completa: la regla de Naegele, el ajuste por ciclo, las semanas y trimestres y ejemplos."),
     faqs=[("¿Cómo se calcula la fecha probable de parto?", "Con la regla de Naegele: se suman 280 días (40 semanas) a la fecha de la última menstruación. Con FUM del 1 de enero, la fecha probable es el 8 de octubre."),
           ("¿Y si mi ciclo no es de 28 días?", "Se ajusta sumando o restando la diferencia: con un ciclo de 32 días, se agregan 4 días."),
           ("¿Cómo se cuentan las semanas de embarazo?", "Desde el primer día de la última menstruación, no desde la concepción, que ocurre unas dos semanas después."),
           ("¿Qué tan segura es la fecha?", "Es una estimación: solo unos pocos bebés nacen exactamente ese día. La ecografía del primer trimestre permite datar mejor el embarazo."),
           ("¿Cuándo termina el primer trimestre?", "En la semana 13 y 6 días. El segundo trimestre va de la semana 14 a la 27 y el tercero empieza en la 28.")])

# ================================================================ gravitación universal
L = Lib("gv")
page("calculadoras/fisica/calculadora-de-gravitacion-universal", FIS,
     slug="calculadora-de-gravitacion-universal", name="Calculadora de Gravitación Universal",
     page_title="Calculadora de Gravitación Universal: Fuerza, Gravedad y Velocidad Orbital | Calculadora Científica",
     desc="Calculá la fuerza gravitatoria entre dos cuerpos, la gravedad en la superficie de un planeta y la velocidad, el período y la velocidad de escape de una órbita. Gratis.",
     og_title="Calculadora de Gravitación Universal",
     og_desc="Fuerza gravitatoria, gravedad de un planeta y velocidad orbital. Gratis.",
     schema_desc="Calcula la fuerza de atracción gravitatoria entre dos masas con la ley de Newton, la aceleración de la gravedad en la superficie de un planeta o astro, y la velocidad orbital, el período y la velocidad de escape de una órbita circular.",
     intro="Elegí qué querés calcular: la fuerza de atracción entre dos cuerpos, la gravedad en la superficie de un planeta o la velocidad y el período de una órbita circular. Con los ejemplos cargás la Tierra, la Luna, Marte o la Estación Espacial en un toque.",
     form_html=L.form([
         L.sel("mode", "Qué querés calcular", [("f", "Fuerza gravitatoria entre dos cuerpos"), ("g", "Gravedad en la superficie de un planeta"), ("orb", "Órbita circular: velocidad y período")]),
         L.num("m1", "Masa del cuerpo 1 (kg)", "Ej: 1,989e30", when="mode=f"),
         L.num("m2", "Masa del cuerpo 2 (kg)", "Ej: 5,972e24", when="mode=f"),
         L.num("M", "Masa del astro (kg)", "Ej: 5,972e24", when="mode=g|orb"),
         L.num("r", "Distancia entre centros (o radio del astro)", "Ej: 6371"),
         L.sel("ru", "Unidad de la distancia", [("km", "kilómetros (km)"), ("m", "metros (m)")]),
     ], chips=[("Gravedad en la Tierra", "mode=g;M=5,972e24;r=6371;ru=km"), ("Gravedad en la Luna", "mode=g;M=7,342e22;r=1737,4;ru=km"), ("Gravedad en Marte", "mode=g;M=6,417e23;r=3389,5;ru=km"),
               ("Estación Espacial (órbita a 400 km)", "mode=orb;M=5,972e24;r=6771;ru=km"), ("Fuerza Sol–Tierra", "mode=f;m1=1,989e30;m2=5,972e24;r=149600000;ru=km")],
         note="Podés escribir notación científica con e: 5,972e24 = 5,972 × 10²⁴."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Ley de gravitación universal", f'<p {FORMULA}>F = G · m₁ · m₂ / r² &nbsp; con &nbsp; G = 6,6743 × 10⁻¹¹ N·m²/kg²</p><p>Dos masas cualesquiera se atraen con una fuerza proporcional al producto de las masas e inversamente proporcional al cuadrado de la distancia entre sus centros.</p>'),
         ("Gravedad de un astro", f'<p {FORMULA}>g = G · M / r²</p><p>Es la aceleración que adquiere un objeto en caída libre sobre la superficie de un astro de masa M y radio r. En la Tierra: 9,82 m/s²; en la Luna, 1,62 m/s².</p>'),
         ("Órbitas", f'<p {FORMULA}>v = √(G·M/r) &nbsp;·&nbsp; T = 2π·√(r³/(G·M)) &nbsp;·&nbsp; v_escape = √(2·G·M/r)</p><p>La velocidad orbital circular no depende de la masa del satélite. Para escapar de la gravedad hay que superar √2 veces la velocidad orbital.</p>'),
     ]),
     related=[("/calculadoras/fisica/calculadora-de-ley-de-coulomb/", "Ley de Coulomb"), ("/calculadoras/fisica/caida-libre-y-tiro-oblicuo/", "Caída Libre y Tiro Oblicuo"),
              ("/calculadoras/fisica/calculadora-de-movimiento-circular/", "Movimiento Circular Uniforme")],
     guide=("/guias/ley-de-gravitacion-universal-explicada/", "Ley de gravitación universal explicada", "Leé la guía completa: la fórmula, la gravedad de los planetas, las órbitas y ejemplos resueltos."),
     faqs=[("¿Qué dice la ley de gravitación universal?", "Que dos masas se atraen con una fuerza proporcional al producto de sus masas e inversamente proporcional al cuadrado de la distancia: F = G·m₁·m₂/r²."),
           ("¿Cuánto vale la gravedad en la Luna?", "Unos 1,62 m/s², alrededor de un sexto de la terrestre. Un objeto de 60 kg pesa allí lo que 10 kg en la Tierra."),
           ("¿A qué velocidad orbita la Estación Espacial?", "Unos 7,67 km/s (más de 27.000 km/h): da una vuelta a la Tierra en aproximadamente 92 minutos."),
           ("¿Qué es la velocidad de escape?", "La velocidad mínima para alejarse de un astro sin propulsión: en la Tierra, unos 11,2 km/s."),
           ("¿Depende la órbita de la masa del satélite?", "No: la velocidad y el período orbital dependen solo de la masa del astro y del radio de la órbita.")])

# ================================================================ ley de Snell
L = Lib("sn")
page("calculadoras/fisica/calculadora-de-ley-de-snell", FIS,
     slug="calculadora-de-ley-de-snell", name="Calculadora de la Ley de Snell: Refracción de la Luz",
     page_title="Calculadora de la Ley de Snell: Refracción, Ángulo Crítico y Reflexión Total | Calculadora Científica",
     desc="Calculá el ángulo de refracción, el índice de refracción o el ángulo crítico con la ley de Snell (n₁·sen θ₁ = n₂·sen θ₂). Detecta la reflexión total interna. Gratis.",
     og_title="Calculadora de la Ley de Snell",
     og_desc="Ángulo de refracción, índice de refracción y ángulo crítico. Gratis.",
     schema_desc="Resuelve la ley de Snell de la refracción de la luz para hallar el ángulo refractado, el índice de refracción de un medio o el ángulo crítico, e indica cuándo ocurre reflexión total interna y la velocidad de la luz en cada medio.",
     intro="Elegí qué querés calcular: el ángulo con el que se desvía un rayo al pasar de un medio a otro, el índice de refracción desconocido o el ángulo crítico. Te avisa cuando hay reflexión total interna y calcula la velocidad de la luz en cada medio.",
     form_html=L.form([
         L.sel("mode", "Qué querés calcular", [("t2", "Ángulo de refracción θ₂"), ("n2", "Índice de refracción n₂"), ("crit", "Ángulo crítico")]),
         L.num("n1", "Índice de refracción del medio 1 (n₁)", "Ej: 1,0003", hint="Aire 1,0003 · agua 1,333 · aceite 1,47 · vidrio 1,52 · diamante 2,417 · hielo 1,31"),
         L.num("n2", "Índice de refracción del medio 2 (n₂)", "Ej: 1,333", when="mode=t2|crit"),
         L.num("a1", "Ángulo de incidencia θ₁ (°, respecto de la normal)", "Ej: 30", rule="nonneg", when="mode=t2|n2"),
         L.num("a2", "Ángulo de refracción θ₂ (°)", "Ej: 22", rule="nonneg", when="mode=n2"),
     ], chips=[("Aire → agua a 30°", "mode=t2;n1=1,0003;n2=1,333;a1=30"), ("Vidrio → aire a 60° (reflexión total)", "mode=t2;n1=1,52;n2=1,0003;a1=60"), ("Ángulo crítico agua → aire", "mode=crit;n1=1,333;n2=1,0003"),
               ("¿Qué índice tiene? (aire a 30°, refracta a 19,47°)", "mode=n2;n1=1,0003;a1=30;a2=19,47")],
         note="Los ángulos se miden respecto de la normal (la perpendicular a la superficie), no respecto de la superficie."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Ley de Snell", f'<p {FORMULA}>n₁ · sen θ₁ = n₂ · sen θ₂</p><p>Relaciona los ángulos de incidencia y de refracción con los índices de refracción de los dos medios. Al pasar a un medio de mayor índice, el rayo se acerca a la normal; a uno de menor índice, se aleja.</p>'),
         ("Índice de refracción", f'<p {FORMULA}>n = c / v</p><p>Es el cociente entre la velocidad de la luz en el vacío (c ≈ 3 × 10⁸ m/s) y su velocidad en el medio. Siempre es mayor o igual que 1: en el agua la luz viaja a unos 225.000 km/s.</p>'),
         ("Ángulo crítico y reflexión total", f'<p {FORMULA}>θc = arcsen(n₂ / n₁) &nbsp; (solo si n₁ &gt; n₂)</p><p>Si el ángulo de incidencia supera el crítico, no hay rayo refractado: la luz se refleja por completo. Es el principio de la fibra óptica y del brillo de los diamantes.</p>'),
     ]),
     related=[("/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/", "Calculadora Científica Online"), ("/calculadoras/matematicas-avanzadas/resolucion-de-triangulos/", "Resolución de Triángulos"),
              ("/calculadoras/fisica/calculadora-de-movimiento-circular/", "Movimiento Circular Uniforme")],
     guide=("/guias/ley-de-snell-y-refraccion-de-la-luz/", "Ley de Snell y refracción de la luz", "Leé la guía completa: la ley, los índices de refracción, el ángulo crítico y ejemplos resueltos."),
     faqs=[("¿Qué dice la ley de Snell?", "Que n₁·sen θ₁ = n₂·sen θ₂: relaciona los ángulos que forma un rayo con la normal a ambos lados de la superficie que separa dos medios."),
           ("¿Cómo se calcula el ángulo de refracción?", "θ₂ = arcsen(n₁·sen θ₁ / n₂). De aire a agua con 30° de incidencia: arcsen(1,0003 × 0,5 / 1,333) ≈ 22°."),
           ("¿Qué es el ángulo crítico?", "El ángulo de incidencia a partir del cual hay reflexión total interna. De agua a aire es de unos 48,6°."),
           ("¿Cuándo ocurre la reflexión total interna?", "Cuando la luz pasa a un medio de menor índice de refracción y el ángulo de incidencia supera el crítico."),
           ("¿Qué es el índice de refracción?", "El cociente entre la velocidad de la luz en el vacío y en el medio: n = c/v. El del agua es 1,333 y el del vidrio, alrededor de 1,52.")])

# ================================================================ medias
L = Lib("md")
page("calculadoras/estadistica/calculadora-de-medias", EST,
     slug="calculadora-de-medias", name="Calculadora de Media Aritmética, Geométrica y Armónica",
     page_title="Calculadora de Media Aritmética, Geométrica y Armónica | Calculadora Científica",
     desc="Calculá la media aritmética, geométrica, armónica y cuadrática de una lista de números, con ejemplos de crecimiento promedio y velocidad media. Gratis y con fórmulas.",
     og_title="Calculadora de Medias: Aritmética, Geométrica y Armónica",
     og_desc="Las cuatro medias de una lista de números en un solo paso. Gratis.",
     schema_desc="Calcula la media aritmética, geométrica, armónica y cuadrática de un conjunto de datos, verifica la desigualdad entre las medias y explica en qué casos conviene usar cada una.",
     intro="Pegá una lista de números y obtenés la media aritmética, la geométrica, la armónica y la cuadrática. Cada una sirve para un caso distinto: la geométrica para tasas de crecimiento, la armónica para velocidades y rendimientos.",
     form_html=L.form([
         L.text("list", "Números", "Ej: 2 8 4,5 10", rows=4, hint="Separalos con espacios, saltos de línea o punto y coma. Los decimales, con coma o con punto."),
     ], chips=[("2 y 8", "list=2 8"), ("1, 2, 3 y 4", "list=1 2 3 4"), ("Crecimiento: 1,10 · 1,20 · 0,95", "list=1,10 1,20 0,95"), ("Velocidades: 60 y 40 km/h", "list=60 40")],
         note="La media geométrica y la armónica solo se definen para números mayores que 0."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Media aritmética y cuadrática", f'<p {FORMULA}>AM = (x₁ + … + xₙ) / n &nbsp;·&nbsp; QM = √((x₁² + … + xₙ²) / n)</p><p>La aritmética es el promedio de siempre. La cuadrática se usa en física e ingeniería (por ejemplo, el valor eficaz de una señal).</p>'),
         ("Media geométrica", f'<p {FORMULA}>GM = ⁿ√(x₁ · x₂ · … · xₙ)</p><p>Es la adecuada para promediar factores de crecimiento, razones y tasas que se acumulan: si algo crece 10 %, 20 % y baja 5 %, el crecimiento promedio por período es la media geométrica de 1,10, 1,20 y 0,95.</p>'),
         ("Media armónica", f'<p {FORMULA}>HM = n / (1/x₁ + … + 1/xₙ)</p><p>Es la correcta para promediar velocidades en tramos de igual distancia o rendimientos: ida a 60 km/h y vuelta a 40 km/h dan una velocidad media de 48 km/h, no de 50.</p>'),
     ]),
     related=[("/calculadoras/estadistica/calculadora-estadistica-descriptiva/", "Estadística Descriptiva"), ("/calculadoras/estadistica/calculadora-de-promedio-de-notas/", "Promedio de Notas"),
              ("/calculadoras/matematicas-avanzadas/calculadora-de-potencias-y-raices/", "Potencias y Raíces")],
     guide=("/guias/media-aritmetica-geometrica-y-armonica/", "Media aritmética, geométrica y armónica", "Leé la guía completa: cuándo usar cada media, la desigualdad entre ellas y ejemplos resueltos."),
     faqs=[("¿Cuál es la diferencia entre la media aritmética y la geométrica?", "La aritmética suma y divide; la geométrica multiplica y saca raíz. La geométrica es la adecuada para tasas de crecimiento y razones."),
           ("¿Cuándo se usa la media armónica?", "Para promediar velocidades en tramos de igual distancia, precios por unidad o rendimientos. Ida a 60 km/h y vuelta a 40 km/h: 48 km/h."),
           ("¿Cómo se calcula el crecimiento promedio?", "Con la media geométrica de los factores. Para +10 %, +20 % y −5 %: (1,10 × 1,20 × 0,95)^(1/3) ≈ 1,078, o sea un 7,8 % por período."),
           ("¿Qué relación hay entre las medias?", "Para números positivos: armónica ≤ geométrica ≤ aritmética ≤ cuadrática, y son iguales solo si todos los datos coinciden."),
           ("¿Se pueden usar números negativos o ceros?", "En la aritmética y la cuadrática sí; en la geométrica y la armónica no.")])

# ================================================================ errores de medición
L = Lib("er")
page("calculadoras/estadistica/calculadora-de-error-absoluto-y-relativo", EST,
     slug="calculadora-de-error-absoluto-y-relativo", name="Calculadora de Error Absoluto, Relativo y Porcentual",
     page_title="Calculadora de Error Absoluto, Relativo y Porcentual (e Incertidumbre) | Calculadora Científica",
     desc="Calculá el error absoluto, relativo y porcentual de una medición, o el promedio, el desvío y el error estándar de una serie de mediciones. Gratis y con fórmulas.",
     og_title="Calculadora de Error Absoluto, Relativo y Porcentual",
     og_desc="Error absoluto, relativo y porcentual, e incertidumbre de una serie de mediciones. Gratis.",
     schema_desc="Calcula el error absoluto, el error relativo y el error porcentual de una medición respecto de un valor real, y el promedio, el desvío estándar y el error estándar de una serie de mediciones.",
     intro="Elegí si querés comparar una medición con el valor real (error absoluto, relativo y porcentual) o analizar varias mediciones de la misma magnitud (promedio, desvío y error estándar). Pensada para informes de laboratorio.",
     form_html=L.form([
         L.sel("mode", "Qué querés calcular", [("uno", "Comparar una medición con el valor real"), ("serie", "Analizar varias mediciones")]),
         L.num("real", "Valor real (o de referencia)", "Ej: 9,81", rule="any", when="mode=uno"),
         L.num("meas", "Valor medido", "Ej: 9,65", rule="any", when="mode=uno"),
         L.text("list", "Mediciones", "Ej: 9,8 9,7 9,9 9,75", rows=3, when="mode=serie", hint="Separalas con espacios, saltos de línea o punto y coma."),
     ], chips=[("Gravedad medida 9,65 vs 9,81", "mode=uno;real=9,81;meas=9,65"), ("Medí 50 mm y dio 49,2", "mode=uno;real=50;meas=49,2"), ("Serie de 4 mediciones", "mode=serie;list=9,8 9,7 9,9 9,75")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Error absoluto, relativo y porcentual", f'<p {FORMULA}>E = |medido − real| &nbsp;·&nbsp; e = E / |real| &nbsp;·&nbsp; e % = e × 100</p><p>El absoluto tiene las unidades de la medición; el relativo es un número sin unidades que permite comparar mediciones de distinta magnitud; el porcentual es el relativo expresado en %.</p>'),
         ("Serie de mediciones", f'<p {FORMULA}>x̄ = Σx / n &nbsp;·&nbsp; s = √(Σ(x − x̄)² / (n − 1)) &nbsp;·&nbsp; error estándar = s / √n</p><p>El resultado se informa como x̄ ± error estándar. Cuantas más mediciones, menor el error estándar.</p>'),
         ("Exactitud y precisión", "<p>La exactitud indica qué tan cerca está la medición del valor real (error pequeño); la precisión, qué tan parecidas son entre sí las mediciones repetidas (desvío pequeño). Se puede ser preciso sin ser exacto.</p>"),
     ]),
     related=[("/calculadoras/estadistica/calculadora-estadistica-descriptiva/", "Estadística Descriptiva"), ("/calculadoras/estadistica/intervalo-de-confianza/", "Intervalo de Confianza"),
              ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes")],
     guide=("/guias/error-absoluto-relativo-y-porcentual/", "Error absoluto, relativo y porcentual", "Leé la guía completa: las fórmulas, el error estándar, exactitud vs. precisión y ejemplos resueltos."),
     faqs=[("¿Cómo se calcula el error absoluto?", "Es la diferencia en valor absoluto entre el valor medido y el real: E = |medido − real|. Si mediste 9,65 y el valor es 9,81, E = 0,16."),
           ("¿Cómo se calcula el error relativo y el porcentual?", "El relativo es E / |real| y el porcentual, ese valor por 100. Para el ejemplo: 0,16 / 9,81 = 0,0163 → 1,63 %."),
           ("¿Cuál es la diferencia entre exactitud y precisión?", "Exactitud: cercanía al valor real. Precisión: cercanía entre mediciones repetidas."),
           ("¿Qué es el error estándar de la media?", "s/√n: mide cuánto puede apartarse el promedio de la medición verdadera. Baja al aumentar la cantidad de mediciones."),
           ("¿Cómo se informa una medición?", "Como promedio ± incertidumbre, con la misma cantidad de decimales: por ejemplo, 9,79 ± 0,04 m/s².")])

# ================================================================ propiedades coligativas
L = Lib("pc")
page("calculadoras/quimica/calculadora-de-propiedades-coligativas", QUI,
     slug="calculadora-de-propiedades-coligativas", name="Calculadora de Propiedades Coligativas",
     page_title="Calculadora de Descenso Crioscópico y Ascenso Ebulloscópico (Propiedades Coligativas) | Calculadora Científica",
     desc="Calculá el punto de congelación y de ebullición de una solución con ΔT = i·K·m: descenso crioscópico y ascenso ebulloscópico en agua, benceno, etanol y ácido acético. Gratis.",
     og_title="Calculadora de Propiedades Coligativas",
     og_desc="Descenso crioscópico y ascenso ebulloscópico de una solución. Gratis.",
     schema_desc="Calcula la molalidad de una solución y el descenso del punto de congelación (crioscopía) y el ascenso del punto de ebullición (ebulloscopía), con el factor de van't Hoff y constantes de agua, benceno, etanol y ácido acético.",
     intro="Ingresá la masa y la masa molar del soluto y la masa de solvente: obtenés la molalidad, cuánto baja el punto de congelación y cuánto sube el de ebullición. Incluye el factor de van't Hoff para sales y electrolitos.",
     form_html=L.form([
         L.sel("mode", "Qué querés ver primero", [("crio", "Punto de congelación (crioscopía)"), ("ebu", "Punto de ebullición (ebulloscopía)")]),
         L.num("mass", "Masa del soluto (g)", "Ej: 58,44"),
         L.num("mm", "Masa molar del soluto (g/mol)", "Ej: 58,44"),
         L.num("solvent", "Masa del solvente (g)", "Ej: 1000"),
         L.sel("solv", "Solvente", [("agua", "Agua"), ("benceno", "Benceno"), ("etanol", "Etanol"), ("acetico", "Ácido acético")]),
         L.num("i", "Factor de van't Hoff (i) — opcional", "1", opt=True, default=1, value="1", hint="1 para solutos que no se disocian (azúcar, urea) · 2 para NaCl · 3 para CaCl₂"),
     ], chips=[("58,44 g de NaCl en 1 kg de agua (i = 2)", "mode=crio;mass=58,44;mm=58,44;solvent=1000;solv=agua;i=2"), ("342,3 g de azúcar en 1 kg de agua", "mode=crio;mass=342,3;mm=342,3;solvent=1000;solv=agua;i=1"), ("100 g de azúcar en 500 g de agua (ebullición)", "mode=ebu;mass=100;mm=342,3;solvent=500;solv=agua;i=1"),
               ("Naftaleno en benceno", "mode=crio;mass=12,8;mm=128,17;solvent=200;solv=benceno;i=1")],
         note="Soluciones diluidas e ideales; el solvente hierve a presión normal."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Propiedades coligativas", "<p>Son las que dependen de cuántas partículas de soluto hay y no de qué partículas son: el descenso del punto de congelación, el ascenso del punto de ebullición, la presión osmótica y el descenso de la presión de vapor.</p>"),
         ("Fórmulas", f'<p {FORMULA}>ΔTf = i · Kf · m &nbsp;·&nbsp; ΔTb = i · Kb · m &nbsp;·&nbsp; m = moles de soluto / kg de solvente</p><p>Kf y Kb son constantes del solvente: para el agua, Kf = 1,86 y Kb = 0,512 °C·kg/mol.</p>'),
         ("Factor de van't Hoff", "<p>Cuenta cuántas partículas genera cada unidad de soluto al disolverse: el NaCl se separa en Na⁺ y Cl⁻ (i ≈ 2), el CaCl₂ en tres iones (i ≈ 3) y el azúcar no se disocia (i = 1). Por eso la sal baja más el punto de congelación que el azúcar.</p>"),
     ]),
     related=[("/calculadoras/quimica/calculadora-de-molaridad/", "Calculadora de Molaridad"), ("/calculadoras/quimica/calculadora-de-masa-molar/", "Masa Molar"),
              ("/calculadoras/quimica/calculadora-de-concentracion-ppm/", "Concentración: ppm y Porcentaje")],
     guide=("/guias/propiedades-coligativas-crioscopia-y-ebulloscopia/", "Propiedades coligativas: crioscopía y ebulloscopía", "Leé la guía completa: las fórmulas, el factor de van't Hoff, las constantes y ejemplos resueltos."),
     faqs=[("¿Qué es el descenso crioscópico?", "Es la disminución del punto de congelación de un solvente al disolver un soluto: ΔTf = i·Kf·m. Por eso se echa sal a las calles heladas."),
           ("¿Qué es el ascenso ebulloscópico?", "El aumento del punto de ebullición por un soluto no volátil: ΔTb = i·Kb·m."),
           ("¿Qué es la molalidad?", "Los moles de soluto por kilogramo de solvente (mol/kg). A diferencia de la molaridad, no cambia con la temperatura."),
           ("¿Cuánto baja el punto de congelación al disolver sal en agua?", "Un mol de NaCl (58,44 g) en 1 kg de agua, con i = 2: ΔTf = 2 × 1,86 × 1 = 3,72 °C; congela a −3,72 °C."),
           ("¿Qué es el factor de van't Hoff?", "El número de partículas que genera cada unidad de soluto al disolverse: 1 para el azúcar, 2 para el NaCl, 3 para el CaCl₂.")])

# ================================================================ pendiente de rampa
L = Lib("rp")
page("calculadoras/hogar-y-construccion/calculadora-de-pendiente-de-rampa", HOG,
     slug="calculadora-de-pendiente-de-rampa", name="Calculadora de Pendiente de Rampa",
     page_title="Calculadora de Pendiente de Rampa: Porcentaje, Grados y Largo Necesario | Calculadora Científica",
     desc="Calculá la pendiente de una rampa en porcentaje y grados, el largo que necesitás para salvar un desnivel o la altura que salva una rampa de cierta longitud. Gratis.",
     og_title="Calculadora de Pendiente de Rampa",
     og_desc="Pendiente en % y grados, largo necesario y desnivel de una rampa. Gratis.",
     schema_desc="Calcula la pendiente de una rampa en porcentaje y en grados a partir del desnivel y la longitud, el largo necesario para una pendiente dada y el desnivel que salva una rampa de cierto largo, con una referencia de accesibilidad.",
     intro="Elegí qué necesitás: la pendiente a partir del desnivel y la longitud, el largo que hace falta para una pendiente dada o el desnivel que salva una rampa. El resultado incluye porcentaje, grados y el largo real de la rampa.",
     form_html=L.form([
         L.sel("mode", "Qué querés calcular", [("pend", "La pendiente (tengo desnivel y longitud)"), ("largo", "El largo necesario (tengo desnivel y pendiente)"), ("alto", "El desnivel (tengo longitud y pendiente)")]),
         L.sel("unit", "Unidad de las medidas", [("m", "metros (m)"), ("cm", "centímetros (cm)")]),
         L.num("rise", "Desnivel (altura a salvar)", "Ej: 0,9", when="mode=pend|largo"),
         L.num("run", "Longitud horizontal", "Ej: 9", when="mode=pend|alto"),
         L.num("pct", "Pendiente (%)", "Ej: 8", when="mode=largo|alto"),
     ], chips=[("0,9 m de desnivel en 9 m", "mode=pend;unit=m;rise=0,9;run=9"), ("0,5 m con pendiente del 8 %", "mode=largo;unit=m;rise=0,5;pct=8"), ("5 m de largo al 8 %", "mode=alto;unit=m;run=5;pct=8"), ("Escalón de 18 cm en 1,5 m", "mode=pend;unit=cm;rise=18;run=150")],
         note="La longitud horizontal es la proyección sobre el piso, no el largo de la superficie inclinada."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Pendiente en porcentaje", f'<p {FORMULA}>pendiente % = desnivel / longitud horizontal × 100</p><p>Una pendiente del 10 % significa que se sube 10 cm por cada metro avanzado en horizontal. Una del 100 % equivale a 45°.</p>'),
         ("Pendiente en grados", f'<p {FORMULA}>ángulo = arctan(desnivel / longitud horizontal)</p><p>Los porcentajes y los grados no son proporcionales: 8 % son unos 4,6° y 12 %, unos 6,8°.</p>'),
         ("Accesibilidad", "<p>Para sillas de ruedas y carritos, las normas suelen fijar pendientes máximas de entre el 6 % y el 12 % según el largo del tramo, con descansos y pasamanos. Para un tramo largo conviene no pasar del 8 %. Consultá la normativa de tu zona.</p>"),
     ]),
     related=[("/calculadoras/hogar-y-construccion/calculadora-de-escaleras/", "Calculadora de Escaleras"), ("/calculadoras/matematicas-avanzadas/recta-y-distancia-entre-puntos/", "Recta y Distancia entre Puntos"),
              ("/calculadoras/matematicas-avanzadas/teorema-de-pitagoras/", "Teorema de Pitágoras")],
     guide=("/guias/como-calcular-la-pendiente-de-una-rampa/", "Cómo calcular la pendiente de una rampa", "Leé la guía completa: pendiente en % y grados, el largo necesario, accesibilidad y ejemplos."),
     faqs=[("¿Cómo se calcula la pendiente de una rampa?", "Dividiendo el desnivel por la longitud horizontal y multiplicando por 100. Una rampa que sube 0,9 m en 9 m tiene una pendiente del 10 %."),
           ("¿Qué largo necesita una rampa para salvar 50 cm con una pendiente del 8 %?", "50 cm ÷ 0,08 = 6,25 m de longitud horizontal."),
           ("¿Cuál es la pendiente máxima de una rampa accesible?", "Depende de la normativa y del largo del tramo; suele estar entre el 6 % y el 12 %, y para tramos largos, alrededor del 8 %."),
           ("¿Cómo paso de porcentaje a grados?", "Con la arcotangente: ángulo = arctan(pendiente / 100). Un 10 % equivale a 5,7°."),
           ("¿Es lo mismo la longitud horizontal que el largo de la rampa?", "No: el largo real es la hipotenusa, un poco mayor. Con 0,9 m de desnivel y 9 m horizontales, la rampa mide 9,04 m.")])
