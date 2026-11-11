"""
build-batch-6.py — Genera las 10 calculadoras del lote 6 (motor común calc-simple.js):
  Finanzas: cuotas vs contado, inflación acumulada, ajuste de alquiler, margen y markup, descuentos sucesivos.
  Hogar y Construcción (categoría nueva): cerámicos, pintura, ladrillos, hormigón y consumo eléctrico.
Generación de una sola vez: después, el HTML de cada página es la fuente de verdad.
"""
from spec_lib import ENGINE, FORMULA, Lib, calc_page, help_blocks, write_page

FIN = dict(cat_slug="finanzas", cat_label="Finanzas")
HOG = dict(cat_slug="hogar-y-construccion", cat_label="Hogar y Construcción")


def page(rel, L, cat, **kw):
    guide = kw.pop("guide")
    write_page(rel, calc_page(pre_scripts=ENGINE, guide=guide, **cat, **kw))


# ============================================================ cuotas vs contado
L = Lib("cv")
page("calculadoras/finanzas/cuotas-vs-contado", L, FIN,
     slug="cuotas-vs-contado", name="Calculadora de Cuotas vs Contado",
     page_title="Calculadora de Cuotas vs Contado: Cuánto Interés Pagás Realmente | Calculadora Científica",
     desc="Descubrí la tasa de interés real de comprar en cuotas: recargo total, tasa mensual (TEM), TNA y TEA, y si conviene más pagar de contado o financiado según la inflación.",
     og_title="Calculadora de Cuotas vs Contado",
     og_desc="La tasa real de comprar en cuotas y si conviene más que el contado. Gratis.",
     schema_desc="Calcula la tasa de interés implícita de una compra en cuotas iguales (TEM, TNA y TEA), el recargo sobre el precio de contado y compara con la inflación para ver si conviene financiar.",
     intro="Ingresá el precio de contado, la cantidad de cuotas y el valor de cada una: te muestro cuánto más pagás en total, la tasa mensual real que te están cobrando y, si querés, si conviene financiar según la inflación.",
     form_html=L.form([
         L.num("cash", "Precio de contado ($)", "Ej: 300000"),
         L.num("n", "Cantidad de cuotas", "Ej: 12", rule="int"),
         L.num("payment", "Valor de cada cuota ($)", "Ej: 32000"),
         L.num("infl", "Inflación mensual esperada (%) — opcional", "Ej: 4", opt=True, rule="nonneg", hint="Sirve para ver si financiar te conviene frente al contado."),
     ], chips=[("$300.000 en 12 cuotas de $32.000", "cash=300000;n=12;payment=32000;infl="), ("$100.000 en 6 cuotas de $20.000", "cash=100000;n=6;payment=20000;infl=3")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Cómo se calcula la tasa real", f'<p {FORMULA}>precio de contado = cuota × (1 − (1 + i)^−n) / i</p><p>Es la tasa que iguala el valor de las cuotas con el precio de contado. Se despeja i por aproximaciones sucesivas. i es la tasa mensual (TEM); la TEA es (1 + i)^12 − 1.</p>'),
         ("Recargo vs tasa", "<p>El recargo total (por ejemplo 28 %) no es la tasa de interés: se reparte en el tiempo y las cuotas se van pagando de a poco, por eso la tasa mensual real es más alta de lo que parece al dividir el recargo por la cantidad de cuotas.</p>"),
         ("¿Conviene financiar?", "<p>Si la inflación mensual es mayor que la tasa implícita, pagar en cuotas te ahorra plata en valor de hoy (siempre que el dinero que no pagás al contado lo conserves invertido a ese ritmo). Si es menor, conviene el contado. Se compara el valor presente de las cuotas con el precio de contado.</p>"),
         ("Qué incluye", "<p>Se asume que las cuotas son iguales y se pagan al final de cada mes. No incluye gastos administrativos, seguros ni impuestos de financiación: si el comercio los cobra aparte, sumalos al valor de la cuota.</p>"),
     ]),
     related=[("/calculadoras/finanzas/amortizacion-prestamos/", "Amortización de Préstamos"), ("/calculadoras/finanzas/calculadora-de-plazo-fijo/", "Calculadora de Plazo Fijo y Tasas"),
              ("/calculadoras/finanzas/calculadora-de-inflacion-acumulada/", "Calculadora de Inflación Acumulada")],
     guide=("/guias/cuotas-o-contado-como-saber-cual-conviene/", "Cuotas o contado: cómo saber cuál conviene", "Leé la guía completa: la tasa real de una compra en cuotas, cuándo conviene financiar y cómo compararlo con la inflación."),
     faqs=[("¿Cómo sé qué tasa me cobran en cuotas?", "Calculando la tasa que iguala el valor de las cuotas al precio de contado. Con 12 cuotas de $32.000 por un producto de $300.000, es aproximadamente 4 % mensual (4,02 %)."),
           ("¿Conviene comprar en cuotas o de contado?", "Depende de la inflación: si el aumento mensual de precios supera la tasa implícita de las cuotas, financiar sale más barato en valor de hoy. Si el comercio te hace descuento por pagar de contado, hay que compararlo con la tasa implícita."),
           ("¿Qué diferencia hay entre TEM, TNA y TEA?", "La TEM es la tasa efectiva mensual; la TNA es la TEM multiplicada por 12 (nominal); la TEA es la tasa efectiva anual, que incluye la capitalización: (1 + TEM)^12 − 1."),
           ("¿Las cuotas sin interés no tienen interés?", "Si el precio en cuotas es igual al de contado, la tasa es 0 %. Pero a veces el precio \"de lista\" ya incluye el recargo y el contado tiene descuento: en ese caso la calculadora te muestra la tasa real."),
           ("¿Incluye el costo financiero total (CFT)?", "No: calcula la tasa implícita con los datos que cargás. El CFT del banco puede sumar seguros, comisiones e impuestos; si los conocés, agregalos al valor de la cuota.")])

