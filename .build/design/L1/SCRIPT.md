# L1: Why Devices Need Memory (script)

**Target runtime:** ~3 min 50 sec
**Format:** video only, no notebook.

**Objective.** Understand why memory can't always live in the cloud: privacy,
offline access, and latency. Learn the on-device memory pattern and the
capture → embed → store → recall loop that guides the course.

**Principle.** Memory lives on the device as plain files managed directly by
the application. Qdrant Edge provides this as an embedded shard running inside
your application, with no server or account required.

Slides are **16:9**, styled per `SLIDE_STYLE.md` (same visual criteria; the
wide format lays flows out left-to-right where the 8:9 briefs stack top-to-
bottom). The instructor on camera is the default; a slide appears only where a
visual earns its place. Four slides here, one per idea:

| Slug | Idea |
|---|---|
| `l1-01-frozen-and-growing` | A frozen model beside a growing memory |
| `l1-02-two-paths` | The answer never leaves the device |
| `l1-03-memory-is-a-folder` | The shard is a directory in your process |
| `l1-04-loop-course-map` | capture → embed → store → recall, mapped to lessons |

`l1-04` is the 16:9 sibling of `l2-00-endpoint` (`SLIDES.md`, slide 1) with all
four stages lit and lesson tags added. Draw it from the same source file.

The endpoint teaser this lesson opens with is beat 1's footage: L1 builds no
single stage of the loop, so the loop slide arrives at beat 5 as the course map
rather than as a highlight.

Lesson 0 introduces the course, the instructor, and the lesson-by-lesson
roadmap. This lesson does not repeat that roadmap. It is the idea: what
on-device memory is, why it stays on the device, and what it looks like on
disk.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | The device that has never met you, then the endpoint | 38 |
| 2 | SLIDE 1 | Frozen weights, growing memory, and why not the prompt | 43 |
| 3 | SLIDE 2 | Privacy, coverage, and the cost of a round trip | 47 |
| 4 | SLIDE 3 | What it is on disk: a folder inside your process | 39 |
| 5 | SLIDE 4 | The loop, and how the lessons walk it | 39 |
| 6 | WRAP | Robot footage, then L2's empty folder | 25 |

Total: ~231 sec (~3 min 51 sec) at 156 words per minute, 601 words of
narration. Beat 3 is the longest hold on one slide; cut the coverage paragraph
first if the edit runs long.

---

## Beat 1: INTRO

