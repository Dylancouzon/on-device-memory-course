# Marketing Script and Lesson 0 Script

**Course:** Building On-Device AI Memory with Qdrant Edge
**Instructor:** Dylan Couzon, Developer Relations Engineer at Qdrant

---

## Marketing Script

**Target runtime:** ~2 min
**Target spoken length:** 250–350 words
**Format:** Talking heads, Andrew and Dylan, with course B-roll

### Script

[Andrew]

AI Apps can interpret what they see and hear, but without memory,
every interaction starts over. In this course, you'll build a persistent,
multimodal memory that runs directly on a device.

Welcome to *Building On-Device AI Memory with Qdrant Edge*, created with
Qdrant and taught by Dylan Couzon, Developer Relations Engineer at Qdrant.

Dylan, what will learners be able to do by the end of the course?

[Dylan]

You'll build the memory layer for an AI assistant. It will capture text,
images, and voice notes, then retrieve the right information by meaning,
visual similarity, or metadata.

[B-ROLL: Show memories being captured, followed by text and image search
results from the course.]

We'll begin with a working robot to see what on-device memory makes possible.
Then we'll trace how observations move from sensors and local models into
searchable memory.

Most of the course is hands-on. You'll create a local Qdrant Edge shard in
Python, add and update memories, filter search results, and remove information
that the application should forget.

[B-ROLL: Show the Qdrant Edge shard, stored records, filtered results, and the
before-and-after delete table.]

You'll also connect several forms of memory. You'll search images with natural
language, retrieve related text and voice notes, and teach the application to
recognize a new subject from a few examples. You'll evaluate similarity scores
and choose a threshold so the application can decide when to return a match
and when to say it doesn't know.

[Andrew]

Why keep this memory on the device?

[Dylan]

Local memory can remain available without a network connection and keep
personal data close to where you captured it. Qdrant Edge runs inside the
application process, so the core lessons don't require a separate vector
search server, special hardware, or a Qdrant account.

If you're comfortable with Python and familiar with embeddings and vector
search, this course will give you a complete memory loop that you can inspect,
adapt, and extend for your own AI applications.

---

## Lesson 0: Introduction to the Course

**Target runtime:** ~2 min
**Target spoken length:** 250–350 words
**Format:** Talking heads, Andrew and Dylan

### Script

[Andrew]

In this course, you'll build persistent, searchable memory for an AI
application. It will support text, images, and voice notes directly on the
device.

Welcome to *Building On-Device AI Memory with Qdrant Edge*, created with
Qdrant. Your instructor is Dylan Couzon, Developer Relations Engineer at
Qdrant.

[Dylan]

Thanks, Andrew. We'll use one memory loop throughout the course: capture an
observation, encode it as a vector, store it with metadata, and retrieve it
when a later query points to the same idea or subject. You can add memories
without retraining the models.

You'll implement this loop with Qdrant Edge, an embedded version of Qdrant's
vector search engine that runs inside your Python process.

In Lesson 1, you'll see a robot use local memory to recall observations and
learn from a few examples. In Lesson 2, you'll examine the system behind it,
from the camera and local models to storage and retrieval.

Then you'll build the memory yourself. In Lesson 3, you'll store, retrieve,
filter, and forget text and image memories. You'll also compare the time spent
creating embeddings with the time spent searching vectors.

In Lesson 4, you'll combine text, photos, and locally transcribed voice notes.
In Lesson 5, you'll teach the application a new visual subject, evaluate its
matches, and calibrate its recognition threshold.

The optional appendix shows how to share selected memories through Qdrant
Cloud while keeping the rest local.

[Andrew]

You should be comfortable reading Python and familiar with embeddings and
vector search. You won't need special hardware, a Qdrant account, or an API
key for the core lessons.

[ACKNOWLEDGMENTS SLIDE]

Many people from DeepLearning.AI and Qdrant contributed to this course. We
would like to thank everyone who helped make it possible.

[PRODUCTION NOTE: Add every name shown on the acknowledgments slide here with
its phonetic pronunciation before recording.]

[BACK TO ANDREW AND DYLAN]

[Andrew]

Dylan, what will we do first?

[Dylan]

We'll begin by seeing on-device memory in action, then use that example to
identify the parts we'll build throughout the course. I'm excited to get
started.
