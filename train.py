import split_data
import numpy as np
import pandas as pd
import tensorflow as tf
import autokeras as ak
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("epochs", help="epoch 數", type=int)
    parser.add_argument("maxtrial",
                        help="maxtrial", type=int)

    args = parser.parse_args()

    train, test = split_data.split_data_by_station('蘭嶼電廠光電', 100)

    x_columns = ['Temperature',
                 'RH', 'SunShineRate', 'UVI Max',
                 'Lng', 'Lat']
    y_columns = ['degree']

    x_train = train[x_columns]
    x_train.dropna()
    y_train = train[y_columns]

    x_test = test[x_columns]
    y_test = test[y_columns]

    # It tries 10 different models.
    reg = ak.StructuredDataRegressor(max_trials=args.maxtrial, overwrite=True)
    # Feed the structured data regressor with training data.
    reg.fit(x_train, y_train, epochs=args.epochs)
    # Predict with the best model.
    predicted_y = reg.predict(x_test)
    # Evaluate the best model with testing data.
    print(reg.evaluate(x_test, y_test))
