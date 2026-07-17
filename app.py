from flask import Flask, render_template, jsonify
import requests
import random

import firebase_admin
from firebase_admin import credentials, db
from joblib import load

from datetime import datetime

cred = credentials.Certificate("smartirrigationsystem-4b612-firebase-adminsdk-fbsvc-f1f87ff845_new.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://smartirrigationsystem-4b612-default-rtdb.asia-southeast1.firebasedatabase.app/'})





app = Flask(__name__)



model = load('irrigation_model.pkl')
encoder = load('status_encoder.pkl')


API_KEY = "3bffb6beae5a39ca6caeb35e0d383aa0"
CITY = "Pune"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"


@app.route('/')
def index():
    try:
        weather_data = requests.get(URL).json()
        temp = weather_data.get('main', {}).get('temp', 0)
        humidity = weather_data.get('main', {}).get('humidity', 0)
    except Exception as e:
        print("Weather API error:", e)
        temp = 0
        humidity = 0

        
    soil_moisture = random.randint(10,90)

    
    pred = model.predict([[temp, humidity, soil_moisture]])[0]
    irrigation_status = encoder.inverse_transform([pred])[0]

    data = {
    
        "city": CITY,
        "temperature": temp,
        "humidity": humidity,
        "soil_moisture": soil_moisture,
        "irrigation_status": irrigation_status,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

    ref = db.reference('irrigation_data')
    ref.push(data)

    return render_template("index.html",data = data)


if __name__ == "__main__":
    app.run(debug=True)


