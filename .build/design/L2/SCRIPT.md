# L2 — Store and Recall — script

**Target runtime:** ~9 min

NOTEBOOK beats reference the section numbers as they appear in the
executed `L2.ipynb`.

One question threads the lesson: "where can I sit outside for a latte?"
It is asked four times — of the empty store, after storing, after
forgetting, and after a restart. Slides: the endpoint teaser and the
anatomy of a point.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Endpoint teaser + what you'll build | 40 |
| 2 | SLIDE 1 | The memory loop, this lesson's piece highlighted | 20 |
| 3 | NOTEBOOK §1 | Ask before there's memory — the empty shard returns nothing | 40 |
| 4 | NOTEBOOK §2 | The memories — a day's notes | 25 |
| 5 | NOTEBOOK §3 | Embed the notes locally | 30 |
| 6 | SLIDE 2 | Anatomy of a point | 30 |
| 7 | NOTEBOOK §4 | Store the memories (Point, upsert, optimize) | 35 |
| 8 | NOTEBOOK §5 | **The payoff:** ask again — keyword search fails, meaning succeeds | 55 |
| 9 | NOTEBOOK §6 | **The payoff:** recall with the network off | 40 |
| 10 | NOTEBOOK §7 | **The payoff:** local recall at 5,000 memories | 40 |
| 11 | NOTEBOOK §8 | **The payoff:** forget a memory (third ask) | 55 |
| 12 | NOTEBOOK §9 | **The payoff:** a restart keeps what you kept, not what you forgot | 55 |
| 13 | WRAP | The lifecycle, what's next | 40 |

Total: ~505 sec (~8.5 min).

---

## Beat 1 — INTRO

**NARRATION:**

By the end of this course, you'll have an assistant that answers a question
like "the ramen place downtown" with the photo you took, the voice memo you
left, and the notes you wrote — all from memory that lives on the device.
This lesson builds the first piece: a store for personal notes. One question
will carry us through the whole lifecycle of a memory. We'll ask it four
times: before anything is stored, after storing, after forgetting, and after
a restart. Let's build something.

---

## Beat 2 — SLIDE 1: the memory loop, this lesson highlighted

```slide-brief
slug: l2-00-endpoint
purpose: the endpoint teaser — the course's capture → embed → store →
  recall loop with this lesson's stages highlighted.
on-slide text: node labels only — "capture", "embed", "store", "recall",
  small tag "this lesson". No headline.
diagram spec (8:9, stack top-to-bottom):
  - Four hand-drawn rounded nodes in a vertical loop: light-blue
    (#03A9F4) "capture", orange (#FF9800) "embed", violet (#6047FF)
    cylinder "store", red (#DC244C) "recall", curved arrows connecting
    them, the recall arrow curving back up toward capture.
  - "store" and "recall" get a solid stroke and full-strength fill;
    "capture" and "embed" render at reduced opacity.
  - A small hand-lettered tag "this lesson" pointing at the highlighted
    pair. Small spiral-notebook motif beside the cylinder.
```

**NARRATION:**

Here's the loop the whole course builds: capture something, embed it, store
it, recall it. Today is the store-and-recall half — plus the two verbs that
make it a memory and not a log: forgetting, and surviving a restart.

---

## Beat 3 — NOTEBOOK §1: ask before there's anything to remember

Run the setup cell, then the cold-open query cell.

**NARRATION:**

Before we store a single thing, let's ask the assistant a question. First
the store itself. The config declares one named vector called `text`: 768
dimensions to match the text embedding model, compared by cosine distance.
`EdgeShard.create` builds the store in a local directory — a shard is the
unit a Qdrant collection is made of; on a server a collection spans many
shards, and Edge gives you exactly one, running inside your process. No
server to start, no account to connect.

Now ask, "where can I sit outside for a latte?" Zero results. The model is
already loaded, but there is nothing to recall yet. Hold onto that exact
question — we'll ask it three more times, and nothing about the model will
change between the asks.

---

## Beat 4 — NOTEBOOK §2: the memories

Run the notes cell.

**NARRATION:**

Here are the memories themselves. These are the kinds of notes a phone
assistant might keep during a day: a coffee shop, a meeting time, a
reminder, an idea, an address, and a pair of shoes.

---

## Beat 5 — NOTEBOOK §3: turn notes into vectors, on the device

Run the embed cell.

**NARRATION:**

To search by meaning rather than by exact words, we turn each note into a
vector. FastEmbed runs Nomic-Embed-Text v1.5 locally and produces 20 vectors
of the same size. After the model is available locally, embedding runs
offline; the helper keeps the loading details out of the way.

---

## Beat 6 — SLIDE 2: anatomy of a point

