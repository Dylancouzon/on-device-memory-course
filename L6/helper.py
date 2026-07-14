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


def embed_text_clip(text):
    """Embed a text query into CLIP's space, to search the image vector."""
    return next(_clip_text().query_embed([text])).tolist()

# --- qdrant_helpers ----------------------------------------
"""EdgeShard lifecycle and memory operations.

Thin wrappers over qdrant-edge-py so notebook cells stay about the concept, not
the boilerplate. Validated against qdrant-edge-py 0.7.2.
"""
import shutil
import socket
from contextlib import contextmanager
from pathlib import Path

from qdrant_edge import (
    EdgeShard, EdgeConfig, EdgeVectorParams, Distance, Point,
    UpdateOperation, Query, QueryRequest, CountRequest,
)


def create_memory_shard(directory, vectors, distance=Distance.Cosine, reset=True):
    """Create a fresh EdgeShard on disk.

    `vectors` maps a named vector to its dimension, e.g. {"text": 768}.
    `EdgeShard.create` refuses a directory that already holds data, so `reset`
    wipes it first, convenient for a notebook you re-run top to bottom.
    """
    if reset:
        shutil.rmtree(directory, ignore_errors=True)
    Path(directory).mkdir(parents=True, exist_ok=True)
    config = EdgeConfig(vectors={
        name: EdgeVectorParams(size=dim, distance=distance)
        for name, dim in vectors.items()
    })
    return EdgeShard.create(directory, config)


def add_memories(shard, vector_name, embeddings, payloads, start_id=0, optimize=True):
    """Upsert memories, one point per (embedding, payload) pair.

    Edge has no background optimizer, so we `optimize()` after the batch to build
    the index and reclaim space.
    """
    points = [
        Point(id=start_id + i, vector={vector_name: emb}, payload=payload)
        for i, (emb, payload) in enumerate(zip(embeddings, payloads))
    ]
    shard.update(UpdateOperation.upsert_points(points))
    if optimize:
        shard.optimize()
    return len(points)


def search_memories(shard, vector_name, query_vector, limit=5, query_filter=None):
    """Nearest-neighbor search over one named vector. Returns list[ScoredPoint]."""
    return shard.query(QueryRequest(
        query=Query.Nearest(query_vector, using=vector_name),
        filter=query_filter,
        limit=limit,
        with_payload=True,
        with_vector=False,
    ))


def count_memories(shard):
    """Exact point count."""
    return shard.count(CountRequest(exact=True))


def count_by(shard, key):
    """Count memories grouped by a payload field, e.g. count_by(shard, 'source_type')."""
    from collections import Counter
    from qdrant_edge import ScrollRequest
    records, _ = shard.scroll(ScrollRequest(limit=10000, with_payload=True))
    return Counter(r.payload.get(key) for r in records)


