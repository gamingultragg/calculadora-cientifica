"""
inject-analytics.py — Agrega el snippet de Cloudflare Web Analytics justo
antes de </body> en todas las páginas. Idempotente.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SNIPPET = (
    "<!-- Cloudflare Web Analytics -->"
    "<script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' "
    'data-cf-beacon=\'{"token": "62cded9cafa8475a9f6f875888b918b9"}\'></script>'
    "<!-- End Cloudflare Web Analytics -->"
)

pages = sorted(ROOT.glob("**/index.html")) + [ROOT / "404.html"]
changed = 0
skipped = 0

for page in pages:
    text = page.read_text(encoding="utf-8")
    if "Cloudflare Web Analytics" in text:
        skipped += 1
        continue
    if "</body>" not in text:
        print(f"AVISO: no se encontró </body> en {page.relative_to(ROOT)}")
        continue

    text = text.replace("</body>", f"  {SNIPPET}\n</body>", 1)
    page.write_text(text, encoding="utf-8")
    changed += 1
    print(f"actualizado: {page.relative_to(ROOT)}")

print(f"\n{changed} archivos actualizados, {skipped} ya lo tenían.")
