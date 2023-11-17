import csv
import pandas as pd
import numpy as np

if __name__ == "__main__":

    df1 = pd.read_csv(
        "./data/gen_station.csv")[["Station", "Lng", "Lat"]]  # 光電站資料 0-43
    df2 = pd.read_csv("./data/weather_station.csv")[
        ["StationName", "StationLongitude", "StationLatitude"]]  # 觀測站資料 0-666
    df3 = pd.read_csv('./data/gen_obv_dist.csv')

    dataframe = []

    solar = df1["Station"].to_list()
    solar_Lng = df1["Lng"].to_list()
    solar_Lat = df1["Lat"].to_list()

    weather = df2["StationName"].to_list()
    weather_Lng = df2["StationLongitude"].to_list()
    weather_Lat = df2["StationLatitude"].to_list()

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

    df = pd.DataFrame(dataframe, columns=[
                      "gen_station", "gen_lng", "gen_lat", "obv_station", "obv_lng", "obv_lat"])

    df.round(2).to_csv("./data/gen_obv_min_dist.csv")
