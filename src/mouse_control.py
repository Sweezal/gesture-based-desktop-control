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

screen_w, screen_h = pyautogui.size()

# Mouse smoothing
prev_x, prev_y = 0, 0
smoothening = 5

# Pinch / click
pinch_start = None
dragging = False
last_release = 0
DOUBLE_CLICK_TIME = 0.35
DRAG_TIME = 0.5

# Right click
last_right_click = 0
RIGHT_CLICK_DELAY = 0.6

# Scroll (thumbs)
last_scroll = 0
SCROLL_DELAY = 0.25
SCROLL_AMOUNT = 350

# Screenshot
last_gesture = None
last_screenshot = 0
SCREENSHOT_COOLDOWN = 1.0

# ---------------- MAIN LOOP ----------------

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

        # -------- SIMPLE finger detection --------
        thumb  = lm[4].x < lm[3].x
        index  = lm[8].y < lm[6].y
        middle = lm[12].y < lm[10].y
        ring   = lm[16].y < lm[14].y
        pinky  = lm[20].y < lm[18].y

        fingers = [thumb, index, middle, ring, pinky]
        finger_count = sum(fingers)

        open_palm = finger_count == 5
        fist = finger_count == 0

        # ====================================================
        # 📸 SCREENSHOT (✋ → ✊)
        # ====================================================
        if open_palm:
            last_gesture = "palm"

        if fist and last_gesture == "palm":
            if now - last_screenshot > SCREENSHOT_COOLDOWN:
                filename = f"screenshot_{int(time.time())}.png"
                pyautogui.screenshot(filename)
                print(f"Screenshot saved: {filename}")
                last_screenshot = now
            last_gesture = None

        # ====================================================
        # 🛑 PAUSE (FIST)
        # ====================================================
        if fist:
            pinch_start = None
            continue

        # ====================================================
        # 🖱️ CURSOR MOVE (INDEX ONLY)
        # ====================================================
        if finger_count == 1 and index:
            x = int(lm[8].x * screen_w)
            y = int(lm[8].y * screen_h)

            curr_x = prev_x + (x - prev_x) / smoothening
            curr_y = prev_y + (y - prev_y) / smoothening

            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

        # ====================================================
        # 👍 👎 THUMBS SCROLL
        # ====================================================
        if thumb and not index and not middle and not ring and not pinky:
            if now - last_scroll > SCROLL_DELAY:
                if lm[4].y < lm[0].y:
                    pyautogui.scroll(SCROLL_AMOUNT)
                else:
                    pyautogui.scroll(-SCROLL_AMOUNT)
                last_scroll = now

        # ====================================================
        # 🤏 PINCH CLICK / DOUBLE CLICK / DRAG
        # ====================================================
        pinch_dist = math.hypot(
            lm[4].x - lm[8].x,
            lm[4].y - lm[8].y
        )

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

        # ====================================================
        # ✌️ RIGHT CLICK
        # ====================================================
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




'''import cv2
import mediapipe as mp
import pyautogui
import time
import math

# ---------------- SETUP ----------------

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()

# Mouse smoothing
prev_x, prev_y = 0, 0
smoothening = 5

# Pinch
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

# ---------------- MAIN LOOP ----------------

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

        # -------- SIMPLE finger detection --------
        thumb  = lm[4].x < lm[3].x
        index  = lm[8].y < lm[6].y
        middle = lm[12].y < lm[10].y
        ring   = lm[16].y < lm[14].y
        pinky  = lm[20].y < lm[18].y

        fingers = [thumb, index, middle, ring, pinky]
        finger_count = sum(fingers)

        # -------- PAUSE --------
        if finger_count == 0:
            pinch_start = None
            continue

        # ====================================================
        # 🖱️ CURSOR MOVE (INDEX ONLY)
        # ====================================================
        if finger_count == 1 and index:
            x = int(lm[8].x * screen_w)
            y = int(lm[8].y * screen_h)

            curr_x = prev_x + (x - prev_x) / smoothening
            curr_y = prev_y + (y - prev_y) / smoothening

            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

        # ====================================================
        # 👍 👎 THUMBS SCROLL
        # ====================================================
        if thumb and not index and not middle and not ring and not pinky:
            thumb_tip_y = lm[4].y
            wrist_y = lm[0].y

            if now - last_scroll > SCROLL_DELAY:
                if thumb_tip_y < wrist_y:
                    pyautogui.scroll(SCROLL_AMOUNT)     # 👍 up
                else:
                    pyautogui.scroll(-SCROLL_AMOUNT)    # 👎 down
                last_scroll = now

        # ====================================================
        # 🤏 PINCH CLICK / DOUBLE CLICK / DRAG
        # ====================================================
        pinch_dist = math.hypot(
            lm[4].x - lm[8].x,
            lm[4].y - lm[8].y
        )

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

        # ====================================================
        # ✌️ RIGHT CLICK
        # ====================================================
        if finger_count == 2 and index and middle:
            if now - last_right_click > RIGHT_CLICK_DELAY:
                pyautogui.rightClick()
                last_right_click = now

        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gesture Desktop Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()'''
