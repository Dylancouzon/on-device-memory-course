# L3: Finding the Right Memory (script)

**Target runtime:** ~7 min

NOTEBOOK beats reference the section numbers as they appear in the
executed `Lesson3.ipynb`.

This lesson has two jobs: find a photo with a description, then narrow a
search with a filter. The notebook output carries most of the explanation;
three diagrams show the relationships that code alone cannot.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Endpoint teaser + from words to photos | 35 |
| 2 | SLIDE 1 | Two encoders, one shard | 35 |
| 3 | NOTEBOOK §1 | A single shard, two named vectors | 35 |
| 4 | NOTEBOOK §2 | Store text notes | 20 |
| 5 | NOTEBOOK §3 | Store a photo library | 35 |
| 6 | NOTEBOOK §4 | Find a photo by describing it | 55 |
| 7 | SLIDE 2 | Cross-modal recall | 30 |
| 8 | SLIDE 3 | Filters run inside the query | 30 |
| 9 | NOTEBOOK §5 | Recall with a filter | 60 |
| 10 | WRAP | What to carry into L4 | 35 |

Total: ~415 sec (~6.9 min).

---

## Beat 1: INTRO, endpoint teaser

```slide-brief
slug: l3-00-endpoint
purpose: the endpoint teaser, recolored from l2-00-endpoint. Same layout,
  same four nodes; "embed" and "recall" are the highlighted pair.
on-slide text: node labels only: "capture", "embed", "store", "recall",
  small tag "this lesson". No headline.
diagram spec (8:9, stack top-to-bottom):
  - Identical to l2-00-endpoint: four hand-drawn rounded nodes in a
    vertical loop, light-blue (#03A9F4) "capture", orange (#FF9800)
    "embed", violet (#6047FF) cylinder "store", red (#DC244C) "recall",
    curved arrows connecting them, the recall arrow curving back up
    toward capture.
  - Only the highlight moves: "embed" and "recall" get a solid stroke and
    full-strength fill; "capture" and "store" render at reduced opacity.
  - The "this lesson" tag points at the highlighted pair. Small
    spiral-notebook motif beside the cylinder.
```

**NARRATION:**

Today we focus on embedding and recall. L2 stored text notes. Now we add
photos using the same storage pattern, then narrow a search to food under
fifteen dollars. You can find a memory by describing it or by adding a rule.

---

## Beat 2: SLIDE 1, two encoders, one shard

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

Text and photos need different encoders. Text goes into `text`; photos go
into `image`. They live in the same shard, but their scores are on different
scales, so we search and show them separately.

---

## Beat 3: NOTEBOOK §1, a single shard, two named vectors

Run the config cell.

**NARRATION:**

This is the same `EdgeConfig` as L2, now with two named vectors: `text` for
Nomic and `image` for CLIP. One shard can hold both.

---

## Beat 4: NOTEBOOK §2, store text notes

Run the add-text-notes cell.

**NARRATION:**

Text notes work exactly as they did in L2: embed with Nomic, then add them
to the `text` vector. This lesson starts fresh, so it does not depend on an
earlier notebook run.

---

## Beat 5: NOTEBOOK §3, store a photo library

Run the photo cell.

**NARRATION:**

Photos follow the same pattern with a different encoder. CLIP turns each
photo into a vector under `image`. CLIP also puts text descriptions in that
same space, which is why a description can find a photo in the next cell.

---

## Beat 6: NOTEBOOK §4, find a photo by describing it

Run the cross-modal query cell, then change `my_description` and run it
again.

**NARRATION:**

Try a description. The starter is “a red bicycle.” We turn those words into
a CLIP vector and search the photo vectors, with no tags or filenames
needed. Try
the suggestions in the cell, then write your own. If the bank does not
contain what you describe, it still returns its closest photo, so look at
the image as well as the score.

---

## Beat 7: SLIDE 2, cross-modal recall

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

The text goes through CLIP’s text encoder, not Nomic, and lands in the same
space as the photos. One shared space lets words retrieve images.

---

## Beat 8: SLIDE 3, filters run inside the query

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

Similarity finds related memories. A filter applies a rule, such as “food
under $15.” It runs with the search inside the shard, rather than afterward
in your code.

---

## Beat 9: NOTEBOOK §5, recall with a filter

Run the index cell, the cell that defines `search`, then the filter cell.
The filter is written out in full, no helper.

**NARRATION:**

First index `category` and `price`. Then search for “somewhere to eat” and
keep only food records priced below 15. Compare the two lists. A record
without a price cannot meet the price rule, so it drops out too.

---

## Beat 10: WRAP

**NARRATION:**

You now have two ways to narrow memory: describe the photo you want, or add
a clear rule to the search. Next, L4 brings photos, voice notes, and text
into one assistant.
