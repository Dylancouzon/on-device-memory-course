# Course Restructure Plan — DLAI meeting, 2026-07-15

North star: **generalization**. Students should learn on-device AI memory as a concept and walk away feeling they learned the field, not a product. Qdrant Edge is *the implementation* — its calls stay visible because they map 1:1 to the concepts (store, query, filter, persist), but titles, narration, and slides lead with the concept.

## New lesson structure

### L1 — Why Devices Need Memory *(video-only, no notebook)*
- Instructor to camera; slides only where a visual earns its place. Slides are **16:9** (not the 8:9 notebook format), built on the same visual criteria as `SLIDE_STYLE.md`.
- Content: why memory can't live in the cloud (privacy, offline, latency), the capture → embed → store → recall loop, what "memory" means for a device.
- Ends with the endpoint teaser: footage of the L6 finale (robot/app recognizing what it was taught).
- Boundary: no re-teach of chunking, embeddings-from-scratch, or ANN/HNSW — prior-course territory. L1 theory is *on-device memory*, not vector search 101.

### L2 — Store and Recall *(old L1 + old L2 merged)*
- Absorbs old L1's setup as richer collection-creation detail: `EdgeConfig`, what a shard is, what lives on disk.
- Keeps the cold open (empty shard → 0 hits → store → 0.653 latte note) and the keyword-scan-vs-semantic proof — that beat *is* the generalization lesson.
- **Gains the forget beat** (`delete_points`, moved from old L5), designed as **one question threading the whole lesson**. The cold-open question is asked four times: §1 empty shard → nothing; §5 after storing → the café note (0.653); **§8 new** — delete the café note by id, `optimize()`, ask again → a different memory surfaces at a lower score, other food notes untouched ("exactly what you deleted, not every trace," carried from old L5 §10); §9 close → load, ask once more → the forgotten note stays forgotten after restart. Store → recall → forget → persist as one arc; the restart payoff upgrades to "including what you chose to remove." Third-ask top hit lands in the payoff registry at M5.
- Keeps `optimize()` narration and the persistence intro (close → load).
- Opens with the endpoint teaser beat (see cross-cutting).

### L3 — Finding the Right Memory *(old L3 + old L4 merged)*
- Keeps what's distinctive on-device: cross-modal CLIP search (text ↔ photo) and one filtered-recall payoff (`Filter`/`FieldCondition` + field index, price < 15).
- Cuts generic retrieval walkthroughs — DLAI already has a retrieval course; don't re-teach it.
- Keeps: photo gallery before the your-turn; `recent_days.json` your-turn (category-only filter, RangeFloat gotcha respected); L2's honest local latency number can move here if pacing needs it.

### L4 — Your On-Device Assistant *(old L5, de-densified)*
- The full day: on-device Whisper transcription (play clip → show transcript), unified recall, add-your-own.
- **Forget moves out to L2** — that's the density cut. L4 focuses on one thing: a whole day of multimodal memories, recalled as one assistant.
- Remaining plumbing pushed into `helper.py` (50-50 target).
- Guard stays: ramen voice memo in top-3 for "the ramen place downtown" (capstone dependency).

### L5 — Teaching It to See *(old L6, now the students' capstone)*
- Object teach / fail / teach / recognize, threshold-gap inspection, your-turn on duck/vase/hard-hat. Trimmed middle to make room: one-view-is-enough (backpack) folds into the teach beats rather than standing alone; your-turn shortened.
- **Ends with the student-built capstone** (old L6 §10–§11): one `assistant_shard` (text 768 + image 512) holding the full day + `recent_days.json` + the taught backpack; two payoff beats (ask about your day → cross-modal recall; show what you taught → recognition recalls the note); then close → reopen offline → both skills still work. This is the students' "I built the whole thing" moment — L6 then shows the same thing embodied.
- **Camera returns on video only:** instructor captures object views live on camera; the student path stays offline on the bundled `data/objects/` photos. No `ipywebrtc`, no sandbox risk.
- Gears outputs: similarity-score bars taught-vs-foreign, query-beside-match rendering (`viz.py` has the pieces).
- `RECOGNIZE_THRESHOLD = 0.80` logic and the check_objects gate carry over unchanged. Guard moves here: ramen voice memo stays top-3 for "the ramen place downtown" (the capstone receipt reads `hits["Voice Notes"][0]`). L5 now reads `recent_days.json` (capstone only) and loads Nomic + CLIP together at the finale (proven to fit the 4 GB budget).

