import csv
import pandas as pd
import numpy as np

if __name__ == "__main__":
    index_cols1 = ["Station", "Lng", "Lat"]  # Lng經度，Lat緯度
    index_cols2 = ["站名", "經度", "緯度"]

    df1 = pd.read_csv("./data/station.csv", usecols=index_cols1)  # 光電站資料 0-43
    df2 = pd.read_csv("./data/weather_station_with_sunshine.csv",
                      usecols=index_cols2)  # 觀測站資料 0-666
    df3 = pd.read_csv('./data/dist.csv')

    dataframe = []

    solar = df1["Station"].to_list()
    solar_Lng = df1["Lng"].to_list()
    solar_Lat = df1["Lat"].to_list()

    weather = df2["站名"].to_list()
    weather_Lng = df2["經度"].to_list()
    weather_Lat = df2["緯度"].to_list()

    new_index = []
    new_index.extend(solar)

    inf = float('Inf')

    for i in range(len(solar)):
        min = inf
        for k in range(len(weather)):
            if df3[solar[i]][k] < min:
                min = df3[solar[i]][k]
                index = k
        temp = [solar[i], solar_Lng[i], solar_Lat[i], weather[index],
                weather_Lng[index], weather_Lat[index]]
        dataframe.append(temp)

    print(dataframe)

    df = pd.DataFrame(dataframe, index=new_index, columns=[
                      "gen_station", "gen_lng", "gen_lat", "obv_station", "obv_lng", "obv_lat"])

    df.round(2).to_csv("./data/mini_dist_with_sunshine.csv")
