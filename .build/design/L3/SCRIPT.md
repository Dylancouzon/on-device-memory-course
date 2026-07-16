# L3: Finding the Right Memory (script)

**Target runtime:** ~7 min

NOTEBOOK beats reference the section numbers as they appear in the
executed `L3.ipynb`.

Two ways to find the right memory in one lesson: describe what you mean
(cross-modal recall over a photo bank), and constrain what comes back (a
payload filter riding inside the query). Filters are taught once, in §5; L6
brings the same idea back on the robot. Slides: the endpoint teaser,
two encoders one shard, cross-modal recall, the shared space seen, and
filters inside the query.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Endpoint teaser + from words to photos | 35 |
| 2 | SLIDE 1 | The memory loop, this lesson's piece highlighted | 15 |
| 3 | SLIDE 2 | Two encoders, one shard | 35 |
| 4 | NOTEBOOK §1 | A single shard, two named vectors (visible EdgeConfig) | 35 |
| 5 | NOTEBOOK §2 | Store text notes (Nomic) | 20 |
| 6 | NOTEBOOK §3 | Store a photo library (CLIP), one batch | 35 |
| 7 | NOTEBOOK §4 | Find a photo by describing it (type anything, bank) | 55 |
| 8 | SLIDE 3 | Cross-modal recall | 30 |
| 9 | SLIDE 4 | One shared space, seen (the bank as a 2-D map) | 30 |
| 10 | SLIDE 5 | Filters run inside the query, not after it | 30 |
| 11 | NOTEBOOK §5 | Recall with a filter (index + food under $15) | 60 |
| 12 | WRAP | Two ways to find the right memory; L4 hands you the recall | 35 |

Total: ~415 sec (~6.9 min).

---

## Beat 1: INTRO

**NARRATION:**

In L2, we stored text notes. But your memory of a day isn't only words.
Half of it is what you saw. So this lesson adds photos, without changing
the storage pattern, and then narrows recall down: not just "something
about food", but food, under fifteen dollars. Two ways to find the right
memory: describe it, or constrain it. Let's code!

---

## Beat 2: SLIDE 1, the memory loop, this lesson highlighted

```slide-brief
slug: l3-00-endpoint
purpose: the endpoint teaser. The same loop diagram as L2's teaser,
  with the embed and recall stages highlighted for this lesson.
on-slide text: node labels only: "capture", "embed", "store", "recall",
  small tag "this lesson". No headline.
diagram spec (8:9): identical layout to slide l2-00-endpoint; the
  highlight moves to "embed" (a second encoder joins) and "recall"
  (described and filtered). Other nodes at reduced opacity.
```

**NARRATION:**

Same loop as last time. Today the highlight moves: a second encoder joins
at the embed stage, and recall learns two new tricks.

---

## Beat 3: SLIDE 2, two encoders, one shard

```slide-brief
slug: two-encoders-one-shard
purpose: show Nomic and CLIP as two separate encoders feeding two named
  rows inside a single EdgeShard.
on-slide text: node labels only: "Nomic-Embed-Text", "CLIP ViT-B/32",
  cylinder "EdgeShard" with rows "text" and "image". No headline.
diagram spec (8:9, stack top-to-bottom):
  - Top: orange (#FF9800) rounded node, document/text icon, label
    "Nomic-Embed-Text", curved arrow down, labeled "768-d", into a violet
    (#6047FF) cylinder's top labeled row "text" (small vector-cell strip
    icon in the row).
  - Middle: the same violet cylinder continues, second labeled row "image"
    just below the first, same cylinder body (this is ONE cylinder with two
    rows, not two cylinders).
  - Bottom: orange (#FF9800) rounded node, photo/image icon, label
    "CLIP ViT-B/32", curved arrow up or down (whichever reads cleanly)
    into that same cylinder's "image" row, labeled "512-d".
  - Cylinder hand-lettered title above it: "EdgeShard".
```

**NARRATION:**

