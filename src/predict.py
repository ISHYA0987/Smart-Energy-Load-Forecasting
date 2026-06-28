import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import joblib
from model import EnergyLSTM
# ==========================
# LSTM MODEL
# ==========================




# ==========================
# LOAD MODEL
# ==========================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model = EnergyLSTM().to(device)

model.load_state_dict(
    torch.load(
        "models/lstm_model.pth",
        map_location=device
    )
)

model.eval()

# ==========================
# LOAD SCALER
# ==========================

scaler = joblib.load(
    "models/scaler.pkl"
)

# ==========================
# LOAD SCALED DATA
# ==========================

df = pd.read_csv(
    "data/processed/scaled_energy_data.csv"
)

# Last 24 records
last_sequence = df.values[-24:]

last_sequence = np.expand_dims(
    last_sequence,
    axis=0
)

last_sequence = torch.tensor(
    last_sequence,
    dtype=torch.float32
).to(device)

# ==========================
# PREDICT
# ==========================

with torch.no_grad():

    prediction = model(
        last_sequence
    )

scaled_prediction = prediction.item()

print(
    "\nScaled Prediction:",
    scaled_prediction
)

# ==========================
# INVERSE SCALE
# ==========================

dummy = np.zeros(
    (1, 12)
)

dummy[0][0] = scaled_prediction

actual_prediction = scaler.inverse_transform(
    dummy
)[0][0]

print(
    "\nPredicted Appliance Consumption:"
)

print(
    f"{actual_prediction:.2f} Wh"
)

if actual_prediction > 300:

    print("\nPeak Load Alert")

    print(
        "Recommendation: Avoid heavy appliances."
    )

elif actual_prediction > 150:

    print("\nModerate Load")

    print(
        "Recommendation: Use appliances carefully."
    )

else:

    print("\nLow Load")

    print(
        "Recommendation: Good time to run washing machine, iron, or charge devices."
    )