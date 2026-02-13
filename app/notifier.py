import threading
import tkinter as tk
import sys

# ---- Sound ----
def play_sound(level="soft"):
    try:
        if sys.platform == "win32":
            import winsound
            freq = 600 if level == "soft" else 1000
            dur = 4000 if level == "soft" else 4000
            winsound.Beep(freq, dur)
        else:
            # macOS / Linux
            import os
            os.system("afplay /System/Library/Sounds/Glass.aiff" if level == "soft" else "afplay /System/Library/Sounds/Basso.aiff")
    except Exception:
        pass


# ---- Popup ----
def popup(title, message, level="info"):
    def _show():
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        win = tk.Toplevel()
        win.title(title)
        win.geometry("320x140")
        win.configure(bg="#1e1e1e")

        color = "#ffaa00" if level == "thinking" else "#ff4444"

        label = tk.Label(
            win,
            text=message,
            fg=color,
            bg="#1e1e1e",
            font=("Segoe UI", 12),
            wraplength=280
        )
        label.pack(pady=30)

        win.after(4000, win.destroy)
        root.mainloop()

    threading.Thread(target=_show, daemon=True).start()


# ---- Public API ----
def notify_thinking():
    popup(
        "Thinking detected",
        "You seem to be thinking for a while.\nNeed help?",
        "thinking"
    )
    play_sound("soft")
    


def notify_confused():
    popup(
        "Confusion detected",
        "You look stuck.\nWould you like assistance?",
        level="confused"
    )
    play_sound("urgent")
    