# ============================================================ inflación acumulada
L = Lib("ia")
page("calculadoras/finanzas/calculadora-de-inflacion-acumulada", L, FIN,
     slug="calculadora-de-inflacion-acumulada", name="Calculadora de Inflación Acumulada",
     page_title="Calculadora de Inflación Acumulada: Compuestá las Inflaciones Mensuales | Calculadora Científica",
     desc="Calculá la inflación acumulada de varios meses a partir de los porcentajes mensuales, el promedio mensual, la inflación anualizada y cuánto necesitás hoy para mantener tu poder de compra.",
     og_title="Calculadora de Inflación Acumulada",
     og_desc="Inflación acumulada, promedio mensual y anualizada a partir de los datos mensuales. Gratis.",
     schema_desc="Calcula la inflación acumulada componiendo las inflaciones mensuales, el promedio mensual geométrico, la inflación anualizada y el monto actualizado para mantener el poder adquisitivo.",
     intro="Pegá las inflaciones mensuales (por ejemplo, las del INDEC) y obtené la inflación acumulada del período, el promedio mensual, la anualizada y cuánto necesitás hoy para mantener el poder de compra de un monto anterior.",
     form_html=L.form([
         L.text("rates", "Inflaciones mensuales (%)", "Ej: 4,2 3,7 2,9 3,5", rows=4, hint="Separadas por espacios, saltos de línea o punto y coma. Usá coma o punto para los decimales."),
         L.num("amount", "Monto de referencia ($) — opcional", "Ej: 100000", opt=True),
     ], chips=[("Seis meses de ejemplo", "rates=4,2 3,7 2,9 3,5 2,8 2,4;amount=100000"), ("Doce meses al 3 %", "rates=3 3 3 3 3 3 3 3 3 3 3 3;amount=")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Por qué no se suman", f'<p {FORMULA}>acumulada = (1 + r₁) × (1 + r₂) × … × (1 + rₙ) − 1</p><p>Cada mes la inflación se aplica sobre precios que ya subieron, así que los porcentajes se multiplican (se componen), no se suman. Dos meses al 10 % acumulan 21 %, no 20 %.</p>'),
         ("Promedio mensual y anualizada", f'<p {FORMULA}>promedio = (1 + acumulada)^(1/n) − 1 &nbsp;·&nbsp; anualizada = (1 + promedio)^12 − 1</p><p>El promedio geométrico es la inflación mensual constante que daría la misma acumulada. La anualizada proyecta ese ritmo a doce meses.</p>'),
         ("Mantener el poder de compra", "<p>Para que un monto de antes compre lo mismo hoy hay que multiplicarlo por (1 + acumulada). Es la base de cualquier actualización de precios o salarios.</p>"),
         ("De dónde sacar los datos", "<p>Los índices mensuales de precios al consumidor los publica el INDEC. La calculadora no consulta datos externos: cargá los porcentajes que quieras componer.</p>"),
     ]),
     related=[("/calculadoras/finanzas/cuotas-vs-contado/", "Cuotas vs Contado"), ("/calculadoras/finanzas/calculadora-de-ajuste-de-alquiler/", "Calculadora de Ajuste de Alquiler"),
              ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes")],
     guide=("/guias/como-calcular-la-inflacion-acumulada/", "Cómo calcular la inflación acumulada", "Leé la guía completa: por qué los porcentajes se componen, cómo anualizar y cómo actualizar un monto por inflación."),
     faqs=[("¿Cómo se calcula la inflación acumulada?", "Multiplicando (1 + inflación mensual) de cada mes y restando 1. Con 4 %, 3 % y 2 %: 1,04 × 1,03 × 1,02 − 1 = 9,3 %."),
           ("¿Por qué no se puede sumar la inflación de cada mes?", "Porque cada mes se aplica sobre precios que ya aumentaron. Sumar subestima el total: dos meses al 10 % dan 21 %, no 20 %."),
           ("¿Cómo se anualiza una inflación mensual?", "Elevando (1 + inflación mensual) a la 12 y restando 1. Una inflación constante del 3 % mensual equivale a 42,6 % anual."),
           ("¿Cómo actualizo un monto por inflación?", "Multiplicándolo por (1 + inflación acumulada). Si la acumulada es 20 %, $100.000 pasan a $120.000."),
           ("¿Qué es el poder adquisitivo perdido?", "Es cuánto menos compra la misma plata: 1 − 1/(1 + acumulada). Con 25 % de inflación acumulada, perdés un 20 % de poder de compra.")])

# ============================================================ ajuste de alquiler
L = Lib("al")
page("calculadoras/finanzas/calculadora-de-ajuste-de-alquiler", L, FIN,
     slug="calculadora-de-ajuste-de-alquiler", name="Calculadora de Ajuste de Alquiler",
     page_title="Calculadora de Ajuste de Alquiler: Por Índice o Porcentaje | Calculadora Científica",
     desc="Calculá cuánto pasa a costar tu alquiler con el ajuste de tu contrato: por índice (ICL, IPC, CER u otro) o por porcentaje de aumento. Gratis y sin registro.",
     og_title="Calculadora de Ajuste de Alquiler",
     og_desc="Nuevo valor del alquiler por índice o porcentaje. Gratis.",
     schema_desc="Calcula el nuevo valor de un alquiler según el ajuste del contrato, ya sea por la variación de un índice (valor final sobre valor inicial) o por un porcentaje de aumento.",
     intro="Elegí cómo se ajusta tu contrato: por la variación de un índice (cargás el valor al inicio y al momento del ajuste) o por un porcentaje fijo. Obtenés el nuevo alquiler y el aumento.",
     form_html=L.form([
         L.sel("mode", "El ajuste es por…", [("indice", "Variación de un índice"), ("pct", "Porcentaje de aumento")]),
         L.num("rent", "Alquiler actual ($)", "Ej: 400000"),
         L.num("i0", "Valor del índice al inicio / último ajuste", "Ej: 1,5231", when="mode=indice"),
         L.num("i1", "Valor del índice hoy", "Ej: 1,9842", when="mode=indice"),
         L.num("pct", "Aumento (%)", "Ej: 25", when="mode=pct", rule="nonneg"),
     ], chips=[("Por índice", "mode=indice;rent=400000;i0=1,5231;i1=1,9842"), ("Aumento del 25 %", "mode=pct;rent=400000;pct=25")],
         note="Los valores del índice los publica el organismo que corresponda a tu contrato (BCRA para el ICL, INDEC para el IPC, etc.): cargalos tal como figuran."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Ajuste por índice", f'<p {FORMULA}>nuevo alquiler = alquiler actual × índice final / índice inicial</p><p>Sirve para el ICL, el IPC, el CER, el índice Casa Propia o cualquier índice que tu contrato indique. El resultado es el mismo que aplicar la variación porcentual del índice.</p>'),
         ("Ajuste por porcentaje", f'<p {FORMULA}>nuevo alquiler = alquiler actual × (1 + aumento / 100)</p><p>Para contratos que fijan aumentos porcentuales (por ejemplo, 25 % cada seis meses).</p>'),
         ("Qué hay que mirar del contrato", "<p>La frecuencia del ajuste (trimestral, semestral, anual), el índice o porcentaje pactado y desde qué fecha se toma el valor inicial. La ley vigente y lo que firmaron las partes mandan: esta calculadora hace solo la cuenta.</p>"),
     ]),
     related=[("/calculadoras/finanzas/calculadora-de-inflacion-acumulada/", "Calculadora de Inflación Acumulada"), ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes"),
              ("/calculadoras/finanzas/cuotas-vs-contado/", "Cuotas vs Contado")],
     guide=("/guias/como-calcular-el-ajuste-de-un-alquiler/", "Cómo calcular el ajuste de un alquiler", "Leé la guía completa: ajuste por índice y por porcentaje, con ejemplos y qué revisar en tu contrato."),
     faqs=[("¿Cómo se calcula el aumento del alquiler por índice?", "Multiplicando el alquiler actual por el índice final y dividiendo por el índice inicial. Con un índice que pasó de 1,5 a 1,8 y un alquiler de $100.000: 100.000 × 1,8 / 1,5 = $120.000."),
           ("¿Cómo calculo un aumento del 25 %?", "Multiplicando el alquiler por 1,25. Un alquiler de $400.000 pasa a $500.000."),
           ("¿Qué índice usa mi contrato?", "El que figure en la cláusula de actualización. Puede ser el ICL, el IPC, el CER, el Casa Propia, un promedio de índices o un porcentaje fijo."),
           ("¿La calculadora busca el valor del índice?", "No: tenés que cargar los valores del índice. Así sirve para cualquier índice y no depende de datos externos."),
           ("¿Cada cuánto se ajusta el alquiler?", "Lo define el contrato. Es habitual el ajuste trimestral, cuatrimestral, semestral o anual; consultá tu contrato y la normativa vigente.")])

