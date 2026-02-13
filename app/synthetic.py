import random

def generate_synthetic(n=1000):
    data = []
    for _ in range(n):
        state = random.choice(["fluent", "thinking", "confused", "idle"])
        if state == "fluent":
            data.append([0.05, 4.0, 0, 1, 0, state])
        elif state == "thinking":
            data.append([0.1, 2.0, 2, 1, 0, state])
        elif state == "confused":
            data.append([0.4, 1.5, 3, 5, 1, state])
        else:
            data.append([0, 0, 0, 0, 0, state])
    return data
