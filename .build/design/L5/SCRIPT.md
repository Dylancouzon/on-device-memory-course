# L5: Teaching It to See (script)

**Target runtime:** ~11 min

NOTEBOOK beats reference the section numbers as they appear in the
executed `L5.ipynb`.

The device learns a new object by writing memory, not by retraining. A
student starts with an unknown object, stores a few examples, then tests a
new angle. The rest of the lesson combines that skill with the assistant
they built earlier.

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
| 2 | SLIDE 1 | Teach → store → recognize | 35 |
| 3 | NOTEBOOK §1 | The object you'll teach | 20 |
| 4 | NOTEBOOK §2 | An object-memory shard | 35 |
| 5 | NOTEBOOK §3 | Teach what it already knows | 50 |
| 6 | NOTEBOOK §4 | Show it your object: not recognized yet | 55 |
| 7 | NOTEBOOK §5 | Teach it, recognize it | 60 |
| 8 | NOTEBOOK §6 | Inspect the threshold gap | 70 |
| 9 | NOTEBOOK §7 | Assemble the assistant | 50 |
| 10 | NOTEBOOK §8 | Two skills, one memory | 70 |
| 11 | NOTEBOOK §9 | It persists, and leaves only when you choose | 70 |
| 12 | WRAP | Wrap the course's hands-on arc | 45 |

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

## Beat 2: SLIDE 1

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

## Beat 3: NOTEBOOK §1, the object you'll teach

Run the first cell (or paste your own image links first).

**NARRATION**

Before anything else, pick what you'll teach. Paste a couple of image links
of one thing you own: two or more angles to teach it, and one more to hold
out as a test. Leave them empty and the bundled example runs, so the lesson
works as-is; a helper turns those links into local images the device can
embed. Everything below reads from this one cell, so you set your object
once, here, and never touch it again.

---

## Beat 4: NOTEBOOK §2, an object-memory shard

Run the shard cell.

**NARRATION**

One shard, one named vector this time: `image`, the CLIP space from L3. Each stored point is one view of an object, with a payload saying which object it is and which view. And one number that turns similarity into a decision: a recognition threshold. Above it, a query image counts as recognized; below it, the device says it doesn't know.

---

## Beat 5: NOTEBOOK §3, teach what it already knows

Run the `teach` cell.

**NARRATION**

`teach` is short: embed each view with CLIP, then store one point per view
with an ID, label, and file name. That is the learning step—writing examples,
not training a model. `flush` saves the new memory to disk right away. The
starter set includes two views of a lithops and one of a backpack.

---

## Beat 6: NOTEBOOK §4, show it your object: not recognized yet

Run the cell.

**NARRATION**

`recognize` embeds a query image, finds the nearest stored view, and checks
the score against the threshold. Your test photo has not been taught yet, so
the result should be UNKNOWN. If your own photo is recognized here, inspect
the match: it may resemble something in the starter set.

---

## Beat 7: NOTEBOOK §5, teach it, recognize it

Run the teach cell, then the recognize cell.

**NARRATION**

Now store your example photos under your label. Run the same held-out photo
again. It was never stored, but it is another view of the object. This time,
the nearest match should clear the threshold. The model is unchanged; it now
has examples to compare against.

---

## Beat 8: NOTEBOOK §6, inspect the threshold gap

Run the evidence cell.

**NARRATION**

Use the chart to inspect the decision. Held-out views of taught objects sit
above the line; a different plant, a book, and a coffee cup sit below it.
Photo-to-photo scores are much higher than the text-to-photo scores in L3,
so a threshold never carries from one task to another. Here, 0.80 separates
the starter examples. The nearby plant is the useful near miss: it shows why
the threshold is not a guarantee. For a real product, test many known and
unknown images before choosing one. If your object misses, add another angle.

---

## Beat 9: NOTEBOOK §7, assemble the assistant

Run the assemble cell, then the teach cell that adds the backpack and
prints the receipt.

**NARRATION**

Now build the assistant. One shard has `text` for notes and voice, and
`image` for photos. We add the day, earlier notes, and a taught backpack.
The backpack point carries both a photo vector and a text vector, so it can
be found by sight or by the note attached to it.

---

## Beat 10: NOTEBOOK §8, two skills, one memory

Run the recall cell, then the recognition cell.

**NARRATION**

The assistant now has two ways to reach the same point. Ask about the ramen
place and it returns the related photo, voice note, and text note. Show it a
new backpack photo and it recognizes the object, then recalls its note. Ask
“what did I buy at SportsWorld?” and text search returns that same point.

---

## Beat 11: NOTEBOOK §9, it persists, and leaves only when you choose

Run the persistence cell, then the cloud cell.

**NARRATION**

Close the shard, block network sockets, reopen it, and run both checks again.
The ramen recall and backpack recognition still work. The final cell makes
uploading an explicit choice: it is off by default. If you switch it on and
provide your own cluster details, it copies the same stored points to Qdrant
Cloud.

---

## Beat 12: WRAP

**NARRATION**

You started with text notes, added photos and filters, then built an
assistant that can remember a day and recognize a taught object. The same
design appears on a robot in the final lesson.
