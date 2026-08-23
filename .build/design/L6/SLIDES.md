# L6 slide briefs


Design handoff for the lesson's slides. `SCRIPT.md` names only which slug plays under each beat.

## `l6-00-endpoint`

```slide-brief
slug: l6-00-endpoint
purpose: the endpoint teaser, recolored from l3-00-endpoint. Same layout,
  same four nodes; all four are highlighted, because the capstone closes
  the whole loop.
on-slide text: node labels only: "capture", "embed", "store", "recall",
  small tag "all of it". No headline.
diagram spec (8:9, stack top-to-bottom):
  - Identical to l3-00-endpoint: four hand-drawn rounded nodes in a
    vertical loop, light-blue (#03A9F4) "capture", orange (#FF9800)
    "embed", violet (#6047FF) cylinder "store", red (#DC244C) "recall",
    curved arrows connecting them, the recall arrow curving back up
    toward capture.
  - No node is dimmed: every node carries a solid stroke and
    full-strength fill. This is the only teaser in the course where the
    whole loop is lit, and that contrast is the beat.
  - The tag reads "all of it" and points at the closing arrow rather
    than at one node. Small spiral-notebook motif beside the cylinder.
```

## `teach-store-recognize`

```slide-brief
slug: teach-store-recognize
purpose: show the whole lesson as a three-step loop. Teach an object by
  storing example photos, then recognize a new photo by nearest match.
on-slide text: node labels only: "photos (teach)", "CLIP", cylinder
  "object shard", "new photo (recognize)", "nearest match > threshold".
  No headline.
diagram spec (8:9, stack top-to-bottom):
  - Top: two small light-blue photo icons side by side labeled
    "photos (teach)", curved orange arrow down into an orange (#FF9800)
    node "CLIP".
  - Middle: the orange CLIP node feeds a violet (#6047FF) cylinder labeled
    "object shard", drawn with a small strip of vector cells and a payload
    tag "label".
  - Bottom: a single light-blue photo icon labeled "new photo (recognize)",
    curved red (#DC244C) arrow up through CLIP into the cylinder, returning
    a teal (#009688) check node labeled "nearest match > threshold".
  - The teach path (orange, top-down) and the recognize path (red,
    bottom-up) share the same CLIP node and the same cylinder: one shared
    space.
```

