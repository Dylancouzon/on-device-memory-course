# L2: Building the Device (script)

**Target runtime:** ~9:20
**Format:** video only, no notebook. Slides are 16:9, briefs in `SLIDES.md` in this directory. Production direction lives in the shotlist, never here.

**Objective.** Answer the question a hobbyist is already asking at the end of lesson one: could I build this? The lesson follows the build in the order it happened. Each beat covers a decision, the alternatives, and the cost. It is a build lesson, not a tour of a prop. By the end, viewers should have a better sense of what they would choose for their own project.

**What this lesson does not do.** It does not teach thresholds, filters, coverage, or recall. The student builds those by hand in lessons three to six. When the robot touches one of them, the beat names it briefly and points to the lesson that covers it. This lesson stays with the gap a notebook cannot show: what changes between one clean photo and six frames a second in a real room.

**STATUS: PROVISIONAL.** The robot app and hardware exist; the shoot does not. Every number below is sourced from the robot repo and must be reconciled against the recorded footage before anything is cut. Numbers on screen are the evidence, and the narration never claims what the footage does not show.

**Sourced claims, with the constraint each one carries:**

- The detector runs at roughly 165 ms per frame on the Jetson GPU, against seconds per frame on CPU. This justifies using the GPU. It is not a board-selection experiment, so the narration says what it is.
- A Raspberry Pi 5 should run the software and has not been tested. Say "should" and "untested", never "does".
- Of the three encoders, only CLIP's vision tower loads at startup. Speech and text load the first time you teach or ask. The service sits at roughly 2.3 to 2.5 GB after startup, before those two load. YOLOE loads as well, so the claim is about encoders.
- The parts: Jetson Orin Nano Super 8 GB at $249, a 256 GB NVMe at about $30, a 37 x 37 mm USB camera at about $60, about 300 g of filament at about $8. Roughly $347. So the build is a $347 build around a $249 board.
- Print time is about 8 hours for the three plates. `docs/hardware.md` still says "about a day and a half" and must be corrected to match before this ships.
- The enclosure page audits itself on every load. The audit passed and the first build still could not be assembled: a 37.4 mm tray for a 37 mm board, a clamp with 2.5 mm per side of interference and nothing to flex, and a written instruction describing a motion that cannot physically happen. The audit now sweeps the assembly motions themselves and requires zero interference.
- The recognition threshold on the robot is 0.90, camera calibrated. The lab notebook uses 0.80. Both numbers are named here, once, and lesson six is where the student calibrates their own.
- CLIP's text tower is deliberately absent, because searching the image space with the words of a question measured useless.
- Recall runs in three steps: the text model picks which object out of the names the operator taught, then sightings are answered by time, and "what did you see today" uses no vectors at all.
- After every memory change the app calls `flush()`, so once the call returns the memory survives reopening from disk. That is the whole claim. Nothing here says pulling power is safe for the filesystem.
- Focus is sticky: a challenger has to be 1.6 times more salient to take the box, and a stable track re-asks memory every two seconds.
- The crop that gets embedded has a 12 percent margin and everything outside the segmentation mask flattened to gray.

## Slides

| Slug | Idea |
|---|---|
| `l2-01-the-parts` | Four parts, what each one is for, and the total |
| `l2-02-where-the-compute-goes` | Detector on the GPU against the same work on CPU, and what stays loaded on 8 GB |
| `l2-04-lesson-map` | The loop's four stages, each tagged with the lesson that builds it, as a promise |

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---:|
| 1 | INTRO | The finished machine, and what this lesson is | 23 |
| 2 | SLIDE 1 + 2 | The four parts, and what 8 GB costs you | 96 |
| 3 | NARRATION | The interface: no screen, no speaker, your phone | 58 |
| 4 | SLIDE 3 | Designing the body with Claude | 86 |
| 5 | DEMO | Making it work in a room | 100 |
| 6 | SLIDE 4 | What you can run tonight, and where this goes | 51 |

Total: ~414 sec (6 min 54 sec) at 156 words per minute. Recount after any edit.

The lesson now lands at just under seven minutes before any additional expansion.

