from app.model import ConfusionModel
from app.synthetic import generate_synthetic

class RFTrainer:
    def __init__(self, retrain_threshold=10):
        self.model = ConfusionModel()
        self.buffer_X = []
        self.buffer_y = []
        self.retrain_threshold = retrain_threshold
        self.total_feedback_used = 0

    def bootstrap(self, samples=500):
        data = generate_synthetic(samples)
        X = [d[:-1] for d in data]
        y = [d[-1] for d in data]
        self.model.train(X, y)

    def add_sample(self, features, label):
        self.buffer_X.append(features)
        self.buffer_y.append(label)

        if len(self.buffer_X) >= self.retrain_threshold:
            self.model.update(self.buffer_X, self.buffer_y)
            self.total_feedback_used += len(self.buffer_X)
            self.buffer_X.clear()
            self.buffer_y.clear()
            return True

        return False

    def stats(self):
        return {
            "rf_trained": self.model.trained,
            "rf_samples": len(self.model.X),
            "rf_buffer": len(self.buffer_X),
            "total_feedback_used": self.total_feedback_used,
            "retrain_threshold": self.retrain_threshold
        }