# ============================================================ margen y markup
L = Lib("mk")
page("calculadoras/finanzas/calculadora-de-margen-y-markup", L, FIN,
     slug="calculadora-de-margen-y-markup", name="Calculadora de Margen y Markup",
     page_title="Calculadora de Margen y Markup: Precio de Venta y Ganancia | Calculadora Científica",
     desc="Calculá el precio de venta a partir del costo y el margen o el markup que querés ganar, o el margen y el markup de un precio ya definido. Con IVA. Gratis.",
     og_title="Calculadora de Margen y Markup",
     og_desc="Precio de venta, margen y markup a partir del costo. Gratis.",
     schema_desc="Calcula el precio de venta con un margen o markup deseado, o el margen y el markup que resultan de un costo y un precio, con la ganancia por unidad y el precio con IVA.",
     intro="Elegí qué necesitás: el precio de venta para ganar un margen sobre el precio, el precio para ganar un markup sobre el costo, o el margen y markup de un precio que ya fijaste.",
     form_html=L.form([
         L.sel("mode", "¿Qué querés calcular?", [("margen", "Precio con un margen deseado"), ("markup", "Precio con un markup deseado"), ("calc", "Margen y markup de un precio")]),
         L.num("cost", "Costo por unidad ($)", "Ej: 6000"),
         L.num("margin", "Margen deseado (%)", "Ej: 40", when="mode=margen", rule="nonneg"),
         L.num("markup", "Markup deseado (%)", "Ej: 66,7", when="mode=markup", rule="nonneg"),
         L.num("price", "Precio de venta ($)", "Ej: 10000", when="mode=calc"),
     ], chips=[("Costo $6.000, margen 40 %", "mode=margen;cost=6000;margin=40"), ("Costo $6.000, markup 50 %", "mode=markup;cost=6000;markup=50"), ("Costo $6.000, precio $10.000", "mode=calc;cost=6000;price=10000")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Margen vs markup", f'<p {FORMULA}>margen = (precio − costo) / precio &nbsp;·&nbsp; markup = (precio − costo) / costo</p><p>Son dos formas de medir la misma ganancia: el margen la compara con el precio de venta y el markup con el costo. Un margen del 40 % equivale a un markup de 66,7 %.</p>'),
         ("Precio a partir del margen", f'<p {FORMULA}>precio = costo / (1 − margen)</p><p>Con un costo de $6.000 y un margen del 40 %: 6.000 / 0,6 = $10.000. El margen no puede ser 100 % ni más.</p>'),
         ("Precio a partir del markup", f'<p {FORMULA}>precio = costo × (1 + markup)</p><p>Con un costo de $6.000 y un markup del 50 %: 6.000 × 1,5 = $9.000.</p>'),
         ("Error frecuente", "<p>Sumar el margen al costo (costo × 1,40) da un margen real menor al 40 %: ese cálculo es un markup. Si lo que querés es ganar un 40 % del precio de venta, usá la fórmula del margen.</p>"),
     ]),
     related=[("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes"), ("/calculadoras/finanzas/calculadora-de-iva/", "Calculadora de IVA"),
              ("/calculadoras/finanzas/descuentos-sucesivos/", "Descuentos Sucesivos")],
     guide=("/guias/diferencia-entre-margen-y-markup/", "Diferencia entre margen y markup", "Leé la guía completa: las dos fórmulas, cómo pasar de una a otra y cómo fijar el precio de venta sin equivocarte."),
     faqs=[("¿Cuál es la diferencia entre margen y markup?", "El margen es la ganancia sobre el precio de venta y el markup es la ganancia sobre el costo. Con costo $6.000 y precio $10.000: ganancia $4.000, margen 40 % y markup 66,7 %."),
           ("¿Cómo calculo el precio de venta con un margen del 30 %?", "Dividiendo el costo por 0,70 (1 − 0,30). Con un costo de $7.000: 7.000 / 0,7 = $10.000."),
           ("¿Cómo calculo el precio con un markup del 30 %?", "Multiplicando el costo por 1,30. Con un costo de $7.000: $9.100."),
           ("¿Puede el margen ser del 100 %?", "No: un margen del 100 % implicaría un costo cero. El margen siempre es menor al 100 %; el markup, en cambio, puede superar el 100 %."),
           ("¿Incluye el IVA?", "El cálculo se hace sobre precio neto; la calculadora muestra además cuánto sería el precio con IVA 21 %.")])

