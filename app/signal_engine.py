import time
from app.notifier import notify_thinking, notify_confused

THINKING_THRESHOLD = 0.5
CONFUSED_THRESHOLD = 0.5

LAST_STATE = None
STATE_START = {}
TRIGGERED = set()


def signal(state):
    global LAST_STATE

    now = time.time()

    # State transition
    if state != LAST_STATE:
        STATE_START.clear()
        STATE_START[state] = now
        TRIGGERED.clear()
        LAST_STATE = state
        return

    duration = now - STATE_START.get(state, now)

    if state == "thinking" and duration >= THINKING_THRESHOLD and state not in TRIGGERED:
        notify_thinking()
        TRIGGERED.add(state)

    elif state == "confused" and duration >= CONFUSED_THRESHOLD and state not in TRIGGERED:
        notify_confused()
        TRIGGERED.add(state)
