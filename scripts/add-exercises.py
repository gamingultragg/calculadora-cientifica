"""
add-exercises.py — Agrega una sección "Ejercicios para practicar" (3 ejercicios con solución desplegable)
a 40 guías (las 16 de uso frecuente y las de los lotes 10, 11 y 12). Idempotente: reemplaza el bloque entre los marcadores CC-EXERCISES.
Las respuestas numéricas se verificaron con cálculos independientes antes de cargarlas acá.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MUTED = "text-[var(--color-text-muted)]"
LINK = "text-[var(--color-primary-link)]"

EX = {
    "como-calcular-molaridad": [
        ("Se disuelven 0,5 mol de soluto en 2 litros de solución. ¿Cuál es la molaridad?", "M = n / V = 0,5 mol / 2 L = <strong>0,25 mol/L</strong>."),
        ("Se disuelven 20 g de NaOH (40 g/mol) hasta completar 500 mL de solución. ¿Cuál es la molaridad?", "n = 20 / 40 = 0,5 mol. V = 0,5 L. M = 0,5 / 0,5 = <strong>1 mol/L</strong>."),
        ("¿Cuántos gramos de NaCl (58,44 g/mol) hay en 250 mL de una solución 0,2 M?", "n = M × V = 0,2 × 0,25 = 0,05 mol. Masa = 0,05 × 58,44 = <strong>2,92 g</strong>."),
    ],
    "como-calcular-porcentajes": [
        ("¿Cuánto es el 15 % de 8.400?", "8.400 × 15 / 100 = <strong>1.260</strong>."),
        ("Un producto de $12.000 pasa a costar $13.800. ¿De qué porcentaje fue el aumento?", "Aumento = 1.800. 1.800 / 12.000 = <strong>15 %</strong>."),
        ("Después de un descuento del 20 %, un producto cuesta $9.600. ¿Cuál era su precio original?", "El precio final es el 80 % del original: 9.600 / 0,80 = <strong>$12.000</strong>."),
    ],
    "como-calcular-cuota-de-prestamo": [
        ("Un préstamo de $500.000 se paga en 3 cuotas mensuales con una tasa del 2 % mensual (sistema francés). ¿De cuánto es la cuota?", "Cuota = P·i / (1 − (1 + i)<sup>−n</sup>) = 500.000 × 0,02 / (1 − 1,02<sup>−3</sup>) = 10.000 / 0,057678 = <strong>$173.377</strong>."),
        ("En el ejercicio anterior, ¿cuánto se paga en total y cuánto es de interés?", "Total = 173.377 × 3 = $520.132. Interés = 520.132 − 500.000 = <strong>$20.132</strong>."),
        ("¿Cuánto del primer pago es interés?", "Interés del primer mes = saldo × tasa = 500.000 × 0,02 = <strong>$10.000</strong>; el resto de la cuota (163.377) amortiza capital."),
    ],
    "como-calcular-mcd-y-mcm": [
        ("Calculá el MCD de 84 y 126.", "84 = 2² × 3 × 7 y 126 = 2 × 3² × 7. Factores comunes con el menor exponente: 2 × 3 × 7 = <strong>42</strong>."),
        ("Calculá el MCM de 12 y 15.", "12 = 2² × 3 y 15 = 3 × 5. Todos los factores con el mayor exponente: 2² × 3 × 5 = <strong>60</strong>."),
        ("Simplificá la fracción 84/126.", "Se divide por el MCD (42): 84/126 = <strong>2/3</strong>."),
    ],
    "regla-de-tres-simple-y-compuesta": [
        ("5 kg de un producto cuestan $7.500. ¿Cuánto cuestan 8 kg?", "Es directa: x = 7.500 × 8 / 5 = <strong>$12.000</strong>."),
        ("6 obreros terminan una obra en 10 días. ¿Cuántos días tardarían 4 obreros?", "Es inversa (menos obreros, más días): x = 6 × 10 / 4 = <strong>15 días</strong>."),
        ("3 máquinas producen 120 piezas en 4 horas. ¿Cuántas piezas producen 5 máquinas en 6 horas?", "Compuesta (ambas directas): 120 × (5/3) × (6/4) = <strong>300 piezas</strong>."),
    ],
    "como-resolver-ecuaciones-de-segundo-grado": [
        ("Resolvé x² − 5x + 6 = 0.", "Δ = 25 − 24 = 1. x = (5 ± 1) / 2 → <strong>x = 3 y x = 2</strong>."),
        ("Resolvé 2x² − 8 = 0.", "2x² = 8 → x² = 4 → <strong>x = 2 y x = −2</strong>."),
        ("¿Qué raíces tiene x² + 2x + 5 = 0?", "Δ = 4 − 20 = −16 &lt; 0: no tiene raíces reales. Las raíces complejas son <strong>x = −1 ± 2i</strong>."),
    ],
    "como-calcular-ph-y-poh": [
        ("Una solución tiene [H⁺] = 1 × 10⁻³ mol/L. ¿Cuál es su pH?", "pH = −log(10⁻³) = <strong>3</strong> (ácida)."),
        ("Una solución tiene pH 9. ¿Cuál es su [H⁺] y su pOH (a 25 °C)?", "[H⁺] = 10⁻⁹ mol/L. pOH = 14 − 9 = <strong>5</strong> (básica)."),
        ("Si el pOH es 2, ¿cuál es el pH?", "pH = 14 − 2 = <strong>12</strong> (muy básica)."),
    ],
    "como-calcular-desviacion-estandar": [
        ("Calculá la desviación estándar poblacional de 2, 4, 4, 4, 5, 5, 7, 9.", "Media = 5. Suma de cuadrados de las desviaciones = 32. σ = √(32/8) = <strong>2</strong>."),
        ("Calculá la desviación estándar muestral de los mismos datos.", "s = √(32/7) = <strong>2,14</strong> (se divide por n − 1)."),
        ("¿Cuál es la desviación estándar de 10, 10, 10, 10?", "Todos los datos son iguales a la media: no hay dispersión, <strong>σ = 0</strong>."),
    ],
    "como-calcular-iva": [
        ("Un producto cuesta $10.000 sin IVA. ¿Cuánto cuesta con IVA del 21 %?", "10.000 × 1,21 = <strong>$12.100</strong> (IVA de $2.100)."),
        ("Un total con IVA del 21 % es de $24.200. ¿Cuál es el neto y el IVA?", "Neto = 24.200 / 1,21 = <strong>$20.000</strong>. IVA = 24.200 − 20.000 = <strong>$4.200</strong>."),
        ("¿Cuánto es el IVA del 10,5 % sobre un neto de $8.000?", "8.000 × 0,105 = <strong>$840</strong>."),
    ],
    "como-operar-con-fracciones": [
        ("Calculá 2/3 + 3/4.", "MCM(3, 4) = 12: 8/12 + 9/12 = <strong>17/12</strong> (= 1 5/12)."),
        ("Calculá 5/6 − 1/4.", "MCM(6, 4) = 12: 10/12 − 3/12 = <strong>7/12</strong>."),
        ("Calculá 3/5 ÷ 9/10.", "3/5 × 10/9 = 30/45 = <strong>2/3</strong>."),
    ],
    "teorema-de-pitagoras-explicado": [
        ("Los catetos de un triángulo rectángulo miden 6 y 8. ¿Cuánto mide la hipotenusa?", "c = √(36 + 64) = √100 = <strong>10</strong>."),
        ("La hipotenusa mide 17 y un cateto 8. ¿Cuánto mide el otro cateto?", "a = √(289 − 64) = √225 = <strong>15</strong>."),
        ("Una escalera de 5 m se apoya en una pared con el pie a 3 m de la base. ¿A qué altura llega?", "h = √(25 − 9) = √16 = <strong>4 m</strong>."),
    ],
    "como-calcular-moles": [
        ("¿Cuántos moles son 36 g de agua (18 g/mol)?", "n = 36 / 18 = <strong>2 mol</strong>."),
        ("¿Cuántos gramos son 0,25 mol de NaCl (58,44 g/mol)?", "m = 0,25 × 58,44 = <strong>14,61 g</strong>."),
        ("¿Cuántos moles hay en 11,2 L de un gas a 0 °C y 1 atm?", "n = 11,2 / 22,414 = <strong>0,5 mol</strong>."),
    ],
    "interes-simple-vs-compuesto": [
        ("Calculá el interés simple de $100.000 al 24 % anual durante 6 meses.", "I = 100.000 × 0,24 × 0,5 = <strong>$12.000</strong>."),
        ("Calculá el monto de $100.000 al 10 % anual compuesto durante 2 años.", "M = 100.000 × 1,10² = <strong>$121.000</strong> (el interés simple daría $120.000)."),
        ("¿Cuánto es el monto de $50.000 al 3 % mensual de interés simple durante 4 meses?", "I = 50.000 × 0,03 × 4 = $6.000. Monto = <strong>$56.000</strong>."),
    ],
    "formulas-de-mru-y-mrua": [
        ("Un auto va a 72 km/h constantes durante 30 s. ¿Qué distancia recorre?", "72 km/h = 20 m/s. d = 20 × 30 = <strong>600 m</strong>."),
        ("Un cuerpo parte del reposo con a = 2 m/s². ¿Qué velocidad y qué distancia alcanza a los 5 s?", "v = a·t = <strong>10 m/s</strong>. d = ½·a·t² = ½ × 2 × 25 = <strong>25 m</strong>."),
        ("Un auto frena de 20 m/s hasta detenerse con a = −4 m/s². ¿En cuánto tiempo y distancia se detiene?", "t = 20 / 4 = <strong>5 s</strong>. d = v₀² / (2·|a|) = 400 / 8 = <strong>50 m</strong>."),
    ],
    "ley-de-ohm-explicada": [
        ("Una resistencia de 4 Ω está conectada a 12 V. ¿Qué corriente circula?", "I = V / R = 12 / 4 = <strong>3 A</strong>."),
        ("Por una resistencia de 100 Ω circulan 0,5 A. ¿Qué tensión hay en sus extremos?", "V = I·R = 0,5 × 100 = <strong>50 V</strong>."),
        ("Un artefacto conectado a 220 V consume 2 A. ¿Qué potencia tiene?", "P = V·I = 220 × 2 = <strong>440 W</strong>."),
    ],
    "como-calcular-promedio-de-notas": [
        ("Calculá el promedio simple de 6, 8 y 10.", "(6 + 8 + 10) / 3 = <strong>8</strong>."),
        ("Calculá el promedio ponderado de un 6 (peso 30 %) y un 9 (peso 70 %).", "6 × 0,30 + 9 × 0,70 = 1,8 + 6,3 = <strong>8,1</strong>."),
        ("Tenés un 6 que vale el 60 % de la nota. ¿Qué nota necesitás en el final (40 %) para promediar 7?", "0,6 × 6 + 0,4 × x = 7 → x = (7 − 3,6) / 0,4 = <strong>8,5</strong>."),
    ],
    # ---- guías de los lotes 10 y 11 (respuestas verificadas con cálculos independientes) ----
    "como-calcular-la-pendiente-y-la-distancia-entre-dos-puntos": [
        ("Calculá la pendiente de la recta que pasa por (2; 3) y (6; 11).", "m = (11 − 3) / (6 − 2) = 8 / 4 = <strong>2</strong>."),
        ("Hallá la ecuación de la recta que pasa por (1; 5) y (4; −1).", "m = (−1 − 5) / (4 − 1) = −2. b = 5 − (−2)·1 = 7. La recta es <strong>y = −2x + 7</strong>."),
        ("Calculá la distancia y el punto medio entre (−1; 2) y (5; 10).", "Δx = 6 y Δy = 8: d = √(36 + 64) = <strong>10</strong>. Punto medio = ((−1 + 5)/2 ; (2 + 10)/2) = <strong>(2; 6)</strong>."),
    ],
    "logaritmos-que-son-y-como-calcularlos": [
        ("Calculá log₂(64).", "2⁶ = 64, entonces log₂(64) = <strong>6</strong>."),
        ("Resolvé 3ˣ = 50.", "x = ln(50) / ln(3) = 3,912 / 1,099 ≈ <strong>3,56</strong>."),
        ("Calculá log(25) + log(4) sin calculadora.", "log(25) + log(4) = log(25 · 4) = log(100) = <strong>2</strong>."),
    ],
    "como-calcular-la-densidad": [
        ("Un cubo de 5 cm de lado tiene una masa de 337,5 g. ¿Cuál es su densidad?", "V = 5³ = 125 cm³. ρ = 337,5 / 125 = <strong>2,7 g/cm³</strong> (es aluminio)."),
        ("¿Cuántos kilogramos pesa el contenido de un tanque de 200 L de nafta (0,74 g/cm³)?", "200 L = 200.000 cm³. m = 0,74 × 200.000 = 148.000 g = <strong>148 kg</strong>."),
        ("Una corona de 650 g desplaza 40 mL de agua al sumergirla. ¿Puede ser de oro puro (19,32 g/cm³)?", "ρ = 650 / 40 = 16,25 g/cm³. Es menor que la del oro: <strong>no es oro puro</strong>."),
    ],
    "calor-especifico-y-calorimetria": [
        ("¿Cuánto calor hace falta para calentar 250 g de agua de 15 °C a 65 °C?", "Q = 250 × 4,186 × 50 = <strong>52.325 J</strong> (unos 52,3 kJ)."),
        ("500 g de aluminio (c = 0,897 J/g·°C) absorben 22.425 J. ¿Cuánto sube su temperatura?", "ΔT = Q / (m·c) = 22.425 / (500 × 0,897) = <strong>50 °C</strong>."),
        ("Se mezclan 300 g de agua a 80 °C con 300 g de agua a 20 °C. ¿Cuál es la temperatura final?", "Es la misma sustancia y la misma masa: la temperatura final es el promedio, (80 + 20) / 2 = <strong>50 °C</strong>."),
    ],
    "movimiento-circular-uniforme-explicado": [
        ("Una rueda de 0,4 m de radio da 3 vueltas por segundo. ¿Cuánto valen ω y v?", "ω = 2π · 3 = <strong>18,85 rad/s</strong>. v = ω · r = 18,85 × 0,4 = <strong>7,54 m/s</strong>."),
        ("Un disco gira a 45 rpm. ¿Cuál es su frecuencia y su período?", "f = 45 / 60 = <strong>0,75 Hz</strong>. T = 1 / 0,75 = <strong>1,33 s</strong>."),
        ("Una piedra gira en una honda de 1,5 m a 12 m/s. ¿Cuál es su aceleración centrípeta?", "a = v² / r = 144 / 1,5 = <strong>96 m/s²</strong>."),
    ],
    "leyes-de-boyle-charles-y-gay-lussac": [
        ("6 L de gas a 2 atm se expanden hasta 9 L sin cambiar la temperatura. ¿Cuál es la presión final?", "Boyle: P₂ = P₁·V₁ / V₂ = 2 × 6 / 9 = <strong>1,33 atm</strong>."),
        ("3 L de gas a 300 K se calientan a 450 K a presión constante. ¿Qué volumen ocupan?", "Charles: V₂ = V₁·T₂ / T₁ = 3 × 450 / 300 = <strong>4,5 L</strong>."),
        ("Una lata rígida con gas a 1,5 atm y 27 °C se calienta a 127 °C. ¿Cuál es la presión final?", "Gay-Lussac con kelvin: P₂ = 1,5 × 400,15 / 300,15 ≈ <strong>2,0 atm</strong>."),
    ],
    "como-calcular-ppm-y-porcentaje-de-concentracion": [
        ("Se disuelven 40 mg de un soluto en 8 L de agua. ¿Cuántas ppm hay?", "40 mg / 8 L = <strong>5 ppm</strong>."),
        ("Pasá 250 ppm a g/L y a porcentaje m/v.", "250 ppm = 250 mg/L = <strong>0,25 g/L</strong>. En porcentaje: 250 / 10.000 = <strong>0,025 %</strong>."),
        ("¿Cuántos gramos de soluto hacen falta para tener 15 ppm en 200 L?", "15 × 200 = 3.000 mg = <strong>3 g</strong>."),
    ],
    "como-calcular-el-consumo-de-combustible-de-un-auto": [
        ("Un auto recorre 520 km y carga 41,6 L. ¿Cuál es su rendimiento y su consumo?", "520 / 41,6 = <strong>12,5 km/L</strong>. Consumo = 100 / 12,5 = <strong>8 L cada 100 km</strong>."),
        ("¿Cuánto cuesta un viaje de 640 km con un consumo de 7,5 L/100 km y nafta a $1.600 el litro?", "Litros = 640 × 7,5 / 100 = 48 L. Costo = 48 × 1.600 = <strong>$76.800</strong>."),
        ("¿Cuántos kilómetros se recorren con un tanque de 45 L a 6 L/100 km?", "45 / 6 × 100 = <strong>750 km</strong>."),
    ],
    "notacion-cientifica-que-es-y-como-usarla": [
        ("Escribí 45.600.000 en notación científica.", "Se corre la coma 7 lugares hacia la izquierda: <strong>4,56 × 10⁷</strong>."),
        ("Calculá (2,5 × 10⁻³) · (4 × 10⁵).", "Mantisas: 2,5 · 4 = 10. Exponentes: −3 + 5 = 2. Da 10 × 10² = <strong>1 × 10³</strong>."),
        ("Calculá (6 × 10⁷) / (3 × 10⁴).", "6 / 3 = 2 y 7 − 4 = 3: <strong>2 × 10³</strong>."),
    ],
    "potencias-y-raices-propiedades-y-ejemplos": [
        ("Simplificá √98.", "98 = 2 · 7²: √98 = 7·√2 ≈ <strong>9,90</strong>."),
        ("Calculá 27^(2/3).", "27^(2/3) = (∛27)² = 3² = <strong>9</strong>."),
        ("Calculá (2⁵ · 2⁻²) / 2².", "Se suman y restan los exponentes: 5 + (−2) − 2 = 1, entonces el resultado es 2¹ = <strong>2</strong>."),
    ],
    "como-calcular-probabilidades": [
        ("Una bolsa tiene 3 bolitas rojas y 7 azules. ¿Qué probabilidad hay de sacar una roja?", "3 / 10 = <strong>30 %</strong>."),
        ("¿Qué probabilidad hay de sacar cara dos veces seguidas con una moneda y después un 6 con un dado?", "0,5 · 0,5 · 1/6 = 1/24 ≈ <strong>4,17 %</strong>."),
        ("¿Qué probabilidad hay de sacar al menos un 6 en 3 tiros de un dado?", "1 − (5/6)³ = 1 − 0,5787 = <strong>0,4213 (42,13 %)</strong>."),
    ],
    "periodo-del-pendulo-simple": [
        ("¿Cuál es el período de un péndulo de 0,5 m en la Tierra?", "T = 2π·√(0,5 / 9,81) ≈ <strong>1,42 s</strong>."),
        ("¿Qué longitud debe tener un péndulo para oscilar con un período de 1 s?", "L = g·T² / (4π²) = 9,81 / 39,48 ≈ <strong>0,25 m</strong> (25 cm)."),
        ("Un péndulo de 0,80 m tiene un período de 1,8 s. ¿Cuánto vale g en ese lugar?", "g = 4π²·L / T² = 39,48 × 0,8 / 3,24 ≈ <strong>9,75 m/s²</strong>."),
    ],
    "ley-de-coulomb-explicada": [
        ("Dos cargas de 4 µC y 5 µC están a 30 cm. ¿Con qué fuerza se repelen?", "F = 8,99 × 10⁹ · 4 × 10⁻⁶ · 5 × 10⁻⁶ / 0,3² ≈ <strong>2,0 N</strong>."),
        ("Si en el ejercicio anterior se duplica la distancia, ¿cuánto vale la fuerza?", "Se reduce a la cuarta parte: 2,0 / 4 ≈ <strong>0,5 N</strong>."),
        ("Dos cargas iguales se repelen con 0,9 N a 10 cm de distancia. ¿Cuánto vale cada una?", "q = r·√(F / k) = 0,1 · √(0,9 / 8,99 × 10⁹) ≈ 1 × 10⁻⁶ C = <strong>1 µC</strong>."),
    ],
    "presion-y-presion-hidrostatica": [
        ("Una persona de 60 kg se apoya en los dos pies, que suman 200 cm². ¿Qué presión ejerce sobre el piso?", "Peso = 60 × 9,81 = 588,6 N. A = 0,02 m². P = 588,6 / 0,02 = <strong>29.430 Pa</strong> (unos 29,4 kPa)."),
        ("¿Cuál es la presión manométrica a 5 m de profundidad en agua dulce?", "P = 1.000 × 9,81 × 5 = <strong>49.050 Pa</strong>."),
        ("¿A qué profundidad del agua la presión absoluta llega a 3 atm?", "La manométrica tiene que ser 2 atm = 202.650 Pa. h = 202.650 / (1.000 × 9,81) ≈ <strong>20,7 m</strong>."),
    ],
    "como-calcular-una-escalera": [
        ("¿Cuántos escalones, qué contrahuella y qué huella necesita una escalera para salvar 2,55 m?", "n = 255 / 17,5 = 14,6 ≈ 15. Contrahuella = 255 / 15 = <strong>17 cm</strong>. Huella = 63 − 2 · 17 = <strong>29 cm</strong>."),
        ("Con una contrahuella de 16 cm, ¿qué huella da la fórmula de Blondel?", "h = 63 − 2 · 16 = <strong>31 cm</strong>."),
        ("¿Cuánto ocupa en horizontal una escalera de 12 escalones con huella de 28 cm?", "Hay 11 huellas: 11 × 28 = 308 cm = <strong>3,08 m</strong>."),
    ],
    "como-calcular-cuanto-ahorrar-para-una-meta": [
        ("¿Cuánto hay que ahorrar por mes para juntar $900.000 en 18 meses, sin interés?", "900.000 / 18 = <strong>$50.000 por mes</strong>."),
        ("Ya tenés $150.000 y querés llegar a $750.000 aportando $40.000 por mes, sin interés. ¿En cuántos meses lo lográs?", "(750.000 − 150.000) / 40.000 = <strong>15 meses</strong>."),
        ("¿Cuánto hay que ahorrar por mes para juntar $600.000 en 24 meses con una TNA del 30 %?", "i = 0,30 / 12 = 0,025. A = 600.000 · 0,025 / (1,025²⁴ − 1) ≈ <strong>$18.548 por mes</strong> (contra $25.000 sin interés)."),
    ],
    # ---- guías del lote 12 (respuestas verificadas con cálculos independientes) ----
    "como-calcular-el-peso-ideal": [
        ("¿Cuál es el rango de peso saludable para una persona de 1,80 m?", "Altura² = 3,24. Mínimo: 18,5 × 3,24 ≈ 59,9 kg. Máximo: 24,9 × 3,24 ≈ 80,7 kg. Rango: <strong>de 59,9 a 80,7 kg</strong>."),
        ("Calculá el peso ideal de Devine para una mujer de 160 cm.", "160 / 2,54 = 63,0 pulgadas: 3,0 sobre las 60. 45,5 + 2,3 × 3,0 ≈ <strong>52,4 kg</strong>."),
        ("Calculá el peso ideal de Robinson para un hombre de 170 cm.", "170 / 2,54 = 66,9 pulgadas: 6,9 sobre las 60. 52 + 1,9 × 6,9 ≈ <strong>65,2 kg</strong>."),
    ],
    "como-calcular-la-fecha-probable-de-parto": [
        ("Con una FUM del 1 de abril de 2026 y un ciclo de 28 días, ¿cuál es la fecha probable de parto?", "1 de abril + 280 días = <strong>6 de enero de 2027</strong>."),
        ("Con la misma FUM pero un ciclo de 30 días, ¿cuál es la fecha probable?", "Se suman 30 − 28 = 2 días: <strong>8 de enero de 2027</strong>."),
        ("Con esa FUM (1 de abril), ¿cuántas semanas de embarazo hay al 10 de junio de 2026?", "Pasaron 70 días: 70 ÷ 7 = <strong>10 semanas y 0 días</strong> (primer trimestre)."),
    ],
    "ley-de-gravitacion-universal-explicada": [
        ("¿Con qué fuerza se atraen dos personas de 70 kg separadas 1 m?", "F = 6,6743 × 10⁻¹¹ · 70 · 70 / 1² ≈ <strong>3,3 × 10⁻⁷ N</strong>: una fuerza imperceptible."),
        ("¿Cuánto vale la gravedad en Júpiter (M = 1,898 × 10²⁷ kg, r = 69.911 km)?", "g = G·M / r² = 6,6743 × 10⁻¹¹ · 1,898 × 10²⁷ / (6,9911 × 10⁷)² ≈ <strong>25,9 m/s²</strong> (2,6 veces la terrestre)."),
        ("¿A qué velocidad orbita la Luna, a 3,844 × 10⁸ m de la Tierra?", "v = √(G·M / r) = √(3,986 × 10¹⁴ / 3,844 × 10⁸) ≈ <strong>1.018 m/s</strong>, con un período de unos 27,5 días."),
    ],
    "ley-de-snell-y-refraccion-de-la-luz": [
        ("Un rayo pasa del aire (n = 1) a un vidrio (n = 1,5) con 40° de incidencia. ¿Cuál es el ángulo refractado?", "sen θ₂ = sen 40° / 1,5 = 0,4285 → θ₂ ≈ <strong>25,4°</strong> (se acerca a la normal)."),
        ("¿Cuál es el ángulo crítico entre el aceite (n = 1,47) y el aire?", "θc = arcsen(1 / 1,47) ≈ <strong>42,9°</strong>."),
        ("Una moneda está en el fondo de una pileta a 80 cm de profundidad. ¿A qué profundidad parece estar mirándola desde arriba?", "Profundidad aparente = 80 / 1,333 ≈ <strong>60 cm</strong>."),
    ],
    "media-aritmetica-geometrica-y-armonica": [
        ("Calculá la media geométrica de 4 y 9.", "GM = √(4 · 9) = √36 = <strong>6</strong>."),
        ("Un auto va a 90 km/h y vuelve por el mismo camino a 60 km/h. ¿Cuál es su velocidad media?", "Es la media armónica: 2 / (1/90 + 1/60) = <strong>72 km/h</strong> (no 75)."),
        ("Un capital crece 20 %, 20 % y −10 % en tres años. ¿Cuál es el crecimiento anual promedio?", "GM = (1,2 · 1,2 · 0,9)^(1/3) = 1,296^(1/3) ≈ 1,090: <strong>9,0 % por año</strong>."),
    ],
    "error-absoluto-relativo-y-porcentual": [
        ("Una balanza marca 250 g para una pesa de 245 g. ¿Cuál es el error absoluto, relativo y porcentual?", "E = |250 − 245| = <strong>5 g</strong>. e = 5 / 245 = <strong>0,0204</strong>. Porcentual: <strong>2,04 %</strong>."),
        ("Se mide una mesa de 119,5 cm como 120,0 cm. ¿Cuál es el error porcentual?", "E = 0,5 cm. e = 0,5 / 119,5 = 0,00418 → <strong>0,42 %</strong>."),
        ("Cuatro mediciones de un tiempo dan 2,1 · 2,3 · 2,2 · 2,2 s. ¿Cómo se informa el resultado?", "Promedio = 2,2 s. s = 0,0816 y error estándar = 0,0816 / √4 = 0,0408. Resultado: <strong>2,20 ± 0,04 s</strong>."),
    ],
    "propiedades-coligativas-crioscopia-y-ebulloscopia": [
        ("¿A qué temperatura congela una solución de 180 g de glucosa (180 g/mol) en 1 kg de agua?", "m = 1 mol/kg, i = 1: ΔTf = 1,86 × 1 = 1,86 °C. Congela a <strong>−1,86 °C</strong>."),
        ("¿A qué temperatura hierve una solución de 29,22 g de NaCl (58,44 g/mol, i = 2) en 500 g de agua?", "n = 0,5 mol → m = 0,5 / 0,5 = 1 mol/kg. ΔTb = 2 × 0,512 × 1 = 1,024 °C. Hierve a <strong>101,02 °C</strong>."),
        ("¿Cuánto baja el punto de congelación al disolver 12 g de urea (60 g/mol) en 400 g de agua?", "n = 0,2 mol → m = 0,2 / 0,4 = 0,5 mol/kg. ΔTf = 1,86 × 0,5 = <strong>0,93 °C</strong> (congela a −0,93 °C)."),
    ],
    "como-calcular-la-pendiente-de-una-rampa": [
        ("Una rampa sube 0,6 m en 7,5 m de largo horizontal. ¿Cuál es su pendiente?", "0,6 / 7,5 × 100 = <strong>8 %</strong>."),
        ("¿Qué longitud horizontal necesita una rampa para salvar 1,2 m con una pendiente del 6 %?", "1,2 / 0,06 = <strong>20 m</strong>."),
        ("¿Qué desnivel salva una rampa de 3 m de largo horizontal con una pendiente del 10 %?", "3 × 0,10 = <strong>0,3 m</strong> (30 cm)."),
    ],
}

START, END = "<!-- CC-EXERCISES:START -->", "<!-- CC-EXERCISES:END -->"
FAQ_H2 = '      <h2 class="font-display font-bold text-xl mt-8 mb-2">Preguntas frecuentes</h2>'

for slug, items in EX.items():
    path = ROOT / "guias" / slug / "index.html"
    html = path.read_text(encoding="utf-8")
    lis = "\n".join(
        f"""        <li>
          <p class="{MUTED} leading-relaxed">{q}</p>
          <details class="mt-1">
            <summary class="cursor-pointer text-sm font-semibold {LINK} min-h-[2rem] flex items-center">Ver la solución</summary>
            <p class="{MUTED} leading-relaxed mt-1">{a}</p>
          </details>
        </li>"""
        for q, a in items
    )
    block = f"""      {START}
      <h2 class="font-display font-bold text-xl mt-8 mb-2">Ejercicios para practicar</h2>
      <p class="{MUTED} leading-relaxed">Probá resolverlos vos y después abrí la solución para comparar.</p>
      <ol class="list-decimal list-inside space-y-4 mt-3">
{lis}
      </ol>
      {END}

"""
    if START in html:
        html = re.sub(r"      " + re.escape(START) + r".*?" + re.escape(END) + r"\n\n", lambda m: block, html, flags=re.S)
    else:
        if FAQ_H2 in html:
            html = html.replace(FAQ_H2, block + FAQ_H2, 1)
        else:  # guías sin sección de preguntas: va al final del artículo
            m = re.search(r"^( *)</article>", html, re.M)
            assert m, f"{slug}: no se encontró dónde insertar los ejercicios"
            html = html[: m.start()] + block + html[m.start():]
    path.write_text(html, encoding="utf-8")
    print("ejercicios:", slug)
