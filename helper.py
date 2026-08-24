"""Helper functions for the course notebooks.

Plumbing for the lessons: the on-device embedding models, speech-to-text for
the voice notes, the result tables and charts the lessons print, and the stores
and searches the lessons repeat. Each Qdrant call is written out in the
notebook of the lesson that teaches it; after that, the repeat lives here.
"""
import gc
import inspect
import json
import shutil
import socket
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from qdrant_edge import EdgeShard, Point, Query, QueryRequest, UpdateOperation


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


def photo_uploader():
    """Two upload buttons: the photos to teach with, and the one to test with.

    Photos land in ./my_photos and stay on the device. Holding one photo back
    is the point of the lab: the device meets it once before it has been
    taught anything, and once after. Leave both empty for the bundled example.
    """
    import ipywidgets as widgets
    from IPython.display import display

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
def load_memories(path, source_type=None):
    """Read a memories JSON file, optionally keeping one source type."""
    memories = json.load(open(path))
    if source_type:
        memories = [m for m in memories if m["source_type"] == source_type]
    return memories


def store_notes(shard, notes):
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
    print(f"Stored {len(notes)} notes")


def store_photos(shard, folder, start_id=1000):
    """Embed a folder of photos with CLIP and store them in the image vector."""
    photos = sorted(Path(folder).glob("*.jpg"))
    vectors = embed_image([str(p) for p in photos])
    shard.update(UpdateOperation.upsert_points([
        Point(id=start_id + i, vector={"image": v},
              payload={"file": p.name, "source_type": "photo"})
        for i, (p, v) in enumerate(zip(photos, vectors))
    ]))
    shard.optimize()
    print(f"Stored {len(photos)} photos as {len(vectors[0])}-d CLIP image",
          f"vectors. Total: {shard.info().points_count} memories")


def store_photo_memories(shard, photos, folder):
    """Embed photo memories with CLIP and store one point per photo."""
    vectors = embed_image([f"{folder}/{m['file']}" for m in photos])
    shard.update(UpdateOperation.upsert_points([
        Point(id=m["id"], vector={"image": v}, payload=m)
        for m, v in zip(photos, vectors)
    ]))
    shard.optimize()
    print(f"Stored {len(photos)} photos.",
          f"Total: {shard.info().points_count} memories")


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


def recognize(shard, photo, threshold):
    """The closest stored photo to this one, and whether it clears the bar.

    The nearest-vector query is Lesson 3's; searching the image vector is
    Lesson 4's. What Lesson 6 adds is the threshold: below it, the device
    says it does not know this object rather than guessing.
    """
    top = shard.query(QueryRequest(
        query=Query.Nearest(embed_image([photo])[0], using="image"),
        limit=1,
        with_payload=True,
    ))[0]
    return top, top.score >= threshold


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


def fetch_snapshot(base_url, api_key, collection, dest, manifest=None):
    """Download a shard snapshot from a Qdrant server to a local file.

    With a manifest (from `EdgeShard.snapshot_manifest`), asks the server
    for a partial snapshot holding only what this shard is missing.
    """
    import urllib.request
    headers = {"api-key": api_key or ""}
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


@contextmanager
def no_network():
    """Block new Python socket creation inside the block.

    Swaps `socket.socket` for one that raises, so any Python code that tries to
    open a new socket fails loudly. It is a demonstration guard, not an OS-level
    network cut: it does not touch sockets already open or native code paths.
    If a query still returns with it active, that query opened no new socket.
    """
    original = socket.socket

    def blocked(*args, **kwargs):
        raise OSError("Python socket creation blocked for this cell")

    socket.socket = blocked
    try:
        yield
    finally:
        socket.socket = original


# The views the lessons print ------------------------------------------
QDRANT_RED = "#DC244C"
INK = "#28324D"
MUTED = "#6B7280"
LINE = "#E5E7EB"
FONT = "font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"
FIG_W = 8.0        # recording frame is 8 wide by 9 high

MODALITY_COLOR = {"photo": QDRANT_RED, "voice": "#8547FF", "text": INK}
MODALITY_EMOJI = {"photo": "📷", "voice": "🎙️", "text": "📝"}


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
    """Show search hits as a table: score, category, price, and the memory."""
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


