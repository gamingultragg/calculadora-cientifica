"""
validate-sitemap.py — Valida que sitemap.xml sea XML bien formado y que
coincida exactamente con las páginas reales del sitio:
  1. Toda URL listada en el sitemap debe resolver a una página real.
  2. Toda página indexable real (todas menos 404.html, que lleva noindex)
     debe estar listada en el sitemap.
No modifica nada, solo reporta.
"""
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.calculadoracientifica.com.ar"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# --- 1. Parsear el sitemap ------------------------------------------------
sitemap_path = ROOT / "sitemap.xml"
try:
    tree = ET.parse(sitemap_path)
except ET.ParseError as e:
    print(f"ERROR: sitemap.xml no es XML válido — {e}")
    raise SystemExit(1)

sitemap_locs = [el.text.strip() for el in tree.getroot().findall("sm:url/sm:loc", NS)]
print(f"sitemap.xml es XML válido. {len(sitemap_locs)} URLs listadas.\n")

# --- 2. Páginas reales en disco (excluyendo la 404, que es noindex) ------
pages = sorted(ROOT.glob("**/index.html"))
real_paths = {"/" + str(p.relative_to(ROOT)).replace("index.html", "").replace("\\", "/") for p in pages}
real_urls = {SITE + p for p in real_paths}

sitemap_url_set = set(sitemap_locs)

# --- 3. Duplicados dentro del propio sitemap ------------------------------
dupes = {u for u in sitemap_locs if sitemap_locs.count(u) > 1}

# --- 4. Comparación --------------------------------------------------------
missing_from_disk = sorted(sitemap_url_set - real_urls)  # en el sitemap pero no existen
missing_from_sitemap = sorted(real_urls - sitemap_url_set)  # existen pero no están listadas

print("=== URLs duplicadas dentro de sitemap.xml ===")
print("  Ninguna." if not dupes else "\n".join(f"  {u}" for u in sorted(dupes)))

print("\n=== URLs en sitemap.xml que no resuelven a una página real ===")
print("  Ninguna." if not missing_from_disk else "\n".join(f"  {u}" for u in missing_from_disk))

print("\n=== Páginas reales (indexables) que faltan en sitemap.xml ===")
print("  Ninguna." if not missing_from_sitemap else "\n".join(f"  {u}" for u in missing_from_sitemap))
