import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Load cleaned dataset
df = pd.read_csv("cleaned_dataset.csv")

# Features & target
X = df[['pm25', 'pm10', 'no', 'no2', 'so2']]
y = df['pm25']  # or any target you want

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
model = LinearRegression()
model.fit(X_train, y_train)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained successfully!")
