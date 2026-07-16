# L5: Teaching It to See (script)

**Target runtime:** ~11 min

NOTEBOOK beats reference the section numbers as they appear in the
executed `L5.ipynb`.

The device learns a new object by *writing memory*, not by retraining. The
lesson's arc is one live reveal, and the object is the student's own: a few
photos of something they own (bundled flower photos as the working
default), a failed recognition, a few lines that teach it, and the held-out
photo recognized seconds later. Then the course capstone: everything they
built, assembled into one assistant that answers questions and recognizes
what it was taught, offline, closing on the one path memory takes off the
device: a cloud upload the user switches on themselves, which L6's fleet
picks up.

The lab runs end-to-end on the bundled object photos in `data/objects/`, so
the core lesson works offline in the course container. Bringing your own
photos (§1, image URLs pasted into the first cell) and the cloud upload (§9,
an `UPLOAD_TO_CLOUD` switch plus `QDRANT_URL`/`QDRANT_API_KEY`) are the two
opt-in beats that leave the container. The object is set once, at the top,
so a single top-to-bottom run teaches it, with no mid-notebook edits. On the
video, the instructor captures object views live on camera; the student path
pastes links or leaves the bundled example in place.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Endpoint teaser + teach it something of your own | 40 |
| 2 | SLIDE 1 | The memory loop, this lesson's piece highlighted | 15 |
| 3 | SLIDE 2 | Teach → store → recognize | 35 |
| 4 | NOTEBOOK §1 | The object you'll teach (paste links, set once) | 20 |
| 5 | NOTEBOOK §2 | An object-memory shard (image vector + threshold) | 35 |
| 6 | NOTEBOOK §3 | Teach what it already knows (view gallery) | 50 |
| 7 | NOTEBOOK §4 | Show it your object: not recognized yet | 55 |
| 8 | NOTEBOOK §5 | Teach it, recognize it | 60 |
| 9 | NOTEBOOK §6 | Inspect the threshold gap (score bars + calibration) | 70 |
| 10 | NOTEBOOK §7 | Assemble the assistant (memory receipt) | 50 |
| 11 | NOTEBOOK §8 | Two skills, one memory (recall + recognize + both doors) | 70 |
| 12 | NOTEBOOK §9 | It persists, and leaves only when you choose | 70 |
| 13 | WRAP | Wrap the course's hands-on arc | 45 |

Total: ~615 sec (~10 min). The longest lesson, a deliberate call for
the students' capstone.

---

## Beat 1: INTRO

**NARRATION**

Every lesson so far stored a memory you already had words or a picture
for. This one does something different: it teaches the device a brand-new
object it has never seen, without retraining or fine-tuning any model. It
just writes a few example vectors to memory. And the object can be yours:
bring a couple of photos of something you own, and teach the device
yourself. At the end, everything you've built in this course lands in one
place: a single assistant that answers questions about your day and
recognizes what you taught it, with the network off. Let's teach a device
to see.

---

## Beat 2: SLIDE 1, the memory loop, this lesson highlighted

```slide-brief
slug: l5-00-endpoint
purpose: the endpoint teaser. The same loop diagram as the earlier
  teasers; a "teach" arrow joins the loop and the whole loop is active.
on-slide text: node labels only: "capture", "embed", "store", "recall",
  new arrow label "teach", small tag "this lesson". No headline.
diagram spec (8:9): identical layout to slide l2-00-endpoint; all nodes
  active, plus a new orange arrow labeled "teach" running from "capture"
  through "embed" into the "store" cylinder, so teaching visibly uses the
  same embed stage as every other write. Tag reads "this lesson:
  teach, then assemble everything".
```

**NARRATION**

The loop, one last time in a notebook. Today a new arrow joins it:
teaching, where a capture is embedded and written straight into memory as
an example to recognize by. Same loop, same embed stage; what changes is
why you're writing. And at the end of this lesson, the loop closes for
good. You assemble every piece you've built into one assistant.