# ============================================================ descuentos sucesivos
L = Lib("dsc")
page("calculadoras/finanzas/descuentos-sucesivos", L, FIN,
     slug="descuentos-sucesivos", name="Calculadora de Descuentos Sucesivos",
     page_title="Calculadora de Descuentos Sucesivos: Precio Final y Descuento Total | Calculadora Científica",
     desc="Calculá el precio final cuando se aplican varios descuentos seguidos (20 % + 10 % + 5 %) y el descuento total real. Con el detalle de cada paso. Gratis.",
     og_title="Calculadora de Descuentos Sucesivos",
     og_desc="Precio final y descuento total de varios descuentos encadenados. Gratis.",
     schema_desc="Calcula el precio final al aplicar varios descuentos porcentuales encadenados, el descuento total equivalente y el detalle de cada paso.",
     intro="Ingresá el precio y los descuentos que se aplican uno después del otro (promoción más cupón más pago en efectivo, por ejemplo) y obtené el precio final y el descuento total real.",
     form_html=L.form([
         L.num("price", "Precio inicial ($)", "Ej: 50000"),
         L.text("discounts", "Descuentos sucesivos (%)", "Ej: 20 10 5", hint="Separados por espacios o punto y coma, en el orden en que se aplican."),
     ], chips=[("20 % + 10 % + 5 %", "price=50000;discounts=20 10 5"), ("30 % + 10 %", "price=100000;discounts=30 10")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Cómo se aplican", f'<p {FORMULA}>precio final = precio × (1 − d₁) × (1 − d₂) × … × (1 − dₙ)</p><p>Cada descuento se calcula sobre el precio que ya quedó después del anterior, por eso no se suman los porcentajes.</p>'),
         ("Descuento total equivalente", f'<p {FORMULA}>total = 1 − (1 − d₁) × (1 − d₂) × …</p><p>Con 20 %, 10 % y 5 % el total es 31,6 % y no 35 %. Cuantos más descuentos, mayor la diferencia con la suma.</p>'),
         ("El orden no cambia el resultado", "<p>Multiplicar es conmutativo: aplicar primero el 10 % y después el 20 % da el mismo precio final que al revés. Lo que sí cambia es el monto de cada paso.</p>"),
     ]),
     related=[("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes"), ("/calculadoras/finanzas/calculadora-de-margen-y-markup/", "Calculadora de Margen y Markup"),
              ("/calculadoras/finanzas/calculadora-de-iva/", "Calculadora de IVA")],
     guide=("/guias/como-calcular-descuentos-sucesivos/", "Cómo calcular descuentos sucesivos", "Leé la guía completa: por qué no se suman los porcentajes, cómo pasar a un descuento único equivalente y ejemplos con promociones."),
     faqs=[("¿20 % más 10 % de descuento es 30 %?", "No: es 28 %. El segundo descuento se calcula sobre el precio ya rebajado: 1 − 0,80 × 0,90 = 0,28."),
           ("¿Cómo calculo dos descuentos seguidos?", "Multiplicando el precio por (1 − primer descuento) y después por (1 − segundo descuento). Con $100.000, 30 % y 10 %: 100.000 × 0,7 × 0,9 = $63.000."),
           ("¿Importa el orden de los descuentos?", "No para el precio final, que es el mismo en cualquier orden. Solo cambian los montos intermedios."),
           ("¿Cómo paso varios descuentos a uno solo?", "Calculando el descuento total equivalente: 1 − (1 − d₁) × (1 − d₂) × …. Con 20 % y 10 % equivale a un único descuento del 28 %."),
           ("¿Sirve para aumentos sucesivos?", "La lógica es la misma, pero esta calculadora acepta solo descuentos (entre 0 y 99,99 %). Para aumentos usá la calculadora de inflación acumulada.")])

