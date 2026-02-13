import time
import math


WINDOW = 20
PAUSE_THRESHOLD = 2.0

def mouse_entropy(moves):
    if len(moves) < 3:
        return 0.0

    directions = []
    for i in range(1, len(moves)):
        dx = moves[i][2][0] - moves[i-1][2][0]
        dy = moves[i][2][1] - moves[i-1][2][1]
        angle = math.atan2(dy, dx)
        directions.append(round(angle, 1))

    return len(set(directions)) / len(directions)


def extract_features(events):
    now = time.time()

    if not events:
        return _idle_features()

    window_events = [
        e for e in events
        if isinstance(e, (list, tuple))
        and len(e) >= 2
        and isinstance(e[1], (int, float))
        and now - e[1] <= WINDOW
    ]

    if not window_events:
        return _idle_features()

    key_events = [e for e in window_events if e[0] == "key"]
    moves = [e for e in window_events if e[0] == "move"]
    mouse_jitter = mouse_entropy(moves)



    backspaces = sum(
        1 for e in key_events
        if "backspace" in str(e[2]).lower()
    )

    total_keys = len(key_events)

    timestamps = sorted(e[1] for e in window_events)
    pauses = sum(
        1 for i in range(1, len(timestamps))
        if timestamps[i] - timestamps[i - 1] > PAUSE_THRESHOLD
    )

    idle_time = now - timestamps[-1]

    return {
        "backspace_rate": backspaces / max(total_keys, 1),
        "typing_speed": total_keys / WINDOW,
        "pause_rate": pauses*50 / WINDOW,
        "scroll_rate": mouse_jitter*100 / WINDOW,
        "idle_ratio": min(idle_time / WINDOW, 1.0)
    }


def _idle_features():
    return {
        "backspace_rate": 0.0,
        "typing_speed": 0.0,
        "pause_rate": 0.0,
        "scroll_rate": 0.0,
        "idle_ratio": 1.0
    }
