"""On-device embedding models.

L3 uses two models through FastEmbed, both small ONNX models that run locally
with no account and no network after the first download: Nomic-Embed-Text v1.5
for words, and CLIP for images and cross-modal recall. Each model loads lazily
and once (4 GB sandbox budget, one model in memory at a time).
"""
from functools import lru_cache
from pathlib import Path

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


# CLIP: one shared text/image space, for cross-modal recall in L3 and later.
# Nomic and CLIP scores sit on different scales, so photos live in their own
# named vector and a text query is embedded twice, once per space.
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

    A path to a file already on disk passes straight through, so the upload
    button and a filename typed by hand both land here.
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
            "ends in .jpg or .png), or use the upload button instead."
        ) from None
    fd, path = tempfile.mkstemp(suffix=".jpg")
    os.close(fd)
    image.save(path, "JPEG")
    return path


def embed_query_clip(text):
    """Embed a text query into CLIP's space, to search the image vector."""
    return next(_clip_text().query_embed([text])).tolist()


EXAMPLE_OBJECT = "./ro_shared_data/objects/rubberduck_"
TEACH_DIR = "./my_photos/teach"
TEST_DIR = "./my_photos/test"
IMAGE_TYPES = (".jpg", ".jpeg", ".png", ".webp")
_UPLOADS_RESET = False


def _uploaded(folder):
    """Photos sitting in an upload folder, oldest first."""
    path = Path(folder)
    if not path.is_dir():
        return []
    files = [f for f in path.iterdir() if f.suffix.lower() in IMAGE_TYPES]
    return sorted(files, key=lambda f: f.stat().st_mtime)


def _upload_box(folder, heading, hint):
    """One labelled upload button that saves into `folder`."""
    import ipywidgets as widgets

    Path(folder).mkdir(parents=True, exist_ok=True)
    title = widgets.HTML(f"<b>{heading}</b><br><small>{hint}</small>")
    button = widgets.FileUpload(accept="image/*", multiple=True)
    status = widgets.HTML(_upload_status(folder))

    def save(change):
        for item in change["new"]:
            (Path(folder) / item["name"]).write_bytes(item["content"])
        button.value = ()
        status.value = _upload_status(folder)

    button.observe(save, names="value")
    return widgets.VBox([title, button, status],
                        layout=widgets.Layout(width="330px"))


def _upload_status(folder):
    files = _uploaded(folder)
    if not files:
        return "<small>Nothing uploaded yet.</small>"
    return f"<small>{len(files)} ready: {', '.join(f.name for f in files)}</small>"


def _reset_uploads_once():
    """Start each fresh kernel with empty upload folders.

    The flag keeps a same-kernel re-run of the first cell from deleting photos
    the student just uploaded. Restarting the kernel reloads this module,
    resets the flag, and clears the previous session's files.
    """
    global _UPLOADS_RESET
    if _UPLOADS_RESET:
        return
    for folder in (TEACH_DIR, TEST_DIR):
        path = Path(folder)
        if path.is_dir():
            for uploaded in path.iterdir():
                if uploaded.is_file() or uploaded.is_symlink():
                    uploaded.unlink()
    _UPLOADS_RESET = True


def photo_uploader():
    """Two upload buttons: the photos to teach with, and the one to test with.

    Photos land in ./my_photos for this kernel session. A fresh kernel clears
    the previous session's uploads; re-running this cell in the same kernel
    keeps them. Holding one photo back is the point of the lab: the device
    meets it once before it has been taught anything, and once after. Leave
    both empty for the bundled example.
    """
    import ipywidgets as widgets
    from IPython.display import display

    _reset_uploads_once()
    display(widgets.HBox([
        _upload_box(TEACH_DIR, "Teach with these",
                    "Two or more photos of one object, from different "
                    "angles or in different places."),
        _upload_box(TEST_DIR, "Test with this one",
                    "One more photo of the same object. Leave this one out "
                    "of the teaching photos."),
    ]))


def object_photos():
    """The photos to teach with, and the one held back to test with.

    Reads the two folders the upload buttons write to, and falls back to the
    bundled example when both are empty.
    """
    teach = [str(f) for f in _uploaded(TEACH_DIR)]
    test = [str(f) for f in _uploaded(TEST_DIR)]
    if not teach and not test:
        example = [EXAMPLE_OBJECT + f"{i}.jpg" for i in (1, 2, 3)]
        print("Bundled example: rubber duck, 2 to teach with, 1 to test")
        return example[:2], example[2]
    if len(teach) < 2 or len(test) != 1:
        raise ValueError(
            f"Found {len(teach)} photo(s) to teach with and {len(test)} to "
            "test with. Upload two or more on the left and exactly one on "
            "the right, or leave both empty for the bundled example."
        )
    print(f"{len(teach)} photos to teach with, 1 held back to test")
    return teach, test[0]
