"""
build-batch-9.py — Calculadora de calorías y metabolismo basal (Vida Diaria) con su guía.
Generación de una sola vez: después, el HTML es la fuente de verdad.
"""
from spec_lib import (ENGINE, FORMULA, Lib, S, calc_page, g_formula, g_h2, g_p, g_steps, g_table, g_ul, guide_page, help_blocks, write_guide,
                      write_page)

L = Lib("ca")
write_page("calculadoras/vida-diaria/calculadora-de-calorias-y-metabolismo-basal", calc_page(
    pre_scripts=ENGINE, cat_slug="vida-diaria", cat_label="Vida Diaria",
    slug="calculadora-de-calorias-y-metabolismo-basal", name="Calculadora de Calorías y Metabolismo Basal",
    page_title="Calculadora de Calorías Diarias y Metabolismo Basal (TMB) | Calculadora Científica",
    desc="Calculá tu metabolismo basal (TMB) con la ecuación de Mifflin-St Jeor y cuántas calorías necesitás por día para mantener, bajar o subir de peso según tu actividad. Gratis.",
    og_title="Calculadora de Calorías y Metabolismo Basal",
    og_desc="Tu TMB y las calorías diarias para mantener, bajar o subir de peso. Gratis.",
    schema_desc="Calcula el metabolismo basal con la ecuación de Mifflin-St Jeor y las calorías diarias de mantenimiento según el nivel de actividad física, con estimaciones para bajar o subir de peso de forma gradual.",
    intro="Ingresá tu sexo, edad, peso, altura y nivel de actividad: obtenés tu metabolismo basal (las calorías que gasta tu cuerpo en reposo) y cuántas calorías necesitás por día para mantener, bajar o subir de peso.",
    form_html=L.form([
        L.sel("sex", "Sexo", [("mujer", "Mujer"), ("hombre", "Hombre")]),
        L.num("age", "Edad (años)", "Ej: 30", rule="int"),
        L.num("weight", "Peso (kg)", "Ej: 70"),
        L.num("height", "Altura (cm)", "Ej: 170"),
        L.sel("activity", "Nivel de actividad", [("sedentario", "Sedentario (poco o nada de ejercicio)"), ("ligero", "Ligero (1 a 3 días por semana)"), ("moderado", "Moderado (3 a 5 días por semana)"),
                                                   ("intenso", "Intenso (6 a 7 días por semana)"), ("muyintenso", "Muy intenso (trabajo físico o doble entrenamiento)")], value="ligero"),
    ], chips=[("Hombre, 30 años, 70 kg, 175 cm", "sex=hombre;age=30;weight=70;height=175;activity=moderado"), ("Mujer, 30 años, 60 kg, 165 cm", "sex=mujer;age=30;weight=60;height=165;activity=ligero")],
        note="Es una estimación para adultos sanos. No reemplaza la consulta con un médico o nutricionista."),
    result_html=L.panel(),
    help_html=help_blocks([
        ("Metabolismo basal (TMB)", f'<p {FORMULA}>TMB = 10·peso + 6,25·altura − 5·edad + 5 (hombres) / − 161 (mujeres)</p><p>Es la energía que el cuerpo necesita en reposo absoluto para mantener sus funciones vitales (respirar, circular la sangre, regular la temperatura). Ecuación de Mifflin-St Jeor, con peso en kg y altura en cm.</p>'),
        ("Gasto total diario", f'<p {FORMULA}>calorías de mantenimiento = TMB × factor de actividad</p><p>Factores: sedentario 1,2 · ligero 1,375 · moderado 1,55 · intenso 1,725 · muy intenso 1,9.</p>'),
        ("Bajar o subir de peso", "<p>Un déficit de unas 500 kcal por día equivale a bajar alrededor de medio kilo por semana; un superávit de 300 a 500 kcal permite subir gradualmente. Por seguridad no se recomienda comer menos de 1.200 kcal (mujeres) o 1.500 kcal (hombres) sin supervisión profesional.</p>"),
    ]),
    related=[("/calculadoras/vida-diaria/calculadora-de-imc/", "Calculadora de IMC"), ("/calculadoras/vida-diaria/conversor-de-cocina/", "Conversor de Cocina"),
             ("/calculadoras/fisica/energia-cinetica-y-potencial/", "Energía Cinética y Potencial")],
    guide=("/guias/como-calcular-el-metabolismo-basal-y-las-calorias-diarias/", "Cómo calcular el metabolismo basal y las calorías diarias", "Leé la guía completa: la fórmula, el factor de actividad y cómo usarlo para bajar, mantener o subir de peso."),
    faqs=[("¿Cómo se calcula el metabolismo basal?", "Con la ecuación de Mifflin-St Jeor: 10 × peso (kg) + 6,25 × altura (cm) − 5 × edad + 5 (hombres) o − 161 (mujeres). Un hombre de 30 años, 70 kg y 175 cm tiene un TMB de unas 1.649 kcal."),
          ("¿Cuántas calorías necesito por día?", "El TMB multiplicado por tu factor de actividad. Con actividad moderada (×1,55), el hombre del ejemplo necesita unas 2.556 kcal para mantener su peso."),
          ("¿Cuántas calorías hay que restar para bajar de peso?", "Un déficit de unas 500 kcal diarias equivale a bajar aproximadamente medio kilo por semana, sin bajar de 1.200 kcal (mujeres) o 1.500 kcal (hombres)."),
          ("¿Qué diferencia hay entre TMB y calorías de mantenimiento?", "El TMB es el gasto en reposo; las calorías de mantenimiento suman el gasto por movimiento y ejercicio."),
          ("¿Es exacta la calculadora?", "No: es una estimación. El metabolismo varía según la composición corporal, la genética, el sueño y otros factores. Consultá con un profesional.")],
))

