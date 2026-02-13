import tkinter as tk
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

API_STATS = "http://127.0.0.1:8000/analytics"
API_STATE = "http://127.0.0.1:8000/state"

root = tk.Tk()
root.title("🧠 Confusion Analytics Dashboard")
root.geometry("900x600")

state_label = tk.Label(root, text="State: --", font=("Arial", 16))
state_label.pack(pady=5)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

def update():
    try:
        stats = requests.get(API_STATS).json()
        state = requests.get(API_STATE).json()["state"]

        state_label.config(text=f"Live State: {state.upper()}")

        # ---- Pie: Thinking vs Confused ----
        ax1.clear()
        ax1.pie(
            [stats["thinking"], stats["confused"], stats["idle"]],
            labels=["Thinking", "Confused", "Idle"],
            autopct="%1.1f%%"
        )
        ax1.set_title("Cognitive States")

        # ---- Bar: Interaction ----
        ax2.clear()
        ax2.bar(
            ["Backspaces", "Typing Events"],
            [stats["backspaces"], stats["typing_events"]]
        )
        ax2.set_title("Interaction Activity")

        canvas.draw()

    except Exception:
        pass

    root.after(3000, update)

update()
root.mainloop()
