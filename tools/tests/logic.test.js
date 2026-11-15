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

test("Edad y fechas", () => {
  const f = load("vida-diaria/calculadora-de-edad-y-fechas");
  const P = f.parseISO;
  const d1 = f.dateDiff(P("2024-01-31"), P("2024-03-01"));
  assert.deepEqual([d1.years, d1.months, d1.days, d1.totalDays], [0, 1, 1, 30]);
  const d2 = f.dateDiff(P("2000-02-29"), P("2026-11-10"));
  assert.equal(d2.years, 26);
  assert.equal(f.dateDiff(P("2026-01-01"), P("2026-12-31")).totalDays, 364);
  assert.equal(f.dateDiff(P("2026-11-02"), P("2026-11-09")).weekdays, 5); // lunes a lunes
  assert.equal(f.dateDiff(P("2026-12-31"), P("2026-01-01")).swapped, true);
  const a = f.ageInfo(P("1990-05-15"), P("2026-11-10"));
  assert.deepEqual([a.years, a.months, a.days], [36, 5, 26]);
  assert.equal(a.nextBirthday.y, 2027);
  assert.equal(a.daysToBirthday, 186);
  assert.equal(f.ageInfo(P("1990-11-10"), P("2026-11-10")).daysToBirthday, 0);
  assert.equal(f.ageInfo(P("2000-02-29"), P("2026-11-10")).nextBirthday.d, 28);
  assert.deepEqual(f.addToDate(P("2026-01-31"), 1, "meses"), { y: 2026, m: 2, d: 28 });
  assert.deepEqual(f.addToDate(P("2026-11-10"), 90, "dias"), { y: 2027, m: 2, d: 8 });
  assert.deepEqual(f.addToDate(P("2026-03-31"), -1, "meses"), { y: 2026, m: 2, d: 28 });
  assert.deepEqual(f.addToDate(P("2024-02-29"), 1, "anios"), { y: 2025, m: 2, d: 28 });
  assert.equal(f.weekdayName(P("2026-11-10")), "martes");
  assert.throws(() => P("2026-02-30"));
  assert.throws(() => f.ageInfo(P("2030-01-01"), P("2026-11-10")));
});

test("IMC", () => {
  const i = load("vida-diaria/calculadora-de-imc");
  near(i.bmi(70, 1.75), 22.857, 1e-3);
  assert.equal(i.category(22.9), "Peso normal");
  assert.equal(i.category(18.4), "Bajo peso");
  assert.equal(i.category(25), "Sobrepeso");
  assert.equal(i.category(31), "Obesidad grado I");
  assert.equal(i.category(45), "Obesidad grado III");
  near(i.toKg(154.32, "lb"), 70, 0.01);
  near(i.toMeters(175, "cm"), 1.75);
  const r = i.healthyRange(1.75);
  near(r.min, 56.66, 0.01);
  near(r.max, 76.26, 0.01);
});

test("Conversor de cocina", () => {
  const c = load("vida-diaria/conversor-de-cocina");
  near(c.toMl(1, "taza", 240, 1), 240);
  near(c.toMl(2, "cda", 240, 1), 30);
  near(c.toMl(200, "g", 240, c.INGREDIENTS.azucar.density), 238.1, 0.1);
  const all = c.allUnits(240, 240, c.INGREDIENTS.harina.density);
  near(all.cda, 16);
  near(all.taza, 1);
  near(all.g, 127.2, 0.1);
  near(c.toMl(1, "kg", 240, 1), 1000);
});

test("Horas trabajadas", () => {
  const h = load("vida-diaria/calculadora-de-horas-trabajadas");
  assert.equal(h.parseTime("08:30"), 510);
  assert.equal(h.workedMinutes(h.parseTime("09:00"), h.parseTime("18:00"), 60), 480);
  assert.equal(h.workedMinutes(h.parseTime("22:00"), h.parseTime("06:00"), 0), 480); // cruza medianoche
  assert.equal(h.hhmm(495), "8:15");
  const r = h.summarize({ perDayMin: 600, days: 5, normalHours: 8, rate: 1000, surchargePct: 50 });
  near(r.totalDecimal, 50);
  near(r.regularMin, 2400);
  near(r.extraMin, 600);
  near(r.pay, 40 * 1000 + 10 * 1000 * 1.5);
  assert.throws(() => h.parseTime("25:00"));
  assert.throws(() => h.workedMinutes(0, 60, 120));
});

test("Propina y división de cuenta", () => {
  const p = load("vida-diaria/calculadora-de-propina");
  const r = p.split(10000, 10, 4, 0);
  near(r.tip, 1000);
  near(r.total, 11000);
  near(r.perPerson, 2750);
  const q = p.split(10000, 10, 3, 100);
  near(q.perPerson, 3700);
  near(q.collected, 11100);
  near(q.extra, 100);
  near(p.split(5000, 0, 1, 0).perPerson, 5000);
  assert.throws(() => p.split(100, 10, 0, 0));
});

