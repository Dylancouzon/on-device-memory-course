# L5: Teaching It to See (script)

**Target runtime:** ~11 min

NOTEBOOK beats reference the section numbers as they appear in the
executed `L5.ipynb`.

The device learns something new by writing memory, not by retraining. A
student starts with an unrecognized photo, stores a few examples under a
label of their own, then tests a photo it never saw. The rest of the lesson
combines that skill with the assistant they built earlier.

The label is the point worth landing. Two photos of one object teach that
object; two different black cats teach black cats. Same call, same store,
and what the examples have in common is what the label means. That is also
why the threshold is a knob: tight subjects leave a wide gap, varied ones a
narrow one.

The lab runs end-to-end on the bundled photos in `data/objects/`, so the
core lesson works offline in the course container. Bringing your own photos
(§1, image links or filenames in the first cell) and the cloud upload
(Appendix A, an `UPLOAD_TO_CLOUD` switch plus `QDRANT_URL`/`QDRANT_API_KEY`)
are the two opt-in beats that leave the container. The lesson arc closes at
§9, on the offline reboot; the cloud is an appendix so the hands-on course
ends on memory staying put. The subject is set once, at the top,
so a single top-to-bottom run teaches it, with no mid-notebook edits. On the
video, the instructor captures photos live on camera; the student path
searches an image site or leaves the bundled example in place.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Endpoint teaser + teach it something of your own | 40 |
| 2 | SLIDE 1 | Teach → store → recognize | 35 |
| 3 | NOTEBOOK §1 | The subject you'll teach | 20 |
| 4 | NOTEBOOK §2 | An object-memory shard | 35 |
| 5 | NOTEBOOK §3 | Give it a few memories first | 50 |
| 6 | NOTEBOOK §4 | Show it your subject: not recognized yet | 55 |
| 7 | NOTEBOOK §5 | Teach it, recognize it | 60 |
| 8 | NOTEBOOK §6 | Inspect the threshold gap | 70 |
| 9 | NOTEBOOK §7 | Assemble the assistant | 50 |
| 10 | NOTEBOOK §8 | Ask it, then show it | 70 |
| 11 | NOTEBOOK §9 | It persists, with no server in the loop | 50 |
| 12 | WRAP | Wrap the course's hands-on arc | 45 |
| 13 | APPENDIX | Send a copy to the cloud, optional | 30 |

Total: ~615 sec (~10 min). The longest lesson, a deliberate call for
the students' capstone.

---

## Beat 1: INTRO, endpoint teaser

```slide-brief
slug: l5-00-endpoint
purpose: the endpoint teaser, recolored from l2-00-endpoint. Same layout,
  same four nodes; all four are highlighted, because the capstone closes
  the whole loop.
on-slide text: node labels only: "capture", "embed", "store", "recall",
  small tag "all of it". No headline.
diagram spec (8:9, stack top-to-bottom):
  - Identical to l2-00-endpoint: four hand-drawn rounded nodes in a
    vertical loop, light-blue (#03A9F4) "capture", orange (#FF9800)
    "embed", violet (#6047FF) cylinder "store", red (#DC244C) "recall",
    curved arrows connecting them, the recall arrow curving back up
    toward capture.
  - No node is dimmed: every node carries a solid stroke and
    full-strength fill. This is the only teaser in the course where the
    whole loop is lit, and that contrast is the beat.
  - The tag reads "all of it" and points at the closing arrow rather
    than at one node. Small spiral-notebook motif beside the cylinder.
```

**NARRATION**

The loop one last time, lit end to end: this lesson uses every stage of it.
Every lesson so far stored a memory you already had words or a picture
for. This one does something different: it teaches the device to recognize
something it has never seen, without retraining or fine-tuning any model.
It just writes a few example vectors to memory. And you pick the subject:
find a couple of photos of anything, give it a name, and teach the device
yourself. At the end, everything you've built in this course lands in one
place: a single assistant that answers questions about your day and
recognizes what you taught it, with the network off. Let's teach a device
to see.

---

## Beat 2: SLIDE 1

```slide-brief
slug: teach-store-recognize
purpose: show the whole lesson as a three-step loop. Teach an object by
  storing example photos, then recognize a new photo by nearest match.
on-slide text: node labels only: "photos (teach)", "CLIP", cylinder
  "object shard", "new photo (recognize)", "nearest match > threshold".
  No headline.
diagram spec (8:9, stack top-to-bottom):
  - Top: two small light-blue photo icons side by side labeled
    "photos (teach)", curved orange arrow down into an orange (#FF9800)
    node "CLIP".
  - Middle: the orange CLIP node feeds a violet (#6047FF) cylinder labeled
    "object shard", drawn with a small strip of vector cells and a payload
    tag "label".
  - Bottom: a single light-blue photo icon labeled "new photo (recognize)",
    curved red (#DC244C) arrow up through CLIP into the cylinder, returning
    a teal (#009688) check node labeled "nearest match > threshold".
  - The teach path (orange, top-down) and the recognize path (red,
    bottom-up) share the same CLIP node and the same cylinder: one shared
    space.
```

**NARRATION**

Here's the whole idea in one picture. To teach, you embed a few photos with CLIP and store the vectors, tagged with a label you choose. To recognize, you embed a new photo the same way and find its nearest stored vector. If that match is close enough, above a threshold, the device knows what it's looking at. Be precise about what this is: memory-based recognition. The device stores examples and asks whether a new photo is close enough to one of them. No classifier gets trained, and nothing decides in advance whether your label names one particular thing or a whole kind of thing. Your examples decide that. Teaching and recognizing use the exact same embedding space; the only difference is whether you're writing or reading.

