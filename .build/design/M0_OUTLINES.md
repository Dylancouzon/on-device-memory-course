# M0 — Design lock: per-lesson section outlines

Built against `.build/PLAN.md` (DLAI meeting, 2026-07-15). This is the spec M1–M5 build to. Dylan reviews this file; the build proceeds without blocking on sign-off per session instruction.

Conventions: every lesson's script opens with the endpoint-teaser beat (script + one slide). "Qdrant" is named in narration only when its API is on screen. Payoffs sit under `## N. The payoff: …` headings. Cleanup is invisible (helper). Collections are per-lesson.

## L1 — Why Devices Need Memory *(video-only, ~5 min, 16:9 slides)*

No notebook. `L1/` folder is deleted from the student repo. Script beats:

1. **INTRO / endpoint teaser** — the course endpoint up front: the finished assistant (and the L6 robot) recognizing what it was taught, recalling a day. "By the end you build this."
2. **Why memory can't live in the cloud** — privacy (a life log is the most personal data there is), offline (memory must work where you are), latency named without numbers (round trips vs in-process). One 16:9 slide: device vs cloud, cloud grayed/crossed per SLIDE_STYLE.
3. **What "memory" means for a device** — weights don't change; memory is the notebook the model keeps beside it. Write, read, filter, grow, forget. The course motif.
4. **The loop** — capture → embed → store → recall. One 16:9 slide: the loop diagram; each stage tagged with the lesson that builds it (course map).
5. **WRAP / robot footage teaser** — L6 finale footage: taught once, recognized from a new angle. "L2 starts with an empty store and one question."

Boundary: no chunking, no embeddings-from-scratch, no ANN/HNSW. Concept anchor: *memory formation* (what it is, why on-device).

## L2 — Store and Recall *(notebook, ~9 min)*

Old L1 + old L2 + forget. One question threads the lesson, asked four times: "where can I sit outside for a latte?" Collection: `coffee_shard`.

