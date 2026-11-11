"""
page_templates.py — Plantillas HTML para páginas nuevas (calculadoras y guías), con el
mismo <head>, header, footer, JSON-LD y botones flotantes que el resto del sitio.

Uso (ver scripts/build-batch-2.py): calc_page(...) y guide_page(...) devuelven el HTML
completo. Después de generar páginas nuevas hay que correr, en este orden:
    python scripts/prerender-cards.py        (grillas de calculadoras)
    python scripts/inject-ad-slots.py        (contenedores de anuncios)
    cd tools/tailwind && npm run build       (CSS compilado, por si hay clases nuevas)
"""
import html
import json

BASE = "https://www.calculadoracientifica.com.ar"
BEACON = (
    "<!-- Cloudflare Web Analytics --><script type='module' "
    "src='https://static.cloudflareinsights.com/beacon.min.js' "
    "data-cf-beacon='{\"token\": \"62cded9cafa8475a9f6f875888b918b9\"}'></script>"
    "<!-- End Cloudflare Web Analytics -->"
)
FLOATING = """<a href="/" id="back-to-home" aria-label="Ir al inicio del sitio"
  class="fixed bottom-6 right-6 z-40 w-11 h-11 rounded-full surface shadow-lg hidden lg:flex items-center justify-center transition-all duration-200 hover:shadow-xl">
  <svg class="w-5 h-5 text-[var(--color-text)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
    <path stroke-linecap="round" stroke-linejoin="round" d="M3 9.5L12 3l9 6.5M5 9.5V20a1 1 0 001 1h4v-6h4v6h4a1 1 0 001-1V9.5"/>
  </svg>
</a>
<button id="back-to-top" type="button" aria-label="Volver al inicio de la página"
  class="fixed bottom-20 right-6 z-40 w-11 h-11 rounded-full bg-[var(--color-primary)] text-white shadow-lg hidden lg:flex items-center justify-center opacity-0 pointer-events-none translate-y-2 transition-all duration-200 hover:brightness-110">
  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
    <path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7"/>
  </svg>
</button>
<script src="/assets/js/back-to-top.js"></script>
<script src="/assets/js/pwa.js" defer></script>"""
SKIP = ('<a href="#main-content" class="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 '
        'focus:z-50 focus:px-4 focus:py-2 focus:rounded-lg focus:bg-[var(--color-primary)] '
        'focus:text-white focus:text-sm focus:font-semibold">Saltar al contenido</a>')
HEADER = """<header class="sticky top-0 z-40 backdrop-blur border-b border-[var(--color-border)] bg-[var(--color-bg)]/85">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <a href="/" class="flex items-center gap-2 font-display font-extrabold text-lg">
        <span class="w-8 h-8 rounded-lg bg-[var(--color-primary)] text-white flex items-center justify-center text-sm">∑</span>
        Calculadora<span class="text-[var(--color-primary-link)]">Científica</span>
      </a>
      <button data-theme-toggle type="button" aria-label="Cambiar tema claro/oscuro"
        class="w-10 h-10 rounded-full surface flex items-center justify-center hover:shadow-md transition-shadow">
        <span data-theme-icon>🌙</span>
      </button>
    </div>
  </header>"""
FOOTER = """<footer class="border-t border-[var(--color-border)] mt-10">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 py-10 text-sm text-[var(--color-text-muted)] flex flex-col sm:flex-row items-center justify-between gap-4">
      <p>© 2026 Calculadora Científica · Hecho en Argentina 🇦🇷 · <a href="/sobre-nosotros/" class="hover:text-[var(--color-primary-link)]">Sobre Nosotros</a> · <a href="/privacidad/" class="hover:text-[var(--color-primary-link)]">Privacidad</a> · <a href="/terminos-de-uso/" class="hover:text-[var(--color-primary-link)]">Términos</a></p>
      <a href="/" class="hover:text-[var(--color-primary-link)]">← Volver al inicio</a>
    </div>
  </footer>"""
ARROW_LINK = "text-[var(--color-primary-link)] hover:underline"


def esc(s):
    return html.escape(s, quote=True)


