import torch
import torch.nn as nn
from app.labels import LABELS

class ConfusionGRU(nn.Module):
    def __init__(self, input_size=5, hidden_size=32):
        super().__init__()
        self.gru = nn.GRU(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, len(LABELS))

    def forward(self, x):
        _, h = self.gru(x)
        return self.fc(h[-1])
