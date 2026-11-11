"""Genera scripts/register-batch-N.py a partir de register-batch-6.py con otras listas (CALCS, GUIDES, CARDS).
Uso: python mk_register_generic.py N spec.json
spec.json: {"calcs": [[id, title, cat, desc, [kw], url]...], "cards": [[slug, label, title, text]...],
            "badges": {"label": "classes"}, "enrich": {"slug-categoria": ["slug-guia", ...]} }
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\santi\Documents\Software\calculadora-cientifica")
n = sys.argv[1]
spec = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
s = (ROOT / "scripts/register-batch-6.py").read_text(encoding="utf-8")

a = s.index("CALCS = [")
b = s.index("data = ROOT")
calcs = "CALCS = [\n"
for id_, title, cat, desc, kw, url in spec["calcs"]:
    calcs += f"    dict(id={id_!r}, title={title!r}, cat={cat!r},\n         desc={desc!r},\n         kw={kw!r},\n         url={url!r}),\n"
calcs += "]\n\n"
s = s[:a] + calcs + s[b:]
guides = [c[0] for c in spec["cards"]]
s = re.sub(r"GUIDES = \[.*?\]\n", "GUIDES = " + repr(guides) + "\n", s, count=1, flags=re.S)
for label, cls in spec.get("badges", {}).items():
    if f'"{label}":' not in s:
        s = s.replace('    "Hogar y Construcción": "bg-cyan-100 text-cyan-700 dark:bg-cyan-500/15 dark:text-cyan-300",\n}', '    "Hogar y Construcción": "bg-cyan-100 text-cyan-700 dark:bg-cyan-500/15 dark:text-cyan-300",\n    %r: %r,\n}' % (label, cls), 1)
a = s.index("CARDS = [")
b = s.index("ARROW = ")
s = s[:a] + "CARDS = [\n" + "".join(f"    {tuple(c)!r},\n" for c in spec["cards"]) + "]\n" + s[b:]
s = s.replace("register-batch-6.py — Registra el lote 6 (Finanzas + categoría Hogar y Construcción)", f"register-batch-{n}.py — Registra el lote {n}")
(ROOT / f"scripts/register-batch-{n}.py").write_text(s, encoding="utf-8")

# guías nuevas en las páginas de categoría
e = ROOT / "scripts/enrich-categories.py"
t = e.read_text(encoding="utf-8")
for cat, new_guides in spec.get("enrich", {}).items():
    m = re.search(r'("' + re.escape(cat) + r'": dict\(.*?guides=\[)(.*?)(\]\))', t, re.S)
    assert m, cat
    cur = re.findall(r'"([^"]+)"', m.group(2))
    allg = cur + [g for g in new_guides if g not in cur]
    t = t[: m.start(2)] + ", ".join(f'"{g}"' for g in allg) + t[m.end(2):]
e.write_text(t, encoding="utf-8")
print("register-batch-%s generado; guías por categoría actualizadas" % n)
