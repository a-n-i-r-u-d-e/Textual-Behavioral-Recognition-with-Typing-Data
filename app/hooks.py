# app/hooks.py
import time
from pynput import keyboard, mouse
from app.analytics import *

event_buffer = []

keyboard_listener = None
mouse_listener = None

RUNNING=False



def on_key_press(key):
    event_buffer.append(("key", time.time(), str(key)))
    if "backspace" in str(key).lower():
        record_backspace()


def on_move(x, y):
    event_buffer.append(("move", time.time(), (x, y)))


def on_scroll(x, y, dx, dy):
    # dx, dy capture scroll direction & magnitude
    event_buffer.append(("scroll", time.time(), (dx, dy)))
    record_scroll()


def start_hooks():
    global keyboard_listener, mouse_listener
    global RUNNING
    if RUNNING:
        return
    RUNNING = True
    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    mouse_listener = mouse.Listener(
        on_move=on_move,
        on_scroll=on_scroll,   # ✅ ENABLED
        on_click=None
    )

    keyboard_listener.start()
    mouse_listener.start()

    print("[HOOKS] Listeners started")


def stop_hooks():
    global keyboard_listener, mouse_listener
    global RUNNING
    RUNNING = False

    if keyboard_listener:
        keyboard_listener.stop()
    if mouse_listener:
        mouse_listener.stop()

    print("[HOOKS] Listeners stopped")
