from flask import Flask, render_template, request
import requests
import pickle
import os
import random

app = Flask(__name__)

# ---------------------------
# LOAD ML MODEL
# ---------------------------
model = None
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    print("Model loaded")
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
    if aqi <= 30:
        return "Excellent air quality 🌿"
    elif aqi <= 60:
        return "Good air quality 🙂"
    elif aqi <= 100:
        return "Moderate air quality 😐"
    elif aqi <= 150:
        return "Unhealthy for sensitive groups ⚠️"
    elif aqi <= 200:
        return "Unhealthy 😷"
    else:
        return "Very dangerous 🚫"

# ---------------------------
# OUTDOOR SUGGESTION
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

    pm25 = pm10 = no = no2 = so2 = 0
    prediction = 0
    advice = ""
    outdoor = ""
    status = "Good"

    if request.method == "POST":
        try:
            city = request.form["city"]

            # GEO API
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
            geo_response = requests.get(geo_url, timeout=10)

            if geo_response.status_code != 200:
                return "❌ Location API failed"

            geo = geo_response.json()

            if len(geo) == 0:
                return "❌ City not found"

            lat = geo[0]["lat"]
            lon = geo[0]["lon"]

            # POLLUTION API
            pollution_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
            response = requests.get(pollution_url, timeout=10)

            if response.status_code != 200:
                return "❌ API failed"

            data = response.json()

            if "list" not in data or len(data["list"]) == 0:
                return "❌ No pollution data"

            comp = data["list"][0]["components"]

            pm25 = comp["pm2_5"]
            pm10 = comp["pm10"]
            no = comp["no"]
            no2 = comp["no2"]
            so2 = comp["so2"]

            # ---------------------------
            # ML PREDICTION
            # ---------------------------
            try:
                if model is not None:
                    prediction = model.predict([[pm25, pm10, no, no2, so2]])[0]
                else:
                    prediction = (pm25 + pm10 + no + no2 + so2) / 5
            except:
                prediction = (pm25 + pm10 + no + no2 + so2) / 5

            prediction = round(prediction, 2)

            # ---------------------------
            # ADVICE
            # ---------------------------
            advice = health_advice(prediction)
            outdoor = safe_time(prediction)

            # ---------------------------
            # STATUS
            # ---------------------------
            if prediction <= 50:
                status = "Good"
            elif prediction <= 100:
                status = "Moderate"
            else:
                status = "Poor"

            # ---------------------------
            # REAL FORECAST API
            # ---------------------------
            forecast = []

            f_url = f"https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={API_KEY}"
            f_response = requests.get(f_url, timeout=10)

            if f_response.status_code == 200:
                f_data = f_response.json()

                if "list" in f_data:
                    for item in f_data["list"][:12]:
                        forecast.append(item["main"]["aqi"])
            else:
                forecast = ["No data"]

        except Exception as e:
            print("ERROR:", e)
            return "❌ Something went wrong"

    return render_template(
        "index.html",
        city=city,
        pm25=pm25,
        pm10=pm10,
        no=no,
        no2=no2,
        so2=so2,
        aqi=prediction,
        advice=advice,
        outdoor=outdoor,
        forecast=forecast,
        status=status
    )

# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
