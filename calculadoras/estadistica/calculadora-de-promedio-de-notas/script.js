/**
 * Calculadora de Promedio de Notas — promedio simple o ponderado (cada nota con su
 * peso) y "¿qué nota necesito?" para llegar a un promedio objetivo.
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

  // rows: [{ nota, peso }]. Si weighted es false, todas pesan 1.
  function average(rows, weighted) {
    if (!rows.length) throw new Error("Ingresá al menos una nota.");
    let sumW = 0;
    let sumNW = 0;
    rows.forEach((r) => {
      const w = weighted ? r.peso : 1;
      sumW += w;
      sumNW += r.nota * w;
    });
    if (!(sumW > 0)) throw new Error("La suma de los pesos tiene que ser mayor a 0.");
    return { average: sumNW / sumW, sumWeights: sumW, count: rows.length };
  }

  // Nota que falta para llegar a "target", con peso restante "remaining" (en las mismas
  // unidades que los pesos de las notas ya cargadas).
  function needed(rows, weighted, target, remaining) {
    if (!(remaining > 0)) throw new Error("El peso de la nota que falta tiene que ser mayor a 0.");
    let sumW = 0;
    let sumNW = 0;
    rows.forEach((r) => {
      const w = weighted ? r.peso : 1;
      sumW += w;
      sumNW += r.nota * w;
    });
    return (target * (sumW + remaining) - sumNW) / remaining;
  }

  if (typeof module !== "undefined") module.exports = { average, needed };
  if (typeof document === "undefined" || !document.getElementById("pn-rows")) return;

  // ------------------------------------------------------------------ UI --
  const $ = (id) => document.getElementById(id);
  const errorEl = $("err");
  const panel = $("pn-result-panel");
  const rowsEl = $("pn-rows");
  const weightedEl = $("pn-weighted");
  const fmt = (n, d = 2) =>
    new Intl.NumberFormat("es-AR", { maximumFractionDigits: d }).format(Math.round((n + 1e-9) * 10 ** d) / 10 ** d);

  function addRow(nota = "", peso = "") {
    const div = document.createElement("div");
    div.className = "pn-row grid grid-cols-[1fr_1fr_auto] gap-2 items-end";
    div.innerHTML = `
      <div>
        <label class="block text-xs font-medium mb-1 text-[var(--color-text-muted)]">Nota</label>
        <input type="text" inputmode="decimal" placeholder="Ej: 7,5" value="${nota}" data-f="nota"
          class="w-full rounded-xl surface px-3 py-2.5 font-numeric focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]" />
      </div>
      <div class="pn-peso">
        <label class="block text-xs font-medium mb-1 text-[var(--color-text-muted)]">Peso (%)</label>
        <input type="text" inputmode="decimal" placeholder="Ej: 30" value="${peso}" data-f="peso"
          class="w-full rounded-xl surface px-3 py-2.5 font-numeric focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]" />
      </div>
      <button type="button" aria-label="Quitar esta nota" class="pn-del w-10 h-10 rounded-xl surface hover:shadow-md text-[var(--color-text-muted)]">✕</button>`;
    div.querySelector(".pn-del").addEventListener("click", () => {
      if (rowsEl.children.length > 1) div.remove();
      else div.querySelectorAll("input").forEach((i) => (i.value = ""));
    });
    rowsEl.appendChild(div);
    syncWeighted();
  }

  function syncWeighted() {
    const on = weightedEl.checked;
    document.querySelectorAll(".pn-peso").forEach((el) => el.classList.toggle("hidden", !on));
    $("pn-remaining-wrap").classList.toggle("hidden", !on);
  }

  function num(raw, label) {
    const s = normalizeNumberInput(raw);
    if (s === "") throw new Error(`Completá "${label}".`);
    const v = Number(s);
    if (!Number.isFinite(v) || v < 0) throw new Error(`"${label}" tiene que ser un número mayor o igual a 0.`);
    return v;
  }

  function readRows() {
    const weighted = weightedEl.checked;
    const rows = [];
    [...rowsEl.children].forEach((div, i) => {
      const nota = div.querySelector('[data-f="nota"]').value;
      const peso = div.querySelector('[data-f="peso"]').value;
      if (nota.trim() === "" && (!weighted || peso.trim() === "")) return; // fila vacía
      rows.push({ nota: num(nota, `Nota ${i + 1}`), peso: weighted ? num(peso, `Peso de la nota ${i + 1}`) : 1 });
    });
    return { rows, weighted };
  }

  function calculate() {
    errorEl.classList.add("hidden");
    try {
      const { rows, weighted } = readRows();
      const res = average(rows, weighted);
      $("pn-average").textContent = fmt(res.average);
      let detail = `Promedio de ${res.count} ${res.count === 1 ? "nota" : "notas"}${weighted ? " ponderado" : ""}.`;
      if (weighted) {
        detail += ` Los pesos suman ${fmt(res.sumWeights)}${
          Math.abs(res.sumWeights - 100) > 1e-9 ? " (no llegan a 100%: se calcula igual sobre ese total)" : "%"
        }.`;
      }
      $("pn-detail").textContent = detail;

      // ¿Qué nota necesito?
      const targetRaw = $("pn-target").value.trim();
      const needEl = $("pn-need");
      if (targetRaw !== "") {
        const target = num(targetRaw, "Promedio que querés lograr");
        const remaining = weighted ? num($("pn-remaining").value, "Peso de la nota que falta") : 1;
        const need = needed(rows, weighted, target, remaining);
        const maxRaw = normalizeNumberInput($("pn-max").value);
        const max = maxRaw === "" ? null : Number(maxRaw);
        let msg = `Para llegar a ${fmt(target)} necesitás sacar <strong>${fmt(need)}</strong> en la nota que falta.`;
        if (need < 0) msg = `Ya llegás a ${fmt(target)} aunque saques 0 en la nota que falta.`;
        else if (max !== null && Number.isFinite(max) && need > max)
          msg += ` Es más que la nota máxima (${fmt(max)}): con esa nota no alcanza para llegar a ${fmt(target)}.`;
        needEl.innerHTML = msg;
        needEl.classList.remove("hidden");
      } else {
        needEl.classList.add("hidden");
      }
      panel.classList.remove("hidden");
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
      panel.classList.add("hidden");
    }
  }

  weightedEl.addEventListener("change", syncWeighted);
  $("pn-add").addEventListener("click", () => addRow());
  $("pn-solve").addEventListener("click", calculate);
  addRow();
  addRow();
  addRow();
  syncWeighted();
})();
