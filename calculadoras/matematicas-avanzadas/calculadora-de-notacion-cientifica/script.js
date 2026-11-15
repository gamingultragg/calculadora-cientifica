/**
 * Notación científica — conversión exacta entre decimal y a × 10ⁿ (trabaja con los dígitos como texto, sin errores de
 * coma flotante), notación de ingeniería (exponente múltiplo de 3) y operaciones entre dos números en notación científica.
 */
(function () {
  const SUP = { 0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹", "-": "⁻" };
  const sup = (n) => String(n).replace(/[0-9-]/g, (c) => SUP[c]);

  // Acepta "123,45", "1.234,5", "0.00045" y "12.345" (punto de miles). Devuelve un texto con punto decimal.
  function parseDecimal(str) {
    let s = String(str).trim().replace(/\s/g, "");
    if (s.includes(",")) s = s.replace(/\./g, "").replace(",", ".");
    else if (/^[+-]?\d{1,3}(\.\d{3})+$/.test(s)) s = s.replace(/\./g, "");
    if (!/^[+-]?(\d+\.?\d*|\.\d+)$/.test(s)) throw new Error("Escribí un número válido, por ejemplo 123456 o 0,00045.");
    return s;
  }

  // Texto decimal → { neg, digits (cifras significativas sin ceros al final), exp } con valor = d,ddd × 10^exp
  function toScientific(str) {
    const s = parseDecimal(str);
    const neg = s.startsWith("-");
    const body = s.replace(/^[+-]/, "");
    const [intPart, fracPart = ""] = body.split(".");
    const int = intPart || "0";
    const digits = int + fracPart;
    const first = digits.search(/[1-9]/);
    if (first === -1) return { neg: false, digits: "0", exp: 0, zero: true };
    return { neg, digits: digits.slice(first).replace(/0+$/, ""), exp: int.length - 1 - first };
  }

  const mantissaText = (digits, intLen = 1) => {
    const d = digits.padEnd(intLen, "0");
    const frac = d.slice(intLen);
    return d.slice(0, intLen) + (frac ? "," + frac : "");
  };
  function formatSci(sc) {
    if (sc.zero) return "0";
    return `${sc.neg ? "−" : ""}${mantissaText(sc.digits)} × 10${sup(sc.exp)}`;
  }
  function formatEng(sc) {
    if (sc.zero) return "0";
    const exp3 = Math.floor(sc.exp / 3) * 3;
    return `${sc.neg ? "−" : ""}${mantissaText(sc.digits, 1 + (sc.exp - exp3))} × 10${sup(exp3)}`;
  }

  // a × 10^exp → texto decimal con separador de miles (punto) y coma decimal
  function toDecimal(mantStr, exp) {
    if (!Number.isInteger(exp) || Math.abs(exp) > 300) throw new Error('"Exponente" tiene que ser un entero entre −300 y 300.');
    const s = parseDecimal(mantStr);
    const neg = s.startsWith("-");
    const [intPart, fracPart = ""] = s.replace(/^[+-]/, "").split(".");
    const int = intPart || "0";
    const digits = int + fracPart;
    const point = int.length + exp;
    let out;
    if (point <= 0) out = "0," + "0".repeat(-point) + digits;
    else if (point >= digits.length) out = digits + "0".repeat(point - digits.length);
    else out = digits.slice(0, point) + "," + digits.slice(point);
    let [i2, f2 = ""] = out.split(",");
    i2 = i2.replace(/^0+(?=\d)/, "");
    f2 = f2.replace(/0+$/, "");
    if (/^0*$/.test(i2) && f2 === "") return "0";
    return (neg ? "−" : "") + i2.replace(/\B(?=(\d{3})+(?!\d))/g, ".") + (f2 ? "," + f2 : "");
  }

  // (ma × 10^ea) op (mb × 10^eb) con 12 cifras significativas, para evitar el ruido de la coma flotante
  function operate(ma, ea, op, mb, eb) {
    [ea, eb].forEach((e) => {
      if (!Number.isInteger(e) || Math.abs(e) > 300) throw new Error('Los exponentes tienen que ser enteros entre −300 y 300.');
    });
    const a = Number(`${parseDecimal(ma)}e${ea}`);
    const b = Number(`${parseDecimal(mb)}e${eb}`);
    let r;
    if (op === "+") r = a + b;
    else if (op === "-") r = a - b;
    else if (op === "*") r = a * b;
    else {
      if (b === 0) throw new Error("No se puede dividir por 0.");
      r = a / b;
    }
    if (!Number.isFinite(r)) throw new Error("El resultado es demasiado grande para calcularlo.");
    if (r === 0) return { sci: { zero: true, digits: "0", exp: 0, neg: false }, decimal: "0" };
    const [m, e] = Number(r.toPrecision(12)).toExponential().split("e");
    const exp = Number(e);
    const sci = toScientific(m);
    sci.exp = exp;
    const decimal = Math.abs(exp) <= 300 ? toDecimal(m, exp) : "—";
    return { sci, decimal };
  }

  // Prefijos del SI para los exponentes múltiplos de 3
  const PREFIX = { "-12": "pico (p)", "-9": "nano (n)", "-6": "micro (µ)", "-3": "mili (m)", 0: "", 3: "kilo (k)", 6: "mega (M)", 9: "giga (G)", 12: "tera (T)" };

  if (typeof module !== "undefined") module.exports = { parseDecimal, toScientific, formatSci, formatEng, toDecimal, operate, sup, PREFIX };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("nc-solve")) return;

  CCSimple.mount({
    prefix: "nc",
    compute(v) {
      if (v.mode === "sci") {
        const sc = toScientific(v.dec);
        const exp3 = sc.zero ? 0 : Math.floor(sc.exp / 3) * 3;
        const lines = [
          `Notación científica: <strong>${formatSci(sc)}</strong>.`,
          `Notación de ingeniería: ${formatEng(sc)}.`,
          sc.zero ? null : `Orden de magnitud: 10${sup(sc.exp)} (${sc.digits.length} cifra${sc.digits.length === 1 ? "" : "s"} significativa${sc.digits.length === 1 ? "" : "s"}).`,
          PREFIX[exp3] ? `Prefijo del SI para 10${sup(exp3)}: ${PREFIX[exp3]}.` : null,
        ];
        return { label: "Notación científica", main: formatSci(sc), lines };
      }
      if (v.mode === "dec") {
        const d = toDecimal(v.man, v.exp);
        const sc = toScientific(parseDecimal(v.man));
        if (!sc.zero) sc.exp += v.exp; // la forma normalizada tiene una sola cifra antes de la coma
        return { label: "Número decimal", main: d, lines: [`${v.man} × 10${sup(v.exp)} = <strong>${d}</strong>.`, `Normalizado: ${formatSci(sc)}.`] };
      }
      const r = operate(v.ma, v.ea, v.op, v.mb, v.eb);
      const sym = { "+": "+", "-": "−", "*": "×", "/": "÷" }[v.op];
      return {
        label: "Resultado",
        main: formatSci(r.sci),
        lines: [`(${v.ma} × 10${sup(v.ea)}) ${sym} (${v.mb} × 10${sup(v.eb)}) = <strong>${formatSci(r.sci)}</strong>.`, `En notación de ingeniería: ${formatEng(r.sci)}.`, `En decimal: ${r.decimal}.`],
      };
    },
  });
})();
