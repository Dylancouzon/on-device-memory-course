"""Lesson helpers, generated from .build/utils by gen_helpers.py.

Edit the source modules under .build/utils and regenerate; do not edit
this file directly."""


# --- embeddings ----------------------------------------
"""On-device embedding models.

L2 uses Nomic-Embed-Text v1.5 through FastEmbed: a small ONNX text model that
runs locally with no account and no network after the first download. The model
loads lazily and once (4 GB sandbox budget, one model in memory at a time).

L3 extends this module with CLIP (image / cross-modal).
"""
from functools import lru_cache

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


# --- CLIP: shared text/image space for cross-modal recall (L3+) -----------------
# Nomic and CLIP scores are NOT comparable, so photos live in their own named
# vector and text queries are embedded twice, once per space. See the course
# cross-modal retrieval policy.
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

    The container has no camera, so pasting an image URL stands in for a
    capture: the bytes are fetched once, normalized to RGB JPEG, and the
    local path is returned so it embeds and displays like a bundled photo.
    A path to a file already on disk passes straight through.
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
            "ends in .jpg or .png), or save your photos into this lesson's "
            "folder and list their filenames instead of links."
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


EXAMPLE_OBJECT = "../data/objects/rubberduck_"


def object_photos(teach_photos, test_photo):
    """Resolve a subject's photos to local files, ready to embed and show.

    Pass two or more photos of one subject in `teach_photos` and one more in
    `test_photo`, either as image links or as filenames saved beside the
    notebook. Leave them empty to fall back to the bundled example. Links
    are fetched once; local paths pass through.
    """
    example = not (teach_photos or test_photo)
    if example:
        teach_photos = [EXAMPLE_OBJECT + "1.jpg", EXAMPLE_OBJECT + "2.jpg"]
        test_photo = EXAMPLE_OBJECT + "3.jpg"
    elif not (teach_photos and test_photo):
        raise ValueError(
            "Fill in both TEACH_PHOTOS (two or more photos) and TEST_PHOTO "
            "(one more), or leave both empty to use the bundled example."
        )
    resolved = [load_image(p) for p in teach_photos]
    print(f"{len(resolved)} teach photos + 1 test photo ready"
          + (" (bundled example: rubber duck)" if example else ""))
    return resolved, load_image(test_photo)

# --- qdrant_helpers ----------------------------------------
"""Non-Qdrant plumbing for the lessons: an offline guard, benchmark filler, and
cleanup.

Every Qdrant Edge call (create a shard, upsert points, query, filter, count) is
written out in the notebooks themselves so the API stays visible. This module
holds only the supporting pieces that would otherwise clutter a cell. Validated
against qdrant-edge-py 0.7.2.
"""
import gc
import inspect
import shutil
import socket
from contextlib import contextmanager
from pathlib import Path

from qdrant_edge import EdgeShard, Point, UpdateOperation


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

