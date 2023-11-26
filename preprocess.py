
import pandas as pd
import numpy as np
import weather
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def get_obv_station(gen_station: str):
    obv_station = pd.read_csv("./data/gen_obv_min_dist_with_uv.csv")
    df = obv_station[obv_station['gen_station'].astype(
        str).str.contains("{}".format(gen_station))]
    print(df)
    try:
        res = df[['obv_station1', 'uv_station']].values.tolist()[0]
        return res[0], res[1]
    except:
        return None, None


def get_location(gen_station: str) -> list:
    total_station = pd.read_csv("./data/station.csv")
    df = total_station[total_station['Station'].astype(
        str).str.contains("{}".format(gen_station))]
    return df[['Lng', 'Lat']].values


if __name__ == "__main__":

    solar_daily = pd.read_csv("./data/solar_daily.csv")
    weather_station = pd.read_csv("./data/weather_station.csv")

    for row in range(1, solar_daily.shape[1]):
        df = solar_daily.iloc[:, [row, -1]]
        current_station = df.columns.tolist()[0]

        obv_station, uva_station = get_obv_station(current_station)
        if (obv_station == None and uva_station == None):
            continue

        try:
            station_weather = weather.get_data(obv_station, uva_station)

            fileName = current_station.replace("/", "\\")

            # # 合併發電站度數和天氣觀測站的天氣資訊
            station_weather['date'] = station_weather['date'].astype(str)
            df['date'] = df["date"].astype(str)

            merged_df = pd.merge(station_weather, df, on="date", how="inner")
            merged_df.rename(columns={current_station: "degree"}, inplace=True)

            # 合併 merge_df 和紫外線資料 放到 UVI max 這格內

            merged_df["station"] = [current_station]*merged_df.shape[0]
            merged_df = merged_df[merged_df['degree'] > 0]

            print(merged_df.head())
            try:
                merged_df.to_csv(
                    "./new_weather_data/{}_{}_{}.csv".format(fileName, obv_station, uva_station))
            except Exception as e:
                print("{} Error: {}".format(fileName, e.args))
        except Exception as e:
            print("{} Error: {}".format(fileName, e.args[0]))
