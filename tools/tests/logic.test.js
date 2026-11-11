/**
 * Pruebas de la lógica pura de las calculadoras (sin navegador ni dependencias).
 * Uso:  node --test tools/tests/
 * Cada script.js exporta su lógica con `module.exports` cuando se carga desde Node.
 */
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");

const load = (rel) => require(path.join(__dirname, "..", "..", "calculadoras", rel, "script.js"));
const near = (a, b, tol = 1e-6) => assert.ok(Math.abs(a - b) <= tol, `${a} no está cerca de ${b} (tol ${tol})`);

test("MCD y MCM", () => {
  const m = load("matematicas-avanzadas/mcd-y-mcm");
  const r = m.compute(m.parseNumbers("48 180 24"));
  assert.equal(r.gcd, 12n);
  assert.equal(r.lcm, 720n);
  assert.deepEqual(m.compute(m.parseNumbers("17 5")), { gcd: 1n, lcm: 85n });
  assert.throws(() => m.parseNumbers("12"));
  assert.throws(() => m.parseNumbers("12 0"));
});

test("Regla de tres", () => {
  const r = load("matematicas-avanzadas/regla-de-tres");
  assert.equal(r.simple("directa", 2, 10, 5), 25);
  assert.equal(r.simple("inversa", 4, 6, 3), 8);
  assert.equal(r.compound(10, [{ v1: 2, v2: 4, dir: "directa" }, { v1: 5, v2: 10, dir: "inversa" }]), 10);
  assert.throws(() => r.simple("directa", 0, 1, 1));
});

test("Promedio de notas", () => {
  const p = load("estadistica/calculadora-de-promedio-de-notas");
  near(p.average([{ nota: 6, peso: 1 }, { nota: 8, peso: 1 }], false).average, 7);
  near(p.average([{ nota: 6, peso: 30 }, { nota: 9, peso: 70 }], true).average, 8.1);
  // para llegar a 7 con 6 y 8 y un 50% restante
  near(p.needed([{ nota: 6, peso: 25 }, { nota: 8, peso: 25 }], true, 7, 50), 7);
});

test("Masa molar", () => {
  const m = load("quimica/calculadora-de-masa-molar");
  near(m.molarMass("H2O").total, 18.015, 0.01);
  near(m.molarMass("H2SO4").total, 98.08, 0.01);
  near(m.molarMass("Fe2(SO4)3").total, 399.87, 0.02);
  assert.throws(() => m.molarMass("Xx2"));
});

test("Interés simple", () => {
  const s = load("finanzas/calculadora-de-interes-simple");
  near(s.interest(100000, 0.24, 0.5), 12000);
  near(s.capitalFromInterest(12000, 0.24, 0.5), 100000);
  near(s.rateFromInterest(100000, 12000, 0.5), 0.24);
  near(s.timeFromInterest(100000, 12000, 0.24), 0.5);
  assert.throws(() => s.capitalFromInterest(1, 0, 1));
});

test("Fracciones", () => {
  const f = load("matematicas-avanzadas/calculadora-de-fracciones");
  const P = f.parseFraction;
  const s = (x) => f.fracStr(f.simplify(x));
  assert.equal(s(f.add(P("1/2"), P("1/3"))), "5/6");
  assert.equal(s(f.sub(P("3/4"), P("5/6"))), "-1/12");
  assert.equal(s(f.mul(P("2/3"), P("9/4"))), "3/2");
  assert.equal(s(f.div(P("1 1/2"), P("3/4"))), "2");
  assert.equal(s(P("0,75")), "3/4");
  assert.equal(s(P("6/-8")), "-3/4");
  assert.equal(f.toDecimal(P("7/8")).text, "0,875");
  assert.equal(f.toDecimal(P("1/3")).exact, false);
  assert.throws(() => f.div(P("1/2"), P("0")));
  assert.throws(() => P("1/0"));
  assert.throws(() => P("abc"));
});

test("Teorema de Pitágoras", () => {
  const p = load("matematicas-avanzadas/teorema-de-pitagoras");
  const r = p.solve("c", 3, 4);
  near(r.c, 5);
  near(r.area, 6);
  near(r.perimeter, 12);
  near(r.height, 2.4);
  near(r.angleA + r.angleB, 90);
  near(p.solve("a", 13, 5).a, 12);
  near(p.solve("b", 5, 3).b, 4);
  assert.throws(() => p.solve("a", 3, 5));
});

test("Aguinaldo", () => {
  const a = load("finanzas/calculadora-de-aguinaldo");
  const full = a.aguinaldo(1000000, a.sacFraction("completo", 0), 17);
  near(full.gross, 500000);
  near(full.net, 415000);
  near(a.aguinaldo(1200000, a.sacFraction("meses", 3), 17).gross, 300000);
  near(a.aguinaldo(900000, a.sacFraction("dias", 90), 0).gross, 225000);
  near(a.sacFraction("meses", 9), 1);
});

