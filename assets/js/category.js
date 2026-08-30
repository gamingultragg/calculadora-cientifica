/**
 * category.js — Render de las tarjetas de calculadoras en una landing page
 * de categoría (ej. /calculadoras/estadistica/). Lee la categoría desde
 * `data-category` en <body> y filtra CC_CALCULATORS (calculators-data.js).
 */
(function () {
  const grid = document.getElementById("cat-grid");
  if (!grid) return;

  const categoryKey = document.body.dataset.category;
  const calcs = CC_CALCULATORS.filter((c) => c.category === categoryKey);

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
    const a = document.createElement("a");
    a.href = calc.url;
    a.className =
      "surface block rounded-2xl p-5 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-150";
    a.innerHTML = `
      <span class="badge ${badgeClass}">${cat.label}</span>
      <h3 class="mt-3 font-display font-semibold text-lg text-[var(--color-text)]">${calc.title}</h3>
      <p class="mt-1.5 text-sm text-[var(--color-text-muted)] leading-relaxed">${calc.description}</p>
      <span class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-[var(--color-primary)]">
        Abrir calculadora
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
      </span>
    `;
    return a;
  }

  calcs
    .filter((c) => c.status === "live")
    .forEach((calc) => grid.appendChild(cardTemplate(calc)));
})();
