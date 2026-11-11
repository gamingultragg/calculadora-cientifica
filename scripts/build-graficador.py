"""
build-graficador.py — Página del Graficador de Funciones (UI propia, sin el motor calc-simple) y su guía.
Generación de una sola vez: después, el HTML es la fuente de verdad.
"""
from spec_lib import (BTN, CHIP, FORMULA, INPUT, LABEL, MUTED, RESULT_H2, S, calc_page, g_formula, g_h2, g_p, g_steps, g_table, g_ul, guide_page,
                      help_blocks, write_guide, write_page)

COLORS = ["#2563eb", "#dc2626", "#16a34a"]
EX = [("x² − 4", "x^2-4"), ("seno", "sin(x)"), ("1/x", "1/x"), ("Parábola y recta", "x^2|2x+3"), ("Seno y coseno", "sin(x)|cos(x)"), ("Exponencial y logaritmo", "exp(x)|ln(x)"), ("Cúbica", "x^3-3x")]
chips = "".join(f'<button type="button" data-fn="{v}" {CHIP}>{l}</button>' for l, v in EX)


def fn_input(i):
    return f"""          <div>
            <label for="gf-f{i}" {LABEL}><span style="color:{COLORS[i - 1]}">●</span> Función {i}: f{i}(x) =</label>
            <input id="gf-f{i}" type="text" autocomplete="off" spellcheck="false" placeholder="{['Ej: x^2 - 4', 'Ej: 2x + 3 (opcional)', 'Opcional'][i - 1]}" {INPUT} />
          </div>"""


def range_input(id_, label, ph):
    return f"""            <div>
              <label for="gf-{id_}" {LABEL}>{label}</label>
              <input id="gf-{id_}" type="text" inputmode="decimal" placeholder="{ph}" {INPUT} />
            </div>"""


form = f"""        <div class="space-y-4">
{fn_input(1)}
{fn_input(2)}
{fn_input(3)}
          <div class="grid grid-cols-2 gap-3">
{range_input("xmin", "x mínimo", "-10")}
{range_input("xmax", "x máximo", "10")}
{range_input("ymin", "y mínimo (vacío = auto)", "auto")}
{range_input("ymax", "y máximo (vacío = auto)", "auto")}
          </div>
          <div class="flex flex-wrap gap-2" aria-label="Ejemplos">{chips}</div>
          <button id="gf-plot" type="button" {BTN}>Graficar</button>
          <p class="text-xs {MUTED}">Podés escribir <span class="font-numeric">2x</span> en vez de 2*x, usar <span class="font-numeric">^</span> para potencias y funciones como <span class="font-numeric">sen(x)</span>, <span class="font-numeric">cos(x)</span>, <span class="font-numeric">tan(x)</span>, <span class="font-numeric">sqrt(x)</span>, <span class="font-numeric">abs(x)</span>, <span class="font-numeric">ln(x)</span>, <span class="font-numeric">log(x)</span> y <span class="font-numeric">exp(x)</span>. Los ángulos van en radianes; <span class="font-numeric">pi</span> y <span class="font-numeric">e</span> son constantes.</p>
        </div>"""

result = f"""        <section id="gf-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
            <h2 {RESULT_H2.replace("mb-3", "mb-0")}>Gráfico</h2>
            <div class="flex flex-wrap gap-2">
              <button type="button" id="gf-zoom-in" class="cc-copy" aria-label="Acercar">＋ Acercar</button>
              <button type="button" id="gf-zoom-out" class="cc-copy" aria-label="Alejar">－ Alejar</button>
              <button type="button" id="gf-reset" class="cc-copy">Restablecer</button>
              <button type="button" id="gf-share" class="cc-copy">Copiar enlace</button>
            </div>
          </div>
          <canvas id="gf-canvas" class="w-full rounded-xl border border-[var(--color-border)] touch-none cursor-grab" style="height:380px" role="img" aria-label="Gráfico de las funciones ingresadas"></canvas>
          <p id="gf-cursor" class="mt-2 min-h-[1.25rem] text-xs font-numeric {MUTED}" aria-live="off"></p>
          <p class="text-xs {MUTED}">Arrastrá para desplazarte y usá la rueda del mouse (o los botones) para hacer zoom.</p>
          <ul id="gf-info" class="mt-4 space-y-3 text-sm {MUTED}"></ul>
          <div class="mt-4 text-sm">
            <label for="gf-eval" {LABEL}>Evaluar las funciones en x =</label>
            <input id="gf-eval" type="text" inputmode="decimal" placeholder="Ej: 3" {INPUT} />
            <p id="gf-eval-out" class="mt-2 font-numeric {MUTED}"></p>
          </div>
        </section>"""

