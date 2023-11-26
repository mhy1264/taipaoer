from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import tensorflow as tf
import autokeras as ak
import argparse

import numpy as np
from sklearn.model_selection import KFold


def myprint(s):
    with open('modelsummary.txt', 'a') as f:
        print(s, file=f)


def mean_norm(df_input):
    return df_input.apply(lambda x: (x - x.mean()) / x.std(), axis=0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filePath", help="file path")
    parser.add_argument("epochs", help="epoch 數", type=int)
    parser.add_argument("maxtrial",
                        help="maxtrial", type=int)

    args = parser.parse_args()

    # train, test = train_test_split(pd.read_csv(args.filePath), test_size=0.3)

    data = pd.read_csv(args.filePath)
    x_columns = ['Temp', 'UV', 'SunShineHour', 'GlobalRad']
    y_columns = ['degree']

    # x_train = mean_norm(train[x_columns])
    # x_train.dropna()
    # y_train = train[y_columns]

    # x_test = mean_norm(test[x_columns])
    # y_test = test[y_columns]

    # It tries 10 different models.
    reg = ak.StructuredDataRegressor(max_trials=args.maxtrial, overwrite=True)

    kf = KFold(n_splits=10)
    kf.get_n_splits(data)
    for i, (train_index, test_index) in enumerate(kf.split(data)):

        print(f"Fold {i}:")
        x_train = data.iloc[train_index][x_columns]
        y_train = data.iloc[train_index][y_columns]

        x_test = data.iloc[test_index][x_columns]
        y_test = data.iloc[test_index][y_columns]

        # Feed the structured data regressor with training data.
        reg.fit(x_train, y_train, epochs=args.epochs)
        # Predict with the best model.
        predicted_y = reg.predict(x_test)
        # Evaluate the best model with testing data.
        print(reg.evaluate(x_test, y_test))
