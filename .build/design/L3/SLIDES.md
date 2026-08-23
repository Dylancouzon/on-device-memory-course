# L3 slide briefs


Design handoff for the lesson's slides. `SCRIPT.md` names only which slug plays under each beat.

## `l3-00-endpoint`

```slide-brief
slug: l3-00-endpoint
purpose: the endpoint teaser. The course's capture → embed → store →
  recall loop with this lesson's stages highlighted.
on-slide text: node labels only: "capture", "embed", "store", "recall",
  small tag "this lesson". No headline.
diagram spec (8:9, stack top-to-bottom):
  - Four hand-drawn rounded nodes in a vertical loop: light-blue
    (#03A9F4) "capture", orange (#FF9800) "embed", violet (#6047FF)
    cylinder "store", red (#DC244C) "recall", curved arrows connecting
    them, the recall arrow curving back up toward capture.
  - "store" and "recall" get a solid stroke and full-strength fill;
    "capture" and "embed" render at reduced opacity.
  - A small hand-lettered tag "this lesson" pointing at the highlighted
    pair. Small spiral-notebook motif beside the cylinder.
```

## `anatomy-of-a-point`

```slide-brief
slug: anatomy-of-a-point
purpose: show the three parts of a stored memory before the notebook writes
  one. Model this on the article's "anatomy of a point" reference in
  SLIDE_STYLE.md.
on-slide text: compartment labels only: "id: 3", "named vector · text",
  "payload · note + fields". No headline.
diagram spec (8:9, stack top-to-bottom):
  - One large rounded container, violet (#6047FF) stroke and ~15% fill,
    hand-lettered title "Point" at top.
  - Inside, three stacked compartments (thin dashed dividers), each with a
    small icon + label, read top to bottom:
      1. tag/hash icon: "id: 3"
      2. waveform icon + small vector-cell strip (orange #FF9800 accent):
         "named vector · text"
      3. small document/page icon: "payload · note + fields"
  - No arrows needed; this is a single object, not a flow. Keep margins
    generous.
```

