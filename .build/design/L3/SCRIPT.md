# L3 — Finding the Right Memory — script

**Target runtime:** ~8 min

NOTEBOOK beats reference the section numbers as they appear in the
executed `L3.ipynb`.

Two ways to find the right memory in one lesson: describe what you mean
(cross-modal recall over photos), and constrain what comes back (a payload
filter riding inside the query). Slides: the endpoint teaser, two encoders
one shard, cross-modal recall, and filters inside the query.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Endpoint teaser + from words to photos | 35 |
| 2 | SLIDE 1 | The memory loop, this lesson's piece highlighted | 15 |
| 3 | SLIDE 2 | Two encoders, one shard | 35 |
| 4 | NOTEBOOK §1 | A single shard, two named vectors (visible EdgeConfig) | 35 |
| 5 | NOTEBOOK §2 | Store text notes (Nomic) | 20 |
| 6 | NOTEBOOK §3 | Store photos (CLIP): first point by hand, then batch | 35 |
| 7 | NOTEBOOK §4 | **The payoff:** find a photo by describing it | 50 |
| 8 | SLIDE 3 | Cross-modal recall | 30 |
| 9 | NOTEBOOK §5 | The photos on hand (gallery, seen before describing) | 20 |
| 10 | NOTEBOOK §6 | Your turn: describe a photo (editable) | 25 |
| 11 | SLIDE 4 | Filters run inside the query, not after it | 30 |
| 12 | NOTEBOOK §7 | **The payoff:** recall with a filter (index + food under $15) | 60 |
| 13 | NOTEBOOK §8 | Your turn: filter weeks of history (editable) | 40 |
| 14 | WRAP | Two ways to find the right memory; reference table pointer | 35 |

Total: ~465 sec (~7.8 min).

---

## Beat 1 — INTRO

**NARRATION:**

In L2, we stored text notes. But your memory of a day isn't only words —
half of it is what you saw. So this lesson adds photos, without changing
the storage pattern, and then narrows recall down: not just "something
about food", but food, under fifteen dollars. Two ways to find the right
memory: describe it, or constrain it. Let's code!

---

## Beat 2 — SLIDE 1: the memory loop, this lesson highlighted

```slide-brief
slug: l3-00-endpoint
purpose: the endpoint teaser — the same loop diagram as L2's teaser,
  with the embed and recall stages highlighted for this lesson.
on-slide text: node labels only — "capture", "embed", "store", "recall",
  small tag "this lesson". No headline.
diagram spec (8:9): identical layout to slide l2-00-endpoint; the
  highlight moves to "embed" (a second encoder joins) and "recall"
  (described and filtered). Other nodes at reduced opacity.
```

**NARRATION:**

Same loop as last time. Today the highlight moves: a second encoder joins
at the embed stage, and recall learns two new tricks.

---

## Beat 3 — SLIDE 2: two encoders, one shard

```slide-brief
slug: two-encoders-one-shard
purpose: show Nomic and CLIP as two separate encoders feeding two named
  rows inside a single EdgeShard.
on-slide text: node labels only — "Nomic-Embed-Text", "CLIP ViT-B/32",
  cylinder "EdgeShard" with rows "text" and "image". No headline.
diagram spec (8:9, stack top-to-bottom):
  - Top: orange (#FF9800) rounded node, document/text icon, label
    "Nomic-Embed-Text" — curved arrow down, labeled "768-d", into a violet
    (#6047FF) cylinder's top labeled row "text" (small vector-cell strip
    icon in the row).
  - Middle: the same violet cylinder continues — second labeled row "image"
    just below the first, same cylinder body (this is ONE cylinder with two
    rows, not two cylinders).
  - Bottom: orange (#FF9800) rounded node, photo/image icon, label
    "CLIP ViT-B/32" — curved arrow up or down (whichever reads cleanly)
    into that same cylinder's "image" row, labeled "512-d".
  - Cylinder hand-lettered title above it: "EdgeShard".
```

**NARRATION:**

Different memory types use different vector spaces. Text notes use
Nomic-Embed-Text, in a vector called `text`. Photos use CLIP, in a vector
called `image`. Nomic and CLIP scores are not comparable, so each modality
has its own named vector, is searched on its own, and the results are never
blended into one score list. Picture it as one shard with two rows — same
cylinder, two named vectors living side by side.

---

## Beat 4 — NOTEBOOK §1: a single shard, two named vectors

Run the config cell.

**NARRATION:**

In L2 you wrote a one-vector `EdgeConfig` by hand. Here it is again, with
two named vectors instead of one: `text` at Nomic's size, `image` at CLIP's
size, both cosine. One `EdgeShard.create`, and the store holds both spaces.
Adding a modality means adding a named vector — the shard itself doesn't
change.

---

## Beat 5 — NOTEBOOK §2: store text notes

Run the add-text-notes cell.

**NARRATION:**

Text notes go in exactly like L2: embed with Nomic, add to the `text`
vector. The coffee-place note is back — every lesson builds its own store,
so nothing depends on what you ran before.

---

## Beat 6 — NOTEBOOK §3: store photos