body = "\n\n".join([
    g_h2("1. Qué es el metabolismo basal"),
    g_p("Es la energía mínima que tu cuerpo gasta en reposo, en ayunas y en un ambiente templado, solo para mantenerse vivo. Representa entre el 60 % y el 70 % del gasto energético total de la mayoría de las personas."),
    g_h2("2. La fórmula de Mifflin-St Jeor"),
    g_formula("TMB = 10 · peso (kg) + 6,25 · altura (cm) − 5 · edad + <em>s</em>"),
    g_p("Con s = +5 para hombres y s = −161 para mujeres. Es la ecuación más validada para adultos y la que recomiendan muchas guías de nutrición."),
    g_steps(["Hombre, 30 años, 70 kg, 175 cm", "10 × 70 = 700 · 6,25 × 175 = 1.093,75 · 5 × 30 = 150", "TMB = 700 + 1.093,75 − 150 + 5 = 1.648,75 ≈ 1.649 kcal/día"]),
    g_steps(["Mujer, 30 años, 60 kg, 165 cm", "600 + 1.031,25 − 150 − 161 = 1.320,25 ≈ 1.320 kcal/día"]),
    g_h2("3. El factor de actividad"),
    g_table(["Nivel", "Factor"], [["Sedentario (casi sin ejercicio)", "1,2"], ["Ligero (1 a 3 días por semana)", "1,375"], ["Moderado (3 a 5 días)", "1,55"], ["Intenso (6 a 7 días)", "1,725"], ["Muy intenso (trabajo físico o doble turno)", "1,9"]]),
    g_p("Las calorías de mantenimiento son el TMB por el factor. Para el hombre del ejemplo con actividad moderada: 1.649 × 1,55 = " + S + "2.556 kcal por día</strong>."),
    g_h2("4. Bajar, mantener o subir de peso"),
    g_ul(["Mantener: las calorías de mantenimiento.", "Bajar: restar unas 500 kcal por día equivale a bajar alrededor de medio kilo por semana (un kilo de grasa son unas 7.700 kcal). No bajar de 1.200 kcal (mujeres) o 1.500 kcal (hombres) sin supervisión profesional.", "Subir: sumar 300 a 500 kcal por día, con proteínas y entrenamiento de fuerza si el objetivo es ganar masa muscular."]),
    g_h2("5. Límites de la estimación"),
    g_ul(["No distingue entre masa muscular y grasa: a igual peso, quien tiene más músculo gasta más.", "No aplica a menores de 15 años, embarazadas ni personas con enfermedades metabólicas.", "El gasto real cambia con el tiempo: conviene recalcular cada vez que cambia el peso y observar la evolución durante 2 a 3 semanas para ajustar."]),
    g_h2("6. Errores comunes"),
    g_ul(["Elegir un nivel de actividad más alto del real, que sobreestima las calorías.", "Hacer déficits extremos que enlentecen el metabolismo y no se sostienen.", "Tomar el resultado como una cifra exacta en vez de un punto de partida."]),
])
write_guide("como-calcular-el-metabolismo-basal-y-las-calorias-diarias", guide_page(
    slug="como-calcular-el-metabolismo-basal-y-las-calorias-diarias", name="Cómo calcular el metabolismo basal y las calorías diarias",
    page_title="Cómo Calcular el Metabolismo Basal y las Calorías Diarias (Mifflin-St Jeor) | Calculadora Científica",
    desc="Cómo calcular el metabolismo basal con la fórmula de Mifflin-St Jeor y las calorías diarias de mantenimiento con el factor de actividad, con ejemplos para bajar, mantener o subir de peso.",
    og_desc="Metabolismo basal y calorías diarias con la fórmula de Mifflin-St Jeor, con ejemplos.",
    headline="Cómo calcular el metabolismo basal y las calorías diarias",
    intro="Saber cuántas calorías gasta tu cuerpo es el punto de partida para cualquier plan de alimentación. Esta guía explica la fórmula más usada para estimar el metabolismo basal y cómo convertirlo en las calorías que necesitás por día.",
    quick="TMB = 10·peso + 6,25·altura − 5·edad + 5 (hombres) o − 161 (mujeres). Calorías de mantenimiento = TMB × factor de actividad (1,2 a 1,9).",
    cta=("/calculadoras/vida-diaria/calculadora-de-calorias-y-metabolismo-basal/", "Abrir calculadora"),
    body_html=body,
    faqs=[("¿Cómo se calcula el metabolismo basal?", "Con 10·peso + 6,25·altura − 5·edad + 5 (hombres) o − 161 (mujeres)."),
          ("¿Qué factor de actividad uso?", "Sedentario 1,2; ligero 1,375; moderado 1,55; intenso 1,725; muy intenso 1,9."),
          ("¿Cuántas calorías restar para bajar de peso?", "Unas 500 por día para bajar medio kilo por semana, sin bajar de los mínimos de seguridad."),
          ("¿Es una cifra exacta?", "No: es una estimación orientativa. Consultá con un profesional de la salud.")],
    related=[("/calculadoras/vida-diaria/calculadora-de-calorias-y-metabolismo-basal/", "Calculadora de Calorías"), ("/calculadoras/vida-diaria/calculadora-de-imc/", "Calculadora de IMC"),
             ("/guias/como-calcular-el-imc/", "Guía: cómo calcular el IMC")],
))
