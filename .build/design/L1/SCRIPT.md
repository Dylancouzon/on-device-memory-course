# L1: Why Devices Need Memory (script)

**Target runtime:** ~8:45
**Format:** video only, no notebook. Slides are 16:9, briefs in `SLIDES.md` in this directory.

**Objective.** Two jobs at once. Give the student the vector search toolbox used through the rest of the course (vector, embedding model, similarity score, details, index, and the store/recall/forget lifecycle), and show a builder why on-device memory is worth a week of their time.

**Thesis.** Getting a model to run on a small board is now mostly an installation problem. There are wheels, runtimes, and a $249 board that can do it. Giving that board a memory of what it has seen is still something you assemble yourself.

**Closing line.** You can download the model I am running on this thing. You cannot download what it saw in my room.

**Audience.** A hobbyist AI and robotics builder. Technical, impatient, building at home in the evening. They will skip a lecture that feels like a product tour.

**Robot claims, checked against the robot repo.** The robot answers on its own panel and has no speaker, so the machine never speaks. Nothing on it generates text. The app formats a stored time, a place label, and a photo. The place is set when the robot starts, not inferred by the model. The question asked on camera is "when and where did you last see my water bottle", never "where did I leave it". Its stack is YOLOE for detection, CLIP's vision tower for image vectors, Nomic for text, and Whisper for speech. There is no LLM and no CLIP text tower. L1 does not name a threshold number. L2 covers both numbers and why they differ.

**Vocabulary.** L1 owns vector, embedding model, similarity score, details, and index. Each is defined when it first appears. Filters are named once in Beat 5 and taught in Lesson 4. No code appears on screen. The internals of the embedding model and index belong to the prior course.

**The robot is on set for the whole shoot.** Beats 1, 10, and 11 are live. Four slide beats cut to the robot's own panel. Anything on its display is real output from the machine.

## Slides

| Slug | Idea | Status |
|---|---|---|
| `l1-01-note-and-nearest` | Two states: a note becomes 768 numbers; then the question ranked against three notes with real scores, and the keyword search that returns nothing | Merged from `l1-01-note-to-vector` + `l1-02-nearest-and-scored` |
| `l1-02-photos-and-words` | Two states: a sentence searching photos in one 512-number space; then two photos compared, and one memory carrying two named vectors | Revised from `l1-03-photos-and-words` |
| `l1-03-the-loop` | capture, embed, store, recall, forget, with the index underneath | Kept, was `l1-05-the-loop` |
| `l1-04-four-questions` | The four questions that put memory on the device | New |
| `l1-05-what-you-give-up` | The four things you give up for it | New |
| `l1-06-horizon` | Where this goes: teaching in the field, fleets, and what a device may keep | New |
| `l1-07-on-device` | Encoders and memory inside one process, the network path struck out | Kept, was `l1-06-on-device` |

Dropped: `l1-04-where-it-matters` (the four use-case tiles, absorbed by the horizon beat) and `l1-08-memory-is-a-folder` (the narrated directory anatomy is not verifiable from the robot repo, so one honest sentence in beat 9 replaces the slide).

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---:|
| 1 | INTRO, robot live | The question nobody can answer, and the machine that can | 55 |
| 2 | SLIDE 1 | A note becomes a vector, and search is the nearest one | 59 |
| 3 | SLIDE 2, state A | Photos and words in one space | 30 |
| 4 | SLIDE 2, state B | Recognition, and one memory with two vectors | 40 |
| 5 | SLIDE 3 | The lifecycle loop, and the index | 49 |
| 6 | SLIDE 4 | Four questions that put memory on the device | 48 |
| 7 | SLIDE 5 | What you give up | 42 |
| 8 | SLIDE 6 | Where this goes | 70 |
| 9 | SLIDE 7 | The architecture, and what it looks like on disk | 39 |
| 10 | ROBOT, live | Teaching instead of training | 76 |

Total: ~525 sec (8 min 45 sec) at 156 words per minute, 1,362 words of narration measured from the narration blocks below. Recount after any edit.

**To reach 7:30**, in this order: cut beat 6 to two questions (18 sec), beat 8's more-than-one-machine sentence (14 sec), beat 7's update-path line (8 sec), beat 9's on-disk paragraph (12 sec), beat 5's index clause (8 sec), beat 1's why-now paragraph (15 sec). Beats 2, 4, 8's teaching-not-training paragraph, and 10 are never cut.

---

## Beat 1: INTRO, robot live on set

Camera, no slide. The robot is in frame from the first second, on a shelf, the way it lives in the room. The water bottle was set down somewhere earlier and the robot saw it there. Dylan asks it out loud, and the answer appears on the robot's own panel.

**NARRATION:**

Where did you leave your water bottle?

Nobody can answer that. Your phone was not in the room, and neither was the biggest model on the internet.

This one was. It watches the room all day.

When and where did you last see my water bottle?

A time, the room, and the photo it took. Nobody trained it on my bottle, and there is no language model on that board. I taught it what my bottle looks like. It saved each sighting, then found the memory again. The app read it back.

Running the model is the easy part now. The memory is the part you build. That is this course, and today is the toolbox.

---

## Beat 2: SLIDE 1, a note becomes a vector

Slide: `l1-01-note-and-nearest`, both states. Robot cutaway on the last line: the recall answer from beat 1 back on the panel, the question at the top, the sightings under it.

**NARRATION:**

That answer starts with a small memory: a note. Say I had a coffee: Flat white on the terrace.

A keyword search only looks for the same words. It would miss that "Flat white on the terrace" answers a question about sitting outside for a latte. The note goes through an embedding model, a small network that turns text into a list of numbers. Ours returns 768 numbers. That list is a vector. Notes with similar meanings land close together.