Run the two photo cells: the first builds one point by hand, the second
batches the rest.

**NARRATION:**

Now the new part. First we build one photo point by hand — an id, the CLIP
vector under the `image` name, and a payload — so you can see a point is the
same shape whichever vector it uses. CLIP's vision encoder turns the photo
into a vector in a space it shares with text, which is what makes
cross-modal recall possible. Notice this point carries only an `image`
vector, no `text`. Then the rest of the photos go in one batch. Check the
total: text notes plus photos, all in one shard.

---

## Beat 7 — NOTEBOOK §4: The payoff — find a photo by describing it

Run the cross-modal query cell. Point at `show_photo_results` — the ranked
photos with scores. Name this as the payoff.

**NARRATION:**

Here's the first payoff. No tags, no filenames. We take a plain text
description — "black and white sneakers" — embed it with CLIP's
text encoder, not Nomic, and search the `image` vector. Look at the
results: the sneakers photo comes back on top, ranked purely by how well
the words match the picture. That's retrieval by description, with zero
metadata written by hand.

---

## Beat 8 — SLIDE 3: cross-modal recall

```slide-brief
slug: cross-modal-recall
purpose: show a text query embedded by CLIP's text tower landing directly
  in image vector space, retrieving a photo.
on-slide text: labels in the diagram only — the query text, "CLIP text
  tower", the highlighted "image" row, "sneakers.jpg". No headline.
diagram spec (8:9, stack top-to-bottom):
  - Top: light-blue (#03A9F4) node, speech-bubble icon, label
    "\"black and white sneakers\"".
  - Curved arrow (Qdrant Red #DC244C) down into an orange (#FF9800) node
    labeled "CLIP text tower".
  - Same red arrow continues down into a violet (#6047FF) cylinder, landing
    specifically in a highlighted "image" row (draw this row with a red
    outline accent to show it's the one being hit).
  - Arrow continues out of the cylinder to a teal (#009688) node, photo
    icon, label "sneakers.jpg" with a small checkmark.
  - Label the long red arrow path once, small: "text query → image space".
```

**NARRATION:**

This is what makes that work. A text query goes through CLIP's text tower,
not Nomic's, and lands directly in image space — the same coordinate
system CLIP used to place the photos. That's the whole trick: one shared
space, two doors in.

---

## Beat 9 — NOTEBOOK §5: the photos on hand

Run the gallery cell.

**NARRATION:**

Before you describe a photo, here are the ones now in the store — all
seventeen, laid out so you're choosing from photos you've actually seen.
Pick one that catches your eye; you'll describe it in the next cell.

---

## Beat 10 — NOTEBOOK §6: your turn — describe a photo

Run the editable cell.

**NARRATION:**

Now try it yourself. The default is `my_description = "a bowl of noodles"`.
Change it to anything in the photo set — a bicycle, a dog, or a train — and
re-run. The same CLIP text encoder embeds your words and searches the
`image` vector. There's a safe default, so the cell always returns
something.

---

## Beat 11 — SLIDE 4: filters run inside the query

```slide-brief
slug: filters-inside-query
purpose: show that a filter runs inside the same query as the vector
  search, not as a second pass afterward.
on-slide text: gate and node labels only — "filter (indexed field)",
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
set of results and filter them later in your own code — more work, and a
separate step to maintain.

---

## Beat 12 — NOTEBOOK §7: The payoff — recall with a filter

Run the index cell, then the filter cell. The filter is written out in
full — no helper.

**NARRATION:**

First, index the payload fields we'll filter on: category and location as
keywords, timestamp and price as floats. Indexing is what makes the filter
efficient — the engine narrows candidates through the index instead of
scanning every point. Then the payoff: the honest form of "somewhere to
eat under fifteen dollars" is two explicit pieces. A semantic search for
"somewhere to eat", narrowed by a `Filter` with two conditions: category
equals food, price below fifteen — raw `FieldCondition`, `MatchValue`, and
`RangeFloat` types, dropped straight into the `QueryRequest` next to the
vector query. There's no hidden natural-language-to-filter translation.
The first list shows what similarity alone returns; below it, what's left
once the filter runs alongside it.

---

## Beat 13 — NOTEBOOK §8: your turn — filter weeks of history

Run the load-history cell, then the editable cell.

**NARRATION:**

A real assistant carries weeks of notes, not a single day. So we load a
few weeks of earlier notes into the same shard — about a hundred more,
each already carrying the same category, timestamp, and price fields. Now
your turn. Change `my_category`, re-run, and the cell builds the filter
directly from your value. Try food, travel, shopping, home, or health, and
watch the list change — now across weeks of memory, not just today. A safe
default is set, so the cell always returns something.

---

## Beat 14 — WRAP

**NARRATION:**

Two ways to find the right memory, one store. Describing works because
CLIP puts words and pictures in one shared space; constraining works
because the payload filter rides inside the same on-device query. The
reference table at the bottom of the notebook has the whole filter
vocabulary you'll need — keyword matches and numeric ranges, combined with
`must` for AND and `should` for OR. Next, in L4, we put the whole day
together — photos, voice notes, and text notes, in a single assistant.
