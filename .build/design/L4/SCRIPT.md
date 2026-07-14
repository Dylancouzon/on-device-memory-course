# L4 — Contextual Filtering for Memory — script

**Target runtime:** ~6–7 min

---

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---|
| 1 | INTRO | Why similarity alone is not enough | 30 |
| 2 | SLIDE 1 | Filters run inside the query, not after it | 35 |
| 3 | NOTEBOOK §1 | Memories with metadata — payload fields | 45 |
| 4 | NOTEBOOK §2 | Store, and index the fields we'll filter on | 30 |
| 5 | NOTEBOOK §3 | The payoff (a): time window, as a raw filter request | 65 |
| 6 | NOTEBOOK §4 | The payoff (b): semantic query + payload filter | 55 |
| 7 | NOTEBOOK §5 | Your turn: change the filter (editable) | 25 |
| 8 | NOTEBOOK §6 | Filter fields reference table | 30 |
| 9 | WRAP | Wrap-up + pointer to L5 | 45 |

Total: ~360 sec (~6 min). One slide, down from three: the time-window and
filter-toolbox slides are cut — a bracket on a timeline and a list of raw
conditions both read more clearly from the code and the reference table.

---

## Beat 1 — INTRO

**NARRATION**

Here is a question similarity search cannot answer by itself: where did I get
coffee this morning? A search for "coffee" can find yesterday's espresso just
as easily as this morning's cup. In this lesson, you'll combine similarity
with details such as time, place, category, and price. Let's get to it!

---

## Beat 2 — SLIDE 1

```
Slide brief
slug: filters-inside-query
purpose: show that a filter runs inside the same query as the vector search, not as a second pass afterward
on-slide text: gate and node labels only — "filter (indexed field)",
  "one pass", crossed-out "filter in your code / second pass, slower".
  No headline.
diagram spec:
  - Top: a single red curved arrow labeled "query" entering from above.
  - Center: a violet hand-drawn cylinder (EdgeShard), dashed-border container labeled "shard".
    Embedded near the top of the cylinder: a small teal rounded-rectangle "gate" node
    with a funnel/filter icon, labeled "filter (indexed field)". The red query arrow
    passes visibly THROUGH this teal gate before continuing down into the cylinder body,
    which shows a few small result rows highlighted teal.
  - Arrow label at the gate: "one pass".
  - Below/beside the cylinder, a separate smaller panel showing the crossed-out alternative:
    a gray dashed cylinder labeled "all results" (desaturated gray #4E5366, no fill),
    a gray arrow to a second gray box labeled "filter in your code" with a hand-drawn ✕
    struck through the whole panel, small label "second pass, slower".
  - Vertical stack for 8:9: query arrow top, shard-with-gate large in the middle,
    crossed-out alternative small at the bottom.
  - Include the small spiral-notebook motif icon near the shard, tiny, non-dominant.
```

**NARRATION**

The query passes through the filter on its way into the shard. The alternative
is to retrieve a large set of results and filter them later in your own code.
That means more work and a separate step to maintain. With Edge, filtering
and vector search happen in one query.

---

## Beat 3 — NOTEBOOK §1. Memories with metadata

Run the memories cell.

**NARRATION**

> Start with 25 text and voice memories — a cappuccino, a standup, a shopping trip, and so on. Each one carries a note or transcript, plus payload fields such as category, location, a timestamp in epoch seconds, and a price. Notice this is nothing exotic: it's the same payload pattern from L2, just with fields we're about to filter on.

---

## Beat 4 — NOTEBOOK §2. Store, and index the fields we'll filter on

Run the store-and-index cell.

**NARRATION**

> Store those 25 memories the usual way, then index the four fields we'll filter on: category and location as keywords, timestamp and price as floats. One call to optimize, and the shard is ready. Passing a filter to the query is what runs it inside the search; indexing these fields is what makes that filtering efficient, so the engine uses the index to narrow candidates instead of scanning every point.

---

## Beat 5 — NOTEBOOK §3. The payoff (a): time window, as a raw filter request

Run the cell. This is the one to slow down on — the filter is written out
in full, no helper.

**NARRATION**

> Here's the first payoff, and it's the cell to slow down on. The question is "where did I get coffee." Similarity alone surfaces coffee mentions from any time of day, including yesterday's coffee run and the reminder to buy coffee for home. Now look at the filter, written out in full from Qdrant Edge's own types: `Filter(must=[FieldCondition(key="timestamp", range=RangeFloat(gte=at(7), lte=at(12)))])`, dropped straight into the `QueryRequest` next to the vector query. Nothing is hidden in a helper here — this is the whole request the shard runs. With the window applied, this morning's cappuccino jumps to the top. Same query, same shard; the only thing added is the filter riding along inside it. The first list is similarity only, with an x on what the filter removes; below it, what comes back once the window applies.

---

## Beat 6 — NOTEBOOK §4. The payoff (b): semantic query + payload filter

Run the cell.

**NARRATION**

> The second payoff is the honest form of "somewhere to eat under fifteen dollars." It's not one clever fuzzy query — it's two explicit pieces. A semantic search for "somewhere to eat," narrowed by `Filter(must=[...])`: `FieldCondition(key="category", match=MatchValue(value="food"))`, and `FieldCondition(key="price", range=RangeFloat(lt=15))`. There's no hidden natural-language-to-filter translation. The first list shows what similarity alone returns; below it, what's left once the filter runs alongside it.

---

## Beat 7 — NOTEBOOK §5. Your turn: change the filter

Run the editable cell.

**NARRATION**

> Your turn. Change `my_category`, then re-run. The cell builds `Filter(must=[FieldCondition(key="category", match=MatchValue(value=my_category))])` directly from your value. Try food, travel, shopping, home, or health and watch the list change. A safe default is set, so the cell always returns something.

---

## Beat 8 — NOTEBOOK §6. The filter fields, for reference

Run or scroll to the reference table.

**NARRATION**

> One reference table before we move on. Category and location are keyword fields; price and timestamp are floats. The table shows the raw `FieldCondition` form for each: `MatchValue` for an exact value and `RangeFloat` for a numeric range. Combine conditions with `Filter(must=[...])` for AND or `Filter(should=[...])` for OR. That's the whole filter vocabulary you need for the rest of the course.

---

## Beat 9 — WRAP

Run the cleanup cell (final action).

**NARRATION**

> So: memory retrieval is similarity plus filters. The vector finds what you mean; the payload filter enforces when, where, and how much. Two recipes cover most of what you'll need — a time window, and a semantic query with a payload filter — and because the fields are indexed, the filter rides along inside the same on-device query, in a single pass. Filters are always composed explicitly in code: the query shows exactly what it asked for. Next, in L5, we put all of this together — photos, a voice note, and text notes from one day, in a single assistant.