test("Cuotas vs contado", () => {
  const c = load("finanzas/cuotas-vs-contado");
  // 6 cuotas de 20.000 para un precio de contado de 100.000: tasa implícita ≈ 5,47 % mensual
  const i = c.implicitRate(100000, 20000, 6);
  near(c.presentValue(20000, 6, i), 100000, 0.01);
  near(i, 0.0547, 1e-3);
  near(c.implicitRate(120000, 10000, 12), 0, 1e-6);
  assert.ok(c.implicitRate(100000, 8000, 12) < 0);
  assert.throws(() => c.implicitRate(100000, 1000, 6));
  near(c.presentValue(1000, 3, 0), 3000);
});

test("Inflación acumulada", () => {
  const f = load("finanzas/calculadora-de-inflacion-acumulada");
  const r = f.accumulate(f.parseRates("10 10"));
  near(r.cumulative, 0.21);
  near(r.monthlyGeo, 0.1, 1e-12);
  near(f.accumulate([2, 3, 4]).cumulative, 1.02 * 1.03 * 1.04 - 1, 1e-12);
  assert.deepEqual(f.parseRates("4,2 3.5;2%"), [4.2, 3.5, 2]);
  assert.throws(() => f.parseRates("abc"));
  assert.throws(() => f.parseRates(""));
});

test("Ajuste de alquiler", () => {
  const a = load("finanzas/calculadora-de-ajuste-de-alquiler");
  near(a.byIndex(100000, 1.5, 1.8), 120000);
  near(a.byPercent(100000, 25), 125000);
});

test("Margen y markup", () => {
  const m = load("finanzas/calculadora-de-margen-y-markup");
  near(m.priceFromMargin(60, 40), 100);
  near(m.priceFromMarkup(60, 50), 90);
  const r = m.fromPrices(60, 100);
  near(r.margin, 0.4);
  near(r.markup, 2 / 3, 1e-12);
  assert.throws(() => m.priceFromMargin(60, 100));
});

test("Descuentos sucesivos", () => {
  const d = load("finanzas/descuentos-sucesivos");
  const r = d.sequential(1000, d.parseDiscounts("20 10 5"));
  near(r.final, 684);
  near(r.totalPct, 0.316);
  near(r.sumPct, 0.35);
  assert.throws(() => d.parseDiscounts("100"));
  assert.throws(() => d.parseDiscounts("x"));
});

test("Cerámicos", () => {
  const c = load("hogar-y-construccion/calculadora-de-ceramicos");
  const t = c.tiles(20, 60, 60, 10);
  assert.equal(t.pieces, 62);
  near(t.buyArea, 62 * 0.36, 1e-9);
  assert.equal(c.tiles(10, 30, 30, 0).pieces, 112);
});

test("Pintura", () => {
  const p = load("hogar-y-construccion/calculadora-de-pintura");
  const a = p.paintArea(4, 3, 2.6, 3, true);
  near(a.walls, 2 * 7 * 2.6 - 3);
  near(a.ceilingArea, 12);
  near(p.liters(50, 2, 10), 10);
  const c = p.cans(9);
  assert.ok(c.total >= 9 && c.total <= 10);
  assert.deepEqual([p.cans(20).c20, p.cans(20).total], [1, 20]);
});

test("Ladrillos", () => {
  const l = load("hogar-y-construccion/calculadora-de-ladrillos");
  near(l.perM2(33, 18, 1.5), 10000 / (34.5 * 19.5), 1e-9);
  const r = l.bricks(10, 33, 18, 1.5, 5);
  assert.equal(r.total, Math.ceil(10 * 10000 / (34.5 * 19.5) * 1.05 - 1e-9));
});

test("Hormigón", () => {
  const h = load("hogar-y-construccion/calculadora-de-hormigon");
  near(h.volumeSlab(5, 4, 12), 2.4);
  near(h.volumeColumns(25, 25, 3, 4), 0.75);
  const m = h.materials(2, "H17");
  near(m.cementKg, 660);
  assert.equal(m.bags, 14);
  near(m.sand, 1.04);
});

test("Consumo eléctrico", () => {
  const c = load("hogar-y-construccion/calculadora-de-consumo-electrico");
  near(c.dailyKwh(1500, 2, 1), 3);
  near(c.dailyKwh(60, 5, 4), 1.2);
});

