import pandas as pd

# Load combined dataset
df = pd.read_csv("final_dataset.csv")

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

print("Columns in dataset:", df.columns.tolist())

# Rename columns to simple format (if needed)
df = df.rename(columns={
    'PM2.5 (ug/m3)': 'PM2.5',
    'PM10 (ug/m3)': 'PM10',
    'NO (ug/m3)': 'NO',
    'NO2 (ug/m3)': 'NO2',
    'SO2 (ug/m3)': 'SO2'
})

# Keep only required columns
df = df[['PM2.5', 'PM10', 'NO', 'NO2', 'SO2']]

# Remove missing values
df = df.dropna()

# Save cleaned dataset
df.to_csv("cleaned_dataset.csv", index=False)

print("Cleaned dataset created successfully!")
