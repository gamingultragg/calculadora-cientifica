"""
generate-favicon-ico.py — Genera el favicon.ico clásico (multi-resolución)
en la raíz del sitio, como respaldo para navegadores/crawlers viejos que
no soportan <link rel="icon" type="image/svg+xml"> ni PNG declarado.

Reusa el mismo ícono (cuadrado redondeado azul + Sigma) que
generate-images.py, para que los tres formatos (SVG, PNG, ICO) sean
visualmente idénticos.

Uso:
    python scripts/generate-favicon-ico.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent

PRIMARY = (37, 99, 235)  # #2563EB — blue-600
WHITE = (255, 255, 255)

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
SIGMA = "\u2211"


def rounded_square_icon(size: int, radius_ratio: float = 0.22) -> Image.Image:
    scale = 4
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    radius = int(s * radius_ratio)
    draw.rounded_rectangle([0, 0, s - 1, s - 1], radius=radius, fill=PRIMARY)

    font = ImageFont.truetype(FONT_BOLD, int(s * 0.62))
    bbox = draw.textbbox((0, 0), SIGMA, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((s - tw) / 2 - bbox[0], (s - th) / 2 - bbox[1]), SIGMA, font=font, fill=WHITE)

    return img.resize((size, size), Image.LANCZOS)


def main():
    sizes = [16, 32, 48, 64]
    base = rounded_square_icon(max(sizes))
    out = ROOT / "favicon.ico"
    base.save(out, format="ICO", sizes=[(s, s) for s in sizes])
    print(f"OK: {out} ({', '.join(str(s) for s in sizes)}px)")


if __name__ == "__main__":
    main()
