# Gesture Based Desktop Control (Windows)

This project is a real-time hand gesture based desktop control system built using Python and computer vision.  
It allows basic desktop operations like mouse movement, clicking, scrolling, and taking screenshots using only hand gestures captured through a webcam.

The main goal of this project was to understand hand tracking, gesture logic, and human–computer interaction, while building something that actually works in real time.

---

## What this project does

Using a webcam, the system detects hand landmarks and maps specific gestures to desktop actions such as:

- Moving the mouse cursor  
- Clicking and dragging  
- Scrolling up and down  
- Taking screenshots  

All gestures were designed carefully to avoid conflicts and accidental triggers.

---

## Gesture Controls

| Gesture | Action |
|------|------|
| Index finger | Move cursor |
| Pinch (thumb + index) | Single click |
| Quick double pinch | Double click |
| Hold pinch | Drag |
| Index + Middle finger | Right click |
| Thumbs up | Scroll up |
| Thumbs down | Scroll down |
| Open palm → Fist | Take screenshot |
| Fist | Pause all actions |
| Open palm | Neutral (no action) |

---

## Tech Used

- Python  
- OpenCV  
- MediaPipe  
- PyAutoGUI  

---

## Project Structure

```text
gesture-based-desktop-control/
│
├── src/
│   └── mouse_control.py
│
├── screenshots/
│   └── sample.png
│
├── demo/
│   └── demo.mp4
│
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE

How to Run:

Clone the repository:

git clone https://github.com/<your-username>/gesture-based-desktop-control.git
cd gesture-based-desktop-control


(Optional but recommended) Create virtual environment:

python -m venv venv
venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Run the program:

python src/mouse_control.py


Make sure your webcam is working and there is good lighting for better gesture detection.


Challenges Faced:

Designing gestures that do not conflict with each other

Handling false detections and jitter

Managing performance and system lag on Windows

Debugging gesture priority and edge cases

Most of the time went into debugging and stabilizing the system rather than just adding features.

What I Learned:

Real-time hand landmark detection using MediaPipe

Gesture logic and priority handling

Practical use of computer vision in system-level applications

Debugging performance issues in CV-based projects

Possible Improvements

Support for multiple hands

Customizable gestures

Volume and brightness control

Cross-platform support

License:

This project is licensed under the MIT License.

Note:

This project was built as a learning-focused and practical implementation, not as a commercial product.
The emphasis was on making it stable, usable, and understandable.

⭐ If you found this interesting, feel free to star the repository.