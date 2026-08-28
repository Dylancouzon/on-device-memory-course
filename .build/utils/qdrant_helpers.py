"""Plumbing for the lessons: stores and searches the notebooks repeat, an
offline guard, benchmark filler, and cleanup.

Each Qdrant Edge call is written out in the notebook of the lesson that
teaches it (create a shard, upsert points, query, filter, delete). After
that first time, the repeat lives here so the cells stay short. Validated
against qdrant-edge-py 0.7.2.
"""
import gc
import json
import shutil
import socket
from pathlib import Path

from qdrant_edge import Distance, EdgeConfig, EdgeShard, EdgeVectorParams
from qdrant_edge import Point, Query, QueryRequest, ScrollRequest
from qdrant_edge import UpdateOperation

from .embeddings import embed_image, embed_query, embed_query_clip, embed_text
from .viz import day_photos, memories_table, show, show_images


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


MODEL_NAME = {"text": "Nomic", "image": "CLIP"}


def new_shard(directory, text=None, image=None):
    """Create an empty shard on a clean directory, one named vector space
    per width given: `new_shard("./day_shard", text=768, image=512)`.

    Lesson 3 writes this out in full, an `EdgeConfig` holding one
    `EdgeVectorParams` per named vector and then `EdgeShard.create`. After
    that first time the repeat lives here. The widths stay arguments, so a
    lesson still says on screen which spaces it has and how wide they are.
    """
    sizes = {name: size for name, size in
             (("text", text), ("image", image)) if size}
    config = EdgeConfig(vectors={
        name: EdgeVectorParams(size=size, distance=Distance.Cosine)
        for name, size in sizes.items()
    })
    shard = EdgeShard.create(fresh_start(directory), config)
    print("Shard ready:", ", ".join(
        f"{name} {size}-d ({MODEL_NAME[name]})"
        for name, size in sizes.items()))
    return shard


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
                         title=f"Stored {len(photos)} photos · "
                               f"{shard.info().points_count} memories"))
    else:
        print(f"Stored {len(photos)} photos · "
              f"{shard.info().points_count} memories")


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
        print(f"Stored {len(photos)} photos · "
              f"{shard.info().points_count} memories")


def text_search(shard, query, query_filter=None, limit=4):
    """Embed a query with Nomic and return the nearest text memories.

    Lesson 3 teaches both halves in the open: the raw nearest query, then
    `query_filter` narrowing it.
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


def recognize(shard, photo, threshold=None):
    """The closest stored photo, and optionally whether it clears the bar.

    The nearest-vector query and the image-vector search are both
    Lesson 3's. What Lesson 5 adds is the threshold: below it, the device
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

    Writes exactly what Lesson 5's `teach` writes: the photo's CLIP vector
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
    show(show_images(paths, captions=list(seeds)))


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


def cloud_client(collection, text=768, image=512):
    """Connect to the cluster in QDRANT_URL / QDRANT_API_KEY, collection ready.

    Pasting credentials is how a student opts in, so there is no second
    switch to forget: returns a ready qdrant_client.QdrantClient with the
    collection created, or None when either variable is empty. A collection
    that already exists is left alone and None comes back, because the
    course never deletes one. None means every memory stays on the device,
    and the calling cell says so.

    The server's vectors_config is the twin of the `EdgeConfig` Lesson 3
    writes out, so it lives here rather than repeating on screen.
    """
    import os
    if not (os.getenv("QDRANT_URL") and os.getenv("QDRANT_API_KEY")):
        return None
    from qdrant_client import QdrantClient, models
    client = QdrantClient(url=os.environ["QDRANT_URL"],
                          api_key=os.environ["QDRANT_API_KEY"])
    if client.collection_exists(collection):
        print(f"{collection} already exists on the cluster.",
              "Delete it there first, or rename the collection here.")
        return None
    client.create_collection(collection, vectors_config={
        "text": models.VectorParams(size=text,
                                    distance=models.Distance.COSINE),
        "image": models.VectorParams(size=image,
                                     distance=models.Distance.COSINE),
    })
    return client


def cloud_points(shard, limit=1000):
    """Every point in a shard, in the shape a Qdrant server takes.

    Same ids, same vectors, same payloads: the format does not change on
    the way up. Reading them back is the `ScrollRequest` the appendix
    shows in the open one cell earlier.
    """
    from qdrant_client import models
    records, _ = shard.scroll(ScrollRequest(limit=limit, with_payload=True,
                                            with_vector=True))
    return [models.PointStruct(id=r.id, vector=r.vector, payload=r.payload)
            for r in records]


def push_note(client, collection, point_id, note):
    """Store one text note straight onto the cluster, as another device would.

    Used where the write belongs to some other device in the fleet. A write
    the student makes themselves stays in the notebook.
    """
    from qdrant_client import models
    client.upsert(collection, points=[models.PointStruct(
        id=point_id,
        vector={"text": embed_text([note])[0]},
        payload={"source_type": "text", "note": note},
    )])


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


def file_size(path):
    """A downloaded snapshot's size, in whichever unit reads better."""
    import os
    kb = os.path.getsize(path) / 1024
    return f"{kb / 1024:.1f} MB" if kb >= 1024 else f"{kb:.0f} KB"


def fresh_start(directory):
    """Delete any previous run's shard directory and recreate it empty.

    A shard the notebook still has bound holds its files open, and Edge flushes
    when that object is dropped. Deleting the files first makes the flush fail
    inside a destructor, which surfaces as a Rust panic rather than a Python
    error. So close any shard the notebook still holds before removing
    anything: that makes re-running a setup cell in a live kernel safe,
    instead of only working on a clean top-to-bottom run.

    The notebook's own namespace is `__main__`, whatever the call depth, so
    this works whether a lesson calls it directly or `new_shard` does.

    Only a directory that already holds a shard can have one open on it, so
    the sweep is skipped for a directory that does not exist yet. Without
    that guard, opening a second shard closes the first, which is exactly
    what a lesson holding two shards at once needs not to happen.
    """
    import sys
    if any(Path(directory).glob("*")):
        notebook = vars(sys.modules.get("__main__", None)) or {}
        for value in list(notebook.values()):
            if isinstance(value, EdgeShard):
                try:
                    value.close()
                except Exception:
                    pass
    gc.collect()
    shutil.rmtree(directory, ignore_errors=True)
    Path(directory).mkdir(parents=True, exist_ok=True)
    return directory


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
    hits = shard.query(QueryRequest(
        query=Query.Nearest([1.0, 0, 0], using="v"),
        limit=1,
        with_payload=True,
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
