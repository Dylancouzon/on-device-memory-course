# L3: Store and Recall (script)

**Target runtime:** ~7 min

Talking points, not narration. Each beat lists what to hit; wording is yours on the day.

NOTEBOOK beats reference the section numbers as they appear in the executed `Lesson3.ipynb`. Slide briefs live in `SLIDES.md` in this directory; beats name only the slug.

One question threads the lesson: "where can I sit outside for a latte?" It is asked three times: of the empty store, after storing, and after forgetting.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | What you'll build + the one question, three times | 25 |
| 2 | SLIDE `l3-00-endpoint` | The memory loop, store and recall highlighted | 20 |
| 3 | NOTEBOOK §1 | Build the store, then ask the empty shard: nothing back | 55 |
| 4 | NOTEBOOK §2 | The memories, a day's notes | 25 |
| 5 | NOTEBOOK §3 | Embed the notes locally, shown in the open | 40 |
| 6 | SLIDE `anatomy-of-a-point` | Anatomy of a point | 30 |
| 7 | NOTEBOOK §4 | Store the memories (Point, upsert, optimize) | 35 |
| 8 | NOTEBOOK §5 | Ask again, now it remembers (second ask) | 40 |
| 9 | NOTEBOOK §6 | Local lookup at 5,020 memories, and the real budget | 55 |
| 10 | NOTEBOOK §7 | Forget a memory (third ask) | 55 |
| 11 | WRAP | The lifecycle, persistence, what's next | 40 |

Total: ~405 sec (~6.75 min).

---

## Beat 1: INTRO

- A simple store for personal notes, built from nothing.
- L1 showed this question already answered: "where can I sit outside for a latte?"
- The same question three times: before storing, after storing, after deleting a result.

## Beat 2: SLIDE `l3-00-endpoint`

- The loop behind the whole course: capture, embed, store, recall.
- This lesson owns storing, finding, and deleting.

## Beat 3: NOTEBOOK §1, ask before there's anything to remember

Run the setup cell, then the cold-open query cell.

- `EdgeConfig`: one kind of vector, named `text`, size 768 because that is the model's output.
- Cosine is how we compare those numbers for meaning.
- `EdgeShard.create` makes the store in a local folder. No server, no account.
- Ask the question: 0 memories found. The model is ready, the memory is empty.

## Beat 4: NOTEBOOK §2, the memories

Run the notes cell.

- Twenty ordinary notes from a day: coffee place, standup, dry cleaning, an idea, Mum's address, running shoes.

## Beat 5: NOTEBOOK §3, turn notes into vectors, on the device

Run the embed cell.

- Each note becomes 768 numbers that represent its meaning.
- One helper call, text model running on the device, once per note. Every lesson embeds through this same call.
- Text in, vectors out.

## Beat 6: SLIDE `anatomy-of-a-point`

- A point is three things: an id, a named vector, and a payload.
- The payload carries the original text plus any fields you want along with it.
- That is the whole shape of a memory in the store.

## Beat 7: NOTEBOOK §4, store the memories

Run the Point / upsert_points / optimize cell.

- One `Point` per note: id, vector, payload.
- All 20 points written, then `optimize()` builds the local index. Edge has no background optimizer, so you call it.

## Beat 8: NOTEBOOK §5, ask again, now it remembers

Run the recall cell.

- Same question, same call: the coffee place on 5th comes back first at 0.653.
- Question and note share none of the words "sit", "outside", or "latte". They match in meaning.
- The model did not change between the two asks; the stored memories did.
- Name the range: text-to-text scores here run roughly 0.45 to 0.80.

## Beat 9: NOTEBOOK §6, local lookup at scale

Run the 5,000-memory build-up cell. Point at the median line, then at the budget under the chart.

- 5,000 filler memories on top of the notes, 5,020 total, 200 timed searches.
- The histogram times the lookup only, and the median stays well under a millisecond on a CPU-only machine.
- The line under the chart is the other half: turning the question into a vector costs several milliseconds.
- Read them together: the encoder is what you budget for, the lookup barely registers.
- A complete local answer in under ten milliseconds, more than a hundred questions a second, no GPU.
- This is the only latency number in the course.

## Beat 10: NOTEBOOK §7, forget a memory

Run the delete cell, then the third-ask cell.

- Delete the coffee place by its id, then build the index again.
- Third ask: a different café comes first, the quiet cafe at 0.590.
- The before-and-after view shows one note gone and the others at unchanged scores: exactly what you deleted, not every trace.

## Beat 11: WRAP

- You stored a note, found it by meaning, and deleted it on purpose.
- The store is local files, so it survives a restart.
- Next: photos and filters.