---

## Beat 1: INTRO

Demo footage: the machine working, cut tight. An object it has never seen goes from an unnamed box to a named one after one spoken sentence, then the memory is deleted on camera and the same object goes unknown again.

**NARRATION:**

One sentence just turned a stranger object into a memory. A moment later, I deleted that memory—and it forgot.

That is the leap from an AI that starts from zero every time to something you can build: a system that learns, recognises, and changes over time. Over months and years, it can build a memory of your life: the objects, places, and routines that make it personal to you.

This robot starts as a home assistant. The lessons extend its memory through audio and text, toward something that could live with you, for example in smart glasses. We’ll take the build apart: four parts, one printed body, and the compute, camera, and engineering decisions that make it work in a real room.

---

## Beat 2: SLIDE 2, what compute

Slide: `l2-02-where-the-compute-goes`.

**NARRATION:**

When building a robot, start with the computer. It sets the limits for everything else.

This build uses an NVIDIA Jetson Orin Nano Super with 8 GB of memory. Its GPU runs the object detector at about 165 milliseconds a frame. On a CPU, the same work takes seconds. At that speed, a robot becomes a slideshow.

A Raspberry Pi 5 should run the same software, though You would have to accept some trade-offs: lower resolution, FPS, smaller models, decreased accuracy and response time. The idea stays the same, but the robot moves at a different pace.

I chose the Jetson because it has enough headroom for a useful live image while keeping the models on-device. It costs 249 dollars which stays fairly affordable. There is still some headroom for a bigger image encoder or a small language model to give it reasoning capabilities. 

The other parts are a USB camera, an NVMe drive, and about 300 grams of filament for the enclosure. Four parts in total, about 347 dollars.

---

## Beat 3: The interface

No slide. Demo footage: the phone view in Dylan's hand, the robot in the background with nothing on it but a camera.

**NARRATION:**

This robot has no screen, speaker, or microphone of its own. Its interface is a web page served to the phone in my hand over direct wifi. The phone is just the interface: all of the vision, speech, and memory compute happens on the robot.

That keeps the hardware simple, but it does not make the phone a performance dependency. Add a microphone or a screen to the robot and the AI would still run the same way; you would only be changing how you interact with it.

The tradeoff is that answers appear on the phone instead of coming from a speaker. If you want the robot to hear the room without the phone, add a USB microphone. The same speech model can process what it hears.

---

## Beat 4: SLIDE 3, designing the body with Claude

No slide. Claude Design UI. 

**NARRATION:**

[Showcase Claude Design, show how the design came to life]

---

## Beat 5: Making it work in a room

Demo footage: the live feed with boxes and scores, a hand entering the frame and holding the object, the box staying put.

**NARRATION:**

The hardware is only the start. A real room is harder than a notebook.

In the notebook lessons, each example starts as a single, clean image file. The robot has to process a live camera stream: objects overlap, backgrounds change, and the same object looks different from one frame to the next. The build has to turn that stream into stable memories.

Start with YOLO. It is a family of fast object-detection models that predicts what is in an image and where it is. That gives us the boxes and generic labels on screen. I use the boxes to crop objects, but I do not rely on those labels. The memory compares each crop with what I have taught it, so I can teach it names that matter to me, even an object or person YOLO was never trained to recognise.

Before the crop enters memory, I remove the background. Everything outside the object's outline becomes gray. That keeps the memory focused on the object instead of my desk, so recognition still works when the object moves.

We use Qdrant's similarity score with a recognition threshold to decide when a match is good enough. Lesson six is where you find the right threshold for your camera and room.

---

## Beat 6: SLIDE 4, what you can run tonight

Slide: `l2-04-lesson-map`.

**NARRATION:**

You do not need this hardware to follow along. Point the same code at a folder of photos instead of a camera, and the recognition path runs on your laptop.

The reusable part is the teaching loop: show the system something, say what it is, and let it keep that memory. It works anywhere you can take a picture and write a record.

Next comes the memory itself. Capture, store, recall, forget. In the next lesson, you will write those four operations yourself, starting with an empty folder and a question the system cannot answer yet.
