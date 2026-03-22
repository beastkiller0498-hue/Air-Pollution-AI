import pandas as pd

df = pd.read_csv("final_dataset.csv")

# lower case
df.columns = df.columns.str.lower()

# select only needed columns
df = df[['pm2.5 (ug/m3)','pm10 (ug/m3)','no (ug/m3)','no2 (ug/m3)','so2 (ug/m3)']]

# rename columns
df.columns = ['pm25','pm10','no','no2','so2']

# remove missing values
df = df.dropna()

df.to_csv("clean_data.csv", index=False)

print("Clean data ready ✅")
