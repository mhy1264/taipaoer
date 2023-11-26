import split_data
import numpy as np
import pandas as pd
import tensorflow as tf
import autokeras as ak
import argparse

import numpy as np
import pandas as pd
import tensorflow as tf
import autokeras as ak
import argparse

import numpy as np
from sklearn.model_selection import KFold


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("epochs", help="epoch 數", type=int)
    # parser.add_argument("maxtrial",
    #                     help="maxtrial", type=int)

    # args = parser.parse_args()

    x_columns = ['Temp', 'UV', 'SunShineHour', 'GlobalRad']
    y_columns = ['degree']

    data = split_data.k_fold(100)
    data.to_csv("./total.csv")
    print(data.shape)

    reg = ak.StructuredDataRegressor(max_trials=100, overwrite=True)

    kf = KFold(n_splits=10)
    kf.get_n_splits(data)

    for i, (train_index, test_index) in enumerate(kf.split(data)):

        print(f"Fold {i}:")
        x_train = data.iloc[train_index][x_columns]
        y_train = data.iloc[train_index][y_columns]

        x_test = data.iloc[test_index][x_columns]
        y_test = data.iloc[test_index][y_columns]

        # Feed the structured data regressor with training data.
        reg.fit(x_train, y_train, epochs=100)
        # Predict with the best model.
        predicted_y = reg.predict(x_test)
        # Evaluate the best model with testing data.
        print(reg.evaluate(x_test, y_test))

    model = reg.export_model()
    model.summary()