test("Sistemas de ecuaciones", () => {
  const s = load("matematicas-avanzadas/sistemas-de-ecuaciones");
  const r = s.solve2(2, 1, 5, 1, -1, 1);
  near(r.x, 2);
  near(r.y, 1);
  assert.equal(s.solve2(1, 2, 3, 2, 4, 6).det, 0);
  const t = s.solve3([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3]);
  near(t.x, 2);
  near(t.y, 3);
  near(t.z, -1);
  assert.equal(s.solve3([[1, 2, 3], [2, 4, 6], [1, 0, 1]], [1, 2, 3]).det, 0);
});

test("Números primos", () => {
  const p = load("matematicas-avanzadas/numeros-primos");
  assert.equal(p.isPrime(2), true);
  assert.equal(p.isPrime(97), true);
  assert.equal(p.isPrime(1), false);
  assert.equal(p.isPrime(100), false);
  assert.equal(p.isPrime(999999999989), true);
  assert.deepEqual([...p.factorize(360)], [[2, 3], [3, 2], [5, 1]]);
  assert.equal(p.divisorCount(p.factorize(360)), 24);
  assert.equal(p.nextPrime(100), 101);
  assert.equal(p.prevPrime(100), 97);
  assert.equal(p.prevPrime(2), null);
});

test("Progresiones", () => {
  const p = load("matematicas-avanzadas/progresiones-aritmeticas-y-geometricas");
  const a = p.arithmetic(3, 4, 10);
  near(a.an, 39);
  near(a.sn, 210);
  const g = p.geometric(2, 3, 5);
  near(g.an, 162);
  near(g.sn, 242);
  near(p.geometric(1, 0.5, 10).infinite, 2);
  assert.equal(p.geometric(5, 1, 4).sn, 20);
  assert.equal(p.geometric(1, 2, 3).infinite, null);
});

test("Resolución de triángulos", () => {
  const t = load("matematicas-avanzadas/resolucion-de-triangulos");
  const r = t.fromSSS(3, 4, 5);
  near(r.C, 90, 1e-9);
  near(r.area, 6);
  near(r.A + r.B + r.C, 180, 1e-9);
  const s = t.fromSAS(5, 7, 60);
  near(s.c, Math.sqrt(25 + 49 - 35), 1e-9);
  const a = t.fromASA(40, 60, 10);
  near(a.C, 80);
  near(a.a, 10 * Math.sin(40 * Math.PI / 180) / Math.sin(80 * Math.PI / 180), 1e-9);
  assert.throws(() => t.fromSSS(1, 2, 10));
  assert.throws(() => t.fromASA(100, 90, 5));
});

test("Números romanos", () => {
  const r = load("matematicas-avanzadas/conversor-de-numeros-romanos");
  assert.equal(r.toRoman(1994), "MCMXCIV");
  assert.equal(r.toRoman(3999), "MMMCMXCIX");
  assert.equal(r.toRoman(4), "IV");
  assert.equal(r.fromRoman("MCMXCIV"), 1994);
  assert.equal(r.fromRoman("xiv"), 14);
  assert.throws(() => r.fromRoman("IIII"));
  assert.throws(() => r.fromRoman("VX"));
  assert.throws(() => r.toRoman(0));
  assert.throws(() => r.toRoman(4000));
});

test("Distribución binomial", () => {
  const b = load("estadistica/distribucion-binomial");
  near(b.pmf(10, 0.5, 5), 0.24609375, 1e-9);
  const r = b.binomial(10, 0.5, 5);
  near(r.cdf, 0.623046875, 1e-9);
  near(r.ge, 0.623046875, 1e-9);
  near(r.mean, 5);
  near(r.sd, Math.sqrt(2.5), 1e-12);
  near(b.binomial(20, 0.3, 6).exact, 0.19163898, 1e-7);
  near(b.pmf(5, 0, 0), 1);
  near(b.pmf(5, 1, 5), 1);
  const big = b.binomial(1000, 0.5, 500);
  near(big.exact, 0.0252250181, 1e-8);
});

test("Intervalo de confianza", () => {
  const i = load("estadistica/intervalo-de-confianza");
  assert.equal(i.critical(95, 10, true).value, 2.262);
  assert.equal(i.critical(95, 50, true).value, 1.96);
  assert.equal(i.critical(99, 8, false).value, 2.576);
  const r = i.interval(50, 10, 100, 95, false);
  near(r.margin, 1.96, 1e-9);
  near(r.lower, 48.04, 1e-9);
  near(r.upper, 51.96, 1e-9);
  assert.throws(() => i.critical(80, 10, false));
});

test("Tamaño de muestra", () => {
  const t = load("estadistica/tamano-de-muestra");
  assert.equal(t.sampleSize(95, 5, 50, 0).n, 385);
  assert.equal(t.sampleSize(95, 5, 50, 1000).n, 278);
  assert.equal(t.sampleSize(99, 3, 50, 0).n, 1844);
  assert.equal(t.sampleSize(90, 10, 50, 0).n, 68);
});