# --- viz ----------------------------------------
"""Course visualizations.

Every figure carries a provenance badge (design principle 7): each number is
labelled as measured live or illustrative. The badge is baked into the figure
so no chart can ship unlabelled.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# provenance -> (label, color)
BADGES = {
    "measured": ("Measured in notebook", "#008A53"),
    "illustrative": ("Illustrative", "#8F98B2"),
}
QDRANT_RED = "#DC244C"


def receipt_table(rows, title="Restart receipt", provenance="measured"):
    """Render a forensic key/value table as a figure with a provenance badge.

    `rows` is a list of (label, value) pairs.
    """
    import textwrap
    # Wrap long values so nothing overflows the value column.
    wrapped = [(str(label), textwrap.fill(str(value), 44)) for label, value in rows]
    extra = sum(v.count("\n") for _, v in wrapped)
    fig, ax = plt.subplots(figsize=(8.5, 0.5 + 0.45 * (len(rows) + extra)))
    ax.axis("off")
    ax.set_title(title, fontweight="bold", loc="left", pad=18)
    table = ax.table(
        cellText=[[label, value] for label, value in wrapped],
        colLabels=["", ""], colWidths=[0.42, 0.58], cellLoc="left", loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.6)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#dddddd")
        if r == 0:
            cell.set_height(0.001)  # hide empty header row
        if c == 0:
            cell.set_text_props(color="#555555")
        else:
            cell.set_text_props(fontweight="bold")
    label, color = BADGES[provenance]
    ax.text(1.0, 1.04, label, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=8, color="white",
            bbox=dict(boxstyle="round,pad=0.3", fc=color, ec="none"))
    plt.show()


def memory_rows(hits):
    """Format hits as 'category · price · note' rows, ready to print."""
    rows = []
    for h in hits:
        p = h.payload
        price = f"${p['price']:.0f}" if "price" in p else "no price"
        text = p.get("note") or p["transcript"]
        rows.append(f"{p['category']:>8} · {price:>8}   {text[:52]}")
    return rows


def before_after(query, before_title, before_items, after_title, after_items,
                 legend="✗ dropped by the filter · ✓ passed the filter"):
    """Print two result lists stacked one above the other as plain text, so a
    change's effect reads at a glance.

    Items in `before_items` that are absent from `after_items` are marked with
    a leading ✗; kept items in the second list get a ✓. Pass `legend` when the
    change isn't a filter (e.g. a deletion).
    """
    kept = {str(s) for s in after_items}
    print(f'query: "{query}"')
    print(f"{legend}\n")
    print(f"{before_title}:")
    for b in before_items:
        mark = "✗" if str(b) not in kept else " "
        print(f"  {mark} {b}")
    print(f"\n{after_title}:")
    for a in after_items:
        print(f"  ✓ {a}")


def show_photo_results(hits, image_dir, query):
    """Show the photos a text query retrieved: the top hit as a hero, the rest muted.

    The winning photo is large, with its filename and score; runners-up sit in a
    small dimmed strip so the cross-modal match reads in one glance.
    """
    from PIL import Image
    hero, rest = hits[0], hits[1:]
    fig = plt.figure(figsize=(9, 4.4))
    gs = fig.add_gridspec(max(len(rest), 1), 3)

    hax = fig.add_subplot(gs[:, :2])
    him = Image.open(Path(image_dir) / hero.payload["file"])
    him.thumbnail((520, 520))
    hax.imshow(him)
    hax.set_title(f'best match  ·  {hero.payload["file"]}  ·  score {hero.score:.3f}',
                  fontsize=12, fontweight="bold", loc="left", color=QDRANT_RED)
    hax.axis("off")

    for i, hit in enumerate(rest):
        ax = fig.add_subplot(gs[i, 2])
        img = Image.open(Path(image_dir) / hit.payload["file"])
        img.thumbnail((200, 200))
        ax.imshow(img, alpha=0.55)
        ax.set_title(f'{hit.payload["file"]} · {hit.score:.3f}', fontsize=8, color="#888")
        ax.axis("off")

    fig.suptitle(f'text query -> photos:  "{query}"', fontsize=12, x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    plt.show()


MODALITY_COLOR = {"photo": QDRANT_RED, "voice": "#8547FF", "text": "#28324D"}


def _thumb_data_uri(path, size=120):
    """Return a base64 data URI for a small thumbnail of an image file."""
    import base64
    import io
    from PIL import Image
    img = Image.open(path).convert("RGB")
    img.thumbnail((size, size))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def day_timeline(memories, image_dir):
    """Two-lane strip of a day's captured memories, in time order.

    Photos sit in an upper lane (thumbnails + store label); voice and text
    notes sit in a lower lane as numbered markers. A compact legend under the
    axis maps each number to its time and full text, so no label collides.
    Each memory is a dict with `timestamp`, `source_type`, and either `file`
    (photo) or `note`/`transcript` (voice/text).
    """
    from datetime import datetime, timezone
    from matplotlib.offsetbox import OffsetImage, AnnotationBbox
    from PIL import Image

    def hhmm(ts):
        return datetime.fromtimestamp(ts, timezone.utc).strftime("%H:%M")
    def hour(ts):
        d = datetime.fromtimestamp(ts, timezone.utc)
        return d.hour + d.minute / 60

    mems = sorted(memories, key=lambda m: m["timestamp"])
    fig, ax = plt.subplots(figsize=(11, 4.2))
    ax.axhline(0, color="#cccccc", lw=2, zorder=0)

    note_legend, n, photo_i = [], 0, 0
    for m in mems:
        st, h = m["source_type"], hour(m["timestamp"])
        color = MODALITY_COLOR.get(st, "#28324D")
        if st == "photo" and m.get("file"):
            # Stagger neighboring thumbnails on two heights so close-in-time
            # photos never overlap.
            y_img = 0.6 if photo_i % 2 == 0 else 0.92
            photo_i += 1
            ax.scatter([h], [0.15], s=40, color=color, zorder=3)
            im = Image.open(Path(image_dir) / m["file"]).convert("RGB")
            im.thumbnail((52, 52))
            ax.add_artist(AnnotationBbox(OffsetImage(im, zoom=1), (h, y_img),
                                         frameon=True, pad=0.1, zorder=4))
            ax.annotate(m.get("store", ""), (h, y_img + 0.22), ha="center", va="bottom",
                        fontsize=8, color=color)
        else:
            n += 1
            ax.scatter([h], [-0.15], s=90, color=color, zorder=3)
            ax.annotate(str(n), (h, -0.32), ha="center", va="top",
                        fontsize=9, fontweight="bold", color=color)
            text = (m.get("note") or m.get("transcript") or "")
            note_legend.append((n, hhmm(m["timestamp"]), st, text))

    ax.set_ylim(-0.5, 1.4)
    ax.set_yticks([])
    ax.set_xlabel("Time of day (hour)")
    ax.set_title("A day of captured memories: photos above, notes below", loc="left")
    ax.spines[["top", "right", "left"]].set_visible(False)
    handles = [Patch(color=c, label=k.capitalize()) for k, c in MODALITY_COLOR.items()]
    ax.legend(handles=handles, loc="upper right", fontsize=8, ncol=3)

    # Compact legend of the numbered notes, full text wrapped, anchored at the
    # figure bottom so it never collides with the x-axis label. The legend is
    # capped so a busy day stays readable and the layout never inverts.
    import textwrap
    LEGEND_MAX = 12
    lines = []
    for i, t, st, txt in note_legend[:LEGEND_MAX]:
        lines += textwrap.wrap(f"{i}. {t} · {st:>5} · {txt}", 104,
                               subsequent_indent="        ") or [""]
    if len(note_legend) > LEGEND_MAX:
        lines.append(f"        ... and {len(note_legend) - LEGEND_MAX} more notes")
    bottom = min(0.82, 0.12 + 0.035 * len(lines))
    fig.subplots_adjust(bottom=bottom, top=0.93)
    fig.text(0.02, 0.02, "\n".join(lines), va="bottom", ha="left",
             fontsize=8.5, family="monospace", color="#333333")
    plt.show()


INBOX_SECTIONS = ("Photos", "Voice Notes", "Text Notes")


def _mem_when(payload):
    """Format a memory's timestamp as HH:MM, or '' if it has none."""
    from datetime import datetime, timezone
    ts = payload.get("timestamp")
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%H:%M") if ts else ""


