import pandas as pd
import numpy as np

df = pd.read_csv(
    "data/processed/scaled_energy_data.csv"
)

print("Dataset Shape:", df.shape)

data = df.values

SEQUENCE_LENGTH = 12

X = []
y = []

for i in range(len(data) - SEQUENCE_LENGTH):

    
    X.append(
        data[i:i + SEQUENCE_LENGTH]
    )

    
    y.append(
        data[i + SEQUENCE_LENGTH][0]
    )

X = np.array(X)
y = np.array(y)

print("\nSequence Creation Completed")
print("X shape:", X.shape)
print("y shape:", y.shape)


np.save(
    "data/processed/X.npy",
    X
)

np.save(
    "data/processed/y.npy",
    y
)

print("\nFiles Saved:")
print("data/processed/X.npy")
print("data/processed/y.npy")