/**
 * Balanceo de ecuaciones químicas por el método algebraico: cada elemento da una ecuación lineal en los
 * coeficientes; se resuelve el sistema homogéneo con aritmética de fracciones exactas (BigInt).
 * Soporta paréntesis y corchetes (Ca(OH)2) e hidratos (CuSO4·5H2O). No soporta cargas iónicas.
 */
(function () {
  const abs = (x) => (x < 0n ? -x : x);
  const gcd = (a, b) => {
    a = abs(a);
    b = abs(b);
    while (b) [a, b] = [b, a % b];
    return a;
  };
  const fr = (n, d = 1n) => {
    if (d < 0n) [n, d] = [-n, -d];
    const g = gcd(n, d) || 1n;
    return [n / g, d / g];
  };
  const fsub = (a, b) => fr(a[0] * b[1] - b[0] * a[1], a[1] * b[1]);
  const fmul = (a, b) => fr(a[0] * b[0], a[1] * b[1]);
  const fdiv = (a, b) => fr(a[0] * b[1], a[1] * b[0]);

  function parseFormula(raw) {
    const text = String(raw).trim();
    if (!text) throw new Error("Hay una fórmula vacía.");
    const parts = text.split(/[·.*]/);
    const total = new Map();
    for (const part of parts) {
      const lead = /^(\d+)(.*)$/.exec(part.trim());
      const mult = lead ? Number(lead[1]) : 1;
      const body = lead ? lead[2] : part.trim();
      const counts = parseGroup(body);
      counts.forEach((c, el) => total.set(el, (total.get(el) || 0) + c * mult));
    }
    return total;
  }

  function parseGroup(s) {
    let i = 0;
    function readNum() {
      let n = "";
      while (i < s.length && /\d/.test(s[i])) n += s[i++];
      return n ? Number(n) : 1;
    }
    function group(close) {
      const map = new Map();
      while (i < s.length) {
        const ch = s[i];
        if (ch === close) return map;
        if (ch === "(" || ch === "[") {
          i++;
          const inner = group(ch === "(" ? ")" : "]");
          if (s[i] !== (ch === "(" ? ")" : "]")) throw new Error(`Falta cerrar un paréntesis en "${s}".`);
          i++;
          const n = readNum();
          inner.forEach((c, el) => map.set(el, (map.get(el) || 0) + c * n));
        } else if (/[A-Z]/.test(ch)) {
          let el = ch;
          i++;
          while (i < s.length && /[a-z]/.test(s[i])) el += s[i++];
          map.set(el, (map.get(el) || 0) + readNum());
        } else {
          throw new Error(`Carácter no válido "${ch}" en la fórmula "${s}". Usá símbolos como H2O, Ca(OH)2 o Fe2(SO4)3.`);
        }
      }
      if (close) throw new Error(`Falta cerrar un paréntesis en "${s}".`);
      return map;
    }
    return group(null);
  }

  function balance(equation) {
    const sides = String(equation).split(/->|→|=>|=/);
    if (sides.length !== 2 || !sides[0].trim() || !sides[1].trim()) throw new Error('Escribí la ecuación con una flecha: por ejemplo "H2 + O2 -> H2O".');
    const reactants = sides[0].split("+").map((x) => x.trim());
    const products = sides[1].split("+").map((x) => x.trim());
    const species = [...reactants, ...products];
    if (species.some((x) => !x)) throw new Error("Hay un signo + sin fórmula a un lado.");
    const parsed = species.map(parseFormula);
    const elements = [...new Set(parsed.flatMap((m) => [...m.keys()]))];
    const nR = reactants.length;
    if (!elements.length) throw new Error("No se reconocieron elementos.");
    // matriz elementos × especies (reactivos +, productos −)
    const M = elements.map((el) => parsed.map((m, j) => fr(BigInt((m.get(el) || 0) * (j < nR ? 1 : -1)))));
    const cols = species.length;
    // RREF
    const pivots = [];
    let row = 0;
    for (let c = 0; c < cols && row < M.length; c++) {
      let p = row;
      while (p < M.length && M[p][c][0] === 0n) p++;
      if (p === M.length) continue;
      [M[row], M[p]] = [M[p], M[row]];
      const pv = M[row][c];
      M[row] = M[row].map((x) => fdiv(x, pv));
      for (let r = 0; r < M.length; r++) {
        if (r !== row && M[r][c][0] !== 0n) {
          const factor = M[r][c];
          M[r] = M[r].map((x, k) => fsub(x, fmul(factor, M[row][k])));
        }
      }
      pivots.push(c);
      row++;
    }
    const free = [...Array(cols).keys()].filter((c) => !pivots.includes(c));
    if (free.length === 0) throw new Error("Esta ecuación no se puede balancear: revisá que las fórmulas sean correctas y estén en el lado que corresponde.");
    if (free.length > 1) throw new Error("La ecuación admite infinitas formas de balanceo (mezcla varias reacciones independientes). Separala en reacciones más simples.");
    const fv = free[0];
    const vec = Array(cols).fill(null);
    vec[fv] = fr(1n);
    pivots.forEach((pc, r) => (vec[pc] = fr(-M[r][fv][0], M[r][fv][1])));
    let lcm = 1n;
    vec.forEach((x) => (lcm = (lcm * x[1]) / gcd(lcm, x[1])));
    let ints = vec.map((x) => (x[0] * lcm) / x[1]);
    const g = ints.reduce((a, b) => gcd(a, b), 0n) || 1n;
    ints = ints.map((x) => x / g);
    if (ints.some((x) => x <= 0n)) throw new Error("No se encontró un balanceo con coeficientes positivos: revisá las fórmulas.");
    return { reactants, products, coeffs: ints.map(Number), nReactants: nR };
  }

  const SUB = "₀₁₂₃₄₅₆₇₈₉";
  const pretty = (f) => f.replace(/(?<=[A-Za-z)\]])(\d+)/g, (m) => m.replace(/\d/g, (d) => SUB[d]));
  function format(result) {
    const side = (names, coeffs) => names.map((n, i) => `${coeffs[i] === 1 ? "" : coeffs[i] + " "}${pretty(n)}`).join(" + ");
    return `${side(result.reactants, result.coeffs.slice(0, result.nReactants))} → ${side(result.products, result.coeffs.slice(result.nReactants))}`;
  }

  if (typeof module !== "undefined") module.exports = { parseFormula, balance, format };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("bq-solve")) return;

  CCSimple.mount({
    prefix: "bq",
    compute(v) {
      const r = balance(v.equation);
      const all = [...r.reactants, ...r.products];
      const elems = [...new Set(all.flatMap((x) => [...parseFormula(x).keys()]))];
      const count = (names, coeffs, el) => names.reduce((a, n, i) => a + coeffs[i] * (parseFormula(n).get(el) || 0), 0);
      const rows = elems.map((el) => `<li>${el}: ${count(r.reactants, r.coeffs.slice(0, r.nReactants), el)} átomos a cada lado</li>`).join("");
      return { label: "Ecuación balanceada", main: format(r), lines: ["Cada elemento tiene la misma cantidad de átomos en reactivos y productos:"], extra: `<ul class="list-disc list-inside space-y-1">${rows}</ul>` };
    },
  });
})();
