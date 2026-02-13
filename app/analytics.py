from collections import defaultdict
import time

# ---- Cognitive state tracking ----
state_time = defaultdict(float)
state_count = defaultdict(int)

LAST_STATE = None
LAST_TS = None

# ---- Interaction metrics ----
daily_metrics = {
    "scroll_time": 0.0,
    "backspaces": 0,
}

LAST_SCROLL_TS = None
SCROLL_GAP = 0.4  # seconds → defines a scroll session

def record_state(state):
    global LAST_STATE, LAST_TS

    now = time.time()

    # First ever call
    if LAST_STATE is None:
        LAST_STATE = state
        LAST_TS = now
        state_count[state] += 1
        return

    # Always accumulate time for previous state
    elapsed = now - LAST_TS
    state_time[LAST_STATE] += elapsed

    # Handle transition
    if state != LAST_STATE:
        state_count[state] += 1
        LAST_STATE = state

    LAST_TS = now

def record_scroll():
    global LAST_SCROLL_TS

    now = time.time()

    if LAST_SCROLL_TS and now - LAST_SCROLL_TS < SCROLL_GAP:
        daily_metrics["scroll_time"] += now - LAST_SCROLL_TS

    LAST_SCROLL_TS = now

def record_backspace():
    daily_metrics["backspaces"] += 1
    
def snapshot():
    return {
        "thinking_time_sec": round(state_time["thinking"], 1),
        "confused_time_sec": round(state_time["confused"], 1),

        "thinking_sessions": state_count["thinking"],
        "confused_sessions": state_count["confused"],

        "scroll_time_sec": round(daily_metrics["scroll_time"], 1),
        "backspaces": daily_metrics["backspaces"],
    }

