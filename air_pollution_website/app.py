from flask import Flask, render_template, request
import requests
import pickle
import os

app = Flask(__name__)

# ---------------------------
# LOAD ML MODEL
# ---------------------------
model = None
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    print("Model Loaded")
except:
    print("Model not found")

# ---------------------------
# API KEY
# ---------------------------
API_KEY = "fd9ee9262822e39a91e587d80cbb302f"

# ---------------------------
# HEALTH ADVICE
# ---------------------------
def health_advice(aqi):
    if aqi <= 50:
        return "Excellent air quality 🌿"
    elif aqi <= 100:
        return "Good air quality 🙂"
    elif aqi <= 150:
        return "Moderate pollution 😐"
    elif aqi <= 200:
        return "Unhealthy air 😷"
    else:
        return "Very dangerous 🚫 Stay indoors"

# ---------------------------
# OUTDOOR TIME
# ---------------------------
def safe_time(aqi):
    if aqi <= 50:
        return "Anytime"
    elif aqi <= 100:
        return "Morning recommended"
    elif aqi <= 150:
        return "6AM - 8AM"
    else:
        return "Avoid outdoor activity"

# ---------------------------
# MAIN ROUTE
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def home():

    city = ""
    forecast = []

    pm25 = pm10 = no2 = so2 = o3 = 0
    prediction = 0
    advice = ""
    outdoor = ""
    status = "Good"

    if request.method == "POST":
        try:
            city = request.form["city"]

            # GEO API
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
            geo = requests.get(geo_url).json()

            if len(geo) == 0:
                return "City not found"

            lat = geo[0]["lat"]
            lon = geo[0]["lon"]

            # CURRENT POLLUTION
            url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
            data = requests.get(url).json()

            comp = data["list"][0]["components"]

            pm25 = comp["pm2_5"]
            pm10 = comp["pm10"]
            no2 = comp["no2"]
            so2 = comp["so2"]
            o3 = comp["o3"]

            # ---------------------------
            # ML PREDICTION
            # ---------------------------
            if model:
                prediction = model.predict([[pm25, pm10, no2, so2, o3]])[0]
            else:
                prediction = pm25 * 0.5 + pm10 * 0.2 + no2 * 0.1 + so2 * 0.1 + o3 * 0.1

            prediction = round(prediction, 2)

            # ---------------------------
            # STATUS + ADVICE
            # ---------------------------
            advice = health_advice(prediction)
            outdoor = safe_time(prediction)

            if prediction <= 50:
                status = "Good"
            elif prediction <= 100:
                status = "Moderate"
            elif prediction <= 150:
                status = "Poor"
            else:
                status = "Severe"

            # ---------------------------
            # REAL FORECAST API
            # ---------------------------
            f_url = f"https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={API_KEY}"
            f_data = requests.get(f_url).json()

            forecast = []
            for item in f_data["list"][:12]:
                forecast.append(item["main"]["aqi"])

        except Exception as e:
            print("ERROR:", e)
            return "Something went wrong"

    return render_template(
        "index.html",
        city=city,
        pm25=pm25,
        pm10=pm10,
        no2=no2,
        so2=so2,
        o3=o3,
        aqi=prediction,
        advice=advice,
        outdoor=outdoor,
        forecast=forecast,
        status=status
    )


if __name__ == "__main__":
    app.run(debug=True)
