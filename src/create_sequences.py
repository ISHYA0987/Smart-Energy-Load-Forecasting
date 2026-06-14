import pandas as pd
import numpy as np

df = pd.read_csv(
    "data/proccessed/scaled_energy_data.csv"
)

print("Dataset Shape:", df.shape)

data = df.values

SEQUENCE_LENGTH = 24

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
    "data/proccessed/X.npy",
    X
)

np.save(
    "data/proccessed/y.npy",
    y
)

print("\nFiles Saved:")
print("data/proccessed/X.npy")
print("data/proccessed/y.npy")