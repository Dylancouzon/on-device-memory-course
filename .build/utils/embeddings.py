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
    example = not (teach_photos and test_photo)
    if example:
        teach_photos = [EXAMPLE_OBJECT + "1.jpg", EXAMPLE_OBJECT + "2.jpg"]
        test_photo = EXAMPLE_OBJECT + "3.jpg"
    resolved = [load_image(p) for p in teach_photos]
    print(f"{len(resolved)} teach photos + 1 test photo ready"
          + (" (bundled example: rubber duck)" if example else ""))
    return resolved, load_image(test_photo)
