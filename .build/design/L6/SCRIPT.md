# L6 — The Robot — script

**Target runtime:** ~8 min
**Format:** video only — no notebook. Slides are **16:9**, styled per
`SLIDE_STYLE.md`. Demo beats reference `SHOTLIST.md`; production
direction lives there, never here.

**STATUS: PROVISIONAL.** The robot app, hardware, and shoot are pending
(`.build/PLAN.md` separate track). Every demo claim below — scores, the
threshold behavior, persistence, "same stack" — must be reconciled
against the recorded robot output before this script is finalized or
anything is recorded. Numbers on screen are the evidence; the script
never claims what the footage doesn't show.

A synthesis lecture that happens to have a robot. The robot runs the
course's exact stack — CLIP for image (512-d), Nomic for text (768-d),
Whisper for audio, Qdrant Edge as the store, the same 0.80 threshold — so
every stage of its loop maps back to a lesson the students built with
their own hands. Two pieces are honestly new, and both are named, not
taught.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Endpoint payoff first: fail → teach by voice → recognize | 75 |
| 2 | SLIDE 1 | The robot's loop: capture → detect → embed → match → teach | 50 |
| 3 | SLIDE 2 | The lesson map: you already built this | 60 |
| 4 | NARRATION | The two new pieces: detection, and when to remember | 60 |
| 5 | DEMO | Teach by voice, in full ("this is my mug") | 55 |
| 6 | DEMO | "What did you see today?" + offline reboot | 70 |
| 7 | WRAP | The course arc + repo pointer | 55 |

Total: ~425 sec (~7 min narration; ~8 min with demo beats at full length).

---

## Beat 1 — INTRO: the payoff first

Demo footage (shotlist #1–3): an object the robot has never seen; the
robot says it doesn't know it; one spoken sentence teaches it; a new
angle is recognized seconds later.

**NARRATION:**

This is the last lesson, so let's start with the payoff. This robot has
never seen this object. It looks — and it says so: it doesn't know. Now I
teach it, the way you'd teach a person: I show it the object and I tell
it what it is. One sentence. That's the whole training procedure. Now a
different angle — and it knows it, and it remembers what I said about it.
No model was retrained in those ten seconds. If you've done the labs, you
already know exactly what just happened — because you built it. This
lesson maps this robot, stage by stage, back to the notebooks.

---

## Beat 2 — SLIDE 1: the robot's loop

```slide-brief
slug: l6-01-robot-loop
purpose: the robot's continuous loop in one picture — the course loop
  with two new stages drawn in.
on-slide text: node labels only — "camera + mic", "detect (crop)",
  "embed", "match ≥ 0.80", "memory", "teach". No headline.
diagram spec (16:9, left-to-right):
  - Light-blue (#03A9F4) node "camera + mic" (photo + waveform icons) →
    gray (#4E5366) node "detect (crop)" drawn with a dashed "new" tag →
    orange (#FF9800) node "embed" → teal (#009688) diamond-ish node
    "match ≥ 0.80" → violet (#6047FF) cylinder "memory" (spiral-notebook
    motif).
  - A red (#DC244C) return arrow from the cylinder back toward the
    camera node, labeled "recognized · recalled".
  - A second, orange arrow labeled "teach" dropping from the camera+mic
    node directly into the cylinder, bypassing the match node.
  - The "detect (crop)" node is the only gray one — visually marked as
    the black box the course doesn't open.
```

**NARRATION:**

Here's the robot's loop. The camera and microphone capture continuously.
A detector finds objects in the frame and crops them — that stage is new,
and I'll come back to it. Each crop embeds with CLIP; each utterance goes
through Whisper and embeds with Nomic. The embedding is matched against
memory: nearest stored view, compared to a threshold of 0.80 — the same
number, literally the same check, as your notebooks. Above it, the robot
recognizes and recalls; below it, it says it doesn't know, and that's
your cue to teach. Teaching writes straight to memory: an upsert, not a
training run.

---

## Beat 3 — SLIDE 2: the lesson map

```slide-brief
slug: l6-02-lesson-map
purpose: every stage of the robot's loop tagged with the lesson where
  students built it themselves — the "you already built this" slide.
on-slide text: stage labels + lesson tags only — "mic → transcript · L4",
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

Now the same loop, with the receipts. The microphone-to-transcript path —
Whisper, then Nomic — is your L4, cell for cell. Store, recall, forget:
the memory lifecycle you walked in L2 with one repeated question. Frame
to embedding to nearest-match against a threshold: that's L5's teach and
recognize, unchanged. Asking about the day across photos, voice, and
text: the cross-modal recall you built in L3 and L4. And the memory
itself is one shard with a text vector and an image vector — the exact
assistant shard you assembled at the end of L5, with a camera and a
microphone bolted on. The robot's memory code mirrors what you wrote.

---

## Beat 4 — The two new pieces

No slide.

**NARRATION:**

Two things on that loop are genuinely new, and I'll name both rather than
teach them. First, detection. Your notebooks got clean, single-object
photos. A robot gets a cluttered frame, so an off-the-shelf detector —
YOLOE — finds and crops the objects before embedding. We throw its labels
away. Detection finds *a thing*; memory tells it *which* thing — your
mug, not "a mug." Second, when to form a memory. A camera at several
frames a second would write thousands of near-duplicate memories, so the
robot tracks what's stable in view and writes at a sensible cadence.
Both are engineering around the loop, not changes to it — and both are
in the repo if you want to open the box.

---

## Beat 5 — DEMO: teach by voice

Demo footage (shotlist #4): the full teach-by-voice interaction, close
up — the spoken sentence, the stored memory appearing.

**NARRATION:**

Watch the teach beat once more, slowly, because it's the course in one
interaction. I hold up the object and say "this is my mug." The camera
crops it and CLIP embeds it — that's the image vector. Whisper turns my
sentence into text and Nomic embeds it — that's a text vector, exactly
like a voice memo from L4. Both land in one memory: one point carrying
both named vectors — `image` and `text` — searchable by sight and by
what was said,
and my sentence in the payload. Next time the robot sees the mug from
another angle — the one you'll watch it recognize — the nearest-match
check clears the threshold, and what comes back isn't just a label —
it's what I told it, in my words.

---

## Beat 6 — DEMO: the day, recalled — then a reboot

Demo footage (shotlist #5–6): "what did you see today?" recall; then
power cycle, network off, both skills repeated.

**NARRATION:**

The robot's day is now a memory store, so you can ask it questions. "What
did you see today?" runs the same filtered recall as your notebooks — a
time window over the day, results grouped by what was seen and what was
heard. And the last check is the one you ran in L2 and again in L5:
reboot. Power off, no network, power on, reopen the shard from disk. The
mug is still recognized; the day is still there. Memory that survives a
restart isn't a feature of the demo — it's what makes any of this count
as memory.

---

## Beat 7 — WRAP

**NARRATION:**

That's the course. In L1 we said memory is not the model's weights — it's
the notebook the model keeps beside it. You then built that notebook with
your own hands: stored and recalled and forgot in L2, found the right
memory by description and by filter in L3, assembled a whole day in L4,
and taught a device to see in L5 — finishing with an assistant that keeps
both skills through a restart, offline. This robot is that same notebook,
walking around. The build is public — the repo link is below, and it runs
on hardware that costs about as much as a textbook stack. Take the loop,
put it on your own device, and teach it something. Thanks for building
with me.
