# L2 — Qdrant Edge: An Embedded Memory Engine — Script

**Target runtime:** ~8 min

NOTEBOOK beats reference the section numbers as they appear in the
executed `L2.ipynb`.

Slides cut to one: the in-process architecture slide is covered in L1, and
the offline-recall-loop slide just re-drew a result the notebook already
proves. Only "anatomy of a point" earns its place, ahead of writing one.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | What memory is and what you'll build | 30 |
| 2 | NOTEBOOK §1 | Ask before there's memory — the empty shard returns nothing | 35 |
| 3 | NOTEBOOK §2 | The memories — a day's notes | 25 |
| 4 | NOTEBOOK §3 | Embed the notes locally with Nomic | 30 |
| 5 | SLIDE 1 | Anatomy of a point | 30 |
| 6 | NOTEBOOK §4 | Store the memories (Point, upsert, optimize) | 35 |
| 7 | NOTEBOOK §5 | Ask again — now it remembers (meaning, not keywords) | 45 |
| 8 | NOTEBOOK §6 | **The payoff:** recall with the network off | 50 |
| 9 | NOTEBOOK §7 | **The payoff:** local recall at 5,000 memories | 45 |
| 10 | NOTEBOOK §8 | **The payoff:** memory survives a restart | 55 |
| 11 | WRAP | Wrap: the pattern, what's next | 45 |

Total: ~445 sec (~7.5 min).

---

## Beat 1 — INTRO

**NARRATION:**

Your AI can run a model on the device and search vectors, but it still needs
a place to keep what it learns about you. In this lesson, you'll build that
place: a local store for personal notes that survives a restart and works
without a network connection. Let's build something.

---

## Beat 2 — NOTEBOOK §1: ask before there's anything to remember

Run the cold-open cell.

**NARRATION:**

Before we store a single thing, let's ask the assistant a question. We create
the shard — empty — and ask, "where can I sit outside for a latte?" Zero
results. The model is already loaded, but there is nothing to recall yet.
Hold onto that exact question; we'll ask it again once the notes are in, and
nothing about the model will have changed between the two cells.

---

## Beat 3 — NOTEBOOK §2: the memories

Run the notes cell.

**NARRATION:**

Here are the memories themselves. These are the kinds of notes a phone
assistant might keep during a day: a coffee shop, a meeting time, a reminder,
an idea, an address, and a pair of shoes. The coffee-shop note with outdoor
seating is the one from L1; we'll return to it later in the course.

---

## Beat 4 — NOTEBOOK §3: turn notes into vectors, on the device

Run the embed cell.

**NARRATION:**

To search by meaning rather than by exact words, we turn each note into a
vector. FastEmbed runs Nomic-Embed-Text v1.5 locally and produces 20 vectors
of the same size. After the model is available locally, embedding runs
offline; the helper keeps the loading details out of the way.

---

## Beat 5 — SLIDE 1: anatomy of a point

```slide-brief
slug: anatomy-of-a-point
purpose: show the three parts of a stored memory before the notebook writes
  one — model this on the article's "anatomy of a point" reference in
  SLIDE_STYLE.md.
on-slide text: compartment labels only — "id: 3", "named vector — text",
  "payload — note + kind". No headline.
diagram spec (8:9, stack top-to-bottom):
  - One large rounded container, violet (#6047FF) stroke and ~15% fill,
    hand-lettered title "Point" at top.
  - Inside, three stacked compartments (thin dashed dividers), each with a
    small icon + label, read top to bottom:
      1. tag/hash icon — "id: 3"
      2. waveform icon + small vector-cell strip (orange #FF9800 accent) —
         "named vector — text"
      3. small document/page icon — "payload — note + kind"
  - No arrows needed; this is a single object, not a flow. Keep margins
    generous.
```

**NARRATION:**

Before we store anything, look at what actually gets stored. A point is
three things: an id, a named vector, and a payload. The payload is the
original text plus any metadata you want to carry along. That's the whole
shape of a memory in Qdrant Edge.

---

## Beat 6 — NOTEBOOK §4: store the memories

Run the Point / upsert_points / optimize cell.

**NARRATION:**

Now we turn each note into a `Point`: an ID, the named vector, and a payload.
The payload holds the note text and its type. We upsert all 20 points in one
batch, then call `optimize()`. Edge has no background optimizer, so we ask for
the index build explicitly — on a server, Qdrant does this for you in the
background.

---

## Beat 7 — NOTEBOOK §5: ask again — now it remembers

Run the recall cell.

**NARRATION:**

Now ask the exact same question from the cold open: "where can I sit outside
for a latte?" This time the coffee place on 5th comes back on top. The model
didn't change between these two cells — the memory did. We embed the question
with `embed_query`, not `embed_text`: Nomic treats queries and documents
differently, and `embed_query` adds the prefix the model expects. And look
closely — not one word of the question, "sit", "outside", or "latte", appears
in that note. Keyword search would return nothing. The vector matched the
meaning. This is the query grep can't run.

---

## Beat 8 — NOTEBOOK §6: The payoff — recall with the network off

Run the `no_network()` cell.

**NARRATION:**

Here's the first payoff. `no_network()` blocks sockets, so any network call
inside the block fails loudly. Run the cell, and recall still returns the
standup note with Sarah. Both embedding and search ran in this process, with
the network disabled.

---

## Beat 9 — NOTEBOOK §7: The payoff — local recall at scale

Run the 5,000-memory build-up cell. Point at the printed median-ms line.

**NARRATION:**

Second payoff: how fast is this at a realistic scale? A device fills up with
memories over months, so we grow the store to 5,000 memories, using random
filler vectors — content doesn't matter here, latency depends on how many
vectors there are and how wide they are, not on what they mean. We time 200
recalls, in the open, and take the median. Even at 5,000 memories, on this
CPU-only container, recall stays in the low milliseconds. The whole lookup
runs in-process, over local files, with nothing leaving the device.

---

## Beat 10 — NOTEBOOK §8: The payoff — memory survives a restart

Run the close / `EdgeShard.load` cell.

**NARRATION:**

Last payoff: does this memory survive a restart? We record today's top
result, then close the shard, which flushes it to disk and releases the
handle. Then we reopen the same directory with `EdgeShard.load`, with Python
socket creation still blocked, and check: is the memory still there, does it
still rank first?

Look at the receipt table — same top result, the point count matches, and no
Python socket was opened during the reopen. That's persistence: not a promise,
a check you can run yourself.

---

## Beat 11 — WRAP

**NARRATION:**

You've now seen the Edge API once, end to end: `EdgeConfig` and
`EdgeShard.create` to build the store, `Point` and `UpdateOperation` to
write, `QueryRequest` and `Query.Nearest` to recall, `close()` and
`EdgeShard.load` to persist. Those calls stay visible in the notebook cells,
so you can see exactly what the shard is doing. The helpers handle only the
supporting plumbing: embeddings, charts, and the offline guard.

Next lesson, we keep this text encoder and add a second one, for photos, so
you can find a picture by describing it in words.
