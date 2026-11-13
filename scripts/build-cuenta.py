"""
build-cuenta.py — Página /cuenta/ (administración de la cuenta). El contenido lo dibuja assets/js/account.js
dentro de #cc-cuenta. No se indexa (noindex) ni va en el sitemap. Generación de una sola vez.
"""
from pathlib import Path

from page_templates import BEACON, FLOATING, FOOTER, HEADER, SKIP, head

ROOT = Path(__file__).resolve().parent.parent
url = "/cuenta/"
html_head = head(url, "Mi cuenta | Calculadora Científica", "Administrá tu cuenta de Calculadora Científica: tus datos guardados, descargarlos o eliminar tu cuenta.",
                 "Mi cuenta", "Tu cuenta de Calculadora Científica.", "website",
                 {"@context": "https://schema.org", "@type": "WebPage", "name": "Mi cuenta", "url": "https://www.calculadoracientifica.com.ar/cuenta/"})
html_head = html_head.replace('<meta name="description"', '<meta name="robots" content="noindex, nofollow" />\n<meta name="description"', 1)

page = f"""{html_head}
<body class="min-h-screen font-sans antialiased">
  {SKIP}

  {HEADER}

  <main id="main-content" class="max-w-3xl mx-auto px-4 sm:px-6 py-8">
    <h1 class="font-display font-extrabold text-2xl sm:text-3xl">Mi cuenta</h1>
    <p class="mt-2 text-sm text-[var(--color-text-muted)]">Tu cuenta es opcional: sirve para guardar tus favoritas, tu historial y tus preferencias en todos tus dispositivos.
      Más información en la <a class="text-[var(--color-primary-link)] hover:underline" href="/privacidad/#cuenta">Política de Privacidad</a>.</p>
    <div id="cc-cuenta" class="surface rounded-2xl p-5 mt-6 shadow-sm">
      <noscript><p>Necesitás activar JavaScript para administrar tu cuenta.</p></noscript>
      <p class="text-sm text-[var(--color-text-muted)]">Cargando…</p>
    </div>
  </main>

  {FOOTER}
  {BEACON}
{FLOATING}
</body>
</html>
"""
out = ROOT / "cuenta" / "index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(page, encoding="utf-8")
print("escrito:", out.relative_to(ROOT))
