"""Helper functions for the course notebooks.

Plumbing for the lessons: the on-device embedding models, speech-to-text for
the voice notes, the result tables and charts the lessons print, and the stores
and searches the lessons repeat. Each Qdrant call is written out in the
notebook of the lesson that teaches it; after that, the repeat lives here.
"""
import gc
import inspect
import json
import math
import shutil
import socket
from collections import Counter
from functools import lru_cache
from pathlib import Path

import matplotlib.pyplot as plt
from qdrant_edge import EdgeShard, Point, Query, QueryRequest, UpdateOperation


# The lessons open with `from helper import *`; this is what that hands them.
__all__ = [
    "add_filler", "answers_table", "before_after", "cloud_client",
    "day_notes", "day_photos", "day_summary", "embed_image",
    "embed_query", "embed_query_clip", "embed_query_ms",
    "embed_text", "fetch_snapshot", "filler_vectors", "fresh_start",
    "latency_hist", "load_day_and_history", "load_image",
    "load_memories", "lookup_times", "memories_table",
    "memory_inbox", "object_photos", "photo_search",
    "photo_uploader", "point_card", "recall", "receipt_table",
    "recognition_result", "recognize", "remember", "results_table",
    "seed_objects", "show", "show_images", "show_photo_results",
    "show_raw", "store_notes", "store_photo_memories",
    "store_photos", "text_search", "threshold_calibration",
    "transcribe", "transcribe_notes", "vector_preview"
]


# Embedding models: Nomic for text, CLIP for images --------------------
NOMIC_MODEL = "nomic-ai/nomic-embed-text-v1.5"
NOMIC_DIM = 768


@lru_cache(maxsize=1)
def _text_model():
    from fastembed import TextEmbedding
    return TextEmbedding(NOMIC_MODEL)


def embed_text(texts):
    """Embed documents for storage. Returns list[list[float]] (one per input)."""
    return [v.tolist() for v in _text_model().embed(list(texts))]


def embed_query(text):
    """Embed a single query string.

    Nomic uses different task prefixes for documents and queries; FastEmbed's
    `query_embed` applies the query prefix so retrieval scores line up.
    """
    return next(_text_model().query_embed([text])).tolist()


# CLIP: one shared text/image space, for cross-modal recall in L4 and later.
# Nomic and CLIP scores sit on different scales, so photos live in their own
# named vector and a text query is embedded twice, once per space.
CLIP_VISION_MODEL = "Qdrant/clip-ViT-B-32-vision"
CLIP_TEXT_MODEL = "Qdrant/clip-ViT-B-32-text"
CLIP_DIM = 512


@lru_cache(maxsize=1)
def _clip_vision():
    from fastembed import ImageEmbedding
    return ImageEmbedding(CLIP_VISION_MODEL)


@lru_cache(maxsize=1)
def _clip_text():
    from fastembed import TextEmbedding
    return TextEmbedding(CLIP_TEXT_MODEL)


def embed_image(paths):
    """Embed image files with CLIP's vision encoder. Returns list[list[float]]."""
    return [v.tolist() for v in _clip_vision().embed(list(paths))]


def load_image(url_or_path):
    """Return a local image path, fetching http(s) URLs to a temp JPEG first.

    A path to a file already on disk passes straight through, so the upload
    button and a filename typed by hand both land here.
    """
    if not str(url_or_path).startswith(("http://", "https://")):
        return url_or_path
    import io
    import os
    import tempfile
    import urllib.parse
    import urllib.request
    from PIL import Image

    # A search-results link points at a viewer page and carries the real
    # image URL in its imgurl parameter.
    query = urllib.parse.parse_qs(urllib.parse.urlparse(url_or_path).query)
    url = query.get("imgurl", [url_or_path])[0]

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
        image = Image.open(io.BytesIO(data)).convert("RGB")
    except OSError:
        raise ValueError(
            f"No image came back from this link:\n  {url[:90]}\n"
            "Right-click the image itself and copy the image address (it "
            "ends in .jpg or .png), or use the upload button instead."
        ) from None
    fd, path = tempfile.mkstemp(suffix=".jpg")
    os.close(fd)
    image.save(path, "JPEG")
    return path


def embed_query_clip(text):
    """Embed a text query into CLIP's space, to search the image vector."""
    return next(_clip_text().query_embed([text])).tolist()


def embed_query_ms(text, runs=50):
    """Median time in milliseconds to embed one query, measured live."""
    from statistics import median
    from time import perf_counter
    times = []
    for _ in range(runs):
        t0 = perf_counter()
        embed_query(text)
        times.append((perf_counter() - t0) * 1000)
    return median(times)


EXAMPLE_OBJECT = "./ro_shared_data/objects/rubberduck_"
TEACH_DIR = "./my_photos/teach"
TEST_DIR = "./my_photos/test"
IMAGE_TYPES = (".jpg", ".jpeg", ".png", ".webp")
_UPLOADS_RESET = False


def _uploaded(folder):
    """Photos sitting in an upload folder, oldest first."""
    path = Path(folder)
    if not path.is_dir():
        return []
    files = [f for f in path.iterdir() if f.suffix.lower() in IMAGE_TYPES]
    return sorted(files, key=lambda f: f.stat().st_mtime)


def _upload_box(folder, heading, hint):
    """One labelled upload button that saves into `folder`."""
    import ipywidgets as widgets

    Path(folder).mkdir(parents=True, exist_ok=True)
    title = widgets.HTML(f"<b>{heading}</b><br><small>{hint}</small>")
    button = widgets.FileUpload(accept="image/*", multiple=True)
    status = widgets.HTML(_upload_status(folder))

    def save(change):
        for item in change["new"]:
            (Path(folder) / item["name"]).write_bytes(item["content"])
        button.value = ()
        status.value = _upload_status(folder)

    button.observe(save, names="value")
    return widgets.VBox([title, button, status],
                        layout=widgets.Layout(width="330px"))


