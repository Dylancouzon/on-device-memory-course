# L2: Building the Device (script)

**Target runtime:** ~6:45
**Format:** video only, no notebook. Slides are 16:9. Briefs will be written in `SLIDES.md` in this directory after the script is locked. Production direction belongs in the shotlist.

**Objective.** Show how the robot is put together and make the build feel achievable. By the end, viewers should understand what the computer, camera, printed body, web interface, detector, embedding models, and memory each do. They should also know which parts they could change in a build of their own.

**Scope.** This is the course's embodiment lesson. It explains the complete robot at system level, but leaves the memory operations, filters, recall code, and threshold calibration to lessons three through six. The student does not need the robot or its hardware to follow the course.

**STATUS: PROVISIONAL.** The robot app and hardware exist; the shoot does not. Every number below comes from the robot repo and must be checked against the recorded footage before the script is locked. Numbers shown on screen are evidence. The narration must not claim more than the footage shows.

**Sourced claims, with their limits:**

- The Jetson Orin Nano Super 8 GB costs $249. YOLOE runs at roughly 165 ms per frame on its GPU and takes seconds per frame on CPU.
- A Raspberry Pi 5 has the parts needed to run the software, but this build has not been tested on one. It is presented as a learning or proof-of-concept option with lower resolution, frame rate, smaller models, or slower responses.
- A larger image encoder or small language model is an extension to explore, not a tested configuration. Either would compete with the detector for memory and compute.
- The parts are a Jetson at $249, a 256 GB NVMe at about $30, a 37 x 37 mm USB camera at about $60, and about 300 g of filament at about $8. The total is roughly $347.
- The enclosure has six printed parts and uses no screws. Its three print plates take about eight hours. The robot documentation still says "about a day and a half" and must be corrected before this ships.
- The enclosure is a parametric model in one HTML file. It opens in Chrome, generates the geometry in the browser, audits the printable parts, and exports STL and 3MF files.
- The robot has no built-in microphone, speaker, or screen. A phone browser records and uploads audio. The Jetson performs the transcription, embedding, recognition, and memory work.
- YOLOE finds object regions and segmentation masks. The app discards its class labels. Detection finds a thing; memory decides which thing it is.
- The image sent to CLIP has a 12 percent margin around the detection. Pixels outside the segmentation mask are replaced with gray.
- A stable object is tracked across frames, and focus stays on it until another object is clearly more prominent.
- The robot's calibrated recognition threshold is 0.90. The lesson six notebook uses 0.80 with its own images. The number belongs to the camera and crop pipeline, and it is not a confidence percentage.
- The recognition path can run from a folder of images on a laptop, with no camera or robot body.

## Slides

| Slug | Idea |
|---|---|
| `l2-01-the-parts` | The four purchased or printed parts, their jobs, and the $347 total |
| `l2-02-the-robot-loop` | Camera through detection and image memory, plus phone audio through speech and text memory |
| `l2-03-lesson-map` | The same loop tagged with the hands-on lesson that builds each part |

## Beat map

| # | Type | Content | Est. sec |
|---|---|---|---:|
| 1 | DEMO | An unknown object is taught, recognized, then forgotten | 30 |
| 2 | SLIDE 1 | Choosing the computer, camera, storage, and body | 82 |
| 3 | DEMO | Designing and exporting the printed body with Claude | 68 |
| 4 | DEMO | The phone web interface and where the work runs | 55 |
| 5 | SLIDE 2 + DEMO | How a camera frame becomes a personal memory | 120 |
| 6 | SLIDE 3 | What viewers can build without this robot | 50 |

Total: ~405 sec (6 min 45 sec) at 156 words per minute. Recount after any edit.

---

## Beat 1: The finished robot

Demo: Hold up an object the robot has not learned. Teach it by voice, show it recognized from another view, delete the memory, then show it as unknown again.

**NARRATION:**

This robot has never seen this object. I hold the teach button and tell it what it is. Now the name appears beside it. I can show it again from another view and it still knows what I taught it.

Delete that memory, and the same object becomes unknown again.

There was no training run in between. The robot took a picture, listened to one sentence, and wrote a memory. This lesson is about everything around that moment: the parts, the printed body, the phone interface, and the software that connects a live camera to memory.

---

## Beat 2: The parts and the computer

Slide: `l2-01-the-parts`.

**NARRATION:**

The computer sets the pace of the robot, so that is where I started.

This build uses an NVIDIA Jetson Orin Nano Super with 8 gigabytes of memory. Its GPU runs the object detector in about 165 milliseconds per frame. The same detector takes seconds per frame on a CPU. That difference matters when the input is a camera rather than one photograph.

