# L2: Building the Device

## Beat 1: From memory to machine
Robot on set; transition to the opened or exploded view.
**TALKING POINTS:**
- We saw it recall the bottle
- We taught it Potato
- Now: what runs where?
- Camera, computer, storage, interface
- Models + Qdrant Edge on device
- Robot = one implementation
- Take it apart

---
## Beat 2: The parts and the computer
Slide: `l2-01-the-parts`. Use an exploded view to locate the computer, storage, camera, and enclosure. Keep prices secondary.

Show the repo and, if useful, demonstrate the local setup.
**TALKING POINTS:**
- Robot hardware = example, not requirement
- Course notebooks run on a regular computer
- Robot app also has laptop mode: webcam + microphone
- Qdrant Edge and memory design are not tied to Jetson
- Raspberry Pi 5: proof of concept; smaller models/images, lower FPS
- Computer determines capacity
- Jetson Orin Nano Super, 8 GB
- GPU: ~165 ms/frame; CPU: seconds
- Live camera needs responsiveness
- ~$250; room to experiment, larger models, SLM
- Parts: 256 GB NVMe, USB camera, 3d printed enclosure, less than $350

---
## Beat 3: Designing the body with Claude
Demo: Claude Design → generated model. Show assembly, print plates, audit, exports, finished robot.
**TALKING POINTS:**
- Start with constraints, not a shape
- Camera needs a view; Jetson needs airflow; ports need access
- Claude generates a few different ideas based on constraints
- Inspect before printing: fit, airflow, printability
- Three plates; no screws
- Print → test fit → revise

---
## Beat 4: The web interface
Demo: phone live view, TEACH, ASK, MEMORY. Show rename and forget.
**TALKING POINTS:**
- No microphone, speaker, or screen on robot
- Phone UI over robot Wi-Fi
- Phone = interface only; AI stays on robot
- Show live view, target, score, recalled memory
- TEACH / ASK / MEMORY
- Voice: record → transcribe → embed → search
- Phone keeps build compact; processing stays on robot
- Add microphone, speaker, or screen; processing architecture stays the same

---
## Beat 5: From a camera frame to a memory
Slide: `l2-02-the-robot-loop`. Camera and voice paths converge on one memory.
**TALKING POINTS:**
- Camera sees a whole scene, not one clean object
- YOLOE finds objects and draws boxes
- Crop one object; add gray background
- CLIP turns crop into a vector
- Search existing image memories
- Matches above a certain threshold: recognize it
- No close match: unknown
- Teach it: save image, words, and metadata
- Later, find that memory by sight or by meaning

---
## Beat 6: ON CAMERA, build the loop you need
No slide. End on robot; connect parts to hands-on lessons.
**TALKING POINTS:**
- Hardware is example, not prerequisite
- Same path → folder of images on laptop
- Board / camera / body / interface can change; design stays
- Empty memory → capture → store → recall → forget
- Later: image search, voice, full day, threshold calibration
- Robot = one implementation
- Next lesson: memory
