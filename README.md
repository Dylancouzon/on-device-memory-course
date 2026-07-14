# Building On-Device AI Memory with Qdrant Edge

A [DeepLearning.AI](https://www.deeplearning.ai) short course by [Qdrant](https://qdrant.tech).

Instructor: **Dylan Couzon**, Developer Advocate at Qdrant

<p align="center">
  <img src="assets/qdrant-edge-scheme.png" alt="Qdrant Edge architecture" width="600">
</p>

## What this course is

You already have models that run on a device and you know how vector search works. The missing piece is **memory**: a place for an AI to keep personal facts that grow over time, persist across restarts, stay private, and work with the network off.

This course builds that memory with **Qdrant Edge**: the Qdrant vector search engine embedded directly in your process, no server and no network. You store notes, photos, and voice transcripts on-device, then recall them by meaning, time, and place. The same memory pattern powers a phone assistant and a simulated robot.

## How it works

- **Qdrant Edge (`EdgeShard`)** embeds Qdrant's vector search engine in the application process and stores its shard on the device. The application creates the shard, stores memories, queries them, and closes the shard to flush it to disk: same data format as server Qdrant, no cluster.
- **On-device embeddings** turn each memory into a vector: Nomic-Embed-Text for text and voice transcripts (768-d), CLIP for photos (512-d). Text and images share one shard as two named vectors, so you can find a photo by describing it.
- **Payload filters** (time, location, category, price) run inside the same query, so recall is "similarity *and* context," not similarity alone.
- **Nothing needs the cloud or a phone.** You build everything locally, in a small CPU-only container with the network off — the same constrained environment an edge device gives you. The code you write here runs the same on a phone, a Pi, or a robot.

## What you'll build

| # | Lesson | Format | What you take away |
|---|--------|--------|--------------------|
| 1 | The On-Device Memory Problem | Video + Notebook | Why cloud-only memory breaks offline; your first `EdgeShard` on disk |
| 2 | An Embedded Memory Engine | Notebook | A memory store that recalls offline and survives a restart |
| 3 | Multimodal Memory: Text and Photos | Notebook | Find a photo by describing it; the right model per modality |
| 4 | Contextual Filtering for Memory | Notebook | Time and payload filters inside one query |
| 5 | Lab: Smartphone Assistant | Notebook | A day of photos, a voice note, and text notes in one Memory Inbox |
| 6 | Lab: Robot Memory Agent + Wrap-Up | Notebook | Observation memory under a budget, hazards persist, noise fades |

**Optional appendix** *(coming)*: **A. Cloud Sync & Cross-Device** (sync a shard to Qdrant Cloud with a snapshot). The six-lesson path is complete without it.

Every notebook ships fully executed, and every chart is labeled with where its numbers came from: measured live or illustrative.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

The course path is CPU-only and fits the 4 GB DLAI sandbox. No account or API token is required; models download once through FastEmbed and then run offline.

This course needs no API keys, but it follows the standard pattern so you can add your own: copy `.env.example` to `.env`. Each notebook loads it with `python-dotenv`; `.env` is gitignored so keys never reach git. L1 walks through this.

## Repository structure

```
L1/ … L6/              one folder per lesson (run in order)
  L{n}.ipynb           the notebook
  helper.py            the helpers that lesson imports (EdgeShard ops,
                       Nomic/CLIP embeddings, filters, charts, robot sim)
  requirements.txt     the lesson's dependencies
data/                  sample photos and a voice-note transcript, shared
requirements.txt       every dependency the course uses
```

## Apply it to your own data

- **Text and voice:** replace the notes in L2/L5 with your own; the same embedding and storage code handles them.
- **Photos:** drop your images in `data/images/` (or point `add_memories(..., "image", ...)` at your folder) and query them by text.
- **Filters:** add payload fields to your points and build conditions with `match`, `numeric`, and `time_window` in the lesson's `helper.py`.
- **Models:** swap the FastEmbed model in the lesson's `helper.py`; keep the vector dimension in the shard config in sync.

## Who should join

Anyone comfortable with basic Python who knows the basics of embeddings and vector search. It picks up where Qdrant's [Retrieval Optimization](https://qdrant.tech/blog/qdrant-deeplearning-ai-course/) course leaves off.

## Image credits

Sample photos in `data/images/` are used under their respective licenses (full metadata in `data/images/CREDITS.json`):

| File | License | Source | Credit |
|---|---|---|---|
| `book.jpg` | CC BY-SA 2.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:A_stack_of_wooden_books_-_geograph.org.uk_-_6462548.jpg) | Evelyn Simak |
| `coffee.jpg` | CC BY-SA 4.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:A-cup-of-cappuccino-coffee-dar-es-salaam-cafe.jpg) | Aneth David (SLU) |
| `plant.jpg` | CC BY-SA 4.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Amaryllis_(Hippeastrum)_18-01-2025._(actm.)_02.jpg) | Agnes Monkelbaan |
| `restaurant.jpg` | CC BY 2.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Elizabeth%27s_Restaurant_-_Food_and_Devices_-_New_Orleans_2016.jpg) | Infrogmation of New Orleans |
| `sneakers.jpg` | CC0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Black_white_sneakers_logo_(Unsplash).jpg) | chuttersnap |
| `street.jpg` | CC0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:City_of_Toy_Cars_(Unsplash).jpg) | Dakota Corbin |
