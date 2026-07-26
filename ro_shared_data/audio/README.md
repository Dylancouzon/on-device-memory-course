# Voice-note audio

Five short voice memos, one per voice capture in `ro_shared_data/memories.json`. L4 transcribes them on-device with a small Whisper model, so the "voice" modality runs a real speech-to-text step. Each file maps to its note through the `audio_file` field in `ro_shared_data/memories.json`.