---

## Beat 3: SLIDE 2

```slide-brief
slug: teach-store-recognize
purpose: show the whole lesson as a three-step loop. Teach an object by
  storing example views, then recognize a new view by nearest match.
on-slide text: node labels only: "views (teach)", "CLIP", cylinder
  "object shard", "new view (recognize)", "nearest match > threshold".
  No headline.
diagram spec (8:9, stack top-to-bottom):
  - Top: two small light-blue photo icons side by side labeled
    "views (teach)", curved orange arrow down into an orange (#FF9800)
    node "CLIP".
  - Middle: the orange CLIP node feeds a violet (#6047FF) cylinder labeled
    "object shard", drawn with a small strip of vector cells and a payload
    tag "label".
  - Bottom: a single light-blue photo icon labeled "new view (recognize)",
    curved red (#DC244C) arrow up through CLIP into the cylinder, returning
    a teal (#009688) check node labeled "nearest match > threshold".
  - The teach path (orange, top-down) and the recognize path (red,
    bottom-up) share the same CLIP node and the same cylinder: one shared
    space.
```

**NARRATION**

Here's the whole idea in one picture. To teach, you embed a few views of an object with CLIP and store the vectors, tagged with a label. To recognize, you embed a new view the same way and find its nearest stored vector. If that match is close enough, above a threshold, the device knows what it's looking at. Be precise about what this is: memory-based recognition of a specific thing. The device stores examples and asks whether a new view is close enough to one of them. No classifier gets trained. Teaching and recognizing use the exact same embedding space; the only difference is whether you're writing or reading.

---

## Beat 4: NOTEBOOK §1, the object you'll teach

Run the first cell (or paste your own image links first).

**NARRATION**

Before anything else, pick what you'll teach. Paste a couple of image links
of one thing you own: two or more angles to teach it, and one more to hold
out as a test. Leave them empty and the bundled example runs, so the lesson
works as-is; a helper turns those links into local images the device can
embed. Everything below reads from this one cell, so you set your object
once, here, and never touch it again.

---

## Beat 5: NOTEBOOK §2, an object-memory shard

Run the shard cell.

**NARRATION**

One shard, one named vector this time: `image`, the CLIP space from L3. Each stored point is one view of an object, with a payload saying which object it is and which view. And one number that turns similarity into a decision: a recognition threshold. Above it, a query image counts as recognized; below it, the device says it doesn't know.

---

## Beat 6: NOTEBOOK §3, teach what it already knows

Run the `teach` cell.

**NARRATION**

Teaching is the mechanism worth slowing down on, and it's short: `teach` embeds each view with CLIP and upserts one point per view, with the object's id, label, and file in the payload. That's the whole learning step. An upsert, not a training run. We seed the shard with two objects, and here they are, exactly what the device now knows: the lithops gets two views, and the backpack gets just one. One view is already enough to recognize against; more views just make the memory more robust. You'll see both hold up later.

---

## Beat 7: NOTEBOOK §4, show it your object: not recognized yet

Run the cell.

**NARRATION**

Now `recognize`: embed a query image, search the `image` vector for the nearest stored view, and compare the top score to the threshold. This is where your object from the first cell comes in. We show the device your held-out test photo and put it next to the closest thing the device knows. That nearest match is well below the threshold, so the verdict is UNKNOWN. That's the honest starting point. The device doesn't pretend to recognize something it has no memory of. One detail worth naming: if your own object comes back recognized here, look at the match. You just learned it resembles something the device was already taught.

---

## Beat 8: NOTEBOOK §5, teach it, recognize it

Run the teach cell, then the recognize cell.

**NARRATION**

So we teach it. One call stores your teach photos as memory, under your label. No model was retrained; no weights changed. We only added vectors. Now the heart of the lesson: run the exact same photo that came back UNKNOWN a moment ago. This photo was never stored. It's a different angle from the views we taught. Now the nearest match is well above the threshold, and the device recognizes the object by your label. Same image, same threshold; the only thing that changed is that the device now has a memory to match against. If you brought your own object, you just taught a device to recognize one of your own things.

