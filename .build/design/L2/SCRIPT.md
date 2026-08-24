# L2: Building the Device

## Beat 1: The finished robot

Demo: Hold up an object the robot has not learned. Teach it by voice, show it recognized from another view, delete the memory, then show it as unknown again.

**NARRATION:**

This robot has never seen this object. I hold TEACH and tell it what it is. The name appears. Now I show it from another view. It still knows.

Delete the memory. The same object goes back to unknown.

Nothing was retrained. The robot took one picture, listened to one sentence, and wrote one memory. This lesson takes apart what made that possible: the computer, the printed body, the phone interface, and the software between the camera and the memory.

---

## Beat 2: The parts and the computer

Slide: `l2-01-the-parts`. Use an exploded view to locate the computer, storage, camera, and enclosure in the finished robot. Keep prices secondary and do not turn the narration into a parts list on screen.

**NARRATION:**

Start with the computer. It decides how much the robot can do at once.

This build uses an NVIDIA Jetson Orin Nano Super with 8 gigabytes of memory. Its GPU runs the object detector in about 165 milliseconds per frame. On a CPU, the same detector takes seconds. In the notebooks, you can wait for one photograph to finish. A live camera does not wait.

The Jetson costs 250 dollars. I chose it to keep the live view responsive while every model runs on the device. Eight gigabytes also leaves some room to experiment. You could add a larger image encoder or put a small language model on top of the memory. Either one takes memory and compute away from the live vision loop.

A Raspberry Pi 5 has what you need to build the same idea. I would treat it as a learning build or proof of concept. You may need a smaller model, smaller images, or a lower frame rate. Interactions will take longer, and accuracy may be lower.

Add a 256 gigabyte NVMe drive, a small USB camera, and the printed enclosure. The Jetson is 250 dollars, the drive about 30, the camera about 60, and the filament about 8. The whole build comes to less than 350 dollars.

---

## Beat 3: Designing the body with Claude

Demo: Work in Claude Design, then open the generated model in the browser. Show the assembled view, the print plates, the audit, and the exported files beside the finished robot.

**NARRATION:**

I designed the body with Claude. The constraints came first: the Jetson stands on edge, the camera sits behind the eye, the ports stay accessible, and air can move through the shell.

Claude built the shape as a parametric model, so the camera and board measurements stay editable. Change those numbers, and it generates new parts around your hardware.

The page shows the assembled robot and the three print plates. It checks the meshes, the build volume, and the clearances. Then it exports individual STL files or 3MF plates that can go straight into a slicer.

There are 3 main printed parts and no screws. The plates use about 300 grams of filament and take about eight hours to print.

You still have to measure your hardware and inspect what comes out. Claude made the rest much more accessible to me. I could start by describing the robot and its constraints, work through the geometry, then print it and revise it. I did not have to master an entire CAD workflow before I could begin.

---

## Beat 4: The web interface

Demo: The robot stays in the background while the phone shows the live view, TEACH, ASK, and MEMORY. Open the memory view and show rename and forget.

**NARRATION:**

The robot has no microphone, speaker, or screen. Its interface is a web page served to a phone over its own Wi-Fi connection. The phone supplies the microphone, screen, and controls. It does not run the AI. All of the vision, speech, and memory processing runs on the robot.

The page shows the live camera, the object in focus, its match score, and the memory it found. Hold TEACH to name an unknown object. Hold ASK to ask about something it remembers. Open MEMORY and you can browse what it has learned, fix a name, or forget an object.

When I hold a voice button, the phone records the audio and uploads it. The Jetson transcribes it, creates the embeddings, and searches the memory.

Using a phone keeps the build small. Add a microphone, screen, and speaker, and the same interface could live on the robot itself. Recognition and recall would not run any faster, because that work already happens on the robot.

---

## Beat 5: From a camera frame to a memory

Slide: `l2-02-the-robot-loop`. Show the camera path and voice path converging on one memory. Use only the labels the diagram needs, then cut to the live feed and memory panel.

**NARRATION:**

The notebooks give you one clean photo. The robot gets a changing room with several objects in it. Before it can remember one, it has to separate it from everything else.

That starts with YOLOE. YOLO is a family of models that find objects in images. This version returns a box outline and an label for each thing it detects.

YOLOE can give each detection a generic label, such as "bottle." I discard that label and keep the outline. The outline tells the robot what to crop. Its memory is what recognizes this particular bottle as mine.

Each outline becomes an image crop with a small margin around it. Everything outside the outline turns gray, so less of the background enters the memory. CLIP turns that crop into a 512-number image vector.

That vector goes to Qdrant Edge. The closest learned view comes back with a score. Above 0.90, the robot recognizes it. Below 0.90, it stays unknown.

That is not 90 percent confidence. It is the threshold I calibrated for this camera and this crop. Lesson six uses 0.80 on different images, then shows you how to find yours.

The detector produces a new result for every frame, so the robot tracks objects over time. That keeps the box and the teach target stable.

Now teach it. CLIP has already made the image vector. Whisper turns my sentence into text, then Nomic turns those words into a second vector. The picture, both vectors, and the words I used become one memory. The camera can find it by sight, and a spoken question can find it through the words I taught.

---

## Beat 6: ON CAMERA, build the loop you need

No slide. End on the robot while connecting its parts to the hands-on lessons.

**NARRATION:**

You do not need this hardware to build the memory loop. Point the same recognition path at a folder of images, and it runs on a laptop without a live camera. Change the board, camera, body, or interface, and the design underneath stays the same.

Next, you create an empty memory and build the capture, store, recall, and forget loop. The later lessons add image search, voice, a full day of memories, and recognition with a threshold you calibrate yourself.

This robot is one way to put those pieces together. The next lesson starts with the memory itself.
