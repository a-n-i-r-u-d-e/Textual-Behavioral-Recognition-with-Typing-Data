import os
import torch
import torch.nn as nn
import torch.optim as optim
from app.gru_model import ConfusionGRU
from app.labels import LABEL_TO_IDX, IDX_TO_LABEL

class GRUWrapper:
    def __init__(self, model_path="models/gru.pt"):
        self.model_path = model_path
        self.model = ConfusionGRU()
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)
        self.loss_fn = nn.CrossEntropyLoss()

        self.X = []  # sequences
        self.y = []  # labels
        self.trained = False

        self.load()

    def add_sequence(self, seq, label):
        if len(seq) < 3:
            return
        self.X.append(torch.tensor(seq, dtype=torch.float32))
        self.y.append(LABEL_TO_IDX[label])

    def train(self):
        if len(self.X) < 5:
            return False

        self.model.train()

        X = torch.stack(self.X)
        y = torch.tensor(self.y)

        for _ in range(5):  # small epochs
            self.optimizer.zero_grad()
            logits = self.model(X)
            loss = self.loss_fn(logits, y)
            loss.backward()
            self.optimizer.step()

        self.trained = True
        self.X.clear()
        self.y.clear()
        self.save()

        return True

    def predict(self, seq):
        if not self.trained:
            return None

        self.model.eval()
        with torch.no_grad():
            x = torch.tensor(seq, dtype=torch.float32).unsqueeze(0)
            logits = self.model(x)
            idx = torch.argmax(logits, dim=1).item()
            return IDX_TO_LABEL[idx]

    def save(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        torch.save({
            "model_state": self.model.state_dict(),
            "optimizer_state": self.optimizer.state_dict()
        }, self.model_path)
        print("[GRU] Weights saved")

    def load(self):
        if os.path.exists(self.model_path):
            checkpoint = torch.load(self.model_path)
            self.model.load_state_dict(checkpoint["model_state"])
            self.optimizer.load_state_dict(checkpoint["optimizer_state"])
            self.trained = True
            print("[GRU] Weights loaded")
