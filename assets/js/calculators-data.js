/**
 * calculators-data.js — Catálogo de calculadoras (fuente única de verdad).
 *
 * Usado por el dashboard (assets/js/main.js) para el buscador instantáneo y
 * el render de tarjetas. En la migración a un framework con build (ver
 * README §1.1) este mismo archivo pasa a alimentar además la generación
 * automática de sitemap.xml y JSON-LD.
 */
const CC_CATEGORIES = {
  matematicas: {
    label: "Matemáticas Avanzadas",
    color: "blue",
    slug: "matematicas-avanzadas",
    description:
      "Calculadora científica, ecuaciones de segundo grado y álgebra de matrices, con desarrollo paso a paso.",
  },
  estadistica: {
    label: "Estadística",
    color: "violet",
    slug: "estadistica",
    description:
      "Estadística descriptiva y herramientas de análisis de datos para cátedras, tesis e informes.",
  },
  fisica: {
    label: "Física",
    color: "orange",
    slug: "fisica",
    description:
      "Cinemática, movimiento rectilíneo uniforme y uniformemente acelerado, con fórmulas explicadas.",
  },
  quimica: {
    label: "Química",
    color: "green",
    slug: "quimica",
    description: "pH, pOH y concentración de iones para química general y analítica.",
  },
  ingenieria: {
    label: "Ingeniería",
    color: "amber",
    slug: "ingenieria",
    description: "Conversión de unidades técnicas: longitud, masa, presión, caudal y torque.",
  },
  finanzas: {
    label: "Finanzas",
    color: "teal",
    slug: "finanzas",
    description: "Interés compuesto, capitalización y proyección de ahorros e inversiones.",
  },
};