Different memory types use different vector spaces. Text notes use
Nomic-Embed-Text, in a vector called `text`. Photos use CLIP, in a vector
called `image`. Nomic and CLIP scores are not comparable, so each modality
has its own named vector, is searched on its own, and the results are never
blended into one score list. Picture it as one shard with two rows: same
cylinder, two named vectors living side by side.

---

## Beat 4: NOTEBOOK §1, a single shard, two named vectors

Run the config cell.

**NARRATION:**

In L2 you wrote a one-vector `EdgeConfig` by hand. Here it is again, with
two named vectors instead of one: `text` at Nomic's size, `image` at CLIP's
size, both cosine. One `EdgeShard.create`, and the store holds both spaces.
Adding a modality means adding a named vector. The shard itself doesn't
change.

---

## Beat 5: NOTEBOOK §2, store text notes

Run the add-text-notes cell.

**NARRATION:**

Text notes go in exactly like L2: embed with Nomic, add to the `text`
vector. The coffee-place note is back. Every lesson builds its own store,
so nothing depends on what you ran before.

---

## Beat 6: NOTEBOOK §3, store a photo library

Run the photo cell.

**NARRATION:**

Now the new part: photos. Same store pattern as the notes, but a different
encoder. We load CLIP's vision model and call `embed` ourselves, exactly as
L2 did with Nomic. Each photo becomes a 512-dimensional vector under the
`image` name, not `text`. CLIP places words and pictures in one shared
space, which is what makes the next cell's cross-modal recall possible. Each
photo point carries only its `image` vector; the two named vectors live side
by side in the shard, each searched on its own. This time it's a bank of
everyday photos, not just a handful, so you can describe almost anything and
see the closest one, all embedded in one batch. Check the total: text notes
plus the photo bank, all in one shard.

---

## Beat 7: NOTEBOOK §4, find a photo by describing it

Run the cross-modal query cell, then change `my_description` and run it
again.

**NARRATION:**

Now find a photo by describing it, and this cell is yours to drive. No
tags, no filenames. It starts on "a red bicycle": we embed that text with
CLIP's text encoder, not Nomic, and search the `image` vector. The bicycle
photo comes back on top, ranked purely by how well the words match the
picture. Retrieval by description, with zero metadata written by hand.
Start with the suggestions in the cell, a slice of pizza, a puppy, a
sunflower, a sailboat; they're checked against this bank. Then type your
own description and re-run, and read the score when you do: if what you
describe isn't really in the bank, the closest photo still comes back,
just with a lower number. That number tells you how good the match is.
This bank is an example set, not the whole world, so you'll see
near-misses; that's cross-modal similarity showing its work.

---

## Beat 8: SLIDE 3, cross-modal recall

```slide-brief
slug: cross-modal-recall
purpose: show a text query embedded by CLIP's text tower landing directly
  in image vector space, retrieving a photo.
on-slide text: labels in the diagram only: the query text, "CLIP text
  tower", the highlighted "image" row, "bicycle.jpg". No headline.
diagram spec (8:9, stack top-to-bottom):
  - Top: light-blue (#03A9F4) node, speech-bubble icon, label
    "\"a red bicycle\"".
  - Curved arrow (Qdrant Red #DC244C) down into an orange (#FF9800) node
    labeled "CLIP text tower".
  - Same red arrow continues down into a violet (#6047FF) cylinder, landing
    specifically in a highlighted "image" row (draw this row with a red
    outline accent to show it's the one being hit).
  - Arrow continues out of the cylinder to a teal (#009688) node, photo
    icon, label "bicycle.jpg" with a small checkmark.
  - Label the long red arrow path once, small: "text query → image space".
```

**NARRATION:**

This is what makes that work. A text query goes through CLIP's text tower,
not Nomic's, and lands directly in image space, the same coordinate
system CLIP used to place the photos. That's the whole trick: one shared
space, two doors in.

---

## Beat 9: SLIDE 4, one shared space, seen

