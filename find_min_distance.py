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
        min = [inf, inf]
        index = [0, 0]
        for k in range(len(weather)):
            if (df3[solar[i]][k] < min[0]) | (df3[solar[i]][k] < min[1]):
                if min[0] >= min [1]:
                    min[0] = df3[solar[i]][k]
                    index[0] = k
                else:
                    min[1] = df3[solar[i]][k]
                    index[1] = k                
        temp = [solar[i], solar_Lng[i], solar_Lat[i], 
                weather[index[0]], weather_Lng[index[0]], weather_Lat[index[0]],
                weather[index[1]], weather_Lng[index[1]], weather_Lat[index[1]]]
        dataframe.append(temp)

    df = pd.DataFrame(dataframe, columns=[
                      "gen_station", "gen_lng", "gen_lat", "obv_station1", "obv_lng1", "obv_lat1", 
                      "obv_station2", "obv_lng2", "obv_lat2"])

    df.round(2).to_csv("./data/gen_obv_min_dist.csv")
