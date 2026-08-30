"""
audit-links.py — Auditoría de integridad de enlaces internos y metadatos
del sitio. Recorre todos los index.html, extrae hrefs internos (que
empiezan con "/"), y verifica que cada uno resuelva a una página real.
También chequea duplicados de <title> y de meta description, y que cada
página tenga los tags de favicon/OG.

No modifica nada — solo reporta. Ejecutar tras cualquier tanda grande de
páginas nuevas, antes de darlas por terminadas.
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
pages = sorted(ROOT.glob("**/index.html"))
page_paths = {"/" + str(p.relative_to(ROOT)).replace("index.html", "").replace("\\", "/") for p in pages}
# Normalizar: la home es "/" ya está bien; el resto debe terminar en "/"
page_paths = {p if p == "/" else p for p in page_paths}

HREF_RE = re.compile(r'href="(/[^"]*)"')
TITLE_RE = re.compile(r"<title>([^<]*)</title>")
DESC_RE = re.compile(r'<meta name="description" content="([^"]*)"')

titles = defaultdict(list)
descriptions = defaultdict(list)
broken_links = []
missing_favicon = []
missing_og_image = []

for page in pages:
    text = page.read_text(encoding="utf-8")
    rel = "/" + str(page.relative_to(ROOT)).replace("index.html", "").replace("\\", "/")

    title_match = TITLE_RE.search(text)
    if title_match:
        titles[title_match.group(1)].append(rel)

    desc_match = DESC_RE.search(text)
    if desc_match:
        descriptions[desc_match.group(1)].append(rel)

    if "favicon.svg" not in text:
        missing_favicon.append(rel)
    if "og-image.png" not in text:
        missing_og_image.append(rel)

    for href in HREF_RE.findall(text):
        # Ignorar anclas (#) y assets (tienen extensión de archivo)
        path_only = href.split("#")[0]
        if path_only == "":
            continue  # href="/#categorias" -> path_only vacío, es la home, válido
        if "." in path_only.rsplit("/", 1)[-1]:
            continue  # asset (css/js/png/xml/txt), no es una página de contenido
        normalized = path_only if path_only.endswith("/") else path_only + "/"
        if normalized not in page_paths:
            broken_links.append((rel, href))

print(f"Páginas analizadas: {len(pages)}\n")

print("=== Enlaces internos rotos ===")
if broken_links:
    for source, href in broken_links:
        print(f"  {source} -> {href}")
else:
    print("  Ninguno.")

print("\n=== <title> duplicados ===")
dupes = {t: locs for t, locs in titles.items() if len(locs) > 1}
if dupes:
    for t, locs in dupes.items():
        print(f'  "{t}": {locs}')
else:
    print("  Ninguno.")

print("\n=== Meta description duplicadas ===")
dupes_desc = {d: locs for d, locs in descriptions.items() if len(locs) > 1}
if dupes_desc:
    for d, locs in dupes_desc.items():
        print(f'  "{d[:60]}...": {locs}')
else:
    print("  Ninguna.")

print("\n=== Páginas sin favicon ===")
print("  Ninguna." if not missing_favicon else "\n".join(f"  {p}" for p in missing_favicon))

print("\n=== Páginas sin og:image ===")
print("  Ninguna." if not missing_og_image else "\n".join(f"  {p}" for p in missing_og_image))
