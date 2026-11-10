"""
inject-ad-slots.py — Coloca los contenedores de anuncios (ver assets/js/ads.js).

Ubicaciones (una por página, nunca arriba de todo ni junto al teclado de una
calculadora, y sin anuncios en páginas legales, "Sobre nosotros" ni 404):
  - calculadoras: columna derecha, debajo de la ayuda y los enlaces   -> data-ad="calc"
  - guías:        al final del artículo, antes de "relacionadas"       -> data-ad="guide"
  - home:         entre la grilla de calculadoras y las guías          -> data-ad="home"
  - categorías:   debajo de la grilla de calculadoras                  -> data-ad="cat"

Los contenedores nacen ocultos (atributo hidden): no ocupan espacio hasta que ads.js
tenga un ID de unidad configurado. Idempotente: salta las páginas que ya los tienen.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_TAG = '<script src="/assets/js/ads.js" defer></script>'
BACKTOP = '<script src="/assets/js/back-to-top.js"></script>'


def aside(kind, indent):
    pad = " " * indent
    return (
        f'{pad}<aside class="cc-ad" data-ad="{kind}" aria-label="Publicidad" hidden>\n'
        f'{pad}  <p class="cc-ad-label">Publicidad</p>\n'
        f'{pad}  <div class="cc-ad-slot"></div>\n'
        f"{pad}</aside>\n"
    )


def add_script(text):
    if SCRIPT_TAG in text:
        return text
    return text.replace(BACKTOP, SCRIPT_TAG + "\n" + BACKTOP, 1)


def process(page, kind):
    text = page.read_text(encoding="utf-8")
    if 'data-ad="' in text:
        return "ya tenía"
    new = None
    if kind == "calc":
        # Fin de la columna derecha: <section>...</section> + </section></div></main>
        pat = re.compile(r"(</section>)(\s*)(</section>\s*</div>\s*</main>)")
        new, n = pat.subn(lambda m: m.group(1) + "\n\n" + aside("calc", 8) + m.group(3), text, count=1)
        if n == 0:
            return "SIN ANCLAJE"
    elif kind == "guide":
        new, n = re.subn(r"(</article>)", lambda m: m.group(1) + "\n\n" + aside("guide", 4).rstrip("\n"), text, count=1)
        if n == 0:
            return "SIN ANCLAJE"
    elif kind == "home":
        marker = '  <section id="guias"'
        if marker not in text:
            return "SIN ANCLAJE"
        new = text.replace(marker, '  <div class="max-w-6xl mx-auto px-4 sm:px-6">\n' + aside("home", 4) + "  </div>\n\n" + marker, 1)
    elif kind == "cat":
        end = "<!-- CC-PRERENDER:END --></div>"
        if end not in text:
            return "SIN ANCLAJE"
        new = text.replace(end, end + "\n" + aside("cat", 4).rstrip("\n"), 1)
    page.write_text(add_script(new), encoding="utf-8")
    return "ok"


def main():
    jobs = []
    for p in sorted(ROOT.glob("calculadoras/*/*/index.html")):
        jobs.append((p, "calc"))
    for p in sorted(ROOT.glob("guias/*/index.html")):
        jobs.append((p, "guide"))
    jobs.append((ROOT / "index.html", "home"))
    for p in sorted(ROOT.glob("calculadoras/*/index.html")):
        jobs.append((p, "cat"))

    counts = {}
    for page, kind in jobs:
        res = process(page, kind)
        counts[res] = counts.get(res, 0) + 1
        if res == "SIN ANCLAJE":
            print(f"AVISO: sin anclaje en {page.relative_to(ROOT)}")
    print(counts)


if __name__ == "__main__":
    main()
