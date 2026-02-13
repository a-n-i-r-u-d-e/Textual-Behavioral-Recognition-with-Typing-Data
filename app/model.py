import os
import joblib
from sklearn.ensemble import RandomForestClassifier

class ConfusionModel:
    def __init__(self, model_path="models/rf.joblib"):
        self.model_path = model_path
        self.model = RandomForestClassifier(
            n_estimators=150,
            max_depth=8,
            random_state=42
        )
        self.X = []
        self.y = []
        self.trained = False

        self.load()

    def save(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({
            "model": self.model,
            "X": self.X,
            "y": self.y
        }, self.model_path)

    def load(self):
        if os.path.exists(self.model_path):
            data = joblib.load(self.model_path)
            self.model = data["model"]
            self.X = data["X"]
            self.y = data["y"]
            self.trained = True
            print("[RF] Loaded saved model")

    def train(self, X, y):
        self.X = X
        self.y = y
        self.model.fit(X, y)
        self.trained = True
        self.save()

    def update(self, X_new, y_new):
        self.X.extend(X_new)
        self.y.extend(y_new)

        if len(self.X) > 2000:
            self.X = self.X[-2000:]
            self.y = self.y[-2000:]

        self.model.fit(self.X, self.y)
        self.trained = True
        self.save()

    def predict(self, features):
        if not self.trained:
            return "idle"
        return self.model.predict([features])[0]