### L6 — The Robot *(video-only, no notebook: the learnings, embodied)*
- **Video-only, like L1** — clean bookends: L1 "here's the idea," L2–L5 hands-on, L6 "here's the idea, embodied." Rationale: a notebook version would either limit the demo or be L5 again on canned frames; students already built the loop with their own hands, and their capstone now closes L5. 16:9 slides, same rules as L1.
- **Platform: a bespoke robot app**, using [`qdrant-labs/memory-fleet`](https://github.com/qdrant-labs/memory-fleet) as the reference/starting point (its capture→detect→embed→match→teach pipeline and two-shard store), rebuilt with **the course's exact stack**: CLIP for image (512-d), Nomic for text (768-d), Whisper for audio→text, Qdrant Edge, `0.80` threshold. Same models, same dims, same calls as the notebooks — the honest claim upgrades from "same concept" to "the robot's memory code mirrors what you wrote." (Old embedder-mismatch caveat deleted.)
- **Audio is a first-class input:** mic → Whisper → text → Nomic, exactly L4's pipeline. Signature beat: **teach by voice** — show the robot an object while saying "this is my mug"; image vector + spoken note land in one memory. That's L4 + L5 fused in one interaction.
- **Coherence map (each robot stage ← the lesson that built it):** mic→transcript ← L4; store/recall/forget ← L2; frame→embed→match ≥ 0.80 ← L5; cross-modal + unified recall ← L3/L4; a filtered "what did you see today?" ← L3; one shard, two skills, offline reboot ← L5 capstone. The L5 assistant shard *is* the robot's memory architecture; L6 adds a camera and a mic.
- **The two honestly-new pieces are narration-only:** (1) detection — YOLOE finds and crops objects in a cluttered frame before embedding; off-the-shelf, labels discarded ("detection finds *a thing*; memory tells it *which* thing"), one slide, black box; (2) when to form a memory — continuous capture, stability tracking, cadence. Neither gets taught; both get named. Respects the don't-re-teach boundary.
- **It teaches, not tours.** The video walks the loop and maps each stage back to the lesson where students built it themselves. A synthesis lecture that happens to have a robot.
- **On camera:** unknown object → fails → taught once (by voice) → recognizes it from a new angle; asked about its day → recalls what it saw and heard. Stretch beat only: fleet sync via Edge synchronization to a Cloud collection ("one unit learns, all units know") — no longer free without memory-fleet proper; wire it or cut it, never fake it. Close with the public repo pointer.
- **Hardware: Jetson Orin Nano 8 GB** (~$250 dev kit, battery-powerable, camera header, 3D-printed case, full YOLOE rate with TensorRT). A Pi has no GPU for detection. If the bespoke build simplifies perception ("center the object, press teach" instead of live tracking), a Pi becomes feasible — but live detection is what makes it read as a robot.
- **Scope deleted by going video-only:** `data/robot/`, the session exporter, the data contract, and the synthetic-session notebook work are all cancelled. Hardware no longer blocks any notebook. **Scope added:** the bespoke robot app itself (fork/strip memory-fleet: swap Unicom→CLIP, add mic + Whisper + Nomic text memories).

## Cross-cutting changes (all lessons)

1. **Endpoint teaser:** every lesson opens with a short "here's the finished thing, today we build this piece" beat — script beat + one slide. Keeps eagerness, costs minutes.
2. **50-50 code/abstraction:** move non-essential plumbing (viz, galleries, filler, cleanup, model loading boilerplate) into `helper.py`. Qdrant Edge calls stay on the page — non-negotiable, they are the curriculum.
3. **Cleanup hidden:** no visible teardown ceremony. Each lesson builds its collection once (helper handles fresh-start) and reuses it for the whole lesson. Collections stay **per-lesson**: students jump into lessons out of order and re-run with fresh kernels, so a shared cross-lesson collection is fragile. Revisit only if DLAI confirms guaranteed sequential persistent state (open question below).
4. **Generalization is a language rule, not a content change.** Scripts and slides talk about vector search and on-device memory; "Qdrant" is named when its API is on screen, otherwise it's "the shard," "your memory," "the index." One concept anchor per lesson (memory formation → selective recall → a full day → recognition → embodiment). Enforced in the script-review pass.
5. **One signature "gears" visual per lesson:** L2 before/after recall (and forget), L3 query-photo-beside-match, L4 the day's recall receipt, L5 threshold-gap chart + the capstone receipt, L6 the robot's live memory map on camera. Visible machinery, not just result tables.
6. **Minute budgets (soft targets, tune after recording):** L1 ~5, L2 ~9, L3 ~8, L4 ~8, L5 ~11, L6 ~8 ≈ 49 min. Over is fine per DLAI; condense in edit.

## Open questions for DLAI

1. **L6: bespoke robot, video-only.** Remaining: DLAI sign-off, hardware purchase (Jetson Orin Nano 8 GB + battery + camera + case), the bespoke app build (fork/strip memory-fleet: CLIP + Nomic + Whisper), TensorRT export test, and shoot logistics. No notebook depends on the hardware anymore.
2. Does the platform guarantee a **persistent filesystem and sequential lesson order**? Determines whether one shared collection is even safe. Default: per-lesson.
3. Are **video-only L1 and L6** (no notebooks) acceptable in their format?
4. Existing open item: container outbound network / baking ONNX weights into the image.

## Repo impact

- `L1/` notebook retired → L1 becomes slides + script only (`.build/design/L1_SCRIPT.md`, 16:9 slides).
- `L2/` absorbs old L1 setup content + forget; `L3/` rebuilt from old L3+L4; `L4/` ← old L5 minus forget; `L5/` ← old L6 (trimmed middle + capstone finale); `L6/` notebook retired — slides + script only, like L1.
- No new student data needed; `data/robot/` cancelled.
- `gen_helpers.py` mapping updated for the new lesson lineup; more `utils/` modules per lesson (50-50 shift).
- All scripts get the endpoint-teaser beat; all slides re-checked; L1 slides 16:9.
- Guards that must survive the shuffle: ramen memo top-3 (now an L5-internal coupling), threshold gap gate (`check_objects.py`, now L5), RangeFloat gotcha (now L3).

## L6 deliverables (video-only)

- `.build/design/L6_SCRIPT.md`: synthesis lecture — endpoint payoff first, capture→detect→embed→match→teach walk with each stage mapped to the lesson that built it, teach-by-voice beat, offline-reboot close.
- 16:9 slides (3–4 max): loop diagram, lesson-map diagram, optionally the threshold gap. Instructor on camera is the default.
- `.build/design/L6_SHOTLIST.md`: demo beats to capture (fail → teach by voice → recognize new angle → "what did you see today" → reboot offline). Production direction lives here, never in SCRIPT.md.
- Bespoke robot app: separate repo, instructor-side, never shipped. Student repo ships nothing for L6.

## Style continuity (binding for the rebuild)

- **Notebook shape unchanged:** short cells, few lines each, near-zero prose — the 50-50 shift means *fewer plumbing cells and richer outputs*, not a different format.
- **Narration:** new scripts must read as the same author as the existing SCRIPT.md files — same voice, verbosity, vocabulary. Match against existing scripts, don't restyle.
- **Slides:** outside L1/L6, a slide exists only when a concept needs visualizing. Default is code + narration.

## Execution plan (one long build session)

- **M0 — Design lock (no code before this):** per-lesson section outlines. Forget-beat design: done (see L2). Model loading: decided — **Nomic + CLIP load together** (verified by the old L6 capstone); L5 releases Whisper after transcription before the capstone as cheap insurance; all-three-at-once gets checked on the sandbox at M5. Dylan signs off on M0.
- **M1 — Plumbing:** `.build/utils` updates (gears viz, any forget/cleanup helpers), `gen_helpers.py` mapping for the new lineup.
- **M2 — Notebooks L2→L3→L4→L5 in order.** A lesson is done when it runs Restart-&-Run-All clean and its payoff-registry entries verify. L5 last — it depends on everything.
- **M3 — Scripts:** all SCRIPT.md rewritten (new numbering, endpoint teasers, generalization language rule, same authorial voice).
- **M4 — Slides:** audit existing 8:9 set, new only where a concept needs it; L1 + L6 16:9 sets.
- **M5 — Full verify:** Restart & Run All L2→L5; **compute the payoff registry from the executed outputs** (every quoted score/output, its section, its guard — cold-open recall, third-ask top hit, add-own score, backpack recognition, ramen top-3, threshold gap) and reconcile scripts against it; ramen guard; `check_objects.py`; all-three-models RAM check; then rewrite CLAUDE.md design notes to the new numbering and drop the restructure banner.
- **M6 — Independent review, two stages:** (1) a **fresh-context Sonnet subagent** runs `.build/design/REVIEW_PLAN.md` end-to-end and produces `REVIEW_FINDINGS.md`; builder fixes blockers/majors; (2) **Codex pass** on quality, content, logic, and narration voice; fix pass; final run.
- **Separate track (not in the session):** robot app build + Orin Nano purchase + shoot. Blocks only L6 script finalization and the shoot, nothing else.

## Build orchestration

- **Fable orchestrates and owns design-sensitive work** (notebook beats, scripts, cross-lesson invariants) — but Fable is expensive: delegate everything bounded and spec-tight, keep only design judgment. When in doubt, write the spec and hand it down.
- **Opus/Sonnet subagents for bounded work:** executing notebooks, payoff verification, image/license checks, slide rendering, mechanical rewrites against a locked spec. **Subagents may not spawn subagents.**
- **The L6 robot app gets dogfooded by cheap models** — drive it, try to break it, review recorded videos of sessions. Reference implementation lives locally at `../hive-mind` (memory-fleet).
- **Codex as end-of-line independent reviewer** (M6): quality, logic, narration voice.
- **Dylan's gates:** M0 outlines, per-lesson payoffs at M2, final at M6.

## Decision log

| Decision | Status |
|---|---|
| Generalization framing course-wide | ✅ Decided |
| L1 video-only theory, 16:9 slides, endpoint teaser | ✅ Decided |
| Old L1 merged into L2 | ✅ Decided |
| Old L3+L4 merged into new L3 | ✅ Decided |
| Old L5 → L4; old L6 §1–9 → L5 | ✅ Decided |
| Forget/delete moves from old L5 into L2 (memory lifecycle) | ✅ Decided |
| L6 = **bespoke robot** (memory-fleet as reference; course's own CLIP/Nomic/Whisper stack, audio + image), **video-only** (no notebook) | ✅ Decided; hardware (Jetson Orin Nano) + DLAI sign-off pending |
| Student capstone (assistant shard + offline reopen) moves to end of L5 | ✅ Decided |
| Generalization = language rule (Qdrant named when API on screen) | ✅ Decided |
| Minute budgets are soft targets; condense after recording | ✅ Decided |
| L2 forget = four asks of the cold-open question (nothing → note → forgotten → stays forgotten) | ✅ Decided |
| Nomic + CLIP load together; Whisper released after transcription; registry computed at M5 | ✅ Decided |
| Fable orchestrates w/ strict delegation; no nested subagents; cheap models dogfood the robot app | ✅ Decided |
| Camera: video demo + bundled frames, student path stays offline | ✅ Decided |
| Cleanup hidden in helper; per-lesson collections | ✅ Decided (revisit if DLAI confirms persistent state) |
| 50-50 code/abstraction | ✅ Decided |
