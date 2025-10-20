import pandas as pd

# Load your collected data
data = pd.read_csv("irrigation_data.csv", encoding="latin1")

# Rename columns for safety (if needed)
data.columns = ["Timestamp", "Soil", "Temperature", "Humidity", "Pump"]

# Drop missing or invalid rows
data = data.dropna()

# Add derived label (PumpNeeded)
data["PumpNeeded"] = data["Soil"].apply(lambda x: 1 if x < 40 else 0)

# Normalize sensor values (optional)
data["Soil"] = data["Soil"] / 100.0
data["Temperature"] = (data["Temperature"] - data["Temperature"].min()) / (data["Temperature"].max() - data["Temperature"].min())
data["Humidity"] = data["Humidity"] / 100.0

# Save the new trained dataset
data.to_csv("irrigation_trained_dataset.csv", index=False)

print("✅ Trained dataset created successfully: irrigation_trained_dataset.csv")
print(data.head())
