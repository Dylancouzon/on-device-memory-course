# Marketing Script and Lesson 0 Script

**Course:** Building On-Device AI Memory with Qdrant Edge
**Instructor:** Dylan Couzon, Developer Advocate at Qdrant

---

## Marketing Script

**Target runtime:** ~2 min
**Target length:** 250–350 words
**Format:** Talking heads, Andrew and Dylan

### Script

[Andrew]

If you're building AI on a device, you may already have a model running
locally. But where does that AI keep what it learns? If every memory requires a
cloud request, the application stops remembering when the network disappears.

I'm excited to introduce *Building On-Device AI Memory with Qdrant Edge*,
created with Qdrant and taught by Dylan Couzon, Developer Advocate at Qdrant.
Dylan works with developers building search and AI applications, helping them
turn retrieval concepts into systems they can run and inspect.

[Dylan]

Thanks, Andrew. In this course, you'll learn how to build persistent AI memory
that runs inside an application. You'll store information on local disk,
retrieve it by meaning, combine semantic search with filters such as time and
location, and keep recall available when the network is off.

We'll use Qdrant Edge as the implementation, but the methods apply more
broadly: separate memory from model weights, choose the right embedding space
for each data type, store useful metadata, and make every retrieval decision
inspectable.

[Andrew]

If you've learned the basics of embeddings, vector search, or on-device AI,
this course connects those ideas. You'll move from a model that can respond in
the moment to an application that can accumulate useful context over time.

[Dylan]

You'll build a local memory store, search text and photos together, add
contextual filters, and assemble an interactive memory assistant. You'll teach
a device to recognize a new object by adding a few examples to its memory —
the model isn't retrained; the memory changes. And in the final lesson, you'll
see that same design running on a robot.

By the end, you'll understand how information moves from input, to embedding,
to local storage, and back into a useful result. I hope you'll join us.

---

## Lesson 0: Introduction to the Course

**Target runtime:** 3–4 min
**Format:** Talking heads, Andrew and Dylan

## Beat Map

| # | Speaker | Content | Est. sec |
|---|---|---|---:|
| 1 | Andrew | Welcome and the missing-memory problem | 35 |
| 2 | Andrew | Why memory belongs on the device | 25 |
| 3 | Andrew | Introduce Dylan | 10 |
| 4 | Dylan | Define the method and course approach | 32 |
| 5 | Dylan | Course roadmap | 70 |
| 6 | Andrew | Prerequisites and learning outcomes | 22 |
| 7 | Dylan | Why the topic matters | 22 |
| 8 | Andrew + Dylan | Acknowledgments and transition to L1 | 10 |

Total: ~226 sec (~3 min 45 sec).

### Script

[Andrew]

Welcome to *Building On-Device AI Memory with Qdrant Edge*, created with
Qdrant.

AI models can now run on phones, laptops, and other edge devices. They can
classify an image, understand text, or generate a response without sending
every input to a remote model. Vector search also gives applications a way to
retrieve information by meaning.

But those capabilities leave an important question unanswered: where does the
application remember what happened before?

A model's weights are not a record of your recent notes, photos, preferences,
or observations. An application needs a separate memory that can grow as new
information arrives, survive a restart, and return the right context later.

When that memory depends on a cloud service, every recall depends on a network
connection. For personal and real-time applications, local memory can reduce
that dependency and keep private data on the device.

I'm delighted to introduce your instructor, Dylan Couzon, Developer Advocate
at Qdrant.

[Dylan]

Thanks, Andrew. I'm excited to work through this with you.

This course focuses on one practical method: turn an observation into an
embedding, store the vector with useful metadata, and retrieve it when its
meaning and context match a later question. The memory lives outside the model
weights, so the application can update what it knows without retraining the
model.

We'll implement that method with Qdrant Edge, an embedded version of Qdrant's
vector search engine. It runs inside the application process and stores its
shard on local disk. Model loading and display code stay out of the way so we
can inspect the memory operations themselves.

Lessons two through five each use one notebook to explore one major idea;
the first and last lessons are on video.

In lesson one, we'll look at why an AI's memory can't live in the cloud, and
at the loop the whole course builds: capture, embed, store, recall.

In lesson two, you'll build the complete memory lifecycle. One question,
asked four times: of an empty store, after writing notes, after forgetting
one on purpose, and after a restart.

In lesson three, you'll work with text and photos together. Each data type
gets the right embedding path, you'll retrieve a photo from a text
description, and structured filters add details such as category and price.

In lesson four, you'll assemble a whole day — photos, voice notes transcribed
on the device, and text notes — into an interactive personal memory
assistant. You'll ask your own question, add a new memory, and retrieve it
immediately.

In lesson five, you'll teach the device a new object from a few images and
test it with a view it has never seen. The model remains unchanged; the
device learns by writing new memory. Then you'll assemble everything from
the course into one assistant that keeps working after a restart, offline.

And in the final lesson, you'll see the whole design embodied: a robot that
runs the same memory loop you built, taught by showing and telling.

[Andrew]

This course assumes you're comfortable with Python and familiar with the basic
ideas behind embeddings and vector search. You won't need special hardware, an
account, or an API key. The exercises run in a CPU-only notebook environment,
and the course path works without a network once the models are available
locally.

By the end, you'll understand the principles behind persistent local memory,
multimodal retrieval, contextual filtering, and learning through memory
updates.

[Dylan]

What excites me about this topic is that memory lets an AI application carry
useful context forward. It can add new information and use that information
later, while keeping the retrieval process visible to the developer.

[Andrew]

Many people from Qdrant and DeepLearning.AI contributed to this course. We'd
like to thank everyone involved in making it possible.

Dylan, what will we do first?

[Dylan]

We'll start with why an AI's memory has to live where the AI runs — and then
we'll build one. Let's get started!
