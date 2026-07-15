"""Generate each lesson's self-contained helper.py from the canonical utils/.

Each DLAI lesson folder ships a helper.py next to its notebook so the folder
runs on its own. This concatenates the utils modules a lesson actually uses
into one file, drops the intra-package imports (everything is now in-file),
and strips the module self-checks. Edit utils/ and re-run:
`python .build/gen_helpers.py`.
"""
import re
from pathlib import Path

BUILD = Path(__file__).parent
SRC = BUILD / "utils"
ROOT = BUILD.parent

# Modules each lesson imports from (whole-module include: safe, self-contained).
LESSONS = {
    "L1": ["embeddings"],
    "L2": ["embeddings", "qdrant_helpers", "viz"],
    "L3": ["embeddings", "qdrant_helpers", "viz"],
    "L4": ["embeddings", "qdrant_helpers", "viz"],
    "L5": ["embeddings", "qdrant_helpers", "viz", "audio"],
    "L6": ["embeddings", "qdrant_helpers", "viz"],
}

HEADER = (
    '"""Lesson helpers, generated from .build/utils by gen_helpers.py.\n\n'
    'Edit the source modules under .build/utils and regenerate; do not edit\n'
    'this file directly."""\n'
)


def module_src(name):
    text = (SRC / f"{name}.py").read_text()
    text = re.split(r"\ndef demo\(", text)[0]          # drop self-check + __main__
    lines = [ln for ln in text.splitlines()
             if not ln.strip().startswith("from .")]   # drop intra-package imports
    return "\n".join(lines).rstrip()


for lesson, mods in LESSONS.items():
    parts = [HEADER]
    for m in mods:
        parts.append(f"\n# --- {m} " + "-" * 40 + "\n" + module_src(m))
    out = ROOT / lesson / "helper.py"
    out.write_text("\n".join(parts) + "\n")
    print("wrote", out.relative_to(ROOT), f"({len(mods)} modules)")
