/**
 * Números primos — verifica si un número es primo, lo factoriza y busca el primo siguiente y anterior.
 * División por tentativa (6k ± 1) hasta √n: instantáneo hasta 10^12.
 */
(function () {
  const LIMIT = 1e12;

  function isPrime(n) {
    if (n < 2) return false;
    if (n < 4) return true;
    if (n % 2 === 0 || n % 3 === 0) return false;
    for (let i = 5; i * i <= n; i += 6) if (n % i === 0 || n % (i + 2) === 0) return false;
    return true;
  }

  function factorize(n) {
    const f = new Map();
    let m = n;
    for (let p = 2; p * p <= m; p += p === 2 ? 1 : 2) {
      while (m % p === 0) {
        f.set(p, (f.get(p) || 0) + 1);
        m /= p;
      }
    }
    if (m > 1) f.set(m, (f.get(m) || 0) + 1);
    return f;
  }

  function nextPrime(n) {
    let c = Math.floor(n) + 1;
    while (!isPrime(c)) c++;
    return c;
  }
  function prevPrime(n) {
    let c = Math.floor(n) - 1;
    while (c >= 2 && !isPrime(c)) c--;
    return c >= 2 ? c : null;
  }
  const divisorCount = (f) => [...f.values()].reduce((a, e) => a * (e + 1), 1);

  if (typeof module !== "undefined") module.exports = { isPrime, factorize, nextPrime, prevPrime, divisorCount, LIMIT };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("np-solve")) return;

  CCSimple.mount({
    prefix: "np",
    compute(v, h) {
      if (v.n > LIMIT) throw new Error("El número es demasiado grande: el máximo es 1.000.000.000.000.");
      const prime = isPrime(v.n);
      const f = v.n >= 2 ? factorize(v.n) : new Map();
      const text = [...f.entries()].map(([p, e]) => (e > 1 ? `${h.fmt(p, 0)}${String(e).replace(/\d/g, (d) => "⁰¹²³⁴⁵⁶⁷⁸⁹"[d])}` : h.fmt(p, 0))).join(" × ");
      const prev = prevPrime(v.n);
      const lines = [
        prime ? "Solo tiene dos divisores: 1 y él mismo." : `Factores primos: <strong>${text || "—"}</strong> · Cantidad de divisores: <strong>${divisorCount(f)}</strong>.`,
        `Primo siguiente: <strong>${h.fmt(nextPrime(v.n), 0)}</strong>${prev ? ` · Primo anterior: <strong>${h.fmt(prev, 0)}</strong>` : ""}.`,
      ];
      return { label: `${h.fmt(v.n, 0)}`, main: v.n === 1 ? "1 no es primo ni compuesto" : prime ? "Es primo" : "No es primo (es compuesto)", lines };
    },
  });
})();
