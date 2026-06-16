
import torch
import torch.nn as nn



class EnergyLSTM(nn.Module):

    def __init__(self):
        super().__init__()

        self.lstm = nn.LSTM(
            input_size=12,
            hidden_size=64,
            num_layers=2,
            batch_first=True,
            dropout=0.2
        )

        self.fc1 = nn.Linear(64, 32)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(32, 1)

    def forward(self, x):

        output, (hidden, cell) = self.lstm(x)

        x = hidden[-1]

        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)

        return x