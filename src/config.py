# How many consecutive frames must match before we "confirm" a gesture
STABLE_FRAMES = 8

# Minimum seconds between triggers (prevents repeated firing)
COOLDOWN_SEC = 1.0

# Actions mapping:
GESTURE_ACTIONS = {
    "PEACE": "NEXT",        # next slide
    "FIST": "PREV",         # previous slide
    "THUMBS_UP": "VOLUME_UP",
    "THUMBS_DOWN": "VOLUME_DOWN",
    "PINCH": "PLAY_PAUSE",
}
