from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

API_KEY = "fd9ee9262822e39a91e587d80cbb302f"
@app.route("/")
def home():
    city = "Hyderabad"
    lat = 17.3850
    lon = 78.4867

    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()
        aqi = data["list"][0]["main"]["aqi"]
    except:
        aqi = random.randint(40,120)

    prediction = random.randint(40,150)

    if prediction < 50:
        status = "Good"
    elif prediction < 100:
        status = "Moderate"
    else:
        status = "Unhealthy"

    return render_template(
        "index.html",
        city=city,
        prediction=prediction,
        status=status,
        aqi=aqi
    )

if __name__ == "__main__":
    app.run(debug=True)