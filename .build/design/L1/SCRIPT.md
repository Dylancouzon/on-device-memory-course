# L1: The On-Device Memory Problem

**Target runtime:** ~3–4 min
**Course:** Building On-Device AI Memory with Qdrant Edge, Lesson 1

Lesson 0 introduces the course, the edge-memory problem, the curriculum, and
the instructor. This lesson starts with the first implementation.

## Beat Map

| # | Type | Content | Est. sec |
|---|---|---|---:|
| 1 | SLIDE 1 | Lesson title | 10 |
| 2 | TALKING HEAD | Build the smallest working memory | 20 |
| 3 | SLIDE 2 | EdgeShard runs inside the application | 30 |
| 4 | NOTEBOOK §1 | Configure the named vector | 25 |
| 5 | NOTEBOOK §2 | Create the local shard | 25 |
| 6 | NOTEBOOK §3 | Embed and store one note | 35 |
| 7 | NOTEBOOK §4 | Close the shard and inspect its files | 40 |
| 8 | TALKING HEAD | Transition to the full memory lifecycle | 15 |

Total: ~200 sec (~3 min 20 sec).

---

## Beat 1: Slide 1, Title

```slide-brief
slug: l1-01-title
purpose: Introduce lesson one.
on-slide text: "Lesson 1: The On-Device Memory Problem". A small
  hand-drawn spiral notebook motif represents external memory.
```

---

## Beat 2: Talking Head

**NARRATION:**

In this lesson, you'll build the smallest working on-device memory. You'll
create a local store, write one note, close it, and inspect what remains on
disk. Let's get coding!

---

## Beat 3: Slide 2, EdgeShard Inside the Application

```slide-brief
slug: l1-02-edge-architecture
purpose: Show where the memory store runs before students create it.
on-slide text: Node labels only: "application", "EdgeShard", and
  "local disk". No headline.
diagram spec: One dashed container labeled "application". Inside it,
  place a violet hand-drawn cylinder labeled "EdgeShard". Connect the
  cylinder to a small disk icon labeled "local disk". Everything stays
  inside one device outline. Do not include a cloud, comparison panel, or
  optional synchronization path. Flow reads top to bottom in the 8:9
  format.
```

**NARRATION:**

The method is simple: keep memory beside the application instead of behind a
network request. Qdrant Edge runs inside the application process, and an
EdgeShard stores its data on local disk. A shard is the unit a Qdrant
collection is made of: on a server a collection spans many shards, and Edge
gives you exactly one, in-process. Now let's create one.

---

## Beat 4: Notebook §1, Configure the Memory Store

Keyed to notebook cells 2–3 (`## 1. Configure the memory store`).

**NARRATION:**

The shard needs to know the shape of the vectors it will store. We give this
vector a name, `text`, set its size to match the text embedding model, and use
cosine distance to compare vectors.

---

## Beat 5: Notebook §2, Create It

Keyed to notebook cells 4–5 (`## 2. Create it`).

**NARRATION:**

`EdgeShard.create` creates the store in a local directory. There is no server
to start and no account to connect. At this point, the application has a place
to keep memory on disk.

---

## Beat 6: Notebook §3, Write the First Memory

Keyed to notebook cells 6–7 (`## 3. Write the first memory`).

**NARRATION:**

Now we'll store one note about a coffee shop. The embedding model turns the
note into a vector, and the point keeps that vector together with the original
text. We upsert the point, and the store now contains one memory.

---

## Beat 7: Notebook §4, Inspect the Files

Keyed to notebook cells 8–10
(`## 4. The payoff: a memory store that is just files`).

**NARRATION:**

Close the shard and inspect its directory. The memory store remains as files
on local disk after the Python object is gone. That is the principle behind
the rest of the course: model weights stay the same, while a separate memory
store can grow and persist over time.

---

## Beat 8: Talking Head

**NARRATION:**

You now have one persistent memory on disk. In L2, you'll turn this into a full
memory lifecycle by storing several notes, recalling them by meaning, and
reopening the shard after a restart.
