# L4 slide briefs


Design handoff for the lesson's slides. `SCRIPT.md` names only which slug plays under each beat.

## `l4-00-endpoint`

```slide-brief
slug: l4-00-endpoint
purpose: the endpoint teaser, recolored from l3-00-endpoint. Same layout,
  same four nodes; "embed" and "recall" are the highlighted pair.
on-slide text: node labels only: "capture", "embed", "store", "recall",
  small tag "this lesson". No headline.
diagram spec (8:9, stack top-to-bottom):
  - Identical to l3-00-endpoint: four hand-drawn rounded nodes in a
    vertical loop, light-blue (#03A9F4) "capture", orange (#FF9800)
    "embed", violet (#6047FF) cylinder "store", red (#DC244C) "recall",
    curved arrows connecting them, the recall arrow curving back up
    toward capture.
  - Only the highlight moves: "embed" and "recall" get a solid stroke and
    full-strength fill; "capture" and "store" render at reduced opacity.
  - The "this lesson" tag points at the highlighted pair. Small
    spiral-notebook motif beside the cylinder.
```

## `two-encoders-one-shard`

```slide-brief
slug: two-encoders-one-shard
purpose: show Nomic and CLIP as two separate encoders feeding two named
  rows inside a single EdgeShard.
on-slide text: node labels only: "Nomic-Embed-Text", "CLIP ViT-B/32",
  cylinder "EdgeShard" with rows "text" and "image". No headline.
diagram spec (8:9, stack top-to-bottom):
  - Top: orange (#FF9800) rounded node, document/text icon, label
    "Nomic-Embed-Text", curved arrow down, labeled "768-d", into a violet
    (#6047FF) cylinder's top labeled row "text" (small vector-cell strip
    icon in the row).
  - Middle: the same violet cylinder continues, second labeled row "image"
    just below the first, same cylinder body (this is ONE cylinder with two
    rows, not two cylinders).
  - Bottom: orange (#FF9800) rounded node, photo/image icon, label
    "CLIP ViT-B/32", curved arrow up or down (whichever reads cleanly)
    into that same cylinder's "image" row, labeled "512-d".
  - Cylinder hand-lettered title above it: "EdgeShard".
```

## `cross-modal-recall`

```slide-brief
slug: cross-modal-recall
purpose: show a text query embedded by CLIP's text tower landing directly
  in image vector space, retrieving a photo.
on-slide text: labels in the diagram only: the query text, "CLIP text
  tower", the highlighted "image" row, "bicycle.jpg". No headline.
diagram spec (8:9, stack top-to-bottom):
  - Top: light-blue (#03A9F4) node, speech-bubble icon, label
    "\"a red bicycle\"".
  - Curved arrow (Qdrant Red #DC244C) down into an orange (#FF9800) node
    labeled "CLIP text tower".
  - Same red arrow continues down into a violet (#6047FF) cylinder, landing
    specifically in a highlighted "image" row (draw this row with a red
    outline accent to show it's the one being hit).
  - Arrow continues out of the cylinder to a teal (#009688) node, photo
    icon, label "bicycle.jpg" with a small checkmark.
  - Label the long red arrow path once, small: "text query → image space".
```

## `filters-inside-query`

```slide-brief
slug: filters-inside-query
purpose: show that a filter runs inside the same query as the vector
  search, not as a second pass afterward.
on-slide text: gate and node labels only: "filter (indexed field)",
  "one pass", crossed-out "filter in your code / second pass".
  No headline.
diagram spec (8:9, stack top-to-bottom):
  - Top: a single red curved arrow labeled "query" entering from above.
  - Center: a violet hand-drawn cylinder (EdgeShard), dashed-border
    container labeled "shard". Embedded near the top of the cylinder: a
    small teal rounded-rectangle "gate" node with a funnel/filter icon,
    labeled "filter (indexed field)". The red query arrow passes visibly
    THROUGH this teal gate before continuing down into the cylinder body,
    which shows a few small result rows highlighted teal.
  - Arrow label at the gate: "one pass".
  - Below the cylinder, a separate smaller panel showing the crossed-out
    alternative: a gray dashed cylinder labeled "all results" (desaturated
    gray #4E5366, no fill), a gray arrow to a second gray box labeled
    "filter in your code" with a hand-drawn ✕ struck through the whole
    panel, small label "second pass".
  - Include the small spiral-notebook motif icon near the shard, tiny,
    non-dominant.
```

