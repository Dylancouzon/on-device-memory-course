# Building On-Device AI Memory with Qdrant Edge

A [DeepLearning.AI](https://www.deeplearning.ai) short course by [Qdrant](https://qdrant.tech). Instructor: **Dylan Couzon**, Developer Advocate at Qdrant.

<p align="center">
  <img src="assets/qdrant-edge-scheme.png" alt="Qdrant Edge architecture" width="600">
</p>

## What it is

You have models that run on a device and you know vector search. The missing piece is **memory**: somewhere an AI keeps personal facts that grow over time, survive restarts, stay private, and work with the network off.

This course builds that memory with **Qdrant Edge**, the Qdrant vector search engine running inside your process, with no server. You store notes, photos, and voice transcripts on-device and recall them by meaning, time, and place. The same pattern powers a phone assistant (Lab 5) and a device that learns a new object by writing to memory instead of retraining (Lab 6).

## How it works

- **The store is a file, not a server.** `EdgeShard` runs Qdrant inside your app and keeps its data on local disk. Close it and the memory persists, in the same format as server Qdrant.
- **One shard, two kinds of memory.** Nomic-Embed-Text encodes text and voice (768-d); CLIP encodes photos (512-d). They live as two named vectors, so you can find a photo by describing it.
- **Filter while you search.** Metadata (time, place, category, price) is applied inside the query, so recall is similarity *and* context, not similarity alone.
- **Everything runs offline** in a small CPU-only container: the same limits a phone, a Pi, or a robot gives you.

## What you'll build

| # | Lesson | Format | What you take away |
|---|--------|--------|--------------------|
| 1 | The On-Device Memory Problem | Video + Notebook | Why cloud-only memory breaks offline; your first `EdgeShard` on disk |
| 2 | An Embedded Memory Engine | Notebook | A memory store that recalls offline and survives a restart |
| 3 | Multimodal Memory: Text and Photos | Notebook | Find a photo by describing it; the right model per modality |
| 4 | Contextual Filtering for Memory | Notebook | Time and payload filters inside one query |
| 5 | Lab: Smartphone Assistant | Notebook | A day of photos, a voice note, and text notes; ask your own questions and add your own memories |
| 6 | Lab: Teach a Device a New Object | Notebook | Teach an object from a few photos, then recognize it from a new angle, no retraining |

*Optional appendix (coming): Cloud Sync and Cross-Device. The six lessons stand alone without it.*

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

CPU-only, fits the 4 GB sandbox. No account or API key: the models download once through FastEmbed, then run offline.

## How it's built

```
L1/ … L6/            one folder per lesson (run in order)
  L{n}.ipynb         the notebook
  helper.py          supporting code the lesson imports (embeddings, charts, offline guard)
  requirements.txt   the lesson's dependencies
data/memories.json   one day of text, voice, and photo memories (L2, L4, L5)
data/images/         scene photos (L3, L5)
data/objects/        multi-view object photos (L6)
requirements.txt     every dependency the course uses
```

Every Qdrant Edge call (create, upsert, query, filter) is written out in the notebook cells, so the API stays in view; the helpers hold only supporting code. Each lesson folder is self-contained, and every chart is labeled with where its numbers came from.

## Apply it to your own data

- **Text and voice:** edit `data/memories.json` with your own entries; the same embedding and `upsert_points` code handles them.
- **Photos:** drop images in `data/images/`, embed them with CLIP, and store one `Point` per image under the `"image"` vector.
- **Filters:** add payload fields to your points, index them with `create_field_index`, and build conditions with `Filter` and `FieldCondition`.
- **Models:** swap the FastEmbed model in `helper.py`, and keep the vector dimension in the shard config in sync.

## Who should join

Anyone comfortable with basic Python who knows the basics of embeddings and vector search. It picks up where Qdrant's [Retrieval Optimization](https://qdrant.tech/blog/qdrant-deeplearning-ai-course/) course leaves off.

## Image credits

Sample photos are used under their respective licenses (all CC0 or CC BY-SA), with full attribution (author, license, link) in `data/images/CREDITS.json` and `data/objects/CREDITS.json`.
