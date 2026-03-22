import pandas as pd

df = pd.read_csv("final_dataset.csv")

# lower case
df.columns = df.columns.str.lower()

# select only needed columns
df = df[['PM2.5', 'PM10', 'NO', 'NO2', 'SO2']]

# rename columns
df.columns = ['pm25','pm10','no','no2','so2']

# remove missing values
df = df.dropna()

df.to_csv("clean_data.csv", index=False)

print("Clean data ready ✅")
