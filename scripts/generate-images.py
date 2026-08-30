"""
generate-images.py — Genera los PNG derivados de la identidad visual
(favicons de respaldo, apple-touch-icon y la imagen Open Graph) a partir
de fuentes del sistema, usando Pillow. Se ejecuta una sola vez (o cuando
cambie la marca); los archivos generados se versionan en assets/img/.

Uso:
    python scripts/generate-images.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "assets" / "img"
IMG_DIR.mkdir(parents=True, exist_ok=True)

PRIMARY = (37, 99, 235)  # #2563EB — blue-600
PRIMARY_DARK = (29, 78, 216)  # #1D4ED8 — blue-700
WHITE = (255, 255, 255)

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_REGULAR = "C:/Windows/Fonts/arial.ttf"

SIGMA = "\u2211"


def rounded_square_icon(size: int, radius_ratio: float = 0.22) -> Image.Image:
    """Cuadrado redondeado azul con el símbolo Sigma blanco, igual que el logo del header."""
    scale = 4  # supersample para bordes prolijos
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


def og_image() -> Image.Image:
    """Imagen Open Graph 1200x630 para compartir en redes sociales."""
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), PRIMARY)
    draw = ImageDraw.Draw(img)

    # Degrade sutil vertical hacia el azul mas oscuro
    for y in range(h):
        t = y / h
        r = int(PRIMARY[0] + (PRIMARY_DARK[0] - PRIMARY[0]) * t)
        g = int(PRIMARY[1] + (PRIMARY_DARK[1] - PRIMARY[1]) * t)
        b = int(PRIMARY[2] + (PRIMARY_DARK[2] - PRIMARY[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Marca de agua Sigma sutil, confinada a la franja derecha para no cruzar el texto
    watermark_font = ImageFont.truetype(FONT_BOLD, 380)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.text((940, 110), SIGMA, font=watermark_font, fill=(255, 255, 255, 22))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Logo pequeno (cuadrado + Sigma) arriba a la izquierda
    logo = rounded_square_icon(72)
    img.paste(logo, (80, 80), logo)
    logo_font = ImageFont.truetype(FONT_BOLD, 34)
    draw.text((168, 96), "Calculadora Científica", font=logo_font, fill=WHITE)

    # Titulo principal
    title_font = ImageFont.truetype(FONT_BOLD, 64)
    draw.text((80, 230), "Calculadoras científicas", font=title_font, fill=WHITE)
    draw.text((80, 305), "online, gratis y explicadas", font=title_font, fill=WHITE)

    # Subtitulo con categorias
    sub_font = ImageFont.truetype(FONT_REGULAR, 28)
    draw.text(
        (80, 415),
        "Matemáticas · Estadística · Física · Química · Ingeniería · Finanzas",
        font=sub_font,
        fill=(219, 234, 254),  # blue-100
    )

    # URL
    url_font = ImageFont.truetype(FONT_BOLD, 26)
    draw.text((80, 505), "www.calculadoracientifica.com.ar", font=url_font, fill=WHITE)

    return img


def main():
    rounded_square_icon(16).save(IMG_DIR / "favicon-16.png")
    rounded_square_icon(32).save(IMG_DIR / "favicon-32.png")
    rounded_square_icon(180).save(IMG_DIR / "apple-touch-icon.png")
    rounded_square_icon(512).convert("RGB").save(IMG_DIR / "logo-512.png")
    og_image().save(IMG_DIR / "og-image.png", quality=92)
    print("OK: favicon-16.png, favicon-32.png, apple-touch-icon.png, logo-512.png, og-image.png")


if __name__ == "__main__":
    main()
