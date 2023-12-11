import numpy as np
import pandas as pd
import tensorflow as tf
import autokeras as ak
import os
import numpy as np
from sklearn.model_selection import KFold, train_test_split


if __name__ == "__main__":

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
    
    data = data.head(100)

    # It tries 10 different models.
    reg = ak.StructuredDataRegressor(max_trials=10, overwrite=True)

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
        reg.fit(x_train, y_train, epochs=100)
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

    print(type(model))  # <class 'tensorflow.python.keras.engine.training.Model'>

    model.save('testmodel', save_format='tf')