test("Caída libre y tiro oblicuo", () => {
  const c = load("fisica/caida-libre-y-tiro-oblicuo");
  const f = c.freeFall(5, 9.81);
  near(f.time, Math.sqrt(10 / 9.81), 1e-12);
  near(f.speed, 9.81 * f.time, 1e-12);
  const p = c.projectile(20, 45, 0, 9.81);
  near(p.range, (20 * 20) / 9.81, 1e-9); // sen(90°) = 1
  near(p.maxHeight, (20 * Math.sin(Math.PI / 4)) ** 2 / (2 * 9.81), 1e-9);
  near(p.impactSpeed, 20, 1e-9);
  const q = c.projectile(10, 0, 20, 9.81); // lanzamiento horizontal desde 20 m
  near(q.time, Math.sqrt(40 / 9.81), 1e-9);
  near(q.range, 10 * q.time, 1e-9);
});

test("Trabajo y potencia", () => {
  const t = load("fisica/trabajo-y-potencia");
  near(t.work(100, 5, 0), 500);
  near(t.work(100, 5, 60), 250, 1e-9);
  near(t.work(100, 5, 90), 0, 1e-9);
  near(t.work(50, 2, 180), -100, 1e-9);
  near(t.power(500, 10), 50);
});

test("Estequiometría y reactivo limitante", () => {
  const s = load("quimica/estequiometria-y-reactivo-limitante");
  // N2 + 3 H2 -> 2 NH3: 28 g de N2 (28 g/mol) -> 2 mol de NH3 = 34,06 g
  const p = s.product(28, 28, 1, 2, 17.03, 100);
  near(p.nB, 2);
  near(p.theoretical, 34.06, 1e-9);
  near(s.product(28, 28, 1, 2, 17.03, 50).actual, 17.03, 1e-9);
  // 10 g de H2 y 28 g de N2: H2 = 4,96 mol (extent 1,65) ; N2 = 1 mol (extent 1) -> limita N2
  const l = s.limiting({ mass: 28, molar: 28, coef: 1 }, { mass: 10, molar: 2.016, coef: 3 }, { coef: 2, molar: 17.03 });
  assert.equal(l.limiting, "A");
  near(l.nP, 2, 1e-9);
  assert.equal(l.excessName, "B");
  near(l.excessMoles, 10 / 2.016 - 3, 1e-9);
});

test("Balanceo de ecuaciones químicas", () => {
  const b = load("quimica/balanceo-de-ecuaciones-quimicas");
  assert.deepEqual(b.balance("H2 + O2 -> H2O").coeffs, [2, 1, 2]);
  assert.deepEqual(b.balance("C3H8 + O2 -> CO2 + H2O").coeffs, [1, 5, 3, 4]);
  assert.deepEqual(b.balance("Fe + O2 -> Fe2O3").coeffs, [4, 3, 2]);
  assert.deepEqual(b.balance("Ca(OH)2 + H3PO4 -> Ca3(PO4)2 + H2O").coeffs, [3, 2, 1, 6]);
  assert.deepEqual(b.balance("KMnO4 + HCl -> KCl + MnCl2 + H2O + Cl2").coeffs, [2, 16, 2, 2, 8, 5]);
  assert.equal(b.format(b.balance("H2 + O2 -> H2O")), "2 H₂ + O₂ → 2 H₂O");
  assert.deepEqual([...b.parseFormula("CuSO4·5H2O")], [["Cu", 1], ["S", 1], ["O", 9], ["H", 10]]);
  assert.throws(() => b.balance("H2 -> O2"));
  assert.throws(() => b.balance("sin flecha"));
  assert.throws(() => b.parseFormula("h2o"));
});

test("Código de colores de resistencias", () => {
  const r = load("ingenieria/codigo-de-colores-de-resistencias");
  const a = r.resistorValue(["marron", "negro"], "rojo", "dorado"); // 10 × 100 = 1 kΩ ±5 %
  near(a.ohms, 1000);
  near(a.min, 950);
  near(a.max, 1050);
  near(r.resistorValue(["amarillo", "violeta"], "naranja", "dorado").ohms, 47000);
  near(r.resistorValue(["rojo", "rojo", "negro"], "marron", "marron").ohms, 2200);
  near(r.resistorValue(["verde", "azul"], "dorado", "plateado").ohms, 5.6, 1e-9);
  assert.equal(r.format(4700), "4,7 kΩ");
  assert.equal(r.format(2200000), "2,2 MΩ");
  assert.equal(r.format(330), "330 Ω");
});

test("Divisor de tensión", () => {
  const d = load("ingenieria/divisor-de-tension");
  near(d.vout(12, 1000, 2000), 8);
  near(d.r2For(12, 8, 1000), 2000);
  assert.throws(() => d.r2For(5, 6, 1000));
});

