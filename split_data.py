
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import os

folder_path = './weather_data'
solar_station = os.listdir(folder_path)

# print (solar_station)

# train = pd.DataFrame(columns=data.columns)
train = pd.DataFrame()
test = train

for station in solar_station:

    data = pd.read_csv("./weather_data/{}".format(station))

    data = data[data['degree'] > 0]
    data = data[data['SunShine'].notna()]
    print(data.shape)    

    if data.shape[0] > 10:
        temp_train, temp_test = train_test_split(data, test_size=0.2)
        train = pd.concat([temp_train, train], ignore_index=True)
        test = pd.concat([temp_test, test], ignore_index=True)
    
    print(train.shape)
    print(test.shape)


train.to_csv("train.csv")
test.to_csv("test.csv")



# data = pd.read_csv("./weather_data/台中龍井光電.csv")

# data = data[data['degree'] > 0]
# data = data[data['SunShine'].notna()]
# print(data.shape)

# train = pd.DataFrame(columns=data.columns)
# test = train

# if data.shape[0] > 10:
#     temp_train, temp_test = train_test_split(data, test_size=0.2)
#     train = pd.concat([temp_train, train], ignore_index=True)
#     test = pd.concat([temp_test, test], ignore_index=True)

# print(train.shape)
# print(test.shape)

# data = pd.read_csv("./weather_data/嘉義民雄光電.csv")


# data = data[data['degree'] > 0]
# data = data[data['SunShine'].notna()]
# print(data.shape)


# if data.shape[0] > 10:
#     temp_train, temp_test = train_test_split(data, test_size=0.2)
#     train = pd.concat([temp_train, train], ignore_index=True)
#     test = pd.concat([temp_test, test], ignore_index=True)


# print(train.shape)
# print(test.shape)


