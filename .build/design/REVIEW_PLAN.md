# Review Plan — restructure quality gate

**Who runs this:** a Sonnet subagent with fresh context, at the end of the build session (after M5, before the Codex pass). You have not seen the build happen — that is the point. Read this file, then `CLAUDE.md`, then `.build/PLAN.md`, before touching anything else.

**Ground rules for the reviewer:**
- You review; you do not fix. Report findings only.
- You may not spawn subagents.
- You may run read-only commands (grep, diff, nbconvert to inspect outputs). Do not edit files, do not re-execute notebooks unless explicitly asked.
- Judge against the rules cited below, not your own taste. Where a rule and your instinct conflict, the rule wins; note the instinct as a `nit` if you must.

## The north stars (what DLAI asked for, 2026-07-15)

Every finding should trace back to one of these:

1. **Generalization.** Students learn on-device AI memory as a concept, not a product. "Learn about Qdrant without feeling that I'm learning about Qdrant."
2. **Show the machine.** Outputs reveal the gears — scores, matches, before/after comparisons — not just result dumps. ~50-50 code/abstraction: plumbing hidden, Qdrant calls visible.
3. **Eagerness.** Every lesson opens by showing the endpoint — what we're building toward.
4. **Density.** Six lessons, ~50 min. Merged lessons must not bloat; each beat earns its seconds.
5. **The arc lands.** L1 (idea) → L2–L5 (build it with your hands) → L6 (idea, embodied). The L5 capstone is the student's "I built the whole thing" moment; L6 maps the robot back to the lessons.

## Review areas and checks

### A. Generalization language audit
- In every `SCRIPT.md` and slide: "Qdrant" is named only when its API is on screen. Otherwise the language is "the shard," "your memory," "the index," "vector search." Grep the scripts; count violations.
- Each lesson has one concept anchor (memory formation → selective recall → a full day → recognition → embodiment) and it's stated, not implied.
- No marketing register anywhere: no "powerful," "seamless," "blazing fast." No unsupported performance claims (no cloud-vs-local latency comparison beyond the one honest live number; no "filters are faster" claim).

### B. Structure conformance
- Lineup: L1 video-only (no notebook), L2–L5 notebooks, L6 video-only. L1/L6 folders ship no notebook.
- Each lesson self-contained: no lesson reads another lesson's shard; collections are per-lesson; notebooks import from their own `helper.py` and read `../data/...`.
- No cleanup ceremony in cells — fresh-start lives in the helper.
- Every lesson's script opens with the endpoint-teaser beat.
- Re-run safety: setup cells must survive Restart & Run All; nothing depends on a previously-run lesson.

### C. Code hygiene (DLAI house format, per CLAUDE.md)
- Short cells, few lines each; near-zero inline comments (only student instructions like "Change this and re-run"); no per-cell prose, no preparation/summary cells.
- Code wraps ≤ 80 chars; one argument per line when a call breaks; never split inside an expression like `Query.Nearest(...)`. Imports/prints/long literals may exceed 80 only where wrapping hurts readability.
- **Every Qdrant Edge call is visible in cells** — `EdgeConfig`/`EdgeShard.create`, `Point` + `upsert_points`, `QueryRequest`/`Query.Nearest`, `Filter`/`FieldCondition`, `create_field_index`, `count`/`info`, `ScrollRequest`, `delete_points`, `EdgeShard.load`. If any of these hides in a helper, that's a **blocker**. Lesson-local wrappers are fine only when the wrapped call is defined on the page.
- Helpers hold only non-Qdrant plumbing (embeddings, viz, filler, cleanup, model loading).
- `helper.py` files match `python .build/gen_helpers.py` output exactly (diff them) — hand-edits are a **blocker**.
- Vector dims hardcoded (768/512). No `.env`, no tokens, no network calls in the student path.

### D. Outputs and payoffs
- Every designated payoff sits under a `## N. The payoff: …` heading and its executed output is saved in the shipped notebook.
- Reconcile the payoff registry (produced at M5) against every number quoted in scripts. A quoted score that doesn't match the executed output is a **blocker**.
- Specific guards:
  - L2: the cold-open question asked four times — nothing → café note → different top hit after `delete_points` → stays forgotten after reopen.
  - L3: RangeFloat gotcha respected (open-ended your-turn filters by category only).
  - L4: voice clip plays before its transcript; L5-bound couplings intact.
  - L5: threshold gap honest (taught held-out ≥ ~0.82, foreign ≤ ~0.75, threshold 0.80); ramen voice memo in top-3 for "the ramen place downtown"; capstone reopens offline and both skills re-verify.
  - Whisper released after transcription before a second embedding model loads.
- Outputs show mechanism (north star 2): scores visible, query-beside-match renders where designed, before/after comparisons actually compare.

### E. Narration review
- **Voice match:** new scripts must read as the same author as the pre-restructure scripts. Compare sentence length, verbosity, vocabulary, and register against the existing SCRIPT.md style (short declaratives, concrete nouns, no hype). Flag any script that sounds like a different writer.
- Neutral beat labels (`INTRO`/`WRAP`); no camera or production direction in SCRIPT.md.
- The explanation lives in narration, not in notebook prose — if a concept is explained in a markdown cell, that's a violation.
- Prior-course boundaries: no re-teaching quantization, compilation, embeddings-from-scratch, ANN/HNSW. L1 and L6 especially.
- L6 teaches, not tours: every robot stage maps to a lesson; detection and capture-cadence are named as new, black-boxed, and not taught.

### F. Slides
- Outside L1/L6: a slide exists only when a concept needs visualizing. Challenge every slide — "could the notebook output carry this?" If yes, flag it.
- L1/L6 slides are 16:9; all others 8:9; all styled per `.build/design/SLIDE_STYLE.md`; labels only, no headlines or subtitles.
- CC attributions for `data/objects/` images render wherever those images appear.

## Output format

Produce `REVIEW_FINDINGS.md` next to this file:

| # | Severity | Area | File / location | Rule cited | Finding | Suggested fix |
|---|---|---|---|---|---|---|

Severities: **blocker** (violates a binding rule or a north star; ship stops), **major** (weakens a payoff or the voice; fix before Codex pass), **minor** (polish), **nit** (taste; builder may ignore).

End with a one-paragraph verdict: does this course feel like learning a field or a product, and does the arc land?
