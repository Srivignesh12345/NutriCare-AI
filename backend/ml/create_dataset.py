import pandas as pd
import numpy as np

np.random.seed(42)

rows = 500  # number of records

data = {
    "Age": np.random.randint(18, 40, rows),
    "SystolicBP": np.random.randint(90, 160, rows),
    "DiastolicBP": np.random.randint(60, 100, rows),
    "BS": np.random.uniform(6.0, 15.0, rows),
    "BodyTemp": np.random.uniform(97.0, 102.0, rows),
    "HeartRate": np.random.randint(60, 120, rows)
}

df = pd.DataFrame(data)

# -----------------------------
# Risk Level Logic (LABEL CREATION)
# -----------------------------
def classify_risk(row):
    if (
        row["SystolicBP"] > 140
        or row["DiastolicBP"] > 90
        or row["BS"] > 11
        or row["BodyTemp"] > 100
        or row["HeartRate"] > 100
    ):
        return "High"
    elif (
        row["SystolicBP"] > 120
        or row["DiastolicBP"] > 80
        or row["BS"] > 8
    ):
        return "Medium"
    else:
        return "Low"

df["RiskLevel"] = df.apply(classify_risk, axis=1)

# -----------------------------
# Save Dataset
# -----------------------------
df.to_excel("data/Maternal_Health_Risk_Dataset.xlsx", index=False)

print("✅ Dataset created successfully")
print(df.head())
