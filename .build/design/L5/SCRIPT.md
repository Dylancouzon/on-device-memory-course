# L5 — Teaching It to See — script

**Target runtime:** ~11 min

NOTEBOOK beats reference the section numbers as they appear in the
executed `L5.ipynb`.

The device learns a new object by *writing memory*, not by retraining. The
lesson's arc is one live reveal: an object the device fails to recognize, a
few lines that teach it, and the same object recognized from a different
angle seconds later. Then you teach one yourself — and the finale is the
course capstone: everything you built, assembled into one assistant that
answers questions and recognizes what you taught it, offline.

Everything runs on the bundled object photos in `data/objects/`, so the
whole lab works offline in the course container. On the video, the
instructor captures object views live on camera; the student path uses the
same bundled photos.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Endpoint teaser + learn an object by writing memory | 40 |
| 2 | SLIDE 1 | The memory loop, this lesson's piece highlighted | 15 |
| 3 | SLIDE 2 | Teach → store → recognize | 35 |
| 4 | NOTEBOOK §1 | An object-memory shard (image vector + threshold) | 35 |
| 5 | NOTEBOOK §2 | The objects on hand (gallery, seen up front) | 25 |
| 6 | NOTEBOOK §3 | Teach what it already knows (two views — and just one) | 50 |
| 7 | NOTEBOOK §4 | Show it something new — not recognized yet | 50 |
| 8 | NOTEBOOK §5 | Teach it the new object | 35 |
| 9 | NOTEBOOK §6 | **The payoff:** recognize it from a new angle | 55 |
| 10 | NOTEBOOK §7 | Inspect the threshold gap (score bars) | 50 |
| 11 | NOTEBOOK §8 | Your turn: teach an object yourself | 45 |
| 12 | NOTEBOOK §9 | Assemble the assistant: a day + weeks + the taught object | 45 |
| 13 | NOTEBOOK §10 | **The payoff:** ask it about your day (cross-modal recall) | 50 |
| 14 | NOTEBOOK §11 | **The payoff:** show it what you taught (recognition + note) | 40 |
| 15 | NOTEBOOK §12 | **The payoff:** it all persists, offline | 40 |
| 16 | WRAP | Wrap the course's hands-on arc | 45 |

Total: ~655 sec (~11 min). The longest lesson — a deliberate call for
the students' capstone.

---

## Beat 1 — INTRO

**NARRATION**

Every lesson so far stored a memory you already had words or a picture
for. This one does something different: it teaches the device a brand-new
object it has never seen — without retraining or fine-tuning any model. It
just writes a few example vectors to memory. And at the end, everything
you've built in this course lands in one place: a single assistant that
answers questions about your day and recognizes what you taught it, with
the network off. Let's teach a device to see.

---

## Beat 2 — SLIDE 1: the memory loop, this lesson highlighted

```slide-brief
slug: l5-00-endpoint
purpose: the endpoint teaser — the same loop diagram as the earlier
  teasers; a "teach" arrow joins the loop and the whole loop is active.
on-slide text: node labels only — "capture", "embed", "store", "recall",
  new arrow label "teach", small tag "this lesson". No headline.
diagram spec (8:9): identical layout to slide l2-00-endpoint; all nodes
  active, plus a new orange arrow labeled "teach" dropping from
  "capture" directly into the "store" cylinder. Tag reads "this lesson:
  teach — then assemble everything".
```

**NARRATION**

The loop, one last time in a notebook. Today a new arrow joins it:
teaching, where a capture writes straight into memory as an example to
recognize by. And at the end of this lesson, the loop closes for good —
you assemble every piece you've built into one assistant.

---

## Beat 3 — SLIDE 2

```slide-brief
slug: teach-store-recognize
purpose: show the whole lesson as a three-step loop — teach an object by
  storing example views, then recognize a new view by nearest match.
on-slide text: node labels only — "views (teach)", "CLIP", cylinder
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
    bottom-up) share the same CLIP node and the same cylinder — one shared
    space.
```

**NARRATION**

Here's the whole idea in one picture. To teach, you embed a few views of an object with CLIP and store the vectors, tagged with a label. To recognize, you embed a new view the same way and find its nearest stored vector. If that match is close enough — above a threshold — the device knows what it's looking at. Teaching and recognizing use the exact same embedding space; the only difference is whether you're writing or reading.

---

## Beat 4 — NOTEBOOK §1. An object-memory shard

Run the shard cell.

**NARRATION**

One shard, one named vector this time — `image`, the CLIP space from L3. Each stored point is one view of an object, with a payload saying which object it is and which view. And one number that turns similarity into a decision: a recognition threshold. Above it, a query image counts as recognized; below it, the device says it doesn't know.

---

## Beat 5 — NOTEBOOK §2. The objects on hand

Run the gallery cell.

**NARRATION**

Before teaching anything, here are the objects this lab uses, laid out so you've seen every one before it's stored or queried. A couple of plants, a backpack, and a few everyday things — a rubber duck, a ceramic vase, a hard hat — each photographed from slightly different angles. Nothing is recognized yet; this is just what's on hand.

