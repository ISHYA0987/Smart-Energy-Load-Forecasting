import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor



df = pd.read_csv(
    "data/processed/cleaned_energy_data.csv"
)

print("Dataset Shape:", df.shape)



X = df.drop(
    "Appliances",
    axis=1
)

y = df["Appliances"]



rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

print("\nTraining Random Forest...")

rf.fit(X, y)

print("Training Completed!")


importance = rf.feature_importances_

feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance")
print("=" * 50)

print(feature_importance)


feature_importance.to_csv(
    "data/processed/feature_importance.csv",
    index=False
)



plt.figure(figsize=(10, 6))

plt.barh(
    feature_importance["Feature"],
    feature_importance["Importance"]
)

plt.title(
    "Feature Importance Analysis"
)

plt.xlabel(
    "Importance Score"
)

plt.ylabel(
    "Features"
)

plt.tight_layout()

plt.savefig(
    "plots/feature_importance.png"
)

plt.show()

print("\nSaved Files:")
print("data/processed/feature_importance.csv")
print("plots/feature_importance.png")