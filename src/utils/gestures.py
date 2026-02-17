from __future__ import annotations
import math

# MediaPipe landmark indices
TIP = {"thumb": 4, "index": 8, "middle": 12, "ring": 16, "pinky": 20}
PIP = {"index": 6, "middle": 10, "ring": 14, "pinky": 18}
MCP = {"index": 5, "middle": 9, "ring": 13, "pinky": 17}

WRIST = 0
THUMB_MCP = 2
INDEX_MCP = 5


def _xy(lm, w: int, h: int):
    return (lm.x * w, lm.y * h)


def _dist(a, b) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _palm_scale(lm, w: int, h: int) -> float:
    wrist = _xy(lm[WRIST], w, h)
    mid_mcp = _xy(lm[9], w, h)  # middle finger MCP
    return _dist(wrist, mid_mcp) + 1e-6


def finger_states(hand_landmarks, w: int, h: int):
    """
    Robust finger extension:
    - Primary: tip y < pip y (good when palm faces camera)
    - Fallback: tip->mcp distance > pip->mcp distance * factor (better when tilted)
    - Thumb: distance-based
    """
    lm = hand_landmarks.landmark
    scale = _palm_scale(lm, w, h)

    states = {}

    # 4 fingers
    for f in ["index", "middle", "ring", "pinky"]:
        tip = _xy(lm[TIP[f]], w, h)
        pip = _xy(lm[PIP[f]], w, h)
        mcp = _xy(lm[MCP[f]], w, h)

        primary = tip[1] < pip[1]
        d_tip = _dist(tip, mcp) / scale
        d_pip = _dist(pip, mcp) / scale
        fallback = d_tip > (d_pip * 1.15)

        states[f] = primary or fallback

    # thumb (distance-based)
    thumb_tip = _xy(lm[TIP["thumb"]], w, h)
    thumb_mcp = _xy(lm[THUMB_MCP], w, h)
    index_mcp = _xy(lm[INDEX_MCP], w, h)

    d1 = _dist(thumb_tip, thumb_mcp) / scale
    d2 = _dist(thumb_tip, index_mcp) / scale
    states["thumb"] = (d1 > 0.55) and (d2 > 0.35)

    return states


def detect_gesture(hand_landmarks, w: int, h: int) -> str:
    """
    Gestures:
      - OPEN_PALM (4 fingers open; thumb optional)
      - FIST
      - PEACE
      - PINCH
      - THUMBS_UP / THUMBS_DOWN
    """
    lm = hand_landmarks.landmark
    scale = _palm_scale(lm, w, h)

    s = finger_states(hand_landmarks, w, h)

    wrist = _xy(lm[WRIST], w, h)
    thumb_tip = _xy(lm[TIP["thumb"]], w, h)
    index_tip = _xy(lm[TIP["index"]], w, h)

    # pinch
    pinch_dist = _dist(thumb_tip, index_tip) / scale
    is_pinch = pinch_dist < 0.22

    # thumb vertical direction (relative to wrist)
    dy = (thumb_tip[1] - wrist[1]) / scale
    thumb_is_up = dy < -0.45
    thumb_is_down = dy > 0.45

    # OPEN PALM (4 fingers open)
    four_open = s["index"] and s["middle"] and s["ring"] and s["pinky"]
    if four_open and not is_pinch:
        return "OPEN_PALM"

    # FIST (4 fingers closed; thumb optional)
    four_closed = (not s["index"]) and (not s["middle"]) and (not s["ring"]) and (not s["pinky"])
    if four_closed and (not s["thumb"]):
        return "FIST"

    # Peace
    if s["index"] and s["middle"] and (not s["ring"]) and (not s["pinky"]):
        return "PEACE"

    # Pinch
    if is_pinch:
        return "PINCH"

    # Thumbs
    if s["thumb"] and four_closed:
        if thumb_is_up:
            return "THUMBS_UP"
        if thumb_is_down:
            return "THUMBS_DOWN"
        return "THUMB_ONLY"

    # fallback
    if four_closed:
        return "FIST"
    if four_open:
        return "OPEN_PALM"

    return "UNKNOWN"
