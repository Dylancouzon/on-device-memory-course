"""Course visualizations.

Results come back as HTML tables so a student can select and copy any number
off the screen. Photos and charts stay images, sized for the recording frame
(8 wide by 9 high), so nothing is cut off.
"""
import math
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

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


def _table(headers, rows, title=None, caption=None, widths=None, above=""):
    """Render a table as HTML. `rows` holds ready-made <td> strings.

    `widths` is one CSS width per column. Without it the browser sizes every
    column by its content, which lets a three-character Price column sit on
    top of Category and squeezes the memory itself into what is left. The
    memory is what the reader came to read, so it gets most of the width.
    """
    cols = ("<colgroup>"
            + "".join(f'<col style="width:{w}">' for w in widths)
            + "</colgroup>") if widths else ""
    layout = "table-layout:fixed;" if widths else ""
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
    parts.append(above)
    parts.append(f'<table style="border-collapse:collapse;width:100%;'
                 f'{layout}font-size:13.5px;color:{INK}">{cols}'
                 f'<thead><tr>{head}</tr></thead>'
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


def _result_row(hit, peak, price=True, when=False):
    """One table row for a search hit: score, category, price, the memory."""
    p = hit.payload
    return (_score_cell(hit.score, peak)
            + _cell(p.get("category", "-"), color=MUTED)
            + (_cell(_price(p), align="right", color=MUTED) if price else "")
            + (_cell(_hhmm(p["timestamp"], "%b %d") if p.get("timestamp")
                     else "-", color=MUTED, nowrap=True) if when else "")
            + _cell(_memory_text(p)))


def results_table(hits, title=None, caption=None, query=None,
                  when=False, price=None):
    """Show search hits as a table: score, category, price, and the memory.

    `query` puts the question above the answers, where a reader looks for it.
    An empty result renders as the same view with nothing in it, so asking
    before and after storing reads as one picture with a row count.
    `when` adds the memory's date, for the lessons that rank by it.
    `price` defaults to showing the column when a memory carries one.
    """
    asked = _query_block(query) if query else ""
    if not hits:
        return _html(
            f'<div style="{FONT};max-width:760px">'
            f'<div style="font-weight:800;font-size:15px;color:{INK};'
            f'margin-bottom:6px">{_esc(title or "No memories found")}</div>'
            + asked
            + f'<div style="border:1px dashed {LINE};border-radius:8px;'
            f'padding:18px;text-align:center;color:{MUTED};font-size:13.5px">'
            f'Nothing stored yet.</div>'
            + (f'<div style="font-size:12px;color:{MUTED};margin-top:6px">'
               f'{_esc(caption)}</div>' if caption else '') + '</div>')
    peak = max((h.score for h in hits), default=1.0)
    if price is None:
        price = _has_price([h.payload for h in hits])
    rows = [_result_row(h, peak, price=price, when=when) for h in hits]
    headers = (["Score", "Category"] + (["Price"] if price else [])
               + (["When"] if when else []) + ["Memory"])
    widths = {(True, True): ("10%", "12%", "9%", "10%", "59%"),
              (True, False): ("10%", "13%", "9%", "68%"),
              (False, True): ("10%", "13%", "11%", "66%"),
              (False, False): ("10%", "14%", "76%")}[(price, when)]
    return _html(_table(headers, rows, title, caption, widths, above=asked))


def memories_table(memories, title=None):
    """Show stored memories, which carry no score: category, price, words."""
    price = _has_price(memories)
    rows = [_cell(m.get("category", "-"), color=MUTED)
            + (_cell(_price(m), align="right", color=MUTED) if price else "")
            + _cell(_memory_text(m)) for m in memories]
    headers = ["Category"] + (["Price"] if price else []) + ["Memory"]
    widths = ("14%", "9%", "77%") if price else ("15%", "85%")
    return _html(_table(headers, rows, title, widths=widths))


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
        f'letter-spacing:.04em">closest photo</div>'
        f'<div style="font-size:17px;font-weight:700;color:{INK};'
        f'margin:2px 0 8px">"{_esc(query)}"</div>'
        f'<img src="{uri}" style="width:100%;border-radius:10px;display:block">'
        f'<div style="margin-top:8px;font-size:13.5px;color:{INK}">'
        f'{_esc(hero.payload["file"])} · similarity '
        f'<span style="color:{QDRANT_RED};font-weight:700">'
        f'{hero.score:.3f}</span></div></div>')


def _query_block(text):
    """The question, shown above its answers rather than captioned under them."""
    return (f'<div style="font-size:13.5px;color:{INK};background:#FAFAFB;'
            f'border-left:3px solid {QDRANT_RED};padding:8px 10px;'
            f'margin-bottom:10px">{_esc(text)}</div>')