# ============================================================ cerámicos
L = Lib("ce")
page("calculadoras/hogar-y-construccion/calculadora-de-ceramicos", L, HOG,
     slug="calculadora-de-ceramicos", name="Calculadora de Cerámicos y Pisos",
     page_title="Calculadora de Cerámicos: Cuántas Piezas y Cajas Necesito | Calculadora Científica",
     desc="Calculá cuántos cerámicos, porcelanatos o pisos comprar para tu ambiente según las medidas y el tamaño de la pieza, con porcentaje de desperdicio y cantidad de cajas. Gratis.",
     og_title="Calculadora de Cerámicos y Pisos",
     og_desc="Cuántas piezas y cajas comprar según el ambiente y la pieza, con desperdicio. Gratis.",
     schema_desc="Calcula la cantidad de cerámicos, porcelanatos o pisos necesarios para cubrir un ambiente a partir de sus medidas y las dimensiones de la pieza, considerando el desperdicio por cortes y la cantidad de cajas.",
     intro="Ingresá el largo y el ancho del ambiente y el tamaño de cada pieza: te digo cuántas piezas y cuántos metros cuadrados tenés que comprar, con el desperdicio por cortes y roturas.",
     form_html=L.form([
         L.num("length", "Largo del ambiente (m)", "Ej: 4,5"),
         L.num("width", "Ancho del ambiente (m)", "Ej: 3,2"),
         L.num("skip", "Superficie a descontar (m²) — opcional", "Ej: 1,2", opt=True, rule="nonneg", hint="Por ejemplo, una zona que no se cubre."),
         L.num("plen", "Largo de la pieza (cm)", "Ej: 60"),
         L.num("pwid", "Ancho de la pieza (cm)", "Ej: 60"),
         L.num("waste", "Desperdicio (%)", "10", opt=True, default=10, rule="nonneg", value="10", hint="10 % es lo habitual; 15 % si se coloca en diagonal o con diseño."),
         L.num("box", "Piezas por caja — opcional", "Ej: 4", opt=True, rule="int"),
     ], chips=[("Living 4,5 × 3,2 con piezas de 60 × 60", "length=4,5;width=3,2;plen=60;pwid=60;waste=10;box=4"), ("Baño 2 × 1,8 con piezas de 30 × 30", "length=2;width=1,8;plen=30;pwid=30;waste=10;box=")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("La cuenta", f'<p {FORMULA}>piezas = (largo × ancho × (1 + desperdicio)) / superficie de la pieza</p><p>Se redondea hacia arriba, porque no se compran piezas partidas. Una pieza de 60 × 60 cm cubre 0,36 m².</p>'),
         ("Por qué el desperdicio", "<p>Los cortes en los bordes, las roturas y los errores de colocación hacen que haga falta más material que la superficie exacta. Lo habitual es 10 %; en diagonal, pisos con diseño o ambientes con muchos recortes, 15 %.</p>"),
         ("Conviene comprar de más", "<p>Comprá todo junto y de un mismo lote: el tono y el calibre varían entre partidas y, si más adelante se rompe una pieza, es útil tener repuesto.</p>"),
     ]),
     related=[("/calculadoras/hogar-y-construccion/calculadora-de-pintura/", "Calculadora de Pintura"), ("/calculadoras/matematicas-avanzadas/calculadora-de-areas-y-volumenes/", "Calculadora de Áreas y Volúmenes"),
              ("/calculadoras/hogar-y-construccion/calculadora-de-ladrillos/", "Calculadora de Ladrillos")],
     guide=("/guias/cuantos-ceramicos-necesito/", "Cuántos cerámicos necesito", "Leé la guía completa: cómo medir el ambiente, calcular piezas y cajas, y cuánto desperdicio prever."),
     faqs=[("¿Cuántos cerámicos necesito para 20 m²?", "Con piezas de 60 × 60 cm (0,36 m²) y 10 % de desperdicio: 20 × 1,1 / 0,36 = 62 piezas."),
           ("¿Cuánto desperdicio debo calcular?", "Un 10 % en colocación recta y hasta un 15 % en diagonal o con muchos cortes."),
           ("¿Cómo calculo cuántas cajas comprar?", "Dividí las piezas por las que trae cada caja y redondeá hacia arriba. Muchas cajas vienen en m²: dividí los m² que necesitás por los de la caja."),
           ("¿Sirve para porcelanato, pisos flotantes o revestimientos?", "Sí, para cualquier pieza rectangular: solo cambian las medidas de la pieza."),
           ("¿Qué hago con los huecos como puertas?", "Descontá su superficie en el campo opcional; los cortes en los bordes se cubren con el desperdicio.")])

