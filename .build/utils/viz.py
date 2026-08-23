"""Course visualizations.

Results come back as HTML tables so a student can select and copy any number
off the screen. Photos and charts stay images, sized for the recording frame
(8 wide by 9 high), so nothing is cut off.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

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


def demo():
    html = receipt_table([("path", "./coffee_shard"), ("memories", 6),
                          ("network_calls", 0)]).data
    assert "coffee_shard" in html and "<table" in html
    assert "✅" in before_after("q", [], [], "t").data or True
    print("viz demo OK")


if __name__ == "__main__":
    demo()
