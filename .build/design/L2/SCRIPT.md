# L2: Building the Device

## Beat 1: From memory to machine
Robot on set; transition to the opened or exploded view.
**TALKING POINTS:**
- We saw the robot recall my watch
- We taught it Potato
- Now let’s look at how it was built
- Camera, computer, storage, and interface
- Models and Qdrant Edge run inside the application
- No separate vector database server
- Memory stored in a local directory
- Robot is one implementation
- Take it apart

---
## Beat 2: The parts and the computer
Show the GitHub repository, hardware files, parts, and the opened robot.
**TALKING POINTS:**
- Everything is available in the GitHub repository: code, parts list, enclosure files, and setup
- You do not need the robot hardware for this course
- In the next lessons, you’ll run the same memory design directly in your browser
- This robot uses an NVIDIA Jetson Orin Nano Super with 8 GB of memory
- This can run on a Raspberry Pi 5 or any computer
- Depending on the compute available, may need smaller models and a lower frame rate
- Continuous camera processing needs more compute than searching stored memories
- Other parts: NVMe SSD, USB camera, and 3D-printed enclosure
- Jetson: about $250; complete build: less than $350
- Computer and storage determine how much the device can remember

---
## Beat 3: Designing the body with Claude
Show `hardware/l6-bot-v54.html` in the repository, import it into Claude Design, and explore the model.
**TALKING POINTS:**
- The repository includes the complete design as an HTML file
- Import the file into Claude Design
- Start with a working model instead of a blank canvas
- Traditional CAD tools take time to learn
- Claude lets you describe changes in natural language
- Change the shape, dimensions, openings, or arrangement
- Explore several approaches quickly
- Adapt the body to different hardware or a different use case
- No need to learn a traditional CAD workflow first
- Physical constraints still matter
- Exact dimensions, airflow, access, and printability
- Inspect the model and its audit before exporting
- More freedom to build a device around your own idea

---
## Beat 4: The phone interface
Demo: phone live view, TEACH, ASK, MEMORY. Show rename and forget.
**TALKING POINTS:**
- No microphone, speaker, or screen on the robot
- Phone connects over the robot’s Wi-Fi
- Phone is the interface; processing stays on the robot
- Live camera view
- Selected object and recognition score
- TEACH: give an object a personal name
- ASK: record a question
- MEMORY: review, rename, or forget what was stored
- Phone keeps the physical build compact
- Could add a microphone, speaker, or screen instead
- Memory architecture stays the same

---
## Beat 5: From a camera frame to a memory
Slide: `l2-02-the-robot-loop`. Camera and voice paths converge on one memory.
**TALKING POINTS:**
- Camera sees a complete scene
- YOLOE finds and separates the objects
- Tracking keeps focus on one object
- Crop the object and replace its background with gray
- CLIP turns the crop into an image vector
- Compare it with the taught image vectors
- Score at or above 0.90 → recognized
- Below 0.90 → unknown
- To teach it: select the object and speak
- Whisper Transcribe the words and create a text vector
- Store the image vector, text vector, and payload together
- Later, find the memory by sight or by meaning

---
## Beat 6: ON CAMERA, from this robot to your device
End on the robot and transition to the hands-on lessons.
**TALKING POINTS:**
- Goal: memory, not this exact robot
- Robot = one complete example
- Smart glasses
- Security system
- Home assistant
- Field device
- Different cameras, sensors, and interfaces
- Same memory loop underneath
- Here Decide what your device should remember
- Next lesson: build the core memory loop
