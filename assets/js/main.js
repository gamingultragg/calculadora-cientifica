/**
 * main.js — Lógica del Dashboard: render de tarjetas, buscador instantáneo
 * y filtro por categoría. Depende de CC_CALCULATORS / CC_CATEGORIES
 * definidos en calculators-data.js (cargado antes que este script).
 */
(function () {
  const grid = document.getElementById("calc-grid");
  const searchInput = document.getElementById("calc-search");
  const emptyState = document.getElementById("calc-empty");
  const resultCount = document.getElementById("calc-result-count");
  const categoryButtons = document.querySelectorAll("[data-category-filter]");

  let activeCategory = "all";

  const categoryColorClasses = {
    blue: "bg-blue-100 text-blue-700 dark:bg-blue-500/15 dark:text-blue-300",
    violet: "bg-violet-100 text-violet-700 dark:bg-violet-500/15 dark:text-violet-300",
    orange: "bg-orange-100 text-orange-700 dark:bg-orange-500/15 dark:text-orange-300",
    green: "bg-green-100 text-green-700 dark:bg-green-500/15 dark:text-green-300",
    amber: "bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300",
    teal: "bg-teal-100 text-teal-700 dark:bg-teal-500/15 dark:text-teal-300",
  };

  function cardTemplate(calc) {
    const cat = CC_CATEGORIES[calc.category];
    const badgeClass = categoryColorClasses[cat.color];
    const isLive = calc.status === "live";

    const inner = `
      <div class="flex items-start justify-between gap-3">
        <span class="badge ${badgeClass}">${cat.label}</span>
        ${
          isLive
            ? ""
            : '<span class="badge bg-slate-100 text-slate-500 dark:bg-slate-700 dark:text-slate-300">Próximamente</span>'
        }
      </div>
      <h3 class="mt-3 font-display font-semibold text-lg text-[var(--color-text)]">${calc.title}</h3>
      <p class="mt-1.5 text-sm text-[var(--color-text-muted)] leading-relaxed">${calc.description}</p>
      <span class="mt-4 inline-flex items-center gap-1 text-sm font-semibold ${
        isLive ? "text-[var(--color-primary)]" : "text-[var(--color-text-muted)]"
      }">
        ${isLive ? "Abrir calculadora" : "Aviso pronto"}
        ${isLive ? '<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>' : ""}
      </span>
    `;

    if (isLive) {
      const a = document.createElement("a");
      a.href = calc.url;
      a.className =
        "surface block rounded-2xl p-5 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-150";
      a.innerHTML = inner;
      return a;
    }
    const div = document.createElement("div");
    div.className = "surface block rounded-2xl p-5 opacity-70 cursor-not-allowed";
    div.innerHTML = inner;
    return div;
  }

  function normalize(str) {
    return str
      .toLowerCase()
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "");
  }

  // Orden de categorías para agrupar la vista "Todas" (si no, las tarjetas
  // quedan mezcladas en el orden en que se fueron agregando al catálogo).
  const categoryOrder = Object.keys(CC_CATEGORIES);

  function render() {
    const query = normalize(searchInput.value.trim());

    const filtered = CC_CALCULATORS.filter((calc) => {
      const matchesCategory = activeCategory === "all" || calc.category === activeCategory;
      if (!matchesCategory) return false;
      if (!query) return true;
      const haystack = normalize(
        [calc.title, calc.description, CC_CATEGORIES[calc.category].label, ...(calc.keywords || [])].join(" ")
      );
      return haystack.includes(query);
    });

    filtered.sort((a, b) => categoryOrder.indexOf(a.category) - categoryOrder.indexOf(b.category));

    grid.innerHTML = "";
    filtered.forEach((calc) => grid.appendChild(cardTemplate(calc)));

    emptyState.classList.toggle("hidden", filtered.length > 0);
    resultCount.textContent = `${filtered.length} ${filtered.length === 1 ? "resultado" : "resultados"}`;
  }

  searchInput.addEventListener("input", render);

  categoryButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      activeCategory = btn.dataset.categoryFilter;
      categoryButtons.forEach((b) => {
        const isActive = b === btn;
        b.classList.toggle("bg-[var(--color-primary)]", isActive);
        b.classList.toggle("text-white", isActive);
        b.classList.toggle("border-transparent", isActive);
        b.classList.toggle("surface", !isActive);
      });
      render();
    });
  });

  render();
})();
