# L1: Why Devices Need Memory (script)

**Target runtime:** ~7 min
**Format:** video only, no notebook.

**Objective.** Give the student the vector search toolbox the course uses
(vectors, similarity scores, one shared space for photos and text, the
store/recall/forget lifecycle), make the use cases land (wearable, worker
robot, offline robots, search and rescue), show the architecture that puts
the toolbox inside a device, and show the end of the course: the robot,
live, running that architecture. Filters are named once and deferred to
lesson three (Dylan's call, 2026-08-17: they don't hold their weight here).

**This version must fit all of DLAI's criteria at once** (do-over logged
2026-08-17):

- **Vector search 101 with real information density.** Each concept beat
  teaches one mechanism with a concrete example and real values. Slides are
  graphically simple but technically deep: every label is a component name,
  a real field, a real dimension, or a real score. Nothing decorative.
- **Show the end of the course.** Lesson 0 introduces the instructor, the
  sequence, and the problem, with no time for the robot. L1 shows it: a
  short live ask in the intro, a live demo beat near the end, and a live
  wrap. The robot is on set for the L1 shoot (recorded with the L6
  footage); no fallback branches. The robot frames the lesson without
  dominating it: three short moments, one demo beat.
- **A diagram of the architecture.** Beat 7's slide is the device
  architecture (encoders + memory in one process, the network path struck
  out); beat 8's slide is the same architecture on disk (the Qdrant Edge
  folder).
- **Why on-device is becoming important.** Beat 1 carries the why-now
  (capable models on ordinary hardware; memory is the missing half),
  beat 7 the three consequences (privacy, coverage, cost).
- **Last chance to talk about the problem, L0 overlap allowed.** Beat 1 is
  the problem; the overlap is deliberate and adds the live robot answer L0
  cannot show.
