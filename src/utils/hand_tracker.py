import cv2
import mediapipe as mp

class HandTracker:
    """
    Wraps MediaPipe Hands:
    - detect hand landmarks (21 points)
    - draw them on the frame
    """
    def __init__(self, max_hands: int = 1, detection_conf: float = 0.6, tracking_conf: float = 0.6):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf,
        )

    def process(self, frame_bgr):
        """
        Returns:
          results: MediaPipe results object
          frame_rgb: converted RGB frame (used internally by mediapipe)
        """
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        results = self.hands.process(frame_rgb)
        frame_rgb.flags.writeable = True
        return results, frame_rgb

    def draw(self, frame_bgr, results):
        if not results.multi_hand_landmarks:
            return frame_bgr

        for hand_landmarks in results.multi_hand_landmarks:
            self.mp_draw.draw_landmarks(
                frame_bgr,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS
            )
        return frame_bgr
