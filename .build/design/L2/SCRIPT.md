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
| `l2-03-the-body` | The six printed parts, exploded, with the three measurements that decide the fit |
| `l2-04-lesson-map` | The loop's four stages, each tagged with the lesson that builds it, as a promise |

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---:|
| 1 | INTRO | The finished machine, and what this lesson is | 23 |
| 2 | SLIDE 1 + 2 | The four parts, and what 8 GB costs you | 96 |
| 3 | NARRATION | The interface: no screen, no speaker, your phone | 58 |
| 4 | SLIDE 3 | Designing the body as a program | 86 |
| 5 | DEMO | Making it work in a room | 100 |
| 6 | DEMO | A real question is not a nearest-neighbour query | 104 |
| 7 | DEMO | Making it a machine instead of a script | 46 |
| 8 | SLIDE 4 | What you can run tonight, and where this goes | 51 |

Total: ~564 sec (9 min 24 sec) at 156 words per minute, 1,466 words of narration measured from the narration blocks below. Recount after any edit.

**To reach 7:30**, in this order: cut beat 6's small-language-model paragraph (18 sec), beat 3's cost paragraph (22 sec), beat 2's Raspberry Pi sentence (8 sec), beat 5's recogniser-that-only-worked-in-one-room line (14 sec), beat 8's laptop paragraph (16 sec), beat 4's parts-and-glue list (12 sec). Beats 4, 5, and 6 are never cut below their core: the audit that passed on an unbuildable part, the three things that bridge notebook and room, and similarity-then-sorting.

---

## Beat 1: INTRO

Demo footage: the machine working, cut tight. An object it has never seen goes from an unnamed box to a named one after one spoken sentence, then the memory is deleted on camera and the same object goes unknown again.

**NARRATION:**

One sentence just turned a stranger object into a memory. A moment later, I deleted that memory—and it forgot.

That is the leap from an AI that starts from zero every time to one that learns, recognises, and changes with you. Over the years, it can become personal—remembering the objects, places, and routines of your life.

Today, it’s a home assistant. Add audio and text, and that same memory could follow you through smart glasses.

---

## Beat 2: SLIDE 2, what compute

Slide: `l2-02-where-the-compute-goes`.

**NARRATION:**

Start with the computer. It sets the limits for everything else.

This build uses an NVIDIA Jetson Orin Nano Super with 8 GB of memory. Its GPU runs the object detector at about 165 milliseconds a frame. On a CPU, the same work takes seconds. At that speed, a robot becomes a slideshow.

A Raspberry Pi 5 should run the software too, though I have not tested it. You would need to reduce the workload: smaller frames, lower resolution and FPS, and smaller models. Accuracy and response time may suffer. The idea stays the same, but the robot moves at a different pace.

I chose the Jetson because it has enough headroom for a useful live image while keeping the models on-device. It costs 249 dollars. The 16 GB version gives you room for a bigger image encoder or a small language model.

The other parts are a USB camera, an NVMe drive, and about 300 grams of filament for the enclosure. Four parts in total, about 347 dollars.

---

## Beat 3: The interface

No slide. Demo footage: the phone view in Dylan's hand, the robot in the background with nothing on it but a camera.

**NARRATION:**

This robot has no screen, speaker, or microphone of its own. Its interface is a web page served to the phone in my hand over its own wifi.

The reasons apply to whatever you build. Fewer parts mean fewer things that can fail during a demo. A phone also gives you a better screen and microphone than anything you would bolt onto the robot.

The tradeoff is that the phone becomes the weak link for video, and answers appear on the screen instead of coming from a speaker. If you want the robot to hear the room without the phone, add a USB microphone. The same speech model can process what it hears.

---

## Beat 4: SLIDE 3, designing the body

Slide: `l2-03-the-body`.

**NARRATION:**

The body is the part I would not have attempted two years ago.

The shell is not a model I sculpted. It is a program that builds the geometry from parameters. I wrote the spec in plain language with Claude, and the page and prompt are in the repo. The fit measurements live in one place, so if your board is a different size, you change a number and export again.

