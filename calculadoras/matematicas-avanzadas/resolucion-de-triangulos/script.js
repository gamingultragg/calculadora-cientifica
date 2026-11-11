/**
 * Resolución de triángulos con los teoremas del coseno y del seno.
 * Casos: LLL (tres lados), LAL (dos lados y el ángulo comprendido) y ALA (dos ángulos y el lado comprendido).
 */
(function () {
  const rad = (d) => (d * Math.PI) / 180;
  const deg = (r) => (r * 180) / Math.PI;
  const clamp = (x) => Math.max(-1, Math.min(1, x));

  function finish(a, b, c, A, B, C) {
    const s = (a + b + c) / 2;
    return { a, b, c, A, B, C, perimeter: a + b + c, area: Math.sqrt(Math.max(0, s * (s - a) * (s - b) * (s - c))) };
  }

  function fromSSS(a, b, c) {
    if (!(a + b > c && a + c > b && b + c > a)) throw new Error("Esos lados no forman un triángulo: cada lado tiene que ser menor que la suma de los otros dos.");
    const A = deg(Math.acos(clamp((b * b + c * c - a * a) / (2 * b * c))));
    const B = deg(Math.acos(clamp((a * a + c * c - b * b) / (2 * a * c))));
    return finish(a, b, c, A, B, 180 - A - B);
  }

  // lados a, b y el ángulo C (en grados) comprendido entre ellos
  function fromSAS(a, b, Cdeg) {
    if (!(Cdeg > 0 && Cdeg < 180)) throw new Error("El ángulo tiene que estar entre 0° y 180°.");
    const c = Math.sqrt(a * a + b * b - 2 * a * b * Math.cos(rad(Cdeg)));
    const A = deg(Math.acos(clamp((b * b + c * c - a * a) / (2 * b * c))));
    return finish(a, b, c, A, 180 - A - Cdeg, Cdeg);
  }

  // ángulos A y B y el lado c comprendido entre ellos
  function fromASA(Adeg, Bdeg, c) {
    if (!(Adeg > 0 && Bdeg > 0 && Adeg + Bdeg < 180)) throw new Error("Los dos ángulos tienen que sumar menos de 180°.");
    const C = 180 - Adeg - Bdeg;
    const a = (c * Math.sin(rad(Adeg))) / Math.sin(rad(C));
    const b = (c * Math.sin(rad(Bdeg))) / Math.sin(rad(C));
    return finish(a, b, c, Adeg, Bdeg, C);
  }

  if (typeof module !== "undefined") module.exports = { fromSSS, fromSAS, fromASA };
  if (typeof document === "undefined" || !window.CCSimple || !document.getElementById("tg-solve")) return;

  CCSimple.mount({
    prefix: "tg",
    compute(v, h) {
      const r = v.mode === "sss" ? fromSSS(v.a, v.b, v.c) : v.mode === "sas" ? fromSAS(v.a, v.b, v.C) : fromASA(v.A, v.B, v.c);
      const f = (x) => h.fmt(x, 4);
      const kind = r.a === r.b && r.b === r.c ? "equilátero" : r.a === r.b || r.b === r.c || r.a === r.c ? "isósceles" : "escaleno";
      const angles = [r.A, r.B, r.C];
      const type = angles.some((x) => Math.abs(x - 90) < 1e-9) ? "rectángulo" : angles.some((x) => x > 90) ? "obtusángulo" : "acutángulo";
      return {
        label: "Triángulo resuelto", main: `Área = ${f(r.area)}`,
        lines: [`Lados: a = <strong>${f(r.a)}</strong> · b = <strong>${f(r.b)}</strong> · c = <strong>${f(r.c)}</strong>`, `Ángulos: A = <strong>${f(r.A)}°</strong> · B = <strong>${f(r.B)}°</strong> · C = <strong>${f(r.C)}°</strong>`, `Perímetro: ${f(r.perimeter)} · Es un triángulo ${kind} y ${type}.`],
      };
    },
  });
})();