| § | Beat | Content |
|---|---|---|
| 1 | Ask before there's anything to remember | Richer setup absorbed from old L1: `EdgeConfig` (named vector `text`, 768, cosine), what a shard is (narration), `EdgeShard.create`. **Ask #1** → 0 hits. |
| 2 | The memories | The day's 20 text notes from `../data/memories.json`. |
| 3 | Turn notes into vectors, on the device | Nomic via helper. |
| 4 | Store the memories | `Point` + `upsert_points`, `optimize()` with the no-background-optimizer narration. |
| 5 | The payoff: ask again — now it remembers | Keyword scan for "latte" → 0 matches, then **ask #2** → café note (id 0) at ~0.653. The semantic-vs-keyword proof. |
| 6 | The payoff: recall with the network off | `no_network()` + standup question (kept from old L2 §6). |
| 7 | The payoff: how fast is local recall? | `add_filler` to 5,020, 200 queries, honest median on this CPU-only sandbox (kept in L2; L3 has no room). |
| 8 | The payoff: forget a memory | `delete_points([0])`, `optimize()`, **ask #3** → a different memory at a lower score; other food notes untouched ("exactly what you deleted, not every trace"). |
| 9 | The payoff: memory survives a restart — including what you removed | `close()` → list the shard directory (old L1's files-on-disk payoff lands here: the object is gone, the files remain) → `EdgeShard.load` under `no_network()` → **ask #4** → the forgotten note stays forgotten. Receipt table. |

Gears visual: before/after recall and forget (the four asks juxtaposed; `before_after` for ask #2 vs ask #3). Slide: anatomy of a point (kept). Concept anchor: *the memory lifecycle* — store → recall → forget → persist. Registry entries: cold-open 0 hits, ask #2 score, ask #3 top hit + score, restart receipt.

## L3 — Finding the Right Memory *(notebook, ~8 min)*

Old L3 + old L4 condensed. Cross-modal recall + one filtered-recall payoff. Cut: old L3 §1 model table (→ slide + narration), old L3 §8 side-by-side beat (never-merge policy moves into narration), old L4 time-window payoff, old L4 §1 metadata tour. Collection: `mem_shard`.

| § | Beat | Content |
|---|---|---|
| 1 | One shard, two named vectors | `EdgeConfig` with `text` 768 + `image` 512. Which-encoder-for-which-memory carried by the two-encoders slide + narration (Nomic and CLIP scores are never comparable, never merged). |
| 2 | Store text notes | Nomic, as in L2. |
| 3 | Store photos | First point by hand (image vector only), then the batch. `optimize()`. |
| 4 | The payoff: find a photo by describing it | "black and white sneakers" through CLIP's text tower → `image` vector. `show_photo_results` (query-beside-match = the gears visual). Cross-modal slide kept. |
| 5 | The photos on hand | `show_images` gallery before the your-turn. |
| 6 | Your turn: describe a photo | Editable `my_description`. |
| 7 | The payoff: recall with a filter | `create_field_index` (category, location, timestamp, price) + `optimize()`, then "somewhere to eat" + `Filter(must=[category=food, price<15])`, `before_after`. Filters-inside-the-query narration (no "faster" claim). |
| 8 | Your turn: filter weeks of history | Load `recent_days.json` (~102 notes) so the filter has weeks to sift; editable `my_category`, **category-only** (RangeFloat gotcha respected). |
| — | Reference | Filter-fields table (markdown, kept from old L4 §7). |

Concept anchor: *selective recall* — describe what you mean, constrain when/where/how much. Registry entries: sneakers score, cheap-food before/after lists.

## L4 — Your On-Device Assistant *(notebook, ~8 min)*

Old L5 minus forget, de-densified. The day only (no `recent_days.json`) — §9's added memory must win clearly. Collection: `day_shard`.

| § | Beat | Content |
|---|---|---|
| 1 | A day's captures | 42 captures; voice notes transcribed on-device (play clip → transcript). Whisper runs via one helper call that releases the model after transcription (RAM insurance before Nomic + CLIP load). |
| 2 | The day at a glance | `day_timeline`. |
| 3 | One shard, two named vectors | Config + `create_field_index` × 4. |
| 4 | Store the day | Two batch upserts (text, image) — the one-by-hand replays from old L5 are cut; L3 §3 already showed a point built by hand. Gallery after. |
| 5 | Inspect a stored point | `ScrollRequest`, one point, named vectors + payload. |
| 6 | How recall works | `recall()` built in the open (two `QueryRequest`s, one per space, same filter, grouped by modality). `show_raw` moves to helper (display plumbing, 50-50 shift). |
| 7 | The payoff: "black and white sneakers under $50" | Filter written out raw; `show_raw` then `memory_inbox` (the day's recall receipt = gears visual). |
| 8 | Your turn: ask a question | Editable `my_question` / `my_category`. |
| 9 | The payoff: add your own memory, then recall it | Spare-key note (id 900), upsert, recall wins (~0.757). |

Guard: the day's ramen voice memo (id 20) stays top-3 for "the ramen place downtown" (L5 capstone dependency). Concept anchor: *a full day, recalled as one assistant*. Registry entries: sneakers hits, add-own score.

## L5 — Teaching It to See *(notebook, ~11 min)*

Old L6 with a trimmed middle + the student capstone finale. Trims: old §9 one-view-is-enough folds into the teach/evidence beats; your-turn shortened. Camera on video only; students use bundled `data/objects/`. Collections: `object_shard`, then `assistant_shard`.

| § | Beat | Content |
|---|---|---|
| 1 | An object-memory shard | `image` vector only, `RECOGNIZE_THRESHOLD = 0.80`. |
| 2 | The objects on hand | `show_images` gallery, all six objects up front. |
| 3 | Teach what it already knows | `teach()` defined (embed views → one point per view, file path in payload). Teach lithops (2 views) **and backpack (1 view, with the SportsWorld note)** — "even one view is enough" narrated here (old §9 folded in). |
| 4 | Show it something new | `recognize()` defined; gaillardia held-out view → UNKNOWN, query beside closest known view. |
| 5 | Teach it the new object | Two gaillardia views, editable label. |
| 6 | The payoff: recognize it from a new angle | Same held-out view now above threshold, beside its matched view. |
| 7 | Inspect the threshold gap | Score bars taught-vs-foreign (new gears viz): gaillardia held-out + backpack_2 (one-view taught) above 0.80; never-taught scene photos below. `check_objects.py` gate unchanged; swap objects, never move the threshold. |
| 8 | Your turn: teach an object | duck / vase / hard-hat, teach 2 views, recognize the third. Shortened. |
| 9 | Assemble the assistant | One `assistant_shard` (text 768 + image 512): the full day + `recent_days.json` + teach the backpack again with its note. Nomic + CLIP together (proven budget). Voice text = `transcript` field (no Whisper here). |
| 10 | The payoff: ask it about your day | "the ramen place downtown" → cross-modal recall: photo + voice memo + text notes. |
| 11 | The payoff: show it what you taught | backpack_2 recognized (~0.86) → recalls its note: "I remember this." |
| 12 | The payoff: it all persists, offline | `close()` → `EdgeShard.load` under `no_network()` → both skills re-run. Receipt reads `hits["Voice Notes"][0]` (ramen top-3 guard). |

Concept anchor: *recognition — learning by writing memory, not retraining*, closing into "I built the whole thing." Registry entries: fail score, recognize score, gap chart values, backpack_2 score, capstone receipt.

## L6 — The Robot *(video-only, ~8 min, 16:9 slides)*

No notebook; `L6/` folder is deleted from the student repo. Deliverables: `design/L6/SCRIPT.md` (synthesis lecture), `design/L6/SHOTLIST.md` (production direction lives there, never in SCRIPT.md), 3–4 slide briefs (loop diagram, lesson-map, optionally threshold gap). Script beats:

1. **INTRO / endpoint payoff first** — the robot on camera: fails on an unknown object, taught once by voice, recognizes it from a new angle.
2. **The loop, mapped back** — capture → detect → embed → match → teach; each stage named with the lesson where students built it (mic→transcript ← L4; store/recall/forget ← L2; frame→embed→match ≥ 0.80 ← L5; cross-modal + unified recall ← L3/L4; one shard, two skills, offline reboot ← L5 capstone). The L5 assistant shard *is* the robot's memory architecture; L6 adds a camera and a mic.
3. **The two honestly-new pieces, narration-only** — detection (YOLOE crops objects; labels discarded; "detection finds *a thing*; memory tells it *which* thing"; one slide, black box) and when to form a memory (stability, cadence). Named, not taught.
4. **Teach by voice** — signature beat: show an object while saying "this is my mug"; image vector + spoken note land in one memory (L4 + L5 fused).
5. **"What did you see today?"** — recall of the robot's day; offline reboot close.
6. **WRAP** — course arc + public repo pointer. Stretch beat (fleet sync) only if wired; never faked.

Same stack claim holds: CLIP 512 / Nomic 768 / Whisper / threshold 0.80 — "the robot's memory code mirrors what you wrote."

## Repo/plumbing impact (M1)

- Delete `L1/` and `L6/` folders (notebook, helper, requirements). `gen_helpers.py` LESSONS: L2 `[embeddings, qdrant_helpers, viz]`, L3 same, L4 `+ audio`, L5 `[embeddings, qdrant_helpers, viz]`.
- `utils/audio.py`: transcription helper that releases Whisper after the pass.
- `utils/viz.py`: add `show_raw` (from old L5 cell) and a threshold-gap score-bar chart for L5 §7. Everything else carries over.
- No new student data. Café note id 0 is the L2 delete target; ramen voice memo id 20 is the capstone guard.
- README.md updated to the new lineup at M5.

## Deviations from PLAN.md (logged)

- L6 deliverables live at `design/L6/SCRIPT.md` + `design/L6/SHOTLIST.md` (existing per-lesson folder convention) rather than `design/L6_SCRIPT.md`.
- L2 keeps the latency payoff (§7): PLAN allows moving it to L3 for pacing, but merged L3 has no slack; L2 runs ~9.5 min — soft target, condense in edit.
- L2 §6 offline-recall beat kept (30 s): it is the on-device proof and the PLAN's §8/§9 numbering presumes §6–7 survive.
