import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib


df = pd.read_csv("data/processed/cleaned_energy_data.csv")

features = [
    "Appliances",
    "T_out",
    "RH_out",
    "Windspeed",
    "T1",
    "RH_1",
    "T2",
    "RH_2",
    "hour",
    "day_of_week",
    "month",
    "is_weekend"
]

df = df[features]


scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df)


joblib.dump(scaler, "models/scaler.pkl")


scaled_df = pd.DataFrame(
    scaled_data,
    columns=features
)

scaled_df.to_csv(
    "data/processed/scaled_energy_data.csv",
    index=False
)

print("Scaling completed!")
print(scaled_df.head())
