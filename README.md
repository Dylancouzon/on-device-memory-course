# Building On-Device AI Memory with Qdrant Edge

A [DeepLearning.AI](https://www.deeplearning.ai) short course built by [Qdrant](https://qdrant.tech). Instructor: Dylan Couzon.

<p align="center">
  <img src="assets/qdrant-edge-scheme.png" alt="Qdrant Edge architecture" width="600">
</p>

## What it is

On-device AI needs **memory**: a place to keep personal facts that grow over time, survive restarts, stay private, and work with the network off. This course builds that memory with **Qdrant Edge**, the Qdrant vector search engine running inside your process with no server. You store notes, photos, and voice transcripts on-device and recall them by meaning, with filters when you need them.

## How it works

- **The store is a file, not a server.** `EdgeShard` runs Qdrant inside your app on local disk. Close it and the memory persists, in the same format as server Qdrant.
- **One shard, two kinds of memory.** Nomic-Embed-Text encodes text and voice (768-d); CLIP encodes photos (512-d), as two named vectors. Describe a photo in words and find it.
- **Filter while you search.** Fields like category and price are applied inside the query, so recall is similarity *and* structure.
- **Everything runs offline** in a small CPU-only container, the same limits a phone, a Pi, or a robot gives you.

## Lessons

Run the notebooks in order; each folder is self-contained. L1 and L6 are
video lessons with no notebook.

| # | Lesson | What it covers |
|---|--------|----------------|
| 1 | Why Devices Need Memory | Video: why memory can't live in the cloud; the capture → embed → store → recall loop |
| 2 | Store and Recall | One question, asked three times: recall by meaning, then forget on purpose |
| 3 | Finding the Right Memory | Find a photo by describing it; narrow recall with filters inside one query |
| 4 | Your On-Device Assistant | A day of photos, voice, and text notes; on-device transcription; ask and add your own memories |
| 5 | Teaching It to See | Teach it an object from your own photos, assemble the full assistant offline, and send memory to the cloud only by choice |
| 6 | The Robot | Video: the same design walking around, every stage mapped back to the lesson that built it |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

CPU-only, fits a 4 GB sandbox. No account or API key: models download once through FastEmbed, then run offline.

Qdrant Edge is in beta and its API can change between releases. This course is validated against `qdrant-edge-py` 0.7.2, which the requirements files pin.

## How it's built

```
L2/ … L5/            one folder per notebook lesson
  L{n}.ipynb         the notebook
  helper.py          supporting code (embeddings, audio, charts, offline guard)
  requirements.txt   the lesson's dependencies
data/memories.json   one day of text, voice, and photo memories (L2–L5)
data/recent_days.json  a few weeks of earlier notes (L5)
data/bank/           everyday photos for L3's describe-a-photo bank
data/audio/          the voice-note recordings L4 transcribes on-device
data/images/         scene photos (L4, L5)
data/objects/        multi-view object photos (L5)
requirements.txt     every dependency the course uses
```

Every Qdrant Edge call (create, upsert, query, filter) is written out in the notebook cells; helpers hold only supporting code. The layout mirrors the DLAI reference course [`SC-Qdrant-C3`](https://github.com/https-deeplearning-ai/SC-Qdrant-C3).

## Apply it to your own data

- **Text and voice:** replace the entries in `data/memories.json`; the same embedding and `upsert_points` code handles them.
- **Photos:** drop images in `data/images/`, embed them with CLIP, and store one `Point` per image under the `"image"` vector.
- **Filters:** add payload fields to your points, index them with `create_field_index`, and build conditions with `Filter` and `FieldCondition`.
- **Models:** swap the FastEmbed model in `helper.py`, and keep the vector dimension in the shard config in sync.

## Who should join

Python developers who know the basics of embeddings and vector search. It picks up where Qdrant's [Retrieval Optimization](https://qdrant.tech/blog/qdrant-deeplearning-ai-course/) course leaves off.

## Image credits

Sample photos are used under their licenses (CC0 or CC BY-SA), with full attribution in `data/bank/CREDITS.json`, `data/images/CREDITS.json`, and `data/objects/CREDITS.json`.
