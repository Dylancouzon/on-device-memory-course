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