# ============================================================ pintura
L = Lib("pi")
page("calculadoras/hogar-y-construccion/calculadora-de-pintura", L, HOG,
     slug="calculadora-de-pintura", name="Calculadora de Pintura",
     page_title="Calculadora de Pintura: Cuántos Litros Necesito para una Habitación | Calculadora Científica",
     desc="Calculá cuántos litros de pintura necesitás para las paredes y el techo de una habitación según las medidas, las manos y el rendimiento, y qué latas comprar. Gratis.",
     og_title="Calculadora de Pintura",
     og_desc="Litros de pintura y latas para paredes y techo. Gratis.",
     schema_desc="Calcula los litros de pintura necesarios para las paredes y el techo de una habitación a partir de sus medidas, la superficie de aberturas, la cantidad de manos y el rendimiento, y sugiere la combinación de latas.",
     intro="Ingresá las medidas de la habitación, cuántas manos vas a dar y el rendimiento de tu pintura: te digo cuántos litros hacen falta y qué latas conviene comprar.",
     form_html=L.form([
         L.num("length", "Largo de la habitación (m)", "Ej: 4"),
         L.num("width", "Ancho de la habitación (m)", "Ej: 3"),
         L.num("height", "Alto de las paredes (m)", "Ej: 2,6", value="2.6"),
         L.num("openings", "Aberturas a descontar (m²) — opcional", "Ej: 3,5", opt=True, rule="nonneg", hint="Puertas y ventanas: una puerta común son unos 1,6 m²; una ventana, 1 a 2 m²."),
         L.sel("ceiling", "¿Pintás también el techo?", [("no", "No, solo paredes"), ("si", "Sí, paredes y techo")]),
         L.num("coats", "Manos", "2", rule="int", value="2"),
         L.num("yield", "Rendimiento (m² por litro y por mano)", "10", value="10", hint="Está en la etiqueta del producto: el látex rinde entre 8 y 12 m²/L por mano."),
     ], chips=[("Dormitorio 4 × 3 con techo", "length=4;width=3;height=2,6;openings=3,5;ceiling=si;coats=2;yield=10"), ("Living 6 × 4, solo paredes", "length=6;width=4;height=2,6;openings=6;ceiling=no;coats=2;yield=10")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Superficie a pintar", f'<p {FORMULA}>paredes = 2 × (largo + ancho) × alto − aberturas &nbsp;·&nbsp; techo = largo × ancho</p><p>Se descuentan puertas y ventanas; si las vas a pintar igual (marcos, aberturas de madera), no las descuentes.</p>'),
         ("Litros", f'<p {FORMULA}>litros = superficie × manos / rendimiento</p><p>El rendimiento depende del producto y de la superficie: una pared nueva sin sellador absorbe más. Revisá siempre la etiqueta de la lata.</p>'),
         ("Latas", "<p>Se sugiere la combinación de latas de 4, 10 y 20 litros que cubre la cantidad con el menor sobrante. Conviene comprar un poco más para retoques y mezclar todo del mismo lote.</p>"),
     ]),
     related=[("/calculadoras/hogar-y-construccion/calculadora-de-ceramicos/", "Calculadora de Cerámicos"), ("/calculadoras/matematicas-avanzadas/calculadora-de-areas-y-volumenes/", "Calculadora de Áreas y Volúmenes"),
              ("/calculadoras/finanzas/calculadora-de-porcentajes/", "Calculadora de Porcentajes")],
     guide=("/guias/cuanta-pintura-necesito/", "Cuánta pintura necesito", "Leé la guía completa: cómo medir una habitación, cuántas manos dar y cómo elegir las latas."),
     faqs=[("¿Cuántos litros de pintura necesito para una habitación?", "Una habitación de 4 × 3 m con paredes de 2,6 m y 3,5 m² de aberturas tiene unos 32,9 m² de paredes: con dos manos y 10 m²/L, son 6,6 litros (8,98 si sumás el techo)."),
           ("¿Cuántas manos hay que dar?", "Dos es lo habitual. Si cambiás a un color muy distinto o la pared está sin pintar, puede hacer falta una mano de fijador y una tercera de color."),
           ("¿Qué rendimiento tiene la pintura?", "Los látex rinden entre 8 y 12 m² por litro y por mano; los esmaltes, algo más. Está indicado en la lata."),
           ("¿Hay que descontar puertas y ventanas?", "Sí, si no las vas a pintar. Una puerta de 0,8 × 2 m son 1,6 m²."),
           ("¿Y si pinto el techo?", "Activá la opción: se suma largo × ancho a la superficie.")])

# ============================================================ ladrillos
L = Lib("la")
page("calculadoras/hogar-y-construccion/calculadora-de-ladrillos", L, HOG,
     slug="calculadora-de-ladrillos", name="Calculadora de Ladrillos",
     page_title="Calculadora de Ladrillos: Cuántos Ladrillos Necesito por m² de Pared | Calculadora Científica",
     desc="Calculá cuántos ladrillos necesitás para una pared según su superficie, el tamaño del ladrillo y el espesor de la junta, con el desperdicio. Cantidad por m². Gratis.",
     og_title="Calculadora de Ladrillos",
     og_desc="Cantidad de ladrillos por m² y para tu pared, con junta y desperdicio. Gratis.",
     schema_desc="Calcula la cantidad de ladrillos por metro cuadrado de pared y el total necesario según las medidas del ladrillo, el espesor de la junta y el porcentaje de desperdicio.",
     intro="Elegí el ladrillo, indicá la superficie de la pared (o sus medidas) y el espesor de la junta: obtenés cuántos ladrillos entran por m² y cuántos tenés que comprar.",
     form_html=L.form([
         L.sel("mode", "La pared se define por…", [("area", "Superficie en m²"), ("medidas", "Largo y alto")]),
         L.num("area", "Superficie de la pared (m²)", "Ej: 25", when="mode=area"),
         L.num("wlen", "Largo de la pared (m)", "Ej: 6", when="mode=medidas"),
         L.num("wheight", "Alto de la pared (m)", "Ej: 2,6", when="mode=medidas"),
         L.num("openings", "Aberturas a descontar (m²) — opcional", "Ej: 3", opt=True, rule="nonneg", when="mode=medidas"),
         L.sel("brick", "Ladrillo (cara colocada: largo × alto en cm)", [("33x18", "Hueco 33 × 18 (de 8, 12 o 18)"), ("25x12", "Hueco 25 × 12"), ("25x5.5", "Común macizo 25 × 5,5 (en soga)"), ("24x11.5", "Cerámico portante 24 × 11,5"), ("40x20", "Bloque de hormigón 40 × 20")]),
         L.num("joint", "Espesor de la junta (cm)", "1,5", opt=True, default=1.5, rule="nonneg", value="1,5"),
         L.num("waste", "Desperdicio (%)", "5", opt=True, default=5, rule="nonneg", value="5"),
     ], chips=[("Pared de 25 m² con hueco 33 × 18", "mode=area;area=25;brick=33x18;joint=1,5;waste=5"), ("Pared de 6 × 2,6 m con ladrillo común", "mode=medidas;wlen=6;wheight=2,6;openings=3;brick=25x5.5;joint=1,5;waste=5")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Ladrillos por m²", f'<p {FORMULA}>unidades por m² = 10.000 / ((largo + junta) × (alto + junta))</p><p>Con medidas en centímetros. Cada ladrillo "ocupa" su cara más la mitad de la junta de cada lado.</p>'),
         ("Cara colocada", "<p>El largo y el alto que se usan son los de la cara que queda a la vista según cómo se coloque: un ladrillo macizo de 25 × 12 × 5,5 cm en soga muestra 25 × 5,5; en tizón, 12 × 5,5. Elegí la opción que corresponda a tu pared.</p>"),
         ("Desperdicio", "<p>Un 5 % cubre roturas y cortes; subí a 8–10 % si hay muchas aberturas o recortes. No incluye el mortero de asiento, que depende del espesor de la pared y de la mezcla.</p>"),
     ]),
     related=[("/calculadoras/hogar-y-construccion/calculadora-de-hormigon/", "Calculadora de Hormigón"), ("/calculadoras/hogar-y-construccion/calculadora-de-ceramicos/", "Calculadora de Cerámicos"),
              ("/calculadoras/matematicas-avanzadas/calculadora-de-areas-y-volumenes/", "Calculadora de Áreas y Volúmenes")],
     guide=("/guias/cuantos-ladrillos-necesito-por-m2/", "Cuántos ladrillos necesito por m²", "Leé la guía completa: la fórmula, ejemplos con los ladrillos más usados y cuánto desperdicio prever."),
     faqs=[("¿Cuántos ladrillos entran en un m² de pared?", "Depende del ladrillo: un hueco de 33 × 18 cm con junta de 1,5 cm son unos 15 por m²; un macizo en soga de 25 × 5,5 cm, unos 53."),
           ("¿Cómo calculo cuántos ladrillos necesito?", "Multiplicá la superficie de la pared (descontando aberturas) por los ladrillos por m² y sumá un 5 % de desperdicio."),
           ("¿Influye el espesor de la junta?", "Sí: una junta de 2 cm en vez de 1 cm reduce la cantidad por m². Por eso se pide el espesor."),
           ("¿Incluye el mortero?", "No, solo cuenta ladrillos. El mortero depende del espesor del muro y de la mezcla."),
           ("¿Sirve para bloques de hormigón?", "Sí: elegí la opción de bloque 40 × 20 o cargá las medidas del tuyo en cm.")])

