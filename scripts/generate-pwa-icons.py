"""generate-pwa-icons.py — Íconos de la PWA (192, 512 y maskable 512) con el Sigma del logo."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

IMG = Path(__file__).resolve().parent.parent / "assets" / "img"
PRIMARY = (37, 99, 235)
FONT = "C:/Windows/Fonts/arialbd.ttf"


def icon(size, rounded, glyph_ratio):
    s = size * 4
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if rounded:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.22), fill=PRIMARY)
    else:
        d.rectangle([0, 0, s, s], fill=PRIMARY)  # maskable: sangrado completo
    f = ImageFont.truetype(FONT, int(s * glyph_ratio))
    b = d.textbbox((0, 0), "\u2211", font=f)
    d.text(((s - (b[2] - b[0])) / 2 - b[0], (s - (b[3] - b[1])) / 2 - b[1]), "\u2211", font=f, fill=(255, 255, 255))
    return img.resize((size, size), Image.LANCZOS)


icon(192, True, 0.62).save(IMG / "pwa-192.png")
icon(512, True, 0.62).save(IMG / "pwa-512.png")
icon(512, False, 0.48).save(IMG / "pwa-maskable-512.png")  # glifo dentro de la zona segura (80 %)
print("ok")