test("Resistencia para LED", () => {
  const l = load("ingenieria/resistencia-para-led");
  const r = l.ledResistor(5, 2, 20);
  near(r.r, 150);
  near(r.power, 0.06);
  assert.equal(l.nextE12(150), 150);
  assert.equal(l.nextE12(160), 180);
  assert.equal(l.nextE12(1000), 1000);
  assert.equal(l.nextE12(1900), 2200);
  assert.equal(l.nextE12(9000), 10000);
  assert.throws(() => l.ledResistor(1.5, 2, 20));
});

test("Graficador: analizador de expresiones", () => {
  const g = load("matematicas-avanzadas/graficador-de-funciones");
  const f = (src, x) => g.compile(src)(x);
  near(f("x^2-4", 3), 5);
  near(f("2x+1", 4), 9);
  near(f("-x^2", 3), -9);
  near(f("2^-1", 0), 0.5);
  near(f("(x+1)(x-1)", 3), 8);
  near(f("sen(pi/2)", 0), 1);
  near(f("sin(x)^2+cos(x)^2", 1.3), 1, 1e-12);
  near(f("sqrt(x)+abs(-2)", 9), 5);
  near(f("ln(e)", 0), 1);
  near(f("log(1000)", 0), 3);
  near(f("log2(8)", 0), 3);
  near(f("2sen(x)", Math.PI / 2), 2, 1e-12);
  near(f("x(x+1)", 3), 12);
  near(f("1,5x", 2), 3);
  near(f("3 * 4 / 2", 0), 6);
  near(f("2^3^2", 0), 512);
  assert.equal(f("1/x", 0), Infinity);
  assert.throws(() => g.compile("x+"));
  assert.throws(() => g.compile("(x+1"));
  assert.throws(() => g.compile("foo(x)"));
  assert.throws(() => g.compile("sin x"));
  assert.throws(() => g.compile("x $ 2"));
  assert.throws(() => g.compile(""));
});

test("Graficador: ceros", () => {
  const g = load("matematicas-avanzadas/graficador-de-funciones");
  const z = g.zeros(g.compile("x^2-4"), -10, 10);
  assert.equal(z.length, 2);
  near(z[0], -2, 1e-6);
  near(z[1], 2, 1e-6);
  const s = g.zeros(g.compile("sin(x)"), 0, 10);
  assert.equal(s.length, 4); // 0, π, 2π, 3π
  near(s[1], Math.PI, 1e-6);
  assert.equal(g.zeros(g.compile("x^2+1"), -10, 10).length, 0);
  assert.equal(g.zeros(g.compile("1/x"), -10, 10).length, 0);
});

test("Calorías y metabolismo basal", () => {
  const c = load("vida-diaria/calculadora-de-calorias-y-metabolismo-basal");
  near(c.bmr("hombre", 70, 175, 30), 1648.75);
  near(c.bmr("mujer", 60, 165, 30), 1320.25);
  near(c.maintenance(1648.75, "moderado"), 2555.5625, 1e-9);
  near(c.maintenance(1000, "sedentario"), 1200);
});

// ---------------------------------------------------------------- Lote 10 (2026-11-14)
test("Recta y distancia entre dos puntos", () => {
  const { line } = load("matematicas-avanzadas/recta-y-distancia-entre-puntos");
  const r = line(1, 2, 3, 6);
  assert.equal(r.slope, 2);
  assert.equal(r.b, 0);
  near(r.distance, Math.sqrt(20));
  assert.deepEqual(r.mid, [2, 4]);
  near(r.incl, 63.434948822922);
  assert.deepEqual([r.A, r.B, r.C], [4, -2, 0]);
  const neg = line(0, 4, 2, 0);
  assert.equal(neg.slope, -2);
  assert.equal(neg.b, 4);
  near(neg.incl, 116.565051177078);
  const vert = line(2, 1, 2, 5);
  assert.equal(vert.vertical, true);
  assert.equal(vert.distance, 4);
  assert.equal(vert.incl, 90);
  const hor = line(1, 3, 5, 3);
  assert.equal(hor.slope, 0);
  assert.equal(hor.b, 3);
  assert.equal(hor.incl, 0);
  assert.throws(() => line(1, 1, 1, 1));
  // la forma general pasa por los dos puntos
  const g = line(-3, 7, 4, -2);
  assert.equal(g.A * -3 + g.B * 7 + g.C, 0);
  assert.equal(g.A * 4 + g.B * -2 + g.C, 0);
});

