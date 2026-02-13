# app/state_engine.py
from collections import deque
from app.rules import is_idle

HISTORY = deque(maxlen=5)

def aggregate(features, rf, gru, sequence):
    if is_idle(features):
        return "idle"

    rf_state = rf.predict(list(features.values()))

    if gru.trained and sequence:
        gru_state, conf = gru.predict(sequence)
        if conf > 0.7:
            return gru_state

    return rf_state

def confirm(state):
    HISTORY.append(state)
    for s in ["confused", "thinking"]:
        if HISTORY.count(s) >= 3:
            return s
    return state
