import cv2

from src.utils.hand_tracker import HandTracker
from src.utils.gestures import detect_gesture
from src.utils.gesture_filter import GestureFilter
from src.utils.actions import do_action
from src.config import STABLE_FRAMES, COOLDOWN_SEC, GESTURE_ACTIONS


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam. Try changing VideoCapture(0) to (1).")

    tracker = HandTracker(max_hands=1, detection_conf=0.6, tracking_conf=0.6)
    gf = GestureFilter(stable_frames=STABLE_FRAMES, cooldown_sec=COOLDOWN_SEC)

    last_confirmed = "NONE"

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        h, w = frame.shape[:2]
        results, _ = tracker.process(frame)

        gesture = "NO_HAND"
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            gesture = detect_gesture(hand_landmarks, w, h)

        # Draw landmarks
        frame = tracker.draw(frame, results)

        # Confirm gesture (stable + cooldown)
        confirmed = gf.update(gesture)
        if confirmed:
            last_confirmed = confirmed
            action = GESTURE_ACTIONS.get(confirmed)
            if action:
                do_action(action)

        # On-screen info
        cv2.putText(frame, f"Gesture: {gesture}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.putText(frame, f"Last Trigger: {last_confirmed}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.putText(frame, f"StableFrames={STABLE_FRAMES} Cooldown={COOLDOWN_SEC}s",
                    (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Gesture Actions - Press Q to quit", frame)

        if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