test("Logaritmos", () => {
  const { logBase, power } = load("matematicas-avanzadas/calculadora-de-logaritmos");
  near(logBase(2, 8), 3);
  near(logBase(10, 1000), 3);
  near(logBase(3, 81), 4);
  near(logBase(Math.E, Math.E), 1);
  near(logBase(5, 1), 0);
  near(logBase(0.5, 8), -3);
  assert.throws(() => logBase(1, 5));
  assert.throws(() => logBase(2, 0));
  assert.throws(() => logBase(2, -4));
  assert.throws(() => logBase(-2, 4));
  assert.equal(power(2, 10), 1024);
  near(power(10, -2), 0.01);
  near(logBase(7, power(7, 3.5)), 3.5);
});

test("Densidad", () => {
  const d = load("fisica/calculadora-de-densidad");
  near(d.density(500 * d.MASS.g, 250 * d.VOL.cm3), 2000); // 500 g en 250 cm³ = 2 g/cm³
  near(d.mass(7.87 * d.DENS.gcm3, 100 * d.VOL.cm3), 0.787);
  near(d.volume(1, 1000), 1e-3); // 1 kg de agua = 1 L
  near(d.volume(2.7 * d.MASS.kg, 2.7 * d.DENS.gcm3) * 1000, 1); // aluminio: 2,7 kg ocupan 1 L
});

test("Calor específico y calorimetría", () => {
  const c = load("fisica/calculadora-de-calor-especifico");
  near(c.heat(1000, 4.186, 60), 251160);
  near(c.heat(1000, 4.186, 60) / c.CAL, 60028.7, 0.1); // calorías
  near(c.specificHeat(251160, 1000, 60), 4.186);
  near(c.mass(251160, 4.186, 60), 1000);
  near(c.deltaT(251160, 1000, 4.186), 60);
  near(c.heat(200, 0.385, -50), -3850); // el cobre que se enfría cede calor
  assert.throws(() => c.specificHeat(100, 10, 0));
  assert.throws(() => c.mass(100, 4, 0));
});

test("Movimiento circular uniforme", () => {
  const { circular } = load("fisica/calculadora-de-movimiento-circular");
  const a = circular(0.5, "T", 2);
  near(a.omega, Math.PI);
  near(a.f, 0.5);
  near(a.rpm, 30);
  near(a.v, Math.PI * 0.5);
  near(a.a, Math.PI * Math.PI * 0.5);
  const b = circular(2, "rpm", 60);
  near(b.f, 1);
  near(b.T, 1);
  near(b.omega, 2 * Math.PI);
  near(b.v, 4 * Math.PI);
  near(b.a, 8 * Math.PI * Math.PI);
  const c = circular(1, "v", 10);
  near(c.omega, 10);
  near(c.a, 100); // v²/r
  near(circular(3, "w", 2).v, 6);
  near(circular(3, "f", 2).omega, 4 * Math.PI);
});

test("Leyes de los gases", () => {
  const g = load("quimica/leyes-de-los-gases");
  near(g.solveP2(1, 10, 300, 5, 300), 2); // Boyle: se comprime a la mitad, la presión se duplica
  near(g.solveV2(1, 10, 300, 2, 300), 5);
  near(g.solveV2(1, 10, 300, 1, 600), 20); // Charles: al duplicar T, se duplica V
  near(g.solveP2(2, 5, 300, 5, 450), 3); // Gay-Lussac: mismo V, T × 1,5 → P × 1,5
  near(g.solveT2(1, 10, 300, 2, 5), 300);
  near(g.toKelvin(27, "C"), 300.15);
  near(g.fromKelvin(373.15, "C"), 100);
  assert.throws(() => g.toKelvin(-300, "C"));
  assert.throws(() => g.toKelvin(0, "K"));
  assert.match(g.lawName(1, 10, 300, 2, 5, 300), /Boyle/);
  assert.match(g.lawName(1, 10, 300, 1, 20, 600), /Charles/);
  assert.match(g.lawName(2, 5, 300, 3, 5, 450), /Gay-Lussac/);
  assert.match(g.lawName(1, 10, 300, 2, 8, 500), /combinada/);
});

test("Concentración en ppm y porcentaje", () => {
  const c = load("quimica/calculadora-de-concentracion-ppm");
  const r = c.concentration(5 * c.MG.g, 2); // 5 g en 2 L
  near(r.mgL, 2500);
  near(r.gL, 2.5);
  near(r.pctMV, 0.25);
  const p = c.fromPpm(1000);
  near(p.gL, 1);
  near(p.pctMV, 0.1);
  near(c.fromPpm(50).pctMV, 0.005);
  near(c.massNeeded(50, 20), 1000); // 50 ppm en 20 L = 1 g
  near(c.concentration(250 * c.MG.mg, 500 * c.LITERS.mL).mgL, 500); // 250 mg en 500 mL
});

test("Consumo de combustible", () => {
  const f = load("vida-diaria/calculadora-de-consumo-de-combustible");
  const e = f.efficiency(450, 36);
  near(e.kmL, 12.5);
  near(e.l100, 8);
  near(f.tripLiters(300, 8), 24);
  near(f.range(50, 8), 625);
  near(f.efficiency(100, 10).l100, 10);
});

