"""
build-contacto.py — Genera /contacto/index.html a partir del molde de /sobre-nosotros/ (mismo head, header, footer y scripts),
cambiando metadatos, JSON-LD (ContactPage), migas de pan y contenido. Generación de una sola vez: después, el HTML es la fuente de verdad.
Luego correr scripts/inject-contact-link.py (enlace "Contacto" en todos los pies) y registrar la URL en sitemap.xml.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.calculadoracientifica.com.ar"
LINK = 'class="text-[var(--color-primary-link)] hover:underline"'
H2 = 'class="font-display font-bold text-xl mt-8 mb-2"'
P = 'class="text-[var(--color-text-muted)] leading-relaxed"'
UL = 'class="list-disc list-inside mt-2 space-y-1 text-[var(--color-text-muted)] leading-relaxed"'
STRONG = 'class="text-[var(--color-text)]"'
MAIL = "contacto@calculadoracientifica.com.ar"

s = (ROOT / "sobre-nosotros" / "index.html").read_text(encoding="utf-8")


def sub(pattern, repl, text, flags=0):
    new, n = re.subn(pattern, lambda _m: repl, text, count=1, flags=flags)
    assert n == 1, pattern
    return new


URL = f"{BASE}/contacto/"
TITLE = "Contacto | Calculadora Científica"
DESC = "Cómo comunicarte con Calculadora Científica: reportar un error en una calculadora, sugerir herramientas nuevas, consultas sobre tu cuenta y pedidos sobre tus datos personales."

s = sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", s)
s = sub(r'<meta name="description" content="[^"]*" />', f'<meta name="description" content="{DESC}" />', s)
s = sub(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{URL}" />', s)
s = sub(r'<link rel="alternate" hreflang="es-AR" href="[^"]*" />', f'<link rel="alternate" hreflang="es-AR" href="{URL}" />', s)
s = sub(r'<link rel="alternate" hreflang="es" href="[^"]*" />', f'<link rel="alternate" hreflang="es" href="{URL}" />', s)
s = sub(r'<meta property="og:title" content="[^"]*" />', '<meta property="og:title" content="Contacto" />', s)
s = sub(r'<meta property="og:description" content="[^"]*" />', '<meta property="og:description" content="Escribinos para reportar un error, sugerir una calculadora o hacer una consulta." />', s)
s = sub(r'<meta property="og:url" content="[^"]*" />', f'<meta property="og:url" content="{URL}" />', s)

jsonld = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "ContactPage",
      "name": "Contacto",
      "url": "{URL}",
      "description": "{DESC}",
      "inLanguage": "es-AR",
      "mainEntity": {{
        "@type": "Organization",
        "name": "Calculadora Científica",
        "url": "{BASE}/",
        "email": "{MAIL}",
        "contactPoint": {{
          "@type": "ContactPoint",
          "contactType": "customer support",
          "email": "{MAIL}",
          "availableLanguage": "es",
          "areaServed": "AR"
        }}
      }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Inicio", "item": "{BASE}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Contacto", "item": "{URL}" }}
      ]
    }}
  ]
}}
</script>"""
s = sub(r'<script type="application/ld\+json">.*?</script>', jsonld, s, re.S)
s = sub(r'(<li class="text-\[var\(--color-text\)\] font-medium" aria-current="page">)Sobre Nosotros(</li>)', r"\g<1>Contacto\g<2>".replace("\\g<1>", "<li class=\"text-[var(--color-text)] font-medium\" aria-current=\"page\">").replace("\\g<2>", "</li>"), s)

article = f"""<article>
      <h1 class="font-display font-extrabold text-2xl sm:text-3xl">Contacto</h1>
      <p class="mt-3 {P[7:-1]}">
        Si encontraste un error, te falta una calculadora o tenés una consulta, escribinos. Leemos todos los mensajes y
        los reportes de errores son los que más valoramos.
      </p>
      <p class="mt-5">
        <a href="mailto:{MAIL}" class="calc-btn calc-btn--op inline-block max-w-full px-4 py-3 font-semibold text-sm sm:text-base break-all">✉ {MAIL}</a>
      </p>

      <h2 {H2}>Cómo reportar un error en una calculadora</h2>
      <p {P}>Para que podamos reproducirlo y corregirlo rápido, contanos:</p>
      <ul {UL}>
        <li>La dirección (URL) de la calculadora donde pasó.</li>
        <li>Los valores que ingresaste y el resultado que obtuviste.</li>
        <li>El resultado que esperabas y de dónde lo sacaste (un libro, un apunte u otra calculadora).</li>
        <li>El dispositivo y el navegador, si el problema parece de pantalla o de funcionamiento.</li>
      </ul>

      <h2 {H2}>Para qué más podés escribirnos</h2>
      <ul {UL}>
        <li><strong {STRONG}>Sugerencias:</strong> calculadoras o guías que te gustaría ver en el sitio.</li>
        <li><strong {STRONG}>Tu cuenta:</strong> ayuda para ingresar, recuperar la contraseña o eliminarla (también podés hacerlo vos desde
          <a {LINK} href="/cuenta/">Mi cuenta</a>).</li>
        <li><strong {STRONG}>Tus datos personales:</strong> acceso, rectificación o supresión, según la
          <a {LINK} href="/privacidad/">Política de Privacidad</a>.</li>
        <li><strong {STRONG}>Publicidad, prensa o colaboraciones:</strong> propuestas de contenido, difusión en cátedras o instituciones.</li>
        <li><strong {STRONG}>Contenido inadecuado:</strong> si viste un anuncio que no corresponde, avisanos con la página donde apareció.</li>
      </ul>

      <h2 {H2}>Cuánto tardamos en responder</h2>
      <p {P}>
        Respondemos en general dentro de los 2 a 5 días hábiles. Los pedidos de acceso, rectificación o supresión de datos personales
        se contestan en los plazos que indica la <a {LINK} href="/privacidad/">Política de Privacidad</a> (10 días corridos para el acceso y
        5 días hábiles para rectificar o suprimir).
      </p>

      <h2 {H2}>Qué no podemos hacer</h2>
      <ul {UL}>
        <li>Resolver tareas o ejercicios completos: el objetivo del sitio es que entiendas el procedimiento, y cada guía trae ejemplos resueltos.</li>
        <li>Dar asesoramiento profesional: los resultados son de referencia y no reemplazan la opinión de un profesional médico, legal, financiero o de ingeniería
          (ver los <a {LINK} href="/terminos-de-uso/">Términos de Uso</a>).</li>
      </ul>

      <h2 {H2}>Quién está detrás</h2>
      <p {P}>
        Calculadora Científica es un proyecto independiente, hecho en Argentina, a cargo de Santiago Rios Centeno. Conocé más en
        <a {LINK} href="/sobre-nosotros/">Sobre Nosotros</a>.
      </p>
    </article>"""
s = sub(r"<article>.*?</article>", article, s, re.S)
(ROOT / "contacto").mkdir(exist_ok=True)
(ROOT / "contacto" / "index.html").write_text(s, encoding="utf-8")
print("escrito: contacto/index.html")
