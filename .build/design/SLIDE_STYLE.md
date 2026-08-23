# Slide style spec — all lessons

Every slide brief in `design/L*/SCRIPT.md` inherits this spec.

## The house template

All slides use the **DeepLearning.AI short-course template**. The
canonical example is the "Sample Slide: font size 18+" reference:

https://docs.google.com/presentation/d/1y0TFDboEH583k_Lirnb0P52e7eIhzipnv0m-HL3CQfE/edit?slide=id.p9

Match that template exactly for the outer frame:

- **Light theme.** White background (`#FFFFFF`). Dark ink for text and
  strokes. This is the DLAI house look — do not use a dark background.
- **Aspect ratio 8:9** (8" × 9", portrait-ish, narrow) for the notebook
  lessons, L3 through L6. Generous margins; never more than one diagram
  or chart per slide.
- **L1 and L6 are 16:9.** They are video-only lessons with no notebook
  beside the slide, so the wide format lays their flows out
  left-to-right where the 8:9 briefs stack top-to-bottom. Every other
  rule on this page applies to them unchanged, and each brief in those
  two scripts states its own ratio.
- **Minimum font size 18 pt** for every text element, including code,
  axis labels, and node labels. Nothing smaller than 18 pt ever.
- **Title** (when present) is centered near the top, large, bold, dark.
  Sentence case. No subtitle under it.
- **Footer.** The template's red/maroon decorative wave band runs across
  the bottom edge. Leave it in place; keep content clear of it.
- One idea per slide. If a diagram needs two ideas, make two slides.

### Logos — both corners, every slide

- **DeepLearning.AI logo** sits in the **top-right** corner (part of the
  template), roughly 1.3" wide with a small (~0.15") top and right
  margin.
- **Qdrant logo** sits in the **top-left** corner, mirroring it: the
  same size as the DeepLearning.AI logo, the same top margin, and a left
  margin equal to the DeepLearning.AI logo's right margin. Balance the
  two by cap-height / visual weight, not by literal bounding box.
- On the white background use the dark-ink asset
  `assets/logos/qdrant-logo-dark.svg` (the wordmark renders in `#111824`).
  Never use the white variant here.
- Both logos appear on **every** slide, not just the title slide.

## Visual language: hand-drawn flowcharts

Model the diagrams on the flowcharts in this article (open the URLs for
reference — they are the target look, before recoloring):

| Reference | URL |
|---|---|
| Hero: capture → embed → Qdrant Edge cylinder | https://miro.medium.com/v2/resize:fit:1000/1*cdyuxM5xH9dYmQs-XBIT-g.png |
| 4-stage pipeline, numbered containers | https://miro.medium.com/v2/resize:fit:700/1*Y-tSqCwHC1xBFrOcmDHVwQ.png |
| Data flow, left→right, labeled arrows | https://miro.medium.com/v2/resize:fit:1000/1*3kThruQRJ74REJD6Ll1-GA.png |
| Anatomy of a point (payload + named vectors) | https://miro.medium.com/v2/resize:fit:1000/1*_1L_qEJ7fdUPRVnxVkkUzg.png |
| Retrieval pipeline, score fusion | (article, "Multi-Modal Retrieval Pipeline" figure) |
| Quantization / consolidation comparisons | (article, last two figures) |

Source: "Building an Offline Life Memorizer" — Satyam Sahu, Towards AI,
Jun 2026. Style inspiration only; never copy a diagram's content.

The language, element by element:

- **Nodes** are rounded rectangles with a hand-drawn (slightly wobbly)
  stroke and a soft translucent fill of their stage color. Each node
  carries a small concrete icon (film strip, waveform, OCR page, clock,
  map pin, magnifier, brain, Σ) plus a 2–6 word label. Mono-spaced,
  code-looking labels for anything that is literally an identifier
  (`edge_config.json`, `text`, `payload`).
- **Containers / stages** are larger dashed-border rounded boxes with a
  hand-lettered title, optionally numbered ("1. Capture", "2. Embed").
- **Databases** are hand-drawn cylinders; a shard with named vectors is
  a cylinder with labeled rows, each row showing an icon + a strip of
  small vector cells (see the hero reference).
- **Arrows** are curved, hand-drawn, with tiny labels naming the thing
  that flows ("768-d vector", "payload", "0 network calls").
- **Flow** reads top→bottom in this 8:9 format (the references are
  landscape; restack their left→right flows vertically).
- **Photos** (when a brief calls for one) are the real course photos in
  `ro_shared_data/images/` — never stock, never generated. Respect the credits in
  `ro_shared_data/images/CREDITS.json`.

## The Qdrant palette (accents on white)

The DLAI template is the frame; the Qdrant palette is how we color the
diagrams *inside* it. On the white background, node fills are the stage
color at ~12–18% opacity with a solid stroke of the same color. Ink
strokes and lettering are dark (`#111824`); secondary text `#656B7F`.

Semantic color coding, consistent across every lesson:

| Stage | Color | |
|---|---|---|
| Capture / input / raw data | Light Blue | `#03A9F4` |
| Embedding / models | Orange | `#FF9800` |
| Storage / EdgeShard / persistence | Violet | `#6047FF` |
| Query / recall | Qdrant Red | `#DC244C` |
| Filters / results / success states | Teal | `#009688` |

Qdrant Red is an accent: arrows, highlights, the recall path, and the
template's footer wave. Never a large background fill in the content
area. Cloud/network elements (the thing we're beating) render in
desaturated gray `#4E5366`, often struck through or crossed out with a
hand-drawn ✕.

## Copy rules

- A slide is a picture, not a sentence to read. It plays under the
  narration, so the only words on it are the ones the diagram itself
  needs: labels inside boxes, on arrows, on axes.
- No headline-and-subtitle. Most slides carry no title — the narrator
  supplies it. Add a short title only when the diagram is ambiguous
  without one, and never a subtitle under it.
- If a text element does not name a part of the diagram, cut it.
- Sentence case everywhere. Contractions fine.
- Banned words: seamless, powerful, unlock, revolutionize, delve,
  robust, journey (except the course-map slide), and any
  "isn't just X, it's Y" construction.
- Numbers only when the notebook proves them or they carry a
  provenance badge (measured / precomputed / illustrative) — same
  labeling rule as the course charts.
- Logos: Qdrant (top-left) + DeepLearning.AI (top-right) on every slide,
  per the house-template rule above. Assets in `assets/logos/`.

## The course motif

"Memory is not the model's weights — it's the notebook the model keeps
beside it." A small hand-drawn spiral notebook icon is the course's
recurring visual: it may appear wherever a slide shows memories being
written or recalled. Draw it once, reuse it everywhere.
