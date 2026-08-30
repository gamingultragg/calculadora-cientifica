/**
 * Calculadora de pH y pOH — calcula pH, pOH, [H+] y [OH-] a partir de
 * cualquiera de los cuatro valores, con clasificación ácido/neutro/base.
 */
(function () {
  const modeSelect = document.getElementById("ph-mode");
  const valueLabel = document.getElementById("ph-value-label");
  const valueInput = document.getElementById("ph-value");
  const errorEl = document.getElementById("ph-error");
  const resultPanel = document.getElementById("ph-result-panel");

  const out = {
    ph: document.getElementById("ph-out-ph"),
    poh: document.getElementById("ph-out-poh"),
    h: document.getElementById("ph-out-h"),
    oh: document.getElementById("ph-out-oh"),
    cls: document.getElementById("ph-out-class"),
  };

  const fmt = (n) =>
    new Intl.NumberFormat("es-AR", { maximumFractionDigits: 6 }).format(
      Object.is(n, -0) ? 0 : Math.round(n * 1e10) / 1e10
    );
  const fmtSci = (n) => n.toExponential(4).replace(".", ",");

  const labels = {
    h: "Concentración de H⁺ (mol/L)",
    oh: "Concentración de OH⁻ (mol/L)",
    ph: "Valor de pH",
    poh: "Valor de pOH",
  };

  modeSelect.addEventListener("change", () => {
    valueLabel.textContent = labels[modeSelect.value];
    valueInput.value = "";
    clearError();
    resultPanel.classList.add("hidden");
  });

  function showError(message) {
    errorEl.textContent = message;
    errorEl.classList.remove("hidden");
    resultPanel.classList.add("hidden");
    valueInput.classList.add("field-error");
  }
  function clearError() {
    errorEl.classList.add("hidden");
    errorEl.textContent = "";
    valueInput.classList.remove("field-error");
  }

  function classify(ph) {
    if (Math.abs(ph - 7) < 1e-9) return "Neutro";
    return ph < 7 ? "Ácido" : "Básico (alcalino)";
  }

  document.getElementById("ph-solve").addEventListener("click", () => {
    clearError();
    const raw = valueInput.value.trim().replace(",", ".");
    if (raw === "") {
      showError("Ingresá un valor antes de calcular.");
      return;
    }
    const value = Number(raw);
    if (!Number.isFinite(value)) {
      showError("El valor ingresado no es un número válido.");
      return;
    }

    const mode = modeSelect.value;
    if ((mode === "h" || mode === "oh") && value <= 0) {
      showError("La concentración debe ser un número mayor a 0 (el logaritmo no está definido para valores ≤ 0).");
      return;
    }

    let ph, poh, hConc, ohConc;

    if (mode === "h") {
      hConc = value;
      ph = -Math.log10(hConc);
      poh = 14 - ph;
      ohConc = Math.pow(10, -poh);
    } else if (mode === "oh") {
      ohConc = value;
      poh = -Math.log10(ohConc);
      ph = 14 - poh;
      hConc = Math.pow(10, -ph);
    } else if (mode === "ph") {
      ph = value;
      poh = 14 - ph;
      hConc = Math.pow(10, -ph);
      ohConc = Math.pow(10, -poh);
    } else {
      poh = value;
      ph = 14 - poh;
      ohConc = Math.pow(10, -poh);
      hConc = Math.pow(10, -ph);
    }

    out.ph.textContent = fmt(ph);
    out.poh.textContent = fmt(poh);
    out.h.textContent = fmtSci(hConc);
    out.oh.textContent = fmtSci(ohConc);
    out.cls.textContent = classify(ph);
    resultPanel.classList.remove("hidden");
  });
})();
