# L2: Building the Device (script)

**Target runtime:** ~9:20
**Format:** video only, no notebook. Slides are 16:9, briefs in `SLIDES.md` in this directory. Production direction lives in the shotlist, never here.

**Objective.** Answer the question a hobbyist is already asking at the end of lesson one: could I build this? The lesson walks the build in the order it was made, and every beat is a decision, what else was on the table, and what the choice cost. It is a build lesson, not a tour of a prop, and every beat has to leave the viewer able to decide something about their own project.

**What this lesson does not do.** It does not teach thresholds, filters, coverage, or recall, all of which the student builds by hand in lessons three to six. Where the robot touches one of those, the beat names it in one sentence and points at the lesson that owns it. Its own spine is the part no notebook can show: what breaks between one clean photo in a notebook and six frames a second of a real room.

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

That is the machine from last lesson, and that is all three verbs: it learns an object from one sentence, it knows it afterwards, and the memory can be deleted.

This lesson is how it got built, in the order I built it. Four parts, one printed body, and about a week of decisions I can save you.

---

## Beat 2: SLIDE 2, what compute

Slide: `l2-02-where-the-compute-goes`.

**NARRATION:**

Start with the compute, because it decides everything downstream.

One measurement made this choice. The detector runs at about 165 milliseconds a frame on the Jetson's GPU. The same work on a CPU takes seconds a frame, and seconds a frame is not a robot, it is a slideshow.

A Raspberry Pi 5 should run all of this software, and I have not tested it. What I used is a Jetson Orin Nano Super with 8 GB, at 249 dollars. If you want a bigger image encoder or a small language model on the box, buy the 16 GB version instead.

Here is what 8 GB costs you: you do not get to keep every model loaded. Of the three encoders on this robot, only the image one is up when it boots, and speech and text load the first time you teach it or ask it something. Load all three at startup and the board runs out of memory, and then it misses the moment you are pointing at.

Three more parts. A USB camera, the kind your operating system already understands, that opens with two lines of OpenCV and no drivers. The ribbon cable modules are cheaper and they will cost you a Saturday of driver work on a board like this. An NVMe drive rather than a memory card, because every model loads off it at startup. And about 300 grams of filament. Four parts, about 347 dollars, and the board is 249 of it.

---

## Beat 3: The interface

No slide. Demo footage: the phone view in Dylan's hand, the robot in the background with nothing on it but a camera.

**NARRATION:**

Now the interface, and this is the decision I would most defend. This robot has no screen, no speaker, and no microphone of its own. The whole interface is a web page it serves to the phone in my hand, over its own wifi.

Two reasons, and both apply to whatever you build. Every part you do not add is a part that cannot fail while someone is watching. And a phone is a better interface than anything you would bolt on: a real screen, a real microphone, already in your pocket.

What it costs: the video feed to the phone becomes the weakest link, and with no speaker the robot never talks back, so answers appear on the panel. If you want it to hear the room without a phone in the loop, add a USB microphone and the same speech model runs on whatever it picks up.

---

## Beat 4: SLIDE 3, designing the body

Slide: `l2-03-the-body`.

**NARRATION:**

Then the body, and this is the part I would not have attempted two years ago.

The shell is not a model I sculpted. It is a program: a page that builds the geometry from parameters, written with Claude from a spec I wrote in plain language, and both the page and the prompt are in the repo. Which means the measurements that decide the fit are numbers in one place. If your board is a different size, you change the number and export again.

Six printed parts and no screws. A twist lock, two snap clips, one zip tie and one drop of glue. Three plates, about eight hours of printing.

Now the part worth taking away. That page checks its own work every time it loads, and it passed. And the first build still could not be assembled. The tray was 37.4 millimetres across for a 37 millimetre board, which is a fit on paper and a jam on a printer. And my own assembly instruction had the board dropping in from above, which the connectors on its back make physically impossible.

A nominal dimension is not a fit, and a generated model that passes its own checks can still be unbuildable. So the check changed: it now drives the parts along the paths they travel during assembly and demands they hit nothing.

---

## Beat 5: Making it work in a room

Demo footage: the live feed with boxes and scores, a hand entering the frame and holding the object, the box staying put.

**NARRATION:**

The hardware is only the start. The harder problem is a real room.

In the notebook lessons you get one clean photograph of one object. A room gives you a cluttered frame, several times a second. Three things bridge that.

First, a detector finds the objects and crops them out, and I throw its labels away. The memory decides which thing it is, by comparing that cut-out picture against everything it has been taught. That is why this robot can learn an object no detector has a word for, including a person.

Second, the cut-out gets its background erased before it is stored. Everything outside the object's outline is flattened to flat gray. Without that, half of what it remembers is my desk, and it stops recognising the object the moment you move it. If you have ever built a recogniser that only worked in the room you built it in, that is why.

Third, the box has to hold still. What stands out changes every frame, so two similar objects trade the highlight several times a second, and you cannot press a button on a target that keeps moving. So a new object has to be about one and a half times more prominent before it takes the highlight. Unglamorous code, and without it nobody can press the button in time.

One number, and then I leave thresholds alone. Recognition here fires at 0.90 where your notebook will use 0.80, because that number belongs to a camera and a room. Lesson six is where you find yours.

---

## Beat 6: A real question is not a nearest-neighbour query

Demo footage: the recall answer on the phone, then the "what did you see today" inventory.

**NARRATION:**

This is the design idea from the build that is most worth reusing.

When I ask when and where it last saw Potato, it is tempting to make that one big vector search. It is not, and it should not be. The words pick which object I mean out of the names I taught it, and that part is a vector search. Then the answer comes from that object's sightings, sorted by time: the newest ones, not the nearest ones. And what did you see today touches no vectors at all. It is a list of what was seen since this morning.

Similarity is for identifying the thing. Ordinary sorting and filtering answer the question about it. Push a question about time through a similarity search and you get an answer that looks reasonable and is not.

Which makes the clock part of the memory. A machine with no internet has no idea what time it is, so fit a coin cell battery, or it will stamp today's memories with the day you last packed it away.

One limit worth being straight about. Image models can search photos with a sentence, which is what you do in lesson four, and I measured it here and did not keep it: a spoken question against pictures of the room did not find the right object often enough to trust. So the words are matched against the words instead.

And if you want it to reason about what it found rather than just find it, that is where a small language model goes: on top of the memory, reading what came back.

---

## Beat 7: Making it a machine instead of a script

Demo footage: the robot with only a power cable, then the plug pulled and the same object recognised again after it comes back.

**NARRATION:**

The last step is what turns a script into something reliable enough to hand to somebody else.

It boots on its own. No keyboard, no screen, no network it depends on: it brings up its own wifi and serves the page, so it works in a hall with no internet at all. Plugging it in is the on switch.

There is also no shutdown procedure. Every time it learns something, that memory is written to disk and committed before the operation finishes, so what it has learned survives losing power.

Watch. It knows this object. Power off. Power on. It takes about a minute to come back, and it still knows it, from the files on the disk.

---

## Beat 8: SLIDE 4, what you can run tonight

Slide: `l2-04-lesson-map`.

**NARRATION:**

One last thing, and it matters more than the parts list: you do not need any of this hardware to follow along. Point the same code at a folder of photos instead of a camera and the whole recognition path runs on your laptop.

The reusable part of this build was never the board or the shell. It is that you teach the thing by showing it something and saying what it is, and it keeps it. That works anywhere you can take a picture and write a record.

Which brings us to the memory itself, the part I have been pointing at for two lessons. Capture, store, recall, forget. Starting next lesson you write those four yourself, beginning with an empty folder and a question it cannot answer yet.
