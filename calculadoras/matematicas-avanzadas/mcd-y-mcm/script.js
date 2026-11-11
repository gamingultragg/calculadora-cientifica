/**
 * MCD y MCM — máximo común divisor y mínimo común múltiplo de 2 a 10 números
 * enteros positivos, con el algoritmo de Euclides paso a paso y la descomposición en
 * factores primos. Usa BigInt para no perder precisión con números grandes.
 */
(function () {
  function parseNumbers(input) {
    const tokens = String(input)
      .trim()
      .split(/[\s,;]+/)
      .filter(Boolean);
    if (tokens.length < 2) throw new Error("Ingresá al menos dos números separados por espacios o comas.");
    if (tokens.length > 10) throw new Error("Podés ingresar hasta 10 números.");
    return tokens.map((tk) => {
      let s = tk;
      if (/^\d{1,3}(\.\d{3})+$/.test(s)) s = s.replace(/\./g, ""); // 1.200 => 1200
      if (!/^\d+$/.test(s)) throw new Error(`"${tk}" no es un entero positivo. Usá solo dígitos (sin decimales ni signos).`);
      const n = BigInt(s);
      if (n === 0n) throw new Error("Los números tienen que ser mayores a 0.");
      return n;
    });
  }

  function gcd(a, b) {
    while (b !== 0n) [a, b] = [b, a % b];
    return a;
  }
  const lcm = (a, b) => (a / gcd(a, b)) * b;

  // Pasos de Euclides: [{a, b, q, r}]
  function euclidSteps(a, b) {
    const steps = [];
    let x = a >= b ? a : b;
    let y = a >= b ? b : a;
    while (y !== 0n) {
      const q = x / y;
      const r = x % y;
      steps.push({ a: x, b: y, q, r });
      x = y;
      y = r;
    }
    return steps;
  }

  function compute(nums) {
    let g = nums[0];
    let l = nums[0];
    for (let i = 1; i < nums.length; i++) {
      g = gcd(g, nums[i]);
      l = lcm(l, nums[i]);
    }
    return { gcd: g, lcm: l };
  }

  // Factorización por división sucesiva (solo para números hasta 10^12).
  const FACTOR_LIMIT = 10n ** 12n;
  function factorize(n) {
    if (n > FACTOR_LIMIT) return null;
    let x = Number(n);
    const out = new Map();
    for (let p = 2; p * p <= x; p += p === 2 ? 1 : 2) {
      while (x % p === 0) {
        out.set(p, (out.get(p) || 0) + 1);
        x /= p;
      }
    }
    if (x > 1) out.set(x, (out.get(x) || 0) + 1);
    return out;
  }

  if (typeof module !== "undefined") module.exports = { parseNumbers, gcd, lcm, euclidSteps, compute, factorize };
  if (typeof document === "undefined" || !document.getElementById("md-input")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("md-result-panel");
  const fmt = (n) => n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  const sup = (e) => (e === 1 ? "" : `<sup>${e}</sup>`);

  function factorsText(map) {
    return [...map.entries()].sort((a, b) => a[0] - b[0]).map(([p, e]) => `${p}${sup(e)}`).join(" × ");
  }

  function calculate() {
    errorEl.classList.add("hidden");
    $("md-input").classList.remove("field-error");
    try {
      const nums = parseNumbers($("md-input").value);
      const { gcd: g, lcm: l } = compute(nums);
      $("md-gcd").textContent = fmt(g);
      $("md-lcm").textContent = fmt(l);

      // Descomposición en factores primos (si todos los números entran en el límite).
      const facts = nums.map(factorize);
      const stepsEl = $("md-steps");
      const parts = [];
      if (facts.every(Boolean)) {
        parts.push(
          `<p class="font-semibold text-[var(--color-text)] mb-1">Descomposición en factores primos</p><ul class="space-y-1">` +
            nums.map((n, i) => `<li><span class="font-numeric">${fmt(n)}</span> = ${facts[i].size === 1 && [...facts[i].values()][0] === 1 ? "primo" : factorsText(facts[i])}</li>`).join("") +
            `</ul>`
        );
        const allPrimes = new Set();
        facts.forEach((f) => f.forEach((_, p) => allPrimes.add(p)));
        const gParts = [];
        const lParts = [];
        [...allPrimes].sort((a, b) => a - b).forEach((p) => {
          const exps = facts.map((f) => f.get(p) || 0);
          const min = Math.min(...exps);
          const max = Math.max(...exps);
          if (min > 0) gParts.push(`${p}${sup(min)}`);
          lParts.push(`${p}${sup(max)}`);
        });
        parts.push(
          `<p class="mt-3"><strong>MCD</strong> = factores comunes con el menor exponente: ${gParts.length ? gParts.join(" × ") : "no hay factores comunes (MCD = 1)"}.</p>`,
          `<p><strong>MCM</strong> = todos los factores con el mayor exponente: ${lParts.join(" × ")}.</p>`
        );
      } else {
        parts.push(`<p>La descomposición en factores primos se muestra para números hasta 10<sup>12</sup>.</p>`);
      }
      // Euclides para los dos primeros números.
      const st = euclidSteps(nums[0], nums[1]);
      parts.push(
        `<p class="font-semibold text-[var(--color-text)] mt-3 mb-1">Algoritmo de Euclides (${fmt(nums[0])} y ${fmt(nums[1])})</p><ul class="space-y-1 font-numeric">` +
          st.map((s) => `<li>${fmt(s.a)} = ${fmt(s.b)} × ${fmt(s.q)} + ${fmt(s.r)}</li>`).join("") +
          `</ul><p class="mt-1">El último resto distinto de 0 es el MCD de esos dos números: <strong>${fmt(gcd(nums[0], nums[1]))}</strong>.</p>`
      );
      if (nums.length > 2) parts.push(`<p class="mt-2">Con más de dos números se aplica el mismo procedimiento de a pares: MCD(a, b, c) = MCD(MCD(a, b), c).</p>`);
      stepsEl.innerHTML = parts.join("");
      panel.classList.remove("hidden");
    } catch (err) {
      $("md-input").classList.add("field-error");
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("md-solve").addEventListener("click", calculate);
  $("md-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter") calculate();
  });
  document.querySelectorAll("[data-example]").forEach((btn) =>
    btn.addEventListener("click", () => {
      $("md-input").value = btn.dataset.example;
      calculate();
    })
  );
})();