```slide-brief
slug: anatomy-of-a-point
purpose: show the three parts of a stored memory before the notebook writes
  one — model this on the article's "anatomy of a point" reference in
  SLIDE_STYLE.md.
on-slide text: compartment labels only — "id: 3", "named vector — text",
  "payload — note + fields". No headline.
diagram spec (8:9, stack top-to-bottom):
  - One large rounded container, violet (#6047FF) stroke and ~15% fill,
    hand-lettered title "Point" at top.
  - Inside, three stacked compartments (thin dashed dividers), each with a
    small icon + label, read top to bottom:
      1. tag/hash icon — "id: 3"
      2. waveform icon + small vector-cell strip (orange #FF9800 accent) —
         "named vector — text"
      3. small document/page icon — "payload — note + fields"
  - No arrows needed; this is a single object, not a flow. Keep margins
    generous.
```

**NARRATION:**

Before we store anything, look at what actually gets stored. A point is
three things: an id, a named vector, and a payload. The payload is the
original text plus any metadata you want to carry along. That's the whole
shape of a memory in the store.

---

## Beat 7 — NOTEBOOK §4: store the memories

Run the Point / upsert_points / optimize cell.

**NARRATION:**

Now we turn each note into a `Point`: an ID, the named vector, and a
payload. The payload holds the note text and its fields. We upsert all 20
points in one batch, then call `optimize()`. Edge has no background
optimizer, so we ask for the index build explicitly — on a server, Qdrant
does this for you in the background.

---

## Beat 8 — NOTEBOOK §5: The payoff — ask again, now it remembers

Run the keyword cell, then the recall cell.

**NARRATION:**

First, try it the old way: a literal search for the word "latte" across all
twenty notes. Zero matches — no note contains it. Now ask the exact same
question from the cold open: "where can I sit outside for a latte?" This
time the coffee place on 5th comes back on top. The model didn't change
between these two cells — the memory did. We embed the question with
`embed_query`, not `embed_text`: Nomic treats queries and documents
differently, and `embed_query` adds the prefix the model expects. And look
closely — not one word of the question, "sit", "outside", or "latte",
appears in that note. The keyword search you just ran proved it returns
nothing; the vector matched the meaning. This is the query grep can't run.

---

## Beat 9 — NOTEBOOK §6: The payoff — recall with the network off

Run the `no_network()` cell.

**NARRATION:**

`no_network()` blocks sockets, so any network call inside the block fails
loudly. Run the cell, and recall still returns the standup note with Sarah.
Both embedding and search ran in this process, with the network disabled.

---

## Beat 10 — NOTEBOOK §7: The payoff — local recall at scale

Run the 5,000-memory build-up cell. Point at the printed median-ms line.

**NARRATION:**

How fast is this at a realistic scale? A device fills up with memories over
months, so we grow the store to 5,000 memories, using random filler
vectors — content doesn't matter here, latency depends on how many vectors
there are and how wide they are, not on what they mean. We time 200 recalls,
in the open, and take the median. Even at 5,000 memories, on this CPU-only
container, recall stays well under a millisecond. The whole lookup runs
in-process, over local files, with nothing leaving the device.

---

## Beat 11 — NOTEBOOK §8: The payoff — forget a memory

Run the delete cell, then the third-ask cell.

**NARRATION:**

Growing is only half of memory — the other half is forgetting. Wrong notes,
stale ones, anything you no longer want: you delete it by id, then optimize.
So let's forget the coffee place. `delete_points` takes the id of the top
hit you just saw, and it's gone. Now the third ask of our question. A
different memory surfaces — the quiet cafe near the park — at a lower
score: the store answers with the best it still has. Look at the
before-and-after: the café note is marked as dropped, and the other notes
are untouched, same scores as before. Forgetting removes exactly what you
deleted, not every trace.

---

## Beat 12 — NOTEBOOK §9: The payoff — a restart keeps what you kept

Run the close / files / `EdgeShard.load` cell.

**NARRATION:**

Last payoff: does this memory survive a restart — including the forgetting?
We close the shard, which flushes it to disk and releases the handle. Look
at what remains: plain files in a local folder. The Python object is gone;
the memory store is still there. Then we reopen the same directory with
`EdgeShard.load`, with Python socket creation blocked, and ask the question
a fourth time. The receipt says it all: the point count matches, the top hit
is the same one the third ask found, and the note you deleted stays
forgotten after the restart. That's persistence: not a promise, a check you
can run yourself.

---

## Beat 13 — WRAP

**NARRATION:**

That's the full lifecycle of a memory, in one lesson: store, recall, forget,
persist. You've seen the Edge API once, end to end: `EdgeConfig` and
`EdgeShard.create` to build the store, `Point` and `UpdateOperation` to
write and delete, `QueryRequest` and `Query.Nearest` to recall, `close()`
and `EdgeShard.load` to persist. Those calls stay visible in the notebook
cells, so you can see exactly what the shard is doing. The helpers handle
only the supporting plumbing: embeddings, charts, and the offline guard.

Next lesson, we keep this text encoder and add a second one, for photos, so
you can find a picture by describing it — and filter what comes back.
