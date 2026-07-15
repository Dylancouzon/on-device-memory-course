"""Gate check for data/objects/: the L6 recognition threshold must sit in a real
gap. For every object with three views, the held-out third view scores >= 0.82
against its taught pair, while no other object or scene image scores > 0.75
against its views. Two-view objects (backpack, lithops) only get the no-collision
check; the backpack's canonical teach-one/recognize-other stays ~0.86.

Objects are curated by hand from Wikimedia Commons upload series (same physical
object, multiple views) recorded in data/objects/CREDITS.json. Run after any
change to that folder: `python .build/check_objects.py`.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils.embeddings import embed_image

HELD_OUT_MIN = 0.82
FOREIGN_MAX = 0.75
OBJ = Path(__file__).parent.parent / "data" / "objects"
SCENES = Path(__file__).parent.parent / "data" / "images"


def cos(a, b):
    return sum(x * y for x, y in zip(a, b)) / (
        math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def main():
    objs = {}
    for f in sorted(OBJ.glob("*.jpg")):
        objs.setdefault(f.stem.rsplit("_", 1)[0], []).append(str(f))
    scenes = [str(s) for s in sorted(SCENES.glob("*.jpg"))]
    allp = [p for v in objs.values() for p in v] + scenes
    vec = dict(zip(allp, embed_image(allp)))
    owner = {p: name for name, v in objs.items() for p in v}

    failures = []
    for name, views in objs.items():
        foreign = [p for p in allp if owner.get(p) != name]
        fmax = max(cos(vec[p], vec[t]) for t in views for p in foreign)
        line = f"{name:12} views={len(views)} foreign_max={fmax:.3f}"
        if len(views) >= 3:
            held = max(cos(vec[views[2]], vec[views[0]]),
                       cos(vec[views[2]], vec[views[1]]))
            ok = held >= HELD_OUT_MIN and fmax <= FOREIGN_MAX
            line += f" held_out={held:.3f} -> {'PASS' if ok else 'FAIL'}"
            if not ok:
                failures.append(name)
        elif fmax > FOREIGN_MAX:
            line += " -> FAIL (collision)"
            failures.append(name)
        print(line)

    bp = objs.get("backpack", [])
    if len(bp) == 2:
        s = cos(vec[bp[0]], vec[bp[1]])
        print(f"backpack recognize (view1->view2) = {s:.3f}")
        assert s >= 0.80, "backpack canonical recognition regressed"

    assert not failures, f"objects failed the gate: {failures}"
    print("\nOK: threshold 0.80 sits in a real gap for every object.")


if __name__ == "__main__":
    main()
