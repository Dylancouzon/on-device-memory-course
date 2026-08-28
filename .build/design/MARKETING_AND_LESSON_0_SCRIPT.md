# Marketing Script and Lesson 0 Script

**Course:** Building On-Device AI Memory with Qdrant Edge
**Instructor:** Dylan Couzon, Developer Relations Engineer at Qdrant

---

## Marketing Script

**Target runtime:** ~2 min
**Target length:** 250–350 words
**Format:** Talking heads, Andrew and Dylan

### Script

[Andrew]

An AI application can respond to what it sees or hears right now. But how does
it remember what happened an hour ago, survive a restart, or recognize
something you taught it yesterday?

If every memory requires a cloud request, recall disappears with the network.
For a phone, wearable, robot, or field device, the memory may need to live
where the application runs.

Welcome to *Building On-Device AI Memory with Qdrant Edge*, created with
Qdrant and taught by Dylan Couzon, Developer Relations Engineer at Qdrant.

[Dylan]

Thanks, Andrew. In this course, you'll build a persistent memory layer that
runs inside an application. You'll turn text and images into vectors, store
them with useful context, retrieve them by meaning, and remove memories you no
longer want.

We'll use Qdrant Edge, the embedded version of Qdrant's vector search engine.
It runs in the application process and stores its data on local disk, so the
core course needs no separate server, Qdrant account, or network connection.

[Andrew]

You'll first see the complete idea running on a robot. It remembers where it
saw an object, and it can learn a personal name from a few examples without
retraining a model. You don't need the robot or any special hardware to follow
along.

[Dylan]

In the notebooks, you'll build the same memory loop on a regular computer.
You'll store and forget notes, add metadata filters, search photos with words,
transcribe voice notes locally, and assemble a memory of an entire day.

Then you'll teach the assistant to recognize a subject it has never seen. A
held-out photo tests whether it learned the subject, and you'll calibrate the
threshold that separates a match from an unknown object.

An optional appendix shows how selected memories can move between devices
through Qdrant Cloud.

If you're comfortable with Python and know the basic ideas behind embeddings
and vector search, this course will take you from those concepts to a memory
system you can run, inspect, and adapt. I hope you'll join us.

---

## Lesson 0: Introduction to the Course

**Target runtime:** 3–4 min
**Format:** Talking heads, Andrew and Dylan

## Beat Map

| # | Speaker | Content | Est. sec |
|---|---|---|---:|
| 1 | Andrew | Welcome and the missing-memory problem | 35 |
| 2 | Andrew | Why local memory matters | 25 |
| 3 | Andrew | Introduce Dylan | 10 |
| 4 | Dylan | Define the memory loop and Qdrant Edge | 35 |
| 5 | Dylan | Current course roadmap | 85 |
| 6 | Andrew | Prerequisites and setup expectations | 20 |
| 7 | Dylan | Learning outcome and transition | 15 |

Total: ~225 sec (~3 min 45 sec).

### Script

[Andrew]

Welcome to *Building On-Device AI Memory with Qdrant Edge*, created with
Qdrant.

AI models can classify an image, understand speech, and generate a response.
But a model's weights are not a record of what happened to you today. They do
not contain the note you wrote this morning, the place you left your keys, or
the object you taught your device five minutes ago.

An application needs a separate memory. That memory has to accept new
observations, keep useful context, survive a restart, and return the right
information later.

For some applications, a cloud service is the right place to store it. For
others, every cloud request adds a dependency on connectivity, latency, and an
external provider. Personal data may also be better kept on the device that
captured it.

This course explores that local path. Your instructor is Dylan Couzon,
Developer Relations Engineer at Qdrant.

[Dylan]

Thanks, Andrew. I'm excited to build this with you.

The method is simple: capture an observation, encode it as a vector, store the
vector with useful metadata, and retrieve it when a later question or image
points to the same memory. When the application learns something new, it adds
a memory. It does not need to retrain the model.

We'll implement that loop with Qdrant Edge, the embedded version of Qdrant's
vector search engine. It runs inside the application process and stores a
shard in a local directory. Search is a function call in your program, not a
request to a separate vector search server.

The course begins with two video lessons.

In Lesson 1, a robot recalls where it saw a water bottle, then learns Potato,
one specific cat plushie. Those examples introduce embeddings, similarity,
multimodal memory, and the capture, store, recall, and forget loop.

In Lesson 2, we'll take the robot apart and follow the path from its camera to
its memory. The Jetson keeps live vision responsive, but it is not a course
requirement.

Then you'll build the memory yourself in three notebooks.

In Lesson 3, you'll store, retrieve, and forget notes in a Qdrant Edge shard.
You'll add metadata filters, search a photo bank with words, and see how lookup
time changes as memory grows.

In Lesson 4, you'll combine a day of text, photos, and locally transcribed voice
notes. You'll ask questions across all three modalities, then add and retrieve
a memory of your own.

In Lesson 5, you'll teach the assistant from a few photos and test it with a
held-out view. You'll compare scores, calibrate a recognition threshold, and
assemble one persistent assistant.

The optional appendix moves selected memory through Qdrant Cloud. You'll pull
it onto a second device, transfer only what changed, and search local and
shared memories together.

[Andrew]

You should be comfortable reading Python and familiar with the basic ideas
behind embeddings and vector search. You won't need special hardware, a
Qdrant account, or an API key for the core lessons. The notebooks run on CPU,
and recall works offline once the local models are available.

[Dylan]

By the end, you'll understand how to give an application a memory that grows
without changing its model weights. You'll be able to inspect what it stored,
control what it retrieves, remove what it should forget, and decide what stays
local.

We'll start with the finished robot and the question that motivates the whole
course: where did you last see my water bottle?