There are six printed parts and no screws: a twist lock, two snap clips, one zip tie, and a drop of glue. The three plates take about eight hours to print.

The page checks its own work every time it loads, and it passed. The first build still could not be assembled. The tray was 37.4 millimetres across for a 37 millimetre board, which is a fit on paper and a jam on a printer. My assembly instructions also said to drop the board in from above, even though its rear connectors make that impossible.

A nominal dimension is not a fit. A generated model can pass its own checks and still be unbuildable. The check now moves the parts along their actual assembly paths and requires zero interference.

---

## Beat 5: Making it work in a room

Demo footage: the live feed with boxes and scores, a hand entering the frame and holding the object, the box staying put.

**NARRATION:**

The hardware is only the start. A real room is harder than a notebook.

In the notebook lessons, you get one clean photograph of one object. In a room, the frame is cluttered and changes several times a second. Three parts of the build handle that gap.

A detector finds the objects and crops them out, but I throw away its labels. The memory identifies each crop by comparing it with everything it has been taught. That lets the robot learn an object the detector has no name for, including a person.

Before the crop is stored, the background is erased. Everything outside the object's outline becomes flat gray. Otherwise, half the memory is my desk, and recognition breaks as soon as the object moves. If you have built a recogniser that only worked in one room, this is the same problem.

The box also has to hold still. What stands out changes every frame, so similar objects can trade the highlight several times a second. A new object has to be about one and a half times more prominent before it takes over. It is unglamorous code, but without it nobody can press the button in time.

One number, then I will leave thresholds alone. Recognition here fires at 0.90. Your notebook uses 0.80 because the right number depends on the camera and the room. Lesson six is where you find yours.

---

## Beat 6: A real question is not a nearest-neighbour query

Demo footage: the recall answer on the phone, then the "what did you see today" inventory.

**NARRATION:**

This is the design idea from the build I would reuse first.

When I ask when and where it last saw Potato, the words first pick the object from the names I taught it. That part is a vector search. The answer then comes from that object's sightings, sorted by time. "What did you see today?" uses no vectors. It is a list of what the robot has seen since this morning.

Use similarity to identify the thing. Use ordinary sorting and filtering to answer questions about it. If you use similarity to answer a question about time, you can get an answer that sounds reasonable but is wrong.

That makes the clock part of the memory. A machine with no internet has no idea what time it is. Fit a coin cell battery, or it will stamp today's memories with the day you last packed it away.

There is one limit to call out. Image models can search photos with a sentence, which is what you do in lesson four. I tested that approach here and did not keep it because a spoken question against pictures of the room did not find the right object often enough to trust. The words are matched against the words instead.

If you want the system to reason about what it found, a small language model can sit on top of the memory and read the results.

---

## Beat 7: Making it a machine instead of a script

Demo footage: the robot with only a power cable, then the plug pulled and the same object recognised again after it comes back.

**NARRATION:**

The last step makes the script reliable enough to hand to somebody else.

It boots on its own. It needs no keyboard, screen, or outside network. It brings up its own wifi and serves the page, so it works in a hall with no internet. Plugging it in is the on switch.

There is no shutdown procedure either. Each new memory is written to disk and committed before the operation finishes, so what the robot learned survives a loss of power.

It knows this object. Power off, then power on. It takes about a minute to come back, and it still knows the object from the files on disk.

---

## Beat 8: SLIDE 4, what you can run tonight

Slide: `l2-04-lesson-map`.

**NARRATION:**

You do not need this hardware to follow along. Point the same code at a folder of photos instead of a camera, and the recognition path runs on your laptop.

The reusable part is the teaching loop: show the system something, say what it is, and let it keep that memory. It works anywhere you can take a picture and write a record.

Next comes the memory itself. Capture, store, recall, forget. In the next lesson, you will write those four operations yourself, starting with an empty folder and a question the system cannot answer yet.
