"""
validate-jsonld.py — Valida que cada bloque <script type="application/ld+json">
de cada página sea JSON sintácticamente válido, y hace chequeos básicos de
forma (tiene "@context", tiene "@graph" o "@type"). No valida contra el
vocabulario completo de Schema.org, solo la sintaxis y forma general.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.calculadoracientifica.com.ar"
JSONLD_RE = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL
)

pages = sorted(ROOT.glob("**/index.html")) + [ROOT / "404.html"]
page_paths = {
    "/" + str(p.relative_to(ROOT)).replace("index.html", "").replace("\\", "/") for p in pages
}

total_blocks = 0
errors = []


def walk_urls(node):
    """Recorre el JSON-LD y devuelve todas las URLs propias del sitio referenciadas."""
    found = []
    if isinstance(node, dict):
        for key in ("url", "item", "mainEntityOfPage"):
            value = node.get(key)
            if isinstance(value, str) and value.startswith(SITE):
                found.append(value)
        for value in node.values():
            found.extend(walk_urls(value))
    elif isinstance(node, list):
        for item in node:
            found.extend(walk_urls(item))
    return found

for page in pages:
    text = page.read_text(encoding="utf-8")
    blocks = JSONLD_RE.findall(text)
    for i, block in enumerate(blocks):
        total_blocks += 1
        rel = page.relative_to(ROOT)
        try:
            data = json.loads(block)
        except json.JSONDecodeError as e:
            errors.append(f"{rel} (bloque {i+1}): JSON inválido — {e}")
            continue

        if "@context" not in data:
            errors.append(f"{rel} (bloque {i+1}): falta \"@context\"")
        if "@graph" not in data and "@type" not in data:
            errors.append(f"{rel} (bloque {i+1}): falta \"@graph\" o \"@type\"")

        # Si es @graph, chequear que cada item tenga @type
        if "@graph" in data:
            for j, item in enumerate(data["@graph"]):
                if "@type" not in item:
                    errors.append(f"{rel} (bloque {i+1}, item {j+1}): falta \"@type\" en @graph")

        # Chequear que las URLs propias referenciadas apunten a páginas reales
        for url in walk_urls(data):
            path = url[len(SITE):] or "/"
            if not path.endswith("/"):
                path += "/"
            if path not in page_paths:
                errors.append(f"{rel} (bloque {i+1}): URL en JSON-LD no resuelve a una página real — {url}")

print(f"Páginas analizadas: {len(pages)}")
print(f"Bloques JSON-LD encontrados: {total_blocks}\n")

if errors:
    print(f"=== {len(errors)} problema(s) encontrado(s) ===")
    for e in errors:
        print(f"  {e}")
else:
    print("=== Todos los bloques son JSON válido y tienen forma correcta ===")
