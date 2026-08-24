# L1: Why Devices Need Memory (script)

**Target runtime:** ~8:45
**Format:** video only, no notebook. Slides are 16:9, briefs in `SLIDES.md` in this directory.

**Objective.** Two jobs at once. Hand the student the vector search toolbox the rest of the course uses (vector, embedding model, similarity score, details, index, and the store/recall/forget lifecycle), and convince a builder that on-device memory is worth their week.

**Thesis.** Getting a model to run on a small board is now an installable problem: there are wheels, runtimes, and a $249 board that does it. Giving that board a memory of what it has seen is still something you assemble yourself.

**Closing line.** You can download the model I am running on this thing. You cannot download what it saw in my room.

**Audience.** A hobbyist AI and robotics builder. Technical, impatient, building at home in the evening. They will skip a lecture that feels like a product tour.

**Robot claims, corrected against the robot repo.** The robot answers on its own panel and has no speaker, so nothing is ever spoken by the machine. Nothing on it generates text: the app formats a stored time, a place label, and a photo, and the place is a label set when the robot starts rather than anything it infers. So the question asked on camera is "when and where did you last see my water bottle", never "where did I leave it". Its stack is YOLOE for detection, CLIP's vision tower for image vectors, Nomic for text, Whisper for speech. There is no LLM, and no CLIP text tower. L1 never names a threshold number; L2 owns both numbers and why they differ.

**Vocabulary.** L1 owns vector, embedding model, similarity score, details, and index, each defined in the beat that first uses it. Filters are named once in beat 5 and taught in lesson four. No code appears on screen. Internals stay out: how an embedding model or an index works inside is prior-course material.

**The robot is on set for the whole shoot.** Beats 1, 10, and 11 are live. Four slide beats cut to the robot's own panel, and anything on its display is real output from the machine.

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

A time, the room, and the photo it took. It was never trained on my bottle, and there is no language model on that board. I taught it what my bottle looks like, it wrote down each sighting, and just found the note again. The app read it back.

The model is the easy part now. The memory is yours to build. That is this course, and today is the toolbox.

---

## Beat 2: SLIDE 1, a note becomes a vector

Slide: `l1-01-note-and-nearest`, both states. Robot cutaway on the last line: the recall answer from beat 1 back on the panel, the question at the top, the sightings under it.

**NARRATION:**

That answer starts with the smallest useful memory: a note. Let's say I drank a coffee: Flat white on the terrace.

A keyword search only looks for the same words. It would miss that “Flat white on the terrace” answers a question about sitting outside for a latte. So the note goes through an embedding model, a small network that turns text into a list of numbers. Ours returns 768 of them, and that list is called a vector. Notes that mean similar things land close together.

Now ask a real question: where can I sit outside for a latte? The question goes through the same model, so search becomes one question: which stored note is closest? The closest note wins because the two pieces of text mean similar things, even though they share no exact words. A keyword search would miss that connection.

That is retrieval, and it sits at the core of every lesson here. One rule about that score: it only means something inside its own model's space. Each lesson names its own range.

---

## Beat 3: SLIDE 2, state A, photos and words in one space

Slide: `l1-02-photos-and-words`, first state.

**NARRATION:**

Text is half a day. What about everything you see?

A model like CLIP has two halves trained together. One embeds images, one embeds text, and both land in the same space of 512 numbers. So a photo of a bicycle and the phrase "a red bicycle" come out as neighbours.

That means you can search photos with a sentence. Embed the words, return the nearest image. No tags and no captions, which is lesson four.

---

## Beat 4: SLIDE 2, state B, recognition and two vectors

Slide: `l1-02-photos-and-words`, second state. Robot cutaway on the last two sentences: the memory tab, one card held in frame, its photo and its taught sentence and its sighting count visible.

**NARRATION:**

That same idea lets the robot recognize objects. A new photo goes through the same image model as the remembered photo, producing another vector. Compare the two; if their similarity clears a threshold you pick, it is a match. No LLM interpreting the image, no model training, no custom vision pipeline—the device. It is simply retrieving the closest visual memory.

And one memory can carry two vectors: one for what the photo looks like, one for what the sentence means. One point, two ways back to the same moment. On the robot, that point holds the photo, the words I taught it, and its sighting count.

---