test("Gases ideales", () => {
  const g = load("quimica/calculadora-de-gases-ideales");
  near(g.volume(1, 1, 273.15), 22.414, 1e-3);
  near(g.pressure(1, 22.414, 273.15), 1, 1e-3);
  near(g.moles(1, 22.414, 273.15), 1, 1e-3);
  near(g.temperature(1, 22.414, 1), 273.15, 0.01);
  near(g.fromKelvin(298.15, "c"), 25);
});

test("Bases numéricas", () => {
  const b = load("matematicas-avanzadas/conversor-de-bases-numericas");
  assert.equal(b.toBase(b.parseInBase("255", 10), 2), "11111111");
  assert.equal(b.toBase(b.parseInBase("0xFF", 16), 8), "377");
  assert.equal(b.toBase(b.parseInBase("-1010", 2), 16), "-a");
  assert.equal(b.toBase(b.parseInBase("zz", 36), 10), "1295");
  assert.equal(b.toBase(b.parseInBase("2024", 10), 16), "7e8");
  assert.throws(() => b.parseInBase("12", 2));
});

test("Moles", () => {
  const m = load("quimica/calculadora-de-moles");
  near(m.molesFromMass(49, 98.08), 0.4996, 1e-3);
  near(m.massFromMoles(0.5, 98.08), 49.04, 1e-6);
  near(m.molesFromMolarity(0.1, 0.25), 0.025);
  near(m.molesFromParticles(6.02214076e23), 1);
  near(m.molesFromGas(22.414), 1);
  assert.throws(() => m.molesFromMass(1, 0));
});

test("Plazo fijo y tasas", () => {
  const f = load("finanzas/calculadora-de-plazo-fijo");
  const r = f.plazoFijo(1000000, 0.4, 30);
  near(r.interest, 32876.71, 0.01);
  near(r.final, 1032876.71, 0.01);
  near(f.tnaToTea(0.4, 30), 0.48226, 1e-4);
  near(f.teaToTna(f.tnaToTea(0.4, 30), 30), 0.4, 1e-9);
});

test("Áreas y volúmenes", () => {
  const g = load("matematicas-avanzadas/calculadora-de-areas-y-volumenes");
  near(g.compute("circulo", [2]).area, 12.566370614, 1e-6);
  near(g.compute("rectangulo", [3, 4]).diagonal, 5);
  near(g.compute("triangulo-lados", [3, 4, 5]).area, 6);
  near(g.compute("cilindro", [1, 2]).volumen, 6.283185307, 1e-6);
  near(g.compute("esfera", [3]).volumen, 113.097335529, 1e-6);
  near(g.compute("cono", [3, 4]).generatriz, 5);
  near(g.compute("cubo", [2]).superficie, 24);
  near(g.compute("piramide", [6, 4]).volumen, 48);
  assert.throws(() => g.compute("triangulo-lados", [1, 2, 10]));
  assert.throws(() => g.compute("cubo", [0]));
});

test("Energía cinética y potencial", () => {
  const e = load("fisica/energia-cinetica-y-potencial");
  near(e.kinetic(2, 3), 9);
  near(e.massFromKinetic(9, 3), 2);
  near(e.speedFromKinetic(9, 2), 3);
  near(e.potential(10, 9.81, 5), 490.5);
  near(e.massFromPotential(490.5, 9.81, 5), 10);
  near(e.heightFromPotential(490.5, 10, 9.81), 5);
  assert.throws(() => e.speedFromKinetic(5, 0));
});

test("Regresión lineal", () => {
  const r = load("estadistica/regresion-lineal");
  const { xs, ys } = r.parsePairs("1 2\n2 4\n3 6\n4 8");
  const res = r.regress(xs, ys);
  near(res.slope, 2);
  near(res.intercept, 0);
  near(res.r, 1);
  const d = r.parsePairs("1 2;2 3;3 5;4 4;5 6".replace(/;/g, "\n"));
  const res2 = r.regress(d.xs, d.ys);
  near(res2.slope, 0.9);
  near(res2.intercept, 1.3);
  near(res2.r2, 0.81, 1e-9);
  assert.deepEqual(r.parsePairs("1,5 2,5\n3 4").xs, [1.5, 3]);
  assert.throws(() => r.regress([2, 2, 2], [1, 2, 3]));
  assert.throws(() => r.parsePairs("1 2"));
  assert.throws(() => r.parsePairs("1 2 3\n4 5"));
});

test("Conversor de temperatura", () => {
  const t = load("ingenieria/conversor-de-temperatura");
  const a = t.convert(100, "c");
  near(a.f, 212);
  near(a.k, 373.15);
  near(a.r, 671.67, 1e-2);
  near(t.convert(32, "f").c, 0);
  near(t.convert(-40, "c").f, -40);
  near(t.convert(0, "k").c, -273.15);
  assert.throws(() => t.convert(-300, "c"));
});