def _upload_status(folder):
    files = _uploaded(folder)
    if not files:
        return "<small>Nothing uploaded yet.</small>"
    return f"<small>{len(files)} ready: {', '.join(f.name for f in files)}</small>"


def _reset_uploads_once():
    """Start each fresh kernel with empty upload folders.

    The flag keeps a same-kernel re-run of the first cell from deleting photos
    the student just uploaded. Restarting the kernel reloads this module,
    resets the flag, and clears the previous session's files.
    """
    global _UPLOADS_RESET
    if _UPLOADS_RESET:
        return
    for folder in (TEACH_DIR, TEST_DIR):
        path = Path(folder)
        if path.is_dir():
            for uploaded in path.iterdir():
                if uploaded.is_file() or uploaded.is_symlink():
                    uploaded.unlink()
    _UPLOADS_RESET = True


def photo_uploader():
    """Two upload buttons: the photos to teach with, and the one to test with.

    Photos land in ./my_photos for this kernel session. A fresh kernel clears
    the previous session's uploads; re-running this cell in the same kernel
    keeps them. Holding one photo back is the point of the lab: the device
    meets it once before it has been taught anything, and once after. Leave
    both empty for the bundled example.
    """
    import ipywidgets as widgets
    from IPython.display import display

    _reset_uploads_once()
    display(widgets.HBox([
        _upload_box(TEACH_DIR, "Teach with these",
                    "Two or more photos of one object, from different "
                    "angles or in different places."),
        _upload_box(TEST_DIR, "Test with this one",
                    "One more photo of the same object. Leave this one out "
                    "of the teaching photos."),
    ]))


def object_photos():
    """The photos to teach with, and the one held back to test with.

    Reads the two folders the upload buttons write to, and falls back to the
    bundled example when both are empty.
    """
    teach = [str(f) for f in _uploaded(TEACH_DIR)]
    test = [str(f) for f in _uploaded(TEST_DIR)]
    if not teach and not test:
        example = [EXAMPLE_OBJECT + f"{i}.jpg" for i in (1, 2, 3)]
        print("Using the bundled example: a rubber duck, 2 photos to teach",
              "with and 1 to test with")
        return example[:2], example[2]
    if len(teach) < 2 or len(test) != 1:
        raise ValueError(
            f"Found {len(teach)} photo(s) to teach with and {len(test)} to "
            "test with. Upload two or more on the left and exactly one on "
            "the right, or leave both empty for the bundled example."
        )
    print(f"{len(teach)} photos to teach with, 1 held back to test")
    return teach, test[0]


# Shard setup, the offline guard, and benchmark filler -----------------
# How much of a write to show back. Small: the recording frame is tall,
# not endless, and the point is what landed, not all of it.
PREVIEW_ROWS = 4
PREVIEW_PHOTOS = 6


def load_memories(path, source_type=None):
    """Read a memories JSON file, optionally keeping one source type."""
    memories = json.load(open(path))
    if source_type:
        memories = [m for m in memories if m["source_type"] == source_type]
    return memories


def store_notes(shard, notes, preview=True):
    """Embed text and voice notes with Nomic and store one point per note.

    The write this wraps is taught in Lesson 3: embed the note, build a
    Point with the note as payload, upsert. A voice note embeds its
    transcript.
    """
    vectors = embed_text([m.get("note") or m["transcript"] for m in notes])
    shard.update(UpdateOperation.upsert_points([
        Point(id=m["id"], vector={"text": v}, payload=m)
        for m, v in zip(notes, vectors)
    ]))
    if preview:
        show(memories_table(notes[:PREVIEW_ROWS],
                            f"Stored {len(notes)} notes"))
    else:
        print(f"Stored {len(notes)} notes")


def store_photos(shard, folder, start_id=1000, preview=True):
    """Embed a folder of photos with CLIP and store them in the image vector."""
    photos = sorted(Path(folder).glob("*.jpg"))
    vectors = embed_image([str(p) for p in photos])
    shard.update(UpdateOperation.upsert_points([
        Point(id=start_id + i, vector={"image": v},
              payload={"file": p.name, "source_type": "photo"})
        for i, (p, v) in enumerate(zip(photos, vectors))
    ]))
    shard.optimize()
    if preview:
        show(show_images([str(p) for p in photos[:PREVIEW_PHOTOS]],
                         captions=[p.name for p in photos[:PREVIEW_PHOTOS]],
                         per_row=6,
                         title=f"Stored {len(photos)} photos as "
                               f"{len(vectors[0])}-d CLIP vectors · "
                               f"{shard.info().points_count} memories"))
    else:
        print(f"Stored {len(photos)} photos."
              f" Total: {shard.info().points_count} memories")


def store_photo_memories(shard, photos, folder, preview=True):
    """Embed photo memories with CLIP and store one point per photo."""
    vectors = embed_image([f"{folder}/{m['file']}" for m in photos])
    shard.update(UpdateOperation.upsert_points([
        Point(id=m["id"], vector={"image": v}, payload=m)
        for m, v in zip(photos, vectors)
    ]))
    shard.optimize()
    if preview:
        show(day_photos(photos[:PREVIEW_PHOTOS], folder,
                        f"Stored {len(photos)} photos · "
                        f"{shard.info().points_count} memories"))
    else:
        print(f"Stored {len(photos)} photos."
              f" Total: {shard.info().points_count} memories")


def text_search(shard, query, query_filter=None, limit=4):
    """Embed a query with Nomic and return the nearest text memories.

    The raw call is taught in Lesson 3; `query_filter` narrows recall the
    way Lesson 4 teaches.
    """
    return shard.query(QueryRequest(
        query=Query.Nearest(embed_query(query), using="text"),
        filter=query_filter,
        limit=limit,
        with_payload=True,
    ))


