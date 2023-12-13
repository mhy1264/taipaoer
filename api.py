import flask as fl
from flask import request
from count_area import three_points_weather
import weather
import time
from tensorflow import keras
import autokeras as ak


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

    mean = data.drop(columns=['date']).mean(axis=0).round(2).values.tolist()

    loaded_model = keras.models.load_model(
        "model_autokeras", custom_objects=ak.CUSTOM_OBJECTS)

    predicted_y = loaded_model.predict(mean)
    print(predicted_y)

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
        "weather": {
            "Temp": mean[0],
            "SunShineHour": mean[1],
            "GlobalRad": mean[2],
            "UV": mean[3]
        },
        "retult": {
            "status": "success",
            "value": -1,
            "request time": current_time
        }
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
