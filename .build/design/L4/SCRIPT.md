# L4: Your On-Device Assistant (script)

**Target runtime:** ~8 min

NOTEBOOK beats reference the section numbers as they appear in the
executed `L4.ipynb`.

This lab is driven by the notebook. Students inspect a day of memories, ask
their own question, and add a new memory. The live output is the visual:
the opening endpoint teaser is the only slide, and nothing comes between it
and the code.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Endpoint teaser + bring a day's memories together | 35 |
| 2 | NOTEBOOK §1 | A day's captures, voice notes transcribed on-device | 50 |
| 3 | NOTEBOOK §2 | The day at a glance | 35 |
| 4 | NOTEBOOK §3 | Set up the day's shard | 30 |
| 5 | NOTEBOOK §4 | Store the day | 45 |
| 6 | NOTEBOOK §5 | Inspect a stored point | 30 |
| 7 | NOTEBOOK §6 | How recall works | 50 |
| 8 | NOTEBOOK §7 | Your turn: recall your day | 60 |
| 9 | NOTEBOOK §8 | Add your own memory, then recall it | 55 |
| 10 | WRAP | Pointer to L5 | 35 |

Total: ~420 sec (~7 min narration; a little more with the editable cells
run live).

---

## Beat 1: INTRO, endpoint teaser

```slide-brief
slug: l4-00-endpoint
purpose: the endpoint teaser, recolored from l2-00-endpoint. Same layout,
  same four nodes; "capture" and "recall" are the highlighted pair.
on-slide text: node labels only: "capture", "embed", "store", "recall",
  small tag "this lesson". No headline.
diagram spec (8:9, stack top-to-bottom):
  - Identical to l2-00-endpoint: four hand-drawn rounded nodes in a
    vertical loop, light-blue (#03A9F4) "capture", orange (#FF9800)
    "embed", violet (#6047FF) cylinder "store", red (#DC244C) "recall",
    curved arrows connecting them, the recall arrow curving back up
    toward capture.
  - Only the highlight moves: "capture" and "recall" get a solid stroke
    and full-strength fill; "embed" and "store" render at reduced
    opacity.
  - The "this lesson" tag points at the highlighted pair. Small
    spiral-notebook motif beside the cylinder.
```

**NARRATION**

Back to the loop. This lesson leans on the two ends of it: everything a day
captures, and asking it a question. This lab puts photos, voice notes, and
text notes from one day into one local store. You will ask it your own
questions, then add a memory of your own.

---

## Beat 2: NOTEBOOK §1, a day's captures

Run the counts cell, then the voice-note cell.

**NARRATION**

This day has 42 captures: 17 photos, five voice notes, and 20 text notes. Each has a time and place, plus details such as a category or price. Voice notes start as audio, so we load Whisper locally and run `recognize` on one clip. Listen, then read the transcript. The helper repeats that for the remaining voice notes and releases the model. After that, transcripts work like any other text memory.

---

## Beat 3: NOTEBOOK §2, the day at a glance

Run `day_timeline`.

**NARRATION**

Before asking anything, here's the raw material laid flat: photos in the upper lane as thumbnails, in the order they were taken, and the voice and text notes below as numbered markers. This is what a day of on-device capture looks like. Nothing recalled yet, just what's there. It's for orientation, not a result.

---

## Beat 4: NOTEBOOK §3, set up the day's shard

Run the shard cell.

**NARRATION**

One shard holds the whole day, with the two named vectors from L3: `text` for Nomic, `image` for CLIP. One `EdgeShard.create`, and the store is ready to hold the day across both spaces.

---

## Beat 5: NOTEBOOK §4, store the day

Run the two cells: the text batch, then the photo batch.

**NARRATION**

Store the day in two batches. The notes and transcripts embed with Nomic and land under the `text` vector; the photos embed with CLIP and land under `image`. Same `Point`, same upsert, whichever modality it came from. You wrote this upsert by hand in the earlier labs, so here the batches can just run. Check the total: 42 memories, one shard. You already saw every photo on the timeline, so when a recall returns one later it's a face you know.

---

## Beat 6: NOTEBOOK §5, inspect a stored point

Run the scroll cell.

**NARRATION**

Pull one point back out and look at it. Its id, the first few of the 768 numbers in its `text` vector, and its full payload. A photo point would carry `image` instead. This is the raw shape everything else in the lab searches over.

---

## Beat 7: NOTEBOOK §6, how recall works

Run the cell that defines `recall`.

**NARRATION**

Now build recall in the open. It embeds the question twice, Nomic for the `text` vector, CLIP for the `image` vector, and runs one `QueryRequest` against each. The text query fetches a few extra hits so the voice and text lanes each keep their own top three. The two result lists stay separate, grouped as photos, voice notes, and text notes, because Nomic and CLIP scores are not on the same scale.

---

## Beat 8: NOTEBOOK §7, your turn: recall your day

Run the cell to see it work, then change it and run again.

**NARRATION**

Start with "the ramen place downtown." Recall searches both vector spaces, so results can include the photo, voice memo, and text note. `show_raw` shows the evidence first: space, score, ID, and payload. The inbox then makes the same results easier to scan. A faded text or voice card is below 0.6, so treat it as a weaker match. Change `my_question`, run again, and see which memories come back.

---

## Beat 9: NOTEBOOK §8, add your own memory, then recall it

Run the editable cell.

**NARRATION**

Add a memory of your own. Change `my_note` and `my_question`, then write the
new point to the same shard. Search for it right away. The new note comes
back first, and it is the only card that is not faded: nothing else in the
day comes close. No rebuild or restart is needed.

---

## Beat 10: WRAP

**NARRATION**

So: one `EdgeShard` held a whole day across three source types and two vector spaces. You built the store, inspected a point, and wrote the recall yourself; you asked your own question and added your own memory, all offline. Next, the final lab takes the same API to a new job, teaching a device to recognize a brand-new object by writing memory, without retraining a model, and then assembles everything you've built into one assistant.
