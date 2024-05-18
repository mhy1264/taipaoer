import flask as fl
from flask import request
from count_area import three_points_weather
import weather
import time
from tensorflow import keras
import autokeras as ak
import pandas as pd


app = fl.Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/predict", methods=["POST"])
def attr():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    _data = request.form.to_dict(flat=False)
    res = {
        "input": {"Lat": "", "Lng": ""},
        "station": {"station1": "", "station2": "", "station3": ""},
        "weather": {"Temp": "", "SunShineHour": "", "GlobalRad": "", "UV": ""},
        "result": {
            "status": "",
            "Message": "",
            "value": "",
            "request time": current_time,
        },
    }

    nearest_weather = ""
    data = pd.DataFrame()

    print(_data)
    if "Lat" not in _data:
        res["result"] = {
            "status": "fail",
            "Message": "no Lat",
            "request time": current_time,
        }
        return res

    if "Lng" not in _data:
        res["result"] = {
            "status": "fail",
            "Message": "no Lng",
            "request time": current_time,
        }
        return res

    try:
        nearest_weather = three_points_weather(
            float(_data["Lng"][0]), float(_data["Lat"][0])
        )
        print(nearest_weather)
    except Exception as e:
        res["input"] = {"Lat": _data["Lat"][0], "Lng": _data["Lng"][0]}

        res["result"] = {
            "status": "fail",
            "Message": e.args[0],
            "request time": current_time,
        }
        return res

    try:
        data = weather.get_history_data(nearest_weather, 30)
    except Exception as e:
        res["input"] = {"Lat": _data["Lat"][0], "Lng": _data["Lng"][0]}
        res["station"] = {
            "station1": nearest_weather[0],
            "station2": nearest_weather[1],
            "station3": nearest_weather[2],
        }

        res["result"] = {
            "status": "fail",
            "Message": e.args[0],
            "request time": current_time,
        }

        return res

    mean = data.drop(columns=["date"]).mean(axis=0).round(2).values.tolist()

    predVal = 0

    try:
        loaded_model = keras.models.load_model(
            "model_autokeras", custom_objects=ak.CUSTOM_OBJECTS
        )

        predVal = loaded_model.predict(mean)
    except Exception as e:
        res["input"] = {"Lat": _data["Lat"][0], "Lng": _data["Lng"][0]}

        res["weather"] = {
            "Temp": mean[0],
            "SunShineHour": mean[1],
            "GlobalRad": mean[2],
            "UV": mean[3],
        }
        res["result"] = {
            "status": "fail",
            "Message": e.args[0],
            "request time": current_time,
        }
        return res

    print("-------------------------------")
    print(predVal[0][0])

    res["input"]["Lat"] = _data["Lat"][0]
    res["input"]["Lng"] = _data["Lng"][0]

    res["station"]["station1"] = nearest_weather[0]
    res["station"]["station2"] = nearest_weather[1]
    res["station"]["station3"] = nearest_weather[2]

    res["weather"]["Temp"] = mean[0]
    res["weather"]["SunShineHour"] = mean[1]
    res["weather"]["GlobalRad"] = mean[2]
    res["weather"]["UV"] = mean[3]

    res["result"]["status"] = "success"
    res["result"]["Message"] = "success"
    res["result"]["value"] = str(predVal[0][0])

    return res


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
