import cv2
import mediapipe as mp
import serial
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

arduino = serial.Serial('COM4', 9600)
time.sleep(2)

prev_y = 0
strike_cooldown = 0

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    h, w, _ = frame.shape

    # define zones
    zone1_color = (0, 0, 255)
    zone2_color = (0, 255, 0)
    zone3_color = (255, 0, 0)

    # draw zones
    cv2.rectangle(frame, (0, 0), (w//3, h), zone1_color, 2)
    cv2.rectangle(frame, (w//3, 0), (2*w//3, h), zone2_color, 2)
    cv2.rectangle(frame, (2*w//3, 0), (w, h), zone3_color, 2)

    # labels
    cv2.putText(frame, "DRUM1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, zone1_color, 2)
    cv2.putText(frame, "DRUM2", (w//3 + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, zone2_color, 2)
    cv2.putText(frame, "DRUM3", (2*w//3 + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, zone3_color, 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            wrist = hand_landmarks.landmark[0]
            wrist_x = int(wrist.x * w)
            wrist_y = int(wrist.y * h)

            if wrist_x < w//3:
                zone = "DRUM1"
            elif wrist_x < 2*w//3:
                zone = "DRUM2"
            else:
                zone = "DRUM3"

            velocity = wrist_y - prev_y
            print(f"velocity: {velocity}  zone: {zone}")

            if velocity > 30 and strike_cooldown == 0:
                print(f"HIT {zone}!")
                if zone == "DRUM1":
                    arduino.write(b'1')
                elif zone == "DRUM2":
                    arduino.write(b'2')
                elif zone == "DRUM3":
                    arduino.write(b'3')
                strike_cooldown = 10

            prev_y = wrist_y

    if strike_cooldown > 0:
        strike_cooldown -= 1

    cv2.namedWindow("Drum Kit", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Drum Kit", 1280, 720)
    cv2.imshow("Drum Kit", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()