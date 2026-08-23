# L6: Teaching It to See (script)

**Target runtime:** ~11 min

Talking points, not narration. Each beat lists what to hit; wording is yours on the day.

NOTEBOOK beats reference the section numbers as they appear in the executed `Lesson6.ipynb`. Slide briefs live in `SLIDES.md` in this directory; beats name only the slug.

The device learns something new by writing memory, not by retraining. A student starts with an unrecognized photo, stores a few examples under a label of their own, then tests a photo it never saw. The rest of the lesson combines that skill with the assistant they built earlier.

The label is the point worth landing. Two photos of one object teach that object; two different black cats teach black cats. Same call, same store, and what the examples have in common is what the label means. That is also why the threshold is a knob: tight subjects leave a wide gap, varied ones a narrow one.

The lab runs end-to-end on the bundled photos in `ro_shared_data/objects/`, so the core lesson works offline in the course container. Bringing your own photos (§1, the upload button in the first cell) and the cloud sync (Appendix A, its own notebook in the lesson folder, a `USE_CLOUD` switch plus `QDRANT_URL`/`QDRANT_API_KEY`) are the two opt-in beats that leave the container. The lesson arc closes at §9, on the offline reboot, so the hands-on course ends on memory staying put. The subject is set once, at the top, so a single top-to-bottom run teaches it with no mid-notebook edits. On the video, the instructor captures photos live on camera; the student path uploads their own photos or leaves the bundled example in place.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO + SLIDE `l6-00-endpoint` | Endpoint teaser + teach it something of your own | 40 |
| 2 | SLIDE `teach-store-recognize` | Teach, store, recognize | 35 |
| 3 | NOTEBOOK §1 | The subject you'll teach | 20 |
| 4 | NOTEBOOK §2 | An object-memory shard | 35 |
| 5 | NOTEBOOK §3 | Give it a few memories first | 50 |
| 6 | NOTEBOOK §4 | Show it your subject: not recognized yet | 55 |
| 7 | NOTEBOOK §5 | Teach it, recognize it | 60 |
| 8 | NOTEBOOK §6 | Inspect the threshold gap | 70 |
| 9 | NOTEBOOK §7 | Assemble the assistant | 50 |
| 10 | NOTEBOOK §8 | Two ways into one memory | 70 |
| 11 | NOTEBOOK §9 | It persists, with no server in the loop | 50 |
| 12 | WRAP | Wrap the course's hands-on arc | 45 |
| 13 | APPENDIX | Cloud sync: one memory, many devices, optional | 45 |

Total: ~615 sec (~10 min). The longest lesson, a deliberate call for the students' capstone.

---

## Beat 1: INTRO, SLIDE `l6-00-endpoint`

- The loop one last time, lit end to end: this lesson uses every stage.
- Every lesson so far stored a memory you already had words or a picture for. This one teaches the device to recognize something it has never seen.
- No retraining, no fine-tuning: it writes a few example vectors to memory.
- You pick the subject. Find a couple of photos of anything, give it a name, teach it yourself.
- The ending: one assistant that answers questions about your day and recognizes what you taught it, with the network off.

## Beat 2: SLIDE `teach-store-recognize`

- To teach: embed a few photos with CLIP, store them under a label you choose.
- To recognize: embed a new photo the same way, find the nearest stored photo, and check the score against a threshold.
- Recognition from stored examples, not a newly trained classifier.
- Your examples decide whether the label means one object or a broader kind of object.

## Beat 3: NOTEBOOK §1, the subject you'll teach

Run the first cell, upload your photos into the two boxes, then run the next one.

- Two boxes, because the photos have two different jobs. On the left, two or more to teach with. On the right, one held back to test with.
- That held-back photo is the whole lab: the device sees it once before it knows anything, and once after you teach it.
- The upload buttons take photos straight off your machine. They land in a folder beside the notebook and stay there.
- Take them from different angles or in different places. Three shots from the same spot teach the device very little.
- Skip the upload and the bundled rubber duck runs, so the lesson works as shipped.
- The label, the note the device should remember, and the question you'll ask later all live in this cell.
- Everything below reads from here, so you set the subject once and never touch it again.

## Beat 4: NOTEBOOK §2, an object-memory shard

Run the shard cell.

- One shard, one named vector this time: `image`, the CLIP space from L4.
- Each point is one view of an object, with a payload saying which object and which file.
- One number turns similarity into a decision: `RECOGNIZE_THRESHOLD = 0.80`. Above it, recognized. Below it, the device says it doesn't know.

