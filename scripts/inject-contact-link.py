"""
inject-contact-link.py — Agrega el enlace "Contacto" a la línea de copyright del pie de TODAS las páginas (idempotente).
Se coloca a continuación del enlace "Términos". Correr después de generar páginas nuevas con una plantilla vieja; las plantillas actuales
(page_templates.py) ya lo traen.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERN = re.compile(r'(<a href="/terminos-de-uso/" class="([^"]*)">Términos</a>)(</p>)')

changed = skipped = missing = 0
for f in sorted(list(ROOT.rglob("index.html")) + [ROOT / "404.html"]):
    rel = f.relative_to(ROOT).as_posix()
    if rel.startswith(("tools/", "functions/", "node_modules/", ".wrangler/")):
        continue
    s = f.read_text(encoding="utf-8")
    if 'href="/contacto/"' in s:
        skipped += 1
        continue
    new, n = PATTERN.subn(lambda m: f'{m.group(1)} · <a href="/contacto/" class="{m.group(2)}">Contacto</a>{m.group(3)}', s, count=1)
    if n:
        f.write_text(new, encoding="utf-8")
        changed += 1
    elif "</footer>" in s:
        missing += 1
        print("AVISO: no encontré el pie esperado en", rel)
print(f"{changed} páginas actualizadas, {skipped} ya lo tenían, {missing} sin patrón.")