write_page("calculadoras/matematicas-avanzadas/graficador-de-funciones", calc_page(
    cat_slug="matematicas-avanzadas", cat_label="Matemáticas Avanzadas",
    slug="graficador-de-funciones", name="Graficador de Funciones Online",
    page_title="Graficador de Funciones Online: Graficá f(x) y Encontrá los Ceros | Calculadora Científica",
    desc="Graficador de funciones online gratis: dibujá hasta tres funciones a la vez, hacé zoom y desplazate, evaluá en cualquier x y encontrá los ceros. Sin instalar nada.",
    og_title="Graficador de Funciones Online",
    og_desc="Graficá hasta 3 funciones, con zoom, ceros y evaluación en x. Gratis.",
    schema_desc="Grafica hasta tres funciones de una variable (polinómicas, trigonométricas, exponenciales, logarítmicas y más) con zoom y desplazamiento, calcula los ceros aproximados y evalúa las funciones en cualquier valor de x.",
    intro="Escribí una o varias funciones de x (como x^2 - 4, sen(x) o 1/x) y mirá su gráfico al instante. Hacé zoom, desplazate, evaluá en cualquier punto y encontrá los ceros de cada función.",
    form_html=form, result_html=result,
    help_html=help_blocks([
        ("Cómo escribir las funciones", f'<p>Usá <span class="font-numeric">x</span> como variable. Podés omitir el signo de multiplicar delante de x o de un paréntesis: <span class="font-numeric">2x</span>, <span class="font-numeric">3(x+1)</span>, <span class="font-numeric">(x+1)(x-1)</span>. Potencias con <span class="font-numeric">^</span>: <span class="font-numeric">x^3</span>. Decimales con coma o punto.</p>'),
        ("Funciones disponibles", "<p>sen (o sin), cos, tan, asin, acos, atan, sinh, cosh, tanh, sqrt (raíz cuadrada), cbrt (raíz cúbica), abs, ln (logaritmo natural), log (base 10), log2, exp, floor, ceil, round y sign. Constantes: pi y e. Los ángulos se miden en radianes.</p>"),
        ("Ceros y ordenada", "<p>Los ceros (o raíces) son los valores de x donde f(x) = 0, es decir, donde la curva corta el eje horizontal. Se calculan en el tramo visible. La ordenada al origen es f(0), donde corta el eje vertical.</p>"),
        ("Asíntotas y discontinuidades", "<p>En funciones como 1/x o tan(x) la curva \"salta\" cerca de los puntos donde no está definida: el graficador corta el trazo ahí para no unir ramas distintas.</p>"),
    ]),
    related=[("/calculadoras/matematicas-avanzadas/ecuaciones-segundo-grado/", "Ecuaciones de Segundo Grado"), ("/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/", "Calculadora Científica Online"),
             ("/calculadoras/estadistica/regresion-lineal/", "Regresión Lineal")],
    guide=("/guias/como-graficar-una-funcion/", "Cómo graficar una función", "Leé la guía completa: tipos de funciones, cómo hallar ceros, vértice y asíntotas, y cómo interpretar el gráfico."),
    faqs=[("¿Cómo grafico una función online?", "Escribí la función en el campo f(x) con la variable x, por ejemplo x^2 - 4, y tocá Graficar. Podés agregar hasta dos funciones más para compararlas."),
          ("¿Cómo escribo una potencia o una raíz?", "Con ^ para potencias (x^3) y sqrt(x) para la raíz cuadrada. La raíz cúbica es cbrt(x) o x^(1/3)."),
          ("¿Los ángulos están en grados o radianes?", "En radianes: sen(pi/2) = 1. Para usar grados, convertí con x*pi/180: sen(x*pi/180)."),
          ("¿Cómo encuentro las raíces de una función?", "Los ceros de cada función se calculan automáticamente en el tramo visible y aparecen debajo del gráfico; podés ampliar el rango de x para buscar más."),
          ("¿Puedo graficar varias funciones a la vez?", "Sí, hasta tres, cada una con su color: sirve para ver dónde se cortan.")],
))

