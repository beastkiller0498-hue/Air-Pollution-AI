from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = "fd9ee9262822e39a91e587d80cbb302f"

@app.route("/", methods=["GET","POST"])
def home():

    city = None
    aqi = None
    status = None
    recommendation = None
    future_aqi = []

    if request.method == "POST":

        city = request.form["city"]

        # get city coordinates
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        geo_data = requests.get(geo_url).json()

        if geo_data:

            lat = geo_data[0]["lat"]
            lon = geo_data[0]["lon"]

            # current air pollution
            air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
            air_data = requests.get(air_url).json()

            aqi = air_data["list"][0]["main"]["aqi"]

            # forecast air pollution
            forecast_url = f"http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={API_KEY}"
            forecast_data = requests.get(forecast_url).json()

            for item in forecast_data["list"][:5]:
                future_aqi.append(item["main"]["aqi"])

            if aqi == 1:
                status = "Good"
                recommendation = "Air quality is good. Enjoy outdoor activities."

            elif aqi == 2:
                status = "Fair"
                recommendation = "Air is acceptable. Sensitive people should reduce outdoor activity."

            elif aqi == 3:
                status = "Moderate"
                recommendation = "Limit prolonged outdoor activities."

            elif aqi == 4:
                status = "Poor"
                recommendation = "Wear mask and avoid outdoor exercise."

            else:
                status = "Very Poor"
                recommendation = "Stay indoors and use air purifiers."

    return render_template(
        "index.html",
        city=city,
        aqi=aqi,
        status=status,
        recommendation=recommendation,
        future_aqi=future_aqi
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