## Beat 5: SLIDE 3, the lifecycle loop

Slide: `l1-03-the-loop`. Robot cutaway on the second line: the live feed, boxes and scores updating while Dylan keeps talking.

**NARRATION:**

Put those pieces together and you get a memory loop. The robot is running it right now.

First, capture a moment: a photo of the thing in front of the camera. The encoder turns it into a vector on the device. When you teach it a label, the photo, vector, label, time, and place become one memory. Teaching happens once. Later, a new photo becomes another vector; retrieval finds the closest match, and the app recalls its label, time, and place.

Then forget. A memory you cannot delete from is not yours. The index underneath keeps retrieval quick as memories run into the thousands.

---

## Beat 6: SLIDE 4, four questions that put memory on the device

Slide: `l1-04-four-questions`.

**NARRATION:**

So why keep the memory on the device? Four questions, and you can answer them about your own project tonight.

Is there a network where the thing lives? In a workshop, a field, a basement, or anything moving, often not.

How long may an answer take? A machine reacting to what it sees cannot wait for a round trip.

Do you want your house on someone's server, or an API key sitting inside your robot?

And what happens the morning a provider retires an endpoint? A device that has to phone home can be switched off by someone who is not you.

If there is a network and seconds are fine, the cloud is the right answer. This course is for the other case.

---

## Beat 7: SLIDE 5, what you give up

Slide: `l1-05-what-you-give-up`.

**NARRATION:**

Now the honest half, because this is a trade and not a free upgrade.

You do not get the biggest model. A device this size recognises and retrieves. It does not reason about your day, unless you put a small language model on top of the memory.

Storage decides how much stays instantly searchable, so what to keep and what to drop becomes your decision.

Two devices know nothing about each other until you sync them, and that sync is yours to design. So is the update path.

The common answer is to keep the memory local and send the heavy thinking out when there is signal and permission.

---

## Beat 8: SLIDE 6, where this goes

Slide: `l1-06-horizon`.

**NARRATION:**

Here is the part I find genuinely exciting, and it is not a prediction. It is what changes for you.

When a device has a memory, you teach it by showing it something and telling it what it is. No dataset. No labels. No retraining and no GPU hours. One sentence, and it knows your thing from then on. That is already true on the board behind me.

Follow that out. A machine that gets better in your house without an update, because the improvement is the memory and not the weights. A machine you teach in the field, about objects nobody put in a dataset. Then more than one machine: one learns something and the others can have it, and what crosses between them is your decision rather than a default.

---

## Beat 9: SLIDE 7, the architecture

Slide: `l1-07-on-device`. Robot cutaway on the last line: the robot's own memory directory listed on its screen, then back to the machine on the shelf.

**NARRATION:**

Every machine like this runs the same shape, and it is the architecture of this course. The embedding models and the memory live inside your application's own process. A question comes in, gets embedded, gets matched, and comes back answered without touching a network. Recall is a function call in your program.

Qdrant Edge is the embedded build of Qdrant's vector search engine, so the search runs inside your program. No server to deploy and no account to create.

On disk it is a directory. Kill the process, start it again, and everything is still there, because the files are.

---

## Beat 10: ROBOT, live

Camera, no slide. Teach, recognise, recall, on one object, on the robot's own panel. Potato the cat plushie enters frame as an unknown box with no name. Dylan holds the button and names her. Potato leaves and comes back, and the panel names her with a real score against the bar. Then he asks when it last saw her. Any score on the display is real output. No threshold number is spoken.

**NARRATION:**

Let me show you the whole thing, live, because it takes about twenty seconds.

This is Potato, my cat plushie. Right now the robot has never seen her. It finds a thing in the frame, draws a box around it, and puts no name on it, because it has nothing to match her against.

So I hold the button and I tell it what she is. This is Potato.

That is the entire training procedure. One sentence. No detector on earth has a word for Potato, and it does not need one. Nothing was retrained. The models on that machine are exactly what they were a second ago. What changed is that there is now one more memory in the folder, with her picture and my words on it.

Potato goes away. Potato comes back. Watch the score clear the bar. She is recognised, out of a memory that is twenty seconds old.

And now I can ask about her. When and where did you last see Potato? A time, the room, and the frame it came from.

That is the machine we build next lesson, and the four after it are you building its memory.
