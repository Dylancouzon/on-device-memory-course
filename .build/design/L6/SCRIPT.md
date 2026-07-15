# L6 — Lab: Teach a Device a New Object — script

**Target runtime:** ~13 min

The device learns a new object by *writing memory*, not by retraining. The
lesson's arc is one live reveal: an object the device fails to recognize, a
few lines that teach it, and the same object recognized from a different
angle seconds later. The finale assembles the whole course into one
assistant — a day of captures, weeks of notes, and the taught object in a
single offline shard — that both answers questions and recognizes what you
show it.

Section 7 teaches from the webcam where the environment supports it: capture
views to teach an object, then capture a new angle to recognize it. When a
camera or widget is unavailable, section 8 uses the bundled photos in
`data/objects/` as the guaranteed offline fallback.

---

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Learn an object by writing memory, not retraining | 40 |
| 2 | SLIDE 1 | Teach → store → recognize | 35 |
| 3 | NOTEBOOK §1 | An object-memory shard (image vector + threshold) | 40 |
| 4 | NOTEBOOK §2 | Teach the objects it already knows | 45 |
| 5 | NOTEBOOK §3 | Show it something new — not recognized yet | 55 |
| 6 | NOTEBOOK §4 | Teach it the new object | 40 |
| 7 | NOTEBOOK §5 | **The payoff:** recognize it from a new angle | 60 |
| 8 | NOTEBOOK §6 | Inspect the evidence and the threshold (the gap) | 55 |
| 9 | NOTEBOOK §7 | **The payoff:** teach from the webcam | 55 |
| 10 | NOTEBOOK §8 | Bundled fallback: teach and recognize | 55 |
| 11 | NOTEBOOK §9 | Assemble the assistant: a day + weeks + the taught object | 30 |
| 12 | NOTEBOOK §9 | **The payoff:** ask it about your day (cross-modal recall) | 50 |
| 13 | NOTEBOOK §9 | **The payoff:** show it what you taught (recognition + note) | 40 |
| 14 | NOTEBOOK §10 | Persistence: reopen, recall + recognize, offline | 35 |
| 15 | WRAP | Wrap the course | 55 |

Total: ~690 sec (~11.5 min narration; ~13 min with the reveals and the
editable cells run live). This makes L6 the longest lesson — a deliberate
call for the course finale.

---

## Beat 1 — INTRO

**NARRATION**

Every lesson so far stored a memory you already had words or a picture for.
This one does something different: it teaches the device a brand-new object
it has never seen. And it does that without retraining or fine-tuning any
model — it just writes a few example vectors to memory. Let's finish the
course by teaching a device to recognize something new.

---

## Beat 2 — SLIDE 1

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
  - The teach path (orange, top-down) and the recognize path (red, bottom-up)
    share the same CLIP node and the same cylinder — one shared space.
