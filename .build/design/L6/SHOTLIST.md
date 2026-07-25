# L6 — The Robot — shotlist

Production direction for the L6 demo beats. The script (`SCRIPT.md`)
carries narration only; every camera and staging note lives here.

**Hardware:** Jetson Orin Nano 8 GB dev kit, battery pack, CSI camera,
USB mic, 3D-printed case. The bespoke app (memory-fleet fork on the
course stack: CLIP 512-d, Nomic 768-d, Whisper, Qdrant Edge, threshold
0.80) must be feature-complete before the shoot.

**Screen capture:** every beat needs a synchronized capture of the
robot's live view (camera feed + detection crop + match score + memory
writes) alongside the physical shot. The score and the 0.80 threshold
must be legible on screen — the numbers are the evidence.

**Required insert, per-frame budget:** at least one shot must show the
robot's own measured timing for a full pass, broken into detect, embed and
search, the same breakdown L2 §6 shows for text. This is the number that
proves the loop closes in real time on the board, and L2 already teaches
that the encoder dominates while the search is close to free. Capture it
live from the robot's view; never re-type it in edit.

**Attribution:** none of the `data/objects/` CC images appear in these
shots (live objects only), so no attribution overlays are needed. If any
bundled photo appears on the robot's screen in an insert, render its
author + license + link per `data/objects/CREDITS.json`.

## Shots

| # | Beat | Shot |
|---|---|---|
| 1 | Fail | A novel object (pick something visually distinctive, not in any training set cliché — e.g. a hand-painted mug) held in front of the robot. Two-shot: object + robot. Screen insert shows the crop, the nearest-match score clearly **below 0.80**, and the "unknown" verdict. |
| 2 | Teach by voice | Presenter holds the object steady and says one sentence: "This is my mug — Maria made it." Screen insert shows the transcript appearing (Whisper), then one memory written: a single point with **both named vectors visible on screen — `image` and `text`** — and the transcript in the payload. Keep the full sentence audible — no cutaway during the utterance. |
| 3 | Recognize | The same object, clearly different angle (rotate ~90°, change height). Screen insert: match score **above 0.80**, the label, and the recalled note verbatim. Beat 1→3 must read as one continuous take or an honest jump cut — never staged out of order. |
| 4 | Teach close-up | Repeat of the teach interaction shot tight: the screen capture full-frame, annotated in edit with the two paths (crop→CLIP→image vector; speech→Whisper→Nomic→note). This is the slow-motion replay the script narrates step by step. |
| 5 | The day recalled | Presenter asks "what did you see today?" Screen insert: the filtered recall — a time-window query, results grouped as seen (photos/crops) vs heard (notes). At least one result must be something taught earlier in the shoot day, so the day is honestly the robot's own. |
| 6 | Offline reboot | Visible power-off, network indicator off (airplane-mode toggle or pulled dongle on camera), power on. Re-run shot 3's recognition and shot 5's question. Screen insert: shard reopened from disk (point count), both results identical. No cuts between power-on and the first recognition. |
| 7 | Forget it | Teach the object a deliberately wrong name, then delete that memory on camera (the **FORGET** control), then re-show the same object. Screen inserts: the wrong label recognized above 0.80, then the point count dropping, then the same object back at **unknown**. Shoot as one take. This is L2's third verb, and the robot already implements it as `delete_points`. |
| 8 | (Stretch) Fleet sync | Only if Edge→Cloud synchronization is actually wired: teach on this robot, show a second unit recognizing the same object. If the sync isn't built, this shot does not exist — never fake it. |
| 9 | B-roll | The robot's case open (Jetson + battery + camera visible), the repo README on screen, the robot on a desk beside the notebook lessons on a laptop. |

## Edit notes

- Beat 1–3 footage opens the lesson (script beat 1) — cut it tight,
  payoff first, before any explanation.
- Shot 4 plays under script beat 5; shots 5–6 under beat 6; shot 7
  under beat 7; shot 8, if it exists, under beat 8.
- Every on-screen score keeps its real value; no re-typed overlays.
- End card: repo URL + hardware bill of materials one-liner.
