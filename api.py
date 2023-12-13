import flask as fl
from flask import request
from count_area import three_points_weather
import requests
import weather
import time

app = fl.Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route("/predict", methods=["POST"])
def attr():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    _data = request.form.to_dict(flat=False)
    print(_data)
    if "Lat" not in _data:
        print("No Lat")
    if "Lng" not in _data:
        print("No Long")

    nearest_weather = three_points_weather(
        float(_data["Lng"][0]), float(_data["Lat"][0]))
    data = weather.get_history_data(nearest_weather, 30)
    print(data.head())

    return {
        "input": {
            "Lat": _data["Lat"][0],
            "Lng": _data["Lng"][0]
        },
        "station": {
            "station1": nearest_weather[0],
            "station2": nearest_weather[1],
            "station3": nearest_weather[2]
        },
        "retult": {
            "status": "success",
            "value": -1,
            "request time": current_time
        }
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
