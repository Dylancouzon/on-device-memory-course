# L2: Store and Recall (script)

**Target runtime:** ~7 min

NOTEBOOK beats reference the section numbers as they appear in the
executed `Lesson2.ipynb`.

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
| 9 | NOTEBOOK §6 | Local lookup at 5,000 memories, and the real budget | 55 |
| 10 | NOTEBOOK §7 | Forget a memory (third ask) | 55 |
| 11 | WRAP | The lifecycle, persistence, what's next | 40 |

Total: ~405 sec (~6.75 min).

---

## Beat 1: INTRO

**NARRATION:**

This lesson starts with a simple store for personal notes. We’ll ask one
question three times: before we store anything, after we store it, and after
we delete a result.

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

This is the loop behind the course. Today we focus on storing, finding, and
deleting a memory.

---

## Beat 3: NOTEBOOK §1, ask before there's anything to remember

Run the setup cell, then the cold-open query cell.

**NARRATION:**

First, create an empty store. `EdgeConfig` says it will hold one kind of
vector, called `text`. The size, 768, matches the model we use to turn notes
into numbers. Cosine is simply the way we compare those numbers for meaning.

`EdgeShard.create` makes the store in a local folder. There is no server or
account involved. Now ask, “where can I sit outside for a latte?” Nothing
comes back. The model is ready; the memory is empty.

---

## Beat 4: NOTEBOOK §2, the memories

Run the notes cell.

**NARRATION:**

These are ordinary notes from a day: a coffee shop, a meeting, a reminder,
an idea, an address, and a pair of shoes.

---

## Beat 5: NOTEBOOK §3, turn notes into vectors, on the device

Run the embed cell.

**NARRATION:**

To search by meaning, we turn each note into a vector: a list of 768 numbers
that represents the note. We run the text model on the device, once for each
note. From now on, a helper makes the same call so the notebook stays easy
to read. The work is unchanged: text in, vectors out.

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

Each note becomes a `Point`: an ID, its vector, and its original text with
other details. We write all 20 points, then call `optimize()` to build the
local search index.

---

## Beat 8: NOTEBOOK §5, ask again, now it remembers

Run the recall cell.

**NARRATION:**

Ask the same question again. This time, the coffee place on 5th comes back
first. The question and the note do not share the words “sit,” “outside,” or
“latte.” They match in meaning. The model did not change between the two
queries; the stored memories did.

---

## Beat 9: NOTEBOOK §6, local lookup at scale

Run the 5,000-memory build-up cell. Point at the median line, then at the
budget under the chart.

**NARRATION:**

What happens as the store grows? We add 5,000 filler memories on top of the
notes and time 200 searches. The histogram measures the lookup only, and on
this CPU-only machine the median stays well below a millisecond.

The lookup is not the whole answer, so we time the other half too. Turning
the question into a vector is the line under the chart, and it costs several
milliseconds against a fraction of one for the lookup. Read the two numbers
together: the encoder is the part you budget for, and the lookup barely
registers next to it. The total on the chart is a complete local answer in
under ten milliseconds, more than a hundred questions a second with no GPU
anywhere.

---

## Beat 10: NOTEBOOK §7, forget a memory

Run the delete cell, then the third-ask cell.

**NARRATION:**

Memory also needs deletion. We delete the coffee place by its ID, then build
the index again. Ask the same question a third time. A different café now
comes first. The before-and-after view shows that one note disappeared while
the others stayed put.

---

## Beat 11: WRAP

**NARRATION:**

You have now stored a note, found it by meaning, and deleted it on purpose.
The store is local files, so it survives a restart. Next, we add photos and
filters.