---

## Beat 6 — NOTEBOOK §3. Teach what it already knows

Run the `teach` cell.

**NARRATION**

Teaching is the mechanism worth slowing down on, and it's short: `teach` embeds each view with CLIP and upserts one point per view, with the object's id, label, and file in the payload. That's the whole learning step — an upsert, not a training run. We seed the shard with two objects: the lithops gets two views, and the backpack gets just one — plus a note about where it was bought; hold onto that note, it comes back at the finale. One view is already enough to recognize against; more views just make the memory more robust. You'll see both hold up later.

---

## Beat 7 — NOTEBOOK §4. Show it something new — not recognized yet

Run the recognize cell on the new object.

**NARRATION**

Now `recognize`: embed a query image, search the `image` vector for the nearest stored view, and compare the top score to the threshold. We show the device a flower it has never been taught, and put the query next to the closest thing it knows. That nearest match is well below the threshold, so the verdict is UNKNOWN. That's the honest starting point — the device doesn't pretend to recognize something it has no memory of.

---

## Beat 8 — NOTEBOOK §5. Teach it the new object

Run the teach-the-flower cell.

**NARRATION**

So we teach it. Give the new object a label — you can change it — and store two views. Two lines, and the device now has a memory of this object. No model was retrained; no weights changed. We only added vectors.

---

## Beat 9 — NOTEBOOK §6. The payoff: recognize it from a new angle

Run the recognize cell again on the same held-out view.

**NARRATION**

The first payoff, and the heart of the lesson: run the exact same query image that came back UNKNOWN a moment ago, side by side with the view it now matches. This query was never stored — it's a different angle from the two we taught. Now the nearest match is well above the threshold, and the device recognizes the object by its label. Same image, same threshold; the only thing that changed is that the device now has a memory to match against.

---

## Beat 10 — NOTEBOOK §7. Inspect the threshold gap

Run the evidence cell.

**NARRATION**

A recognition should be inspectable, so look at the evidence as a chart. Two taught objects, queried from views we never stored: the flower's held-out angle and the backpack's second photo — remember, the backpack was taught from a single view — both score above the line. Then images the device was never taught — a different plant, a book, a coffee cup — all land below it. That's the point: recognized objects and unknowns fall into two groups with a clear gap, and 0.80 sits inside that gap. It isn't a magic number; it's a known-versus-unknown line you can move as you teach more objects.

---

## Beat 11 — NOTEBOOK §8. Your turn: teach an object yourself

Run the editable cell, then change `my_object` and run again.

**NARRATION**

Your turn. Pick any object from the gallery with three views — the rubber duck, the vase, the hard hat — and teach two of them. Then hand it the third, an angle it never saw, and let it recognize what you just taught. Change `my_object`, re-run, and you get the same teach-and-recognize loop, now driven by you.

---

## Beat 12 — NOTEBOOK §9. Assemble the assistant

Run the assemble cell.

**NARRATION**

Here is where the whole course comes together, and you're building it yourself. One shard with both vectors — `text` for notes and voice, `image` for photos — the same design as L4. Into it goes the full day of captures, plus a few weeks of earlier notes, so the assistant has real history to draw on. Then we teach it today's object, the backpack: its view goes in the image vector with that note attached. One shard now holds everything you built — recorded memories and a taught object, side by side.

---

## Beat 13 — NOTEBOOK §10. The payoff: ask it about your day

Run the recall cell.

**NARRATION**

This assistant does two things. The first is answering a question about your day. The question — "the ramen place downtown" — goes into both vector spaces at once. It comes back with the photo you took, the voice memo you left, and the notes you wrote, all about the same place, drawn from today and from weeks ago. One question, every kind of memory, on the device.

---

## Beat 14 — NOTEBOOK §11. The payoff: show it what you taught

Run the recognition cell.

**NARRATION**

The second thing it does is recognize what you show it. We hand it a new photo of the backpack, a different angle than the one we taught. It matches above the threshold, and because we stored a note with the object, it doesn't just name the backpack — it recalls it: "I remember this, bought at SportsWorld, forty-five dollars." Asking and recognizing, both reading from the same local memory. That's the difference between a classifier and a memory: "I know what this is" becomes "I remember this."

---

## Beat 15 — NOTEBOOK §12. The payoff: it all persists, offline

Run the persistence cell.

**NARRATION**

One last check, the one that makes it real. Close the shard, block the network, reopen from disk, and run both skills again: the recall still finds the ramen place, and the backpack is still recognized. Everything this assistant knows lives on the device and survives a restart, with no server in the loop.

---

## Beat 16 — WRAP

**NARRATION**

That's the hands-on arc of the course, and you just closed it. You started with text notes in an embedded shard, added photos and cross-modal recall, combined meaning with structured filters, assembled a full day into an assistant — and now you've taught a device a new object by writing memory instead of retraining, and folded that into the same assistant. The through-line is one idea: with vector search on the device, memory is something an AI writes, reads, filters, grows, and forgets — private, persistent, and offline. In the final lesson, you'll see this exact design walking around on a robot.