```slide-brief
slug: one-shared-space-map
purpose: show the actual photo bank as one 2-D map of CLIP space, with a
  text description dropped in beside its nearest photo, so "one shared
  space" is evidence, not just a diagram.
on-slide text: legend labels only: "photos in the bank", "your
  description", "best match". Small footnote: "flattened to 2-D for
  viewing; ranking happens in the full space". No headline.
diagram spec (8:9): a scatter of ~165 small grey-violet dots (the bank's
  image vectors, PCA to two axes). One Qdrant-red star labeled
  "\"a red bicycle\"" for the text query, projected into the same plane.
  One teal dot labeled "bicycle.jpg" for the nearest photo, joined to the
  star by a short dashed red line. Axes hidden. Rendered from the real
  bank vectors (PCA of the CLIP image vectors; the query embedded with
  CLIP's text tower).
```

**NARRATION:**

Don't take the last slide's word for it. Here's the space itself. Every
photo in the bank laid out on one map, and a text description dropped in as
the star. The dashed line points to the nearest photo, the match the search
found. Change the description and the star moves, and the match moves with
it. Words and pictures on one map: that's the whole reason describing works.
One caveat on the chart: this view flattens the vectors to two axes so we
can look at them, so spacing here is approximate. The search itself always
ranks in the full space.

---

## Beat 10: SLIDE 5, filters run inside the query

```slide-brief
slug: filters-inside-query
purpose: show that a filter runs inside the same query as the vector
  search, not as a second pass afterward.
on-slide text: gate and node labels only: "filter (indexed field)",
  "one pass", crossed-out "filter in your code / second pass".
  No headline.
diagram spec (8:9, stack top-to-bottom):
  - Top: a single red curved arrow labeled "query" entering from above.
  - Center: a violet hand-drawn cylinder (EdgeShard), dashed-border
    container labeled "shard". Embedded near the top of the cylinder: a
    small teal rounded-rectangle "gate" node with a funnel/filter icon,
    labeled "filter (indexed field)". The red query arrow passes visibly
    THROUGH this teal gate before continuing down into the cylinder body,
    which shows a few small result rows highlighted teal.
  - Arrow label at the gate: "one pass".
  - Below the cylinder, a separate smaller panel showing the crossed-out
    alternative: a gray dashed cylinder labeled "all results" (desaturated
    gray #4E5366, no fill), a gray arrow to a second gray box labeled
    "filter in your code" with a hand-drawn ✕ struck through the whole
    panel, small label "second pass".
  - Include the small spiral-notebook motif icon near the shard, tiny,
    non-dominant.
```

**NARRATION:**

Similarity finds what you mean; it can't enforce what you need. "Somewhere
to eat" is meaning; "under fifteen dollars" is structure. The filter
passes through the query on its way into the shard, so filtering and
vector search happen in one pass. The alternative is to retrieve a large
set of results and filter them later in your own code: more work, and a
separate step to maintain.

---

## Beat 11: NOTEBOOK §5, recall with a filter

Run the index cell, the cell that defines `search`, then the filter cell.
The filter is written out in full, no helper.

**NARRATION:**

First, index the two fields we'll filter on: category as a keyword, price
as a float. Indexing is what makes the filter efficient. The engine
narrows candidates through the index instead of scanning every point. Then
the recall itself: "somewhere to eat under fifteen dollars" is really two
explicit pieces. A semantic search for "somewhere to eat", narrowed by a
`Filter` with two conditions: category equals food, price below fifteen.
Raw `FieldCondition`, `MatchValue`, and `RangeFloat` types, dropped
straight into the `QueryRequest` next to the vector query. There's no
hidden natural-language-to-filter translation. The first list shows what
similarity alone returns; below it, what's left once the filter runs
alongside it.

---

## Beat 12: WRAP

**NARRATION:**

Two ways to find the right memory, one store. Describing works because
CLIP puts words and pictures in one shared space; constraining works
because the payload filter rides inside the same on-device query. And
that's the whole filter vocabulary you need: a keyword match, a numeric
range, combined with `must`. Next, in L4, we put the whole day together,
photos, voice notes, and text notes in a single assistant, and the
recall becomes yours to drive.