# ------------------------------------------------------------------ guía
body = "\n\n".join([
    g_h2("1. Qué es graficar una función"),
    g_p("Graficar f(x) es dibujar todos los puntos (x, f(x)). Cada valor de x en el eje horizontal se asocia con su resultado en el eje vertical. La curva resultante muestra de un vistazo dónde crece, dónde decrece, dónde corta los ejes y qué valores alcanza."),
    g_h2("2. Los tipos de función más comunes"),
    g_table(["Función", "Forma", "Gráfico"], [["Lineal", "f(x) = m·x + b", "Una recta: m es la pendiente y b la ordenada al origen"], ["Cuadrática", "f(x) = a·x² + b·x + c", "Una parábola con vértice; abre hacia arriba si a > 0"],
                                              ["Cúbica", "f(x) = a·x³ + …", "Curva en S, hasta dos cambios de dirección"], ["Exponencial", "f(x) = aˣ", "Crece (o decrece) cada vez más rápido; nunca toca el eje x"],
                                              ["Logarítmica", "f(x) = ln(x)", "Crece despacio; solo existe para x > 0"], ["Racional", "f(x) = 1/x", "Dos ramas con asíntotas en los ejes"], ["Trigonométrica", "f(x) = sen(x)", "Onda periódica entre −1 y 1"]]),
    g_h2("3. Cómo encontrar los puntos importantes"),
    g_ul([S + "Ordenada al origen:</strong> el punto donde corta el eje y: se calcula f(0). Para x² − 4 es −4.", S + "Ceros o raíces:</strong> donde corta el eje x: se resuelve f(x) = 0. Para x² − 4 = 0, x = −2 y x = 2.", S + "Vértice de una parábola:</strong> en x = −b / (2a). Para x² − 4 está en x = 0, con y = −4 (el mínimo).", S + "Asíntotas:</strong> rectas a las que la curva se acerca sin tocarlas; en 1/x son los ejes."]),
    g_h2("4. Ejemplo: x² − 4"),
    g_steps(["Es una parábola (a = 1 > 0): abre hacia arriba", "Vértice: x = −b/(2a) = 0 → y = −4", "Ceros: x² = 4 → x = ±2", "Ordenada al origen: f(0) = −4"]),
    g_h2("5. Comparar dos funciones"),
    g_p("Para saber dónde se cortan f(x) = x² y g(x) = 2x + 3 se grafican juntas y se miran los puntos de cruce; algebraicamente se resuelve x² = 2x + 3, o sea x² − 2x − 3 = 0, con soluciones x = −1 y x = 3."),
    g_h2("6. Cómo leer un gráfico"),
    g_ul(["Donde la curva sube de izquierda a derecha, la función crece; donde baja, decrece.", "Los máximos y mínimos son los puntos donde cambia de sentido.", "Si la curva es simétrica respecto del eje y, la función es par (como x²); si lo es respecto del origen, es impar (como x³).", "Los \"saltos\" indican discontinuidades: valores de x donde la función no está definida."]),
    g_h2("7. Errores comunes"),
    g_ul(["Escribir 2x² como 2x^2 está bien, pero (2x)^2 es otra función: 4x².", "Usar grados en lugar de radianes en las funciones trigonométricas.", "Mirar un rango de x tan grande o tan chico que la forma de la curva se pierde: ajustá el zoom.", "Olvidar el dominio: ln(x) y sqrt(x) no existen para ciertos valores."]),
])
write_guide("como-graficar-una-funcion", guide_page(
    slug="como-graficar-una-funcion", name="Cómo graficar una función",
    page_title="Cómo Graficar una Función: Ceros, Vértice, Asíntotas y Ejemplos | Calculadora Científica",
    desc="Cómo graficar funciones lineales, cuadráticas, exponenciales y trigonométricas: ceros, vértice, ordenada al origen y asíntotas, con un ejemplo resuelto y cómo leer un gráfico.",
    og_desc="Cómo graficar funciones: tipos, puntos importantes y cómo leer el gráfico.",
    headline="Cómo graficar una función paso a paso",
    intro="Un gráfico muestra de un vistazo lo que una fórmula esconde: dónde sube, dónde baja y dónde corta los ejes. Esta guía explica los tipos de función, los puntos que conviene buscar y cómo interpretar la curva.",
    quick="Buscá la ordenada al origen f(0), los ceros (f(x) = 0), el vértice si es una parábola (x = −b/2a) y las asíntotas. Con esos puntos se esboza cualquier curva.",
    cta=("/calculadoras/matematicas-avanzadas/graficador-de-funciones/", "Abrir graficador"),
    body_html=body,
    faqs=[("¿Cómo se grafica una función?", "Se calculan varios puntos (x, f(x)) y se unen con una curva, marcando ceros, ordenada al origen, vértice y asíntotas."),
          ("¿Cómo se halla el vértice de una parábola?", "En x = −b/(2a); el valor de y se obtiene evaluando la función en ese x."),
          ("¿Qué son los ceros de una función?", "Los valores de x donde f(x) = 0: donde la curva corta el eje horizontal."),
          ("¿Qué es una asíntota?", "Una recta a la que la curva se acerca indefinidamente sin tocarla, como los ejes en 1/x.")],
    related=[("/calculadoras/matematicas-avanzadas/graficador-de-funciones/", "Graficador de Funciones"), ("/calculadoras/matematicas-avanzadas/ecuaciones-segundo-grado/", "Ecuaciones de Segundo Grado"),
             ("/guias/como-resolver-ecuaciones-de-segundo-grado/", "Guía: ecuaciones de segundo grado")],
))