// ---------------------------------------------------------------- Lote 11 (2026-11-14)
test("Notación científica", () => {
  const n = load("matematicas-avanzadas/calculadora-de-notacion-cientifica");
  assert.equal(n.formatSci(n.toScientific("123,45")), "1,2345 × 10²");
  assert.equal(n.formatSci(n.toScientific("0,00045")), "4,5 × 10⁻⁴");
  assert.equal(n.formatEng(n.toScientific("0,00045")), "450 × 10⁻⁶");
  assert.equal(n.formatSci(n.toScientific("300000")), "3 × 10⁵");
  assert.equal(n.formatEng(n.toScientific("300000")), "300 × 10³");
  assert.equal(n.formatSci(n.toScientific("-6,02")), "−6,02 × 10⁰");
  assert.equal(n.formatSci(n.toScientific("1.234.567")), "1,234567 × 10⁶"); // punto de miles
  assert.equal(n.formatSci(n.toScientific("0.00045")), "4,5 × 10⁻⁴"); // punto decimal
  assert.equal(n.formatSci(n.toScientific("0")), "0");
  assert.equal(n.toDecimal("6,02", 23), "602.000.000.000.000.000.000.000");
  assert.equal(n.toDecimal("1,6", -19), "0,00000000000000000016");
  assert.equal(n.toDecimal("2,5", 3), "2.500");
  assert.equal(n.toDecimal("-3,2", -2), "−0,032");
  assert.equal(n.toDecimal("4,5", 0), "4,5");
  assert.equal(n.toDecimal("0", 5), "0");
  assert.throws(() => n.toDecimal("1", 400));
  assert.throws(() => n.parseDecimal("abc"));
  const m = n.operate("3", 8, "*", "2", -3);
  assert.equal(n.formatSci(m.sci), "6 × 10⁵");
  assert.equal(m.decimal, "600.000");
  assert.equal(n.formatSci(n.operate("5", 3, "+", "2", 3).sci), "7 × 10³");
  assert.equal(n.formatSci(n.operate("1,1", 0, "+", "2,2", 0).sci), "3,3 × 10⁰"); // sin ruido de coma flotante
  assert.equal(n.formatSci(n.operate("1", 0, "/", "3", 0).sci), "3,33333333333 × 10⁻¹");
  assert.equal(n.formatSci(n.operate("2", 3, "-", "5", 3).sci), "−3 × 10³");
  assert.throws(() => n.operate("1", 0, "/", "0", 0));
});

test("Potencias y raíces", () => {
  const p = load("matematicas-avanzadas/calculadora-de-potencias-y-raices");
  assert.equal(p.power(2, 10), 1024);
  assert.equal(p.power(2, -2), 0.25);
  assert.equal(p.power(-2, 3), -8);
  near(p.power(9, 0.5), 3);
  assert.throws(() => p.power(0, -1));
  assert.throws(() => p.power(-8, 1 / 3));
  assert.equal(p.root(27, 3), 3);
  assert.equal(p.root(-27, 3), -3);
  assert.equal(p.root(16, 4), 2);
  near(p.root(2, 2), 1.4142135623731);
  assert.throws(() => p.root(-4, 2));
  assert.throws(() => p.root(4, 1));
  assert.deepEqual(p.simplify(72, 2), { out: 6, inside: 2 });
  assert.deepEqual(p.simplify(50, 2), { out: 5, inside: 2 });
  assert.deepEqual(p.simplify(16, 2), { out: 4, inside: 1 });
  assert.deepEqual(p.simplify(54, 3), { out: 3, inside: 2 });
  assert.deepEqual(p.simplify(7, 2), { out: 1, inside: 7 });
  assert.deepEqual(p.simplify(49, 2), { out: 7, inside: 1 });
  assert.deepEqual(p.simplify(1, 2), { out: 1, inside: 1 });
  assert.equal(p.simplify(0.5, 2), null);
  // out^n · inside = x
  const s = p.simplify(1000000007 * 4, 2);
  assert.equal(s.out * s.out * s.inside, 1000000007 * 4);
});

test("Probabilidad básica", () => {
  const p = load("estadistica/calculadora-de-probabilidad");
  const a = p.simple(1, 6);
  near(a.p, 1 / 6);
  near(a.complement, 5 / 6);
  near(a.oneIn, 6);
  assert.equal(p.simple(0, 10).oneIn, Infinity);
  assert.throws(() => p.simple(7, 5));
  assert.throws(() => p.simple(1, 0));
  const t = p.twoEvents(0.5, 0.3);
  near(t.and, 0.15);
  near(t.or, 0.65);
  near(t.none, 0.35);
  near(t.exactlyOne, 0.5);
  near(t.onlyA, 0.35);
  near(t.orExclusive, 0.8);
  near(t.or + t.none, 1);
  const r = p.atLeastOne(0.5, 3);
  near(r.none, 0.125);
  near(r.atLeast, 0.875);
  near(r.expected, 1.5);
  near(p.atLeastOne(1 / 6, 4).atLeast, 1 - Math.pow(5 / 6, 4));
});

