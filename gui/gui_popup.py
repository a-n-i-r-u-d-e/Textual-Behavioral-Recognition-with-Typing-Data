import time
import requests
import threading
import tkinter as tk
from tkinter import messagebox
import winsound  # Windows

API = "http://127.0.0.1:8000/state"

last_state = None
state_start = {}

def play_sound():
    winsound.Beep(1000, 300)

def poll_state():
    global last_state

    while True:
        try:
            r = requests.get(API, timeout=1).json()
            state = r.get("state", "idle")

            now = time.time()

            if state != last_state:
                state_start[state] = now
                last_state = state
                continue

            duration = now - state_start.get(state, now)

            if state == "thinking" and duration > 20:
                show_popup("Thinking too long 🤔")
            elif state == "confused" and duration > 30:
                show_popup("User is confused 🚨")

        except Exception:
            pass

        time.sleep(2)


def show_popup(msg):
    play_sound()
    messagebox.showwarning("Confusion Detector", msg)


def start():
    root = tk.Tk()
    root.withdraw()  # Hide main window

    threading.Thread(target=poll_state, daemon=True).start()
    root.mainloop()


if __name__ == "__main__":
    start()
