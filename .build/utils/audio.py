"""On-device speech-to-text for L5's voice notes.

A voice note is audio until a speech model turns it into text. This runs a small
Whisper model exported to ONNX through onnxruntime (already present for
FastEmbed), so transcription is local and offline after the first download. The
model loads lazily and once.
"""
from functools import lru_cache

WHISPER_MODEL = "whisper-base"


@lru_cache(maxsize=1)
def _asr_model():
    import onnx_asr
    return onnx_asr.load_model(WHISPER_MODEL, providers=["CPUExecutionProvider"])


def transcribe(audio_path):
    """Transcribe one audio file to text with a local Whisper model."""
    return _asr_model().recognize(audio_path).strip()
