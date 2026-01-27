import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# Finger tip landmark indices
FINGER_TIPS = [4, 8, 12, 16, 20]

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark

            fingers = []

            hand_label = results.multi_handedness[0].classification[0].label

            # Thumb logic based on hand type
            if hand_label == "Right":
                if lm[4].x < lm[3].x:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:  # Left hand
                if lm[4].x > lm[3].x:
                    fingers.append(1)
                else:
                    fingers.append(0)


            # Other fingers (y-axis comparison)
            for tip in FINGER_TIPS[1:]:
                if lm[tip].y < lm[tip - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Display finger states
            cv2.putText(
                frame,
                f"Fingers: {fingers}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow("Finger Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
