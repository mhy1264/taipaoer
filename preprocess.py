
import pandas as pd
import numpy as np
import weather
import uva


def get_obv_station(gen_station: str) -> str:
    obv_station = pd.read_csv("./data/mini_dist_with_sunshine.csv")
    df = obv_station[obv_station['gen_station'].astype(
        str).str.contains("{}".format(gen_station))]
    return df['obv_station'].tolist()[0]


def get_uva_station(gen_station: str):
    uva_station = pd.read_csv("./data/mini_dist_adduv.csv")
    uva_station = uva_station[["gen_station",
                               "uv_station", "uv_lng", "uv_lat"]]
    df = uva_station[uva_station['gen_station'].astype(
        str).str.contains("{}".format(gen_station))]
    return df['uv_station'].tolist()[0]


def get_location(gen_station: str) -> list:
    total_station = pd.read_csv("./data/station.csv")
    df = total_station[total_station['Station'].astype(
        str).str.contains("{}".format(gen_station))]
    return df[['Lng', 'Lat']].values


solar_daily = pd.read_csv("./data/solar_daily.csv")
station = pd.read_csv("./data/station.csv")


# In[30]:

for row in range(1, solar_daily.shape[1]):
    df = solar_daily.iloc[:, [row, -1]]
    current_station = df.columns.tolist()[0]

    obv_station = get_obv_station(current_station)
    station_weather = weather.get_data(obv_station)
    fileName = current_station.replace("/", "\\")

    # 合併發電站度數和天氣觀測站的天氣資訊
    station_weather['date'] = station_weather['date'].astype(str)
    df['date'] = df["date"].astype(str)
    merged_df = pd.merge(station_weather, df, on="date", how="inner")
    merged_df.rename(columns={current_station: "degree"}, inplace=True)

    # 合併 merge_df 和紫外線資料 放到 UVI max 這格內
    # uva_station = get_uva_station(current_station)
    # uva_data = uva.get_data(uva_station)

    # print(current_station, obv_station, uva_station)

    # merged_df = pd.merge(merged_df, uva_data, on="date", how="inner")
    merged_df["station"] = [current_station]*merged_df.shape[0]

    location = get_location(current_station)[0]
    merged_df['Lng'] = location[0]
    merged_df['Lat'] = location[1]

    try:
        merged_df.to_csv("./weather_data/{}.csv".format(fileName))
    except:
        print(fileName, "fail")
