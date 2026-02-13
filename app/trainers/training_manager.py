from app.trainers.rf_trainer import RFTrainer
from app.trainers.gru_trainer import GRUTrainer

class TrainingManager:
    def __init__(self):
        self.rf = RFTrainer()
        self.gru = GRUTrainer()

    def bootstrap(self):
        self.rf.bootstrap()

    def add_feedback(self, features, label, sequence=None):
        rf_retrained = self.rf.add_sample(features, label)

        if sequence is not None:
            self.gru.add_sequence(sequence, label)

        self.gru.maybe_train()

        return rf_retrained

    def stats(self):
        stats = {}
        stats.update(self.rf.stats())
        stats.update(self.gru.stats())
        return stats