- **Retrieval 101 and use cases shown visually** (DLAI's 2026-08-11 ask):
  beats 2 and 3 are retrieval 101 with more depth. Use cases get their own
  beat (beat 6, expanded 2026-08-17 on Dylan's note that they were
  under-weighted): four settings on one montage slide, wearable (real L4
  §7 output), worker robot (course robot still), offline inspection
  robots and search and rescue (Dylan's renders, "illustration" labeled),
  plus the robot live in beats 1 and 9.

**Principle.** Memory lives on the device as plain files managed directly by
the application. Qdrant Edge provides this as an embedded shard running
inside your application, with no server or account required.

Slides are **16:9**, styled per `SLIDE_STYLE.md`. A slide comes up under the
sentence it illustrates and drops away after it; the camera (and the robot)
is the default shot. Two number rules: any score or vector value on a slide
is computed with the course's own encoders at slide-build time, never
invented; and no latency numbers appear in L1, because the course shows
latency exactly once, in L2 §6.

**Vocabulary.** L1 now owns the course's words: vector, embedding model,
similarity score, details (payload), index. Each is defined in the beat
that first uses it, then used without apology for the rest of the course.
Filters are named once in beat 5 and defined properly in lesson three. No code appears on screen. Internals stay out: how the embedding
model or the index works inside is prior-course material and is named as
such, not re-taught (no chunking, no embeddings-from-scratch, no ANN/HNSW).

Lesson 0 gives the lesson-by-lesson roadmap; L1 does not repeat it. Scores
follow the course's score-scale rule: beat 3 teaches that a score only means
something inside its own model's space, and each later lesson names its own
range.

**Beat 3's example is a deliberate L2 callback** (Dylan's call, 2026-08-17):
the latte question and terrace note are L2's own arc, shown answered here,
then rebuilt from an empty shard there; L2's intro acknowledges it. The two
lessons never show their scores side by side: L1's slide scores are computed
on its card strings, L2's payoff is the executed notebook's 0.653.

| Slug | Idea | Status |
|---|---|---|
| `l1-01-note-to-vector` | A note becomes 768 numbers; similar meaning, nearby vectors | New |
| `l1-02-nearest-and-scored` | The question ranked against three notes, real scores, keyword miss beside it | New |
| `l1-03-photos-and-words` | CLIP: image and text meet in one 512-number space | New |
| `l1-05-the-loop` | capture → embed → store → recall (+ forget) | Revised from `l1-03-the-loop` |
| `l1-04-where-it-matters` | Four use-case tiles: wearable, worker robot, offline inspection, search and rescue | New (replaces `l1-04-memory-record`, cut with the filter beat) |
| `l1-06-on-device` | Architecture: encoders + memory in-process, network path struck out | Merged from `l1-01`/`l1-04` of the prior version |
| `l1-08-memory-is-a-folder` | The shard is a directory in your process | Kept |

`l1-05-the-loop` stays the 16:9 sibling of `l2-00-endpoint` (brief in
`.build/design/L2/SCRIPT.md`), drawn from the same source file, all four
stages lit, no lesson tags. There is no `l1-00-endpoint` slide: the endpoint
teaser is the robot itself answering in beat 1.

Dropped: the mood-word slides (`frozen`/`grows` as standalone labels), the
robot capture slide, and the memory-record/filter slide (filters are lesson
three's). Two of Dylan's renders (mine/tunnel inspection, search and rescue)
are now in use on `l1-04-where-it-matters`; the edge anomaly render stays
standby.

## Visual sourcing

| Beat | Visual | Class | Source |
|---|---|---|---|
| 1 | The robot answering "where did you last see my keys?" | Live on set | L1 shoot; blocking in `L6/SHOTLIST.md` |
| 6 | Four use-case tiles: L4 §7 inbox, course robot still, mine/tunnel inspection, search and rescue | Captures + renders | `L4/Lesson4.ipynb` §7 executed output; L1/L6 shoot; Dylan's renders |
| 9 | The robot recognizing, then answering a spoken question, then being taught | Live on set | L1 shoot; blocking in `L6/SHOTLIST.md` |
| 10 | The robot after a power cut, network off | Live on set | L1 shoot; blocking in `L6/SHOTLIST.md` |
| 2–5, 7–8 | Diagrams | Drawn | House style, `SLIDE_STYLE.md` |

Anything on the robot's own display during the live beats is real output
from the machine; nothing staged goes on its screen. Captures keep the small
teal caption naming them.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---:|
| 1 | INTRO, robot on set | The problem, the robot's answer, why now | 56 |
| 2 | SLIDE 1 | A note becomes a vector | 37 |
| 3 | SLIDE 2 | Search, scores, and the score-scale rule | 61 |
| 4 | SLIDE 3 | Photos and words in one space; two vectors on one memory | 52 |
| 5 | SLIDE 4 | The lifecycle loop, plus forget and the index | 48 |
| 6 | SLIDE 5 | Where it matters: four use cases | 49 |
| 7 | SLIDE 6 | The on-device architecture and its three consequences | 37 |
| 8 | SLIDE 7 | The same architecture on disk: a folder | 31 |
| 9 | ROBOT, live demo | The end of the course: recognize, ask, teach | 42 |
| 10 | WRAP, robot on set | Power cut, memory intact; then L2 | 18 |

Total: ~431 sec (~7 min 11 sec) at 156 words per minute, 1,120 words of
narration. Budgets are counted from the narration below; re-count after any
edit. About 11 seconds over DLAI's 7 minutes: the trim order is beat 5's
index sentence, then beat 4's two-vector sentence. Beats 2 and 3 (retrieval
101), beat 6 (the use cases), and beat 9's demo (the end of the course) are
never cut.

---

## Beat 1: INTRO, robot on set

Camera, no slide. The robot is beside Dylan from the first frame; partway
through he asks it where his keys are and it answers with the stored frame.

**NARRATION:**

Where did you leave your keys?

Nobody can answer that except someone who was in the room and happened to
notice. Let me ask someone who was. Where did you last see my keys?

That answer came out of a memory: notes this robot wrote down as the day
happened, searched by meaning, on the machine that took them.

Here's why this is suddenly worth building. Models that can look at a
picture or listen to a sentence now run on ordinary hardware; everything you
just saw ran on the small computer inside this robot. The missing half is no
longer the model. It's the memory: writing things down, and finding the
right note when you ask.

This course builds that memory end to end, and it ends on this robot. This
first lesson is the toolbox: the handful of vector search ideas everything
else uses.

---

## Beat 2: SLIDE 1, a note becomes a vector

```slide-brief
slug: l1-01-note-to-vector
purpose: define embedding model and vector concretely. One note goes
  through the encoder and comes out as 768 numbers; a second note with
  the same meaning and no shared words lands beside it.
on-slide text: two note cards, "flat white on the terrace" and "coffee
  outside on the patio"; an orange node labeled "embedding model"; under
  each card its real vector snippet, set like "[ 0.03  -0.11  0.42  … ]";
  one shared sub-label "768 numbers". No headline.
diagram spec (16:9, left-to-right):
  - Left: the two note cards stacked, visibly sharing no words.
  - Center: one orange (#FF9800) rounded node labeled "embedding model",
    both cards' arrows passing through it.
  - Right: the two bracketed number strips, drawn close together, a short
    brace between them. Proximity is the payoff; nothing labels it.
  - Build note: the snippets are the first three components from
    `helper.embed_text` on these exact strings, pasted as produced.
```

**NARRATION:**

Start with one note: "flat white on the terrace". To make it findable by
meaning, the device runs it through an embedding model: a small neural
network whose only job is to turn text into a vector, a list of numbers.
Ours produces 768 of them.

No single number means anything on its own; what matters is geometry: notes
with similar meanings come out as vectors that sit close together, and
unrelated notes come out far apart. "Flat white on the terrace" and "coffee
outside on the patio" share no words, and still land side by side.

---

## Beat 3: SLIDE 2, search, scores, and the score-scale rule

```slide-brief
slug: l1-02-nearest-and-scored
purpose: retrieval itself. The question becomes a vector through the same
  model, the stored vectors are ranked by closeness, and each result
  carries a real score. The keyword miss is drawn small beside it.
on-slide text: the question "where can I sit outside for a latte?"; three
  memory cards, "flat white on the terrace", "dentist at 4", "new running
  shoes"; each card's real similarity score to the question; in the gray
  band, no text. No headline, no band labels.
diagram spec (16:9, two bands):
  - Top band, small, desaturated gray (#4E5366): the question, a gray
    magnifier, the three cards each under a hand-drawn ✕. Reads as a
    failed keyword search: zero shared words.
  - Bottom band, full color, most of the slide: the question with an
    orange (#FF9800) arrow through a small "embedding model" node reused
    from slide 1, then the three cards arranged by closeness, nearest
    first. The terrace card sits nearest, against a teal (#009688)
    checkmark and its score; the other two sit visibly far, each with its
    lower score. Distance and score agree; that agreement is the slide.
  - Build note: the three scores come from `helper.embed_text` cosine
    similarity on these exact strings, pasted as produced. Expected
    shape: the match lands in the measured text-to-text band (0.45 to
    0.80), the other two clearly below. If the terrace card does not
    score highest, fix the card text, never the numbers.
```

**NARRATION:**

Put a few notes like that into the memory, then ask it: "where can I sit
outside for a latte?" The question runs through the same embedding
model and becomes a vector too.

Search is then a measurement. The device compares the question's vector
against every stored vector and hands back the nearest ones, best first,
each with a similarity score. Higher means closer in meaning. Here the
terrace note wins clearly, and the dentist appointment and the running shoes
trail far behind. A keyword search on this memory finds nothing at all: not
one shared word. That's retrieval, and everything else in this course builds on that one
move.

One rule about scores. A score only means something inside
its own model's space. Scores top out at one; strong matches for our text
model land well below that, and image models run entirely different ranges. Each lesson names the
range it's playing in; never compare across.

---

## Beat 4: SLIDE 3, photos and words in one space

```slide-brief
slug: l1-03-photos-and-words
purpose: cross-modal embedding. CLIP's two encoders put an image and a
  description of it near each other in one shared space, which is what
  makes photo search by sentence, and later recognition, work.
on-slide text: the phrase card "a red bicycle"; labels "image encoder"
  and "text encoder" on the two nodes; one shared sub-label "one space ·
  512 numbers"; the bicycle photo itself. No headline.
diagram spec (16:9, left-to-right):
  - Left: two inputs stacked, the bicycle photo (from the L3 bank,
    `ro_shared_data/bank/`) and the phrase card.
  - Center: two orange (#FF9800) nodes, "image encoder" above, "text
    encoder" below, one arrow through each.
  - Right: both outputs landing in one violet (#6047FF) dashed region,
    drawn close together, sub-label "one space · 512 numbers".
  - Build note: use the same bicycle image L3 §4's verified default query
    returns, so the course shows one bicycle, not two.
```

**NARRATION:**

What about photos? One addition brings them into the same system. A model
like CLIP has two
halves: one embeds images, the other embeds text, and their outputs land in
one shared space of 512 numbers. A photo of a bicycle and the phrase "a red
bicycle" come out close together.

That means you can search photos with a sentence: embed the words, return
the nearest image vectors. No tags, no captions.
In lesson three you'll run exactly that over a bank of 165 photos. In lesson
five the same space gives you recognition: comparing a new photo with
remembered ones, image to image, against a threshold. That comparison is the
robot's "I've seen this before." And one memory can carry both vectors at
once, the words and the picture: one moment, findable both ways.

---

## Beat 5: SLIDE 4, the lifecycle loop

```slide-brief
slug: l1-05-the-loop
purpose: the four verbs in order, as one closed loop, each named by what
  it produces, with forget as the lifecycle's fifth verb on the cylinder.
on-slide text: stage names "capture", "embed", "store", "recall" with one
  sub-label each: "photo · voice · text", "→ a vector, on device",
  "original + vector + details", "nearest first, with scores"; a small
  "forget" tag with a minus sign on the cylinder. No headline, no lesson
  tags.
diagram spec (16:9, left-to-right):
  - Four hand-drawn nodes: light-blue (#03A9F4) "capture" with tiny
    photo, waveform and note icons; orange (#FF9800) "embed"; violet
    (#6047FF) cylinder "store" with the spiral notebook motif; red
    (#DC244C) "recall". Curved arrows left to right; the recall arrow
    arcs back over the top to capture, closing the loop above the nodes.
  - Sub-labels beneath each node at the template minimum size.
  - A small gray (#4E5366) "forget" tag with a minus sign hangs off the
    cylinder, opposite the details tag position used on the L2 sibling.
  - Draw from the same source file as l2-00-endpoint; the sub-labels and
    forget tag belong to this L1 version only and are dropped from the
    per-lesson teaser variants.
```

**NARRATION:**

Put the pieces in order and you get the loop the whole course walks. Capture
something: a photo, a voice note, a line of text. Embed it into a vector, on
the device. Store it, along with plain details like a category or a time;
lesson three puts those to work as filters. Recall it by asking in your own
words.

And one more verb: forget. A memory you can't delete from isn't yours, so
removing one note, and only that note, is part of the lifecycle. Lesson two
teaches store, recall, and forget as its three verbs. Under the store step
sits an index, the structure that keeps search fast as memories pile up.
You'll build one; how it works inside is lesson zero material.

---

## Beat 6: SLIDE 5, where it matters

```slide-brief
slug: l1-04-where-it-matters
purpose: the use cases, as one montage. Four settings where the memory has
  to answer on the machine itself, each shown honestly: captures captioned,
  renders labeled.
on-slide text: only the honesty labels: a teal caption on each capture
  ("real output, lesson 4" on the inbox; "our robot, lesson 6" on the
  robot tile) and a gray "illustration" label on each render. No headline,
  no stake words, no counts.
diagram spec (16:9, four tiles in a 2x2 grid inside the template margins):
  - Tile 1: the L4 §7 memory inbox capture (crop to the three result
    rows, labels and scores re-set at the 18 pt minimum, values as the
    notebook produced them), teal (#009688) caption.
  - Tile 2: a still of the course robot from the L1/L6 shoot, teal
    caption.
  - Tile 3: Dylan's mine or tunnel inspection render, gray (#4E5366)
    "illustration" label.
  - Tile 4: Dylan's search-and-rescue render, gray "illustration" label.
  - Renders follow the standing rules: no interface elements, no invented
    result rows, no numbers, no third-party branding.
  - Tiles appear one at a time under their sentences, then hold as a
    grid for the closing line.
```

**NARRATION:**

Why does the memory have to live on the device? Look where this is headed.

Glasses and phones that see and hear your whole day, and answer "where did I
leave my badge?" out of a memory that never left your pocket. You'll build
that assistant in lesson four. A worker robot that remembers where it last
saw the torque wrench, and tells you in plain words at the end of a shift.
Inspection robots in mines and tunnels, where there is no internet to call.
And search and rescue: a team indexing everything its drones see, in terrain
with no signal, because "did anyone see a red jacket near the north ridge?"
can't wait for coverage.

Different machines, one requirement: the memory answers right here, right
now.

---

## Beat 7: SLIDE 6, the on-device architecture

```slide-brief
slug: l1-06-on-device
purpose: the architecture diagram DLAI asked for. Encoders and memory
  inside one process on one device; the answer path never leaves; the
  network path is struck out with what it would cost written on it.
on-slide text: the question "where did I put it?"; inside the container,
  node labels "your app", "embedding model", "memory"; "in-process" along
  the returning arrow; on the gray path, "your data, uploaded" and "needs
  coverage". No headline, no numbers.
diagram spec (16:9, left-to-right):
  - Left: a light-blue (#03A9F4) speech bubble with the question.
  - Center: one dashed rounded container, unlabeled, reading as the
    device. Inside: light-blue "your app", the orange (#FF9800)
    "embedding model" node, and the violet (#6047FF) cylinder "memory".
    A short red (#DC244C) arrow runs question → embedding model →
    memory → back out to a teal (#009688) checkmark, "in-process" set
    small on the returning segment.
  - A hand-drawn padlock on the container boundary where the long path
    would cross.
  - Right: a long desaturated gray (#4E5366) dashed arrow out to a gray
    cloud and back, struck with a ✕, "your data, uploaded" on the way
    out, "needs coverage" on the way back.
  - The local loop is short and tight; the gray path takes the long way
    around the slide.
```

**NARRATION:**

Every one of those machines runs the same design, and this is it: the
architecture of the whole course. The embedding models and the memory live
inside your application's own process. A question is embedded, matched, and
answered without touching a network. Recall is a function call.

Three things follow. Privacy: your day never leaves the machine; there's no
copy on anyone else's disk. Coverage: the memory answers with the network
gone. And cost: a memory consulted on every question and every camera frame
can't afford a round trip. Lesson two puts numbers on that.

---

## Beat 8: SLIDE 7, the same architecture on disk

```slide-brief
slug: l1-08-memory-is-a-folder
purpose: de-mystify the store. The shard is a directory of ordinary files
  managed by a library inside the application's own process.
on-slide text: "Qdrant Edge" on its node; three mono-spaced file rows
  with one annotation each: "edge_config.json · settings", "segments/ ·
  vectors + notes + details", "wal/ · recent writes". No headline.
diagram spec (16:9, left-to-right):
  - The same dashed container, unlabeled. Inside, left: the light-blue
    (#03A9F4) app node with a small code icon. Inside, right: a violet
    (#6047FF) rounded node "Qdrant Edge" joined by a short plain line
    (no arrow, no network glyph) to a hand-drawn folder holding the
    three annotated file rows; the spiral notebook motif in the folder's
    corner.
  - The short line is the point: nothing crosses a process boundary. The
    absent server and account are absent from the slide too.
```

**NARRATION:**

On disk, this whole memory is a folder. Qdrant Edge, the embedded build of
Qdrant's vector search engine, runs inside your own process, and that folder
holds three things: a config file with the settings, segments holding each
vector with its note and details, and a write-ahead log of recent writes.
There's no server and no account. You copy it, move it, or delete it like any other folder. Restart the process, and everything is still
there, because the files are.

---

## Beat 9: ROBOT, live demo

Camera, no slide. Three quick moments: the robot recognizes an object it
knows, answers a spoken question with the stored frame, and is taught a new
object by showing and naming. Any score on its display is real output.

**NARRATION:**

Now watch the far end of the course, live. This robot watches the room,
detects objects, embeds them, and writes them to memory as it goes: the same
loop, at camera speed.

I'll show it something it knows. Watch: it's seen this before, and it says
so, with a score against a threshold. Now the other direction: where did you last see
a hat? The answer comes back with the frame it came from. And I can
teach it something new by showing it and naming it: one new memory in the
folder, no retraining.

That's lesson six, and every lesson on the way there builds one piece.

---

## Beat 10: WRAP, robot on set

Camera, no slide. Dylan cuts the robot's power and brings it back; it still
recognizes the object taught in beat 9. Network off throughout.

**NARRATION:**

Its network has been off this whole time. Now I'll cut the power and bring
it back. Watch: everything it was taught is still there, because the files
are.

Next lesson, we start where every memory starts. An empty folder, and a
question it can't answer yet.
