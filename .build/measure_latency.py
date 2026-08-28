"""Measure vector-lookup latency as the store grows, for L3's latency curve.

The lesson shows a precalculated curve rather than timing anything live: a
notebook cell cannot build a 250,000-vector store inside a 4 GB container,
and a number measured on the student's shared sandbox would move on every
re-run. So the measurement happens here, once, and the result is pasted into
LOOKUP_LATENCY in .build/utils/viz.py.

Run from the repository root: `python .build/measure_latency.py`.
"""
import platform
import shutil
import statistics
import sys
import tempfile
from pathlib import Path
from time import perf_counter

import numpy as np
from qdrant_edge import (Distance, EdgeConfig, EdgeShard, EdgeVectorParams,
                         Point, Query, QueryRequest, UpdateOperation)

sys.path.insert(0, str(Path(__file__).parent.parent))
from helper import embed_query                          # noqa: E402

SIZES = [1_000, 5_000, 25_000, 100_000, 250_000]
DIM = 768
BATCH = 25_000
RUNS = 300


def machine():
    """A readable name for the machine the numbers came from."""
    if platform.system() == "Darwin":
        import subprocess
        chip = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"],
                              capture_output=True, text=True).stdout.strip()
        if chip:
            return chip
    return f"{platform.machine()} / {platform.system()}"


def build(shard, start, count, rng):
    """Upsert `count` random vectors in batches, so nothing large is held."""
    for offset in range(0, count, BATCH):
        n = min(BATCH, count - offset)
        vectors = rng.normal(size=(n, DIM)).astype("float32")
        shard.update(UpdateOperation.upsert_points([
            Point(id=start + offset + i, vector={"text": v.tolist()},
                  payload={"kind": "filler"})
            for i, v in enumerate(vectors)
        ]))
    shard.optimize()


def embed_ms(text, runs=50):
    """Median milliseconds to embed one query. Only this script needs it."""
    times = []
    for _ in range(runs):
        t0 = perf_counter()
        embed_query(text)
        times.append((perf_counter() - t0) * 1000)
    return statistics.median(times)


def lookup_ms(shard, query_vector):
    """Milliseconds per lookup, query embedded before the clock starts."""
    for _ in range(20):                                   # warm the caches
        shard.query(QueryRequest(
            query=Query.Nearest(query_vector, using="text"), limit=3))
    timings = []
    for _ in range(RUNS):
        t0 = perf_counter()
        shard.query(QueryRequest(
            query=Query.Nearest(query_vector, using="text"),
            limit=3, with_payload=True))
        timings.append((perf_counter() - t0) * 1000)
    return statistics.median(timings)


def main():
    query_vector = embed_query("coffee")
    query_embed = embed_ms("coffee")
    rng = np.random.default_rng(0)
    directory = tempfile.mkdtemp()
    shard = EdgeShard.create(directory, EdgeConfig(vectors={
        "text": EdgeVectorParams(size=DIM, distance=Distance.Cosine)}))

    results, stored = [], 0
    for size in SIZES:
        build(shard, stored, size - stored, rng)
        stored = size
        median = lookup_ms(shard, query_vector)
        results.append((size, median))
        print(f"  {size:>9,} memories  {median:6.3f} ms", flush=True)

    shard.close()
    shutil.rmtree(directory, ignore_errors=True)

    print("\nPaste into .build/utils/viz.py:\n")
    print(f"# Measured by .build/measure_latency.py on {machine()}, CPU only,")
    print(f"# Python {platform.python_version()}, {RUNS} queries per size,"
          " median reported.")
    print("LOOKUP_LATENCY = [")
    for size, median in results:
        print(f"    ({size}, {median:.3f}),")
    print("]")
    print(f"QUERY_EMBED_MS = {query_embed:.2f}")


if __name__ == "__main__":
    main()
