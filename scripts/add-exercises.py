"""
add-exercises.py — Agrega una sección "Ejercicios para practicar" (3 ejercicios con solución desplegable)
a 16 guías de uso frecuente. Idempotente: reemplaza el bloque entre los marcadores CC-EXERCISES.
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
