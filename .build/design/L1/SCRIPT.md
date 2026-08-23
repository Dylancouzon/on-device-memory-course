# L1: Why Devices Need Memory (script)

**Target runtime:** ~7 min
**Format:** video only, no notebook.

**Objective.** Give the student the vector search toolbox the course uses
(vectors, similarity scores, one shared space for photos and text, the
store/recall/forget lifecycle), make the use cases land (wearable, a robot
in the room, offline robots, search and rescue), show the architecture that
puts
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
  under-weighted): four settings on one montage slide, wearable (real L4 §7
output), the robot in the room (course robot still, one unit per room),
offline inspection robots and search and rescue (Dylan's renders,
"illustration" labeled), plus the robot live in beats 1 and 9.

**The robot is in every beat** (Dylan's call, 2026-08-19): the machine is the
product students are working toward, so each slide beat cuts to the robot's
own panel showing the thing that slide just explained. Beat 3 shows its recall
answer, beat 4 one memory card with its photo and taught sentence, beat 5 the
live feed writing memories while Dylan talks, beat 8 its folder on disk. Those
cutaways are the robot's real screen, never a mock, and they carry no code: a
panel, a card, a feed, and a file listing. **Principle.** Memory lives on the
device as plain files managed directly by the application. Qdrant Edge
provides this as an embedded shard running
inside your application, with no server or account required.

Slides are **16:9**, one per slide beat, **specified in `SLIDES.md` in this
directory**: the self-contained handoff for the design agent (Claude
Design), carrying the style capsule, the asset pack list, the baked-in real
encoder values, and all seven briefs. This script names only which slide
plays under each beat. A slide comes up under the sentence it illustrates
and drops away after it; the camera (and the robot) is the default shot. No
latency numbers appear in L1 (the course shows latency exactly once, in
L2 §6), and every number on a slide is real encoder output, baked into
SLIDES.md; recompute only if the embedding-model pins change.

**Vocabulary.** L1 now owns the course's words: vector, embedding model,
similarity score, details (payload), index. Each is defined in the beat
that first uses it, then used without apology for the rest of the course.
Filters are named once in beat 5 and defined properly in lesson three. No code
appears on screen. Internals stay out: how the embedding
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

The seven slides (briefs in `SLIDES.md`):

| Slug | Idea | Status |
|---|---|---|
| `l1-01-note-to-vector` | A note becomes 768 numbers; similar meaning, nearby vectors | New |
| `l1-02-nearest-and-scored` | The question ranked against three notes, real scores, keyword miss beside it | New |
| `l1-03-photos-and-words` | CLIP: image and text meet in one 512-number space | New |
| `l1-05-the-loop` | capture → embed → store → recall (+ forget) | Revised from `l1-03-the-loop` |
| `l1-04-where-it-matters` | Four use-case tiles: wearable, the robot in the room, offline inspection, search and rescue | New (replaces `l1-04-memory-record`, cut with the filter beat) |
| `l1-06-on-device` | Architecture: encoders + memory in-process, network path struck out | Merged from `l1-01`/`l1-04` of the prior version |
| `l1-08-memory-is-a-folder` | The shard is a directory in your process | Kept |

`l1-05-the-loop` stays the 16:9 sibling of `l2-00-endpoint` (brief in
`.build/design/L2/SLIDES.md`), drawn from the same source file, all four
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
| 1 | The robot answering "when did you last see my water bottle?" | Live on set | L1 shoot; blocking in `L6/SHOTLIST.md` |
| 6 | Four use-case tiles: L4 §7 inbox, course robot still, mine/tunnel inspection, search and rescue | Captures + renders | `L4/Lesson4.ipynb` §7 executed output; L1/L6 shoot; Dylan's renders |
| 9 | Potato taught by voice, recognized, then recalled by question | Live on set | L1 shoot; blocking in `L6/SHOTLIST.md` |
| 10 | The robot after a power cut, still knowing Potato, network off | Live on set | L1 shoot; blocking in `L6/SHOTLIST.md` |
| 3 | Cutaway: the recall answer on the robot's panel | Live on set | L1 shoot
| | 4 | Cutaway: one memory card, photo and taught sentence | Live on set | L1
shoot | | 5 | Cutaway: the live feed, boxes and scores updating | Live on set
| L1 shoot | | 8 | Cutaway: the robot's own folder on its screen | Live on set
| L1 shoot | | 2–5, 7–8 | Diagrams | Drawn | Briefs and style capsule in
`SLIDES.md` |

Anything on the robot's own display during the live beats is real output
from the machine; nothing staged goes on its screen. Captures keep the small
teal caption naming them.

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---:|
| 1 | INTRO, robot on set | The problem, the robot's answer, why now | 58 |
| 2 | SLIDE 1 | A note becomes a vector | 45 |
| 3 | SLIDE 2 + robot | Search, scores, and the score-scale rule | 64 |
| 4 | SLIDE 3 + robot | Photos and words in one space; two vectors on one memory | 63 |
| 5 | SLIDE 4 + robot | The lifecycle loop, plus forget and the index | 54 |
| 6 | SLIDE 5 | Where it matters: four use cases | 49 |
| 7 | SLIDE 6 | The on-device architecture and its three consequences | 42 |
| 8 | SLIDE 7 + robot | The same architecture on disk: a folder | 35 |
| 9 | ROBOT, live demo | The end of the course: teach Potato, recognize, recall | 55 |
| 10 | WRAP, robot on set | Power cut, memory intact; then L2 | 17 |

Total: ~482 sec (~8 min 2 sec) at 156 words per minute, 1,253 words of
narration. Budgets are counted from the narration below; re-count after any
edit. That is 62 seconds over DLAI's 7 minutes, and delivery on camera with a
live robot runs longer still. The overrun buys the robot: beats 1, 9, and 10
are live, and four slide beats cut to its panel. Trim order, in this order:
beat 6's harder-rooms pair, beat 4's photo-search sentence, then beat 7's cost
consequence. The cutaways in beats 3, 4, 5, and 8 stay, and so does beat 4's
recognition sentence, which beat 9's score against the bar depends on. Beats 2
and 3 (retrieval 101), the four use-case tiles in beat 6, and beat 9's demo
(the end of the course) are never cut.

---

## Beat 1: INTRO, robot on set

Camera, no slide. The robot sits on a shelf in frame from the first second,
the way it lives in the room. The water bottle was set down somewhere in the
room earlier and the robot saw it there. Partway through, Dylan asks when it
last saw the bottle, and it answers on its own panel with a time, the room,
and the photo it took. The hat he is wearing is taught too, so it is the
backup object if a bottle take goes wrong. Its stack is detection, CLIP,
Nomic, and Whisper, with no language model anywhere, so the narration's no-LLM
claim is literal: the answer is a lookup.

**NARRATION:**

Where did you leave your water bottle?

Nobody can answer that. Not your phone, not your laptop, not the biggest model
on the internet. None of them were in the room when you put it down. This one
was. It sits on that shelf and watches the room all day.

When did I leave my water bottle? 

A time, the room, and the photo it took. It was never trained on my bottle,
and there's no language model on it. It saw the bottle once, wrote it down,
and just found the note again. Nothing generated that answer, it came out of a
search.

Here's why this is suddenly worth building. Models that see a picture or hear
a sentence now run on hardware this small. The model is no longer the hard
part. The memory is.

That's what we build, and we end right back here. Today is the toolbox.

---

## Beat 2: SLIDE 1, a note becomes a vector

Slide: `l1-01-note-to-vector` (brief in SLIDES.md).

**NARRATION:**

The robot answered that from a picture. The second lesson today start simpler, with the
smallest memory a device can hold: a note you type on your phone. "Flat white
on the terrace." All the device can do is match words. So it
runs them through an embedding model, a small neural network with one job: turn
text into a vector, a list of numbers. Ours returns 768 of them.

Read any single number and you learn nothing. The meaning is in where the
vector lands.
Notes that mean similar things come out close together, and unrelated notes
come out far apart. "Flat white on the terrace", and "coffee outside on the
patio". Not one shared word. Neighbors anyway.

---

## Beat 3: SLIDE 2, search, scores, and the score-scale rule

Slide: `l1-02-nearest-and-scored` (brief in SLIDES.md). Robot cutaway on the
last line: the recall answer from beat 1 back on the panel, the question at
the top and the sightings under it, best match first.

**NARRATION:**

Put a handful of notes like that in memory, then ask a real question: where
can I sit outside for a latte? The question goes through the same embedding
model and becomes a vector too. Same space, same rules.

So search is one question: which stored vector is closest? Compare the
question against every one of them and take the nearest, each with a
similarity score. Higher means closer in meaning. The terrace note wins at
0.476, and the other two trail far behind. A keyword search over these same
notes returns nothing: no shared words.

That's retrieval, and every lesson here is built on it. It's also what the
robot just did with my bottle: one question, every note it has, best match
first.

One rule about scores. A score only means something inside its own model's
space. One is the ceiling, and a strong text match for our model lands well
under it. Image models run in a different range. Every lesson names its own.

---

## Beat 4: SLIDE 3, photos and words in one space

Slide: `l1-03-photos-and-words` (brief in SLIDES.md). Robot cutaway on the
last two sentences: the memory tab, one card held in frame, its photo and its
taught sentence and its sighting count all visible.

**NARRATION:**

Text is half a day. What about everything you see?

A model like CLIP has two halves, trained together: one embeds images, one
embeds text, and both land in the same space of 512 numbers. So a photo of a
bicycle and the phrase "a red bicycle" come out as neighbors.

That means you can search photos with a sentence. Embed the words, return the
nearest image vectors. No tags, no captions. This is what we're going to do in 
Lesson 3

The same space also compares two photos, a new one against a remembered one.
Close enough, past a threshold you pick, and that's recognition. It's how this
robot decides it has seen something before.

And one memory can carry both vectors, the words and the picture. One moment,
two ways back to it. On the robot that's one card: the photo it kept, the
sentence I taught it with, and how many times it has seen the thing since.

---

## Beat 5: SLIDE 4, the lifecycle loop

Slide: `l1-05-the-loop` (brief in SLIDES.md). Robot cutaway on the second
line: the live feed, boxes and scores updating on objects around the room
while Dylan keeps talking.

**NARRATION:**

Line the pieces up and you get the loop this whole course walks. That robot is
running it right now, so watch its screen while I talk: boxes appear, scores
update, memories get written.

Something happens in the room and it gets captured: a photo, a voice note, a
line of text. The encoder turns it into a vector, on the device. Into the store
it goes, with plain details attached, a category, a time, a room; lesson three
turns those into filters. Later you ask in your own words, and it comes back.

Then forget, the verb people skip. A memory you can't delete from isn't yours.
Take out one note, and only that note. Lesson two teaches all three: store,
recall, forget.

Under store sits an index, so search stays quick once the notes run into the
thousands.

---

## Beat 6: SLIDE 5, where it matters

Slide: `l1-04-where-it-matters` (brief in SLIDES.md).

**NARRATION:**

So why does the memory have to live on the device? Look at where this is
going.

Glasses and earbuds that see and hear your whole day, and answer "where did I
leave my badge?" out of a memory that never left your pocket. You build that
assistant in lesson four. One robot like this one on a kitchen shelf, another in
the workshop, each remembering its own room, answering "who moved the car
keys?" with no camera feed of your home leaving it. Then the harder rooms.
Inspection robots in mines and tunnels, with no signal to call home to. And
search and rescue, indexing everything the drones see in terrain with no
coverage at all.

Four machines, one requirement. The memory answers here, and now.

Add reasons: Privacy, cost, performance, speed, ect.... Map those use cases. Why are we using on device.

---

## Beat 7: SLIDE 6, the on-device architecture

Slide: `l1-06-on-device` (brief in SLIDES.md).

**NARRATION:**

Every one of those machines runs the same design: the architecture of this
whole course, and of the robot on that shelf. The embedding models and the
memory live inside your application's own process. A question comes in, gets
embedded, gets matched, comes back answered, and never touches a network.
Recall is a function call.

Three things fall out of that. Privacy: your day stays on the machine, with no
copy on anyone else's disk. Coverage: it answers with the network gone. And
cost: a memory you hit on every question and every camera frame can't pay for
a round trip. Lesson two puts a number on that.

---

## Beat 8: SLIDE 7, the same architecture on disk

Slide: `l1-08-memory-is-a-folder` (brief in SLIDES.md). Robot cutaway on the
last line: the robot's own folder listed on its screen, the three entries
visible, then back to the machine on the shelf.

**NARRATION:**

On disk, all of this is a folder.

Qdrant Edge is the embedded build of Qdrant's vector search engine. It runs
inside your process, and it keeps three things in that directory: a config
file with the settings, segments holding every vector with its note and its
details, and a write-ahead log of recent writes. No server, no account. Kill
the process and start it again, and everything is still there, because the
files are. That folder is on the robot behind me, and it holds everything the
machine knows.

---

## Beat 9: ROBOT, live demo

Camera, no slide. Teach, recognize, recall, on one object, on the robot's own
panel. Potato the cat plushie enters the frame as an unknown box with no name;
Dylan holds TEACH and says "this is Potato"; Potato leaves the frame and comes
back, and the panel names her with a real score against the bar; then he asks
out loud when it last saw Potato and it answers with a time, the room, and the
frame. Any score on its display is real output.

**NARRATION:**

Now the far end of the course, live. It watches its room, detects objects,
embeds them, and writes them down with the time and the place attached.

This is Potato, my cat plushie. Right now the robot has never seen her: a box
around her, and no name on it.

So I hold the button and I name her out loud: this is Potato. No detector has
a word for Potato, and it doesn't need one.

Potato goes away. Potato comes back. Watch the score clear the bar: she is
recognized, out of a memory that is twenty seconds old. The model on that
machine never changed. One write.

And now I can ask it. When did you last see Potato? A time, the room, and the
frame it came from.

That is lesson six, and everything before it builds one piece of it.

---

## Beat 10: WRAP, robot on set

Camera, no slide. Dylan cuts the robot's power and brings it back; it still
recognizes Potato, taught in beat 9. Network off throughout.

**NARRATION:**

Its network has been off this whole time. Now watch me cut its power.

Back up, and it still knows Potato, because the files are still there.

Next lesson, we start where every memory starts. An empty folder, and a
question it can't answer yet.