## Beat 5: NOTEBOOK §3, give it a few memories first

Run the `teach` cell.

- `teach` is short: embed each photo with CLIP, store one point per photo with an id, label, and file name.
- That is the learning step, writing examples rather than training a model. `flush` puts the new memory on disk right away, so it survives a power cut.
- Three everyday things go in first, a bicycle, a handful of chess pieces, and a camera, so the store isn't empty when we test.
- Notice what a label is here: whatever you say it is, and what your examples share is what it comes to mean.

## Beat 6: NOTEBOOK §4, show it your subject: not recognized yet

Run the cell.

- `recognize` embeds a query image, finds the nearest stored photo, and checks the score against the threshold.
- Your test photo hasn't been taught, so the verdict is UNKNOWN, and the chart names the closest thing the device does know.
- That is the honest starting point: it doesn't pretend to recognize something it has no memory of.
- If your own photo is recognized here, inspect the match. You just found out it resembles one of the three starters.

## Beat 7: NOTEBOOK §5, teach it, recognize it

Run the teach cell, then the recognize cell.

- Store your example photos under your label, two photos for the bundled duck: one on a car hood, one on a desk.
- Run the same held-out photo that came back UNKNOWN a moment ago. It was never stored, and now it clears the threshold at 0.880 and the device answers with your label.
- The model is unchanged. It only has examples to compare against now.
- How far this generalizes: two photos of one thing you own and it knows that thing; two different black cats and it knows black cats, because that is what those examples share.

## Beat 8: NOTEBOOK §6, inspect the threshold gap

Run the evidence cell.

- Your held-out photo sits above the line; five never-taught photos sit below it. That gap is the evidence for the threshold.
- Photo-to-photo scores run high, roughly 0.86 to 0.96 for a good match, so a number from another task means nothing here.
- If your subject landed below the line, add clearer examples, and test more known and unknown photos before settling on a number.
- The threshold itself is the `RECOGNIZE_THRESHOLD` line in the shard cell.

## Beat 9: NOTEBOOK §7, assemble the assistant

Run the assemble cell, then the cell that stores your subject and prints the receipt.

- One shard with `text` for notes and voice, `image` for photos: today's day, 102 earlier notes, and the subject you taught.
- Look at how that last point is built: one id, one payload, two vectors, the photo embedded with CLIP and your note with Nomic.
- The first point in this course with both, and it is what lets you reach one memory two ways, by sight or by what was said about it.

## Beat 10: NOTEBOOK §8, two ways into one memory

Run the one cell.

- Two skills, one store of 145 memories.
- Show it the held-out photo from the object lab. It clears the threshold, and because a note is stored with it, it tells you what you said about it.
- Then ask for that note in words: the same memory comes back, same id 5000, reached by sight a moment ago and by words now.
- That is the difference between a classifier and a memory: "I know what this is" becomes "I remember this".

## Beat 11: NOTEBOOK §9, it persists, with no server in the loop

Run the persistence cell.

- Close the shard, block Python's sockets, reopen from disk, run both skills again.
- Ask about the day and the ramen place still comes back. Your subject is still recognized.
- Everything this assistant knows lives in files on the device and survives being closed, with no server in the loop and nothing to reload.

## Beat 12: WRAP

- Text notes, then photos and filters, then an assistant that remembers a day and recognizes something you taught it, holding both through a restart with the network off.
- Nothing you stored has left this machine.
- The same design appears on a robot in the final lesson.

## Beat 13: APPENDIX A, cloud sync: one memory, many devices

Open `Lesson6_Appendix.ipynb` in the lesson folder and run its three sections. It sits outside the lesson arc, so it can be skipped on camera and left for students who want it.

- One appendix, for when you do want memory to travel. The switch ships off, so running it as-is reports that nothing left the device.
- Turn it on, point it at your own cluster, and three things happen.
- Push: the shard's points upsert to Qdrant Cloud, same points, same format, because Edge and the server share it.
- Restore: a second device, here a second folder, downloads one snapshot and knows everything this one learned, your day and the subject you taught.
- Stay in sync: the device sends a manifest of what it has, and the server answers with only what is new.
- That push-pull loop is fleet memory. It runs on real robots today in memory-fleet, and it is the doorway to the next lesson.
