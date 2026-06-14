import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from model import EnergyLSTM


X = np.load("data/proccessed/X.npy")
y = np.load("data/proccessed/y.npy")

print("X Shape:", X.shape)
print("y Shape:", y.shape)


train_size = int(len(X) * 0.70)
val_size = int(len(X) * 0.15)

X_train = X[:train_size]
y_train = y[:train_size]

X_val = X[train_size:train_size + val_size]
y_val = y[train_size:train_size + val_size]

X_test = X[train_size + val_size:]
y_test = y[train_size + val_size:]

print("\nDataset Split")
print("=" * 40)
print("Train      :", X_train.shape)
print("Validation :", X_val.shape)
print("Test       :", X_test.shape)



X_train = torch.tensor(
    X_train,
    dtype=torch.float32
)

X_val = torch.tensor(
    X_val,
    dtype=torch.float32
)

X_test = torch.tensor(
    X_test,
    dtype=torch.float32
)

y_train = torch.tensor(
    y_train,
    dtype=torch.float32
).reshape(-1, 1)

y_val = torch.tensor(
    y_val,
    dtype=torch.float32
).reshape(-1, 1)

y_test = torch.tensor(
    y_test,
    dtype=torch.float32
).reshape(-1, 1)


train_dataset = TensorDataset(
    X_train,
    y_train
)

train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)


device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

print("\nUsing Device:", device)


model = EnergyLSTM().to(device)

criterion = nn.MSELoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

epochs = 20


train_losses = []
val_losses = []

for epoch in range(epochs):

    model.train()

    total_loss = 0

    for batch_X, batch_y in train_loader:

        batch_X = batch_X.to(device)
        batch_y = batch_y.to(device)

        optimizer.zero_grad()

        predictions = model(batch_X)

        loss = criterion(
            predictions,
            batch_y
        )

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    avg_train_loss = (
        total_loss / len(train_loader)
    )

    train_losses.append(
        avg_train_loss
    )


    model.eval()

    with torch.no_grad():

        val_predictions = model(
            X_val.to(device)
        )

        val_loss = criterion(
            val_predictions,
            y_val.to(device)
        )

    val_losses.append(
        val_loss.item()
    )

    print(
        f"Epoch {epoch+1}/{epochs} | "
        f"Train Loss: {avg_train_loss:.6f} | "
        f"Val Loss: {val_loss.item():.6f}"
    )


model.eval()

with torch.no_grad():

    test_predictions = model(
        X_test.to(device)
    )

predictions = (
    test_predictions.cpu()
    .numpy()
)

actuals = (
    y_test.cpu()
    .numpy()
)

mae = mean_absolute_error(
    actuals,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        actuals,
        predictions
    )
)

r2 = r2_score(
    actuals,
    predictions
)

print("\nModel Metrics")
print("=" * 40)

print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")



torch.save(
    model.state_dict(),
    "models/lstm_model.pth"
)

print("\nModel Saved Successfully!")


plt.figure(figsize=(8, 5))

plt.plot(
    train_losses,
    label="Train Loss"
)

plt.plot(
    val_losses,
    label="Validation Loss"
)

plt.title(
    "Training vs Validation Loss"
)

plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.legend()

plt.grid(True)

plt.savefig(
    "plots/training_validation_loss.png"
)

plt.show()

print(
    "\nGraph Saved:"
)

print(
    "plots/training_validation_loss.png"
)
