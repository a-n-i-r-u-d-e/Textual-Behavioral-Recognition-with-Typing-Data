from collections import deque

class FeatureSequenceBuffer:
    def __init__(self, max_len=10):
        self.buffer = deque(maxlen=max_len)

    def add(self, features: dict):
        self.buffer.append(list(features.values()))

    def is_ready(self):
        return len(self.buffer) == self.buffer.maxlen

    def get_sequence(self):
        return list(self.buffer)

    def clear(self):
        self.buffer.clear()
