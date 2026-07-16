# L2: Store and Recall (script)

**Target runtime:** ~7 min

NOTEBOOK beats reference the section numbers as they appear in the
executed `L2.ipynb`.

One question threads the lesson: "where can I sit outside for a latte?"
It is asked three times: of the empty store, after storing, and after
forgetting. Slides: the endpoint teaser and the anatomy of a point.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | What you'll build + the one question, three times | 25 |
| 2 | SLIDE 1 | The memory loop, this lesson's piece highlighted | 20 |
| 3 | NOTEBOOK §1 | Build the store, then ask the empty shard: nothing back | 55 |
| 4 | NOTEBOOK §2 | The memories, a day's notes | 25 |
| 5 | NOTEBOOK §3 | Embed the notes locally, shown in the open | 40 |
| 6 | SLIDE 2 | Anatomy of a point | 30 |
| 7 | NOTEBOOK §4 | Store the memories (Point, upsert, optimize) | 35 |
| 8 | NOTEBOOK §5 | Ask again, now it remembers (second ask) | 40 |
| 9 | NOTEBOOK §6 | Local lookup at 5,000 memories | 40 |
| 10 | NOTEBOOK §7 | Forget a memory (third ask) | 55 |
| 11 | WRAP | The lifecycle, persistence, what's next | 40 |

Total: ~405 sec (~6.75 min).

---

## Beat 1: INTRO

**NARRATION:**

This lesson builds the first piece of that assistant: a store for personal
notes. One question will carry us through the whole lifecycle of a memory.
We'll ask it three times: before anything is stored, after storing, and
after forgetting. Let's build something.

---

## Beat 2: SLIDE 1, the memory loop, this lesson highlighted

```slide-brief
slug: l2-00-endpoint
purpose: the endpoint teaser. The course's capture → embed → store →
  recall loop with this lesson's stages highlighted.
on-slide text: node labels only: "capture", "embed", "store", "recall",
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
it, recall it. Today is the store-and-recall half, plus forgetting, the
verb that turns a log into a memory.

---

## Beat 3: NOTEBOOK §1, ask before there's anything to remember

Run the setup cell, then the cold-open query cell.

**NARRATION:**

Before we store a single thing, let's ask the assistant a question. But
first we build the store itself.

`EdgeConfig` is the blueprint: it says what every memory in this store will
look like. It declares one named vector called `text`, sized 768 to match
the text embedding model we'll use; the model produces vectors of exactly
that length. Cosine is how two vectors get compared: it measures whether
they point the same way, which is what "close in meaning" comes down to. We
give the vector a name because a single memory will soon hold more than one
kind, text now, photos in the next lesson, and the names keep them apart.

`EdgeShard.create` takes that blueprint and builds the store in a local
directory: a single shard running inside your process. No server to start,
no account to connect.

Now ask, "where can I sit outside for a latte?" Zero results. The model is
already loaded, but there is nothing to recall yet. Hold onto that exact
question. We'll ask it two more times, and nothing about the model will
change between the asks.

---

## Beat 4: NOTEBOOK §2, the memories

Run the notes cell.

**NARRATION:**

Here are the memories themselves. These are the kinds of notes a phone
assistant might keep during a day: a coffee shop, a meeting time, a
reminder, an idea, an address, and a pair of shoes.

---

## Beat 5: NOTEBOOK §3, turn notes into vectors, on the device

Run the embed cell.

**NARRATION:**

To search by meaning instead of by exact words, we turn each note into a
vector. This is the one place we do it in the open. We load
Nomic-Embed-Text v1.5 through FastEmbed, a small model that runs on the
device, and call `embed` on the twenty notes. Back come twenty vectors,
768 numbers each: the note's meaning as coordinates. From here on a helper
wraps this same call to keep the cells short, but the work never changes:
text goes in, vectors come out, and none of it leaves the machine.

---

## Beat 6: SLIDE 2, anatomy of a point

```slide-brief
slug: anatomy-of-a-point
purpose: show the three parts of a stored memory before the notebook writes
  one. Model this on the article's "anatomy of a point" reference in
  SLIDE_STYLE.md.