def _mem_context(payload):
    """The store / location / price line for a memory (only the fields present)."""
    parts = [payload.get("store"), payload.get("location")]
    if payload.get("price") is not None:
        parts.append(f"${payload['price']:.0f}")
    return " · ".join(p for p in parts if p)


def memory_inbox(sections, image_dir, min_score=None):
    """Render query results grouped by modality (never one blended list). Returns HTML.

    `sections` maps a section title to a list of ScoredPoint. Every section in
    INBOX_SECTIONS is rendered even when empty ("No matches"). Each card shows
    the memory's timestamp, its store/location/price context, and its score.
    Scores below `min_score` are dimmed and tagged as weaker matches. Scores are
    measured live in the notebook, so the header carries that provenance badge.
    """
    import html as html_lib
    from IPython.display import HTML

    def card(h):
        p = h.payload
        # Only text/voice (Nomic) scores are thresholded; CLIP photo scores live
        # on a different scale and are never marked weak against a Nomic cutoff.
        weak = min_score is not None and not p.get("file") and h.score < min_score
        when = _mem_when(p)
        ctx = _mem_context(p)
        head = (f'<div style="font-size:11px;color:#888">{when}'
                + (f' · {ctx}' if ctx else '') + '</div>')
        if p.get("file"):
            uri = _thumb_data_uri(Path(image_dir) / p["file"])
            body = f'<img src="{uri}" style="height:96px;border-radius:6px;display:block;margin-top:4px">'
        else:
            text = html_lib.escape(p.get("transcript") or p.get("note") or "")
            body = f'<div style="max-width:240px;font-size:13px;margin-top:4px">{text}</div>'
        tag = ('<span style="font-size:10px;color:#b08">weaker match</span>' if weak else '')
        score = f'<span style="color:#DC244C;font-weight:700">{h.score:.3f}</span>'
        return (f'<div style="border:1px solid #e0e0e0;border-radius:8px;padding:8px;'
                f'margin:4px;background:#fff;{"opacity:.55" if weak else ""}">{head}{body}'
                f'<div style="font-size:12px;margin-top:4px">score {score} {tag}</div></div>')

    blocks = []
    for title in INBOX_SECTIONS:
        hits = sections.get(title, [])
        if hits:
            inner = f'<div style="display:flex;flex-wrap:wrap">{"".join(card(h) for h in hits)}</div>'
        else:
            inner = '<div style="font-size:13px;color:#aaa;font-style:italic;margin:4px">No matches</div>'
        blocks.append(
            f'<div style="margin:10px 0">'
            f'<div style="font-weight:700;color:#28324D;border-bottom:2px solid #DC244C;'
            f'display:inline-block;margin-bottom:6px">{title}</div>{inner}</div>')
    _badge_label, _badge_color = BADGES["measured"]
    header = (
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">'
        '<span style="font-weight:800;font-size:15px">Memory Inbox</span>'
        f'<span style="font-size:11px;color:#fff;background:{_badge_color};'
        f'border-radius:10px;padding:2px 8px">{_badge_label}</span></div>')
    return HTML(
        '<div style="font-family:system-ui,sans-serif;background:#f7f7f8;'
        'border-radius:12px;padding:12px 16px">' + header + "".join(blocks) + "</div>")


