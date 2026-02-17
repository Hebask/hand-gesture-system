import time
from dataclasses import dataclass

@dataclass
class GestureFilter:
    stable_frames: int = 8
    cooldown_sec: float = 1.0

    _last_gesture: str = "NONE"
    _count: int = 0
    _last_trigger_time: float = 0.0

    def update(self, gesture: str) -> str | None:
        """
        Feed the current frame's gesture.
        Returns a confirmed gesture string when:
          - stable for N frames, AND
          - cooldown passed
        Otherwise returns None.
        """
        now = time.time()

        if gesture == self._last_gesture:
            self._count += 1
        else:
            self._last_gesture = gesture
            self._count = 1

        # Only trigger for known gestures (avoid UNKNOWN/NO_HAND spam)
        if gesture in ("UNKNOWN", "NO_HAND", "NONE"):
            return None

        if self._count >= self.stable_frames:
            if (now - self._last_trigger_time) >= self.cooldown_sec:
                self._last_trigger_time = now
                # reset count so it won’t immediately retrigger
                self._count = 0
                return gesture

        return None