def photo_search(shard, description, limit=1):
    """Embed a description with CLIP and return the nearest photos.

    The raw cross-modal call is taught in Lesson 4.
    """
    return shard.query(QueryRequest(
        query=Query.Nearest(embed_query_clip(description), using="image"),
        limit=limit,
        with_payload=True,
    ))


def recall(shard, question):
    """One question, two lanes: text memories by Nomic, photos by CLIP.

    Lesson 5 builds this in the open; later lessons import it. Extra text
    hits are fetched so one lane cannot crowd out the other.
    """
    text_hits = text_search(shard, question, limit=10)
    photo_hits = photo_search(shard, question, limit=3)
    return {
        "Photos": [h for h in photo_hits
                   if h.payload.get("source_type") == "photo"][:1],
        "Voice Notes": [h for h in text_hits
                        if h.payload.get("source_type") == "voice"][:3],
        "Text Notes": [h for h in text_hits
                       if h.payload.get("source_type") == "text"][:3],
    }


def recognize(shard, photo, threshold=None):
    """The closest stored photo, and optionally whether it clears the bar.

    The nearest-vector query is Lesson 3's; searching the image vector is
    Lesson 4's. What Lesson 6 adds is the threshold: below it, the device
    says it does not know this object rather than guessing.
    """
    top = shard.query(QueryRequest(
        query=Query.Nearest(embed_image([photo])[0], using="image"),
        limit=1,
        with_payload=True,
    ))[0]
    known = None if threshold is None else top.score >= threshold
    return top, known


def seed_objects(shard, folder="./ro_shared_data/bank"):
    """Store three known objects and show them, one photo each at ids 0-2.

    Writes exactly what Lesson 6's `teach` writes: the photo's CLIP vector
    with the label as payload, flushed to disk so a taught memory survives
    a power cut.
    """
    seeds = {"a bicycle": "bicycle.jpg",
             "chess pieces": "chess_set.jpg",
             "a camera": "camera.jpg"}
    paths = [f"{folder}/{f}" for f in seeds.values()]
    vectors = embed_image(paths)
    shard.update(UpdateOperation.upsert_points([
        Point(id=i, vector={"image": v},
              payload={"label": label, "file": p})
        for i, (label, p, v) in enumerate(zip(seeds, paths, vectors))
    ]))
    shard.optimize()
    shard.flush()
    show(show_images(paths, captions=list(seeds),
                     title=f"It already knows {len(seeds)} objects"))


def load_day_and_history(folder="./ro_shared_data"):
    """The assistant's full memory: today's captures plus the earlier days.

    Returns (day, history, notes, photos): the two files, then the text
    and voice notes from both, then today's photos.
    """
    day = load_memories(f"{folder}/memories.json")
    history = load_memories(f"{folder}/recent_days.json")
    notes = [m for m in day + history
             if m["source_type"] in ("text", "voice")]
    photos = [m for m in day if m["source_type"] == "photo"]
    return day, history, notes, photos


def cloud_client(enabled, collection):
    """Connect to the Qdrant cluster named in QDRANT_URL / QDRANT_API_KEY.

    Returns a ready qdrant_client.QdrantClient, or None when syncing is
    off, the env vars are missing, or the collection already exists on
    the cluster (the course never deletes one). None means every memory
    stays on the device, and the calling cell says so.
    """
    import os
    if not (enabled and os.getenv("QDRANT_URL")
            and os.getenv("QDRANT_API_KEY")):
        return None
    from qdrant_client import QdrantClient
    client = QdrantClient(url=os.environ["QDRANT_URL"],
                          api_key=os.environ["QDRANT_API_KEY"])
    if client.collection_exists(collection):
        print(f"{collection} already exists on the cluster.",
              "Delete it there first, or rename the collection here.")
        return None
    return client


def remember(shard, note, memories, point_id=900):
    """Store one new text note, stamped at the end of the day."""
    memory = {
        "id": point_id, "source_type": "text", "category": "home",
        "location": "Home",
        "timestamp": max(m["timestamp"] for m in memories),
        "note": note,
    }
    shard.update(UpdateOperation.upsert_points([
        Point(id=point_id, vector={"text": embed_text([note])[0]},
              payload=memory)
    ]))
    shard.optimize()


def fetch_snapshot(collection, dest, manifest=None):
    """Download a shard snapshot from the cluster in QDRANT_URL to a file.

    With a manifest (from `EdgeShard.snapshot_manifest`), asks the server
    for a partial snapshot holding only what this shard is missing.
    """
    import os
    import urllib.request
    base_url = os.environ["QDRANT_URL"]
    headers = {"api-key": os.getenv("QDRANT_API_KEY") or ""}
    if manifest is None:
        url = f"{base_url}/collections/{collection}/shards/0/snapshot"
        req = urllib.request.Request(url, headers=headers)
    else:
        url = (f"{base_url}/collections/{collection}"
               "/shards/0/snapshot/partial/create")
        headers["Content-Type"] = "application/json"
        req = urllib.request.Request(
            url, data=json.dumps(manifest).encode(),
            headers=headers, method="POST")
    with urllib.request.urlopen(req) as response, open(dest, "wb") as f:
        f.write(response.read())
    return dest


def add_filler(shard, count=5000, dim=768, start_id=1000):
    """Grow the shard with random filler so a latency number is credible.

    Returns the new total point count.
    """
    shard.update(UpdateOperation.upsert_points([
        Point(id=start_id + i, vector={"text": v},
              payload={"kind": "filler"})
        for i, v in enumerate(filler_vectors(count, dim))
    ]))
    shard.optimize()
    return shard.info().points_count


def lookup_times(shard, query_vector, runs=200):
    """Milliseconds per vector lookup, one number per run.

    The query vector is embedded before the clock starts, so this times
    the search alone.
    """
    from time import perf_counter
    timings = []
    for _ in range(runs):
        t0 = perf_counter()
        shard.query(QueryRequest(
            query=Query.Nearest(query_vector, using="text"),
            limit=3,
            with_payload=True,
        ))
        timings.append((perf_counter() - t0) * 1000)
    return timings