def _cosine(a, b):
    """Cosine similarity between two embeddings, the score a search returns."""
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a))
                  * math.sqrt(sum(y * y for y in b)))


def _payload_value(key, value):
    """A payload value as stored, glossed where the raw number is unreadable.

    A timestamp is an epoch integer on disk and stays one here, with the time
    it stands for beside it: the point of the card is what was really stored.
    """
    if key == "timestamp" and isinstance(value, (int, float)):
        return f"{value}  ({_hhmm(value, '%b %d, %H:%M')})"
    return value


def vector_preview(text, vector, shown=8):
    """One memory beside the start of the vector it became.

    The caption names the vector and counts its dimensions, because those are two
    different things and the lesson leans on the difference: one note becomes
    one vector, and that vector is a list of coordinates.
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
        f'{len(vector)} dimensions'
        f'</div></div>')


def point_card(record, vector_name="text", shown=6):
    """One point in full: its id, its vector, and its payload.

    Takes anything carrying `.id`, `.vector`, and `.payload`, so it renders a
    `Point` the lesson just built as readily as a record read back off disk.
    """
    vector = record.vector[vector_name]
    # shown=0 where the cell above already printed the vector in full:
    # the card is then about the point's shape, not its values twice.
    values = ", ".join(f"{x:+.3f}" for x in vector[:shown])
    rows = [_cell(k, color=MUTED, nowrap=True) + _cell(_payload_value(k, v))
            for k, v in record.payload.items()]
    return _html(
        f'<div style="{FONT};max-width:760px">'
        f'<div style="font-weight:800;font-size:15px;color:{INK}">'
        f'Point {_esc(record.id)}</div>'
        f'<div style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace;'
        f'font-size:12.5px;color:{QDRANT_RED};background:#FAFAFB;'
        f'border:1px solid {LINE};border-radius:8px;padding:10px;'
        f'margin:8px 0">{_esc(vector_name)}: '
        f'{f"[{values}, ...] " if shown else ""}'
        f'<span style="color:{MUTED}">{len(vector)} dimensions</span></div>'
        + _table(["Field", "Value"], rows,
                  widths=("20%", "80%")) + '</div>')


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


def day_notes(memories, limit=10):
    """The day's voice and text notes as a table: time, kind, and words.

    Shows the earliest `limit` notes, because a whole day of them runs off
    the bottom of the recording frame. Pass a bigger number for more, or
    `limit=None` for the lot. The title says how many there are either way.
    """
    notes = sorted((m for m in memories if not m.get("file")),
                   key=lambda m: m["timestamp"])
    total = len(notes)
    if limit is not None:
        notes = notes[:limit]
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
    title = (f"{total} voice and text notes" if len(notes) == total
             else f"First {len(notes)} of {total} voice and text notes")
    return _html(_table(["Time", "Kind", "Note"], rows, title,
                        widths=("15%", "12%", "73%")))


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
    """One question's answers as side-by-side lanes, never one blended list.

    `sections` maps a lane title to a list of ScoredPoint, and each lane is a
    column ranked best first. Columns rather than a wrapping row because the
    lanes are the point: a reader compares down one lane and across three,
    and a wrap would put two lanes' cards on the same line. Every lane is
    drawn even when empty. Scores below `min_score` are dimmed.
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
            body = (f'<img src="{uri}" style="width:100%;height:130px;'
                    f'object-fit:cover;border-radius:8px;display:block;'
                    f'margin-top:6px">')
        else:
            body = (f'<div style="font-size:13px;margin-top:6px;'
                    f'color:{INK}">{_esc(_memory_text(p))}</div>')
        tag = ('<span style="font-size:11px;color:#B0088A"> · weaker</span>'
               if weak else '')
        head = (f'<div style="font-size:11px;color:{MUTED}">{_esc(ctx)}</div>'
                if ctx else '')
        return (f'<div style="border:1px solid {LINE};border-radius:10px;'
                f'padding:9px;margin-bottom:8px;background:#fff;'
                f'{"opacity:.5" if weak else ""}">'
                f'{head}'
                f'{body}<div style="font-size:12.5px;margin-top:6px">'
                f'<span style="color:{QDRANT_RED};font-weight:700">'
                f'{h.score:.3f}</span>{tag}</div></div>')

    lanes = []
    for title, hits in sections.items():
        ranked = sorted(hits, key=lambda h: h.score, reverse=True)
        inner = ("".join(card(h) for h in ranked) if ranked else
                 f'<div style="font-size:13px;color:{MUTED};font-style:italic">'
                 f'No matches</div>')
        lanes.append(
            f'<div style="flex:1 1 0;min-width:0">'
            f'<div style="font-weight:700;font-size:13px;color:{INK};'
            f'border-bottom:2px solid {QDRANT_RED};margin-bottom:8px;'
            f'padding-bottom:3px">{_esc(title)}</div>{inner}</div>')
    return _html(
        f'<div style="{FONT};background:#F7F7F8;border-radius:12px;'
        f'padding:14px 16px;max-width:760px">'
        f'<div style="display:flex;gap:12px;align-items:flex-start">'
        f'{"".join(lanes)}</div></div>')


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

    same = []
    different = []
    for label, query in held_out.items():
        same.append(max(_cosine(vectors[query], vectors[p])
                        for p in taught[label]))
        different.extend(
            _cosine(vectors[query], vectors[p])
            for other, views in taught.items() if other != label
            for p in views)
    different.extend(
        _cosine(vectors[scene], vectors[p])
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


# Measured by .build/measure_latency.py on Apple M5 Pro, CPU only,
# Python 3.14.6, 300 queries per size, median reported. The lesson draws
# this curve rather than timing anything live: a 250,000-vector store does
# not fit in the course container, and a number timed on a shared sandbox
# moves on every re-run. Re-measure and paste if the model or Edge changes.
LOOKUP_LATENCY = [
    (1_000, 0.054),
    (5_000, 0.179),
    (25_000, 0.526),
    (100_000, 1.439),
    (250_000, 2.646),
]
QUERY_EMBED_MS = 5.50
MEASURED_ON = "Apple M5 Pro, CPU only, median of 300 queries per size"


def latency_curve(points=LOOKUP_LATENCY, embed_ms=QUERY_EMBED_MS):
    """Vector lookup time as the store grows, against the cost of embedding.

    Two local costs make up one answer. Embedding the question is a fixed
    price the encoder charges whatever the store holds, so it draws as a
    flat line. The lookup grows with the number of vectors, so it draws as
    a curve. Both stay on the device, which keeps this a breakdown of where
    the time goes and never a comparison against a server.
    """
    sizes = [n for n, _ in points]
    times = [ms for _, ms in points]
    fig, ax = plt.subplots(figsize=(FIG_W, 3.5))

    ax.axhline(embed_ms, color="#8F98B2", lw=2, ls="--")
    ax.annotate(f"query embedding · {embed_ms:.1f} ms",
                xy=(sizes[0], embed_ms), xytext=(0, 7),
                textcoords="offset points", color="#5C6480", fontsize=9.5)
    ax.plot(sizes, times, color=QDRANT_RED, lw=2.2, marker="o",
            markersize=6, markerfacecolor="white",
            markeredgecolor=QDRANT_RED, markeredgewidth=2, zorder=3)
    for n, ms in points:
        ax.annotate(f"{ms:.2f} ms", xy=(n, ms), xytext=(0, 11),
                    textcoords="offset points", ha="center", va="bottom",
                    color=QDRANT_RED, fontsize=9.5, fontweight="bold")

    ax.set_xscale("log")
    ax.set_xticks(sizes)
    ax.set_xticklabels([f"{n:,}" for n in sizes])
    ax.minorticks_off()
    ax.set_xlabel("memories")
    ax.set_ylabel("milliseconds")
    ax.set_ylim(0, max(embed_ms, max(times)) * 1.35)
    ax.set_title("Vector lookup as memory grows", loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    # One provenance line, kept shorter than the figure: a wider line makes
    # matplotlib grow the whole figure past the recording frame.
    fig.subplots_adjust(bottom=0.24)
    fig.text(0.012, 0.03, MEASURED_ON, fontsize=9.5, color="#4E5366")
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
            detail = ""
        else:
            detail = ""
    elif threshold is not None:
        if known:
            detail = f'{top.score:.3f} clears the {threshold:.3f} threshold.'
        else:
            detail = f'{top.score:.3f} is below the {threshold:.3f} threshold.'
        detail = (f'<div style="font-size:13px;color:{color};font-weight:650;'
                  f'margin:0 0 10px">{_esc(detail)}</div>')

    heading = f"{mark} " if mark else ""
    score_detail = (f" · closest: {_esc(label)} · similarity {top.score:.3f}"
                    if known is False else
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


def demo():
    html = receipt_table([("path", "./coffee_shard"), ("memories", 6),
                          ("network_calls", 0)]).data
    assert "coffee_shard" in html and "<table" in html
    print("viz demo OK")


if __name__ == "__main__":
    demo()
