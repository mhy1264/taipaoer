import flask
from requests import get
import count_area as ca
from weather import get_history_data as get_weather_data
from flask import jsonify, request
import pandas as pd

from tensorflow import keras
import autokeras as ak

app = flask.Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/getThreeStation", methods=["post"])
def getThreeStaton():
    _data = request.form.to_dict(flat=False)
    print(_data)

    Lng = float(_data["Lng"][0])
    Lat = float(_data["Lat"][0])

    print(Lng, Lat)
    weather_stations = ca.three_points_weather(Lng, Lat)

    w1, w2, w3, wc = get_weather_data(weather_stations, 30)
    w1 = pd.concat([w1, w2])
    w1 = pd.concat([w1, w3])

    data = {
        "stations": {
            "weather": {
                "station1": {
                    "station": weather_stations[0],
                    "Lng": 1,
                    "Lat": 1,
                },
                "station2": {
                    "station": weather_stations[1],
                    "Lng": 1,
                    "Lat": 1,
                },
                "station3": {
                    "station": weather_stations[2],
                    "Lng": 1,
                    "Lat": 1,
                },
            },
        },
        "data": {
            "Temp": w1["Temp"].dropna().to_list(),
            "UV": w1["UV"].dropna().to_list(),
            "SunShineHour": w1["SunShineHour"].dropna().to_list(),
            "GlobalRad": w1["GlobalRad"].dropna().to_list(),
            "mean": {
                "Temp": w1["Temp"].mean(),
                "UV": w1["UV"].mean(),
                "SunShineHour": w1["SunShineHour"].mean(),
                "GlobalRad": w1["GlobalRad"].mean(),
            },
        },
    }

    return flask.jsonify(data)


@app.route("/predict", methods=["POST"])
def predict():
    _data = request.form.to_dict(flat=False)
    global_rad = float(_data["GlobalRad"][0])
    uv = float(_data["UV"][0])
    temp = float(_data["Temp"][0])
    sun_shine_hour = float(_data["SunShineHour"][0])

    loaded_model = keras.models.load_model(
        "model_autokeras.h5", custom_objects=ak.CUSTOM_OBJECTS
    )

    predVal = loaded_model.predict([[temp, sun_shine_hour, global_rad, uv]])
    print(predVal[0][0])
    return jsonify({"predict": str(predVal[0][0])})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