```

**NARRATION**

> Here's the whole idea in one picture. To teach, you embed a few views of an object with CLIP and store the vectors, tagged with a label. To recognize, you embed a new view the same way and find its nearest stored vector. If that match is close enough — above a threshold — the device knows what it's looking at. Teaching and recognizing use the exact same embedding space; the only difference is whether you're writing or reading.

---

## Beat 3 — NOTEBOOK §1. An object-memory shard

Run the shard cell.

**NARRATION**

> One shard, one named vector this time — `image`, the CLIP space from L3. Each stored point is one view of an object, with a payload saying which object it is and which view. And one number that turns similarity into a decision: a recognition threshold. Above it, a query image counts as recognized; below it, the device says it doesn't know.

---

## Beat 4 — NOTEBOOK §2. Teach the objects it already knows

Run the `teach` cell.

**NARRATION**

> Teaching is the mechanism worth slowing down on, and it's short: `teach` embeds each view with CLIP and upserts one point per view, with the object's id and label in the payload. That's the whole learning step — an upsert, not a training run. We seed the shard with one object it already knows, so it isn't starting empty.

---

## Beat 5 — NOTEBOOK §3. Show it something new — not recognized yet

Run the recognize cell on the new object.

**NARRATION**

> Now `recognize`: embed a query image, search the `image` vector for the nearest stored view, and compare the top score to the threshold. Here we show the device a flower it has never been taught. The nearest thing it knows is well below the threshold, so the verdict is UNKNOWN. That's the honest starting point — the device doesn't pretend to recognize something it has no memory of.

---

## Beat 6 — NOTEBOOK §4. Teach it the new object

Run the teach-the-flower cell.

**NARRATION**

> So we teach it. Give the new object a label — you can change it — and store two views. Two lines, and the device now has a memory of this object. No model was retrained; no weights changed. We only added vectors.

---

## Beat 7 — NOTEBOOK §5. The payoff: recognize it from a new angle

Run the recognize cell again on the same held-out view.

**NARRATION**

> The first payoff, and the heart of the lesson: run the exact same query image that came back UNKNOWN a moment ago. This view was never stored — it's a different angle from the two we taught. Now the nearest match is well above the threshold, and the device recognizes the object by its label. Same image, same threshold; the only thing that changed is that the device now has a memory to match against.

---

## Beat 8 — NOTEBOOK §6. Inspect the evidence and the threshold

Run the evidence cell.

**NARRATION**

> A recognition should be inspectable, so look at the evidence and at why the threshold is 0.80. First, the flower recognized from a held-out view: its two stored views rank at the top, both above the line. Then objects the device was never taught — a different flower, a book, a coffee cup — all land below it. That's the point: recognized objects and unknowns fall into two groups with a clear gap, and 0.80 sits inside that gap. It isn't a magic number; it's a known-versus-unknown line you can move as you teach more objects.

---

## Beat 9 — NOTEBOOK §7. The payoff: teach from the webcam

Point the camera at an object, capture a view to teach it, then capture a new
angle to recognize it.

**NARRATION**

> Another payoff — your turn, with the webcam. Point the camera at an object and use the capture button to save a view. The next cell sends that snapshot through `snapshot_to_file`, then teaches it as `my object`. Capture a NEW angle, run the recognition cell, and the device searches its local image memory for the nearest view. Capture a couple of teaching views if you want a stronger memory. If no camera or widget is available, skip to the bundled fallback in the next section — it demonstrates the same teach-and-recognize loop entirely offline.

---

## Beat 10 — NOTEBOOK §8. Bundled fallback: teach and recognize

Run the bundled fallback cell.

**NARRATION**

> The guaranteed fallback uses the bundled backpack photos. Teach one view, then recognize a second, unseen angle. One view is enough to recognize; more views make the memory more robust. This is the same loop as the webcam section — see, teach, recognize — using files that work in every offline course environment.

---

## Beat 11 — NOTEBOOK §9. Assemble the assistant

Run the assemble cell.

**NARRATION**

> Here is where the whole course comes together. We build one shard with both vectors — `text` for notes and voice, `image` for photos — the same design as L5. Into it goes a full day of captures, plus a few weeks of earlier notes, so the assistant has real history to draw on. Then we teach it today's object, the backpack: its views go in the image vector with a note attached. One shard now holds everything you built — recorded memories and a taught object, side by side.

---

## Beat 12 — NOTEBOOK §9. The payoff: ask it about your day

Run the recall cell.

**NARRATION**

> This assistant does two things. The first is answering a question about your day. The question — "the ramen place downtown" — goes into both vector spaces at once. It comes back with the photo you took, the voice memo you left, and the notes you wrote, all about the same place, drawn from today and from weeks ago. One question, every kind of memory, on the device.

---

## Beat 13 — NOTEBOOK §9. The payoff: show it what you taught

Run the recognition cell.

**NARRATION**

> The second thing it does is recognize what you show it. We hand it a new photo of the backpack, a different angle than the one we taught. It matches above the threshold, and because we stored a note with the object, it doesn't just name the backpack — it recalls it: "I remember this, bought at SportsWorld, forty-five dollars." Asking and recognizing, both reading from the same local memory. That's the difference between a classifier and a memory: "I know what this is" becomes "I remember this."

---

## Beat 14 — NOTEBOOK §10. Wrap: it all persists, offline

Run the persistence cell, then the cleanup cell.

**NARRATION**

> One last check, the one that makes it real. Close the shard, block the network, reopen from disk, and run both skills again: the recall still finds the ramen place, and the backpack is still recognized. Everything this assistant knows lives on the device and survives a restart, with no server in the loop.

---

## Beat 15 — WRAP

**NARRATION**

> That's the course. You started with text notes in an embedded shard, added photos and cross-modal recall, combined meaning with structured filters, assembled a full personal-memory assistant you could question and extend, and just now taught a device a new object by writing memory instead of retraining. The through-line is one idea: with an embedded vector search engine on the device, memory is something an AI writes, reads, filters, grows, and forgets — private, persistent, and offline. Everything you built here runs in the same small container an edge device gives you.
