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
    if aqi <= 50:
        return "Good air quality 🌿"
    elif aqi <= 100:
        return "Moderate air quality 🙂"
    elif aqi <= 150:
        return "Unhealthy for sensitive groups 😐"
    elif aqi <= 200:
        return "Unhealthy 😷"
    else:
        return "Very dangerous 🚫 Stay indoors"

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

            # GEO LOCATION
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
            geo = requests.get(geo_url).json()

            if not geo:
                return "❌ City not found"

            lat = geo[0]["lat"]
            lon = geo[0]["lon"]

            # CURRENT AIR DATA
            url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
            data = requests.get(url).json()

            if "list" not in data:
                return "❌ API error"

            comp = data["list"][0]["components"]

            pm25 = comp.get("pm2_5", 0)
            pm10 = comp.get("pm10", 0)
            no = comp.get("no", 0)
            no2 = comp.get("no2", 0)
            so2 = comp.get("so2", 0)

            # ---------------------------
            # ML PREDICTION (REAL)
            # ---------------------------
            try:
                if model:
                    prediction = model.predict([[pm25, pm10, no, no2, so2]])[0]
                else:
                    prediction = pm25 * 0.6 + pm10 * 0.2 + no2 * 0.1 + so2 * 0.1
            except:
                prediction = pm25 * 0.6 + pm10 * 0.2 + no2 * 0.1 + so2 * 0.1

            prediction = round(prediction, 2)

            # STATUS + ADVICE
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
            # REAL FORECAST (FIXED)
            # ---------------------------
            forecast = []

            try:
                f_url = f"https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={API_KEY}"
                f_data = requests.get(f_url).json()

                if "list" in f_data:
                    for item in f_data["list"][:12]:

                        comp_f = item["components"]

                        pm25_f = comp_f.get("pm2_5", 0)
                        pm10_f = comp_f.get("pm10", 0)
                        no2_f = comp_f.get("no2", 0)
                        so2_f = comp_f.get("so2", 0)

                        # REAL AQI CALCULATION
                        aqi_val = pm25_f * 0.6 + pm10_f * 0.2 + no2_f * 0.1 + so2_f * 0.1

                        forecast.append(round(aqi_val, 2))
                else:
                    forecast = [prediction] * 12

            except:
                forecast = [prediction] * 12

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