---

## Beat 9: NOTEBOOK §6, inspect the threshold gap

Run the evidence cell.

**NARRATION**

A recognition should be inspectable, so look at the evidence as a chart. Two taught objects, queried from views we never stored: your object's held-out angle and the backpack's second photo. Remember, the backpack was taught from a single view. Both score above the line. Then images the device was never taught, a different plant, a book, a coffee cup: all land below it. For the bundled objects, taught and never-taught fall into two groups with a clear gap, and 0.80 sits inside it. It isn't a magic number, and it isn't universal. If your own object landed below the line, this chart is telling you why: the two views were too different for the device to be sure, and the fix is the same one the seed objects used. Give it another angle. Leave the threshold fixed in this lab, and know that a production system calibrates it against a much larger held-out set of knowns and unknowns.

---

## Beat 10: NOTEBOOK §7, assemble the assistant

Run the assemble cell.

**NARRATION**

Here is where the whole course comes together, and you're building it yourself. One shard with both vectors, `text` for notes and voice, `image` for photos, the same design as L4. Into it goes the full day of captures, plus a few weeks of earlier notes, so the assistant has real history to draw on. Then we teach it today's object, the backpack, and this time we don't just show it, we tell it something too. Its photo goes into the image vector and a note about it goes into the text vector, both in one memory. That's the first point in this course carrying both vectors at once: one thing the device can find by sight and by what was said about it. Read the receipt: recorded memories and a taught object, side by side in one shard.

---

## Beat 11: NOTEBOOK §8, two skills, one memory

Run the recall cell, then the recognition cell.

**NARRATION**

This assistant does two things from the same memory. The first is answering a question about your day. The question, "the ramen place downtown", goes into both vector spaces at once, and it comes back with the photo you took, the voice memo you left, and the notes you wrote, all about the same place, drawn from today and from weeks ago. The second is recognizing what you show it. We hand it a new photo of the backpack, a different angle than the one we taught. It matches above the threshold, and because we stored a note with the object, it doesn't just name the backpack. It recalls it: "I remember this, bought at SportsWorld, forty-five dollars." And now watch the two-vector point earn its keep. Ask in words, "what did I buy at SportsWorld?", and the text search returns the same memory the photo just matched. Same id, one point, two ways in: by sight, and by what was said about it. That's the difference between a classifier and a memory: "I know what this is" becomes "I remember this."

---

## Beat 12: NOTEBOOK §9, it persists, and leaves only when you choose

Run the persistence cell, then the cloud cell.

**NARRATION**

Two last checks, and they're two sides of the same promise. First: close the shard, block Python socket creation with the offline guard, reopen from disk, and run both skills again. The recall still finds the ramen place; the backpack is still recognized. Everything this assistant knows lives on the device and survives a restart, with no server in the loop. Second: memory leaving the device is a choice you make, never a default. This cell is that choice, written as code: a switch in the cell, set to off, and until you flip it and point it at your own cluster, running the cell reports that nothing left the device. Flip it, and the upload is nothing exotic: it reads every point back out of the shard and upserts them to a Qdrant Cloud cluster. Same points, same format, because Edge and the server share it. That upload is the doorway to the next lesson: when many devices share what they've each been taught, this is the write they share it with.

---

## Beat 13: WRAP

**NARRATION**

That's the hands-on arc of the course, and you just closed it. You started with text notes in an embedded shard, added photos and cross-modal recall, combined meaning with structured filters, assembled a whole day into an assistant, and now you've taught a device a new object by writing memory instead of retraining, and folded that into the same assistant. The through-line is one idea: with vector search on the device, memory is something an AI writes, reads, filters, grows, and forgets. Private, persistent, and offline, with the cloud as an option instead of a requirement. In the final lesson, you'll see this exact design walking around on a robot.
