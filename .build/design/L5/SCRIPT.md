# L5: Your On-Device Assistant (script)

**Target runtime:** ~8 min

Talking points, not narration. Each beat lists what to hit; wording is yours on the day.

NOTEBOOK beats reference the section numbers as they appear in the executed `Lesson5.ipynb`. The slide brief lives in `SLIDES.md` in this directory; the beat names only the slug.

The notebook drives this lab. Students inspect a day of memories, ask their own question, and add a new memory. The live output is the visual: the opening endpoint teaser is the only slide, and nothing comes between it and the code.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO + SLIDE `l5-00-endpoint` | Endpoint teaser + bring a day's memories together | 35 |
| 2 | NOTEBOOK §1 | A day's captures, voice notes transcribed on-device | 50 |
| 3 | NOTEBOOK §2 | The day at a glance | 35 |
| 4 | NOTEBOOK §3 | Set up the day's shard | 30 |
| 5 | NOTEBOOK §4 | Store the day | 45 |
| 6 | NOTEBOOK §5 | Inspect a stored point | 30 |
| 7 | NOTEBOOK §6 | How recall works | 50 |
| 8 | NOTEBOOK §7 | Your turn: recall your day | 60 |
| 9 | NOTEBOOK §8 | Add your own memory, then recall it | 55 |
| 10 | WRAP | Pointer to L6 | 35 |

Total: ~420 sec (~7 min of talking; a little more with the editable cells run live).

---

## Beat 1: INTRO, SLIDE `l5-00-endpoint`

- Back to the loop, this time the two ends of it: what a day captures, and asking it a question.
- One local store holds photos, voice notes, and text notes from a single day.
- You will ask your own questions, then add a memory of your own.

## Beat 2: NOTEBOOK §1, a day's captures

Run the counts cell, then the voice-note cell.

- 42 captures: 17 photos, 20 text notes, five voice notes. Each carries a time and place, plus fields like category or price.
- Voice notes start as audio, so a small Whisper model runs locally: one helper call transcribes all five and releases the model.
- Play a clip, read its transcript. From here a transcript behaves like any other text memory.

## Beat 3: NOTEBOOK §2, the day at a glance

Run the two cells: the photos, then the notes.

- The raw material laid flat: 17 photos as thumbnails in capture order, then the 25 voice and text notes as a table with their times.
- Photos and words are separated on purpose, because that is how they are stored: two vectors, two spaces.
- This is what a day of on-device capture looks like. Orientation, not a result.

## Beat 4: NOTEBOOK §3, set up the day's shard

Run the shard cell.

- One shard for the whole day, with L4's two named vectors: `text` at 768 for Nomic, `image` at 512 for CLIP.
- One `EdgeShard.create` and the store is ready across both spaces.

## Beat 5: NOTEBOOK §4, store the day

Run the two cells: the text batch, then the photo batch.

- Two batches: 25 notes and transcripts under `text`, 17 photos under `image`.
- Same `Point`, same upsert, whichever modality it came from. You wrote that upsert by hand in L3, so these batches just run.
- Total: 42 memories in one shard. You already saw every photo in the strip, so a recalled photo will be a face you know.

## Beat 6: NOTEBOOK §5, inspect a stored point

Run the scroll cell.

- Pull one point back out: its id, the first six of 768 numbers in its `text` vector, and its full payload.
- A photo point would carry `image` instead.
- This is the raw shape everything else in the lab searches over.

## Beat 7: NOTEBOOK §6, how recall works

Run the cell that defines `recall`.

- Build recall in the open: embed the question twice, Nomic for `text` and CLIP for `image`, one search per space.
- The text query asks for ten hits so the voice and text lanes each keep their own top three.
- Results stay grouped as photos, voice notes, and text notes, because Nomic and CLIP scores are not on the same scale.

## Beat 8: NOTEBOOK §7, your turn: recall your day

Run the cell to see it work, then change it and run again.

- Start with "the ramen place downtown": the ramen photo, the voice memo at 0.809, and the typed note at 0.786 all come back.
- `show_raw` shows the evidence first: space, score, id, payload. The inbox then makes the same results scannable.
- A faded text or voice card scored below 0.6, so treat it as a weaker match. Photo scores are CLIP's, never measured against that cutoff.
- Change `my_question`, run again, see what comes back.

## Beat 9: NOTEBOOK §8, add your own memory, then recall it

Run the editable cell.

- Change `my_note` and `my_question` together, then write the new point to the same shard.
- Ask for it right away: the new note comes back first at 0.757, and it is the only text card that is not faded. Nothing else in the day comes close.
- No rebuild, no restart.

## Beat 10: WRAP

- One `EdgeShard` held a whole day across three source types and two vector spaces.
- You built the store, inspected a point, wrote the recall yourself, asked your own question, and added your own memory, all offline.
- Next: the same API on a new job, teaching a device to recognize a brand-new object by writing memory, then assembling everything into one assistant.