def benchmark_query(shard, vector_name, query_vector, query_filter=None, limit=3, runs=200):
    """Median query latency in milliseconds over `runs` repeats."""
    import time
    timings = []
    for _ in range(runs):
        t0 = time.perf_counter()
        search_memories(shard, vector_name, query_vector, limit=limit, query_filter=query_filter)
        timings.append((time.perf_counter() - t0) * 1000)
    timings.sort()
    return timings[len(timings) // 2]


def reopen_shard(directory):
    """Reload a closed shard from disk. Config is read back from disk."""
    return EdgeShard.load(directory)


def gather_device_knowledge(robot_shard, phone_shard, evicted):
    """Collect the closing-dashboard stats from the two on-device shards.

    Queries the robot shard for its top hazard and, when the phone shard from L5
    is present, its memory counts by modality, top purchase, and the recurring
    coffee note. Returns the dict `knowledge_dashboard` expects. Wrap the call in
    `no_network()` to prove every read stayed on-device.
    """

    robot_total = count_memories(robot_shard)
    top_hazard = distinct_objects(
        search_memories(robot_shard, "text", embed_query("hazard"), limit=8)
    )[0].payload["object_class"]

    if phone_shard is not None:
        phone_total = count_memories(phone_shard)
        mods = count_by(phone_shard, "source_type")
        buy = search_memories(phone_shard, "image", embed_text_clip("shoes to buy"), limit=1)[0].payload
        top_purchase = f"{buy['category']}, ${buy['price']:.0f}"
        coffee = search_memories(
            phone_shard, "text", embed_query("coffee place with outdoor seating"), limit=1
        )[0].payload["note"]
    else:
        phone_total, mods, top_purchase, coffee = 0, {}, "run L5 first", None

    return {
        "combined": robot_total + phone_total,
        "robot_total": robot_total,
        "phone_total": phone_total,
        "by_modality": {"photos": mods.get("photo", 0), "voice notes": mods.get("voice", 0),
                        "text notes": mods.get("text", 0), "robot observations": robot_total},
        "network": "off",
        "top_hazard": top_hazard,
        "top_purchase": top_purchase,
        "evicted": evicted,
        "recurring": coffee,
    }


def cleanup(shard, directory=None):
    """Close the shard and optionally delete its directory."""
    try:
        shard.close()
    except Exception:
        pass
    if directory:
        shutil.rmtree(directory, ignore_errors=True)


@contextmanager
def no_network():
    """Block all socket creation inside the block.

    Anything that tries to reach the network raises OSError; if a query still
    returns, it ran entirely on-device.
    """
    original = socket.socket

    def blocked(*args, **kwargs):
        raise OSError("Network disabled for this cell")

    socket.socket = blocked
    print("⚠ Network disabled for this cell")
    try:
        yield
    finally:
        socket.socket = original

# --- filters ----------------------------------------
"""Payload-filter builders.

Thin constructors over qdrant-edge-py's filter types so a notebook cell reads
like the intent ("category is shoes, price under 50") instead of nested objects.
Combine conditions with `all_of` (AND) / `any_of` (OR).
"""
from qdrant_edge import Filter, FieldCondition, MatchValue, RangeFloat


def match(key, value):
    """Exact match on a keyword/value field, e.g. match("category", "shoes")."""
    return FieldCondition(key=key, match=MatchValue(value=value))


def numeric(key, gt=None, lt=None, gte=None, lte=None):
    """Numeric range on a float field, e.g. numeric("price", lt=50)."""
    return FieldCondition(key=key, range=RangeFloat(gt=gt, lt=lt, gte=gte, lte=lte))


def time_window(start, end, key="timestamp"):
    """Memories whose timestamp falls in [start, end] (epoch seconds)."""
    return FieldCondition(key=key, range=RangeFloat(gte=start, lte=end))


def all_of(*conditions):
    """AND: every condition must hold."""
    return Filter(must=list(conditions))


def any_of(*conditions):
    """OR: at least one condition must hold."""
    return Filter(should=list(conditions))

# --- viz ----------------------------------------
"""Course visualizations.

Every figure carries a provenance badge (design principle 7): each number is
labelled as measured live or illustrative. The badge is baked into the figure
so no chart can ship unlabelled.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# provenance -> (label, color)
BADGES = {
    "measured": ("Measured in notebook", "#2ecc71"),
    "illustrative": ("Illustrative", "#95a5a6"),
}
QDRANT_RED = "#DC244C"


def _badge(ax, provenance):
    """Place a provenance badge in the margin reserved above the axes.

    Pair with `fig.tight_layout(rect=[0, 0, 1, 0.9])` so the badge never
    overlaps the title or clips at the top of the figure.
    """
    label, color = BADGES[provenance]
    ax.text(1.0, 1.06, label, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=8, color="white",
            bbox=dict(boxstyle="round,pad=0.3", fc=color, ec="none"))


def latency_showdown(measured_ms, cloud_ms=102.8, save=None):
    """Bar chart: local Edge query (measured live) vs. a real cloud round-trip.

    Both numbers are measured, not illustrative. The local bar is timed live in
    the notebook; the cloud bar is Qdrant Cloud query p50 from the edge-bench
    comparison (10k x 384-dim, one laptop to a Cloud region, measured Jul 2026),
    dominated by internet round-trip rather than engine compute. The local bar
    is tiny next to it (that gap is the point), so both values are annotated and
    the speedup is called out.
    """
    fig, ax = plt.subplots(figsize=(6.5, 4))
    labels = ["Qdrant Edge\n(local, on-device)", "Qdrant Cloud\nround-trip"]
    values = [measured_ms, cloud_ms]
    colors = [BADGES["measured"][1], "#3498db"]  # cloud bar (Qdrant Cloud)
    bars = ax.bar(labels, values, color=colors, width=0.6)
    for bar, val in zip(bars, values):
        label = f"{val:.2f} ms" if val < 10 else f"{val:.0f} ms"
        ax.text(bar.get_x() + bar.get_width() / 2, val, label,
                ha="center", va="bottom", fontweight="bold")
    # The local bar is invisible next to the cloud bar; call out the ratio as a
    # centered label over it (no arrow, so it never clips the bar's ms label).
    ratio = cloud_ms / measured_ms if measured_ms else 0
    ax.text(0, cloud_ms * 0.5, f"{ratio:,.0f}x faster\nthan the cloud round-trip",
            ha="center", va="center", fontsize=11, fontweight="bold",
            color=BADGES["measured"][1])
    ax.set_ylabel("Query latency (ms)")
    ax.set_title(f"On-device recall: {measured_ms:.2f} ms, no network round-trip", loc="left")
    ax.set_ylim(0, cloud_ms * 1.15)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(
        handles=[
            Patch(color=BADGES["measured"][1], label="Measured live in notebook (local)"),
            Patch(color="#3498db", label="Measured on Qdrant Cloud (edge-bench, Jul 2026)"),
        ],
        fontsize=8, loc="upper right", framealpha=0.9,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    if save:
        fig.savefig(save, dpi=120, bbox_inches="tight")
    plt.show()


def receipt_table(rows, title="Resurrection receipt", provenance="measured", save=None):
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
    if save:
        fig.savefig(save, dpi=120, bbox_inches="tight")
    plt.show()


def two_column_table(left_title, left_items, right_title, right_items, title="", save=None):
    """Side-by-side comparison of two result lists (e.g. before/after a filter)."""
    import textwrap
    # Wide half-columns hold a normal result line; only very long strings wrap.
    wrap = lambda s: textwrap.fill(str(s), 64)
    left_items = [wrap(s) for s in left_items]
    right_items = [wrap(s) for s in right_items]
    n = max(len(left_items), len(right_items), 1)
    data = [[left_items[i] if i < len(left_items) else "",
             right_items[i] if i < len(right_items) else ""] for i in range(n)]
    line_counts = [max(data[r][0].count("\n"), data[r][1].count("\n")) + 1 for r in range(n)]
    fig, ax = plt.subplots(figsize=(11, 0.7 + 0.34 * sum(line_counts)))
    ax.axis("off")
    if title:
        ax.set_title(title, fontweight="bold", loc="left", pad=16)
    table = ax.table(cellText=data, colLabels=[left_title, right_title],
                     colWidths=[0.5, 0.5], cellLoc="left", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    # Row height tracks wrapped-line count so multi-line cells never overlap.
    for (r, c), cell in table.get_celld().items():
        cell.set_height(0.13 if r == 0 else 0.16 * line_counts[r - 1])
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#dddddd")
        if r == 0:
            cell.set_text_props(fontweight="bold", color="white")
            cell.set_facecolor(QDRANT_RED)
    fig.tight_layout()
    if save:
        fig.savefig(save, dpi=120, bbox_inches="tight")
    plt.show()


def filter_latency_chart(unfiltered_ms, filtered_ms, save=None):
    """Two bars: same query, without vs. with a payload filter (both measured)."""
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    bars = ax.bar(["Similarity only", "Similarity + filter"],
                  [unfiltered_ms, filtered_ms], width=0.55,
                  color=["#95a5a6", QDRANT_RED])
    for bar, val in zip(bars, [unfiltered_ms, filtered_ms]):
        ax.text(bar.get_x() + bar.get_width() / 2, val, f"{val:.2f} ms",
                ha="center", va="bottom", fontweight="bold")
    ax.set_ylabel("Query latency (ms)")
    ax.set_title("Filtering runs in the same query", loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    _badge(ax, "measured")
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    if save:
        fig.savefig(save, dpi=120, bbox_inches="tight")
    plt.show()


def show_photo_results(hits, image_dir, query, save=None):
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
    if save:
        fig.savefig(save, dpi=120, bbox_inches="tight")
    plt.show()


MODALITY_COLOR = {"photo": QDRANT_RED, "voice": "#8e44ad", "text": "#2c3e50"}


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


def day_timeline(memories, image_dir, save=None):
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
        color = MODALITY_COLOR.get(st, "#2c3e50")
        if st == "photo" and m.get("file"):
            # Stagger neighbouring thumbnails on two heights so close-in-time
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
    # figure bottom so it never collides with the x-axis label.
    import textwrap
    lines = []
    for i, t, st, txt in note_legend:
        lines += textwrap.wrap(f"{i}. {t} · {st:>5} · {txt}", 104,
                               subsequent_indent="        ") or [""]
    fig.subplots_adjust(bottom=0.14 + 0.045 * len(lines), top=0.92)
    fig.text(0.02, 0.02, "\n".join(lines), va="bottom", ha="left",
             fontsize=8.5, family="monospace", color="#333333")
    if save:
        fig.savefig(save, dpi=120, bbox_inches="tight")
    plt.show()


def query_contract(semantic_query, filters, search_space):
    """Render a query as its three explicit inputs (honest-demo panel). Returns HTML."""
    from IPython.display import HTML
    rows = "".join(
        f'<tr><td style="color:#888;padding:4px 12px;white-space:nowrap">{k}</td>'
        f'<td style="padding:4px 12px;font-family:monospace">{v}</td></tr>'
        for k, v in [("semantic_query", f'"{semantic_query}"'),
                     ("filters", filters or "none"),
                     ("search_space", search_space)]
    )
    return HTML(
        f'<div style="border:1px solid #DC244C;border-radius:8px;display:inline-block;'
        f'padding:6px 10px;margin:6px 0">'
        f'<div style="color:#DC244C;font-weight:700;font-size:13px;padding:2px 12px">Query contract</div>'
        f'<table style="border-collapse:collapse;font-size:13px">{rows}</table></div>')


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


def routing_diagram():
    """Show how L3 grows L2's routing: one named vector becomes two. Returns HTML.

    L2 routed text to a single `text` vector. L3 keeps that Nomic text encoder
    and adds CLIP on a second `image` vector: no new text model, one new row.
    """
    from IPython.display import HTML

    def row(modality, model, vector, added):
        bg = "#fff5f7" if added else "#ffffff"
        tag = ('<span style="font-size:10px;color:#DC244C;font-weight:700">new in L3</span>'
               if added else '')
        return (f'<tr style="background:{bg}">'
                f'<td style="padding:6px 14px">{modality}</td>'
                f'<td style="padding:6px 14px;font-family:monospace">{model}</td>'
                f'<td style="padding:6px 14px;font-family:monospace">{vector}</td>'
                f'<td style="padding:6px 14px">{tag}</td></tr>')

    def panel(title, rows_html):
        return (f'<div style="border:1px solid #e0e0e0;border-radius:10px;padding:8px 4px;background:#fff">'
                f'<div style="font-weight:700;color:#2c3e50;padding:2px 14px 6px">{title}</div>'
                f'<table style="border-collapse:collapse;font-size:13px">'
                f'<tr style="color:#888"><td style="padding:2px 14px">memory</td>'
                f'<td style="padding:2px 14px">model</td><td style="padding:2px 14px">named vector</td>'
                f'<td></td></tr>{rows_html}</table></div>')

    before = panel("Before (L2): one vector",
                   row("Text notes", "Nomic 768-d", "text", False))
    after = panel("After (L3): two vectors, routed by modality",
                  row("Text notes", "Nomic 768-d", "text", False)
                  + row("Photos", "CLIP 512-d", "image", True))
    return HTML(
        '<div style="font-family:system-ui,sans-serif;display:flex;gap:14px;'
        'align-items:flex-start;flex-wrap:wrap">'
        + before + '<div style="align-self:center;font-size:22px;color:#DC244C">&rarr;</div>'
        + after + '</div>')


def memory_inbox(sections, image_dir, min_score=None):
    """Render query results grouped by modality (never one blended list). Returns HTML.

    `sections` maps a section title to a list of ScoredPoint. Every section in
    INBOX_SECTIONS is rendered even when empty ("No matches"). Each card shows
    the memory's timestamp, its store/location/price context, and its score.
    Scores below `min_score` are dimmed and tagged as weaker matches. Scores are
    measured live in the notebook, so the header carries that provenance badge.
    """
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
            text = p.get("transcript") or p.get("note") or ""
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
            f'<div style="font-weight:700;color:#2c3e50;border-bottom:2px solid #DC244C;'
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


def grid_frames(frames, save=None):
    """Show the grid world at each snapshot: robot path, live memories fading by value."""
    fig, axes = plt.subplots(1, len(frames), figsize=(5 * len(frames), 4.2))
    if len(frames) == 1:
        axes = [axes]
    for ax, frame in zip(axes, frames):
        # faint ground truth
        for (x, y), (cls, conf, hazard) in WORLD.items():
            ax.scatter([x], [y], s=180, marker="s",
                       color=("#f7c6cf" if hazard else "#e5e5e5"), zorder=1)
        # robot path so far
        pts = PATH[:frame["tick"] + 1]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color="#3498db", lw=1.5, zorder=2)
        rx, ry = frame["robot"]
        ax.scatter([rx], [ry], s=140, marker="^", color="#3498db", zorder=5, label="robot")
        # live memories, opacity = value
        for m in frame["memories"]:
            color = QDRANT_RED if m["is_hazard"] else "#2c3e50"
            ax.scatter([m["x"]], [m["y"]], s=150, color=color,
                       alpha=max(0.15, min(1.0, m["score"] / 0.9)), zorder=4)
        ax.set_xlim(-1, GRID_W)
        ax.set_ylim(-1, GRID_H)
        ax.set_xticks(range(GRID_W))
        ax.set_yticks(range(GRID_H))
        ax.grid(True, color="#f0f0f0")
        ax.set_title(f"t = {frame['tick']}   ({len(frame['memories'])} memories)")
        ax.set_aspect("equal")

    # Annotate the story on the last frame: one hazard that persists, one
    # ground-truth cell whose sighting has been evicted (faded to nothing).
    last, lax = frames[-1], axes[-1]
    live = {(m["x"], m["y"]) for m in last["memories"]}
    kept_haz = next((m for m in last["memories"] if m["is_hazard"]), None)
    if kept_haz:
        lax.annotate("retained hazard", (kept_haz["x"], kept_haz["y"]),
                     xytext=(kept_haz["x"], kept_haz["y"] + 1.4), ha="center", fontsize=8,
                     color=QDRANT_RED, fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color=QDRANT_RED))
    evicted = next(((x, y) for (x, y), (_c, _cf, hz) in WORLD.items()
                    if not hz and (x, y) not in live), None)
    if evicted:
        lax.annotate("stale sighting evicted", evicted,
                     xytext=(evicted[0], evicted[1] - 1.4), ha="center", fontsize=8,
                     color="#888", arrowprops=dict(arrowstyle="->", color="#888"))

    handles = [
        Line2D([], [], color="#3498db", marker="^", lw=1.5, label="robot + path"),
        Patch(color=QDRANT_RED, label="hazard memory"),
        Patch(color="#2c3e50", label="object memory"),
        Patch(color="#f7c6cf", label="hazard in world"),
        Patch(color="#e5e5e5", label="object in world"),
    ]
    fig.legend(handles=handles, fontsize=8, loc="lower center", ncol=5, frameon=False)
    fig.suptitle("Robot memory over time: opacity = remaining value; hazards persist, stale sightings fade",
                 fontsize=13)
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    if save:
        fig.savefig(save, dpi=120, bbox_inches="tight")
    plt.show()


def decay_chart(sizes_capped, sizes_uncapped, budget, save=None):
    """Shard size over time: with an eviction budget vs. unbounded growth."""
    ticks = range(len(sizes_capped))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ticks, sizes_uncapped, "--", color="#95a5a6", label="without eviction (unbounded)")
    ax.plot(ticks, sizes_capped, color=QDRANT_RED, lw=2, label="with eviction (budgeted)")
    ax.axhline(budget, color="#bbbbbb", lw=1)
    ax.text(0, budget + 0.3, f"budget = {budget}", fontsize=8, color="#888")
    ax.set_xlabel("Patrol tick")
    ax.set_ylabel("Memories in shard")
    ax.set_title("A memory budget keeps the shard bounded on-device", loc="left")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    _badge(ax, "measured")
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    if save:
        fig.savefig(save, dpi=120, bbox_inches="tight")
    plt.show()


def knowledge_dashboard(stats):
    """'Ask the device what it knows': one compact closing dashboard. Returns HTML.

    `stats` carries the counts gathered offline from the two local shards:
    `robot_total`, `phone_total`, `combined`, `by_modality` (dict), `network`,
    `top_hazard`, `top_purchase`, `evicted`, and optional `recurring` note text.
    Counts are measured live; the eviction budget is an illustrative device
    constraint, so it is labelled as such.
    """
    from IPython.display import HTML

    def tile(label, value, color="#2c3e50", note=""):
        note_html = f'<div style="font-size:10px;color:#95a5a6">{note}</div>' if note else ""
        return (f'<div style="background:#fff;border-radius:10px;padding:10px 16px;margin:6px;'
                f'min-width:120px;box-shadow:0 1px 3px rgba(0,0,0,.08)">'
                f'<div style="font-size:22px;font-weight:800;color:{color}">{value}</div>'
                f'<div style="font-size:12px;color:#888">{label}</div>{note_html}</div>')

    mod = stats.get("by_modality", {})
    primary = "".join([
        tile("memories on device (combined)", stats["combined"], QDRANT_RED),
        tile("robot shard", stats["robot_total"]),
        tile("phone shard", stats["phone_total"]),
        tile("network", stats["network"], "#2ecc71"),
    ])
    modality = "".join(tile(k, v) for k, v in mod.items())
    insight = "".join([
        tile("top recalled hazard", stats["top_hazard"], QDRANT_RED),
        tile("phone: top purchase", stats["top_purchase"]),
        tile("stale evicted", stats["evicted"], note="budget: Illustrative"),
    ])
    recurring = ""
    if stats.get("recurring"):
        recurring = (
            '<div style="background:#fff;border-radius:10px;padding:10px 16px;margin:6px">'
            '<div style="font-size:12px;color:#888">recurring note, recalled offline</div>'
            f'<div style="font-size:13px;color:#2c3e50">{stats["recurring"]}</div></div>')

    badge_label, badge_color = BADGES["measured"]
    header = (
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">'
        '<span style="font-weight:800;font-size:16px">Ask the device what it knows</span>'
        f'<span style="font-size:11px;color:#fff;background:{badge_color};'
        f'border-radius:10px;padding:2px 8px">{badge_label}</span></div>')

    def row(label, tiles):
        return (f'<div style="font-size:11px;color:#95a5a6;margin:6px 0 0 6px">{label}</div>'
                f'<div style="display:flex;flex-wrap:wrap">{tiles}</div>')
    return HTML(
        '<div style="font-family:system-ui,sans-serif;background:#f2f3f5;border-radius:14px;padding:16px">'
        + header
        + row("totals", primary)
        + row("by modality", modality)
        + row("what it found", insight)
        + recurring + "</div>")

# --- robot ----------------------------------------
"""A tiny grid-world robot that accumulates observation memories under a budget.

The point of the lesson: a robot on a small, memory-constrained device can't
keep every observation forever. It stores each sighting in an EdgeShard, and when memory
exceeds a budget it evicts the lowest-value memories: recent, high-confidence
hazards survive; stale, low-confidence noise fades. Everything runs on a real
EdgeShard so the API is the same one from L2.
"""
import math

from qdrant_edge import Point, UpdateOperation, ScrollRequest, CountRequest


GRID_W, GRID_H = 9, 6

# fixed world: (x, y) -> (class, confidence, is_hazard)
WORLD = {
    (2, 2): ("wet floor spill", 0.92, True),
    (6, 4): ("loose cable", 0.88, True),
    (3, 1): ("cardboard box", 0.60, False),
    (7, 5): ("doorway", 0.70, False),
    (1, 4): ("chair", 0.55, False),
    (5, 2): ("shelf", 0.58, False),
    (4, 5): ("puddle", 0.40, False),   # low-confidence, will go stale
}

# robot patrol path (a loop through the space)
PATH = [(0, 0), (1, 1), (2, 2), (3, 2), (4, 2), (5, 2), (6, 3), (6, 4),
        (7, 5), (6, 5), (5, 4), (4, 5), (3, 3), (2, 2), (1, 3), (0, 4)]


def _observe(pos):
    """Items within Chebyshev distance 1 of the robot become sightings."""
    x0, y0 = pos
    seen = []
    for (x, y), (cls, conf, hazard) in WORLD.items():
        if abs(x - x0) <= 1 and abs(y - y0) <= 1:
            # is_hazard stored as 0/1: this edge build matches integers, not bools.
            seen.append({"x": x, "y": y, "object_class": cls,
                         "confidence": conf, "is_hazard": int(hazard)})
    return seen


def _score(payload, now_tick, tau=6.0):
    """Memory value = confidence decayed by age. Hazards decay slower."""
    age = now_tick - payload["timestamp"]
    half_life = tau * (2.0 if payload["is_hazard"] else 1.0)
    return payload["confidence"] * math.exp(-age / half_life)


def _all_points(shard):
    records, _ = shard.scroll(ScrollRequest(limit=1000, with_payload=True))
    return records


def simulate(directory="./robot_shard", budget=8, snapshots=(0, 7, 15)):
    """Run the patrol, storing observations in an EdgeShard under a memory budget.

    Returns frames (grid state at the snapshot ticks), the shard-size series with
    and without eviction, and the live shard.
    """
    shard = create_memory_shard(directory, {"text": NOMIC_DIM})
    next_id = 0
    sizes_capped, sizes_uncapped = [], []
    total_inserted = 0
    frames = []

    for tick, pos in enumerate(PATH):
        sightings = _observe(pos)
        if sightings:
            vecs = embed_text([f"{s['object_class']} at ({s['x']},{s['y']})" for s in sightings])
            pts = []
            for s, v in zip(sightings, vecs):
                s = {**s, "timestamp": tick}
                pts.append(Point(id=next_id, vector={"text": v}, payload=s))
                next_id += 1
            shard.update(UpdateOperation.upsert_points(pts))
            total_inserted += len(pts)

        # evict lowest-value memories when over budget
        records = _all_points(shard)
        if len(records) > budget:
            ranked = sorted(records, key=lambda r: _score(r.payload, tick))
            drop = [r.id for r in ranked[:len(records) - budget]]
            shard.update(UpdateOperation.delete_points(drop))

        sizes_capped.append(shard.count(CountRequest(exact=True)))
        sizes_uncapped.append(total_inserted)

        if tick in snapshots:
            frames.append({
                "tick": tick, "robot": pos,
                "memories": [{**r.payload, "score": _score(r.payload, tick)}
                             for r in _all_points(shard)],
            })

    return frames, sizes_capped, sizes_uncapped, shard


def distinct(hits, n=3):
    """Collapse repeat sightings to one memory per object, keeping the best-scored."""
    seen, out = set(), []
    for h in hits:
        key = h.payload["object_class"]
        if key not in seen:
            seen.add(key)
            out.append(h)
        if len(out) == n:
            break
    return out


# --- public aliases ---------------------------------
ROBOT_WORLD = WORLD
robot_simulate = simulate
distinct_objects = distinct
