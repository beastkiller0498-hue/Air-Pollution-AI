from flask import Flask, render_template, request
import requests
import os
import random

app = Flask(__name__)

API_KEY = "fd9ee9262822e39a91e587d80cbb302f"

def get_coordinates(city):
    url=f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    data=requests.get(url).json()
    if data:
        return data[0]["lat"],data[0]["lon"]
    return None,None

def get_air_data(lat,lon):
    url=f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    data=requests.get(url).json()
    return data

def get_forecast(lat,lon):
    url=f"http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={API_KEY}"
    data=requests.get(url).json()
    return data

def recommendation(aqi):
    if aqi<=1:
        return "Air quality good. Outdoor activities safe."
    elif aqi==2:
        return "Fair air. Sensitive people careful."
    elif aqi==3:
        return "Moderate pollution. Reduce outdoor exercise."
    elif aqi==4:
        return "Poor air. Wear mask."
    else:
        return "Very poor air. Stay indoors."

@app.route("/",methods=["GET","POST"])
def home():

    city=None
    aqi=None
    pm25=None
    pm10=None
    forecast=[]
    advice=None
    future_ai=None

    if request.method=="POST":

        city=request.form["city"]

        lat,lon=get_coordinates(city)

        if lat:

            data=get_air_data(lat,lon)

            aqi=data["list"][0]["main"]["aqi"]

            pm25=data["list"][0]["components"]["pm2_5"]
            pm10=data["list"][0]["components"]["pm10"]

            advice=recommendation(aqi)

            forecast_data=get_forecast(lat,lon)

            for item in forecast_data["list"][:6]:
                forecast.append(item["main"]["aqi"])

            future_ai=aqi+random.randint(-1,2)

    return render_template("index.html",
                           city=city,
                           aqi=aqi,
                           pm25=pm25,
                           pm10=pm10,
                           forecast=forecast,
                           advice=advice,
                           future_ai=future_ai)

if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
