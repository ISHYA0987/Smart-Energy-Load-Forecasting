import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import joblib
from datetime import datetime, timedelta
from model import EnergyLSTM

# ==========================
# MODEL DEFINITION
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
# LOAD DATA
# ==========================

df = pd.read_csv(
    "data/processed/scaled_energy_data.csv"
)

# Last 24 timesteps
current_sequence = df.values[-24:]

forecast = []

# ==========================
# FORECAST NEXT 24 HOURS
# ==========================

for hour in range(24):

    input_sequence = np.expand_dims(
        current_sequence,
        axis=0
    )

    input_tensor = torch.tensor(
        input_sequence,
        dtype=torch.float32
    ).to(device)

    with torch.no_grad():

        prediction = model(
            input_tensor
        )

    scaled_prediction = prediction.item()

    # Convert prediction back to real units
    dummy = np.zeros((1, 12))
    dummy[0][0] = scaled_prediction

    actual_prediction = scaler.inverse_transform(
        dummy
    )[0][0]

    forecast.append(actual_prediction)

    # Create next row
    next_row = current_sequence[-1].copy()

    # Update Appliances value only
    next_row[0] = scaled_prediction

    # Slide window
    current_sequence = np.vstack(
        [
            current_sequence[1:],
            next_row
        ]
    )

# ==========================
# DISPLAY RESULTS
# ==========================

print("\n24 Hour Forecast")
print("=" * 40)
start_time = datetime.now()

forecast_times = []

for i in range(24):
    forecast_times.append(
        start_time + timedelta(hours=i+1)
    )

for i, value in enumerate(forecast):

    print(
        f"{forecast_times[i].strftime('%H:%M')} -> {value:.2f} Wh"
    )

# ==========================
# PEAK DETECTION
# ==========================
peak_threshold = np.mean(forecast) + np.std(forecast)

print(f"\nPeak Threshold: {peak_threshold:.2f} Wh")

peak_hours = []

for i, value in enumerate(forecast, start=1):

    if value > peak_threshold:
        peak_hours.append(i)

print("\nPeak Hours")

if peak_hours:

    for hour in peak_hours:
        print(
            forecast_times[hour - 1].strftime("%H:%M")
        )

else:
    print("No peak hours detected")

# ==========================
# RECOMMENDATIONS
# ==========================
print("\nSMART RECOMMENDATIONS")
print("=" * 40)

# Get hours sorted by lowest load
sorted_indices = np.argsort(forecast)

# Top 3 lowest-load hours
best_hours = sorted_indices[:3]

print("\nRecommended Low Load Windows:")

for idx in best_hours:

    time_str = forecast_times[idx].strftime("%H:%M")

    print(
        f"{time_str} -> {forecast[idx]:.2f} Wh"
    )

# Peak hours
print("\nAvoid Heavy Appliance Usage:")

for idx in np.argsort(forecast)[-3:]:

    time_str = forecast_times[idx].strftime("%H:%M")

    print(
        f"{time_str} -> {forecast[idx]:.2f} Wh"
    )

print("\nSuggested Activities")

print("✓ Washing Machine: Use during low-load windows")
print("✓ Device Charging: Use during low-load windows")
print("✓ Water Heater: Use during low-load windows")
print("✗ Avoid running multiple heavy appliances during peak hours")

import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))

plt.plot(
    forecast,
    marker="o"
)

plt.title(
    "24 Hour Energy Forecast"
)

plt.xlabel("Forecast Hour")

plt.ylabel(
    "Energy Consumption (Wh)"
)

plt.grid(True)

plt.savefig(
    "plots/forecast_24h.png"
)

plt.show()
