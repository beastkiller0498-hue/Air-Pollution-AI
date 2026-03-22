import pandas as pd

# Load all city files
df1 = pd.read_csv("delhi.csv")
df2 = pd.read_csv("hyderabad.csv")
df3 = pd.read_csv("mumbai.csv")
df4 = pd.read_csv("kolkata.csv")
df5 = pd.read_csv("visakhapatnam.csv")

# Combine all
final_df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)

# Save new dataset
final_df.to_csv("final_dataset.csv", index=False)

print("Final dataset created successfully!")
