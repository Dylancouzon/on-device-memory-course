"""One-command course gate: run after any notebook re-execution.

Checks helper freshness, notebook hygiene (line width, no forward
references across cells), and the payoff guards from the saved outputs.
Run `.build/check_objects.py` separately for the recognition-threshold
gate, and see `.build/design/PAYOFF_REGISTRY.md` for the full value list.

Usage: python .build/verify_course.py  (from the repo root)
"""
import ast
import builtins
import json
import subprocess
import sys
from pathlib import Path

fails = []


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))
    if not ok:
        fails.append(name)


def cell_sources(nb_path):
    nb = json.loads(Path(nb_path).read_text())
    for c in nb["cells"]:
        src = c["source"] if isinstance(c["source"], str) else "".join(c["source"])
        yield c, src


def outputs_text(nb_path):
    out = []
    nb = json.loads(Path(nb_path).read_text())
    for c in nb["cells"]:
        for o in c.get("outputs", []):
            t = o.get("text")
            if t:
                out.append("".join(t) if isinstance(t, list) else t)
    return "\n".join(out)


# 1. helper freshness: regenerating must not change what's on disk
HELPERS = ["L2/helper.py", "L3/helper.py", "L4/helper.py", "L5/helper.py"]
before = {p: Path(p).read_bytes() for p in HELPERS}
subprocess.run([sys.executable, ".build/gen_helpers.py"], capture_output=True)
after = {p: Path(p).read_bytes() for p in HELPERS}
check("helpers regenerate cleanly (no drift vs utils)", before == after)

# 2. notebook hygiene: <=80-char code lines, no name used before its cell
for n in [2, 3, 4, 5]:
    path = f"L{n}/L{n}.ipynb"
    wide = []
    defined = set(dir(builtins))
    forward = []
    for c, src in cell_sources(path):
        if c["cell_type"] != "code":
            continue
        wide += [ln for ln in src.splitlines() if len(ln) > 80]
        tree = ast.parse(src)
        used = {x.id for x in ast.walk(tree)
                if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load)}
        defs = set()
        for x in ast.walk(tree):
            if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Store):
                defs.add(x.id)
            elif isinstance(x, (ast.FunctionDef, ast.ClassDef)):
                defs.add(x.name)
            elif isinstance(x, ast.alias):
                defs.add((x.asname or x.name).split(".")[0])
            elif isinstance(x, ast.arg):
                defs.add(x.arg)
            elif isinstance(x, ast.ExceptHandler) and x.name:
                defs.add(x.name)
        forward += sorted(used - defined - defs)
        defined |= defs
    check(f"L{n} code lines <= 80 chars", not wide, f"{len(wide)} wide" if wide else "")
    check(f"L{n} no forward references", not forward, ", ".join(forward[:4]))

# 3. payoff guards, from the saved (shipped) outputs
t2 = outputs_text("L2/L2.ipynb")
check("L2 cold open returns 0", "Memories found: 0" in t2)
check("L2 keyword scan returns 0", 'Notes containing "latte": 0' in t2)
check("L2 ask #2 finds the cafe note", "0.653  Great little coffee place" in t2)
check("L2 forget removes the cafe note", "Forgot: Great little coffee place" in t2)
check("L2 forget legend is delete-specific", "still remembered" in t2)
t4 = outputs_text("L4/L4.ipynb")
check("L4 has 42 captures", "42 captures: 17 photo, 20 text, 5 voice" in t4)
check("L4 added memory wins", "id=900" in t4)
t5 = outputs_text("L5/L5.ipynb")
check("L5 backpack note recalled", "I remember this: Quechua daypack" in t5)
check("L5 assistant holds day+history+object", "145 memories" in t5)

print("\n" + ("ALL CHECKS PASS" if not fails else f"{len(fails)} FAILURES"))
sys.exit(1 if fails else 0)