def head(url, title, desc, og_title, og_desc, og_type, jsonld):
    return f"""<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<link rel="canonical" href="{BASE}{url}" />
<link rel="alternate" hreflang="es-AR" href="{BASE}{url}" />
<link rel="alternate" hreflang="es" href="{BASE}{url}" />
<link rel="icon" type="image/svg+xml" href="/assets/img/favicon.svg" />
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png" />
<link rel="icon" type="image/png" sizes="16x16" href="/assets/img/favicon-16.png" />
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png" />
<link rel="manifest" href="/manifest.webmanifest" />
<meta name="theme-color" content="#2563eb" />

<meta property="og:type" content="{og_type}" />
<meta property="og:locale" content="es_AR" />
<meta property="og:site_name" content="Calculadora Científica" />
<meta property="og:title" content="{esc(og_title)}" />
<meta property="og:description" content="{esc(og_desc)}" />
<meta property="og:url" content="{BASE}{url}" />
<meta property="og:image" content="{BASE}/assets/img/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:image" content="{BASE}/assets/img/og-image.png" />
<meta name="twitter:card" content="summary_large_image" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Roboto+Mono:wght@400;500;700&display=swap" rel="stylesheet" />

<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7274131858034505" crossorigin="anonymous"></script>
<link rel="stylesheet" href="/assets/css/styles.css" />
<link rel="stylesheet" href="/assets/css/tailwind.css" />
<script src="/assets/js/theme.js"></script>

<script type="application/ld+json">
{json.dumps(jsonld, ensure_ascii=False, indent=2)}
</script>
</head>"""


def faq_schema(faqs):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs
        ],
    }


def faq_html(faqs, tag="dl"):
    items = "\n".join(
        f'        <div>\n          <dt class="font-semibold text-[var(--color-text)]">{esc(q)}</dt>\n          <dd>{a_html}</dd>\n        </div>'
        for q, a_html in [(q, esc(a)) for q, a in faqs]
    )
    return f'<dl class="space-y-4 text-[var(--color-text-muted)] leading-relaxed">\n{items}\n      </dl>'


def calc_page(*, slug, cat_slug, cat_label, name, page_title, desc, og_title, og_desc, schema_desc,
              intro, top_html="", form_html, result_html, help_html, related, guide, faqs, extra_scripts=""):
    """related: [(href, label)]; guide: (href, titulo, texto del bloque)."""
    url = f"/calculadoras/{cat_slug}/{slug}/"
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SoftwareApplication", "name": name,
                "applicationCategory": "EducationalApplication", "operatingSystem": "Web",
                "url": BASE + url, "description": schema_desc,
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "ARS"}, "inLanguage": "es-AR",
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": cat_label, "item": f"{BASE}/calculadoras/{cat_slug}/"},
                    {"@type": "ListItem", "position": 3, "name": name, "item": BASE + url},
                ],
            },
            faq_schema(faqs),
        ],
    }
    rel = "\n".join(f'            <li><a class="{ARROW_LINK}" href="{h}">{esc(l)}</a></li>' for h, l in related)
    g_href, g_title, g_text = guide
    return f"""{head(url, page_title, desc, og_title, og_desc, "website", jsonld)}
<body class="min-h-screen font-sans antialiased">
  {SKIP}

  {HEADER}

  <main id="main-content" class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
    <nav aria-label="Breadcrumb" class="text-sm text-[var(--color-text-muted)] mb-4">
      <ol class="flex flex-wrap items-center gap-1">
        <li><a href="/" class="hover:text-[var(--color-primary-link)]">Inicio</a></li>
        <li aria-hidden="true">/</li>
        <li><a href="/calculadoras/{cat_slug}/" class="hover:text-[var(--color-primary-link)]">{esc(cat_label)}</a></li>
        <li aria-hidden="true">/</li>
        <li class="text-[var(--color-text)] font-medium" aria-current="page">{esc(name)}</li>
      </ol>
    </nav>

    <h1 class="font-display font-extrabold text-2xl sm:text-3xl">{esc(name)}</h1>
    <p class="mt-2 text-[var(--color-text-muted)] max-w-2xl">
      {intro}
    </p>
{top_html}
    <div class="mt-6 grid grid-cols-1 lg:grid-cols-[420px_1fr] gap-6 items-start">
      <section class="surface rounded-2xl p-5 shadow-sm">
        <div id="err" class="hidden alert-error rounded-lg px-3 py-2 text-sm mb-4" role="alert" aria-live="polite"></div>
{form_html}
      </section>

      <section class="space-y-4">
{result_html}

        <details class="help-accordion surface rounded-2xl p-5 shadow-sm" open>
          <summary class="flex items-center justify-between font-display font-semibold text-lg">
            Ayuda y Fórmulas Teóricas
            <svg class="chevron w-5 h-5 text-[var(--color-text-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg>
          </summary>
          <div class="mt-4 space-y-4 text-sm leading-relaxed text-[var(--color-text-muted)]">
{help_html}
          </div>
        </details>

        <section class="surface rounded-2xl p-5 shadow-sm">
          <h2 class="font-display font-semibold text-lg mb-3">Preguntas frecuentes</h2>
          <div class="text-sm">
      {faq_html(faqs)}
          </div>
        </section>

        <section class="surface rounded-2xl p-5 shadow-sm">
          <h2 class="font-display font-semibold text-lg mb-2">Calculadoras relacionadas</h2>
          <ul class="space-y-2 text-sm">
{rel}
          </ul>
        </section>

        <section class="surface rounded-2xl p-5 shadow-sm">
          <h2 class="font-display font-semibold text-lg mb-2">¿Querés entender el "por qué"?</h2>
          <p class="text-sm text-[var(--color-text-muted)] mb-3">{esc(g_text)}</p>
          <a class="{ARROW_LINK} text-sm font-semibold" href="{g_href}">{esc(g_title)} →</a>
        </section>
      </section>
    </div>
  </main>

  {FOOTER}

  <script src="script.js"></script>
{extra_scripts}  {BEACON}
{FLOATING}
</body>
</html>
"""


