/**
 * Calculadora de Fracciones — suma, resta, multiplicación y división, y simplificación.
 * Aritmética exacta con BigInt: nunca se pasa por decimales intermedios.
 * Acepta "3/4", "1 1/2" (número mixto), "-2/5", "7" y decimales ("0,75").
 */
(function () {
  const abs = (x) => (x < 0n ? -x : x);
  function gcd(a, b) {
    a = abs(a);
    b = abs(b);
    while (b) [a, b] = [b, a % b];
    return a;
  }
  function make(n, d) {
    if (d === 0n) throw new Error("El denominador no puede ser 0.");
    if (d < 0n) {
      n = -n;
      d = -d;
    }
    return { n, d };
  }
  function simplify(f) {
    const g = gcd(f.n, f.d) || 1n;
    return { n: f.n / g, d: f.d / g };
  }

  function parseFraction(text) {
    const s = String(text).trim().replace(/\s+/g, " ").replace("−", "-");
    if (!s) throw new Error("Completá la fracción.");
    let m;
    // número mixto: "-1 1/2"
    if ((m = s.match(/^(-?)(\d+) (\d+)\/(\d+)$/))) {
      const w = BigInt(m[2]), n = BigInt(m[3]), d = BigInt(m[4]);
      const num = w * d + n;
      return make(m[1] ? -num : num, d);
    }
    if ((m = s.match(/^(-?\d+)\s*\/\s*(-?\d+)$/))) return make(BigInt(m[1]), BigInt(m[2]));
    if ((m = s.match(/^(-?)(\d+)[.,](\d+)$/))) {
      const digits = m[3];
      const num = BigInt(m[2] + digits);
      return make(m[1] ? -num : num, 10n ** BigInt(digits.length));
    }
    if (/^-?\d+$/.test(s)) return make(BigInt(s), 1n);
    throw new Error(`No entendí "${text}". Escribila como 3/4, 1 1/2, 7 o 0,75.`);
  }

  const add = (a, b) => make(a.n * b.d + b.n * a.d, a.d * b.d);
  const sub = (a, b) => make(a.n * b.d - b.n * a.d, a.d * b.d);
  const mul = (a, b) => make(a.n * b.n, a.d * b.d);
  function div(a, b) {
    if (b.n === 0n) throw new Error("No se puede dividir por una fracción igual a 0.");
    return make(a.n * b.d, a.d * b.n);
  }

  function toMixed(f) {
    const s = simplify(f);
    const n = abs(s.n);
    return { whole: n / s.d, num: n % s.d, den: s.d, negative: s.n < 0n };
  }

  // Decimal exacto si el denominador (simplificado) solo tiene factores 2 y 5; si no, se corta.
  function toDecimal(f, maxDigits = 10) {
    const s = simplify(f);
    let d = s.d;
    while (d % 2n === 0n) d /= 2n;
    while (d % 5n === 0n) d /= 5n;
    const exact = d === 1n;
    const neg = s.n < 0n;
    const n = abs(s.n);
    const intPart = n / s.d;
    let rem = n % s.d;
    let digits = "";
    const limit = exact ? 400 : maxDigits;
    while (rem !== 0n && digits.length < limit) {
      rem *= 10n;
      digits += (rem / s.d).toString();
      rem %= s.d;
    }
    const text = (neg ? "-" : "") + intPart.toString() + (digits ? "," + digits : "");
    return { text, exact };
  }

  const fracStr = (f) => (f.d === 1n ? f.n.toString() : `${f.n}/${f.d}`);

  function compute(op, a, b) {
    switch (op) {
      case "add": return add(a, b);
      case "sub": return sub(a, b);
      case "mul": return mul(a, b);
      case "div": return div(a, b);
      default: throw new Error("Operación desconocida.");
    }
  }

  if (typeof module !== "undefined") module.exports = { gcd, parseFraction, simplify, add, sub, mul, div, toMixed, toDecimal, fracStr, compute };
  if (typeof document === "undefined" || !document.getElementById("fr-a")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("fr-result-panel");
  const SYMBOL = { add: "+", sub: "−", mul: "×", div: "÷" };

  function steps(op, a, b, raw) {
    const out = [];
    const A = fracStr(a), B = fracStr(b);
    if (op === "add" || op === "sub") {
      const lcm = (a.d * b.d) / gcd(a.d, b.d);
      const na = a.n * (lcm / a.d), nb = b.n * (lcm / b.d);
      const sign = op === "add" ? "+" : "−";
      out.push(`Denominador común: MCM(${a.d}, ${b.d}) = ${lcm}.`);
      out.push(`${A} = ${na}/${lcm} y ${B} = ${nb}/${lcm}.`);
      out.push(`${na}/${lcm} ${sign} ${nb}/${lcm} = ${op === "add" ? na + nb : na - nb}/${lcm}.`);
    } else if (op === "mul") {
      out.push(`Se multiplican numeradores y denominadores: (${a.n} × ${b.n}) / (${a.d} × ${b.d}) = ${raw.n}/${raw.d}.`);
    } else {
      out.push(`Dividir es multiplicar por la inversa: ${A} × ${b.d}/${b.n} = (${a.n} × ${b.d}) / (${a.d} × ${b.n}) = ${raw.n}/${raw.d}.`);
    }
    const g = gcd(raw.n, raw.d);
    if (g > 1n) out.push(`Se simplifica dividiendo numerador y denominador por su MCD (${g}): ${raw.n}/${raw.d} = ${raw.n / g}/${raw.d / g}.`);
    return out;
  }

  function show(main, lines, stepList) {
    $("fr-main").textContent = main;
    $("fr-lines").innerHTML = lines.map((l) => `<p>${l}</p>`).join("");
    $("fr-steps").innerHTML = stepList.length
      ? `<p class="font-semibold text-[var(--color-text)] mb-1">Desarrollo</p><ol class="list-decimal list-inside space-y-1">${stepList.map((s) => `<li>${s}</li>`).join("")}</ol>`
      : "";
    panel.classList.remove("hidden");
  }

  function extraLines(s) {
    const mixed = toMixed(s);
    const dec = toDecimal(s);
    return [
      mixed.whole !== 0n && mixed.num !== 0n ? `Número mixto: <strong>${mixed.negative ? "-" : ""}${mixed.whole} ${mixed.num}/${mixed.den}</strong>` : "",
      `Decimal: <strong>${dec.exact ? "" : "≈ "}${dec.text}</strong>`,
    ].filter(Boolean);
  }

  function calculate() {
    errorEl.classList.add("hidden");
    ["fr-a", "fr-b"].forEach((id) => $(id).classList.remove("field-error"));
    try {
      const op = $("fr-op").value;
      let a, b;
      try { a = parseFraction($("fr-a").value); } catch (e) { $("fr-a").classList.add("field-error"); throw e; }
      if (op === "simp") {
        const s = simplify(a);
        const g = gcd(a.n, a.d);
        const lines = [g > 1n ? `Se dividió por el MCD (${g}).` : "La fracción ya es irreducible.", ...extraLines(s)];
        show(fracStr(s), lines, [`MCD(${abs(a.n)}, ${a.d}) = ${g}.`, `${a.n}/${a.d} = ${s.n}/${s.d}.`]);
        return;
      }
      try { b = parseFraction($("fr-b").value); } catch (e) { $("fr-b").classList.add("field-error"); throw e; }
      const raw = compute(op, a, b);
      const s = simplify(raw);
      show(fracStr(s), [`${fracStr(a)} ${SYMBOL[op]} ${fracStr(b)} = <strong>${fracStr(s)}</strong>`, ...extraLines(s)], steps(op, a, b, raw));
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  function sync() {
    $("fr-b-wrap").classList.toggle("hidden", $("fr-op").value === "simp");
    errorEl.classList.add("hidden");
    panel.classList.add("hidden");
  }

  $("fr-op").addEventListener("change", sync);
  $("fr-solve").addEventListener("click", calculate);
  document.querySelectorAll("input").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && calculate()));
  document.querySelectorAll("[data-example]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const [a, op, b] = btn.dataset.example.split("|");
      $("fr-a").value = a;
      $("fr-op").value = op;
      $("fr-b").value = b || "";
      sync();
      calculate();
    })
  );
  sync();
})();