def filler_vectors(count, dim, seed=0):
    """Random vectors that grow the shard so a latency number is credible.

    Content is irrelevant to latency, it tracks how many vectors there are and
    how wide they are. The notebook builds the points and upserts them itself,
    so every write stays visible in the cell.
    """
    import numpy as np
    rng = np.random.default_rng(seed)
    return rng.normal(size=(count, dim)).astype("float32").tolist()


def fresh_start(directory):
    """Delete any previous run's shard directory and recreate it empty.

    A shard the notebook still has bound holds its files open, and Edge flushes
    when that object is dropped. Deleting the files first makes the flush fail
    inside a destructor, which surfaces as a Rust panic rather than a Python
    error. So close any shard the caller still holds before removing anything:
    that makes re-running a setup cell in a live kernel safe, instead of only
    working on a clean top-to-bottom run.
    """
    frame = inspect.stack()[1].frame
    try:
        for value in list(frame.f_globals.values()):
            if isinstance(value, EdgeShard):
                try:
                    value.close()
                except Exception:
                    pass
    finally:
        del frame
    gc.collect()
    shutil.rmtree(directory, ignore_errors=True)
    Path(directory).mkdir(parents=True, exist_ok=True)
    return directory


# The views the lessons print ------------------------------------------
QDRANT_RED = "#DC244C"
INK = "#28324D"
MUTED = "#6B7280"
LINE = "#E5E7EB"
FONT = "font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"
FIG_W = 8.0        # recording frame is 8 wide by 9 high

MODALITY_COLOR = {"photo": QDRANT_RED, "voice": "#8547FF", "text": INK}
MODALITY_EMOJI = {"photo": "📷", "voice": "🎙️", "text": "📝"}


def show(view):
    """Put a view on screen from inside a helper, mid-cell."""
    from IPython.display import display
    display(view)


def _html(markup):
    from IPython.display import HTML
    return HTML(markup)


def _esc(value):
    import html
    return html.escape(str(value))


def _score_cell(score, peak):
    """A score with a proportional bar behind it, still selectable as text.

    Pass `peak=None` where the column mixes score scales: a bar would invite
    a comparison between a CLIP score and a Nomic one, which means nothing.
    """
    pct = max(0.0, min(1.0, score / peak)) * 100 if peak else 0
    return (f'<td style="text-align:right;font-variant-numeric:tabular-nums;'
            f'font-weight:700;color:{QDRANT_RED};'
            f'background:linear-gradient(to left,rgba(220,36,76,.14) {pct:.0f}%,'
            f'transparent {pct:.0f}%)">{score:.3f}</td>')


def _table(headers, rows, title=None, caption=None):
    """Render a table as HTML. `rows` holds ready-made <td> strings."""
    head = "".join(
        f'<th style="text-align:left;padding:6px 10px;font-size:12px;'
        f'letter-spacing:.04em;text-transform:uppercase;color:{MUTED};'
        f'border-bottom:2px solid {QDRANT_RED}">{_esc(h)}</th>'
        for h in headers)
    body = "".join(
        f'<tr style="background:{"#FFFFFF" if i % 2 else "#FAFAFB"}">{r}</tr>'
        for i, r in enumerate(rows))
    parts = [f'<div style="{FONT};max-width:760px">']
    if title:
        parts.append(f'<div style="font-weight:800;font-size:15px;color:{INK};'
                     f'margin-bottom:6px">{_esc(title)}</div>')
    parts.append('<table style="border-collapse:collapse;width:100%;'
                 f'font-size:13.5px;color:{INK}"><thead><tr>{head}</tr></thead>'
                 f'<tbody>{body}</tbody></table>')
    if caption:
        parts.append(f'<div style="font-size:12px;color:{MUTED};'
                     f'margin-top:6px">{_esc(caption)}</div>')
    parts.append("</div>")
    return "".join(parts)


def _cell(value, align="left", color=INK, weight=400, size=13.5,
          nowrap=False):
    return (f'<td style="padding:6px 10px;text-align:{align};color:{color};'
            f'font-weight:{weight};font-size:{size}px;'
            f'{"white-space:nowrap;" if nowrap else ""}'
            f'border-bottom:1px solid {LINE}">{_esc(value)}</td>')


def _memory_text(payload):
    """The words of a memory: its note, its transcript, or its filename."""
    return payload.get("note") or payload.get("transcript") or payload.get("file", "")


def _price(payload):
    return f"${payload['price']:.0f}" if payload.get("price") is not None else "-"


def _has_price(payloads):
    """Whether the price column is worth a column at all."""
    return any(p.get("price") is not None for p in payloads)


def _result_row(hit, peak, mark=None, muted=False, price=True):
    """One table row for a search hit, with an optional status mark."""
    p = hit.payload
    color = MUTED if muted else INK
    return ((_cell(mark, color=color, nowrap=True)
             if mark is not None else "")
            + _score_cell(hit.score, peak)
            + _cell(p.get("category", "-"), color=MUTED)
            + (_cell(_price(p), align="right", color=MUTED) if price else "")
            + _cell(_memory_text(p), color=color))


def results_table(hits, title=None, caption=None):
    """Show search hits as a table: score, category, price, and the memory.

    An empty result renders as the same view with nothing in it, so asking
    before and after storing reads as one picture with a row count.
    """
    if not hits:
        return _html(
            f'<div style="{FONT};max-width:760px">'
            f'<div style="font-weight:800;font-size:15px;color:{INK};'
            f'margin-bottom:6px">{_esc(title or "No memories found")}</div>'
            f'<div style="border:1px dashed {LINE};border-radius:8px;'
            f'padding:18px;text-align:center;color:{MUTED};font-size:13.5px">'
            f'Nothing stored yet, so there is nothing to find.</div>'
            + (f'<div style="font-size:12px;color:{MUTED};margin-top:6px">'
               f'{_esc(caption)}</div>' if caption else '') + '</div>')
    peak = max((h.score for h in hits), default=1.0)
    price = _has_price([h.payload for h in hits])
    rows = [_result_row(h, peak, price=price) for h in hits]
    headers = ["Score", "Category"] + (["Price"] if price else []) + ["Memory"]
    return _html(_table(headers, rows, title, caption))