on-slide text: compartment labels only: "id: 3", "named vector · text",
  "payload · note + fields". No headline.
diagram spec (8:9, stack top-to-bottom):
  - One large rounded container, violet (#6047FF) stroke and ~15% fill,
    hand-lettered title "Point" at top.
  - Inside, three stacked compartments (thin dashed dividers), each with a
    small icon + label, read top to bottom:
      1. tag/hash icon: "id: 3"
      2. waveform icon + small vector-cell strip (orange #FF9800 accent):
         "named vector · text"
      3. small document/page icon: "payload · note + fields"
  - No arrows needed; this is a single object, not a flow. Keep margins
    generous.
```

**NARRATION:**

Before we store anything, look at what actually gets stored. A point is
three things: an id, a named vector, and a payload. The payload is the
original text plus any metadata you want to carry along. That's the whole
shape of a memory in the store.

---

## Beat 7: NOTEBOOK §4, store the memories

Run the Point / upsert_points / optimize cell.

**NARRATION:**

Now we turn each note into a `Point`: an ID, the named vector, and a
payload. The payload holds the note text and its fields. We upsert all 20
points in one batch, then call `optimize()`. Edge has no background
optimizer, so we ask for the index build explicitly. On a server, Qdrant
does this for you in the background.

---

## Beat 8: NOTEBOOK §5, ask again, now it remembers

Run the recall cell.

**NARRATION:**

Now ask the exact same question from the cold open: "where can I sit outside
for a latte?" This time the coffee place on 5th comes back on top, at 0.65.
The model didn't change between the empty ask and this one. The memory did.
One detail worth naming: we embed the question with `embed_query`, which adds
the prefix Nomic uses for questions so its score lines up with the stored
notes. And look closely: not one word of the question, "sit", "outside", or
"latte", appears in that note. The match is the meaning, not the words. That
is the search a plain keyword scan can't do.

---

## Beat 9: NOTEBOOK §6, local lookup at scale

Run the 5,000-memory build-up cell. Point at the median line on the chart.

**NARRATION:**

How fast is this at a realistic scale? A device fills up with memories over
months, so we grow the store to 5,000 memories, using random filler
vectors. Content doesn't matter here; latency depends on how many vectors
there are and how wide they are, not on what they mean. We time 200
lookups, in the open, and here's the whole distribution as a chart, with
the median marked. To be precise about what's measured: this is the vector
lookup itself; embedding the question happens once, before the clock
starts. Even at 5,000 memories, on this CPU-only container, the lookup
stays well under a millisecond. It runs in-process, over local files, with
nothing leaving the device.

---

## Beat 10: NOTEBOOK §7, forget a memory

Run the delete cell, then the third-ask cell.

**NARRATION:**

Growing is only half of memory. The other half is forgetting. Wrong notes,
stale ones, anything you no longer want: you delete it by id, then optimize.
So let's forget the coffee place. `delete_points` takes the id of the top
hit you just saw, and it's gone. Now the third ask of our question. A
different memory surfaces, the quiet cafe near the park, at a lower
score: the store answers with the best it still has. Look at the
before-and-after: the café note is marked as dropped, and the other notes
are untouched, same scores as before. Forgetting removes exactly what you
deleted, not every trace.

---

## Beat 11: WRAP

**NARRATION:**

That's the lifecycle of a memory, in one lesson: store it, recall it by
meaning, and forget it on command. And because the store is just files in a
local folder, it is still there when you close the app and open it later.
Nothing to sync, nothing to reload from a server. Every call the shard made
stayed visible in the cells, so you can see exactly what it is doing; the
helpers handle only the supporting plumbing, like the query wrapper and the
charts.

Next lesson, we keep this text encoder and add a second one, for photos, so
you can find a picture by describing it, and filter what comes back.
