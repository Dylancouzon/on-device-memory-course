# L1: Why Devices Need Memory (script)

**Target runtime:** ~5 min
**Format:** video only, no notebook. Slides are **16:9**, styled per
`SLIDE_STYLE.md` (same visual criteria; the wide format restacks flows
left-to-right where the 8:9 briefs stack top-to-bottom). The instructor on
camera is the default; a slide appears only where a visual earns its place.

Lesson 0 introduces the course and the instructor. This lesson is the
idea: what on-device memory is, why it can't depend on the cloud, and the
loop the rest of the course builds. No code.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Endpoint teaser: the finished assistant, then the robot | 45 |
| 2 | NARRATION | Why memory can't depend on the cloud | 60 |
| 3 | SLIDE 1 | Memory beside the model, on the device | 40 |
| 4 | NARRATION | What "memory" means for a device | 50 |
| 5 | SLIDE 2 | The loop: capture → embed → store → recall, mapped to lessons | 60 |
| 6 | WRAP | Robot footage + what L2 builds | 45 |

Total: ~300 sec (~5 min).

---

## Beat 1: INTRO

Footage (shotlist #1): the L5 finale, endpoint first.

**NARRATION:**

By the end of this course, you will have built this: an assistant that
answers a question about your day with the photo you took, the voice memo
you left, and the notes you wrote, and that recognizes an object you
taught it, from an angle it never saw. All of it runs on the device in
front of you, and all of it keeps working with the network off. This
lesson is about the idea that makes that possible, and why it has to live
on the device, not in the cloud.

---

## Beat 2: Why memory can't depend on the cloud

No slide.

**NARRATION:**

Think about what this memory actually holds. Where you had coffee. What
your kitchen looks like. When your dentist appointment is. A log of your
day is the most personal data a device can hold, and the simplest privacy
guarantee is physical: it leaves the device only when you decide it
should. That's the first reason.

The second is availability. A memory that lives behind a network request
disappears on the plane, in the basement, on a hike. Your own memory
doesn't need coverage; a device's shouldn't either.

And the third is the shape of the interaction. An assistant that remembers
is consulted constantly: every question, every glance at a camera frame.
Recall has to be a local function call, not a round trip.

---

## Beat 3: SLIDE 1, memory beside the model

```slide-brief
slug: l1-01-memory-beside-model
purpose: the course's core mental model. An application orchestrating a
  frozen model and a growing memory store, all inside the device; the
  cloud crossed out.
on-slide text: node labels only: "model (frozen)", "assistant app",
  "memory (grows)", "device", crossed-out "cloud". No headline.
diagram spec (16:9, left-to-right):
  - One large dashed container spanning most of the slide, hand-lettered
    label "device".
  - Inside, left: an orange (#FF9800) rounded node with a brain icon,
    label "model (frozen)", drawn with a small padlock.
  - Inside, center: a light-blue (#03A9F4) rounded node, label
    "assistant app".
  - Inside, right: a violet (#6047FF) hand-drawn cylinder with the spiral
    notebook motif, label "memory (grows)", with a few small "+" marks
    to suggest growth.
  - Two red (#DC244C) arrows between the app and the cylinder, labeled
    "write" and "recall"; one thin arrow from the app to the model,
    labeled "context".
  - Outside the device container, top-right corner: a small desaturated
    gray (#4E5366) cloud with a hand-drawn ✕ through it.
```

**NARRATION:**

Here's the mental model for the whole course. The model's weights are
frozen. They're the same for everyone, and they don't change when your
day happens. Around the model sits your application, the assistant. The
application turns what the device captures into vectors and writes them
to a memory store on the same device; when you ask a question, it recalls
the closest memories and hands them to the model as context. The memory
grows; the weights never change. Memory is not the model's weights. It's
the notebook kept beside the model. Everything we build in this course is
that notebook, and the application code that writes and reads it. One
thing this picture leaves out on purpose: a language model generating
answers. Nothing in this course generates text. Memory and retrieval do
the work, and memory alone gets you surprisingly far. When you add a
language model later, this store is the memory it reads from.

---

## Beat 4: What "memory" means for a device

No slide.

**NARRATION:**

So what does that notebook have to do? The naive answer is to hand the
model your whole day in the prompt. But a prompt has a ceiling, and even
under it you get the right fact at the wrong moment. What the device needs
instead is retrieval, and retrieval takes five verbs. It writes: a photo, a
voice note, a text note becomes an entry. It reads: you ask in plain
words, and the closest memories come back by meaning, not by keyword. It
filters: "food, under fifteen dollars" is structure, not similarity. It
grows: a new memory is available the moment it's written, with no
retraining. And it forgets: you delete exactly what you choose, and it
stays deleted. If those five verbs sound like a database's job description,
that's the point: on-device memory is a small, private search engine over
your own life, running next to the model.

---

## Beat 5: SLIDE 2, the loop, mapped to the course

```slide-brief
slug: l1-02-loop-course-map
purpose: the capture → embed → store → recall loop as the course map,
  each stage tagged with the lesson that builds it. This is the
  course-map slide (the one place the journey framing is allowed).
on-slide text: node labels and lesson tags only: "capture", "embed",
  "store", "recall", tags "L2", "L3", "L4", "L5", "L6". No headline.
diagram spec (16:9, left-to-right):
  - Four hand-drawn rounded nodes in a horizontal loop: light-blue
    (#03A9F4) "capture" (tiny photo/waveform/note icons), orange
    (#FF9800) "embed", violet (#6047FF) cylinder "store", red (#DC244C)
    "recall"; curved arrows connect them, recall arcing back to capture.
  - Small hand-lettered lesson tags under the stages: "L2 store + recall",
    "L3 photos + filters", "L4 the whole day", "L5 teach it to see",
    "L6 on a robot", placed under the stage each lesson deepens, L6's
    tag under the loop arrow itself.
  - Spiral-notebook motif beside the cylinder.
```

**NARRATION:**

And here's how you'll build it. The loop is capture, embed, store, recall.
In the next lesson you build the store-and-recall half with text notes,
and walk one memory through its whole life: stored, recalled by meaning,
and forgotten on command. Lesson three adds photos and filters: finding
the right memory by describing it, or by constraining it. Lesson four
brings the whole day together, photos, voice notes, and text, into one
assistant. Lesson five teaches a device to recognize a brand-new object by
writing memory, and ends with you assembling the full assistant yourself.
And lesson six takes that exact design and puts it on a robot.

---

## Beat 6: WRAP

Footage (shotlist #2): the L6 robot finale.

**NARRATION:**

One last look at where this ends. This robot is running the same design
you'll build in the notebooks: the same encoders, the same store, the
same threshold. It has never been retrained; everything it knows about
its world, someone taught it by showing and telling. That's on-device
memory. In the next lesson, we start with an empty store and one question
it can't answer yet.
