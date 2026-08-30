"""
fix-number-parsing.py — Corrige un bug real de parseo numérico presente en
las 17 calculadoras que leen inputs de texto: `.trim().replace(",", ".")`
solo convierte la coma decimal, pero no contempla el punto de miles del
formato es-AR. Consecuencia:
  - "15.000" (quince mil, con punto de miles) se interpretaba como 15
    — silenciosamente, sin ningún error. El bug más peligroso: da un
    resultado numérico "válido" pero incorrecto.
  - "1.234,56" (mil doscientos treinta y cuatro con 56, con punto de
    miles Y coma decimal) daba NaN — al menos visible como error, pero
    innecesario.

Reemplaza cada `<expr>.trim().replace(",", ".")` por
`normalizeNumberInput(<expr>)`, e inyecta esa función (validada con 12
casos de borde, ver el commit) al principio del IIFE de cada archivo.
Idempotente.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HELPER = '''  // Convierte un input numérico en formato es-AR ("15.000" con punto de
  // miles, "1.234,56" con punto de miles y coma decimal, o un número
  // simple como "9.8") al formato que entiende Number(). Un punto seguido
  // de 1, 2 o más de 3 dígitos se interpreta como separador decimal (no
  // de miles), evitando falsos positivos como "3.14" o "0.5".
  function normalizeNumberInput(value) {
    let str = String(value).trim();
    if (str.includes(",")) {
      str = str.replace(/\\./g, "").replace(",", ".");
    } else if (/^-?[1-9]\\d{0,2}(\\.\\d{3})+$/.test(str)) {
      str = str.replace(/\\./g, "");
    }
    return str;
  }

'''

CALL_RE = re.compile(r'= (.+?)\.trim\(\)\.replace\(",", "\."\);')
IIFE_RE = re.compile(r'(\(function \(\) \{\n)')

script_files = sorted(ROOT.glob("calculadoras/**/script.js"))
changed = 0
skipped = 0

for path in script_files:
    text = path.read_text(encoding="utf-8")
    if "normalizeNumberInput" in text:
        skipped += 1
        continue
    if not CALL_RE.search(text):
        continue  # esta calculadora no tiene el patrón (no debería pasar, pero por las dudas)

    text = CALL_RE.sub(lambda m: f"= normalizeNumberInput({m.group(1)});", text)
    text = IIFE_RE.sub(lambda m: m.group(1) + HELPER, text, count=1)

    path.write_text(text, encoding="utf-8")
    changed += 1
    print(f"actualizado: {path.relative_to(ROOT)}")

print(f"\n{changed} archivos actualizados, {skipped} ya tenían el fix.")
