/**
 * Densidad — ρ = m / V, con despeje de la masa (m = ρ·V) y del volumen (V = m / ρ).
 * Todo se convierte a unidades del SI (kg, m³, kg/m³) y se muestra en las unidades de uso común.
 */
(function () {
  const MASS = { kg: 1, g: 1e-3, mg: 1e-6 };
  const VOL = { m3: 1, L: 1e-3, mL: 1e-6, cm3: 1e-6 };
  const DENS = { kgm3: 1, gcm3: 1000 };
  const density = (massKg, volM3) => massKg / volM3;
  const mass = (dens, volM3) => dens * volM3;
  const volume = (massKg, dens) => massKg / dens;

  if (typeof module !== "undefined") module.exports = { MASS, VOL, DENS, density, mass, volume };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("dn-solve")) return;

  CCSimple.mount({
    prefix: "dn",
    compute(v, h) {
      const f = (x, d = 4) => h.fmt(x, d);
      let m = v.m !== undefined ? v.m * MASS[v.mu] : undefined; // kg
      let vol = v.v !== undefined ? v.v * VOL[v.vu] : undefined; // m³
      let d = v.d !== undefined ? v.d * DENS[v.du] : undefined; // kg/m³
      let main;
      let label;
      if (v.mode === "dens") {
        d = density(m, vol);
        label = "Densidad";
        main = `${f(d / 1000)} g/cm³`;
      } else if (v.mode === "masa") {
        m = mass(d, vol);
        label = "Masa";
        main = m >= 1 ? `${f(m)} kg` : `${f(m * 1000)} g`;
      } else {
        vol = volume(m, d);
        label = "Volumen";
        main = vol >= 1e-3 ? `${f(vol * 1000)} L` : `${f(vol * 1e6)} cm³`;
      }
      const water = Math.abs(d - 1000) < 1e-9 * 1000 ? "Es igual a la del agua (1 g/cm³): queda en equilibrio." : d < 1000 ? "Es menor que la del agua (1 g/cm³): <strong>flota</strong>." : "Es mayor que la del agua (1 g/cm³): <strong>se hunde</strong>.";
      const lines = [
        `Densidad: ${f(d)} kg/m³ = ${f(d / 1000)} g/cm³ = ${f(d / 1000)} kg/L.`,
        `Masa: ${f(m)} kg = ${f(m * 1000)} g.`,
        `Volumen: ${f(vol * 1000)} L = ${f(vol * 1e6)} cm³ (mL) = ${f(vol, 6)} m³.`,
        water,
      ];
      return { label, main, lines };
    },
  });
})();
