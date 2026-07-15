# L4 — Your On-Device Assistant — script

**Target runtime:** ~8 min

NOTEBOOK beats reference the section numbers as they appear in the
executed `L4.ipynb`.

This lab is built to be student-driven: they see the store, the point, and
the recall built in the open, then ask their own question and add their own
memory. One slide — the endpoint teaser; the notebook and its live output
carry the rest.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Endpoint teaser + bring a day's memories together | 35 |
| 2 | SLIDE 1 | The memory loop, this lesson's piece highlighted | 15 |
| 3 | NOTEBOOK §1 | A day's captures — voice notes transcribed on-device | 50 |
| 4 | NOTEBOOK §2 | The day at a glance (timeline, for inspection) | 35 |
| 5 | NOTEBOOK §3 | One shard, two named vectors + indexed fields | 35 |
| 6 | NOTEBOOK §4 | Store the day: two batches, then the gallery | 45 |
| 7 | NOTEBOOK §5 | Inspect a stored point | 30 |
| 8 | NOTEBOOK §6 | How recall works (QueryRequest for both spaces) | 50 |
| 9 | NOTEBOOK §7 | **The payoff:** sneakers under $50 (raw hits, then inbox) | 55 |
| 10 | NOTEBOOK §8 | Your turn: ask a question | 45 |
| 11 | NOTEBOOK §9 | **The payoff:** add your own memory, then recall it | 55 |
| 12 | WRAP | Wrap-up + pointer to L5 | 35 |

Total: ~485 sec (~8 min narration; a little more with the editable cells
run live).

---

## Beat 1 — INTRO

**NARRATION**

This lab brings together everything you've built so far. You'll store
photos, a voice note, and text notes from one day — the kind of day a phone
or a pair of smart glasses captures — in a single on-device shard, then ask
it your own questions and add your own memories — all offline. By the end
of this lesson, the assistant from the course teaser exists; L5 teaches it
to see. Let's build something.

---

## Beat 2 — SLIDE 1: the memory loop, this lesson highlighted

```slide-brief
slug: l4-00-endpoint
purpose: the endpoint teaser — the same loop diagram as the earlier
  teasers, with the capture stage joining and the whole loop now active.
on-slide text: node labels only — "capture", "embed", "store", "recall",
  small tag "this lesson: the whole loop". No headline.
diagram spec (8:9): identical layout to slide l2-00-endpoint; all four
  nodes at full strength for the first time, "capture" annotated with
  three tiny icons (photo, waveform, note). Tag reads "this lesson: the
  whole loop".
```

**NARRATION**

The loop again — and for the first time, all of it at once. Three kinds of
capture, two embedding paths, one store, one recall.

---

## Beat 3 — NOTEBOOK §1. A day's captures

Run the captures cell.

**NARRATION**

A day starts with 17 photos, five voice notes, and 20 text notes: 42 captures in all. Each capture carries the same metadata: source type, timestamp, location, category, price when relevant, and store. The voice notes arrive as audio, so a small Whisper model transcribes them on-device — the kind of speech-to-text a phone or a pair of smart glasses runs, no server and no account. Play the clip and read what the model heard, side by side. From there the transcript embeds exactly like any other text. The helper frees the speech model as soon as transcription is done — on a small device, you load what you need and release what you don't. Three source types, two embedding paths.

---

## Beat 4 — NOTEBOOK §2. The day at a glance

Run `day_timeline`.

**NARRATION**

Before asking anything, here's the raw material laid flat: photos in the upper lane as thumbnails, in the order they were taken, and the voice and text notes below as numbered markers. This is what a day of on-device capture looks like — nothing recalled yet, just what's there. It's for orientation, not a result.

---

## Beat 5 — NOTEBOOK §3. One shard, two named vectors

Run the shard-and-index cell.

**NARRATION**

One shard holds the whole day, with the two named vectors from L3: `text` for Nomic, `image` for CLIP. Then we index the four payload fields we'll filter on — category and location as keywords, timestamp and price as floats. That index is what lets the filters in a few cells' time run inside the query.

---

## Beat 6 — NOTEBOOK §4. Store the day

Run the three cells: the text batch, the photo batch, then the photo
gallery.

**NARRATION**

Store the day in two batches. The notes and transcripts embed with Nomic and land under the `text` vector; the photos embed with CLIP and land under `image`. Same `Point`, same upsert, whichever modality it came from — you built one by hand in L3, so here the batches can just run. Check the total: 42 memories, one shard. The last cell lays out all seventeen photos, so when a recall returns one later you've already seen it.

---

## Beat 7 — NOTEBOOK §5. Inspect a stored point

Run the scroll cell.

**NARRATION**

Pull one point back out and look at it. Its id, the named vectors it actually carries — this one is a text note, so only `text` — and its full payload. A photo point would show `image` instead. This is the raw shape everything else in the lab searches over.

---

## Beat 8 — NOTEBOOK §6. How recall works

Run the cell that defines `recall`.

**NARRATION**

Now build recall in the open. It embeds the question twice — Nomic for the `text` vector, CLIP for the `image` vector — and runs one `QueryRequest` against each, with the same filter. The two result lists stay separate, grouped as photos, voice notes, and text notes, because Nomic and CLIP scores are not on the same scale. The helper's `show_raw` prints the plain evidence — which space, the score, the id, the payload — so you always see the hits before any rendering.

---

## Beat 9 — NOTEBOOK §7. The payoff: sneakers under $50

Run the cell. Raw hits print first, then the memory inbox renders.

**NARRATION**

First payoff: "black and white sneakers under fifty dollars." The filter is spelled out in code: `Filter(must=[...])` with category equal to `shopping` and price below 50, using raw `FieldCondition`, `MatchValue`, and `RangeFloat` types. Look at `show_raw` first: the space searched, the score, the id, the payload, in plain text. Then the same hits rendered as the memory inbox. The evidence comes before the presentation, never the other way round.

---

## Beat 10 — NOTEBOOK §8. Your turn: ask a question

Run the editable cell, then change it and run again.

**NARRATION**

Your turn. The cell lists a handful of questions the day can answer — where you parked the bike, the gym locker code, when the dentist is — so you can start from one that lands. Change `my_question` to any of them or to your own, and set `my_category` to filter, or `None` to search everything. Re-run, and you get the same raw hits and the same inbox for your question.

---

## Beat 11 — NOTEBOOK §9. The payoff: add your own memory, then recall it

Run the editable cell.

**NARRATION**

The second payoff, and the one that makes it yours: add a memory. Change `my_note` and its metadata, embed it, build a `Point`, and upsert it into the same shard. Then recall it right away. The memory you just wrote comes back at the top — the store didn't need a rebuild or a restart to know something new. That's the whole promise of on-device memory: it grows as you use it.

---

## Beat 12 — WRAP

**NARRATION**

So: one `EdgeShard` held a whole day across three source types and two vector spaces. You built the store, inspected a point, and wrote the recall yourself; you asked your own question and added your own memory — all offline. Next, the final lab takes the same API to a new job — teaching a device to recognize a brand-new object by writing memory, without retraining a model — and then assembles everything you've built into one assistant.
