# Webcam Based Drum Set

Uses your webcam to detect hand drumming motions and triggers servo-mounted strikers via Arduino to hit drum pads.


---------------------------------------------------------------------

How to Run: 

git clone https://github.com/mayonike52/webcam-based-drum-set.git
cd webcam-based-drum-set

python -m venv venv
venv\Scripts\activate
pip install opencv-python mediapipe==0.10.13 pyserial

python main.py

-------------------------------------------------------------------

Upload drum_kit.ino to your Arduino, wire 3 servos to pins 3, 5, and 6, and update the COM port in main.py to match yours. (this was done on a arduino nano, but can be done with any other microcontroller model!)
