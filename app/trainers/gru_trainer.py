from app.gru_wrapper import GRUWrapper

class GRUTrainer:
    def __init__(self):
        self.gru = GRUWrapper()
        self.train_steps = 0

    def add_sequence(self, sequence, label):
        if label != "idle":
            self.gru.add_sequence(sequence, label)

    def maybe_train(self):
        if self.gru.train():
            self.train_steps += 1
            return True
        return False

    def stats(self):
        return {
            "gru_trained": self.gru.trained,
            "gru_pending_sequences": len(self.gru.X),
            "gru_train_steps": self.train_steps
        }