const CC_CALCULATORS = [
  {
    id: "calculadora-basica",
    title: "Calculadora Básica Online",
    description: "Sumar, restar, multiplicar, dividir y porcentajes, simple y rápida.",
    category: "matematicas",
    keywords: ["basica", "simple", "sumar", "restar", "multiplicar", "dividir", "porcentaje"],
    url: "/calculadoras/matematicas-avanzadas/calculadora-basica/",
    status: "live",
  },
  {
    id: "calculadora-cientifica",
    title: "Calculadora Científica Online",
    description:
      "Trigonometría, logaritmos, exponenciales, factoriales, paréntesis y memoria (M+, M-, MR).",
    category: "matematicas",
    keywords: ["cientifica", "trigonometria", "seno", "coseno", "logaritmo", "factorial", "memoria"],
    url: "/calculadoras/matematicas-avanzadas/calculadora-cientifica-online/",
    status: "live",
  },
  {
    id: "ecuaciones-segundo-grado",
    title: "Ecuaciones de Segundo Grado",
    description:
      "Fórmula cuadrática con desarrollo paso a paso. Raíces reales y complejas.",
    category: "matematicas",
    keywords: ["cuadratica", "bhaskara", "raices", "discriminante", "polinomio"],
    url: "/calculadoras/matematicas-avanzadas/ecuaciones-segundo-grado/",
    status: "live",
  },
  {
    id: "calculadora-matrices",
    title: "Calculadora de Matrices 2×2 y 3×3",
    description:
      "Determinante, matriz inversa, transpuesta y multiplicación de matrices.",
    category: "matematicas",
    keywords: ["matrices", "determinante", "inversa", "transpuesta", "algebra lineal"],
    url: "/calculadoras/matematicas-avanzadas/calculadora-matrices/",
    status: "live",
  },
  {
    id: "estadistica-descriptiva",
    title: "Estadística Descriptiva",
    description:
      "Media, mediana, moda, desviación estándar, varianza y rango a partir de tus datos.",
    category: "estadistica",
    keywords: ["media", "mediana", "moda", "desviacion estandar", "varianza", "rango"],
    url: "/calculadoras/estadistica/calculadora-estadistica-descriptiva/",
    status: "live",
  },
  {
    id: "cinematica",
    title: "Cinemática (MRU / MRUA)",
    description: "Velocidad, aceleración, tiempo y distancia en movimiento rectilíneo.",
    category: "fisica",
    keywords: ["velocidad", "aceleracion", "mru", "mrua", "cinematica", "distancia", "tiempo"],
    url: "/calculadoras/fisica/cinematica-mru-mrua/",
    status: "live",
  },
  {
    id: "calculadora-ph",
    title: "Calculadora de pH y pOH",
    description: "pH, pOH y concentración de iones H⁺ / OH⁻ a partir de la molaridad.",
    category: "quimica",
    keywords: ["ph", "poh", "acido", "base", "concentracion", "iones", "molaridad"],
    url: "/calculadoras/quimica/calculadora-de-ph/",
    status: "live",
  },
  {
    id: "interes-compuesto",
    title: "Interés Compuesto",
    description: "Capitalización, aportes periódicos y proyección de ahorro o inversión.",
    category: "finanzas",
    keywords: ["interes", "capitalizacion", "ahorro", "tasa", "inversion", "compuesto"],
    url: "/calculadoras/finanzas/interes-compuesto/",
    status: "live",
  },
  {
    id: "conversor-unidades-ingenieria",
    title: "Conversor de Unidades Técnicas",
    description: "Longitud, masa, presión, caudal y torque, con conversión instantánea.",
    category: "ingenieria",
    keywords: ["unidades", "presion", "torque", "caudal", "conversor", "longitud", "masa"],
    url: "/calculadoras/ingenieria/conversor-de-unidades/",
    status: "live",
  },
  {
    id: "distribucion-normal",
    title: "Distribución Normal (Puntaje Z)",
    description: "Puntaje Z y probabilidad acumulada a partir de un valor, la media y el desvío estándar.",
    category: "estadistica",
    keywords: ["distribucion normal", "puntaje z", "z-score", "probabilidad", "campana de gauss"],
    url: "/calculadoras/estadistica/distribucion-normal/",
    status: "live",
  },
  {
    id: "segunda-ley-de-newton",
    title: "Segunda Ley de Newton",
    description: "Fuerza, masa o aceleración a partir de los otros dos valores (F = m·a).",
    category: "fisica",
    keywords: ["newton", "fuerza", "masa", "aceleracion", "dinamica", "f=ma"],
    url: "/calculadoras/fisica/segunda-ley-de-newton/",
    status: "live",
  },
  {
    id: "calculadora-diluciones",
    title: "Calculadora de Diluciones",
    description: "Concentración o volumen final de una dilución, con la fórmula C₁V₁ = C₂V₂.",
    category: "quimica",
    keywords: ["dilucion", "concentracion", "c1v1", "c2v2", "solucion madre"],
    url: "/calculadoras/quimica/calculadora-de-diluciones/",
    status: "live",
  },
  {
    id: "ley-de-hooke",
    title: "Ley de Hooke",
    description: "Fuerza elástica, constante del resorte o deformación (F = k·x).",
    category: "ingenieria",
    keywords: ["hooke", "resorte", "elasticidad", "deformacion", "constante elastica"],
    url: "/calculadoras/ingenieria/ley-de-hooke/",
    status: "live",
  },
  {
    id: "calculadora-porcentajes",
    title: "Calculadora de Porcentajes",
    description: "Qué es el X% de Y, qué porcentaje representa un valor, y variación porcentual.",
    category: "finanzas",
    keywords: ["porcentaje", "descuento", "aumento", "variacion porcentual", "regla de tres"],
    url: "/calculadoras/finanzas/calculadora-de-porcentajes/",
    status: "live",
  },
  {
    id: "permutaciones-combinaciones",
    title: "Permutaciones y Combinaciones",
    description: "Análisis combinatorio: permutaciones, combinaciones y factorial, con y sin repetición.",
    category: "estadistica",
    keywords: ["permutaciones", "combinaciones", "combinatoria", "factorial", "probabilidad"],
    url: "/calculadoras/estadistica/permutaciones-y-combinaciones/",
    status: "live",
  },
  {
    id: "ley-de-ohm",
    title: "Ley de Ohm",
    description: "Voltaje, corriente, resistencia y potencia eléctrica, a partir de los datos conocidos.",
    category: "fisica",
    keywords: ["ohm", "voltaje", "corriente", "resistencia", "potencia", "circuito", "electricidad"],
    url: "/calculadoras/fisica/ley-de-ohm/",
    status: "live",
  },
  {
    id: "calculadora-molaridad",
    title: "Calculadora de Molaridad",
    description: "Molaridad, moles y volumen de una solución, y moles a partir de la masa.",
    category: "quimica",
    keywords: ["molaridad", "moles", "concentracion", "solucion", "masa molar"],
    url: "/calculadoras/quimica/calculadora-de-molaridad/",
    status: "live",
  },
  {
    id: "resistencias-serie-paralelo",
    title: "Resistencias en Serie y Paralelo",
    description: "Resistencia total de un circuito con múltiples resistores, en serie o en paralelo.",
    category: "ingenieria",
    keywords: ["resistencias", "circuito", "serie", "paralelo", "electronica", "ohm"],
    url: "/calculadoras/ingenieria/resistencias-serie-paralelo/",
    status: "live",
  },
  {
    id: "amortizacion-prestamos",
    title: "Amortización de Préstamos",
    description: "Cuota fija (sistema francés), total pagado e interés total de un préstamo.",
    category: "finanzas",
    keywords: ["prestamo", "amortizacion", "cuota", "credito", "sistema frances"],
    url: "/calculadoras/finanzas/amortizacion-prestamos/",
    status: "live",
  },
];