Footage (shotlist #1): the L5 finale, endpoint first.

**NARRATION:**

Your phone can describe a photo and transcribe your voice, offline, on the
device. Then you close the app, and it has never met you. Those weights know
an enormous amount about the world and nothing at all about your Tuesday.

Four lessons from now, you'll have an assistant that answers a question about
your day with the photo you took and the voice memo you left. After that, a
robot that recognizes an object you taught it an hour ago. All of it on the
device, and all of it still working with the network off.

---

## Beat 2: SLIDE 1, a frozen model beside a growing memory

```slide-brief
slug: l1-01-frozen-and-growing
purpose: the course's mental model. One device holding a frozen model, the
  application, and a memory that grows. No cloud on this slide; that idea
  gets its own.
on-slide text: node labels and arrow labels only: "model (frozen)",
  "your app", "memory (grows)", container "device", arrows "write",
  "recall", "context". No headline.
diagram spec (16:9, left-to-right):
  - One large dashed rounded container spanning most of the slide,
    hand-lettered label "device".
  - Left, inside: an orange (#FF9800) rounded node with a brain icon and a
    small padlock, label "model (frozen)".
  - Center: a light-blue (#03A9F4) rounded node, label "your app".
  - Right: a violet (#6047FF) hand-drawn cylinder carrying the spiral
    notebook motif, label "memory (grows)", with three small "+" ticks
    rising off its top edge.
  - Two red (#DC244C) curved arrows between the app and the cylinder,
    labeled "write" and "recall". One thin arrow from the app to the model,
    labeled "context".
  - The model node and the cylinder are drawn at the same size, so the
    slide reads as two equal halves of one device.
```

**NARRATION:**

So where does yesterday go? Nothing writes to the weights. They're frozen:
identical on every device that downloaded them, and unchanged by anything that
happens to you today.

The obvious move is to paste your whole day into the prompt. That holds up
until the day gets long, and fails the moment you want last month. The prompt
is what you can hold in your hands right now. The notebook is what you wrote
down so you wouldn't have to.

We put a notebook beside the model. Your application writes to it as things
happen, and reads from it when you ask something. The model stays fixed while
the memory grows.

---

## Beat 3: SLIDE 2, the answer never leaves the device

```slide-brief
slug: l1-02-two-paths
purpose: one question, two possible paths. The short one stays inside the
  device; the long one crosses the network and is struck out. Carries all
  three reasons (privacy, coverage, cost) as drawing, not as text.
on-slide text: the question in quotes, "device", gray "cloud", path labels
  "answered here" and "round trip". No headline, no numbers.
diagram spec (16:9, left-to-right):
  - Left: a light-blue (#03A9F4) speech bubble, "where did I put it?".
  - Center: the same dashed "device" container from slide 1, simplified to
    the app node and the violet cylinder. A short red (#DC244C) arrow loops
    from the question through the cylinder and straight back out to a teal
    (#009688) checkmark. Label it "answered here".
  - A small hand-drawn padlock sits on the device boundary, at the point the
    long path would have to cross.
  - Right: a long desaturated gray (#4E5366) dashed arrow leaving the device
    for a gray cloud and returning, labeled "round trip". A hand-drawn ✕
    struck through it. The gray path passes a tiny gray signal-bars icon
    with the bars empty.
  - The two paths must differ obviously in length: the local loop short and
    tight, the gray one taking the long way around the slide.
```

**NARRATION:**

Why keep it on the device? Start with what's in it. A day's memory holds where
you had coffee, what your kitchen looks like, and when your dentist
appointment is. That's about as personal as data gets, and keeping it local
makes the privacy story a mechanical one: there's no network call in the
recall path, so there's no copy of your day on anyone else's disk.

Then there's coverage. Basements, planes, tunnels, the middle of a hike: the
memory has to answer in all of them.

And a memory like this gets consulted constantly, on every question and every
camera frame. So recall runs as a function call inside your own process.
Lesson two puts a number on it.

---

## Beat 4: SLIDE 3, memory is a folder

```slide-brief
slug: l1-03-memory-is-a-folder
purpose: de-mystify the store. The shard is a directory of ordinary files,
  managed by a library running inside the application's own process.
on-slide text: container "your app (one process)", node "Qdrant Edge",
  mono file rows "edge_config.json", "segments/", "wal/", gray struck-out
  labels "server", "account". No headline.
diagram spec (16:9, left-to-right):
  - One dashed rounded container across the left two-thirds, hand-lettered
    "your app (one process)".
  - Inside, left: a light-blue (#03A9F4) node with a small gear or code
    icon, unlabeled beyond the container title, representing the app code.
  - Inside, right: a violet (#6047FF) rounded node "Qdrant Edge", joined by
    a short plain line (no arrow, no network glyph) to a hand-drawn folder
    holding three mono-spaced rows: "edge_config.json", "segments/", "wal/".
    The spiral notebook motif tucks into the folder's corner.
  - Outside the container, right edge: two small gray (#4E5366) boxes
    "server" and "account", each with a hand-drawn ✕ through it.
  - The short line is the point: nothing crosses a process boundary.
```

**NARRATION:**

Here's what that notebook looks like on disk. Qdrant Edge, the embedded build
of Qdrant's vector search engine, runs as a shard inside your own process. The
shard is a folder: a config file, some segments, and a write-ahead log.
There's no server and no account. You copy it, move it, or delete it with the
same tools you use for any other folder.

Restart the process and the memories are still there, because the files are
still there. Everything we build over the next four lessons is that folder,
plus the code that writes to it and reads from it.

---

## Beat 5: SLIDE 4, the loop and the lessons

```slide-brief
slug: l1-04-loop-course-map
purpose: the capture → embed → store → recall loop as the course map, each
  stage tagged with the lesson that deepens it. The wide sibling of
  l2-00-endpoint, all four stages lit.
on-slide text: stage labels "capture", "embed", "store", "recall"; lesson
  tags "L2 store + recall", "L3 photos", "L4 a whole day", "L5 teach it to
  see", "L6 on a robot". No headline.
diagram spec (16:9, left-to-right):
  - Four hand-drawn nodes across the slide: light-blue (#03A9F4) "capture"
    carrying tiny photo, waveform and note icons; orange (#FF9800) "embed";
    violet (#6047FF) cylinder "store" with the spiral notebook motif; red
    (#DC244C) "recall". Curved arrows connect them left to right.
  - The recall arrow arcs back over the top of the row to capture, closing
    the loop above the nodes rather than below them.
  - Small hand-lettered lesson tags sit under the stage each lesson
    deepens: "L2 store + recall" under the store/recall pair, "L3 photos"
    under embed, "L4 a whole day" under capture, "L5 teach it to see"
    under the full row, "L6 on a robot" under the return arc.
  - All four stages at full strength here. The per-lesson teasers are this
    same drawing with stages dimmed.
```

**NARRATION:**

Four steps fill that folder, and it's the same four every time. Capture
something: a photo, a voice note, a line of text. Embed it, on the device.
Store it in the shard with the details you'd want to filter on later, like a
category or a price. Recall it later by asking in plain words.

The loop ends at recall. These notebooks retrieve, and when you add a language
model, recall is what feeds it. Every lesson from here runs this loop, and the
tags show which stage each one deepens. The last lesson runs all four on a
robot.

---

## Beat 6: WRAP

Footage (shotlist #2): the L6 robot finale.

**NARRATION:**

That robot is running the design you're about to build: the same encoders, the
same shard, the same threshold. Nobody retrained it. Everything in its memory,
someone put there by showing it and telling it, and it'll still be there
tomorrow with the Wi-Fi switched off.

Next lesson, we start where every memory starts. An empty folder, and a
question it can't answer yet.
</content>
</invoke>
