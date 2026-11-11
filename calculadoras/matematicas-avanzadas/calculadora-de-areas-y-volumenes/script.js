/**
 * Calculadora de Áreas, Perímetros y Volúmenes de figuras geométricas.
 * Cada figura declara sus datos (fields) y una función que devuelve las magnitudes calculadas.
 */
(function () {
  function normalizeNumberInput(value) {
    let str = String(value).trim();
    if (str.includes(",")) {
      str = str.replace(/\./g, "").replace(",", ".");
    } else if (/^-?[1-9]\d{0,2}(\.\d{3})+$/.test(str)) {
      str = str.replace(/\./g, "");
    }
    return str;
  }

  const PI = Math.PI;
  // kind: "plana" (área y perímetro) o "cuerpo" (volumen y superficie)
  // out: [clave, etiqueta, fórmula] en orden de importancia; la primera es el resultado principal.
  const SHAPES = {
    cuadrado: {
      name: "Cuadrado", kind: "plana", fields: [["l", "Lado"]],
      calc: ([l]) => ({ area: l * l, perimetro: 4 * l, diagonal: l * Math.SQRT2 }),
      out: [["area", "Área", "l²"], ["perimetro", "Perímetro", "4·l"], ["diagonal", "Diagonal", "l·√2"]],
    },
    rectangulo: {
      name: "Rectángulo", kind: "plana", fields: [["b", "Base"], ["h", "Altura"]],
      calc: ([b, h]) => ({ area: b * h, perimetro: 2 * (b + h), diagonal: Math.hypot(b, h) }),
      out: [["area", "Área", "b·h"], ["perimetro", "Perímetro", "2·(b + h)"], ["diagonal", "Diagonal", "√(b² + h²)"]],
    },
    triangulo: {
      name: "Triángulo (base y altura)", kind: "plana", fields: [["b", "Base"], ["h", "Altura"]],
      calc: ([b, h]) => ({ area: (b * h) / 2 }),
      out: [["area", "Área", "b·h / 2"]],
    },
    "triangulo-lados": {
      name: "Triángulo (tres lados, Herón)", kind: "plana", fields: [["a", "Lado a"], ["b", "Lado b"], ["c", "Lado c"]],
      calc: ([a, b, c]) => {
        if (a + b > c && a + c > b && b + c > a) {
          const s = (a + b + c) / 2;
          return { area: Math.sqrt(s * (s - a) * (s - b) * (s - c)), perimetro: a + b + c, semiperimetro: s };
        }
        throw new Error("Esos lados no forman un triángulo: cada lado tiene que ser menor que la suma de los otros dos.");
      },
      out: [["area", "Área", "√(s·(s−a)·(s−b)·(s−c))"], ["perimetro", "Perímetro", "a + b + c"], ["semiperimetro", "Semiperímetro s", "(a + b + c) / 2"]],
    },
    circulo: {
      name: "Círculo", kind: "plana", fields: [["r", "Radio"]],
      calc: ([r]) => ({ area: PI * r * r, perimetro: 2 * PI * r, diametro: 2 * r }),
      out: [["area", "Área", "π·r²"], ["perimetro", "Circunferencia", "2·π·r"], ["diametro", "Diámetro", "2·r"]],
    },
    trapecio: {
      name: "Trapecio", kind: "plana", fields: [["B", "Base mayor"], ["b", "Base menor"], ["h", "Altura"]],
      calc: ([B, b, h]) => ({ area: ((B + b) * h) / 2 }),
      out: [["area", "Área", "(B + b)·h / 2"]],
    },
    rombo: {
      name: "Rombo", kind: "plana", fields: [["D", "Diagonal mayor"], ["d", "Diagonal menor"]],
      calc: ([D, d]) => {
        const lado = Math.hypot(D / 2, d / 2);
        return { area: (D * d) / 2, lado, perimetro: 4 * lado };
      },
      out: [["area", "Área", "D·d / 2"], ["lado", "Lado", "√((D/2)² + (d/2)²)"], ["perimetro", "Perímetro", "4·lado"]],
    },
    paralelogramo: {
      name: "Paralelogramo", kind: "plana", fields: [["b", "Base"], ["h", "Altura"]],
      calc: ([b, h]) => ({ area: b * h }),
      out: [["area", "Área", "b·h"]],
    },
    cubo: {
      name: "Cubo", kind: "cuerpo", fields: [["a", "Arista"]],
      calc: ([a]) => ({ volumen: a ** 3, superficie: 6 * a * a, diagonal: a * Math.sqrt(3) }),
      out: [["volumen", "Volumen", "a³"], ["superficie", "Superficie total", "6·a²"], ["diagonal", "Diagonal", "a·√3"]],
    },
    prisma: {
      name: "Prisma rectangular", kind: "cuerpo", fields: [["a", "Largo"], ["b", "Ancho"], ["c", "Alto"]],
      calc: ([a, b, c]) => ({ volumen: a * b * c, superficie: 2 * (a * b + b * c + a * c), diagonal: Math.sqrt(a * a + b * b + c * c) }),
      out: [["volumen", "Volumen", "a·b·c"], ["superficie", "Superficie total", "2·(ab + bc + ac)"], ["diagonal", "Diagonal", "√(a² + b² + c²)"]],
    },
    cilindro: {
      name: "Cilindro", kind: "cuerpo", fields: [["r", "Radio"], ["h", "Altura"]],
      calc: ([r, h]) => ({ volumen: PI * r * r * h, lateral: 2 * PI * r * h, superficie: 2 * PI * r * (r + h) }),
      out: [["volumen", "Volumen", "π·r²·h"], ["lateral", "Superficie lateral", "2·π·r·h"], ["superficie", "Superficie total", "2·π·r·(r + h)"]],
    },
    cono: {
      name: "Cono", kind: "cuerpo", fields: [["r", "Radio"], ["h", "Altura"]],
      calc: ([r, h]) => {
        const g = Math.hypot(r, h);
        return { volumen: (PI * r * r * h) / 3, generatriz: g, lateral: PI * r * g, superficie: PI * r * (r + g) };
      },
      out: [["volumen", "Volumen", "π·r²·h / 3"], ["generatriz", "Generatriz", "√(r² + h²)"], ["lateral", "Superficie lateral", "π·r·g"], ["superficie", "Superficie total", "π·r·(r + g)"]],
    },
    esfera: {
      name: "Esfera", kind: "cuerpo", fields: [["r", "Radio"]],
      calc: ([r]) => ({ volumen: (4 / 3) * PI * r ** 3, superficie: 4 * PI * r * r }),
      out: [["volumen", "Volumen", "4/3·π·r³"], ["superficie", "Superficie", "4·π·r²"]],
    },
    piramide: {
      name: "Pirámide de base cuadrada", kind: "cuerpo", fields: [["a", "Lado de la base"], ["h", "Altura"]],
      calc: ([a, h]) => {
        const ap = Math.hypot(h, a / 2);
        return { volumen: (a * a * h) / 3, apotema: ap, lateral: 2 * a * ap, superficie: a * a + 2 * a * ap };
      },
      out: [["volumen", "Volumen", "a²·h / 3"], ["apotema", "Apotema", "√(h² + (a/2)²)"], ["lateral", "Superficie lateral", "2·a·apotema"], ["superficie", "Superficie total", "a² + 2·a·apotema"]],
    },
  };

  function compute(shape, values) {
    const s = SHAPES[shape];
    if (!s) throw new Error("Figura desconocida.");
    if (values.length !== s.fields.length || values.some((v) => !(v > 0))) throw new Error("Todos los datos tienen que ser números mayores a 0.");
    return s.calc(values);
  }

  if (typeof module !== "undefined") module.exports = { SHAPES, compute };
  if (typeof document === "undefined" || !document.getElementById("av-shape")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("av-result-panel");
  const fmt = (n) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: 4 }).format(Math.round((n + 1e-12) * 1e4) / 1e4);
  const MAX_FIELDS = 3;

  function sync() {
    const s = SHAPES[$("av-shape").value];
    for (let i = 0; i < MAX_FIELDS; i++) {
      const wrap = $("av-wrap-" + i);
      const f = s.fields[i];
      wrap.classList.toggle("hidden", !f);
      if (f) $("av-label-" + i).textContent = f[1];
    }
    errorEl.classList.add("hidden");
    panel.classList.add("hidden");
  }

  function calculate() {
    errorEl.classList.add("hidden");
    try {
      const key = $("av-shape").value;
      const s = SHAPES[key];
      const values = s.fields.map(([, label], i) => {
        const el = $("av-f" + i);
        el.classList.remove("field-error");
        const raw = normalizeNumberInput(el.value);
        if (raw === "") {
          el.classList.add("field-error");
          throw new Error(`Completá el campo "${label}".`);
        }
        const v = Number(raw);
        if (!Number.isFinite(v) || v <= 0) {
          el.classList.add("field-error");
          throw new Error(`"${label}" tiene que ser un número mayor a 0.`);
        }
        return v;
      });
      const r = compute(key, values);
      const unit = $("av-unit").value;
      const [mainKey, mainLabel] = s.out[0];
      const unitFor = (k) => (k === "volumen" ? `${unit}³` : ["area", "superficie", "lateral"].includes(k) ? `${unit}²` : unit);
      $("av-label").textContent = mainLabel + " — " + s.name;
      $("av-main").textContent = `${fmt(r[mainKey])} ${unitFor(mainKey)}`;
      $("av-lines").innerHTML = s.out
        .slice(1)
        .map(([k, label, formula]) => `<p>${label}: <strong>${fmt(r[k])} ${unitFor(k)}</strong> <span class="font-numeric">(${formula})</span></p>`)
        .join("") + `<p class="font-numeric">${mainLabel} = ${s.out[0][2]}</p>`;
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("av-shape").addEventListener("change", sync);
  $("av-solve").addEventListener("click", calculate);
  document.querySelectorAll("input").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && calculate()));
  document.querySelectorAll("[data-example]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const [shape, ...vals] = btn.dataset.example.split("|");
      $("av-shape").value = shape;
      sync();
      vals.forEach((v, i) => ($("av-f" + i).value = v));
      calculate();
    })
  );
  sync();
})();
