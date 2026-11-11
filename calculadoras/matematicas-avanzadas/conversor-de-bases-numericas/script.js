/**
 * Conversor de Bases Numéricas — binario, octal, decimal, hexadecimal y cualquier base de 2 a 36.
 * Usa BigInt: no pierde precisión con números enormes. Solo enteros (con signo).
 */
(function () {
  const DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz";

  function parseInBase(text, base) {
    let s = String(text).trim().toLowerCase().replace(/[\s_]/g, "");
    if (!s) throw new Error("Ingresá un número.");
    let neg = false;
    if (s[0] === "-" || s[0] === "+") {
      neg = s[0] === "-";
      s = s.slice(1);
    }
    // prefijos habituales
    if (base === 16 && s.startsWith("0x")) s = s.slice(2);
    if (base === 2 && s.startsWith("0b")) s = s.slice(2);
    if (base === 8 && s.startsWith("0o")) s = s.slice(2);
    if (!s) throw new Error("Ingresá un número.");
    if (s.length > 300) throw new Error("El número es demasiado largo (máximo 300 dígitos).");
    let value = 0n;
    const B = BigInt(base);
    for (const ch of s) {
      const d = DIGITS.indexOf(ch);
      if (d < 0 || d >= base) throw new Error(`"${ch.toUpperCase()}" no es un dígito válido en base ${base}.`);
      value = value * B + BigInt(d);
    }
    return neg ? -value : value;
  }

  function toBase(value, base) {
    if (value === 0n) return "0";
    const neg = value < 0n;
    let v = neg ? -value : value;
    const B = BigInt(base);
    let out = "";
    while (v > 0n) {
      out = DIGITS[Number(v % B)] + out;
      v /= B;
    }
    return (neg ? "-" : "") + out;
  }

  // Divisiones sucesivas (para mostrar el desarrollo con números chicos).
  function divisionSteps(value, base) {
    const steps = [];
    let v = value < 0n ? -value : value;
    const B = BigInt(base);
    while (v > 0n) {
      const q = v / B, r = v % B;
      steps.push({ dividend: v, quotient: q, remainder: r, digit: DIGITS[Number(r)] });
      v = q;
    }
    return steps;
  }

  if (typeof module !== "undefined") module.exports = { parseInBase, toBase, divisionSteps };
  if (typeof document === "undefined" || !document.getElementById("bn-input")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("bn-result-panel");

  const group = (s, size) => {
    const neg = s.startsWith("-");
    const body = neg ? s.slice(1) : s;
    const parts = [];
    for (let i = body.length; i > 0; i -= size) parts.unshift(body.slice(Math.max(0, i - size), i));
    return (neg ? "-" : "") + parts.join(" ");
  };

  function readBase(id, label) {
    const v = Number($(id).value);
    if (!Number.isInteger(v) || v < 2 || v > 36) {
      $(id).classList.add("field-error");
      throw new Error(`"${label}" tiene que ser un número entero entre 2 y 36.`);
    }
    return v;
  }

  function syncCustom() {
    $("bn-from-custom-wrap").classList.toggle("hidden", $("bn-from").value !== "custom");
  }

  function calculate() {
    errorEl.classList.add("hidden");
    ["bn-input", "bn-from-custom", "bn-to-custom"].forEach((id) => $(id).classList.remove("field-error"));
    try {
      const fromSel = $("bn-from").value;
      const base = fromSel === "custom" ? readBase("bn-from-custom", "Base de origen") : Number(fromSel);
      let value;
      try {
        value = parseInBase($("bn-input").value, base);
      } catch (e) {
        $("bn-input").classList.add("field-error");
        throw e;
      }
      const rows = [
        ["Binario (base 2)", group(toBase(value, 2), 4)],
        ["Octal (base 8)", toBase(value, 8)],
        ["Decimal (base 10)", toBase(value, 10)],
        ["Hexadecimal (base 16)", toBase(value, 16).toUpperCase()],
      ];
      const customTo = $("bn-to-custom").value.trim();
      if (customTo) {
        const b = readBase("bn-to-custom", "Otra base");
        rows.push([`Base ${b}`, toBase(value, b).toUpperCase()]);
      }
      $("bn-rows").innerHTML = rows
        .map(([k, v]) => `<div class="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 border-b border-[var(--color-border)] py-2 last:border-0"><span class="text-sm text-[var(--color-text-muted)]">${k}</span><span class="font-numeric font-bold break-all">${v}</span></div>`)
        .join("");

      // Desarrollo: divisiones sucesivas por 2 para valores chicos
      const abs = value < 0n ? -value : value;
      if (abs > 0n && abs <= 65535n) {
        const st = divisionSteps(value, 2);
        $("bn-steps").innerHTML =
          `<p class="font-semibold text-[var(--color-text)] mb-1">Desarrollo a binario (divisiones sucesivas por 2)</p><ol class="list-decimal list-inside space-y-1 font-numeric">` +
          st.map((s) => `<li>${s.dividend} ÷ 2 = ${s.quotient}, resto <strong>${s.remainder}</strong></li>`).join("") +
          `</ol><p class="mt-2">Se leen los restos de abajo hacia arriba: <strong class="font-numeric">${toBase(abs, 2)}</strong>.</p>`;
      } else {
        $("bn-steps").innerHTML = "";
      }
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  $("bn-from").addEventListener("change", syncCustom);
  $("bn-solve").addEventListener("click", calculate);
  document.querySelectorAll("input").forEach((el) => el.addEventListener("keydown", (e) => e.key === "Enter" && calculate()));
  document.querySelectorAll("[data-example]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const [v, base] = btn.dataset.example.split("|");
      $("bn-from").value = base;
      syncCustom();
      $("bn-input").value = v;
      calculate();
    })
  );
  syncCustom();
})();
