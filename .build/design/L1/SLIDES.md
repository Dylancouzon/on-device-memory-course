# L1 slides, for Claude Design

Seven 16:9 slides for Lesson 1 of a DeepLearning.AI short course, "Building
On-Device AI Memory with Qdrant Edge". You get three things: this file,
`SCRIPT.md` from the same directory, and the asset pack. There is no repo
access, and none is needed.

**Read the script first.** It carries the narration word for word, and the
narration is what each slide has to illustrate. This file gives you the style,
the assets, the verified numbers you may put on screen, and the one idea each
slide owns. The composition is yours: pick the diagram that teaches that idea
fastest, with the least text on screen. Where the script and this file
disagree about wording, the script wins.

Design for a technical audience. Every label should name a real component, a
real field, a real dimension, or a real score, so a developer pausing the video
learns something from the picture alone. A slide that could be replaced by a
sentence of narration is not worth building.

Deliverable: seven slides in the order below, plus an editable source for
`l1-05-the-loop`, which later lessons reuse with stages dimmed.

## What We're Looking For

The taste to design against, before any specific slide:

- **Graphically simple, technically concrete.** A student who pauses the video
  should learn something from the picture alone. Simple means few elements, not
  vague ones: every label names a real component, field, dimension, or score.
- **One idea per slide, held in one glance.** No slide argues two things. If a
  second idea needs a picture, it belongs to a different slide or to the
  narration.
- **The least text that still teaches.** No titles, no headlines, no bullet
  lists, no sentences to read aloud. The presenter is already saying the
  sentence.
- **The hand-drawn flowchart language below is the house look.** Wobbly
  strokes, soft semantic fills, curved arrows, mono type for literal
  identifiers. Consistent, not clip-art: no stock icon sets, no gradients, no
  drop shadows, no 3D, no stock photography, no decorative emoji.
- **Never draw a fake interface.** Captures of real output are welcome and get
  a caption saying what they are. A drawn mockup of an app screen, a fabricated
  result row, or an invented number is the one thing that sinks a slide.
- **Diagram the concept, name the product once.** The course teaches on-device
  AI memory as a general idea, and Qdrant Edge is the implementation of it, so
  prefer "the memory", "the shard", "the index" on labels, and name Qdrant
  where the product itself is the subject, which is slide 7.
- **Qdrant is a vector search engine.** Never write "vector database" anywhere,
  on a slide or in a file name.
- **Accessibility is part of the design.** 18 pt floor, contrast that survives
  a projector, and color as a supporting cue rather than the only one: anything
  the palette distinguishes should also be distinguishable by label, shape, or
  position.
- **Ask rather than invent.** If a slide seems to need a value, a string, or an
  asset that is neither in this file nor in the script, leave the space empty
  and flag it instead of filling it in.

## How These Slides Get Used

Each slide comes up under the narration it belongs to and drops away after it.
A presenter stands beside it, with a real robot in shot. Four beats cut from
the slide to the robot's own screen partway through (beats 3, 4, 5, and 8), so
each slide holds one idea and stays readable in a glance rather than building
toward a second point. Slide 5 is the exception: its four tiles may appear one
at a time.

The presenter says the sentences. The slide shows the mechanism.

## Style: The DLAI Short-Course Template

- **16:9, light theme:** white background `#FFFFFF`, dark ink `#111824` for
  text and strokes, secondary text `#656B7F`. Never a dark background.
- **Minimum font size 18 pt** for every text element, labels and scores
  included. Nothing smaller, ever.
- **Logos on every slide:** Qdrant top-left (dark-ink asset, in the asset
  pack), DeepLearning.AI top-right (part of the template), both ~1.3" wide
  with ~0.15" outer margins, balanced by visual weight.
- **Footer:** the template's red/maroon decorative wave runs across the
  bottom edge; keep content clear of it.
- **Hand-drawn flowchart language:** nodes are rounded rectangles with a
  slightly wobbly stroke and a soft fill of their stage color at 12–18%
  opacity with a solid stroke of the same color; each node carries a small
  concrete icon plus a 2–6 word label. Containers are larger dashed-border
  rounded boxes. Databases are hand-drawn cylinders. Arrows are curved and
  hand-drawn. Mono-spaced type for literal identifiers
  (`edge_config.json`). The course motif is a small hand-drawn spiral
  notebook icon, reused wherever memories are written or recalled.
- **Palette, semantic and consistent:** capture/input light blue `#03A9F4`;
  embedding/models orange `#FF9800`; storage/persistence violet `#6047FF`;
  query/recall Qdrant red `#DC244C` (accent only, never a large fill);
  results/success teal `#009688`; cloud/network (the thing being beaten)
  desaturated gray `#4E5366`, struck through with a hand-drawn ✕ where the
  idea calls for it.
- **Copy rules:** a slide is a picture, not a sentence to read. No titles, no
  headlines. Sentence case. "·" as separator. If a text element does not name
  a part of the diagram, cut it. No em dashes anywhere.
- **Consistency across the seven:** the encoder node, the memory cylinder, and
  the device container appear on more than one slide. Draw each one the same
  way every time, so a student reads them as the same component.

## Asset Pack

