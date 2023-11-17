import csv
import pandas as pd
from haversine import haversine
import numpy


def cal_dis(s_Lng, s_Lat, w_Lng, w_Lat) -> float:
    d1 = (s_Lat, s_Lng)
    d2 = (w_Lat, w_Lng)
    dis = haversine(d1, d2) * 1000
    result = "%.7f" % dis
    return result


if __name__ == "__main__":

    df1 = pd.read_csv(
        "./data/station.csv")[["Station", "Lng", "Lat"]]  # 光電站資料 0-43
    df2 = pd.read_csv(
        "./data/weather_station.csv")[["StationName", "StationLongitude", "StationLatitude"]]  # 觀測站資料 0-666

    dataframe = []

    new_columns = ['/']
    new_columns.extend(df1['Station'].to_list())

    solar = df1["Station"].to_list()
    solar_Lng = df1["Lng"].to_list()
    solar_Lat = df1["Lat"].to_list()

    weather = df2["StationName"].to_list()
    weather_Lng = df2["StationLongitude"].to_list()
    weather_Lat = df2["StationLatitude"].to_list()

    for i in range(len(weather)):
        temp = [weather[i]]
        for k in range(len(solar)):
            temp.append(
                cal_dis(solar_Lng[k], solar_Lat[k], weather_Lng[i], weather_Lat[i]))
        dataframe.append(temp)

    df = pd.DataFrame(dataframe, columns=new_columns)
    print(df.head())

    df.to_csv("./data/gen_obv_dist.csv")