def memories_table(memories, title=None):
    """Show stored memories, which carry no score: category, price, words."""
    price = _has_price(memories)
    rows = [_cell(m.get("category", "-"), color=MUTED)
            + (_cell(_price(m), align="right", color=MUTED) if price else "")
            + _cell(_memory_text(m)) for m in memories]
    headers = ["Category"] + (["Price"] if price else []) + ["Memory"]
    return _html(_table(headers, rows, title))


def before_after(query, before_hits, after_hits, title, kept="kept",
                 dropped="removed"):
    """One table showing what a change did: every memory from `before_hits`,
    marked kept or removed by whether it survived into `after_hits`.

    Scores stay the ones each memory scored, so a reader can see the
    runners-up are untouched. Memories the change let through for the first
    time are added at the bottom.
    """
    survivors = {h.id for h in after_hits}
    peak = max((h.score for h in before_hits), default=1.0)
    price = _has_price([h.payload for h in before_hits + after_hits])
    rows = [_result_row(h, peak, price=price,
                        mark=f"✅ {kept}" if h.id in survivors
                        else f"❌ {dropped}",
                        muted=h.id not in survivors)
            for h in before_hits]
    seen = {h.id for h in before_hits}
    rows += [_result_row(h, peak, price=price, mark=f"✅ {kept}")
             for h in after_hits if h.id not in seen]
    headers = ["", "Score", "Category"] + (["Price"] if price else []) + ["Memory"]
    return _html(_table(headers, rows, title,
                        caption=f'question: "{query}"'))


def receipt_table(rows, title="Restart receipt"):
    """Render a list of (label, value) pairs as a two-column table."""
    cells = [_cell(label, color=MUTED)
             + _cell(value, weight=700) for label, value in rows]
    return _html(_table(["", ""], cells, title))


def _thumb_data_uri(path, size=120):
    """Return a base64 data URI for a small thumbnail of an image file."""
    import base64
    import io
    from PIL import Image
    img = Image.open(path).convert("RGB")
    img.thumbnail((size, size))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def show_photo_results(hits, image_dir, query):
    """Show the photo a description retrieved, large, with its score.

    Only the closest match is shown: the search always returns something, and
    a big single answer says that more clearly than a row of runners-up.
    """
    hero = hits[0]
    uri = _thumb_data_uri(Path(image_dir) / hero.payload["file"], size=420)
    return _html(
        f'<div style="{FONT};max-width:460px">'
        f'<div style="font-size:12px;color:{MUTED};text-transform:uppercase;'
        f'letter-spacing:.04em">closest photo to your description</div>'
        f'<div style="font-size:17px;font-weight:700;color:{INK};'
        f'margin:2px 0 8px">"{_esc(query)}"</div>'
        f'<img src="{uri}" style="width:100%;border-radius:10px;display:block">'
        f'<div style="margin-top:8px;font-size:13.5px;color:{INK}">'
        f'{_esc(hero.payload["file"])} · similarity '
        f'<span style="color:{QDRANT_RED};font-weight:700">'
        f'{hero.score:.3f}</span></div></div>')


def vector_preview(text, vector, shown=8, name="text vector"):
    """One memory beside the start of the vector it became.

    The caption names the vector and counts its numbers, because those are two
    different things and the lesson leans on the difference: one note becomes
    one vector, and that vector is a list of numbers.
    """
    numbers = ", ".join(f"{x:+.3f}" for x in vector[:shown])
    return _html(
        f'<div style="{FONT};max-width:760px">'
        f'<div style="font-size:13.5px;color:{INK};margin-bottom:6px">'
        f'"{_esc(text)}"</div>'
        f'<div style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace;'
        f'font-size:12.5px;color:{QDRANT_RED};background:#FAFAFB;'
        f'border:1px solid {LINE};border-radius:8px;padding:10px">'
        f'[{numbers}, ...]</div>'
        f'<div style="font-size:12px;color:{MUTED};margin-top:6px">'
        f'one {_esc(name)} · showing {shown} of its {len(vector)} numbers'
        f'</div></div>')


def point_card(record, vector_name="text", shown=6):
    """One stored point in full: its id, its vector, and its payload."""
    vector = record.vector[vector_name]
    numbers = ", ".join(f"{x:+.3f}" for x in vector[:shown])
    rows = [_cell(k, color=MUTED, nowrap=True) + _cell(v)
            for k, v in record.payload.items()]
    return _html(
        f'<div style="{FONT};max-width:760px">'
        f'<div style="font-weight:800;font-size:15px;color:{INK}">'
        f'Point {_esc(record.id)}</div>'
        f'<div style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace;'
        f'font-size:12.5px;color:{QDRANT_RED};background:#FAFAFB;'
        f'border:1px solid {LINE};border-radius:8px;padding:10px;'
        f'margin:8px 0">{_esc(vector_name)}: [{numbers}, ...] '
        f'<span style="color:{MUTED}">{len(vector)} numbers</span></div>'
        + _table(["Field", "Value"], rows) + '</div>')


def _hhmm(ts, fmt="%H:%M"):
    from datetime import datetime, timezone
    return datetime.fromtimestamp(ts, timezone.utc).strftime(fmt)


def day_summary(memories):
    """One line: how many captures the day holds, by source type."""
    counts = Counter(m["source_type"] for m in memories)
    print(len(memories), "captures:",
          ", ".join(f"{v} {k}" for k, v in sorted(counts.items())))