def show_raw(hits):
    """Print the plain evidence for a grouped recall: space, score, id, text."""
    for space, rows in hits.items():
        for h in rows:
            p = h.payload
            label = (p.get("store") or p.get("note")
                     or p.get("transcript") or p.get("file", ""))[:34]
            print(f"{space:11} {h.score:.3f} id={h.id}  {label}")


def score_gap_chart(taught, foreign, threshold):
    """Horizontal score bars for recognition evidence: taught held-out photos
    vs never-taught images, with the threshold line drawn inside the gap.

    `taught` and `foreign` are lists of (label, score); scores are measured
    live in the notebook.
    """
    rows = [(lbl, s, True) for lbl, s in taught] + \
           [(lbl, s, False) for lbl, s in foreign]
    fig, ax = plt.subplots(figsize=(8.5, 0.55 * len(rows) + 1.2))
    ys = range(len(rows))
    ax.barh(list(ys),
            [s for _, s, _ in rows],
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
    handles = [Patch(color="#009688", label="taught (held-out photo)"),
               Patch(color="#8F98B2", label="never taught")]
    ax.legend(handles=handles, loc="lower right", fontsize=9)
    label, color = BADGES["measured"]
    ax.text(1.0, 1.02, label, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=8, color="white",
            bbox=dict(boxstyle="round,pad=0.3", fc=color, ec="none"))
    fig.tight_layout()
    plt.show()


def latency_hist(timings_ms, points_count, embed_ms=None):
    """Histogram of live recall timings with the median marked.

    `timings_ms` are per-query latencies measured in the notebook; the median
    is the course's one honest local latency number, so it is drawn on the
    chart rather than printed beside it. Pass `embed_ms`, also measured live,
    to add the budget line: embedding the question costs far more than the
    lookup, and a reader planning a real loop needs to see which term wins.
    Both halves are local, so this stays a where-the-time-goes breakdown and
    never a comparison against a server.
    """
    timings = sorted(timings_ms)
    median = timings[len(timings) // 2]
    fig, ax = plt.subplots(figsize=(8.5, 3.2 if embed_ms is None else 3.9))
    ax.hist(timings, bins=30, color="#8F98B2", edgecolor="white")
    ax.axvline(median, color=QDRANT_RED, lw=2, ls="--")
    ax.text(median, ax.get_ylim()[1] * 0.92, f"  median {median:.2f} ms",
            color=QDRANT_RED, fontsize=11, fontweight="bold", va="top")
    ax.set_title(f"Vector lookup at {points_count:,} memories "
                 f"({len(timings)} queries, CPU only)", loc="left")
    ax.set_xlabel("milliseconds per lookup (query embedding not included)")
    ax.set_ylabel("queries")
    ax.spines[["top", "right"]].set_visible(False)
    label, color = BADGES["measured"]
    ax.text(1.0, 1.04, label, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=8, color="white",
            bbox=dict(boxstyle="round,pad=0.3", fc=color, ec="none"))
    fig.tight_layout()
    if embed_ms is not None:
        # The budget goes under the axes, where it has the full width and does
        # not run into the badge.
        total = embed_ms + median
        fig.subplots_adjust(bottom=0.36)
        fig.text(0.012, 0.10,
                 f"embed {embed_ms:.2f} ms + lookup {median:.2f} ms"
                 f" = {total:.2f} ms per answer",
                 fontsize=11, fontweight="bold", color="#28324D")
        fig.text(0.012, 0.02,
                 f"embedding is {embed_ms / median:.0f}x the lookup"
                 f" · about {1000 / total:.0f} answers per second",
                 fontsize=10, color="#4E5366")
    plt.show()


def show_images(paths, captions=None, height=2.2, per_row=6):
    """One row of images with optional captions under each, wrapping to a new
    row past `per_row`. White background, axes off. For showing inputs a student
    hasn't seen yet, so there is no provenance badge (these aren't results).
    """
    from PIL import Image
    paths = list(paths)
    n = len(paths)
    cols = min(per_row, n) or 1
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, squeeze=False,
                             figsize=(height * cols, height * rows))
    fig.patch.set_facecolor("white")
    for i, ax in enumerate(ax for row in axes for ax in row):
        ax.axis("off")
        if i < n:
            img = Image.open(paths[i]).convert("RGB")
            img.thumbnail((int(height * 110), int(height * 110)))
            ax.imshow(img)
            if captions and i < len(captions):
                ax.set_title(str(captions[i]), fontsize=8, fontweight="bold")
    fig.tight_layout()
    plt.show()
