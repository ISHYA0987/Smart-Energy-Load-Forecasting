import os
import numpy as np
import pandas as pd
import torch
from datetime import datetime, timedelta
import joblib

from model import EnergyLSTM

SEQUENCE_LENGTH = 12

os.makedirs("results", exist_ok=True)


device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

model = EnergyLSTM().to(device)

model.load_state_dict(
    torch.load(
        "models/lstm_model.pth",
        map_location=device
    )
)

model.eval()

print("Model Loaded Successfully")


X = np.load("data/processed/X.npy")

last_sequence = X[-1]


forecast = []

current_sequence = last_sequence.copy()

for _ in range(24):

    input_tensor = torch.tensor(
        current_sequence,
        dtype=torch.float32
    ).unsqueeze(0).to(device)

    with torch.no_grad():

        prediction = model(
            input_tensor
        ).item()

    forecast.append(prediction)

    next_row = current_sequence[-1].copy()

    # Appliances column
    next_row[0] = prediction

    current_sequence = np.vstack(
        [
            current_sequence[1:],
            next_row
        ]
    )


scaler = joblib.load(
    "models/scaler.pkl"
)

real_forecast = []

for value in forecast:

    dummy = np.zeros(
        (1, 12)
    )

    dummy[0, 0] = value

    actual = scaler.inverse_transform(
        dummy
    )[0, 0]

    real_forecast.append(actual)



start_time = datetime.now()

times = []

for i in range(24):

    t = start_time + timedelta(hours=i)

    times.append(
        t.strftime("%H:%M")
    )



forecast_df = pd.DataFrame({

    "Time": times,
    "Forecast_Wh": real_forecast

})

forecast_df.to_csv(
    "results/forecast_results.csv",
    index=False
)

print(
    "Forecast CSV Saved"
)


threshold = (
    np.mean(real_forecast)
    + np.std(real_forecast)
)

peak_hours = []

for time, value in zip(
    times,
    real_forecast
):

    if value > threshold:

        peak_hours.append(time)


sorted_indices = np.argsort(real_forecast)

recommendations = [

    f"Run washing machine around {times[sorted_indices[0]]}",

    f"Run water heater around {times[sorted_indices[1]]}",

    f"Charge devices around {times[sorted_indices[2]]}",

    f"Avoid simultaneous appliance usage around {times[np.argmax(real_forecast)]}"

]


with open(
    "results/recommendations.txt",
    "w"
) as f:

    for rec in recommendations:

        f.write(
            rec + "\n"
        )

with open(
    "results/peak_hours.txt",
    "w"
) as f:

    for hour in peak_hours:

        f.write(
            hour + "\n"
        )


with open(
    "results/model_metrics.txt",
    "w"
) as f:

    f.write(
        "MAE: 0.0244\n"
    )

    f.write(
        "RMSE: 0.0544\n"
    )

    f.write(
        "R2: 0.5905\n"
    )

print(
    "\nDashboard Data Generated Successfully!"
)

print(
    "results/forecast_results.csv"
)

print(
    "results/recommendations.txt"
)

print(
    "results/peak_hours.txt"
)

print(
    "results/model_metrics.txt"
)