The Jetson costs 249 dollars. I chose it for a responsive live view with all of the models running on the device. Eight gigabytes also leaves some room to experiment. A larger image encoder or a small language model could sit on top of the memory, but either one would take memory and compute away from the live vision loop.

A Raspberry Pi 5 has what you need to build the same idea, though I have not tested this software on one. I would treat it as a learning build or proof of concept. You may need a smaller model, smaller images, or a lower frame rate, and interactions will take longer.

The other parts are a 256 gigabyte NVMe drive, a small USB camera, and the printed enclosure. The Jetson is 249 dollars, the drive about 30, the camera about 60, and the filament about 8. The complete build comes to roughly 347 dollars.

---

## Beat 3: Designing the body with Claude

Demo: Work in Claude Design, then open the generated model in the browser. Show the assembled view, the print plates, the audit, and the exported files beside the finished robot.

**NARRATION:**

The body was designed with Claude. I started with the hardware that had to fit: the Jetson standing on edge, the camera behind the eye, access to the ports, and enough open space for cooling.

The model is built by code in a single HTML file. It generates the geometry in the browser, with the important measurements kept as parameters. Change the camera or board dimensions, and you can generate the parts again.

The page shows the assembled robot and three print plates. It checks the meshes, build volume, and clearances, then exports individual STL files or ready-to-slice 3MF plates.

There are six printed parts and no screws. A twist lock and two clips hold the body together. One zip tie secures the camera cable, and the visor takes a drop of glue. The plates use about 300 grams of filament and take about eight hours to print.

You still have to measure your hardware and inspect the result. The difference is that you do not have to begin with a blank CAD screen. I could describe the robot, work through the geometry with Claude, then print and revise it myself.

---

## Beat 4: The web interface

Demo: The robot stays in the background while the phone shows the live view, TEACH, ASK, and MEMORY. Open the memory view and show rename and forget.

**NARRATION:**

The robot has no microphone, speaker, or screen. A phone supplies the microphone, screen, and controls through a web page served by the Jetson over its own Wi-Fi connection. Answers appear on the phone rather than coming from a speaker.

The page shows the live camera, the object in focus, its match score, and the memory it matched. Hold TEACH to name an unknown object. Hold ASK to ask about something it remembers. The MEMORY view shows everything it has learned, with controls to rename a label or forget it.

When I hold one of the voice buttons, the phone records the audio and uploads it. The Jetson transcribes it and runs the embedding and memory search. The phone is the interface, not the computer running the AI.

This keeps the physical build small and gives it a screen, microphone, and touch controls that are easy to change. You could attach those parts to the robot later without changing the memory underneath.

---

## Beat 5: From a camera frame to a memory

Slide: `l2-02-the-robot-loop`, followed by the live feed and memory panel.

**NARRATION:**

A notebook starts with a clean photo. The robot sees a changing room, with several objects in the frame at once. It needs to separate those objects before it can remember any of them.

YOLOE handles that first step. YOLO is a family of models for finding objects in images. This version returns a box and an outline for each object it detects.

YOLOE can also produce generic class names, but this app throws them away. The detector only needs to answer, "Where is a thing?" The memory answers, "Which thing is it?" That is how the robot can learn my bottle or my keyboard instead of stopping at a generic category such as bottle or keyboard.

Each outline becomes its own image crop, with a small margin around it. Everything outside the outline is replaced with gray so less of the desk and the room enters the memory. CLIP then turns that crop into a 512-number image vector.

The robot searches those numbers against the views it has already learned in Qdrant Edge. If the nearest score clears 0.90, the object is recognized. That score is a similarity measurement, not 90 percent confidence. The robot uses 0.90 because it was calibrated for this camera and this crop pipeline. In lesson six, the notebook uses 0.80 with a different set of images, and you will measure the right threshold for your own.

The detector produces a new answer on every pass, so the robot also tracks objects across frames. An object has to remain stable before it can be selected or embedded. Once selected, it keeps the focus until something else is clearly more prominent. That gives you time to reach for the teach button without the target changing underneath your finger.

When I teach an unknown object, Whisper turns my sentence into text and Nomic turns that text into a second vector. The image vector, the text vector, the picture, and the words I used are written into one memory. From then on, the camera can find that memory by sight, and a spoken question can find it through the words I taught.

---

## Beat 6: Build the loop you need

Slide: `l2-03-lesson-map`.

**NARRATION:**

You do not need this hardware to build the memory loop. The same recognition path can read a folder of images on a laptop instead of a live camera. You can replace the board, camera, body, or interface and keep the same basic design.

In the next lesson, you will create an empty memory and build the capture, store, recall, and forget loop. Later lessons add image search, voice, a full day of memories, and recognition with a threshold you calibrate yourself.

The robot is one way to package those pieces. The next lesson starts with the memory itself.
