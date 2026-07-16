# L6 demo build — instructions for a fresh session

Build the bespoke, instructor-side robot/demo app that L6's video records. It is a **separate repo, never shipped to students**; the course repo ships nothing for L6. Read this file, then `.build/design/L6/SCRIPT.md` (provisional — the demo must make its claims true), `.build/design/L6/SHOTLIST.md` (the beats the app must produce on screen), and the L6 section of `.build/PLAN.md` before writing code.

## What it is

A continuously-running memory loop on a camera + mic: **capture → detect → embed → match → teach**. Show it an object it doesn't know, it says so; teach it with one spoken sentence ("this is my mug"); it recognizes the object from a new angle seconds later and recalls what you said about it. Ask "what did you see today?" and it answers from its memory. Power-cycle it offline and both skills still work.

## Hard constraints (the honest-claim contract)

The course claims on camera: "the robot's memory code mirrors what you wrote." That is only true if the stack is exactly the course's:

- **qdrant-edge-py 0.7.2** (pin it), one `EdgeShard` with two named vectors: `text` 768 / `image` 512, cosine — the same shape as the L5 `assistant_shard`.
- **CLIP ViT-B/32 via FastEmbed** (`Qdrant/clip-ViT-B-32-vision` + `Qdrant/clip-ViT-B-32-text`, 512-d) for images and cross-modal queries.
- **Nomic-Embed-Text v1.5 via FastEmbed** (768-d) for transcripts and text queries (`query_embed` for questions — the prefix matters).
- **whisper-base via onnx-asr** for speech-to-text.
- **`RECOGNIZE_THRESHOLD = 0.80` default, same nearest-match ≥ threshold check as L5.** The number is a calibration knob (`--threshold`), not scripture — demo quality rules (Dylan, 2026-07-15). What must hold is coherence: if live calibration moves it, edit L5 to the same number and re-reconcile L5's outputs, so the script's "same number, same check" claim stays true.
- **Teach-by-voice writes ONE point carrying BOTH named vectors** (`image` from the crop, `text` from the transcript) plus the transcript and metadata in the payload — this contract is written into SCRIPT.md beat 5 and SHOTLIST shot 2, and the screen capture must show both vector names.
- Every score shown on screen is a real, live value. **No fabricated output anywhere.** Fleet sync (SHOTLIST shot 7) exists only if actually wired; otherwise it does not exist.

## Reference implementation

`/Users/dylanc/Documents/GitHub/hive-mind` is the local checkout of [qdrant-labs/memory-fleet]. Read its `CLAUDE.md` and `fleetmemory/` first. Reuse its capture → detect → track → crop loop design and its YOLOE usage (prompt-free `yoloe-11l-seg-pf.pt` sits in that repo root, 70 MB — copy it, labels are discarded: "detection finds *a thing*; memory tells it *which* thing"). **Replace** its embedding stack (Unicom → CLIP via FastEmbed) and add the audio path (mic → Whisper → Nomic), which memory-fleet does not have. Its two-shard store becomes one shard with two named vectors.

## Pipeline spec

1. **Capture**: webcam via OpenCV on macOS (laptop-first; Jetson Orin Nano + TensorRT is a later, separate step — do not block on hardware). Mic capture for teach/ask; push-to-talk is fine.
2. **Detect**: YOLOE prompt-free finds and crops objects per frame. Black box, off the shelf.
3. **Cadence**: don't write memories per frame. Track what's stable in view (N consecutive frames with a persistent detection) before it becomes a match candidate or teachable. Keep this simple; it's narrated as "engineering around the loop, not taught."
4. **Match**: CLIP-embed the crop, `Query.Nearest` on `image`, compare top score to 0.80. Above: recognized — show label + score + recall the stored note. Below: unknown — visibly invite teaching.
5. **Teach by voice**: capture utterance → Whisper transcript → one upsert: `{image: clip_vec, text: nomic_vec}` + payload (transcript, label parsed or free-form, timestamp).
6. **"What did you see today?"**: voice or typed question → recall in both spaces (Nomic on `text`, CLIP text tower on `image`), **with a timestamp-window filter for "today"** — this is the course's one filtered-recall mapping (L3, the only lesson that teaches filters). Results grouped seen vs heard, never merged across spaces.
7. **Offline reboot**: a demo command that closes the shard, drops the network (airplane mode is toggled on camera by the presenter), reloads from disk, and re-runs recognition + the day question. **This beat now carries the course's only on-camera offline/persistence proof** (L2 no longer demonstrates it live, per the current CLAUDE.md) — it is a must-have, not a stretch.

## On-screen view (this is what gets filmed)

Per SHOTLIST: a live view showing the camera feed, the active crop, the nearest-match score against the 0.80 line, and memory writes as they happen — the numbers are the evidence and must be legible on video. UI rules from Dylan's standing feedback: **no dark low-contrast generic-terminal look**; high contrast, readable from across a room, styled for the domain. A simple always-on-top window or local web page is fine; polish the readability, not the chrome.

## Dev + dogfooding mode

Everything must run headless too: image-directory / video-file input instead of the webcam, WAV files instead of the mic. This enables development without camera permissions and lets cheap-model subagents dogfood it per PLAN.md ("drive it, try to break it") with scripted sessions. Add one smoke test that runs the whole loop on files: teach two crops + one WAV → recognize a held-out crop ≥ 0.80 → day-question returns the taught memory → close/reload → both repeat.

## Repo mechanics

- New repo at `/Users/dylanc/Documents/GitHub/l6-robot` (rename if Dylan prefers). Own venv or uv project; deps: qdrant-edge-py==0.7.2 pin, fastembed, onnx-asr, onnxruntime, ultralytics (YOLOE), opencv-python, numpy. Keep the dependency list this short.
- Local git, **no remote, no push, no publishing** without Dylan's explicit ask. Commit per working milestone.
- Ponytail applies: smallest app that produces every SHOTLIST beat honestly. No config systems, no plugin architecture, no speculative fleet code.

## Definition of done

1. File-mode smoke test passes end to end (the loop above).
2. Live on the MacBook webcam: unknown → teach by voice → recognized from a new angle ≥ 0.80, with real scores on screen.
3. "What did you see today?" answers from the session's memory with the time filter.
4. Offline reboot beat reproducible exactly as SHOTLIST shot 6 describes.
5. Then: reconcile `.build/design/L6/SCRIPT.md` against real recorded values (it is marked PROVISIONAL for exactly this) and drop the banner only when every claim matches app output.

## Open items you do NOT own

Jetson purchase, TensorRT export, the shoot itself, and fleet sync. Flag anything that blocks them; build nothing for them.