# ============================================================ hormigón
L = Lib("hm")
page("calculadoras/hogar-y-construccion/calculadora-de-hormigon", L, HOG,
     slug="calculadora-de-hormigon", name="Calculadora de Hormigón",
     page_title="Calculadora de Hormigón: Volumen, Cemento, Arena y Piedra | Calculadora Científica",
     desc="Calculá el volumen de hormigón de una losa, platea o columnas y los materiales aproximados: bolsas de cemento, arena, piedra y agua según la resistencia. Gratis.",
     og_title="Calculadora de Hormigón",
     og_desc="Volumen de hormigón y materiales para losas y columnas. Gratis.",
     schema_desc="Calcula el volumen de hormigón de una losa, platea o conjunto de columnas y estima los materiales (cemento, arena, piedra y agua) según la resistencia elegida, con porcentaje de desperdicio.",
     intro="Elegí si es una losa/platea o columnas, cargá las medidas y la resistencia: te doy el volumen de hormigón y los materiales aproximados, con las bolsas de cemento de 50 kg.",
     form_html=L.form([
         L.sel("shape", "Elemento", [("losa", "Losa o platea"), ("columna", "Columnas (sección rectangular)")]),
         L.num("length", "Largo (m)", "Ej: 5", when="shape=losa"),
         L.num("width", "Ancho (m)", "Ej: 4", when="shape=losa"),
         L.num("thickness", "Espesor (cm)", "Ej: 12", when="shape=losa"),
         L.num("sa", "Lado A de la sección (cm)", "Ej: 25", when="shape=columna"),
         L.num("sb", "Lado B de la sección (cm)", "Ej: 25", when="shape=columna"),
         L.num("height", "Altura (m)", "Ej: 3", when="shape=columna"),
         L.num("qty", "Cantidad de columnas", "Ej: 4", rule="int", when="shape=columna"),
         L.sel("grade", "Resistencia del hormigón", [("H13", "H-13 (13 MPa)"), ("H17", "H-17 (17 MPa)"), ("H21", "H-21 (21 MPa)")], value="H17"),
         L.num("waste", "Desperdicio (%)", "5", opt=True, default=5, rule="nonneg", value="5"),
     ], chips=[("Losa de 5 × 4 m con 12 cm", "shape=losa;length=5;width=4;thickness=12;grade=H17;waste=5"), ("4 columnas de 25 × 25 cm y 3 m", "shape=columna;sa=25;sb=25;height=3;qty=4;grade=H21;waste=5")],
         note="Cantidades orientativas. La resistencia, el armado y la dosificación de una obra los define un profesional (ingeniero o arquitecto)."),
     result_html=L.panel(),
     help_html=help_blocks([
         ("Volumen", f'<p {FORMULA}>losa: V = largo × ancho × espesor &nbsp;·&nbsp; columnas: V = lado A × lado B × altura × cantidad</p><p>Medidas en metros (los centímetros se dividen por 100). Se suma un porcentaje de desperdicio por derrames y desniveles.</p>'),
         ("Materiales por m³", "<p>Para un hormigón elaborado en obra se usan, aproximadamente, entre 280 y 380 kg de cemento, 0,5 a 0,55 m³ de arena, 0,8 m³ de piedra partida y unos 185 litros de agua por m³. Cuanto mayor la resistencia, más cemento.</p>"),
         ("Hormigón elaborado", "<p>Para volúmenes grandes (más de 2 a 3 m³) conviene pedir hormigón elaborado a una planta: se pide por m³ completos y con la resistencia que indica el proyecto.</p>"),
     ]),
     related=[("/calculadoras/hogar-y-construccion/calculadora-de-ladrillos/", "Calculadora de Ladrillos"), ("/calculadoras/matematicas-avanzadas/calculadora-de-areas-y-volumenes/", "Calculadora de Áreas y Volúmenes"),
              ("/calculadoras/ingenieria/conversor-de-unidades/", "Conversor de Unidades Técnicas")],
     guide=("/guias/como-calcular-el-hormigon-de-una-losa/", "Cómo calcular el hormigón de una losa", "Leé la guía completa: el volumen, la dosificación aproximada y cuándo conviene pedir hormigón elaborado."),
     faqs=[("¿Cuántos m³ de hormigón lleva una losa?", "Largo × ancho × espesor. Una losa de 5 × 4 m con 12 cm de espesor lleva 5 × 4 × 0,12 = 2,4 m³ (más desperdicio)."),
           ("¿Cuánto cemento lleva un m³ de hormigón?", "Entre 280 y 380 kg según la resistencia: unas 6 a 8 bolsas de 50 kg."),
           ("¿Qué significa H-17?", "Es la clase de resistencia: el hormigón soporta una compresión característica de 17 MPa a los 28 días. H-21 es más resistente que H-17."),
           ("¿Conviene hacerlo en obra o pedirlo elaborado?", "Para más de 2 o 3 m³ suele convenir el elaborado: tiene calidad uniforme y ahorra mano de obra."),
           ("¿La calculadora reemplaza un cálculo estructural?", "No: da cantidades aproximadas de materiales. El diseño, el armado y la resistencia los define un profesional.")])

