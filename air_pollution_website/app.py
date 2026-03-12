from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your OpenWeather API key
API_KEY = "fd9ee9262822e39a91e587d80cbb302f"


# Health advice function
def health_advice(aqi):
    if aqi <= 2:
        return "Air quality is good"
    elif aqi <= 3:
        return "Moderate air quality"
    elif aqi <= 4:
        return "Poor air. Wear mask"
    else:
        return "Very poor air. Stay indoors"


# Safe outdoor time suggestion
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

    city = None
    pm25 = pm10 = no2 = so2 = o3 = 0
    prediction = 0
    advice = ""
    outdoor = ""
    forecast = []

    if request.method == "POST":

        city = request.form["city"]

        # Get city coordinates
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        geo = requests.get(geo_url).json()

        lat = geo[0]["lat"]
        lon = geo[0]["lon"]

        # Get current pollution data
        pollution_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        data = requests.get(pollution_url).json()

        comp = data["list"][0]["components"]

        pm25 = comp["pm2_5"]
        pm10 = comp["pm10"]
        no2 = comp["no2"]
        so2 = comp["so2"]
        o3 = comp["o3"]

        prediction = data["list"][0]["main"]["aqi"]

        advice = health_advice(prediction)
        outdoor = safe_time(prediction)

        # Get 12 hour forecast
        forecast_url = f"https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={API_KEY}"
        forecast_data = requests.get(forecast_url).json()

        for i in range(12):
            forecast.append(forecast_data["list"][i]["main"]["aqi"])

    return render_template(
        "index.html",
        city=city,
        pm25=pm25,
        pm10=pm10,
        no2=no2,
        so2=so2,
        o3=o3,
        prediction=prediction,
        forecast=forecast,
        advice=advice,
        outdoor=outdoor,
    )


if __name__ == "__main__":
    app.run(debug=True)
