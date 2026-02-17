import pyautogui

def do_action(action: str):
    """
    Sends keyboard shortcuts. These are common defaults:
    - NEXT/PREV: PowerPoint/Slides
    - PLAY_PAUSE: common media toggle (space often works in YouTube, VLC uses space too)
    - VOLUME: OS-level media keys (may vary by laptop/permissions)
    """
    action = action.upper()

    if action == "NEXT":
        pyautogui.press("right")

    elif action == "PREV":
        pyautogui.press("left")

    elif action == "PLAY_PAUSE":
        pyautogui.press("space")

    elif action == "VOLUME_UP":
        pyautogui.press("volumeup")

    elif action == "VOLUME_DOWN":
        pyautogui.press("volumedown")

    else:
        print(f"[WARN] Unknown action: {action}")
