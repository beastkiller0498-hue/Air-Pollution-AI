import pandas as pd

# Load dataset
df = pd.read_csv("final_dataset.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower()

print("Columns:", df.columns.tolist())

# Select correct columns
df = df[['pm25', 'pm10', 'no', 'no2', 'so2']]

# Drop missing values
df = df.dropna()

# Save cleaned dataset
df.to_csv("cleaned_dataset.csv", index=False)

print("Cleaned dataset created successfully!")