def _hhmm(ts, fmt="%H:%M"):
    from datetime import datetime, timezone
    return datetime.fromtimestamp(ts, timezone.utc).strftime(fmt)


def day_photos(memories, image_dir):
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
        f'margin-bottom:8px">📷 {len(photos)} photos, in time order</div>'
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


def score_gap_chart(taught, foreign, threshold):
    """Horizontal score bars for recognition evidence: the taught held-out
    photo against never-taught images, with the threshold drawn in the gap.

    `taught` and `foreign` are lists of (label, score).
    """
    rows = [(lbl, s, True) for lbl, s in taught] + \
           [(lbl, s, False) for lbl, s in foreign]
    fig, ax = plt.subplots(figsize=(FIG_W, 0.5 * len(rows) + 1.2))
    ys = range(len(rows))
    ax.barh(list(ys), [s for _, s, _ in rows],
            color=["#009688" if t else "#8F98B2" for _, _, t in rows],
            height=0.6)
    for y, (_, s, _) in zip(ys, rows):
        ax.text(s + 0.008, y, f"{s:.3f}", va="center", fontsize=9)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([lbl for lbl, _, _ in rows])
    ax.invert_yaxis()
    ax.axvline(threshold, color=QDRANT_RED, lw=2, ls="--")
    ax.text(threshold - 0.012, -0.7, f"threshold {threshold}",
            color=QDRANT_RED, ha="right", fontsize=10, fontweight="bold")
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("similarity to nearest stored view")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(handles=[Patch(color="#009688", label="taught (held-out photo)"),
                       Patch(color="#8F98B2", label="never taught")],
              loc="lower right", fontsize=9)
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


def show_images(paths, captions=None, per_row=3):
    """A row of photos with a caption under each, sized to the video frame."""
    paths = list(paths)
    cards = []
    for i, path in enumerate(paths):
        caption = captions[i] if captions and i < len(captions) else ""
        width = int(720 / min(per_row, max(len(paths), 1)))
        cards.append(
            f'<figure style="margin:0;width:{width}px">'
            f'<img src="{_thumb_data_uri(path, 460)}" style="width:100%;'
            f'border-radius:10px;display:block">'
            f'<figcaption style="font-size:13px;font-weight:600;color:{INK};'
            f'margin-top:6px">{_esc(caption)}</figcaption></figure>')
    return _html(f'<div style="{FONT};display:flex;flex-wrap:wrap;gap:14px;'
                 f'max-width:760px">{"".join(cards)}</div>')


def recognition_result(query_photo, top, known, image_dir=None):
    """The photo you showed beside the closest memory, with the verdict.

    `known` is whether the score cleared the threshold. Unknown is shown as a
    real answer, not an error: the device says so rather than guessing.
    """
    stored = top.payload["file"]
    if image_dir:
        stored = str(Path(image_dir) / stored)
    verdict = top.payload.get("label", "UNKNOWN") if known else "UNKNOWN"
    color = "#009688" if known else MUTED
    mark = "✅" if known else "❓"
    return _html(
        f'<div style="{FONT};max-width:620px">'
        f'<div style="font-size:19px;font-weight:800;color:{color};'
        f'margin-bottom:10px">{mark} {_esc(verdict)}'
        f'<span style="font-size:14px;font-weight:600;color:{MUTED}">'
        f' · similarity {top.score:.3f}</span></div>'
        f'<div style="display:flex;gap:16px">'
        f'<figure style="margin:0;width:290px">'
        f'<img src="{_thumb_data_uri(query_photo, 460)}" style="width:100%;'
        f'border-radius:10px;display:block">'
        f'<figcaption style="font-size:13px;color:{MUTED};margin-top:6px">'
        f'the photo you showed it</figcaption></figure>'
        f'<figure style="margin:0;width:290px">'
        f'<img src="{_thumb_data_uri(stored, 460)}" style="width:100%;'
        f'border-radius:10px;display:block">'
        f'<figcaption style="font-size:13px;color:{MUTED};margin-top:6px">'
        f'closest memory: {_esc(top.payload.get("label", ""))}'
        f'</figcaption></figure></div></div>')


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
