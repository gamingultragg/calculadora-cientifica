/**
 * Amortización de Préstamos — sistema francés (cuota fija): calcula la
 * cuota periódica, el total pagado y el interés total.
 */
(function () {
  // Convierte un input numérico en formato es-AR ("15.000" con punto de
  // miles, "1.234,56" con punto de miles y coma decimal, o un número
  // simple como "9.8") al formato que entiende Number(). Un punto seguido
  // de 1, 2 o más de 3 dígitos se interpreta como separador decimal (no
  // de miles), evitando falsos positivos como "3.14" o "0.5".
  function normalizeNumberInput(value) {
    let str = String(value).trim();
    if (str.includes(",")) {
      str = str.replace(/\./g, "").replace(",", ".");
    } else if (/^-?[1-9]\d{0,2}(\.\d{3})+$/.test(str)) {
      str = str.replace(/\./g, "");
    }
    return str;
  }

  const form = document.getElementById("am-form");
  const errorEl = document.getElementById("am-error");
  const resultPanel = document.getElementById("am-result-panel");
  const stepsEl = document.getElementById("am-steps");

  const out = {
    cuota: document.getElementById("am-cuota"),
    total: document.getElementById("am-total"),
    interes: document.getElementById("am-interes"),
  };

  const fmtMoney = (n) =>
    new Intl.NumberFormat("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(
      Object.is(n, -0) ? 0 : Math.round(n * 100) / 100
    );
  const fmt0 = (n) => new Intl.NumberFormat("es-AR", { maximumFractionDigits: 4 }).format(n);

  function showError(message) {
    errorEl.textContent = message;
    errorEl.classList.remove("hidden");
    resultPanel.classList.add("hidden");
  }
  function clearError() {
    errorEl.classList.add("hidden");
    errorEl.textContent = "";
  }
  function addStep(html) {
    const li = document.createElement("li");
    li.innerHTML = html;
    stepsEl.appendChild(li);
  }

  function parsePositive(id, label) {
    const el = document.getElementById(id);
    el.classList.remove("field-error");
    const raw = normalizeNumberInput(el.value);
    if (raw === "") {
      el.classList.add("field-error");
      throw new Error(`El campo "${label}" no puede estar vacío.`);
    }
    const value = Number(raw);
    if (!Number.isFinite(value) || value <= 0) {
      el.classList.add("field-error");
      throw new Error(`El campo "${label}" debe ser un número mayor a 0.`);
    }
    return value;
  }

  // Tabla de amortización: interés = saldo × i; capital = cuota − interés; la última cuota cierra el saldo en 0.
  const TABLE_MAX_ROWS = 600;
  function renderTable(principal, i, cuota, N) {
    const body = document.getElementById("am-table");
    const note = document.getElementById("am-table-note");
    body.textContent = "";
    let balance = principal;
    const shown = Math.min(N, TABLE_MAX_ROWS);
    for (let k = 1; k <= shown; k++) {
      const interest = balance * i;
      const capital = k === N ? balance : cuota - interest;
      balance = Math.max(0, balance - capital);
      const tr = document.createElement("tr");
      tr.className = "border-t border-[var(--color-border)]";
      [k, fmtMoney(k === N ? interest + capital : cuota), fmtMoney(interest), fmtMoney(capital), fmtMoney(balance)].forEach((v, idx) => {
        const td = document.createElement("td");
        td.className = "px-2 py-1.5" + (idx === 0 ? " text-left" : "");
        td.textContent = v;
        tr.appendChild(td);
      });
      body.appendChild(tr);
    }
    note.textContent = N > shown ? `Se muestran las primeras ${shown} de ${N} cuotas.` : "";
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    clearError();
    document.querySelectorAll("#am-form input").forEach((input) => input.classList.remove("field-error"));

    try {
      const principal = parsePositive("am-principal", "Monto del préstamo");
      const ratePercent = normalizeNumberInput(document.getElementById("am-rate").value);
      const rateEl = document.getElementById("am-rate");
      rateEl.classList.remove("field-error");
      if (ratePercent === "") {
        rateEl.classList.add("field-error");
        throw new Error('El campo "Tasa de interés" no puede estar vacío.');
      }
      const rate = Number(ratePercent);
      if (!Number.isFinite(rate) || rate < 0) {
        rateEl.classList.add("field-error");
        throw new Error('El campo "Tasa de interés" debe ser un número mayor o igual a 0.');
      }
      const years = parsePositive("am-years", "Plazo (años)");
      const n = Number(document.getElementById("am-frequency").value);

      const i = rate / 100 / n;
      const N = Math.round(n * years);

      let cuota;
      if (i === 0) {
        cuota = principal / N;
      } else {
        cuota = (principal * i) / (1 - Math.pow(1 + i, -N));
      }
      const total = cuota * N;
      const interes = total - principal;

      stepsEl.innerHTML = "";
      addStep(`<strong>Datos:</strong> P = ${fmtMoney(principal)} · i = ${fmt0(i * 100)}% por período · N = ${N} cuotas`);
      addStep(`<strong>Fórmula:</strong> Cuota = P × i / (1 − (1 + i)^−N)`);
      addStep(`Cuota = ${fmtMoney(principal)} × ${fmt0(i)} / (1 − (1 + ${fmt0(i)})^−${N}) = <strong class="text-[var(--color-primary)]">${fmtMoney(cuota)}</strong>`);
      addStep(`Total pagado = ${fmtMoney(cuota)} × ${N} = <strong class="text-[var(--color-primary)]">${fmtMoney(total)}</strong>`);
      addStep(`Interés total = ${fmtMoney(total)} − ${fmtMoney(principal)} = <strong class="text-[var(--color-danger)]">${fmtMoney(interes)}</strong>`);

      renderTable(principal, i, cuota, N);

      out.cuota.textContent = fmtMoney(cuota);
      out.total.textContent = fmtMoney(total);
      out.interes.textContent = fmtMoney(interes);
      resultPanel.classList.remove("hidden");
    } catch (err) {
      showError(err.message);
    }
  });
})();
