from sklearn.model_selection import train_test_split, KFold
import pandas as pd
import numpy as np
import os
import math
folder_path = './weather_data'
solar_station = os.listdir(folder_path)


def split_data_by_station(station: str, percentage=100):
    train = pd.DataFrame()
    test = train
    percentage = 100 if percentage > 100 else percentage
    percentage = 0 if percentage < 0 else percentage

    data = pd.read_csv("./weather_data/{}.csv".format(station))
    data = data[data['degree'] > 0]
    data = data[data['SunShine'].notna()]
    data = data.head(math.ceil(data.shape[0] * percentage / 100))

    if data.shape[0] > 10:
        temp_train, temp_test = train_test_split(data, test_size=0.2)
        train = pd.concat([temp_train, train], ignore_index=True)
        test = pd.concat([temp_test, test], ignore_index=True)

    return train, test


def split_data(percentage=100):

    train = pd.DataFrame()
    test = train
    percentage = 100 if percentage > 100 else percentage
    percentage = 0 if percentage < 0 else percentage

    for station in solar_station:

        data = pd.read_csv("./weather_data/{}".format(station))

        data = data[data['degree'] > 0]
        data = data[data['SunShine'].notna()]
        data = data.head(math.ceil(data.shape[0] * percentage / 100))

        if data.shape[0] > 10:
            temp_train, temp_test = train_test_split(data, test_size=0.2)
            train = pd.concat([temp_train, train], ignore_index=True)
            test = pd.concat([temp_test, test], ignore_index=True)

    return train, test


def k_fold(data: pd.DataFrame):
    x_columns = ['Temp', 'UV', 'SunShineHour', 'GlobalRad']
    y_columns = ['degree']

    X = data[x_columns]
    y = data[y_columns]
    kf = KFold(n_splits=2)
    kf.get_n_splits()
    for X_train, X_test in kf.split(X):
        print(X_train.tolist())
        print("-----")
        print(X_test.tolist())
        print("======")


if __name__ == "__main__":
    data = pd.read_csv("nwd/中科E\S光電_臺中_沙鹿.csv")
    data = data[data['degree'] > 0]

    k_fold(data)
    # train, test = split_data_by_station('蘭嶼電廠光電', 100)
    # print(train, test)
    # train.to_csv("./train.csv")
    # test.to_csv("./test.csv")
