import numpy as np
import pandas as pd
import tensorflow as tf
import autokeras as ak
import os
import numpy as np
import datetime
from sklearn.model_selection import KFold, train_test_split


def getSession(date):
    date = date.split(" ")[0]
    date = date.split("-")
    date = [int(i) for i in date]
    date = datetime.date(date[0], date[1], date[2])
    if date.month in [3, 4, 5]:
        return 0
    elif date.month in [6, 7, 8]:
        return 1
    elif date.month in [9, 10, 11]:
        return 2
    else:
        return 3


if __name__ == "__main__":

    log_dir = "logs/all/".format(
        datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    tf_callback = tf.keras.callbacks.TensorBoard(
        log_dir=log_dir)
    maxt = 10
    epochs = 100

    x_columns = ['Temp', 'UV', 'SunShineHour', 'GlobalRad']
    y_columns = ['unit_deg']

    data = pd.DataFrame(columns=x_columns+y_columns)

    # 走訪資料夾下的檔案
    for file in os.listdir("./t_data"):
        data = pd.concat([data, pd.read_csv("./t_data/"+file)])

    print(data)
    print(data.shape)

    data = data[data['degree'] > 0]
    data = data[data['Temp'] > 0]
    data = data[data['UV'] > 0]
    data = data[data['SunShineHour'] > 0]
    data = data[data['GlobalRad'] > 0]
    data['unit_deg'] = data['degree'] / data['capacity']

    print(data.shape)

    data['session'] = data['date'].apply(lambda x: getSession(x))

    total = data

    for j in range(3):
        data = total[total['session'] == j]

        # It tries 10 different models.
        reg = ak.StructuredDataRegressor(max_trials=maxt, overwrite=True)

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
        print(reg.evaluate(test_x, test_y))

        model = reg.export_model()

        # <class 'tensorflow.python.keras.engine.training.Model'>
        print(type(model))

        with open('result.txt', 'a') as f:
            f.write("====== Final Result: Session "+str(j)+" =====\n")
            f.write(str(reg.evaluate(test_x, test_y))+"\n")

        model.save('testmodel', save_format='tf')
