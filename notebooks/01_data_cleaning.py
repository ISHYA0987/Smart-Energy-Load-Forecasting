import pandas as pd
df = pd.read_csv("C:/Users/ishya b/Desktop/SELF/data/raw/energydata_complete.csv")
print("Dataset Loaded Successfully")

print("\nShape of Dataset:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nData Types:")
print(df.dtypes)

print("\nDuplicate Rows:")
print(df.duplicated().sum())

df["date"] = pd.to_datetime(df["date"])

df["hour"] = df["date"].dt.hour

df["day_of_week"] = df["date"].dt.dayofweek

df["month"] = df["date"].dt.month

df["is_weekend"] = (
    df["day_of_week"] >= 5
).astype(int)

selected_features = [
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

df = df[selected_features]

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())

output_path = r"C:\Users\ishya b\Desktop\SELF\data\proccessed\cleaned_energy_data.csv"

df.to_csv(output_path, index=False)

print("\nCleaned Dataset Saved Successfully")
print(f"Location: {output_path}")