---

## Beat 3: NOTEBOOK §1, the subject you'll teach

Run the first cell (or paste your own image links first).

**NARRATION**

Before anything else, pick what you'll teach. You need two or more photos
of one subject, and one more held back as a test. The easiest way is to
search an image site for something you like, a black cat, a red tractor,
whatever, and copy two or three image addresses. Photos saved next to the
notebook work the same way, by filename, and that's the route to take if
you'd rather teach something you own. Leave both empty and the bundled
example runs, so the lesson works as-is. Everything below reads from this
one cell, so you set your subject once, here, and never touch it again.

---

## Beat 4: NOTEBOOK §2, an object-memory shard

Run the shard cell.

**NARRATION**

One shard, one named vector this time: `image`, the CLIP space from L3. Each stored point is one view of an object, with a payload saying which object it is and which view. And one number that turns similarity into a decision: a recognition threshold. Above it, a query image counts as recognized; below it, the device says it doesn't know.

---

## Beat 5: NOTEBOOK §3, give it a few memories first

Run the `teach` cell.

**NARRATION**

`teach` is short: embed each photo with CLIP, then store one point per photo
with an ID, label, and file name. That is the learning step: writing
examples, not training a model. `flush` saves the new memory to disk right
away. First we give it three everyday things, a bicycle, a chess set, and a
camera, so the store isn't empty when we test. Notice what a label is here.
It is whatever you say it is, and what your examples have in common is what
it comes to mean.

---

## Beat 6: NOTEBOOK §4, show it your subject: not recognized yet

Run the cell.

**NARRATION**

`recognize` embeds a query image, finds the nearest stored photo, and checks
the score against the threshold. Your test photo has not been taught yet, so
the verdict is UNKNOWN, and the chart names the closest thing the device does
know. That is the honest starting point: it does not pretend to recognize
something it has no memory of. If your own photo is recognized here, inspect
the match. You just found out it resembles one of the three starters.

---

## Beat 7: NOTEBOOK §5, teach it, recognize it

Run the teach cell, then the recognize cell.

**NARRATION**

Now store your example photos under your label. Then run the same held-out
photo again, the one that came back UNKNOWN a moment ago. It was never
stored. This time the nearest match clears the threshold and the device
answers with your label. The model is unchanged; it only has examples to
compare against now. And notice how far this generalizes. Teach it two
photos of one thing you own and it knows that thing. Teach it two different
black cats and it knows black cats, because that is what those two examples
share. Same call, same store; the examples decide what the label means.

---

## Beat 8: NOTEBOOK §6, inspect the threshold gap

Run the evidence cell.

**NARRATION**

Use the chart to inspect the decision. Your held-out photo sits above the
line; five photos the device was never taught sit below it. Photo-to-photo
scores run much higher than the text-to-photo scores in L3, around 0.86 to
0.96 for a good match against about 0.30 there, so a threshold never
carries from one task to another. Read the size of the gap, because that is
what the threshold is really made of, and it depends on what you taught. A
tight subject like a cat leaves a wide gap. Something visually varied, three
different chairs, leaves a narrower one, and 0.80 may need to move. If your
own subject landed below the line, that is the chart doing its job: add
another photo, or pick examples with more in common. For a real product,
test many known and unknown images before settling on a number.

---

## Beat 9: NOTEBOOK §7, assemble the assistant

Run the assemble cell, then the teach cell that adds your subject and prints
the receipt.

**NARRATION**

Now build the assistant. One shard has `text` for notes and voice, and
`image` for photos. We add the day, earlier notes, and the subject you taught
in the first half. This time it goes in with a note attached, so the point
carries a photo vector and a text vector at once. That is the first point in
this course with both, and it is what lets you reach one memory two ways: by
sight, or by what was said about it.

---

## Beat 10: NOTEBOOK §8, ask it, then show it

Run the recall cell, then the recognition cell.

**NARRATION**

Two things, one store. First ask about your day: the ramen place returns the
photo you took, the voice memo you left, and the note you typed. Then show it
the held-out photo of your subject, the same one from the object lab, now
against a shard holding a hundred and forty-five memories. It clears the
threshold, and because you stored a note with it, it does not just name the
thing. It tells you what you said about it. Then ask for that note in words.
The same memory comes back, same ID, reached by sight a moment ago and by
words now. That is the difference between a classifier and a memory: "I know
what this is" becomes "I remember this".

---

## Beat 11: NOTEBOOK §9, it persists, with no server in the loop

Run the persistence cell.

**NARRATION**

One last check, and it is the one that makes any of this count as memory.
Close the shard, block Python's sockets, reopen it from disk, and run both
skills again. The ramen recall still finds the ramen place. Your subject is
still recognized. Everything this assistant knows lives in files on the
device and survives being closed, with no server in the loop and nothing to
reload.

---

## Beat 12: WRAP

**NARRATION**

You started with text notes, added photos and filters, then built an
assistant that can remember a day and recognize something you taught it, and
it held both through a restart with the network off. Nothing you stored has
left this machine. The same design appears on a robot in the final lesson.

---

## Beat 13: APPENDIX A, send a copy to the cloud

Run the appendix cell. It is outside the lesson arc, so it can be skipped
on camera and left for students who want it.

**NARRATION**

One appendix, for when you do want a copy off the device. The switch is off,
so running it as shipped reports that nothing left. Turn it on and point it
at your own cluster and it reads the points back out of the shard and upserts
them to Qdrant Cloud: same points, same format, because Edge and the server
share it. That is also the doorway to the next lesson, where devices share
what they have each been taught.
