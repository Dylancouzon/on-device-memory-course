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


def embed_query_clip(text):
    """Embed a text query into CLIP's space, to search the image vector."""
    return next(_clip_text().query_embed([text])).tolist()
