from sklearn.model_selection import train_test_split
import pandas as pd
import tensorflow as tf
import autokeras as ak
import os
from sklearn.model_selection import KFold
from datetime import datetime


def myprint(s):
    with open('modelsummary.txt', 'a') as f:
        print(s, file=f)


def mean_norm(df_input):
    return df_input.apply(lambda x: (x - x.mean()) / x.std(), axis=0)


if __name__ == "__main__":

    epochs = 100
    maxtrial = 10

    for file in os.listdir("./t_data"):
        log_dir = "logs/partital/{}_{}".format(file,
                                               datetime.now().strftime("%Y%m%d-%H%M%S"))
        tf_callback = tf.keras.callbacks.TensorBoard(
            log_dir=log_dir)
        data = pd.read_csv("./t_data/" + file)

        orig = data.shape[0]
        x_columns = ['Temp', 'UV', 'SunShineHour', 'GlobalRad']
        y_columns = ['unit_deg']

        data = data[data['degree'] > 0]
        data = data[data['Temp'] > 0]
        data = data[data['UV'] > 0]
        data = data[data['SunShineHour'] > 0]
        data = data[data['GlobalRad'] > 0]
        data['unit_deg'] = data['degree'] / data['capacity']

        # It tries 10 different models.
        reg = ak.StructuredDataRegressor(max_trials=maxtrial, overwrite=True)

        kf = KFold(n_splits=10)
        train, test = train_test_split(data, test_size=0.3)
        kf.get_n_splits(train)
        for i, (train_index, test_index) in enumerate(kf.split(train)):

            print(f"Fold {i}:")
            x_train = train.iloc[train_index][x_columns]
            y_train = train.iloc[train_index][y_columns]

            x_test = train.iloc[test_index][x_columns]
            y_test = train.iloc[test_index][y_columns]

            # Feed the structured data regressor with training data.
            reg.fit(x_train, y_train, epochs=epochs, callbacks=[tf_callback])
            # Predict with the best model.
            predicted_y = reg.predict(x_test)
            # Evaluate the best model with testing data.
            print(reg.evaluate(x_test, y_test))

        test_x = test[x_columns]
        test_y = test[y_columns]
        prid_y = reg.predict(test_x)
        print("====== Final Result =====")
        res = reg.evaluate(x_test, y_test)
        print(res)

        # getting the current date and time
        current_datetime = datetime.now()
        current_date_time = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")

        loss = orig - data.shape[0]
        with open("./result.csv", "a") as f:
            f.write("{},{},{},{},{},{}\n".format(current_date_time, file, orig,
                    loss, 100*(loss/orig), res))
            # drop_rate(%),evaluate_value[0], evaluate_value[1]

        model = reg.export_model()
