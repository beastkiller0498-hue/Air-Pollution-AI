from flask import Flask, render_template, request
import requests
import pickle
import os

app = Flask(__name__)

# Load ML model
model = pickle.load(open("model.pkl", "rb"))

# Your API key
API_KEY = "fd9ee9262822e39a91e587d80cbb302f"

# Health advice
def health_advice(aqi):
    if aqi <= 2:
        return "Air quality is good"
    elif aqi <= 3:
        return "Moderate air quality"
    elif aqi <= 4:
        return "Poor air. Wear mask"
    else:
        return "Very poor air. Stay indoors"

# Safe time suggestion
def safe_time(aqi):
    if aqi <= 2:
        return "Anytime"
    elif aqi <= 3:
        return "Morning recommended"
    elif aqi <= 4:
        return "6AM - 8AM"
    else:
        return "Avoid outdoor activity"

@app.route("/", methods=["GET", "POST"])
def home():
    pm25 = pm10 = no2 = so2 = o3 = 0
    prediction = 0
    advice = ""
    outdoor = ""

    if request.method == "POST":
        city = request.form["city"]

        # Get coordinates
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        geo = requests.get(geo_url).json()

        if len(geo) == 0:
            return "❌ City not found"

        lat = geo[0]["lat"]
        lon = geo[0]["lon"]

        # Get pollution data
        pollution_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        data = requests.get(pollution_url).json()

        if "list" not in data:
            return "❌ API error"

        comp = data["list"][0]["components"]

        pm25 = comp["pm2_5"]
        pm10 = comp["pm10"]
        no2 = comp["no2"]
        so2 = comp["so2"]
        o3 = comp["o3"]

        # ML Prediction
        prediction = model.predict([[pm25, pm10, no2, so2, o3]])[0]

        advice = health_advice(prediction)
        outdoor = safe_time(prediction)

    return render_template(
        "index.html",
        pm25=pm25,
        pm10=pm10,
        no2=no2,
        so2=so2,
        o3=o3,
        aqi=round(prediction, 2),
        advice=advice,
        outdoor=outdoor
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