- Qdrant dark-ink logo (wordmark renders in `#111824`).
- `bicycle.jpg`: the course's red bicycle photo.
- `l4-inbox-crop.png`: a finished crop of the course's memory inbox answering
  one question with a photo, a voice note, and a text note. Already cropped
  and re-set; place as supplied.
- `robot-still.png`: the course robot on set, on a shelf indoors.
- `render-mine-inspection.png`, `render-search-rescue.png`: artistic renders.

Honesty rules, non-negotiable: each capture carries a small teal `#009688`
caption naming what it is and where it came from; each render carries a small
gray `#4E5366` "illustration" label at 18 pt in its bottom-left corner, and
gains nothing else, no interface elements, no result rows, no numbers.

## Numbers You May Use

Real output from the course's encoders. Use them exactly as printed. Never
invent, round, or improve a number, and never put a number on a slide that is
not in this list or in the script.

| Value | What it is |
|---|---|
| 768 | text vector dimensions (`nomic-embed-text-v1.5`, fastembed 0.8.0) |
| 512 | CLIP ViT-B/32 shared image and text dimensions |
| `[ 0.75  0.79  -4.32  … ]` | the first components of the real vector for "flat white on the terrace" |
| 0.476 | "where can I sit outside for a latte?" vs "flat white on the terrace" |
| 0.372 | the same question vs "dentist at 4" |
| 0.366 | the same question vs "new running shoes" |
| 165 | photos in the lesson-three image bank |
| `edge_config.json`, `segments/`, `wal/` | the three things in a shard directory |

Text scores in this lesson come from documents embedded as documents and the
question embedded as a query. A score means something only against other
scores from the same model, which is a rule the narration states out loud, so
never draw a text score and an image score in a way that invites comparison.

## The Seven Slides

Each row gives the file slug, the narration it plays under (find the full
wording in `SCRIPT.md`), and the single idea it has to land. What the picture
looks like is your call.

### 1 · `l1-01-note-to-vector`

Plays under beat 2, from "So it runs them through an embedding model" to
"Neighbors anyway."

Idea: an embedding model turns one note into a fixed-length list of real
numbers, and two notes that mean the same thing land close together even with
no words in common. The two notes are "flat white on the terrace" and "coffee
outside on the patio".

Watch out: three components out of 768 cannot show closeness, so digits prove
the vector is real while position has to carry the similarity.

### 2 · `l1-02-nearest-and-scored`

Plays under beat 3, from "So search is one question" to "no shared words."

Idea: retrieval itself. The question goes through the same encoder as the
notes, the stored notes get ranked by closeness, and each result carries a
score. Keyword matching on the same three notes returns nothing.

The three scores above are the whole point, so they belong on screen. The
keyword failure is the smaller half of the slide.

### 3 · `l1-03-photos-and-words`

Plays under beat 4, from "A model like CLIP has two halves" to "come out as
neighbors."

Idea: two encoders, one shared space of 512 numbers, so a photo and a
description of it land near each other. This is what makes searching photos
with a sentence work, and later makes image-to-image recognition work.

Use `bicycle.jpg` and the phrase "a red bicycle".

### 4 · `l1-05-the-loop`

Plays under beat 5, from "Line the pieces up" through the forget sentence.

Idea: capture, embed, store, recall, as one closed loop, with forget hanging
off the store step and the index sitting under it. Stored alongside each
memory: the original, its vector, and its details.

Two hard requirements. This drawing is the lesson-one sibling of a slide every
other lesson reuses, so deliver an editable source where stages can be dimmed
individually and the forget tag and sub-label can be removed. And keep it free
of lesson tags.

### 5 · `l1-04-where-it-matters`

Plays under beat 6, one tile per sentence: the wearable, the robot in the
room, inspection robots in mines and tunnels, search and rescue.

Idea: four settings where the memory has to answer on the machine itself. All
four assets are in the pack and none of them get embellished. Tiles may appear
one at a time in that order, then hold as a grid.

This is the only slide built from photography rather than drawing, so the
honesty labels above are the design, not decoration.

### 6 · `l1-06-on-device`

Plays under beat 7, from "Every one of those machines runs the same design" to
"Recall is a function call."

Idea: the architecture of the whole course. The encoders and the memory live
inside one application process on one device, a question is answered without
leaving it, and the network path is drawn as what it would have cost: your data
uploaded, and coverage required. The local path should be visibly shorter than
the network path.

Beat 7 then names three consequences out loud (privacy, coverage, cost). They
stay spoken. Do not put them on the slide.

### 7 · `l1-08-memory-is-a-folder`

Plays under beat 8, from "On disk, all of this is a folder" to "No server, no
account."

Idea: the memory is a directory of ordinary files, managed by a library inside
the application's own process. The three entries and what each holds are in the
numbers table. Qdrant Edge is named on this slide.

Watch out: the absent server and account are absent from the picture too, and
nothing crosses a process boundary.

## Two Things To Get Right

**Technical depth beats decoration.** If a choice is between one more decorative
element and one more real label, take the label. Every score, dimension, and
file name on these slides is verifiable, and students will pause the video.

**Text is expensive.** The narration is already saying the sentence. Cut any
word on screen that the picture or the presenter already carries.
