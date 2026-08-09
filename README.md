# AirCanvas
 AirCanvas – Virtual Air Writing System

AirCanvas is a computer vision-based virtual drawing board that allows users to draw and write in the air using hand gestures.

The system uses a webcam to detect the user's hand, tracks hand landmarks in real time, and converts finger movements into digital strokes on a virtual canvas. No physical pen, touchscreen, or drawing board is required.

🚀 Features

- ✋ Real-time hand tracking using a webcam
- 🖊️ Draw/write in the air using the index finger
- 🎨 Color palette for selecting different drawing colors
- 🧹 Eraser using a thumb-index finger pinch gesture
- ↩️ Undo the previous drawing using Z
- 🗑️ Clear the entire canvas using C
- 🖥️ Large virtual canvas with a 1280×720 board
- ⚡ Real-time drawing with OpenCV
- 👋 Visual hand skeleton/landmarks displayed on screen

🛠️ Technologies Used

- Python
- OpenCV – Image processing and camera handling
- MediaPipe Tasks – Real-time hand landmark detection
- NumPy – Numerical operations
- Webcam – Captures real-time hand movements

📂 Project Structure

AirCanvas/
│
├── main.py
├── config.py
├── requirements.txt
├── hand_landmarker.task
│
├── drawing/
│   └── ...
│
├── gestures/
│   └── ...
│
└── hand_tracking/
    └── ...

⚙️ How It Works

1. The webcam captures the user's hand in real time.
2. MediaPipe detects the hand and identifies its landmarks.
3. The system tracks the position of the index finger.
4. The index finger movement is converted into drawing strokes.
5. The strokes are rendered on the virtual canvas using OpenCV.
6. Hand gestures are detected to perform additional actions such as erasing and clearing.

✏️ Drawing

Move your index finger through the air to draw on the virtual canvas.

🧹 Eraser

Use a thumb-index finger pinch gesture to activate the eraser.

↩️ Undo

Press:

Z

to undo the previous drawing.

🗑️ Clear

Press:

C

to clear the entire canvas.

📦 Installation

Clone the repository:

git clone https://github.com/shreshtagupta/AirCanvas.git
cd AirCanvas

Install the required dependencies:

pip install -r requirements.txt

Make sure the "hand_landmarker.task" model file is present in the project directory.

▶️ Running the Project

Run:

python main.py

Allow the application to access your webcam.

Once the camera starts, place your hand in front of the camera and use your index finger to write or draw in the air.

🎯 Applications

AirCanvas can be used for:

- Virtual whiteboards
- Online teaching
- Interactive presentations
- Touchless interfaces
- Gesture-based computer interaction
- Digital art
- Educational applications

🔮 Future Improvements

- Add more gesture-based controls
- Add shape recognition
- Add text recognition
- Add save/export functionality
- Add multiple brush sizes
- Add more color options
- Improve gesture accuracy
- Add support for multiple hands

👩‍💻 Author

Shreshta Gupta 

---

⭐ If you find this project interesting, consider giving the repository a star!
