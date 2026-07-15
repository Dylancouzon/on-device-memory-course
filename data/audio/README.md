# Voice-note audio

Five short voice memos, one per voice capture in `data/memories.json`. L4
transcribes them on-device with a small Whisper model, so the "voice" modality
is a real speech-to-text step rather than a pre-written string. Each file maps
to its note through the `audio_file` field in `data/memories.json`.
