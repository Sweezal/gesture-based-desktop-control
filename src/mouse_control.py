import cv2
import mediapipe as mp
import pyautogui
import time
import math

# ---------------- SETUP ----------------

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Click / pinch
pinch_start = None
dragging = False
last_release = 0
DOUBLE_CLICK_TIME = 0.35
DRAG_TIME = 0.5

# Right click
last_right_click = 0
RIGHT_CLICK_DELAY = 0.6

# Scroll
last_scroll = 0
SCROLL_DELAY = 0.25
SCROLL_AMOUNT = 350

# Screenshot
last_gesture = None
last_screenshot = 0
SCREENSHOT_COOLDOWN = 1.0
screenshot_triggered = False

# Cursor control (stable)
prev_ix = None
prev_iy = None
smooth_dx = 0
smooth_dy = 0

SENSITIVITY = 1600
SMOOTHING = 0.25
DEAD_ZONE = 0.002
MAX_STEP = 40

# ---------------- MAIN LOOP ---------------

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        lm = hand.landmark
        now = time.time()

        # -------- FINGER DETECTION --------
        thumb  = lm[4].x < lm[3].x
        index  = lm[8].y < lm[6].y
        middle = lm[12].y < lm[10].y
        ring   = lm[16].y < lm[14].y
        pinky  = lm[20].y < lm[18].y

        fingers = [thumb, index, middle, ring, pinky]
        finger_count = sum(fingers)

        open_palm = finger_count == 5
        fist = finger_count == 0

        
        # SCREENSHOT 
        
        if open_palm:
            last_gesture = "palm"
            screenshot_triggered = False

        if fist and last_gesture == "palm" and not screenshot_triggered:
            if now - last_screenshot > SCREENSHOT_COOLDOWN:
                pyautogui.screenshot(f"screenshot_{int(time.time())}.png")
                print("Screenshot taken")
                last_screenshot = now
            screenshot_triggered = True
            last_gesture = None

        
        # PAUSE (FIST)
        
        if fist:
            prev_ix = None
            prev_iy = None
            smooth_dx = 0
            smooth_dy = 0
            pinch_start = None
            continue

        
        #  CURSOR MOVE 
        
        if finger_count == 1 and index:
            ix, iy = lm[8].x, lm[8].y

            if prev_ix is None:
                prev_ix, prev_iy = ix, iy
            else:
                dx = ix - prev_ix
                dy = iy - prev_iy

                if abs(dx) < DEAD_ZONE:
                    dx = 0
                if abs(dy) < DEAD_ZONE:
                    dy = 0

                smooth_dx = smooth_dx * (1 - SMOOTHING) + dx * SMOOTHING
                smooth_dy = smooth_dy * (1 - SMOOTHING) + dy * SMOOTHING

                move_x = smooth_dx * SENSITIVITY
                move_y = smooth_dy * SENSITIVITY

                move_x = max(-MAX_STEP, min(MAX_STEP, move_x))
                move_y = max(-MAX_STEP, min(MAX_STEP, move_y))

                pyautogui.moveRel(move_x, move_y, duration=0)

                prev_ix, prev_iy = ix, iy
        else:
            prev_ix = None
            prev_iy = None
            smooth_dx = 0
            smooth_dy = 0

        
        # SCROLL 
        
        if thumb and not index and not middle and not ring and not pinky:
            if now - last_scroll > SCROLL_DELAY:
                if lm[4].y < lm[0].y:
                    pyautogui.scroll(SCROLL_AMOUNT)
                else:
                    pyautogui.scroll(-SCROLL_AMOUNT)
                last_scroll = now

        
        # CLICK / DOUBLE CLICK / DRAG
        
        pinch_dist = math.hypot(lm[4].x - lm[8].x, lm[4].y - lm[8].y)

        if pinch_dist < 0.04:
            if pinch_start is None:
                pinch_start = now
            elif not dragging and (now - pinch_start) > DRAG_TIME:
                pyautogui.mouseDown()
                dragging = True
        else:
            if pinch_start is not None:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False
                else:
                    if now - last_release < DOUBLE_CLICK_TIME:
                        pyautogui.doubleClick()
                        last_release = 0
                    else:
                        pyautogui.click()
                        last_release = now
                pinch_start = None

        
        #  RIGHT CLICK
        
        if finger_count == 2 and index and middle:
            if now - last_right_click > RIGHT_CLICK_DELAY:
                pyautogui.rightClick()
                last_right_click = now

        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gesture Desktop Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()







