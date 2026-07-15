# Building On-Device AI Memory with Qdrant Edge

A [DeepLearning.AI](https://www.deeplearning.ai) short course built by [Qdrant](https://qdrant.tech). Instructor: Dylan Couzon.

<p align="center">
  <img src="assets/qdrant-edge-scheme.png" alt="Qdrant Edge architecture" width="600">
</p>

## What it is

On-device AI needs **memory**: a place to keep personal facts that grow over time, survive restarts, stay private, and work with the network off. This course builds that memory with **Qdrant Edge**, the Qdrant vector search engine running inside your process with no server. You store notes, photos, and voice transcripts on-device and recall them by meaning, time, and place.

## How it works

- **The store is a file, not a server.** `EdgeShard` runs Qdrant inside your app on local disk. Close it and the memory persists, in the same format as server Qdrant.
- **One shard, two kinds of memory.** Nomic-Embed-Text encodes text and voice (768-d); CLIP encodes photos (512-d), as two named vectors. Describe a photo in words and find it.
- **Filter while you search.** Time, place, category, and price are applied inside the query, so recall is similarity *and* context.
- **Everything runs offline** in a small CPU-only container, the same limits a phone, a Pi, or a robot gives you.

## Lessons

Run in order; each folder is self-contained.

| # | Lesson | What it covers |
|---|--------|----------------|
| 1 | The On-Device Memory Problem | Why cloud-only memory breaks offline; your first `EdgeShard` on disk |
| 2 | An Embedded Memory Engine | A store that recalls offline and survives a restart |
| 3 | Multimodal Memory: Text and Photos | Find a photo by describing it; the right model per modality |
| 4 | Contextual Filtering for Memory | Time and payload filters inside one query |
| 5 | Lab: Smartphone Assistant | A day of photos, voice, and text notes; ask and add your own memories |
| 6 | Lab: Teach a Device a New Object | Teach an object from a few photos, recognize it from a new angle, no retraining |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

CPU-only, fits a 4 GB sandbox. No account or API key: models download once through FastEmbed, then run offline.

Qdrant Edge is in beta and its API can change between releases. This course is validated against `qdrant-edge-py` 0.7.2, which the requirements files pin.

## How it's built

```
L1/ … L6/            one folder per lesson
  L{n}.ipynb         the notebook
  helper.py          supporting code (embeddings, charts, offline guard)
  requirements.txt   the lesson's dependencies
data/memories.json   one day of text, voice, and photo memories (L2, L4, L5)
data/images/         scene photos (L3, L5)
data/objects/        multi-view object photos (L6)
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

Sample photos are used under their licenses (CC0 or CC BY-SA), with full attribution in `data/images/CREDITS.json` and `data/objects/CREDITS.json`.
