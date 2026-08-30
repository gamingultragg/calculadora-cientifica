"""
check-contrast.py — Calcula el ratio de contraste WCAG entre los pares
texto/fondo de la paleta de diseño (assets/css/styles.css), en modo claro
y oscuro, y los evalúa contra AA (4.5:1 texto normal, 3:1 texto grande /
componentes de UI). No modifica nada, solo reporta.
"""


def relative_luminance(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4))

    def channel(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = channel(r), channel(g), channel(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(hex1, hex2):
    l1, l2 = relative_luminance(hex1), relative_luminance(hex2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


LIGHT = {
    "bg": "#f8fafc",
    "surface": "#ffffff",
    "text": "#0f172a",
    "text-muted": "#64748b",
    "primary": "#2563eb",
    "primary-link": "#2563eb",
    "danger": "#e11d48",
    "accent": "#10b981",
}

DARK = {
    "bg": "#0f172a",
    "surface": "#1e293b",
    "text": "#f1f5f9",
    "text-muted": "#94a3b8",
    "primary": "#3b82f6",
    "primary-link": "#60a5fa",
    "danger": "#fb7185",
    "accent": "#34d399",
}

# Pares (texto, fondo, "tipo de uso") a chequear en cada tema
PAIRS = [
    ("text", "bg", "texto principal sobre fondo de página (normal, requiere 4.5:1)"),
    ("text", "surface", "texto principal sobre tarjeta (normal, requiere 4.5:1)"),
    ("text-muted", "bg", "texto secundario sobre fondo de página (normal, requiere 4.5:1)"),
    ("text-muted", "surface", "texto secundario sobre tarjeta (normal, requiere 4.5:1)"),
    ("primary-link", "bg", "enlaces sobre fondo de página (normal, requiere 4.5:1)"),
    ("primary-link", "surface", "enlaces sobre tarjeta (normal, requiere 4.5:1)"),
    ("danger", "surface", "texto de error sobre tarjeta (normal, requiere 4.5:1)"),
]


def evaluate(theme_name, palette):
    print(f"\n=== Modo {theme_name} ===")
    for fg_key, bg_key, desc in PAIRS:
        ratio = contrast_ratio(palette[fg_key], palette[bg_key])
        passes_aa = ratio >= 4.5
        status = "OK" if passes_aa else "FALLA AA"
        print(f"  {fg_key} / {bg_key}: {ratio:.2f}:1 — {status} — {desc}")


evaluate("claro", LIGHT)
evaluate("oscuro", DARK)