Now ask: where can I sit outside for a latte? The question goes through the same model. Search then asks which stored note is closest. The closest note wins because the two pieces of text mean similar things, even though they share no exact words. A keyword search misses that connection.

That is retrieval, and it sits at the core of every lesson here. The score only means something inside its own model's space. Each lesson names its own range.

---

## Beat 3: SLIDE 2, state A, photos and words in one space

Slide: `l1-02-photos-and-words`, first state.

**NARRATION:**

Text only gets us so far. What about everything you see?

A model like CLIP has two halves trained together. One embeds images and the other embeds text. Both produce 512-number vectors, so a photo of a bicycle and the phrase "a red bicycle" land near each other.

You can search photos with a sentence. Embed the words, then return the nearest image. No tags or captions. Lesson 4 adds those later.

---

## Beat 4: SLIDE 2, state B, recognition and two vectors

Slide: `l1-02-photos-and-words`, second state. Robot cutaway on the last two sentences: the memory tab, one card held in frame, its photo and its taught sentence and its sighting count visible.

**NARRATION:**

That same idea lets the robot recognize objects. A new photo goes through the same image model as the remembered photo and produces another vector. Compare the two. If their similarity clears a threshold you pick, it is a match. No LLM interprets the image. You do not retrain the model or build a custom vision pipeline. The device retrieves the closest visual memory.

One memory can carry two vectors: one for what the photo looks like and one for what the sentence means. One card, two ways back to the same moment. On the robot, that card holds the photo, the words I taught it, and its sighting count.

---

## Beat 5: SLIDE 3, the lifecycle loop

Slide: `l1-03-the-loop`. Robot cutaway on the second line: the live feed, boxes and scores updating while Dylan keeps talking.

**NARRATION:**

Put those pieces together and you get a memory loop. The robot is running it right now.

First, capture a moment: a photo of the thing in front of the camera. The encoder turns it into a vector on the device. When you teach it a label, the photo, vector, label, time, and place become one memory. Teaching happens once. Later, a new photo becomes another vector. Retrieval finds the closest match, and the app recalls its label, time, and place.

Then forget. If you cannot delete a memory, it is not yours. The index underneath keeps retrieval quick as the collection reaches the thousands. Lesson 4 turns those details into filters.

---

## Beat 6: SLIDE 4, four questions that put memory on the device

Slide: `l1-04-four-questions`.

**NARRATION:**

Why keep the memory on the device? Ask four questions about your own project.

Is there a network where the thing lives? In a workshop, a field, a basement, or anything moving, often there is not.

How long can an answer take? A machine reacting to what it sees cannot wait for a round trip.

Do you want your house on someone else's server, or an API key inside your robot?

What happens the morning a provider retires an endpoint? A device that has to phone home can be switched off by someone who is not you.

If there is a network and seconds are fine, the cloud is the right answer. This course is for the other case.

---

## Beat 7: SLIDE 5, what you give up

Slide: `l1-05-what-you-give-up`.

**NARRATION:**

There is a tradeoff here. This is not a free upgrade.

You do not get the biggest model. A device this size recognizes and retrieves. It does not reason about your day unless you put a small language model on top of the memory.

Storage limits how much stays instantly searchable. What to keep and what to drop becomes your decision.

Two devices know nothing about each other until you sync them. You decide how that sync works and how updates reach the devices.

One practical answer is to keep the memory local and send the heavy thinking out when there is a signal and permission.

---

## Beat 8: SLIDE 6, where this goes

Slide: `l1-06-horizon`.

**NARRATION:**

This is what changes for you.

When a device has a memory, you teach it by showing it something and telling it what it is. You do not need a dataset, a labeling project, retraining, or GPU hours. One sentence, and it knows your thing from then on. That is already true on the board behind me.

Take that outside the house. The machine gets better without an update because the improvement lives in its memory, not its weights. You can teach it in the field about objects nobody put in a dataset. With more than one machine, one can learn something and the others can receive it. You decide what crosses between them.

---

## Beat 9: SLIDE 7, the architecture

Slide: `l1-07-on-device`. Robot cutaway on the last line: the robot's own memory directory listed on its screen, then back to the machine on the shelf.

**NARRATION:**

The architecture is simple. The embedding models and the memory live inside your application's own process. A question comes in, gets embedded, gets matched, and comes back answered without touching a network. Recall is a function call in your program.

Qdrant Edge is the embedded build of Qdrant's vector search engine, so the search runs inside your program. You do not deploy a server or create an account.

On disk, it is a directory. Stop the process and start it again. The memory is still there because the files are.

---

## Beat 10: ROBOT, live

Camera, no slide. Teach, recognise, recall, on one object, on the robot's own panel. Potato the cat plushie enters frame as an unknown box with no name. Dylan holds the button and names her. Potato leaves and comes back, and the panel names her with a real score against the bar. Then he asks when it last saw her. Any score on the display is real output. No threshold number is spoken.

**NARRATION:**

I can show you the whole thing live in about twenty seconds.

This is Potato, my cat plushie. The robot has never seen her. It finds a thing in the frame, draws a box around it, and gives it no name because it has nothing to match her against.

So I hold the button and I tell it what she is. This is Potato.

That is the entire training procedure: one sentence. No detector on earth has a word for Potato, and it does not need one. Nothing was retrained. The models on that machine are exactly what they were a second ago. The change is one more memory in the folder, with her picture and my words on it.

Potato goes away and comes back. Watch the score clear the bar. The robot recognizes her from a memory that is twenty seconds old.

Now I can ask about her. When and where did you last see Potato? The answer is a time, the room, and the frame it came from.

That is the machine we build next lesson. The four lessons after that are about building its memory.
