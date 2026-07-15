# Payoff registry — computed from the executed notebooks (M5)

Every quoted score/output, its section, and its guard. Recomputed from the
shipped, executed L2–L5 notebooks (run in order, fresh kernels, this
machine; the DLAI sandbox run remains the shipped source of truth).
Reconcile scripts against this file; a quoted value that drifts is a
blocker.

## L2 — Store and Recall (`coffee_shard`)

| § | Payoff | Executed value | Guard |
|---|---|---|---|
| 1 | Ask #1 (empty shard) | 0 hits | must be exactly 0 |
| 5 | Keyword scan "latte" | 0 matches | must be exactly 0 |
| 5 | Ask #2 top hit | id 0 café note @ **0.653** (then 0.590 quiet cafe, 0.511 espresso) | café note ranks #1 |
| 6 | Offline recall | standup note with Sarah | returns under `no_network()` |
| 7 | Local latency | **0.16 ms** median at **5,020** memories, 200 queries | one honest live number; no cloud comparison |
| 8 | Ask #3 (after `delete_points([0])`) | top = quiet cafe @ **0.590**; runners-up scores unchanged; café marked ✗ | different top, lower score, others untouched |
| 9 | Restart receipt | 34 files on disk; points 5,019 before = after; top hit = ask #3's; forgotten_note_returned = no | forgotten note stays gone after `EdgeShard.load` |

## L3 — Finding the Right Memory (`mem_shard`)

| § | Payoff | Executed value | Guard |
|---|---|---|---|
| 3 | Store totals | 20 notes + 17 photos = 37 | — |
| 4 | "black and white sneakers" | **sneakers.jpg @ 0.252** (bicycle 0.204, gym 0.196) | sneakers.jpg ranks #1 |
| 6 | Default "a bowl of noodles" | ramen.jpg @ 0.240 | top hit is a plausible noodle photo |
| 7 | Food under $15 | before: café ✗, quiet cafe ✗, ramen note ✗, espresso ✓; after: espresso ✓, bakery cronut ✓ | filter passes only priced food notes (RangeFloat excludes missing price — curated payoff) |
| 8 | History load | 102 notes, total 139 | your-turn filters by **category only** |

## L4 — Your On-Device Assistant (`day_shard`)

| § | Payoff | Executed value | Guard |
|---|---|---|---|
| 1 | Captures + on-device transcript | 42 captures (17 photo / 20 text / 5 voice); ramen memo transcript shows "$14" (real ASR artifact) | transcript produced by local Whisper, not the JSON fallback |
| 4 | Store totals | 25 text+voice, total 42 | — |
| 7 | Sneakers under $50 | Photos: sneakers.jpg (id 30) @ **0.252** top; Text: id 5 running-shoes note @ 0.652 | sneakers photo #1 under the filter |
| 9 | Add your own | id 900 spare-key note @ **0.757**, ranked #1 | added memory wins clearly |

## L5 — Teaching It to See (`object_shard`, `assistant_shard`)

| § | Payoff | Executed value | Guard |
|---|---|---|---|
| 3 | Seeded views | 3 (lithops 2, backpack 1 + note) | — |
| 4 | Fail beat | gaillardia_3 → UNKNOWN; closest lithops_2 @ **0.609** | pre-teach score below 0.80 |
| 6 | Recognize new angle | gaillardia_3 @ **0.903** "orange flower" | held-out ≥ 0.82 |
| 7 | Threshold gap chart | taught: gaillardia_3 0.903, backpack_2 0.863; foreign: plant 0.739, book 0.634, coffee 0.562; line at 0.80 | `check_objects.py` gate: held-out ≥ 0.82, foreign ≤ 0.75; swap objects, never move the threshold |
| 8 | Your turn (rubberduck default) | held-out view 0.935 | ≥ 0.82 per gate |
| 9 | Assistant assembled | **145** memories (day + 102 history + 1 taught view) | Nomic + CLIP loaded together |
| 10 | "the ramen place downtown" | Voice: id 20 memo @ **0.803** (#1 text-space hit); Text: id 8 @ 0.786; Photo: ramen.jpg @ 0.247 | **ramen voice memo top-3** — §12 receipt reads `hits["Voice Notes"][0]` |
| 11 | Show what you taught | backpack_2 @ **0.863** + "I remember this: Quechua daypack…" | ≥ 0.80 and note recalled |
| 12 | Offline restart receipt | 145 memories; ramen memo recalled; backpack recognized; sockets blocked | both skills survive `close()` → `load` |

## Cross-checks (M5, this machine)

- `check_objects.py`: PASS for all six objects (threshold 0.80 in a real gap).
- RAM: Whisper → release → Nomic + CLIP peaks at **1.94 GB** RSS (4 GB budget holds; sandbox re-check still pending with DLAI).
- Script reconciliation: no scripted number contradicts this table (narration quotes "quiet cafe", "well under a millisecond", "well below/above the threshold" — all hold).
