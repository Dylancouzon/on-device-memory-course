"""Generate the course's top-level helper.py from the canonical utils/.

The DLAI layout keeps one shared helper.py at the repo root and a symbolic
link to it in every lesson folder, so each folder is self-contained once the
platform replaces the links with copies.

The output has to read like one hand-written file, because that is what a
reviewer sees. So this does more than concatenate: it lifts every
module-level import into a single block at the top, drops each module's own
docstring in favour of the section headings below, and strips the module
self-checks and intra-package imports. Edit utils/ and re-run:
`python .build/gen_helpers.py`.
"""
import ast
import re
from pathlib import Path

BUILD = Path(__file__).parent
SRC = BUILD / "utils"
ROOT = BUILD.parent

# Section heading per module, written by hand so the seams read as structure.
SECTIONS = [
    ("embeddings", "Embedding models: Nomic for text, CLIP for images"),
    ("qdrant_helpers", "Shard setup, the offline guard, and benchmark filler"),
    ("viz", "The views the lessons print"),
    ("audio", "Speech to text for the voice notes"),
]
LESSONS = ["L3", "L4", "L5", "L6", "L7"]

HEADER = '''"""Helper functions for the course notebooks.

Plumbing for the lessons: the on-device embedding models, speech-to-text for
the voice notes, the result tables and charts the lessons print, and the stores
and searches the lessons repeat. Each Qdrant call is written out in the
notebook of the lesson that teaches it; after that, the repeat lives here.
"""
'''

STDLIB = {"gc", "inspect", "shutil", "socket", "contextlib", "functools",
          "pathlib", "textwrap", "json", "os", "re", "time", "statistics"}


def split_module(name):
    """Return (module-level import lines, body) for one utils module."""
    text = (SRC / f"{name}.py").read_text()
    text = re.split(r"\ndef demo\(", text)[0]      # drop self-check + __main__

    # Drop the module docstring: the section heading replaces it.
    tree = ast.parse(text)
    lines = text.splitlines()
    if (tree.body and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, ast.Constant)
            and isinstance(tree.body[0].value.value, str)):
        del lines[:tree.body[0].end_lineno]

    imports, body = [], []
    for ln in lines:
        is_top_import = re.match(r"(import|from)\s", ln)      # column 0 only
        if is_top_import and not ln.startswith("from ."):
            imports.append(ln)                                # hoist it
        elif is_top_import:
            continue                                          # intra-package
        else:
            body.append(ln)
    return imports, "\n".join(body).strip("\n")


def sort_imports(lines):
    """Stdlib block, then third-party, `import x` before `from x import y`."""
    def key(ln):
        root = re.sub(r"^(?:import|from)\s+([\w.]+).*", r"\1", ln).split(".")[0]
        return (0 if root in STDLIB else 1, 0 if ln.startswith("import") else 1,
                root, ln)

    ordered = sorted(set(lines), key=key)
    out, prev_third_party = [], None
    for ln in ordered:
        third_party = key(ln)[0]
        if prev_third_party is not None and third_party != prev_third_party:
            out.append("")                       # blank line between blocks
        out.append(ln)
        prev_third_party = third_party
    return out


all_imports, sections = [], []
for name, heading in SECTIONS:
    imports, body = split_module(name)
    all_imports += imports
    rule = "-" * max(3, 69 - len(heading))   # "# " + heading + " " + rule <= 72
    sections.append(f"# {heading} {rule}\n{body}")

body = "\n\n\n".join(["\n".join(sort_imports(all_imports)), *sections])
(ROOT / "helper.py").write_text(HEADER + body + "\n")
print(f"wrote helper.py ({len(SECTIONS)} sections)")

for lesson in LESSONS:
    link = ROOT / lesson / "helper.py"
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to("../helper.py")
    print(f"linked {lesson}/helper.py")
