"""Optional webcam capture for L6, using ipywebrtc (a Jupyter camera widget).

`camera()` shows the webcam with a snapshot button; `snapshot_to_file()` saves
the most recent snapshot to disk so CLIP can embed it. When the widget stack or
a camera is missing (the case on a headless sandbox), `camera()` returns None
and the lesson falls back to the bundled object photos.
"""


def camera():
    """Show the webcam with a snapshot button. Returns an ipywebrtc
    ImageRecorder, or None when no camera widget is available."""
    try:
        from ipywebrtc import CameraStream, ImageRecorder
    except ImportError:
        print("ipywebrtc is not installed; use a bundled photo path instead.")
        return None
    stream = CameraStream(constraints={"video": True, "audio": False})
    return ImageRecorder(stream=stream)


def snapshot_to_file(recorder, path="./capture.jpg"):
    """Save the recorder's latest snapshot to `path` and return it.

    Click the snapshot button in the camera widget first, then run this.
    """
    from io import BytesIO
    from PIL import Image
    data = recorder.image.value
    if not data:
        raise RuntimeError(
            "No snapshot yet: click the camera's capture button, then re-run."
        )
    Image.open(BytesIO(data)).convert("RGB").save(path)
    return path
