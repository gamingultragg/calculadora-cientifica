"""
spec_lib.py — Piezas para generar calculadoras del motor común (assets/js/calc-simple.js).
Uso: L = Lib("cv"); L.num("precio", "Precio ($)", "Ej: 100000"); L.form([...], chips=[...]); L.panel()
Los atributos data-* que deja en el HTML son los que lee calc-simple.js.
"""
from pathlib import Path

from page_templates import calc_page, guide_page  # noqa: F401  (re-export)

ROOT = Path(__file__).resolve().parent.parent
INPUT = ('class="w-full rounded-xl surface px-3 py-2.5 font-numeric focus:outline-none '
         'focus:ring-2 focus:ring-[var(--color-primary)]"')
SELECT = ('class="w-full rounded-xl surface px-3 py-2.5 focus:outline-none '
          'focus:ring-2 focus:ring-[var(--color-primary)]"')
BTN = 'class="calc-btn calc-btn--op w-full py-2.5"'
LABEL = 'class="block text-sm font-medium mb-1"'
CHIP = ('class="px-3 py-1.5 rounded-full surface text-xs font-semibold font-numeric '
        'hover:shadow-md transition-shadow"')
H3 = 'class="font-semibold text-[var(--color-text)] mb-1"'
FORMULA = 'class="font-numeric text-[var(--color-text)]"'
RESULT_H2 = 'class="font-display font-semibold text-lg mb-3"'
MUTED = "text-[var(--color-text-muted)]"
PRIMARY = "text-[var(--color-primary-link)]"
ENGINE = '  <script src="/assets/js/calc-simple.js"></script>\n'


def esc(s):
    return str(s).replace("&", "&amp;").replace('"', "&quot;")


class Lib:
    def __init__(self, prefix):
        self.p = prefix

    def _wrap(self, id_, inner, when):
        w = f' data-when="{when}"' if when else ""
        return f'        <div id="{self.p}-w-{id_}"{w}>\n{inner}\n        </div>'

    def num(self, id_, label, ph="", rule="pos", opt=False, default=None, value="", when=None, hint=""):
        attrs = f'data-kind="num" data-label="{esc(label)}" data-rule="{rule}"'
        if opt:
            attrs += " data-opt"
        if default is not None:
            attrs += f' data-def="{default}"'
        v = f' value="{value}"' if value != "" else ""
        h = f'\n          <p class="mt-1 text-xs {MUTED}">{hint}</p>' if hint else ""
        inner = (f'          <label for="{self.p}-{id_}" {LABEL}>{label}</label>\n'
                 f'          <input id="{self.p}-{id_}" type="text" inputmode="decimal" placeholder="{esc(ph)}"{v} {attrs} {INPUT} />{h}')
        return self._wrap(id_, inner, when)

    def sel(self, id_, label, options, when=None, value=None):
        opts = "".join(f'<option value="{v}"{" selected" if v == value else ""}>{t}</option>' for v, t in options)
        inner = (f'          <label for="{self.p}-{id_}" {LABEL}>{label}</label>\n'
                 f'          <select id="{self.p}-{id_}" data-kind="sel" data-label="{esc(label)}" {SELECT}>{opts}</select>')
        return self._wrap(id_, inner, when)

    def text(self, id_, label, ph="", when=None, rows=0, opt=False, value="", hint=""):
        o = " data-opt" if opt else ""
        h = f'\n          <p class="mt-1 text-xs {MUTED}">{hint}</p>' if hint else ""
        if rows:
            el = (f'<textarea id="{self.p}-{id_}" rows="{rows}" spellcheck="false" placeholder="{esc(ph)}" data-kind="text" '
                  f'data-label="{esc(label)}"{o} {INPUT}>{value}</textarea>')
        else:
            v = f' value="{esc(value)}"' if value else ""
            el = (f'<input id="{self.p}-{id_}" type="text" autocomplete="off" spellcheck="false" placeholder="{esc(ph)}"{v} '
                  f'data-kind="text" data-label="{esc(label)}"{o} {INPUT} />')
        inner = f'          <label for="{self.p}-{id_}" {LABEL}>{label}</label>\n          {el}{h}'
        return self._wrap(id_, inner, when)

    def form(self, parts, chips=None, button="Calcular", note=""):
        c = ""
        if chips:
            btns = "".join(f'<button type="button" data-ex="{esc(v)}" {CHIP}>{l}</button>' for l, v in chips)
            c = f'\n          <div class="flex flex-wrap gap-2" aria-label="Ejemplos">{btns}</div>'
        n = f'\n          <p class="text-xs {MUTED}">{note}</p>' if note else ""
        body = "\n".join(parts)
        return (f'        <div class="space-y-4">\n{body}{c}\n'
                f'          <button id="{self.p}-solve" type="button" {BTN}>{button}</button>{n}\n        </div>')

    def panel(self, label_static="", title="Resultado"):
        lab = (f'<p class="text-sm {MUTED}">{label_static}</p>' if label_static
               else f'<p id="{self.p}-label" class="text-sm {MUTED}"></p>')
        return f"""        <section id="{self.p}-result-panel" class="hidden surface rounded-2xl p-5 shadow-sm">
          <h2 {RESULT_H2}>{title}</h2>
          {lab}
          <p id="{self.p}-main" class="font-numeric text-3xl font-bold {PRIMARY} break-words">—</p>
          <div id="{self.p}-lines" class="mt-3 text-sm {MUTED} space-y-1"></div>
          <div id="{self.p}-extra" class="mt-3 text-sm {MUTED}"></div>
        </section>"""


def help_blocks(items):
    """items: [(titulo, html)] -> bloques de ayuda."""
    out = []
    for t, body in items:
        out.append(f'            <div>\n              <h3 {H3}>{t}</h3>\n              {body}\n            </div>')
    return "\n".join(out)


def write_page(rel, html):
    path = ROOT / rel / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("escrito:", path.relative_to(ROOT))


# ---- guías: mini-DSL ---------------------------------------------------------------
S = '<strong class="text-[var(--color-text)]">'


def g_h2(t):
    return f'      <h2 class="font-display font-bold text-xl mt-8 mb-2">{t}</h2>'


def g_p(t):
    return f'      <p class="{MUTED} leading-relaxed">\n        {t}\n      </p>'


def g_formula(t):
    return f'      <p class="font-numeric text-center my-3 text-[var(--color-text)]">{t}</p>'


def g_steps(items):
    li = "\n".join(f"        <li>{i}</li>" for i in items)
    return f'      <ol class="list-decimal list-inside space-y-1 {MUTED} font-numeric">\n{li}\n      </ol>'


def g_ul(items):
    li = "\n".join(f"        <li>{i}</li>" for i in items)
    return f'      <ul class="list-disc list-inside space-y-1 {MUTED}">\n{li}\n      </ul>'


def g_table(head, rows):
    th = "".join(f'<th class="px-3 py-2 font-semibold">{c}</th>' for c in head)
    tr = "\n".join('            <tr class="border-t border-[var(--color-border)]">' + "".join(f'<td class="px-3 py-2">{c}</td>' for c in r) + "</tr>" for r in rows)
    return (f'      <div class="mt-3 overflow-x-auto rounded-xl border border-[var(--color-border)]">\n'
            f'        <table class="w-full text-sm min-w-[360px] font-numeric">\n'
            f'          <thead><tr class="text-left {MUTED}">{th}</tr></thead>\n'
            f'          <tbody class="{MUTED}">\n{tr}\n          </tbody>\n        </table>\n      </div>')


def write_guide(slug, html):
    path = ROOT / "guias" / slug / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("escrito:", path.relative_to(ROOT))
