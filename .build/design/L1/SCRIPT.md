# L1: Why Devices Need Memory

## Beat 1: INTRO, robot live on set
Camera, no slide. Robot in frame; water bottle was seen in several places throughout the day. Ask on the robot’s panel.
**TALKING POINTS:**
- Where did you last see my water bottle?
- No phone / LLM in room
- Robot watched all day
- [ASK]
- Multiple sightings: latest first
- Time + place + photo
- No bottle-specific training; no LLM
- Teach once → save new sightings
- Course focus: memory

---
## Beat 2: SLIDE 1, a note becomes a vector
Slide: `l1-01-note-and-nearest`. Note → numbers; question → nearest note. Robot cutaway with recall answer.
**TALKING POINTS:**
- How did we do that?
- Start with the simplest version: text
- Example: lunch
- Keywords vs. semantic understanding
- Embedding: text → vector
- List of embeddings > On a graph
- Cluster together > Similar meaning
- Query → same embedding model → vector
- Vector location → mathematical similarity score
- Higher score = closer meaning
- Retrieval = core pattern

---
## Beat 3:  photos and words in one space
**TALKING POINTS:**
- Beyond text: everything you see
- CLIP: Two halves trained together: image encoder + text encoder
- Water bottle photo and words land near each other
- Search photos with a sentence
- No tags or captions

---
## Beat 4: recognition and two vectors
**TALKING POINTS:**
- Same idea lets robot recognize
- Compare vectors; threshold → match
- No LLM, retraining, or custom vision pipeline
- One memory, two vectors: image + text
- Two ways to recall a memory: sight or meaning

---
## Beat 5: SLIDE 3, the lifecycle loop
Slide: `l1-03-the-loop`. Show lifecycle loop and payload.
**TALKING POINTS:**
- Memory loop
- Capture → encode → store → recall and forget if we want to
- Photos are turned into vectors
- We also store metadata, which we call payload: label, time, place, name
- anything you want becomes part of that memory
- Those payloads allow for filtering, specific moment or location for example
- Forgetting: delete the vector; remove it from searchable memory
- No retraining

---
## Beat 6: ON CAMERA, why keep memory on the device
No slide.
**TALKING POINTS:**
- Why keep memory on device
- Four questions: network, latency, privacy, provider dependence
- Offline: workshop, field, basement, moving device
- Real-time response; no round trip
- Data ownership; API keys
- Provider changes / endpoint retirement
- Cloud is fine when connected and seconds are acceptable
- Local memory for the other cases
- tradeoffs: smaller models, limited storage, and no automatic sharing between devices.

---
## Beat 8: ON CAMERA, where this goes
No slide.
**TALKING POINTS:**
- [Show Potato: unknown]
- Generic category: cat plushie; personal identity: Potato
- [TEACH] “This is Potato”
- One sentence → personal memory
- No dataset, labeling, retraining, or GPU hours
- Improvement in memory, not weights
- Learn in field; no update
- Multiple devices: share selected memories
- Owner controls what crosses devices

---
## Beat 9: SLIDE 4, What runs on the device
Slide: `l1-04-on-device`. Encoders and memory inside one process; network path struck out.
**TALKING POINTS:**
- One process
- Models + memory together
- Question → vector → search → result
- Qdrant Edge = embedded Qdrant vector search engine
- Runs inside your application; no separate server
- No Qdrant account; no network needed for recall
- Memory = local directory
- Stop and restart; memories persist
- Same architecture: laptop, edge computer, or robot

---
## Conclusion
A memory system has three jobs: turn an experience into a searchable representation, store it with useful context, and retrieve the most relevant memories when you ask. In the next lessons, we’ll build each part locally on a device.
