"""Non-Qdrant plumbing for the lessons: an offline guard, benchmark filler, and
cleanup.

Every Qdrant Edge call (create a shard, upsert points, query, filter, count) is
written out in the notebooks themselves so the API stays visible. This module
holds only the supporting pieces that would otherwise clutter a cell. Validated
against qdrant-edge-py 0.7.2.
"""
import shutil
import socket
from contextlib import contextmanager
from pathlib import Path

from qdrant_edge import Point, UpdateOperation


def add_filler(shard, vector_name, count, dim, payload_fn=None, start_id=1000, seed=0):
    """Grow the shard with `count` random vectors, so a latency number is credible.

    Content is irrelevant to latency, it tracks how many vectors there are and how
    wide they are. Pass `payload_fn(i, rng)` to attach filter fields when the
    benchmark is a filtered search.
    """
    import numpy as np
    rng = np.random.default_rng(seed)
    vecs = rng.normal(size=(count, dim)).astype("float32")
    points = [
        Point(id=start_id + i, vector={vector_name: vecs[i].tolist()},
              payload=(payload_fn(i, rng) if payload_fn else {"kind": "filler"}))
        for i in range(count)
    ]
    shard.update(UpdateOperation.upsert_points(points))
    shard.optimize()
    return count


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
    print("⚠ Python socket creation blocked for this cell")
    try:
        yield
    finally:
        socket.socket = original


def demo():
    """Self-check: the raw Qdrant calls the notebooks use, run offline."""
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
    cleanup(reloaded, d)
    print("qdrant_helpers demo OK")


if __name__ == "__main__":
    demo()
