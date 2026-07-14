# L3 — Multimodal Memory: Text and Photos — Script

**Target runtime:** ~6 min (≈ 365 sec)

NOTEBOOK beats reference the section numbers as they appear in the
executed `L3.ipynb`.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | From text memories to photos | 30 |
| 2 | NOTEBOOK §1 | Which model for which memory? (table) | 45 |
| 3 | SLIDE 1 | Two encoders, one shard | 30 |
| 4 | NOTEBOOK §2 | A single shard, two named vectors (visible EdgeConfig) | 40 |
| 5 | NOTEBOOK §3 | Store text notes (Nomic) | 25 |
| 6 | NOTEBOOK §4 | Store photos (CLIP): first point by hand, then batch | 35 |
| 7 | NOTEBOOK §5 | **The payoff:** find a photo by describing it | 50 |
| 8 | SLIDE 2 | Cross-modal recall | 30 |
| 9 | NOTEBOOK §6 | Your turn: describe a photo (editable) | 25 |
| 10 | NOTEBOOK §7 | Two spaces, shown side by side — never merged | 40 |
| 11 | WRAP | Wrap: summary, what's next | 40 |
| | | **Total** | **~390 (6.5 min)** |

---

## Beat 1 — INTRO

**NARRATION:**

In L2, we stored text notes. But your memory of a day isn't only words — half
of it is what you saw. So this lesson adds photos, without changing the
storage pattern. You'll use the right encoder for each kind of memory, then
find a photo by describing what is in it. Let's code!

---

## Beat 2 — NOTEBOOK §1: which model for which memory?

Scroll to "## 1." and its table (recreate or narrate over the markdown
table: text notes → Nomic → `text`; photos → CLIP → `image`; voice notes →
Whisper → transcript → Nomic → `text`).

**NARRATION:**

Different memory types use different vector spaces. Nomic and CLIP scores
are not comparable, so each modality has its own named vector and is
searched separately.

Text notes use Nomic-Embed-Text, in a vector called `text`. Photos use CLIP
ViT-B/32, in a vector called `image`. Voice notes, which you'll see in L5,
go through Whisper to a transcript, then Nomic — so they end up back in
that same `text` vector.

A text question actually gets embedded twice: once with Nomic, to search
`text`, once with CLIP, to search `image`. The results are shown per
modality, never blended into one score list.

---

## Beat 3 — SLIDE 1: two encoders, one shard

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

Picture it as one shard with two rows. Nomic takes in text and produces a
vector in the `text` row. CLIP takes in an image and produces a vector in
the `image` row. Same cylinder, same EdgeShard — two named vectors living
side by side.

---

## Beat 4 — NOTEBOOK §2: a single shard, two named vectors

Run the config cell.

**NARRATION:**

In L2 you wrote a one-vector `EdgeConfig` by hand. Here it is again, with
two named vectors instead of one: `text` at Nomic's size, `image` at CLIP's
size, both cosine. One `EdgeShard.create`, and the store holds both spaces.
Adding a modality means adding a named vector — the shard itself doesn't
change.

---

## Beat 5 — NOTEBOOK §3: store text notes (Nomic)

Run the add-text-notes cell.

**NARRATION:**

Text notes go in exactly like L2: embed with Nomic, add to the `text`
vector. The coffee-place note is back again — we're keeping it for a recall
in L5.

---

## Beat 6 — NOTEBOOK §4: store photos (CLIP)

Run the two photo cells: the first builds one point by hand, the second
batches the rest.

**NARRATION:**

Now the new part. First we build one photo point by hand — an id, the CLIP
vector under the `image` name, and a payload — so you can see a point is the
same shape whichever vector it uses. CLIP's vision encoder turns the photo
into a vector in a space it shares with text, which is what makes cross-modal
recall possible. Notice this point carries only an `image` vector, no `text`.
Then the rest of the photos go in one batch. Check the total: text notes plus
photos, all in one shard.

---

## Beat 7 — NOTEBOOK §5: The payoff — find a photo by describing it

Run the cross-modal query cell. Point at `show_photo_results` — the ranked
photos with scores. Name this as the payoff.

**NARRATION:**

Here's the payoff. No tags, no filenames. We take a plain text
description — "black and white sneakers" — embed it with CLIP's
text encoder, not Nomic, and search the `image` vector. Look at the
results: the sneakers photo comes back on top, ranked purely by how well
the words match the picture. That's retrieval by description, with zero
metadata written by hand.

---

## Beat 8 — SLIDE 2: cross-modal recall

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

## Beat 9 — NOTEBOOK §6: your turn — describe a photo

Run the editable cell.

**NARRATION:**

Now try it yourself. The default is `my_description = "a bowl of noodles"`.
Change it to anything in the photo set — a bicycle, a dog, or a train — and
re-run. The same CLIP text encoder embeds your words and searches the `image`
vector. There's a safe default, so the cell always returns something.

---

## Beat 10 — NOTEBOOK §7: two spaces, shown side by side

Run the dual-query cell and `memory_inbox`.

**NARRATION:**

One more useful pattern: send one query, "coffee," to both named vectors.
Nomic searches the text notes and CLIP searches the photos. We do not merge
the scores into one ranked list because they come from different vector
spaces. The memory inbox keeps the results grouped by modality.

---

## Beat 11 — WRAP

**NARRATION:**

The memory store didn't change at all here — same EdgeShard, same API.
Only the embedding models changed with the modality. Named vectors keep
text and image apart, cross-modal recall works because CLIP puts them in
one shared space, and we never merge scores across modalities.

Next lesson, L4 adds filters: "photos from last Tuesday near the office"
isn't similarity alone — it's similarity plus structure.
