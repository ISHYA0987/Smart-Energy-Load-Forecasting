import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(
    r"C:\Users\ishya b\Desktop\SELF\data\processed\cleaned_energy_data.csv"
)

#print(df.head())
#print(df.describe())

#Distribution of energy consumption
# plt.figure(figsize=(8,5))
# sns.histplot(df["Appliances"], bins=50, kde=True)
# plt.title("Distribution of Energy Consumption")
# plt.xlabel("Appliances")
# plt.show()

#correlation analaysis
plt.figure(figsize=(12,8))

sns.heatmap(
    df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Matrix")
plt.show()

corr_target = df.corr()["Appliances"].sort_values(ascending=False)

print(corr_target)