def guide_page(*, slug, name, page_title, desc, og_desc, headline, intro, quick, cta, body_html, faqs, related):
    """cta: (href, texto del botón). quick: texto de la 'respuesta rápida' (HTML)."""
    url = f"/guias/{slug}/"
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article", "headline": headline, "description": desc,
                "author": {"@type": "Organization", "name": "Calculadora Científica"},
                "publisher": {"@type": "Organization", "name": "Calculadora Científica"},
                "mainEntityOfPage": BASE + url, "inLanguage": "es-AR",
                "datePublished": "2026-11-10", "dateModified": "2026-11-10",
            },
            faq_schema(faqs),
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Guías", "item": BASE + "/guias/"},
                    {"@type": "ListItem", "position": 3, "name": name, "item": BASE + url},
                ],
            },
        ],
    }
    rel = "\n".join(f'        <li><a class="{ARROW_LINK}" href="{h}">{esc(l)}</a></li>' for h, l in related)
    return f"""{head(url, page_title, desc, name, og_desc, "article", jsonld)}
<body class="min-h-screen font-sans antialiased">
  {SKIP}

  {HEADER}

  <main id="main-content" class="max-w-3xl mx-auto px-4 sm:px-6 py-8">
    <nav aria-label="Breadcrumb" class="text-sm text-[var(--color-text-muted)] mb-4">
      <ol class="flex flex-wrap items-center gap-1">
        <li><a href="/" class="hover:text-[var(--color-primary-link)]">Inicio</a></li>
        <li aria-hidden="true">/</li>
        <li><a href="/guias/" class="hover:text-[var(--color-primary-link)]">Guías</a></li>
        <li aria-hidden="true">/</li>
        <li class="text-[var(--color-text)] font-medium" aria-current="page">{esc(name)}</li>
      </ol>
    </nav>

    <article>
      <h1 class="font-display font-extrabold text-2xl sm:text-3xl">{esc(headline)}</h1>
      <p class="mt-3 text-[var(--color-text-muted)] leading-relaxed">
        {intro}
      </p>

      <div class="mt-5 rounded-2xl surface p-4 text-sm leading-relaxed">
        <p class="font-semibold text-[var(--color-text)] mb-1">Respuesta rápida</p>
        <p class="text-[var(--color-text-muted)]">{quick}</p>
      </div>

      <div class="mt-6 rounded-2xl surface p-4 flex items-center justify-between gap-3">
        <p class="text-sm">¿Preferís que lo calcule por vos?</p>
        <a href="{cta[0]}" class="calc-btn calc-btn--op px-4 py-2 text-sm whitespace-nowrap">{esc(cta[1])}</a>
      </div>

{body_html}

      <h2 class="font-display font-bold text-xl mt-8 mb-2">Preguntas frecuentes</h2>
      {faq_html(faqs)}
    </article>

    <section class="mt-10 surface rounded-2xl p-5 shadow-sm">
      <h2 class="font-display font-semibold text-lg mb-2">Calculadoras relacionadas</h2>
      <ul class="space-y-2 text-sm">
{rel}
      </ul>
    </section>
  </main>

  {FOOTER}
  {BEACON}
{FLOATING}
</body>
</html>
"""
