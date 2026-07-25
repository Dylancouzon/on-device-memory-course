# L6: The Robot (script)

**Target runtime:** ~8 min
**Format:** video only, no notebook. Slides are **16:9**, styled per
`SLIDE_STYLE.md`. Demo beats reference `SHOTLIST.md`; production
direction lives there, never here.

**STATUS: PROVISIONAL.** The robot app, hardware, and shoot are pending
(`.build/PLAN.md` separate track). Every demo claim below, the scores, the
threshold behavior, persistence, fleet sync, "same stack", the location
label shown on recall, must be reconciled against the recorded robot output
before this script is finalized or anything is recorded. Numbers on screen
are the evidence; the script never claims what the footage doesn't show. The
location is a label set when the robot starts (`--location`), the same
`where` field your L4 captures carried, not a GPS reading, and never faked.

A synthesis lecture that happens to have a robot. The robot runs the
course's exact stack: CLIP for image (512-d), Nomic for text (768-d),
Whisper for audio, Qdrant Edge as the store, the same 0.80 threshold. So
every stage of its loop maps back to a lesson the students built with
their own hands. Two pieces are genuinely new, and both are named, not
taught. The fleet-sync beat is committed (L5 §9's upload tees it up): wire
it for real, never fake it.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Endpoint first: fail → teach by voice → recognize | 75 |
| 2 | SLIDE 1 | The robot's loop: capture → detect → embed → match → teach | 50 |
| 3 | SLIDE 2 | The lesson map: you already built this | 55 |
| 4 | NARRATION | The two new pieces: detection, and when to remember | 55 |
| 5 | DEMO | Teach by voice, in full ("this is my mug") | 55 |
| 6 | DEMO | "What did you see today?" · "where are my keys?" · offline reboot | 70 |
| 7 | DEMO | Forget it: teach wrong, delete, back to unknown | 35 |
| 8 | DEMO | Fleet sync: one robot teaches, another remembers | 45 |
| 9 | WRAP | The course arc + repo pointer | 50 |

Total: ~490 sec (~8.2 min narration; trim beat 6 or 8 in edit if it runs
long).

---

## Beat 1: INTRO, the finished robot first

Demo footage (shotlist #1–3): an object the robot has never seen; the
robot says it doesn't know it; one spoken sentence teaches it; a new
angle is recognized seconds later.

**NARRATION:**

This is the last lesson, so let's start at the end. This robot has
never seen this object. It looks, and it says so: it doesn't know. Now I
teach it, the way you'd teach a person: I show it the object and I tell
it what it is. One sentence. That's the whole training procedure. Now a
different angle, and it knows it, and it remembers what I said about it.
No model was retrained in those ten seconds. If you've done the labs, you
already know exactly what just happened, because you built it. This
lesson maps this robot, stage by stage, back to the notebooks.

---

## Beat 2: SLIDE 1, the robot's loop

```slide-brief
slug: l6-01-robot-loop
purpose: the robot's continuous loop in one picture. The course loop
  with two new stages drawn in.
on-slide text: node labels only: "camera + mic", "detect (crop)",
  "embed", "match ≥ 0.80", "memory", "teach". No headline.
diagram spec (16:9, left-to-right):
  - Light-blue (#03A9F4) node "camera + mic" (photo + waveform icons) →
    gray (#4E5366) node "detect (crop)" drawn with a dashed "new" tag →
    orange (#FF9800) node "embed" → teal (#009688) diamond-ish node
    "match ≥ 0.80" → violet (#6047FF) cylinder "memory" (spiral-notebook
    motif).
  - A red (#DC244C) return arrow from the cylinder back toward the
    camera node, labeled "recognized · recalled".
  - A second, orange arrow labeled "teach" from the camera+mic node
    through the "embed" node into the cylinder, bypassing only the match
    check, so teaching visibly shares the embed stage.
  - The "detect (crop)" node is the only gray one, visually marked as
    the black box the course doesn't open.
```

**NARRATION:**

Here's the robot's loop. The camera and microphone capture continuously.
A detector finds objects in the frame and crops them. That stage is new,
and I'll come back to it. Each crop embeds with CLIP; each utterance goes
through Whisper and embeds with Nomic. The embedding is matched against
memory: nearest stored view, compared to a threshold of 0.80, the same
number, literally the same check, as your notebooks. Above it, the robot
recognizes and recalls; below it, it says it doesn't know, and that's
your cue to teach. Teaching runs through the same embed stage and writes
straight to memory: an upsert, not a training run.

---

## Beat 3: SLIDE 2, the lesson map

```slide-brief
slug: l6-02-lesson-map
purpose: every stage of the robot's loop tagged with the lesson where
  students built it themselves. The "you already built this" slide.
on-slide text: stage labels + lesson tags only: "mic → transcript · L4",
  "store / recall / forget · L2", "frame → embed → match · L5",
  "cross-modal recall · L3–L4", "one shard, two skills, offline · L5".
  No headline.
diagram spec (16:9):
  - The same loop layout as slide l6-01-robot-loop, at reduced opacity,
    with five hand-lettered tags pinned to the stages, each tag a small
    card: the stage phrase and the lesson number in Qdrant Red.
  - No new nodes; this slide is the previous slide annotated.
```

**NARRATION:**

Now the same loop, with the receipts. The microphone-to-transcript path,
Whisper, then Nomic, is your L4, cell for cell. Store, recall, forget:
the memory lifecycle you walked in L2 with one repeated question, and
you'll watch all three of those on this robot before the lesson is out.
Frame to embedding to nearest-match against a threshold: that's L5's
teach and recognize, unchanged. Asking about the day across photos,
voice, and text: the cross-modal recall you built in L3 and L4. And
the memory itself is one shard with a text vector and an image vector,
the exact assistant shard you assembled at the end of L5, with a camera and a
microphone bolted on. The robot's memory code mirrors what you wrote.

---

## Beat 4: The two new pieces

No slide.

**NARRATION:**

Two things on that loop are genuinely new, and I'll name both rather than
teach them. First, detection. Your notebooks got clean, single-object
photos. A robot gets a cluttered frame, so an off-the-shelf detector,
YOLOE, finds and crops the objects before embedding. We throw its labels
away. Detection finds *a thing*; memory tells it *which* thing: your
mug, not "a mug." Second, when to form a memory. A camera at several
frames a second would write thousands of near-duplicate memories, so the
robot tracks what's stable in view and writes at a sensible cadence.
Both are engineering around the loop, not changes to it, and both are
in the repo if you want to open the box.

---

## Beat 5: DEMO, teach by voice

Demo footage (shotlist #4): the full teach-by-voice interaction, close
up. The spoken sentence, the stored memory appearing.

**NARRATION:**

Watch the teach beat once more, slowly, because it's the course in one
interaction. I hold up the object and say "this is my mug." The camera
crops it and CLIP embeds it: that's the image vector. Whisper turns my
sentence into text and Nomic embeds it: that's a text vector, exactly
like a voice memo from L4. Both land in one memory: one point carrying
both named vectors, `image` and `text`, searchable by sight and by what
was said, with my sentence in the payload. You built exactly this point
at the end of L5, when you taught the backpack with a note. Next time the
robot sees the mug from another angle, the one you'll watch it recognize,
the nearest-match check clears the threshold, and what comes back isn't
just a label. It's what I told it, in my words.

---

## Beat 6: DEMO, the day, recalled, then a reboot

Demo footage (shotlist #5–6): "what did you see today?" recall, then the
"where are my keys?" question that surfaces the location; then power cycle,
network off, both skills repeated.

**NARRATION:**

The robot's day is now a memory store, so you can ask it questions. "What
did you see today?" is the two ideas you built in L3 and L4 running
together: cross-modal recall over the day, narrowed by a filter. The
filter here is a time window, a new field for the same numeric-range
condition you wrote for "under fifteen dollars", and the results come
back grouped by what was seen and what was heard. And every memory also
carries where it was formed. Earlier I left this robot running in my hotel
room, and it saw my keys on the desk. So I can ask it something a photo
alone can't answer: where did I leave my keys? The keys come back, and the
memory says where it learned them, the hotel room. That's the same location
field you stored on every capture in L4, set once when the robot starts and
written onto every memory it forms. And here's the surprising part: no
language model answered any of that. The robot matched
vectors and grouped what it found. Retrieval, not generation. Put a
language model on top and it would phrase the reply in a sentence; the
remembering underneath is all memory. And the last check is the one you
ran at the end of L5: reboot. Power off, no network, power on, reopen the
shard from disk. The mug is still recognized; the day is still there.
Memory that survives a restart isn't a feature of the demo. It's what
makes any of this count as memory.

---

## Beat 7: DEMO, forget it

Demo footage (shotlist #7): the robot is taught the wrong label on
purpose, the memory is deleted on camera, and the same object comes back
unknown.

**NARRATION:**

One more verb, and it's the one that makes this a memory instead of a log.
Watch me teach it wrong on purpose: I hold up the object and give it the
wrong name, and now it's confidently wrong, because it believes what it
was told. So I delete that memory. One press, and what runs underneath is
`delete_points` on the ids for that label, the same call you made in L2
when you forgot the coffee place. Now the same object, same angle, and
it's unknown again. Nothing lingers, no retraining, no relearning around
the mistake. A device that can be taught has to be correctable, and on
this design correcting it is a delete.

---

## Beat 8: DEMO, fleet sync

Demo footage (shotlist #8, pending build): robot A is taught the mug;
an explicit sync runs; robot B (or a second device) recognizes the mug
and recalls the spoken note. Every claim here must match the recorded
output; if the fleet build isn't ready, this beat is cut, never staged.

**NARRATION:**

One robot learning is memory. Two robots sharing it is a fleet. In the
last lab, you ran the cell that uploads a shard to the cloud, and you
flipped that switch yourself. This is the same write, running between
machines: the mug this robot was just taught goes up as points, and the
second device pulls them down. Now it recognizes an object it has never
seen, because a teammate remembered for it. Same points, same format,
same choice: nothing syncs until someone decides it should.

---

## Beat 9: WRAP

**NARRATION:**

That's the course. In L1 we said memory is not the model's weights. It's
the notebook the model keeps beside it. You then built that notebook with
your own hands: stored and recalled and forgot in L2, found the right
memory by description and by filter in L3, assembled a whole day in L4,
and taught a device to recognize your own object in L5, finishing with an
assistant that keeps both skills through a restart, offline. This robot
is that same notebook, walking around, and it got this far without a
language model writing a word. Memory and retrieval carried it, and
that's the store your own model would read from. The build is public.
The repo link is below, and it runs on a board that costs about $250.
Take the loop, put it on your own device, and teach it something. Thanks
for building with me.
