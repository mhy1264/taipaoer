import numpy as np
import pandas as pd
import tensorflow as tf
import autokeras as ak
import os
import numpy as np
import datetime
from sklearn.model_selection import KFold, train_test_split


from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import tensorflow as tf
import autokeras as ak
import argparse
import datetime
import numpy as np
from sklearn.model_selection import KFold
import os


def myprint(s):
    with open('modelsummary.txt', 'a') as f:
        print(s, file=f)


def mean_norm(df_input):
    return df_input.apply(lambda x: (x - x.mean()) / x.std(), axis=0)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("filePath", help="file path")

    args = parser.parse_args()
    log_dir = "logs/partital/{}_{}".format(args.filePath.split("/")[-1],
                                           datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    val = os.fork()

    if val == 0:
        os.system("tensorboard --logdir " + log_dir + "  --port=6007")
    elif val > 0:
        tf_callback = tf.keras.callbacks.TensorBoard(
            log_dir=log_dir, histogram_freq=1)

        train, test = train_test_split(
            pd.read_csv(args.filePath), test_size=0.3)

        data = pd.read_csv(args.filePath)

        x_columns = ['Temp', 'UV', 'SunShineHour', 'GlobalRad']
        y_columns = ['unit_deg']

        data = data[data['degree'] > 0]
        data = data[data['Temp'] > 0]
        data = data[data['UV'] > 0]
        data = data[data['SunShineHour'] > 1]
        data = data[data['GlobalRad'] > 0]
        data['unit_deg'] = data['degree'] / data['capacity']

        # It tries 10 different models.

        predict_from = 1
        predict_until = 100
        lookback = 3

        reg = ak.TimeseriesForecaster(
            lookback=lookback,
            predict_from=predict_from,
            predict_until=predict_until,
            max_trials=100,
            objective="val_loss",
        )

        kf = KFold(n_splits=10)
        train, test = train_test_split(data, test_size=0.3)
        kf.get_n_splits(train)

        for i, (train_index, test_index) in enumerate(kf.split(train)):

            print(f"Fold {i}:")
            x_train = train.iloc[train_index][x_columns]
            y_train = train.iloc[train_index][y_columns]

            x_test = train.iloc[test_index][x_columns]
            y_test = train.iloc[test_index][y_columns]

            # Train the TimeSeriesForecaster with train data
            reg.fit(
                x=x_train,
                y=y_train,
                batch_size=32,
                epochs=100,
                callbacks=[tf_callback])

            # Predict with the best model(includes original training data).
            predictions = reg.predict(x_test)

            # Evaluate the best model with testing data.
            print(reg.evaluate(x_test, y_test))

        test_x = test[x_columns]
        test_y = test[y_columns]
        prid_y = reg.predict(test_x)

        print("====== Final Result =====")
        print(reg.evaluate(test_x, test_y))

        model = reg.export_model()
        model.save("model_autokeras.h5")
        os.wait(val)
