# L1: Why Devices Need Memory

## Beat 1: INTRO, robot live on set
Camera, no slide. Robot in frame
**TALKING POINTS:**
- Where did I leave my Watch?
- No phone or LLM in the cloud can answer that question
- This robot has been traveling with me, saving what it sees
- [ASK]
- Multiple sightings: latest first
- Time + place + photo
- No specific training; no LLM
- Teach once → save new sightings
- Qdrant Edge: vector search engine running on the device

---
## Beat 2: SLIDE 1, a note becomes a vector
Slide: `l1-01-note-and-nearest`. Note → numbers; question → nearest note. Robot cutaway with recall answer.
**TALKING POINTS:**
- How did we do that?
- Start with simplest version of a memory, text: “I had ramen for lunch”
- An embedding model turns the text into a vector
- A vector is a list of numbers, represents the meaning of the text
- On the graph, similar meanings land near each other
- The question goes through the same embedding model
- We compare its distance from the stored memories
- The closer the vectors, the higher the similarity score
- Returning the closest memories is called retrieval
- This is the core pattern you’ll build in this course

---
## Beat 3: photos, words, and recognition
Probably a slide here too 
**TALKING POINTS:**
- That same idea also works with photos
- For this, we use a model called CLIP
- CLIP has one encoder for images and another for text
- Both place their vectors on the same graph
- A photo of a watch lands near words that describe a watch
- That means we can search images using words
- The same idea lets the robot recognize what it sees
- By comparing vectors of what it sees and what it knows
- If score > threshold → match
- No LLM, retraining, or custom vision pipeline
- Since we’re using custom labels, every memory has two vectors: image + text
- Two ways to recall a memory: sight or meaning

---
## Beat 4: SLIDE 3, the lifecycle loop
Slide: `l1-03-the-loop`. Show lifecycle loop and payload.
**TALKING POINTS:**
- So far, we’ve focused on finding a memory
- A memory needs more than its vectors
- Qdrant Edge keeps the vectors in an index for search
- Alongside them, we store context called the payload
- Name, time, place, and photo
- Vectors find memories by similarity
- Payload filters by exact details, such as a place or time
- Store a new memory when something happens
- Delete the complete memory when it should be forgotten
- Memories are stored locally and remain after the application restarts
- Store → recall → forget

---
## Beat 5: ON CAMERA, why keep memory on the device
No slide.
**TALKING POINTS:**
- Why keep memory on the device?
- It keeps working without an internet connection
- Useful in a workshop, vehicle, basement, or the field
- No network round trip
- Recall can be faster and more predictable
- Private memories can stay on the device
- No cloud account or API required
- Cloud is useful when memories need to be shared
- Local devices have less compute and storage
- Choose based on where the device works and where its data can go

---
## Beat 6: ON CAMERA, where this goes
No slide.
**TALKING POINTS:**
- [Show Potato: unknown]
- Generic category: cat plushie; personal identity: Potato
- [TEACH] “This is Potato”
- One sentence → personal memory
- Teach it from another angle → add another vector
- Each new taught view adds a vector instead of replacing the others
- Recognition compares what it sees with all the taught views
- More varied views → better recognition
- No dataset, labeling, retraining, or GPU hours
- Improvement in memory, not weights
- Learn in field; no update
- Multiple devices: share selected memories
- Owner controls what crosses devices

---
## Conclusion
**TALKING POINTS:**
- The model did not change
- What changed was the device’s memory
- Next, we’ll open the robot and see how it was built
