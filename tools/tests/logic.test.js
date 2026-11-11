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