test("Péndulo simple", () => {
  const d = load("fisica/calculadora-de-pendulo-simple");
  near(d.period(1, 9.81), 2.0061, 1e-3);
  near(d.period(0.25, 9.81), 1.00304, 1e-3); // un cuarto de longitud, la mitad del período
  near(d.length(2, 9.81), 0.99397, 1e-4);
  near(d.gravity(1, 2), (4 * Math.PI * Math.PI) / 4);
  near(d.gravity(d.length(1.5, 9.8), 1.5), 9.8, 1e-9);
  near(d.amplitudeFactor(0), 1);
  near(d.amplitudeFactor((30 * Math.PI) / 180), 1.0174, 1e-4);
});

test("Ley de Coulomb", () => {
  const c = load("fisica/calculadora-de-ley-de-coulomb");
  near(c.force(1e-6, 1e-6, 0.1), 0.898755, 1e-6);
  assert.ok(c.force(1e-6, -1e-6, 0.1) < 0); // atractiva
  near(c.force(1.602176634e-19, -1.602176634e-19, 5.29177e-11), -8.2387e-8, 5e-12); // electrón y protón en el hidrógeno
  near(c.force(2e-6, 2e-6, 0.2) / c.force(1e-6, 1e-6, 0.1), 1); // duplicar cargas y distancia: (4)/(4) = 1
  near(c.distance(0.898755, 1e-6, 1e-6), 0.1, 1e-6);
  near(c.charge2(0.898755, 1e-6, 0.1), 1e-6, 1e-12);
  near(3 * c.CHARGE.uC, 3e-6);
  near(50 * c.DIST.cm, 0.5);
});

test("Presión", () => {
  const p = load("fisica/calculadora-de-presion");
  near(p.pressure(100, 0.5), 200);
  near(p.pressure(50, 25 * p.AREA.cm2), 20000);
  near(p.hydrostatic(1000, 9.81, 10), 98100);
  near(p.ATM * p.UNITS.atm, 1);
  near(p.ATM * p.UNITS.bar, 1.01325);
  near(p.ATM * p.UNITS.mmHg, 760, 1e-3);
  near(p.ATM * p.UNITS.psi, 14.6959, 1e-3);
  near((p.hydrostatic(1000, 9.81, 10) + p.ATM) * p.UNITS.atm, 1.968, 1e-3); // 10 m bajo el agua
});

test("Escaleras", () => {
  const { stairs } = load("hogar-y-construccion/calculadora-de-escaleras");
  const a = stairs(270, 17.5);
  assert.equal(a.n, 15);
  near(a.riser, 18);
  near(a.tread, 27);
  near(a.run, 378);
  near(a.blondel, 63);
  near(a.angle, 33.690067, 1e-5);
  near(a.stringer, Math.sqrt(270 * 270 + 378 * 378));
  const b = stairs(280, 17);
  assert.equal(b.n, 16);
  near(b.riser, 17.5);
  near(b.tread, 28);
  near(b.run, 420);
  const c = stairs(250, 18, 30); // huella propia
  assert.equal(c.n, 14);
  near(c.tread, 30);
  near(c.blondel, 2 * (250 / 14) + 30);
  assert.equal(stairs(10, 17.5).n, 2); // mínimo
});

test("Meta de ahorro", () => {
  const s = load("finanzas/calculadora-de-meta-de-ahorro");
  near(s.contribution(120000, 0, 0, 12), 10000);
  near(s.contribution(100000, 20000, 0, 10), 8000);
  near(s.futureValue(0, 1000, 0, 12), 12000);
  const A = s.contribution(1000000, 0, 0.03, 24);
  near(s.futureValue(0, A, 0.03, 24), 1000000, 1e-6);
  near(s.months(1000000, 0, A, 0.03), 24, 1e-9);
  const B = s.contribution(500000, 100000, 0.02, 36);
  near(s.futureValue(100000, B, 0.02, 36), 500000, 1e-6);
  near(s.months(500000, 100000, B, 0.02), 36, 1e-9);
  near(s.months(120000, 0, 10000, 0), 12);
  assert.ok(A < 1000000 / 24); // con interés se aporta menos que sin interés
  assert.throws(() => s.contribution(1000, 1000, 0, 5));
  assert.throws(() => s.months(1000, 1500, 10, 0));
  assert.throws(() => s.contribution(110000, 100000, 0.05, 120));
});
