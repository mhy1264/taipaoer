import pandas as pd
from util import cal_dis


if __name__ == "__main__":

    df1 = pd.read_csv(
        "./data/gen_station.csv")[["Station", "Lng", "Lat"]]  # 光電站資料 0-43
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
