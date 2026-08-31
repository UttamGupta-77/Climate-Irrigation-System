from flask import Flask, render_template
import requests
import random

import firebase_admin
from firebase_admin import credentials, db
from joblib import load

from datetime import datetime


# --------------------------------------------------
# FIREBASE CONFIGURATION
# --------------------------------------------------

cred = credentials.Certificate(
    "smartirrigationsystem-4b612-firebase-adminsdk-fbsvc-f1f87ff845_new.json"
)

firebase_admin.initialize_app(
    cred,
    {
        'databaseURL':
        'https://smartirrigationsystem-4b612-default-rtdb.asia-southeast1.firebasedatabase.app/'
    }
)


# --------------------------------------------------
# FLASK APPLICATION
# --------------------------------------------------

app = Flask(__name__)


# --------------------------------------------------
# LOAD MACHINE LEARNING MODEL
# --------------------------------------------------

model = load('irrigation_model.pkl')
encoder = load('status_encoder.pkl')


# --------------------------------------------------
# OPENWEATHERMAP CONFIGURATION
# --------------------------------------------------

API_KEY = "3bffb6beae5a39ca6caeb35e0d383aa0"

CITY = "Pune"

URL = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?q={CITY}&appid={API_KEY}&units=metric"
)


# --------------------------------------------------
# MAIN DASHBOARD
# --------------------------------------------------

@app.route('/')
def index():

    # ----------------------------------------------
    # 1. GET WEATHER DATA
    # ----------------------------------------------

    try:

        response = requests.get(URL, timeout=10)

        weather_data = response.json()

        temp = weather_data.get(
            'main', {}
        ).get(
            'temp', 0
        )

        humidity = weather_data.get(
            'main', {}
        ).get(
            'humidity', 0
        )

    except Exception as e:

        print("Weather API error:", e)

        temp = 0
        humidity = 0


    # ----------------------------------------------
    # 2. SIMULATE SOIL MOISTURE
    # ----------------------------------------------
    #
    # This is still simulated for now.
    # Later we will replace this with the
    # Raspberry Pi Pico sensor value.
    #

    soil_moisture = random.randint(10, 90)


    # ----------------------------------------------
    # 3. ML MODEL PREDICTION
    # ----------------------------------------------

    prediction = model.predict(
        [[temp, humidity, soil_moisture]]
    )[0]

    irrigation_status = encoder.inverse_transform(
        [prediction]
    )[0]


    # ----------------------------------------------
    # 4. CREATE CURRENT RECORD
    # ----------------------------------------------

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    data = {

        "city": CITY,

        "temperature": round(temp, 2),

        "humidity": humidity,

        "soil_moisture": soil_moisture,

        "irrigation_status": irrigation_status,

        "timestamp": timestamp
    }


    # ----------------------------------------------
    # 5. SAVE CURRENT DATA TO FIREBASE
    # ----------------------------------------------

    ref = db.reference('irrigation_data')

    ref.push(data)


    # ----------------------------------------------
    # 6. GET ALL DATA FROM FIREBASE
    # ----------------------------------------------

    firebase_data = ref.get()

    history = []

    if firebase_data:

        for key, record in firebase_data.items():

            history.append(record)


    # ----------------------------------------------
    # 7. SORT HISTORY BY TIMESTAMP
    # ----------------------------------------------

    history.sort(
        key=lambda x: x.get(
            "timestamp",
            ""
        )
    )


    # ----------------------------------------------
    # 8. GET LAST 20 RECORDS
    # ----------------------------------------------

    history = history[-20:]


    # ----------------------------------------------
    # 9. PREPARE DATA FOR CHART
    # ----------------------------------------------

    chart_labels = []

    temperature_data = []

    humidity_data = []

    moisture_data = []


    for record in history:

        timestamp_value = record.get(
            "timestamp",
            ""
        )


        # Convert timestamp to a
        # shorter time format

        if timestamp_value:

            try:

                time_object = datetime.strptime(
                    timestamp_value,
                    "%Y-%m-%d %H:%M:%S"
                )

                label = time_object.strftime(
                    "%H:%M:%S"
                )

            except ValueError:

                label = timestamp_value

        else:

            label = ""


        chart_labels.append(label)


        # Add temperature

        temperature_data.append(
            record.get(
                "temperature",
                0
            )
        )


        # Add humidity

        humidity_data.append(
            record.get(
                "humidity",
                0
            )
        )


        # Add soil moisture

        moisture_data.append(
            record.get(
                "soil_moisture",
                0
            )
        )


    # ----------------------------------------------
    # 10. SEND DATA TO HTML
    # ----------------------------------------------

    return render_template(
        "index.html",

        data=data,

        chart_labels=chart_labels,

        temperature_data=temperature_data,

        humidity_data=humidity_data,

        moisture_data=moisture_data
    )


# --------------------------------------------------
# RUN FLASK
# --------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)