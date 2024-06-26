import onnxmltools
from keras.models import load_model
from tensorflow import keras
import autokeras as ak

input_keras_model = "model_autokeras.h5"
output_onnx_model = "weather.onnx"
loaded_model = keras.models.load_model(
        "model_autokeras.h5", custom_objects=ak.CUSTOM_OBJECTS
    )
print("--------------- Step #2 - convert ---------------")
onnx_model  = onnxmltools.convert_keras(loaded_model) 
print("--------------- Step #3 - save Onnx ---------------")
onnxmltools.utils.save_model(onnx_model, output_onnx_model)
