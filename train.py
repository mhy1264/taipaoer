import split_data
import numpy as np
import pandas as pd
import tensorflow as tf
import autokeras as ak

if __name__ == "__main__":
    train, test = split_data.split_data(100)

    x_columns = ['date', 'ObsTime', 'Temperature',
                 'RH', 'SunShine', 'SunShineRate', 'UVI Max_y',
                 'Lng', 'Lat']
    y_columns = ['degree']

    x_train = train[x_columns]
    x_train.dropna()
    y_train = train[y_columns]

    x_test = test[x_columns]
    y_test = test[y_columns]

    # It tries 10 different models.
    reg = ak.StructuredDataRegressor(max_trials=10, overwrite=True)
    # Feed the structured data regressor with training data.
    reg.fit(x_train, y_train, epochs=100)
    # Predict with the best model.
    predicted_y = reg.predict(x_test)
    # Evaluate the best model with testing data.
    print(reg.evaluate(x_test, y_test))