def day_photos(memories, image_dir, title=None):
    """A wrapping strip of the day's photos, each stamped with its time."""
    photos = sorted((m for m in memories if m.get("file")),
                    key=lambda m: m["timestamp"])
    cards = "".join(
        f'<figure style="margin:0;width:104px">'
        f'<img src="{_thumb_data_uri(Path(image_dir) / m["file"], 200)}" '
        f'style="width:104px;height:104px;object-fit:cover;'
        f'border-radius:8px;display:block">'
        f'<figcaption style="font-size:11px;color:{MUTED};margin-top:3px">'
        f'{_hhmm(m["timestamp"])} · {_esc(m.get("store") or m.get("location", ""))}'
        f'</figcaption></figure>' for m in photos)
    return _html(
        f'<div style="{FONT};max-width:760px">'
        f'<div style="font-weight:800;font-size:15px;color:{INK};'
        f'margin-bottom:8px">📷 {_esc(title) if title else f"{len(photos)} photos, in time order"}</div>'
        f'<div style="display:flex;flex-wrap:wrap;gap:10px">{cards}</div></div>')


def day_notes(memories):
    """The day's voice and text notes as a table: time, kind, and words."""
    notes = sorted((m for m in memories if not m.get("file")),
                   key=lambda m: m["timestamp"])
    # A couple of notes are stamped the evening before, so the date is shown
    # whenever the set spans more than one day.
    spans_days = len({_hhmm(m["timestamp"], "%j") for m in notes}) > 1
    fmt = "%b %d · %H:%M" if spans_days else "%H:%M"
    rows = []
    for m in notes:
        kind = m["source_type"]
        rows.append(_cell(_hhmm(m["timestamp"], fmt), color=MUTED,
                          nowrap=True)
                    + _cell(f'{MODALITY_EMOJI.get(kind, "")} {kind}',
                            color=MODALITY_COLOR.get(kind, INK), weight=600,
                            nowrap=True)
                    + _cell(_memory_text(m)))
    return _html(_table(["Time", "Kind", "Note"], rows,
                        f"{len(notes)} voice and text notes"))


def answers_table(answers, image_dir=None, title="Ask your assistant"):
    """Questions answered from both lanes at once: the words and the picture.

    `answers` is a list of (question, text_hit, photo_hit). The two scores sit
    in their own columns and carry no bars, because words are scored by Nomic
    and photos by CLIP and the two numbers do not compare. When both lanes
    land on the same point, the row says so: one memory, reached two ways.
    """
    rows = []
    for question, words, photo in answers:
        p = words.payload
        when = ("you taught this" if p.get("label")
                else _hhmm(p["timestamp"], "%b %d") if p.get("timestamp")
                else "-")
        same = photo is not None and photo.id == words.id
        file = photo.payload.get("file", "") if photo is not None else ""
        if file and "/" not in file and image_dir:
            file = str(Path(image_dir) / file)
        thumb = (f'<img src="{_thumb_data_uri(file, 180)}" style="width:88px;'
                 f'height:66px;object-fit:cover;border-radius:6px;display:block">'
                 if file else "")
        tag = ('<div style="font-size:11px;color:#009688;font-weight:700;'
               'white-space:nowrap">✅ same memory</div>' if same else "")
        photo_cell = (f'<td style="padding:6px 10px;border-bottom:1px solid '
                      f'{LINE}">{thumb}<div style="font-size:11px;'
                      f'color:{QDRANT_RED};font-weight:700;margin-top:3px">'
                      f'{photo.score:.3f}</div>{tag}</td>'
                      if photo is not None else _cell("-"))
        rows.append(_cell(question, weight=600)
                    + _cell(_memory_text(p))
                    + _score_cell(words.score, None)
                    + _cell(when, color=MUTED, nowrap=True)
                    + photo_cell)
    return _html(_table(["You asked", "It remembered", "Words", "When",
                         "Photo"], rows, title))


def memory_inbox(sections, image_dir, min_score=None):
    """Render query results grouped by modality, never one blended list.

    `sections` maps a section title to a list of ScoredPoint. Every section is
    rendered even when empty. Scores below `min_score` are dimmed and tagged
    as weaker matches.
    """
    def card(h):
        p = h.payload
        # Only text/voice (Nomic) scores are thresholded; CLIP photo scores
        # live on a different scale and never meet a Nomic cutoff.
        weak = min_score is not None and not p.get("file") and h.score < min_score
        ctx = " · ".join(x for x in [_hhmm(p["timestamp"]) if p.get("timestamp") else "",
                                     p.get("store"), p.get("location"),
                                     _price(p) if p.get("price") is not None else ""]
                         if x)
        if p.get("file"):
            uri = _thumb_data_uri(Path(image_dir) / p["file"], 260)
            body = (f'<img src="{uri}" style="width:100%;height:150px;'
                    f'object-fit:cover;border-radius:8px;display:block;'
                    f'margin-top:6px">')
        else:
            body = (f'<div style="font-size:13.5px;margin-top:6px;'
                    f'color:{INK}">{_esc(_memory_text(p))}</div>')
        tag = ('<span style="font-size:11px;color:#B0088A"> · weaker match</span>'
               if weak else '')
        return (f'<div style="border:1px solid {LINE};border-radius:10px;'
                f'padding:10px;width:230px;background:#fff;'
                f'{"opacity:.5" if weak else ""}">'
                f'<div style="font-size:11px;color:{MUTED}">{_esc(ctx)}</div>'
                f'{body}<div style="font-size:12.5px;margin-top:6px">score '
                f'<span style="color:{QDRANT_RED};font-weight:700">'
                f'{h.score:.3f}</span>{tag}</div></div>')

    blocks = []
    for title, hits in sections.items():
        inner = (f'<div style="display:flex;flex-wrap:wrap;gap:10px">'
                 f'{"".join(card(h) for h in hits)}</div>' if hits else
                 f'<div style="font-size:13px;color:{MUTED};font-style:italic">'
                 f'No matches</div>')
        blocks.append(
            f'<div style="margin:12px 0">'
            f'<div style="font-weight:700;color:{INK};'
            f'border-bottom:2px solid {QDRANT_RED};display:inline-block;'
            f'margin-bottom:8px">{_esc(title)}</div>{inner}</div>')
    return _html(
        f'<div style="{FONT};background:#F7F7F8;border-radius:12px;'
        f'padding:14px 16px;max-width:760px">'
        f'<div style="font-weight:800;font-size:15px;color:{INK}">'
        f'Memory Inbox</div>{"".join(blocks)}</div>')


