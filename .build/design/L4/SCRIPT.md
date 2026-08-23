# L4: Finding the Right Memory (script)

**Target runtime:** ~7 min

Talking points, not narration. Each beat lists what to hit; wording is yours on the day.

NOTEBOOK beats reference the section numbers as they appear in the executed `Lesson4.ipynb`. Slide briefs live in `SLIDES.md` in this directory; beats name only the slug.

Two jobs: find a photo with a description, then narrow a search with a filter. The notebook output carries most of the explanation; three diagrams show the relationships code alone cannot.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO + SLIDE `l4-00-endpoint` | Endpoint teaser + from words to photos | 35 |
| 2 | SLIDE `two-encoders-one-shard` | Two encoders, one shard | 35 |
| 3 | NOTEBOOK §1 | A single shard, two named vectors | 35 |
| 4 | NOTEBOOK §2 | Store text notes | 20 |
| 5 | NOTEBOOK §3 | Store a photo library | 35 |
| 6 | NOTEBOOK §4 | Find a photo by describing it | 55 |
| 7 | SLIDE `cross-modal-recall` | Cross-modal recall | 30 |
| 8 | SLIDE `filters-inside-query` | Filters run inside the query | 30 |
| 9 | NOTEBOOK §5 | Recall with a filter | 60 |
| 10 | WRAP | What to carry into L5 | 35 |

Total: ~415 sec (~6.9 min).

---

## Beat 1: INTRO, SLIDE `l4-00-endpoint`

- This lesson's stages on the loop: embed and recall.
- L3 stored text notes. Now photos join, same storage pattern.
- Two ways to narrow memory today: describe what you saw, or add a rule.

## Beat 2: SLIDE `two-encoders-one-shard`

- Text and photos need different encoders: Nomic for text, CLIP for images.
- Text goes into the `text` vector, photos into `image`, both in one shard.
- Their scores sit on different scales, so we search and show them separately.

## Beat 3: NOTEBOOK §1, a single shard, two named vectors

Run the config cell.

- Same `EdgeConfig` as L3, now with two named vectors: `text` at 768, `image` at 512.
- One shard holds both.

## Beat 4: NOTEBOOK §2, store text notes

Run the add-text-notes cell.

- Text notes work exactly as in L3: embed with Nomic, store under `text`. Twenty notes.
- The lesson starts fresh, so it does not depend on an earlier notebook run.

## Beat 5: NOTEBOOK §3, store a photo library

Run the photo cell.

- Same pattern, different encoder: 165 everyday photos into the `image` vector, 185 memories in the shard.
- CLIP also places text descriptions in that same space, which is what the next cell uses.

## Beat 6: NOTEBOOK §4, find a photo by describing it

Run the cross-modal query cell, then change `my_description` and run it again.

- Starter description: "a red bicycle". Those words become a CLIP vector and search the photo vectors.
- No tags, no filenames, no captions involved.
- Try the suggestions in the cell, then write your own.
- One photo comes back, large, with its score. If the bank holds nothing like your description, that is still its closest photo, so read the image alongside the score.
- Name the range: CLIP text-to-image scores here run roughly 0.19 to 0.33, and a score only ranks one description against this bank.

## Beat 7: SLIDE `cross-modal-recall`

- The description goes through CLIP's text encoder, not Nomic.
- It lands in the same space as the photos, which is what lets words retrieve images.

## Beat 8: SLIDE `filters-inside-query`

- Similarity finds related memories. A filter applies a rule, such as food under $15.
- The filter runs with the search inside the shard, in one pass, rather than afterward in your code.

## Beat 9: NOTEBOOK §5, recall with a filter

Run the index cell, the similarity-only cell, then the filter cell. The filter is written out in full; the query it narrows runs through the `text_search` helper.

- Index `category` and `price` first: a filter needs an index on the field.
- Same question twice: "somewhere to eat", then narrowed to food under $15.
- Every row prints `category · price`, so each drop is explained on screen.
- Espresso bar at $3 and the bakery at $4 pass. The coffee place and the ramen note carry no price, so they cannot meet a price rule and drop out too.

## Beat 10: WRAP

- Two ways to narrow memory: describe the photo you want, or add a clear rule.
- Next: photos, voice notes, and text notes together in one assistant.
