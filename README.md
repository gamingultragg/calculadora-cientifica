# Calculadora Científica — www.calculadoracientifica.com.ar

Plataforma web gratuita de calculadoras especializadas para estudiantes, docentes,
ingenieros e investigadores de habla hispana. Este documento es la arquitectura
técnica de referencia del proyecto: estructura, diseño, SEO y estado de la
implementación.

---

## 1. Arquitectura del sitio

### 1.1 Stack elegido para el MVP

- **HTML5 semántico** + **Tailwind CSS (CDN Play)** + **JavaScript vanilla (ES2022, sin build step)**.
- Sin framework de frontend ni bundler: cada calculadora es una página independiente,
  indexable individualmente por Google, con su propio bundle JS pequeño y autocontenido.
- **Por qué no un SPA/framework en el MVP:** las calculadoras son herramientas
  transaccionales de alto volumen de búsqueda long-tail ("calculadora de matrices
  3x3", "resolver ecuación cuadrática online"). Cada una necesita ser una URL real,
  server-rendered desde el primer byte, sin esperar hidratación de JS para SEO y
  Core Web Vitals (LCP/INP). HTML estático + Tailwind CDN cumple esto con cero
  infraestructura.
- **Ruta de evolución recomendada (fase 2):** migrar a **Astro** (islands
  architecture) o **Next.js (App Router, SSG)** cuando el catálogo supere ~30
  calculadoras, para:
  - Reutilizar layout/header/footer como componentes (hoy están duplicados a mano
    en cada `index.html`, marcado con el comentario `<!-- SHARED: ... -->` para
    facilitar la extracción futura).
  - Compilar Tailwind (purge de CSS, sin el script CDN render-blocking).
  - Generar el `sitemap.xml` y los JSON-LD automáticamente desde
    `assets/js/calculators-data.js`, que ya funciona como fuente única de verdad
    (single source of truth) del catálogo.

### 1.2 Estructura de carpetas

```
calculadora-cientifica/
├── index.html                          # Dashboard / Home
├── robots.txt
├── sitemap.xml
├── README.md                           # Este documento
├── assets/
│   ├── css/
│   │   └── styles.css                  # Design tokens + componentes compartidos
│   ├── js/
│   │   ├── theme.js                    # Toggle modo oscuro/claro (persistente)
│   │   ├── calculators-data.js         # Catálogo (fuente única de verdad)
│   │   └── main.js                     # Buscador instantáneo + filtros del dashboard
│   └── img/                            # Iconografía, OG images, favicons
└── calculadoras/
    ├── matematicas-avanzadas/
    │   ├── calculadora-cientifica-online/index.html + script.js
    │   ├── ecuaciones-segundo-grado/index.html + script.js
    │   └── calculadora-matrices/index.html + script.js
    └── estadistica/
        └── calculadora-estadistica-descriptiva/index.html + script.js
```

**Categorías planificadas (carpetas ya reservadas en la IA de información, se
crean a medida que se suman calculadoras):**

| Categoría | Slug | Ejemplos futuros |
|---|---|---|
| Matemáticas Avanzadas | `/calculadoras/matematicas-avanzadas/` | derivadas, integrales, combinatoria, logaritmos |
| Estadística | `/calculadoras/estadistica/` | regresión lineal, distribución normal, intervalos de confianza |
| Física | `/calculadoras/fisica/` | cinemática, MRUA, ley de Ohm, caída libre |
| Química | `/calculadoras/quimica/` | estequiometría, pH, molaridad |
| Ingeniería | `/calculadoras/ingenieria/` | vigas, circuitos, conversor de unidades técnico |
| Finanzas | `/calculadoras/finanzas/` | interés compuesto, VAN/TIR, amortización de préstamos |

Cada categoría es tanto una ruta de navegación como una futura **landing page de
categoría** (`/calculadoras/estadistica/index.html`) que agrupará todas sus
calculadoras — clave para SEO de términos "categoría" de mayor volumen (ej.
"calculadoras de estadística online").

### 1.3 Convenciones de código

- Cada calculadora es **autocontenida**: su `script.js` vive junto a su
  `index.html` y no depende de imports de otras calculadoras (sí puede reusar
  `assets/js/theme.js`, que es puramente cosmético).
- Validación de inputs siempre en el cliente, con mensajes de error visuales
  (nunca `alert()` bloqueante) y `aria-live="polite"` para accesibilidad.
- Todo número que se muestra al usuario pasa por un formateador común
  (`Intl.NumberFormat('es-AR', ...)`) para coherencia (coma decimal, punto de miles).

---

## 2. Diseño visual

### 2.1 Paleta de colores

Definida como tokens CSS (`assets/css/styles.css`) y extendida en la config de
Tailwind de cada página, para que **modo claro y modo oscuro** compartan la
misma semántica.

| Token | Uso | Claro | Oscuro |
|---|---|---|---|
| `--color-primary` | Marca, CTA principal, enlaces | `#2563EB` (blue-600) | `#3B82F6` (blue-500) |
| `--color-primary-dark` | Hover/active de CTA | `#1D4ED8` | `#60A5FA` |
| `--color-accent` | Resultados correctos, éxito | `#10B981` (emerald-500) | `#34D399` |
| `--color-danger` | Errores de validación | `#E11D48` (rose-600) | `#FB7185` |
| `--color-warning` | Advertencias (ej. raíces complejas) | `#D97706` (amber-600) | `#FBBF24` |
| `--color-bg` | Fondo de página | `#F8FAFC` (slate-50) | `#0F172A` (slate-900) |
| `--color-surface` | Tarjetas, paneles | `#FFFFFF` | `#1E293B` (slate-800) |
| `--color-border` | Bordes, separadores | `#E2E8F0` (slate-200) | `#334155` (slate-700) |
| `--color-text` | Texto principal | `#0F172A` | `#F1F5F9` |
| `--color-text-muted` | Texto secundario | `#64748B` | `#94A3B8` |

**Color por categoría** (chips/badges en el dashboard, para escaneo visual rápido):
Matemáticas = `blue`, Estadística = `violet`, Física = `orange`, Química =
`green`, Ingeniería = `amber`, Finanzas = `teal`.

### 2.2 Tipografía

- **Interfaz y texto general:** [Inter](https://fonts.google.com/specimen/Inter)
  — alta legibilidad en pantalla, excelente soporte de números tabulares.
- **Pantallas/resultados de calculadoras:** [Roboto Mono](https://fonts.google.com/specimen/Roboto+Mono)
  — ancho fijo, evita que los dígitos "salten" al recalcular, sensación de
  calculadora física.
- Cargadas vía Google Fonts con `rel="preconnect"` + `font-display: swap` para
  no penalizar el LCP.

### 2.3 Estilo visual — "SaaS educativo"

- Layout con mucho aire (`padding`/`gap` generosos), tarjetas con `rounded-2xl`
  y sombra suave (`shadow-sm` → `shadow-md` en hover), sin bordes duros.
- Iconografía lineal minimalista (emoji-free en UI de producto; se usan solo
  como acento visual en el dashboard para escaneo rápido de categorías).
- Modo oscuro real (no solo "invertir colores"): superficies con jerarquía
  propia (`slate-900` → `slate-800` → `slate-700`), no un negro puro.
- Responsive **mobile-first**: en mobile las calculadoras usan un teclado
  numérico tipo grid de botones grandes (`min-h-12`, objetivo táctil ≥44px);
  en desktop se aprovecha el espacio con panel lateral de "Ayuda y fórmulas".
- Toggle de tema persistente en `localStorage`, respeta
  `prefers-color-scheme` en la primera visita.

---

## 3. Estrategia SEO técnico (.com.ar)

### 3.1 URLs

- Kebab-case, en español, descriptivas y con intención de búsqueda ("online",
  "gratis" cuando aplica de forma natural):
  - `www.calculadoracientifica.com.ar/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/`
  - `www.calculadoracientifica.com.ar/calculadoras/estadistica/calculadora-estadistica-descriptiva/`
  - `www.calculadoracientifica.com.ar/calculadoras/matematicas-avanzadas/ecuaciones-segundo-grado/`
  - `www.calculadoracientifica.com.ar/calculadoras/matematicas-avanzadas/calculadora-matrices/`
- Sin parámetros de query ni IDs numéricos. Sin barras finales inconsistentes
  (siempre con `/` final, configurar redirect 301 canónico en el hosting).

### 3.2 Metadatos on-page (por página)

Cada `index.html` de calculadora incluye:

- `<title>` con patrón: `{Nombre} Online Gratis | Calculadora Científica Argentina`
  (≤60 caracteres).
- `<meta name="description">` de ~150-155 caracteres con palabra clave +
  beneficio + CTA implícito ("con pasos detallados", "gratis y sin registro").
- `<link rel="canonical">` autorreferencial.
- `hreflang`: `es-AR` como principal, `es` como fallback genérico (preparado
  para expansión a otros países hispanohablantes sin canibalizar el ranking
  local .com.ar).
- Open Graph (`og:title`, `og:description`, `og:image`, `og:locale=es_AR`) y
  Twitter Card `summary_large_image`.

### 3.3 Datos estructurados (Schema.org / JSON-LD)

- **Homepage:** `WebSite` con `SearchAction` (sitelinks search box) +
  `Organization`.
- **Cada calculadora:** `SoftwareApplication` (`applicationCategory:
  "EducationalApplication"`, `operatingSystem: "Web"`, `offers.price: "0"`) +
  `BreadcrumbList` reflejando Home → Categoría → Calculadora.
- **Bloque "Ayuda y Fórmulas Teóricas":** marcado además como `FAQPage` cuando
  el contenido tiene formato pregunta/respuesta — capta featured snippets y
  refuerza el valor educativo ante Google (contenido único, no thin content).

### 3.4 Rendimiento y Core Web Vitals

- HTML estático servido directo (sin JS bloqueante crítico); Tailwind vía CDN
  en el MVP es un trade-off consciente de velocidad de desarrollo vs. peso —
  documentado como deuda técnica a resolver en la migración a Astro/Next
  (Tailwind compilado + purgado bajaría el CSS de ~formato CDN a unos pocos KB).
  Mientras tanto, no requiere ningún proceso de build.
- Scripts con `defer`, sin render-blocking salvo la fuente (mitigada con
  `preconnect` + `swap`).
- Imágenes (cuando se sumen: OG images, iconos de categoría) en formato WebP
  con `width`/`height` explícitos para evitar CLS.

### 3.5 Arquitectura de enlazado interno

- Dashboard → tarjetas de categoría → tarjetas de calculadora (máx. 3 clics
  desde home a cualquier herramienta).
- Cada calculadora muestra "Calculadoras relacionadas" (misma categoría) y
  breadcrumb visible (`Inicio / Categoría / Calculadora`) que además alimenta
  el `BreadcrumbList` schema.
- `sitemap.xml` versión inicial incluida en la raíz; `robots.txt` la referencia
  y permite rastreo total (`Allow: /`).

### 3.6 Roadmap de contenido SEO

1. Landing por categoría (agrupa long-tail de "calculadoras de X").
2. Blog/guías ("Cómo resolver una ecuación cuadrática paso a paso") enlazando
   a la calculadora correspondiente — top-of-funnel informacional que
   convierte a uso de herramienta.
3. Expansión de cada calculadora con ejemplos resueltos indexables (contenido
   único adicional, no duplicado entre herramientas).

---

## 4. Estado de la implementación (este entregable)

✅ Dashboard (`index.html`) con buscador instantáneo cliente-side y filtro por categoría.
✅ Landing page por categoría (`/calculadoras/<categoria>/`) para las 6 categorías, alimentadas por
   `assets/js/category.js` + `calculators-data.js` (fuente única de verdad del catálogo).
✅ Calculadora Científica Avanzada (Matemáticas Avanzadas).
✅ Calculadora de Ecuaciones de Segundo Grado, con raíces complejas (Matemáticas Avanzadas).
✅ Calculadora de Matrices 2×2 y 3×3 (Matemáticas Avanzadas).
✅ Calculadora de Estadística Descriptiva (Estadística).
✅ Calculadora de Cinemática — MRU y MRUA (Física).
✅ Calculadora de pH y pOH (Química).
✅ Conversor de Unidades Técnicas — longitud, masa, presión, caudal, torque (Ingeniería).
✅ Calculadora de Interés Compuesto, con aportes periódicos (Finanzas).
✅ `robots.txt` + `sitemap.xml` con las 8 calculadoras y las 6 categorías.

**Cobertura de categorías:** las 6 categorías del dashboard ya tienen al menos una calculadora
en producción y su propia landing page indexable.

✅ Identidad visual: favicon (`favicon.svg` + PNG de respaldo 16/32px), `apple-touch-icon.png` y
   una imagen Open Graph (`og-image.png`, 1200×630) generados con `scripts/generate-images.py`
   (Pillow) e inyectados en las 15 páginas del sitio — así las 4 tarjetas al compartir en
   WhatsApp/redes muestran marca en vez de un enlace pelado.
✅ Primera pieza de contenido del roadmap SEO (sección 3.6): `/guias/` (índice) y
   `/guias/como-resolver-ecuaciones-de-segundo-grado/`, con `Article` + `HowTo` + `BreadcrumbList`
   en JSON-LD, enlazada desde el nav global y desde la calculadora de ecuaciones.

**Cómo regenerar las imágenes de marca** si cambia la paleta o el logo:

```bash
python scripts/generate-images.py
```

✅ Segunda calculadora en cada una de las 5 categorías que tenían solo una, para reforzar sus
   landing pages: **Permutaciones y Combinaciones** (Estadística), **Ley de Ohm** (Física),
   **Calculadora de Molaridad** (Química), **Resistencias en Serie y Paralelo** (Ingeniería) y
   **Amortización de Préstamos** — sistema francés (Finanzas). Las cinco están enlazadas entre sí
   como "calculadoras relacionadas" con su categoría vecina (ej. Ley de Ohm ↔ Resistencias).

**Catálogo actual: 13 calculadoras** en las 6 categorías (dashboard muestra "13 resultados").

✅ 6 guías nuevas, una por categoría (además de la de ecuaciones cuadráticas ya existente),
   cada una con `Article` + `BreadcrumbList` (y `HowTo` donde aplica) en JSON-LD, enlazada desde
   `/guias/` y con un cross-link "¿Querés entender el por qué?" en su calculadora correspondiente:
   - Matemáticas Avanzadas: `/guias/determinante-y-matriz-inversa/`
   - Estadística: `/guias/como-calcular-desviacion-estandar/`
   - Física: `/guias/ley-de-ohm-explicada/`
   - Química: `/guias/como-calcular-ph-y-poh/`
   - Ingeniería: `/guias/resistencias-serie-vs-paralelo/`
   - Finanzas: `/guias/interes-simple-vs-compuesto/`

✅ **Cobertura de guías al 100%**: se agregó una segunda tanda de 6 guías (una por categoría),
   completando así una guía por cada una de las 13 calculadoras del catálogo:
   - Matemáticas Avanzadas: `/guias/grados-y-radianes/`
   - Estadística: `/guias/permutaciones-vs-combinaciones/`
   - Física: `/guias/formulas-de-mru-y-mrua/`
   - Química: `/guias/como-calcular-molaridad/`
   - Ingeniería: `/guias/conversion-de-unidades-de-presion/`
   - Finanzas: `/guias/como-calcular-cuota-de-prestamo/`

**Catálogo de contenido actual: 13 calculadoras + 13 guías + 6 landing pages de categoría + home
= 33 páginas indexables**, todas en `sitemap.xml`, cada calculadora con su guía companion
enlazada en ambas direcciones.

✅ **Auditoría de integridad** (`scripts/audit-links.py`, no destructiva, para correr después de
   cualquier tanda grande de páginas): recorre las 34 páginas y verifica enlaces internos rotos,
   `<title>`/meta description duplicados y presencia de favicon/OG en todas. Resultado actual:
   **0 problemas encontrados** en las 34 páginas.
✅ [404.html](404.html) — página de error personalizada que reutiliza el buscador y el filtro por
   categoría del dashboard (mismo `calculators-data.js` / `main.js`, cero código nuevo de
   búsqueda), para que un enlace roto no sea un callejón sin salida. Nota de despliegue: para que
   el hosting la sirva automáticamente en rutas inexistentes hay que configurarlo según la
   plataforma (Netlify/Vercel/GitHub Pages la detectan por convención de nombre; Apache necesita
   `ErrorDocument 404 /404.html`; Nginx necesita `error_page 404 /404.html`).

✅ **Tercera calculadora en las 5 categorías que tenían solo dos**, para emparejarlas con
   Matemáticas Avanzadas: **Distribución Normal / Puntaje Z** (Estadística), **Segunda Ley de
   Newton** (Física), **Calculadora de Diluciones** (Química), **Ley de Hooke** (Ingeniería) y
   **Calculadora de Porcentajes** (Finanzas).

✅ **Cobertura de guías al 100% otra vez**: guía companion para las 5 calculadoras más nuevas —
   `/guias/puntaje-z-y-curva-normal/`, `/guias/segunda-ley-de-newton-explicada/`,
   `/guias/como-hacer-una-dilucion/`, `/guias/ley-de-hooke-y-elasticidad/` y
   `/guias/como-calcular-porcentajes/`. Las 18 calculadoras del catálogo tienen su guía.

✅ **Páginas legales**: `/privacidad/` y `/terminos-de-uso/` — sin recolección de datos personales,
   `localStorage` solo para el tema claro/oscuro, exención de responsabilidad sobre los resultados
   de las calculadoras (uso educativo/referencial, verificar antes de decisiones importantes) y
   propiedad del contenido. Enlazadas desde el footer de las 46 páginas del sitio
   (`scripts/inject-legal-links.py`, idempotente, mismo patrón que el de favicons).

✅ **Calculadora Básica** (`/calculadoras/matematicas-avanzadas/calculadora-basica/`): 4 operaciones
   + porcentaje, con evaluación **secuencial** (como una calculadora de bolsillo real —
   `2+3×4` da `20`, no `14`), a diferencia de la científica que sí respeta la prioridad de
   operaciones. Lógica de evaluación secuencial validada con 5 casos en Node antes de implementar
   (orden de operaciones, división encadenada, cambio de operador a mitad de cuenta, división por
   cero, decimales) y confirmada en el navegador. Al principio se agregó también al catálogo
   data-driven (`calculators-data.js`), pero quedaba duplicada en la home (banner destacado +
   tarjeta repetida más abajo), así que se sacó de ahí a pedido del usuario — la página sigue viva
   y en el sitemap, solo dejó de listarse en la grilla/buscador y en la categoría Matemáticas;
   se accede por el banner destacado o por URL directa.

**Catálogo actual (2026-11-10): 35 calculadoras + 35 guías + 6 landing
pages de categoría + home + 404 + sobre-nosotros + 2 legales = 83 páginas**, todas en `sitemap.xml`
(excepto la 404, que lleva `noindex`), auditoría en 0 problemas.

✅ **Validación de JSON-LD** (`scripts/validate-jsonld.py`, no destructiva): parsea los 44 bloques
   `<script type="application/ld+json">` del sitio y verifica que sean JSON sintácticamente válido,
   que tengan forma correcta (`@context`, `@type`/`@graph`), y que toda URL propia referenciada
   adentro (breadcrumbs, `mainEntityOfPage`) resuelva a una página real. Resultado actual:
   **44/44 bloques válidos, 0 problemas** — protege los rich snippets de Google de errores de
   sintaxis invisibles a simple vista.

✅ **Accesibilidad — contraste WCAG y navegación por teclado**:
   - `scripts/check-contrast.py` calculó el contraste de la paleta en ambos temas contra AA (4.5:1).
     Encontró un problema real: el color primario usado como texto de enlace sobre tarjetas en modo
     oscuro daba 3,98:1 (por debajo del mínimo). Se separó en dos tokens —
     `--color-primary` (fondos de botones, se queda igual) y `--color-primary-link` (texto/enlaces,
     más claro en modo oscuro: `#60a5fa`) — vía `scripts/fix-link-contrast.py`, que redirigió los
     420 usos de `text-[var(--color-primary)]` en las 47 páginas sin tocar los 49 usos de fondo de
     botón ni los 43 anillos de foco. Resultado: **todos los pares texto/fondo pasan AA en ambos
     temas** (el peor caso pasó de 3,98:1 a 5,75:1).
   - `scripts/inject-skip-link.py` agregó un enlace "Saltar al contenido" (oculto hasta recibir foco
     por teclado) en las 47 páginas, para no forzar a usuarios de teclado/lectores de pantalla a
     tabular por todo el header en cada página.

✅ **Bug real de parseo numérico corregido en las 17 calculadoras con inputs de texto**: el código
   original solo convertía la coma decimal (`.replace(",", ".")`), sin contemplar el punto de miles
   del formato es-AR. Consecuencia real: escribir `"15.000"` (quince mil) se interpretaba
   silenciosamente como `15` — sin ningún error, un resultado 1000 veces menor sin ninguna señal de
   que algo estaba mal. `"1.234,56"` directamente daba `NaN`. Se reemplazó por
   `normalizeNumberInput()` (validado con 12 casos de borde antes de aplicarlo: miles, miles+decimal,
   decimal con coma, decimal con punto tipo "9.8"/"3.14" sin romperse, negativos, múltiples grupos de
   miles) vía `scripts/fix-number-parsing.py`, que tocó los 19 puntos de parseo en 17 archivos.
   Verificado en vivo: `"15.000"` en Interés Compuesto ahora da el resultado correcto
   ($16.902,38 al 12% anual sobre $15.000, antes hubiera calculado sobre "$15").

✅ **Revisión de seguridad (XSS)**: se auditaron los ~40 usos de `innerHTML` en las 18
   calculadoras. Todos interpolan exclusivamente números ya validados y formateados (`fmt()`) o
   strings fijos del código fuente (etiquetas de campos); ninguno inserta texto crudo tipeado por
   el usuario. Los mensajes de error que citan el input inválido (ej. `"${input.value}" no es un
   número válido`) usan `textContent` en los 18 archivos sin excepción, nunca `innerHTML` — así que
   no ejecutan HTML/JS aunque alguien escriba algo como `<script>` en un campo numérico.
   **Resultado: 0 vectores XSS encontrados.**

✅ **Validación de `sitemap.xml`** (`scripts/validate-sitemap.py`, no destructiva): confirma que el
   archivo sea XML bien formado y que coincida 1:1 con las páginas reales del sitio — sin URLs
   duplicadas, sin entradas que apunten a páginas que ya no existen, y sin páginas indexables que
   falten. Necesario porque el sitemap se fue editando a mano en ~10 tandas distintas a lo largo del
   proyecto; resultado actual: **46 URLs, 0 problemas**, servido en producción con
   `content-type: application/xml`.

## Pendientes

Actualizado 2026-11-10.

**Esperando a terceros**
- [ ] **AdSense: esperar que el sitio pase de "Preparando" a "Listo"** (AdSense > Sitios; llega
  un email). La cuenta ya está completa (datos de pago cargados, sitio conectado, anuncios
  automáticos desactivados, 4 unidades creadas). Cuando diga "Listo": poner `ENABLED = true` en
  `assets/js/ads.js`, commitear y verificar en producción que los anuncios aparezcan donde
  corresponde y sin saltos de layout. Ver "Ubicaciones de anuncios".
- [ ] **Search Console: indexación.** 9 páginas indexadas y 42 "Descubierta, sin indexar". La
  tarea programada `indexacion-search-console` (diaria, 10:14) pide ~8 URLs por día desde
  `indexacion-cola.md` (archivo local, no versionado). Revisar el avance en Indexación > Páginas.

**Por hacer (en orden de prioridad)**
- [x] ~~Calculadoras nuevas con su guía (masa molar, promedio de notas, regla de tres, interés
  simple, MCD y MCM)~~ — hechas 2026-11-10 (24 calculadoras, 24 guías).
- [x] ~~Mejoras de producto: PWA instalable y offline, botón "copiar resultado", historial local
  y teclado físico en la científica~~ — hechas 2026-11-10 (ver "PWA y offline" y "Copiar
  resultado e historial").
- [x] ~~Enviar mails como `contacto@calculadoracientifica.com.ar` desde Gmail~~ — hecho 2026-11-10
  (alias verificado con SMTP de Gmail y contraseña de aplicación; responde desde la misma dirección).
- [ ] **Plan de difusión** (artifact "Plan de Difusión"): grupos de docentes, foros de dudas,
  Reddit con cuidado, directorios, un video del "orden de operaciones".
- [ ] **Performance:** Lighthouse mobile quedó en 74 por los scripts de Google (~380 KiB). Si
  molesta, cargar `adsbygoogle.js` de forma diferida en lugar de en el `<head>`.

## Deploy

El sitio está en producción en **Cloudflare Pages**, conectado al repo de GitHub
(`gamingultragg/calculadora-cientifica`, rama `main`). Cada `git push` a `main` dispara un
redeploy automático — no hay build command, se sirve la raíz del repo tal cual. Dominio propio
(`calculadoracientifica.com.ar`, registrado en NIC Argentina) **conectado y activo**, con SSL en
ambos hosts (`calculadoracientifica.com.ar` y `www.calculadoracientifica.com.ar`). El subdominio
`calculadora-cientifica.pages.dev` redirige con 301 al dominio definitivo vía
`functions/_middleware.js` (Pages Function), necesario para que Search Console aceptara el "Cambio
de dirección". Google Search Console: propiedad `www.calculadoracientifica.com.ar` verificada,
sitemap enviado (0 errores), Change of Address confirmado.

Cloudflare Web Analytics activo (beacon cookieless). Sin Google Analytics ni ningún otro tracker.

### Auditoría Lighthouse (PageSpeed Insights, mobile, 4G simulado)

Performance 84 · Accessibility 100 · Best Practices 100 · SEO 100 · Agentic Browsing 2/2.

El cuello de botella de Performance es conocido y ya documentado más abajo: Tailwind Play CDN
genera el CSS en el navegador en tiempo de ejecución, lo cual bloquea el render (~1.700ms
estimados) — es el mismo trade-off de la migración a framework con build pendiente. TBT 0ms y CLS 0
son excelentes; no hay bloqueo de interactividad ni saltos de layout.

Un hallazgo real de esta auditoría: el banner destacado de Calculadora Básica en el home no
llegaba a 4.5:1 de contraste (texto blanco sobre `blue-600`, con o sin opacidad reducida, topeaba
en 3.68:1 — insuficiente incluso en blanco sólido). Se corrigió pasando el fondo a `blue-800` y el
subtítulo a `blue-100` opaco (en vez de `text-white/85` translúcido, para no depender del
compositing de alpha en el muestreo de píxeles de Lighthouse). Accessibility pasó de 95 a 100.

### Ubicaciones de anuncios (AdSense)

El script de AdSense (`ca-pub-7274131858034505`) está en el `<head>` de todas las páginas y
`ads.txt` en la raíz. Las ubicaciones propias están preparadas pero **apagadas**: contenedores
`<aside class="cc-ad" data-ad="...">` (47 páginas, colocados con `scripts/inject-ad-slots.py`) que
nacen ocultos y sin ocupar espacio, y `assets/js/ads.js`, que solo muestra uno cuando su tipo tiene
un ID de unidad en `SLOTS`.

| Tipo | Dónde | Reserva |
|---|---|---|
| `calc` | calculadoras: columna derecha, debajo de la ayuda (en mobile, al final, lejos del teclado) | 280 px |
| `guide` | guías: al final del artículo, antes de "relacionadas" | 280 px |
| `home` | home: entre la grilla de calculadoras y las guías | 250 px |
| `cat` | categorías: debajo de la grilla | 250 px |

Sin anuncios en páginas legales, "Sobre nosotros", 404 ni el índice de guías. El anuncio se pide
con carga diferida (400 px antes de entrar en pantalla) y, si AdSense no lo llena
(`data-ad-status="unfilled"`), el contenedor se oculta solo.

**Estado (2026-11-10):** las 4 unidades display (adaptables) ya están creadas en AdSense
(`calculadoras` 8844192446, `guias` 4200359527, `home` 5593332249, `categorias` 4144519200) y sus IDs
cargados en `SLOTS`, pero `ENABLED = false` en `ads.js`. Los anuncios automáticos ya estaban
DESACTIVADOS en AdSense. **Para encenderlos:** cuando AdSense > Sitios muestre el sitio como
"Listo" (hoy "Preparando"; pendientes de la cuenta: datos de pago/identidad y que Google vuelva a
revisar `ads.txt`, que está bien servido en ambos dominios), poner `ENABLED = true` y commitear.
Encenderlos antes solo mostraría el espacio un instante y lo ocultaría.

### CSS compilado (sin Tailwind CDN)

Desde 2026-11-10 el sitio **ya no carga el Tailwind Play CDN**: el CSS se compila a
`assets/css/tailwind.css` (~20 KB minificado, contra ~400 KB de JS que el CDN descargaba y
ejecutaba en cada visita) y se enlaza después de `styles.css` (mismo orden de cascada que tenía el
CDN). Sigue siendo HTML estático, sin build en Cloudflare: el CSS compilado se commitea.

**Cada vez que se usen clases de Tailwind nuevas (en HTML o en JS), recompilar y commitear:**

```bash
cd tools/tailwind && npm install && npm run build
```

La herramienta vive en `tools/tailwind/` (Tailwind 3.4.17, `tailwind.config.js` con las rutas a
escanear) y no en la raíz a propósito: un `package.json` en la raíz haría que Cloudflare Pages
intente instalar dependencias en cada deploy. Páginas nuevas: copiar el `<head>` de una existente
(ya trae el `<link>` a `tailwind.css`). `scripts/replace-tailwind-cdn.py` fue la migración única.

Verificación de la migración: se compararon las propiedades CSS calculadas de **todos** los
elementos de las 52 páginas, versión con CDN contra versión compilada, en modo claro y oscuro
(~11.000 elementos): 0 diferencias (se excluyeron los nodos que inyecta AdSense, que descalibran
una comparación elemento por elemento).

### Tarjetas pre-renderizadas (enlaces estáticos para Google)

Las grillas de calculadoras de la home y de las 6 categorías se dibujan con JS desde
`calculators-data.js`, pero además se **pre-renderizan en el HTML** con
`scripts/prerender-cards.py` (entre los marcadores `CC-PRERENDER`), para que Google vea los
enlaces sin ejecutar JS (en Search Console había 42 páginas "descubiertas, sin indexar" y la home
tenía un solo enlace estático a una calculadora). **Cada vez que se agregue o cambie una
calculadora en `calculators-data.js`, correr `python scripts/prerender-cards.py`** y commitear.
El script es idempotente y el JS redibuja las mismas tarjetas, así que no hay salto visual.

### Sobre la migración a framework con build

Evalué lanzar la migración a Astro/Next en esta iteración (fase 2 de la sección 1.1) y decidí
posponerla: es un cambio de arquitectura real (agrega Node/npm como dependencia de build, cambia
el modelo de despliegue de "subís la carpeta tal cual" a "corré un build y subís `dist/`") con
riesgo no trivial de introducir regresiones al reescribir 35 páginas ya verificadas una por una —
no es una extensión incremental como las anteriores. Sigue siendo la deuda técnica real del
proyecto a este tamaño, pero es una decisión que vale la pena tomar mirando el resultado (¿el sitio
va a seguir creciendo? ¿dónde se va a hospedar?) en vez de ejecutarla de una sola pasada sin
supervisión. Mientras tanto, la auditoría de integridad de este punto cumple un rol similar de red
de seguridad con costo y riesgo mucho menores.

## PWA y offline

- `manifest.webmanifest` + íconos `assets/img/pwa-*.png` (`scripts/generate-pwa-icons.py`).
- `sw.js` se **genera** con `python scripts/build-sw.py` desde `scripts/sw-template.js`: precarga
  todas las páginas del sitemap + CSS/JS/íconos (≈100 archivos) y usa red-primero con respaldo en
  caché. La versión es un hash del contenido, así que cada cambio publica un SW nuevo.
  **Correr `build-sw.py` siempre al final, antes de commitear.**
- `assets/js/pwa.js` registra el SW y muestra "Instalar app" en el pie cuando el navegador lo ofrece.
- `scripts/inject-pwa-and-copy.py` (idempotente) agrega manifest, `theme-color`, `pwa.js` y
  `copy-result.js` a todas las páginas; `page_templates.py` ya incluye manifest y `pwa.js`.

## Copiar resultado e historial

- `assets/js/copy-result.js`: botón bajo cada panel `*-result-panel` (visible solo con resultado) y
  botones `data-copy-target="<id>"` (científica y básica). Páginas nuevas con panel de resultado:
  correr `inject-pwa-and-copy.py`.
- Científica: historial en `localStorage` (`cc-sci-history`, 30 cálculos; click en la cuenta la
  recarga, click en el resultado lo inserta), teclado físico con coma decimal, atajos de letras
  (s c t l n r p e a) y sin pisar Ctrl+C/Ctrl+R. Tras `=`, un número nuevo empieza de cero y un
  operador sigue con el resultado.

## Lote 3 (2026-11-10)

Fracciones, Teorema de Pitágoras, Conversor de bases numéricas, Aguinaldo (SAC) y Gases ideales,
cada una con su guía. Se generaron con `scripts/build-batch-3.py` y `build-batch-3-guides.py` y se
registraron con `scripts/register-batch-3.py`. Orden para sumar un lote nuevo: generadores →
`register-batch-N.py` → `prerender-cards.py` → `inject-pwa-and-copy.py` → `cd tools/tailwind && npm run build`
→ `build-sw.py` → QA (`audit-links`, `validate-jsonld`, `validate-sitemap`, `check-contrast`).

## Lote 4 (2026-11-10) y mejoras de producto

- **Lote 4, elegido con las consultas reales de Search Console:** moles (la gente busca "moles de soluto"),
  plazo fijo con TNA/TEA, áreas y volúmenes, energía cinética y potencial, regresión lineal y conversor
  de temperatura, cada una con su guía (`build-batch-4.py`, `build-batch-4-guides.py`, `register-batch-4.py`).
- **Tabla de amortización** (cuota por cuota) en la calculadora de préstamos, y título/descripción
  orientados a "sistema francés" (consultas: cálculo de cuota sistema francés, etc.).
- **Enlace compartible:** el botón "Copiar enlace" de cada calculadora genera una URL con los valores
  (`?is-capital=100000&is-tasa=24…`); al abrirla se completan los campos y se calcula solo
  (`applyQueryParams` en `assets/js/copy-result.js`; usa los `id` de los campos, así que los `id` no se pueden renombrar a la ligera).
- **Imprimir / PDF:** botón "Imprimir" y estilos `@media print` en `styles.css`.
- **Pruebas automáticas de la lógica:** `node --test tools/tests/logic.test.js` (16 pruebas; correrlas antes de commitear
  cambios a un `script.js`). Al sumar una calculadora nueva, exportar la lógica con `module.exports` y agregar su prueba.
- **AdSense y velocidad:** el `<script async>` de AdSense se dejó estático a propósito mientras el sitio está en revisión
  (Google necesita verlo en el HTML). Cuando esté aprobado se puede diferir su carga para recuperar puntaje de Lighthouse.