def show_raw(hits):
    """The plain evidence behind a grouped recall: lane, score, id, memory."""
    rows = []
    for lane, group in hits.items():
        for h in group:
            # No bar: the photo lane is CLIP, the note lanes are Nomic, and
            # the two scales do not compare.
            rows.append(_cell(lane, color=MUTED, nowrap=True)
                        + _score_cell(h.score, None)
                        + _cell(h.id, align="right", color=MUTED)
                        + _cell(_memory_text(h.payload)[:60]))
    return _html(_table(["Lane", "Score", "id", "Memory"], rows,
                        "What came back, before the inbox groups it"))


def threshold_calibration(object_dir, scene_dir, selected, current=None):
    """Calibrate image recognition on held-out and unrelated photos.

    Each bundled object keeps its last view out of the teaching set. Positive
    scores compare that held-out view with its own taught views. Negative
    scores compare held-out and scene photos with taught views of a different
    object. `current` may be `(label, score)` for the student's held-out photo.
    """
    groups = {}
    for path in sorted(Path(object_dir).glob("*.jpg")):
        groups.setdefault(path.stem.rsplit("_", 1)[0], []).append(path)

    taught = {label: views[:-1] for label, views in groups.items()}
    held_out = {label: views[-1] for label, views in groups.items()}
    scenes = sorted(Path(scene_dir).glob("*.jpg"))
    paths = [p for views in groups.values() for p in views] + scenes
    vectors = dict(zip(paths, embed_image([str(p) for p in paths])))

    def cosine(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        return dot / (na * nb)

    same = []
    different = []
    for label, query in held_out.items():
        same.append(max(cosine(vectors[query], vectors[p])
                        for p in taught[label]))
        different.extend(
            cosine(vectors[query], vectors[p])
            for other, views in taught.items() if other != label
            for p in views)
    different.extend(
        cosine(vectors[scene], vectors[p])
        for scene in scenes for views in taught.values() for p in views)

    same_min = min(same)
    different_max = max(different)
    fig, ax = plt.subplots(figsize=(FIG_W, 3.2))

    # Hundreds of negative dots hide the boundary that matters. Show their
    # tested range and hardest example instead, then keep each positive test.
    different_min = max(0.4, min(different))
    ax.hlines(0, different_min, different_max, color="#C8CEDD",
              linewidth=12, alpha=0.65)
    ax.scatter([different_max], [0], s=70, color="#8F98B2",
               edgecolors="white", linewidths=0.8, zorder=3)
    same_y = [0.96 + 0.04 * (i % 3) for i in range(len(same))]
    ax.scatter(same, same_y, s=58, color="#009688",
               edgecolors="white", linewidths=0.8, zorder=3)
    if different_max < same_min:
        ax.axvspan(different_max, same_min, color="#009688", alpha=0.09)
    ax.axvline(selected, color=QDRANT_RED, lw=2, ls="--")
    ax.annotate(f"highest {different_max:.3f}",
                xy=(different_max, 0), xytext=(-5, 14),
                textcoords="offset points", ha="right", color=MUTED,
                fontsize=9)
    ax.annotate(f"lowest {same_min:.3f}",
                xy=(same_min, 1), xytext=(5, -18),
                textcoords="offset points", ha="left", color="#00796B",
                fontsize=9)
    if current:
        ax.scatter([current[1]], [1.25], marker="*", s=170,
                   color=QDRANT_RED, edgecolors="white", linewidths=0.8,
                   zorder=4)
        ax.annotate(f"your view {current[1]:.3f}",
                    xy=(current[1], 1.25), xytext=(7, 0),
                    textcoords="offset points", va="center",
                    color=QDRANT_RED, fontsize=9, fontweight="bold")
    ax.set_xlim(0.4, 1.0)
    ax.set_ylim(-0.35, 1.50)
    ax.set_yticks([0, 1])
    ax.set_yticklabels([f"{len(different)} non-matches",
                        f"{len(same)} held-out matches"])
    ax.set_xlabel("similarity to nearest taught view")
    ax.set_title("Where should the threshold go?", loc="left")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    plt.show()


def latency_hist(timings_ms, points_count, embed_ms=None):
    """Histogram of live recall timings with the median marked.

    Pass `embed_ms`, also measured live, to add the budget line: embedding the
    question costs far more than the lookup, and a reader planning a real loop
    needs to see which term wins. Both halves are local, so this stays a
    where-the-time-goes breakdown and never a comparison against a server.
    """
    timings = sorted(timings_ms)
    median = timings[len(timings) // 2]
    fig, ax = plt.subplots(figsize=(FIG_W, 3.2 if embed_ms is None else 3.9))
    ax.hist(timings, bins=30, color="#8F98B2", edgecolor="white")
    ax.axvline(median, color=QDRANT_RED, lw=2, ls="--")
    ax.text(median, ax.get_ylim()[1] * 0.92, f"  median {median:.2f} ms",
            color=QDRANT_RED, fontsize=11, fontweight="bold", va="top")
    ax.set_title(f"Vector lookup at {points_count:,} memories "
                 f"({len(timings)} queries, CPU only)", loc="left")
    ax.set_xlabel("milliseconds per lookup (query embedding not included)")
    ax.set_ylabel("queries")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    if embed_ms is not None:
        # The budget goes under the axes, where it has the full width.
        total = embed_ms + median
        fig.subplots_adjust(bottom=0.36)
        fig.text(0.012, 0.10,
                 f"embed {embed_ms:.2f} ms + lookup {median:.2f} ms"
                 f" = {total:.2f} ms per answer",
                 fontsize=11, fontweight="bold", color=INK)
        fig.text(0.012, 0.02,
                 f"embedding is {embed_ms / median:.0f}x the lookup"
                 f" · about {1000 / total:.0f} answers per second",
                 fontsize=10, color="#4E5366")
    plt.show()


def show_images(paths, captions=None, per_row=None, title=None, height=170):
    """A row of photos with a caption under each, sized to the video frame.

    Every photo gets the same box, whatever its shape, so a row reads as a row
    rather than a ragged stack. `contain` keeps the whole subject visible,
    which matters when the photo is the evidence.
    """
    paths = list(paths)
    # Fill the row with what there is, rather than leaving a hole for photos
    # that were never uploaded.
    per_row = per_row or min(len(paths), 4) or 1
    gap = 14
    cards = []
    for i, path in enumerate(paths):
        caption = captions[i] if captions and i < len(captions) else ""
        cards.append(
            f'<figure style="margin:0;flex:0 0 auto;'
            f'width:calc((100% - {gap * (per_row - 1)}px) / {per_row})">'
            f'<img src="{_thumb_data_uri(path, 460)}" style="width:100%;'
            f'height:{height}px;object-fit:contain;background:#FAFAFB;'
            f'border-radius:10px;display:block">'
            f'<figcaption style="font-size:12.5px;font-weight:600;color:{INK};'
            f'margin-top:6px;overflow:hidden;text-overflow:ellipsis;'
            f'white-space:nowrap">{_esc(caption)}</figcaption></figure>')
    head = (f'<div style="font-weight:800;font-size:15px;color:{INK};'
            f'margin-bottom:8px">📷 {_esc(title)}</div>' if title else '')
    return _html(f'<div style="{FONT};max-width:760px">{head}'
                 f'<div style="display:flex;flex-wrap:wrap;gap:{gap}px">'
                 f'{"".join(cards)}</div></div>')


def recognition_result(query_photo, top, known, image_dir=None,
                       threshold=None, expected=None):
    """The photo you showed beside the closest memory, with the verdict.

    `known=None` shows the nearest memory without making a decision. Otherwise
    `known` is whether the score cleared the threshold. Both photos get the
    same box so the pair reads as a comparison.
    """
    stored = top.payload["file"]
    if image_dir:
        stored = str(Path(image_dir) / stored)
    label = top.payload.get("label", "UNKNOWN")
    if known is None:
        verdict, color, mark = f"Closest memory: {label}", INK, ""
    elif known:
        verdict, color, mark = label, "#009688", "✅"
    else:
        verdict, color, mark = "UNKNOWN", MUTED, "❓"

    def pane(path, caption):
        return (f'<figure style="margin:0;width:290px">'
                f'<img src="{_thumb_data_uri(path, 460)}" style="width:100%;'
                f'height:210px;object-fit:contain;background:#FAFAFB;'
                f'border-radius:10px;display:block">'
                f'<figcaption style="font-size:13px;color:{MUTED};'
                f'margin-top:6px">{_esc(caption)}</figcaption></figure>')

    detail = ""
    if known is None:
        if expected and label == expected:
            detail = ("Retrieval found the right memory. Next, choose when "
                      "a match is close enough to accept.")
        else:
            detail = ("Nearest search always returns something. Your subject "
                      "has not been taught yet.")
        detail = (f'<div style="font-size:13px;color:{MUTED};font-weight:650;'
                  f'margin:0 0 10px">{_esc(detail)}</div>')
    elif threshold is not None:
        delta = abs(top.score - threshold)
        if known:
            detail = (f'Similarity {top.score:.3f} clears the '
                      f'{threshold:.3f} threshold by {delta:.3f}.')
        else:
            detail = (f'The closest memory scores {top.score:.3f}, below the '
                      f'{threshold:.3f} threshold.')
        detail = (f'<div style="font-size:13px;color:{color};font-weight:650;'
                  f'margin:0 0 10px">{_esc(detail)}</div>')

    heading = f"{mark} " if mark else ""
    score_detail = (f" · similarity {top.score:.3f}" if known is None else
                    f" · closest memory: {_esc(label)}"
                    f" · similarity {top.score:.3f}")
    return _html(
        f'<div style="{FONT};max-width:620px">'
        f'<div style="font-size:19px;font-weight:800;color:{color};'
        f'margin-bottom:10px">{heading}{_esc(verdict)}'
        f'<span style="font-size:14px;font-weight:600;color:{MUTED}">'
        f'{score_detail}</span></div>{detail}'
        f'<div style="display:flex;gap:16px">'
        + pane(query_photo, "the photo you showed it")
        + pane(stored, f"closest memory: {label}")
        + '</div></div>')


# Speech to text for the voice notes -----------------------------------
WHISPER_MODEL = "whisper-base"


@lru_cache(maxsize=1)
def _asr_model():
    import onnx_asr
    return onnx_asr.load_model(WHISPER_MODEL, providers=["CPUExecutionProvider"])


def transcribe(audio_path):
    """Transcribe one audio file to text with a local Whisper model."""
    return _asr_model().recognize(audio_path).strip()


def transcribe_notes(memories, audio_dir):
    """Transcribe every voice note in place, then free the speech model.

    Releasing Whisper before the embedding models load keeps the notebook
    inside the 4 GB sandbox budget.
    """
    voice = [m for m in memories if m["source_type"] == "voice"]
    for m in voice:
        m["transcript"] = transcribe(f"{audio_dir}/{m['audio_file']}")
    _asr_model.cache_clear()
    return voice
