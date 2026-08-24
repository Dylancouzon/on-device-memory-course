# L1: Why Devices Need Memory

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

Slide: `l1-01-note-and-nearest`, both states. Visualize the note becoming numbers, then the question pulling the nearest note forward. Do not recap the narration in text. Robot cutaway on the last line: the recall answer from beat 1 back on the panel, the question at the top, the sightings under it.

**NARRATION:**

That answer starts with a small memory: a note. Say I had a coffee: Flat white on the terrace.

A keyword search only looks for the same words. It would miss that "Flat white on the terrace" answers a question about sitting outside for a latte. The note goes through an embedding model, a small network that turns text into a list of numbers. Ours returns 768 numbers. That list is a vector. Notes with similar meanings land close together.

Now ask: where can I sit outside for a latte? The question goes through the same model. Search then asks which stored note is closest. The closest note wins because the two pieces of text mean similar things, even though they share no exact words. A keyword search misses that connection.

That is retrieval, and it sits at the core of every lesson here. The score only means something inside its own model's space. Each lesson names its own range.

---

## Beat 3: SLIDE 2, state A, photos and words in one space

Slide: `l1-02-photos-and-words`, first state. Show the sentence and photo converging in one vector space, with only the labels the diagram needs.

**NARRATION:**

Text only gets us so far. What about everything you see?

A model like CLIP has two halves trained together. One embeds images and the other embeds text. Both produce 512-number vectors, so a photo of a bicycle and the phrase "a red bicycle" land near each other.

You can search photos with a sentence. Embed the words, then return the nearest image. No tags or captions. Lesson 4 adds those later.

---

## Beat 4: SLIDE 2, state B, recognition and two vectors

Slide: `l1-02-photos-and-words`, second state. Show two routes into one memory: image similarity and text meaning. Robot cutaway on the last two sentences: the memory tab, one card held in frame, its photo and its taught sentence and its sighting count visible.

**NARRATION:**

That same idea lets the robot recognize objects. A new photo goes through the same image model as the remembered photo and produces another vector. Compare the two. If their similarity clears a threshold you pick, it is a match. No LLM interprets the image. You do not retrain the model or build a custom vision pipeline. The device retrieves the closest visual memory.

One memory can carry two vectors: one for what the photo looks like and one for what the sentence means. One card, two ways back to the same moment. On the robot, that card holds the photo, the words I taught it, and its sighting count.

---

## Beat 5: SLIDE 3, the lifecycle loop

Slide: `l1-03-the-loop`. Show the lifecycle as a loop, with the index beneath store and recall. Do not turn the five stages into a text list. Robot cutaway on the second line: the live feed, boxes and scores updating while Dylan keeps talking.

**NARRATION:**

Put those pieces together and you get a memory loop. The robot is running it right now.

First, capture a moment: a photo of the thing in front of the camera. The encoder turns it into a vector on the device. When you teach it a label, the photo, vector, label, time, and place become one memory. Teaching happens once. Later, a new photo becomes another vector. Retrieval finds the closest match, and the app recalls its label, time, and place.

Then forget. If you cannot delete a memory, it is not yours. The index underneath keeps retrieval quick as the collection reaches the thousands. Lesson 4 turns those details into filters.

---

## Beat 6: ON CAMERA, why keep memory on the device

No slide. Keep the robot in frame.

**NARRATION:**

Why keep the memory on the device? Ask four questions about your own project.

Is there a network where the thing lives? In a workshop, a field, a basement, or anything moving, often there is not.

How long can an answer take? A machine reacting to what it sees cannot wait for a round trip.

Do you want your house on someone else's server, or an API key inside your robot?

What happens the morning a provider retires an endpoint? A device that has to phone home can be switched off by someone who is not you.

If there is a network and seconds are fine, the cloud is the right answer. This course is for the other case.

---

## Beat 7: ON CAMERA, what you give up

No slide. The tradeoffs are clear in the narration and do not need a text recap.

**NARRATION:**

There is a tradeoff here. This is not a free upgrade.

You do not get the biggest model. A device this size recognizes and retrieves. It does not reason about your day unless you put a small language model on top of the memory.

Storage limits how much stays instantly searchable. What to keep and what to drop becomes your decision.

Two devices know nothing about each other until you sync them. You decide how that sync works and how updates reach the devices.

One practical answer is to keep the memory local and send the heavy thinking out when there is a signal and permission.

---

## Beat 8: ON CAMERA, where this goes

No slide. Use the robot as the concrete example while describing teaching in the field.

**NARRATION:**

This is what changes for you.

When a device has a memory, you teach it by showing it something and telling it what it is. You do not need a dataset, a labeling project, retraining, or GPU hours. One sentence, and it knows your thing from then on. That is already true on the board behind me.

Take that outside the house. The machine gets better without an update because the improvement lives in its memory, not its weights. You can teach it in the field about objects nobody put in a dataset. With more than one machine, one can learn something and the others can receive it. You decide what crosses between them.

---

## Beat 9: SLIDE 4, the architecture

Slide: `l1-04-on-device`. Show the encoders and memory inside one process, with the network path struck out. Robot cutaway on the last line: the robot's own memory directory listed on its screen, then back to the machine on the shelf.

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
