# L5 — Lab: Your Smartphone Assistant — script

**Target runtime:** ~12 min

This lab is built to be student-driven: they see the store, the point, and
the recall built in the open, then ask their own question and add their own
memory. No slides — the notebook and its live output carry the whole lesson.

---

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Bring a day's memories together | 30 |
| 2 | NOTEBOOK §1 | A day's captures — photos, voice note, text notes | 45 |
| 3 | NOTEBOOK §2 | The day at a glance (timeline, for inspection) | 40 |
| 4 | NOTEBOOK §3 | One shard, two named vectors + indexed fields | 40 |
| 5 | NOTEBOOK §4 | Store the day: one text + one photo by hand, then batch | 55 |
| 6 | NOTEBOOK §5 | Inspect a stored point | 35 |
| 7 | NOTEBOOK §6 | How recall works (QueryRequest for both spaces) | 55 |
| 8 | NOTEBOOK §7 | **The payoff:** sneakers under $50 (raw hits, then inbox) | 55 |
| 9 | NOTEBOOK §8 | Your turn: ask a question | 45 |
| 10 | NOTEBOOK §9 | **The payoff:** add your own memory, then recall it | 60 |
| 11 | NOTEBOOK §10 | **The payoff:** forget a memory (delete by id, re-recall) | 40 |
| 12 | NOTEBOOK §11 | Persistence: reopen and recall, offline | 45 |
| 13 | WRAP | Wrap-up + pointer to L6 | 40 |

Total: ~585 sec (~10 min narration; ~12–13 min with the two editable cells
run live). No slides, down from three: the architecture is L3's, and the
query and results read more clearly as code and live output than as a diagram.

---

## Beat 1 — INTRO

**NARRATION**

This lab brings together everything you've built so far. You'll store photos,
a voice note, and text notes from one day in a single on-device shard, then
ask it your own questions and add your own memories — all offline. Let's
build something.

---

## Beat 2 — NOTEBOOK §1. A day's captures

Run the captures cell.

**NARRATION**

> A day starts with 17 photos, five voice notes, and 20 text notes: 42 captures in all. Each capture carries the same metadata: source type, timestamp, location, category, price when relevant, and store. The voice notes arrive as audio, so a small Whisper model transcribes them on-device — the kind of speech-to-text a phone runs, no server and no account. From there Nomic embeds the transcript exactly like any other text. Three source types, two embedding paths.

---

## Beat 3 — NOTEBOOK §2. The day at a glance

Run `day_timeline`.

**NARRATION**

> Before asking anything, here's the raw material laid flat: photos in the upper lane as thumbnails, in the order they were taken, and the voice and text notes below as numbered markers. This is what a day of on-device capture looks like — nothing recalled yet, just what's there. It's for orientation, not a result.

---

## Beat 4 — NOTEBOOK §3. One shard, two named vectors

Run the shard-and-index cell.

**NARRATION**

> One shard holds the whole day, with the two named vectors from L3: `text` for Nomic, `image` for CLIP. Then we index the four payload fields we'll filter on — category and location as keywords, timestamp and price as floats. That index is what lets the filters in a few cells' time run inside the query.

---

## Beat 5 — NOTEBOOK §4. Store the day

Run the two cells: the first stores one text note and one photo by hand, the
second batches the rest.

**NARRATION**

> Store the day in two steps. First, one of each by hand — a text note embedded with Nomic under the `text` vector, and one photo embedded with CLIP under the `image` vector — so you can see a memory is the same `Point` whichever modality it came from. Then the rest go in two batches, text and image. Check the total: 42 memories, one shard.

---

## Beat 6 — NOTEBOOK §5. Inspect a stored point

Run the scroll cell.

**NARRATION**

> Pull one point back out and look at it. Its id, the named vectors it actually carries — this one is a text note, so only `text` — and its full payload. A photo point would show `image` instead. This is the raw shape everything else in the lab searches over.

---

## Beat 7 — NOTEBOOK §6. How recall works

Run the cell that defines `recall` and `show_raw`.

**NARRATION**

> Now build recall in the open. It embeds the question twice — Nomic for the `text` vector, CLIP for the `image` vector — and runs one `QueryRequest` against each, with the same filter. The two result lists stay separate, grouped as photos, voice notes, and text notes, because Nomic and CLIP scores are not on the same scale. `show_raw` prints the plain evidence — which space, the score, the id, the payload — so you always see the hits before any rendering.

---

## Beat 8 — NOTEBOOK §7. The payoff: sneakers under $50

Run the cell. Raw hits print first, then the memory inbox renders.

**NARRATION**

> First payoff: "black and white sneakers under fifty dollars." The filter is spelled out in code: `Filter(must=[...])` with category equal to `shopping` and price below 50, using raw `FieldCondition`, `MatchValue`, and `RangeFloat` types. Look at `show_raw` first: the space searched, the score, the id, the payload, in plain text. Then the same hits rendered as the memory inbox. The evidence comes before the presentation, never the other way round.

---

## Beat 9 — NOTEBOOK §8. Your turn: ask a question

Run the editable cell, then change it and run again.

**NARRATION**

> Your turn. The cell lists a handful of questions the day can answer — where you parked the bike, the gym locker code, when the dentist is — so you can start from one that lands. Change `my_question` to any of them or to your own, and set `my_category` to filter, or `None` to search everything. Re-run, and you get the same raw hits and the same inbox for your question.

---

## Beat 10 — NOTEBOOK §9. The payoff: add your own memory, then recall it

Run the editable cell.

**NARRATION**

> The second payoff, and the one that makes it yours: add a memory. Change `my_note` and its metadata, embed it, build a `Point`, and upsert it into the same shard. Then recall it right away. The memory you just wrote comes back at the top — the store didn't need a rebuild or a restart to know something new. That's the whole promise of on-device memory: it grows as you use it.

---

## Beat 11 — NOTEBOOK §10. The payoff: forget a memory

Run the delete cell.

**NARRATION**

> Growing is only half of memory — the other half is forgetting. Wrong notes, stale ones, anything you no longer want: you delete it by id, then optimize the shard. Delete the sneakers photo, then run the very same recall from a moment ago. The sneakers photo disappears from the Photos lane, while the note about the shoes and other shopping memories can still be recalled. Forgetting removes exactly what you deleted, not every trace. Memory you can write, filter, grow — and forget.

---

## Beat 12 — NOTEBOOK §11. Persistence: reopen and recall

Run the persistence cell, then the cleanup cell.

**NARRATION**

> One last check, quickly — L2 already proved this, so we keep it short. Close the shard, disable the network, reopen the same path from disk, and recall the memory you just added. The receipt: the count is unchanged, the recall still returns your note, and no Python socket was opened. Your added memory survived the restart, offline.

---

## Beat 13 — WRAP

**NARRATION**

> So: one `EdgeShard` held a whole day across three source types and two vector spaces. You built the store, inspected a point, and wrote the recall yourself; you asked your own question, added your own memory, and forgot one — all offline. Next, the final lesson takes the same API to a new job — teaching a device to recognize a brand-new object by writing memory, without retraining a model.