# ============================================================ consumo eléctrico
L = Lib("co")
page("calculadoras/hogar-y-construccion/calculadora-de-consumo-electrico", L, HOG,
     slug="calculadora-de-consumo-electrico", name="Calculadora de Consumo Eléctrico",
     page_title="Calculadora de Consumo Eléctrico: kWh y Costo de un Artefacto | Calculadora Científica",
     desc="Calculá cuántos kWh consume un artefacto y cuánto te cuesta por día, mes y año según su potencia, las horas de uso y el precio del kWh. Gratis y sin registro.",
     og_title="Calculadora de Consumo Eléctrico",
     og_desc="kWh y costo mensual de cualquier artefacto. Gratis.",
     schema_desc="Calcula el consumo en kWh y el costo diario, mensual y anual de un artefacto eléctrico a partir de su potencia en watts, las horas de uso por día, los días de uso y el precio del kWh.",
     intro="Ingresá la potencia del artefacto (en watts, figura en su etiqueta), las horas de uso y el precio del kWh de tu factura: obtenés el consumo y el costo por día, mes y año.",
     form_html=L.form([
         L.num("watts", "Potencia (W)", "Ej: 1500", hint="En la etiqueta: un aire acondicionado 3000 frigorías ≈ 1100–1300 W; una heladera ≈ 100–200 W; una lámpara LED ≈ 9 W."),
         L.num("qty", "Cantidad de artefactos iguales", "1", opt=True, default=1, rule="int", value="1"),
         L.num("hours", "Horas de uso por día", "Ej: 8"),
         L.num("days", "Días de uso al mes", "30", value="30"),
         L.num("price", "Precio del kWh ($)", "Ej: 120", hint="Lo encontrás en tu factura: sumá el cargo variable por kWh y los impuestos si querés el costo total."),
     ], chips=[("Aire acondicionado 8 h al día", "watts=1200;qty=1;hours=8;days=30;price=120"), ("4 lámparas LED de 9 W, 5 h", "watts=9;qty=4;hours=5;days=30;price=120")]),
     result_html=L.panel(),
     help_html=help_blocks([
         ("La fórmula", f'<p {FORMULA}>kWh = potencia (W) × horas / 1000 &nbsp;·&nbsp; costo = kWh × precio del kWh</p><p>Un artefacto de 1000 W encendido durante una hora consume 1 kWh.</p>'),
         ("Consumo real", "<p>La potencia de la etiqueta es la máxima: heladeras y aires inverter no trabajan siempre a pleno, por lo que el consumo real suele ser menor. Para un cálculo más fino usá las horas equivalentes de funcionamiento.</p>"),
         ("Precio del kWh", "<p>Depende de tu distribuidora, de la categoría de usuario y de los subsidios. El costo total de tu factura incluye cargos fijos e impuestos, así que el resultado es una estimación del consumo variable.</p>"),
     ]),
     related=[("/calculadoras/fisica/ley-de-ohm/", "Ley de Ohm"), ("/calculadoras/fisica/energia-cinetica-y-potencial/", "Energía Cinética y Potencial"),
              ("/calculadoras/ingenieria/resistencias-serie-paralelo/", "Resistencias en Serie y Paralelo")],
     guide=("/guias/como-calcular-el-consumo-electrico/", "Cómo calcular el consumo eléctrico de un artefacto", "Leé la guía completa: de watts a kWh, cuánto cuesta cada artefacto y cómo bajar tu factura."),
     faqs=[("¿Cómo se calcula el consumo en kWh?", "Multiplicando la potencia en watts por las horas de uso y dividiendo por 1000. Un aire de 1200 W durante 8 horas consume 9,6 kWh."),
           ("¿Cuánto cuesta usar un artefacto?", "Multiplicando los kWh por el precio del kWh. Con 9,6 kWh y $120 el kWh: $1.152 por día."),
           ("¿Dónde veo la potencia de un artefacto?", "En la etiqueta o el manual, en watts (W). Si figura en amperes y volts, multiplicalos: W = A × V."),
           ("¿Por qué el consumo real puede ser menor?", "Porque motores y compresores se apagan y prenden según la necesidad: la potencia de la etiqueta es el máximo."),
           ("¿Cómo bajo el consumo?", "Elegí artefactos eficientes (clase A), usá lámparas LED, apagá el stand-by y ajustá los termostatos del aire y la heladera.")])
