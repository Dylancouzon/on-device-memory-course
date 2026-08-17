"""Plumbing for the lessons: stores and searches the notebooks repeat, an
offline guard, benchmark filler, and cleanup.

Each Qdrant Edge call is written out in the notebook of the lesson that
teaches it (create a shard, upsert points, query, filter, delete). After
that first time, the repeat lives here so the cells stay short. Validated
against qdrant-edge-py 0.7.2.
"""
import gc
import inspect
import json
import shutil
import socket
from contextlib import contextmanager
from pathlib import Path

from qdrant_edge import EdgeShard, Point, Query, QueryRequest, UpdateOperation

from .embeddings import embed_image, embed_query, embed_query_clip, embed_text


def load_memories(path, source_type=None):
    """Read a memories JSON file, optionally keeping one source type."""
    memories = json.load(open(path))
    if source_type:
        memories = [m for m in memories if m["source_type"] == source_type]
    return memories


def store_notes(shard, notes):
    """Embed text and voice notes with Nomic and store one point per note.

    The write this wraps is taught in Lesson 2: embed the note, build a
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

    The raw call is taught in Lesson 2; `query_filter` narrows recall the
    way Lesson 3 teaches.
    """
    return shard.query(QueryRequest(
        query=Query.Nearest(embed_query(query), using="text"),
        filter=query_filter,
        limit=limit,
        with_payload=True,
    ))


def photo_search(shard, description, limit=1):
    """Embed a description with CLIP and return the nearest photos.

    The raw cross-modal call is taught in Lesson 3.
    """
    return shard.query(QueryRequest(
        query=Query.Nearest(embed_query_clip(description), using="image"),
        limit=limit,
        with_payload=True,
    ))


def recall(shard, question):
    """One question, two lanes: text memories by Nomic, photos by CLIP.

    Lesson 4 builds this in the open; later lessons import it. Extra text
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


def demo():
    """Self-check: the raw Qdrant calls the notebooks use, run offline.

    Run from .build/ as `python -m utils.qdrant_helpers` (the module
    imports its siblings relatively).
    """
    import tempfile
    from qdrant_edge import (
        EdgeShard, EdgeConfig, EdgeVectorParams, Distance,
        Query, QueryRequest, CountRequest,
    )
    d = tempfile.mkdtemp()
    config = EdgeConfig(vectors={"v": EdgeVectorParams(size=3, distance=Distance.Cosine)})
    shard = EdgeShard.create(d, config)
    shard.update(UpdateOperation.upsert_points([
        Point(id=0, vector={"v": [1.0, 0, 0]}, payload={"note": "a"}),
        Point(id=1, vector={"v": [0, 1.0, 0]}, payload={"note": "b"}),
    ]))
    shard.optimize()
    assert shard.count(CountRequest(exact=True)) == 2
    with no_network():
        hits = shard.query(QueryRequest(
            query=Query.Nearest([1.0, 0, 0], using="v"),
            limit=1, with_payload=True,
        ))
    assert hits[0].payload["note"] == "a"
    shard.close()
    reloaded = EdgeShard.load(d)
    assert reloaded.count(CountRequest(exact=True)) == 2
    reloaded.close()
    shutil.rmtree(d, ignore_errors=True)
    print("qdrant_helpers demo OK")


if __name__ == "__main__":
    demo()
