import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

data = pd.read_csv("dataset/pollution_data.csv")

X = data[["temperature","humidity","pm25"]]
y = data["aqi"]

model = RandomForestRegressor()
model.fit(X,y)

pickle.dump(model,open("model.pkl","wb"))

print("Model trained successfully")