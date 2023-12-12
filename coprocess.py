
import pandas as pd
import numpy as np
import weather
import warnings
import os
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


def is_file_in_folder(folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    return os.path.exists(file_path)


if __name__ == "__main__":

    solar_daily = pd.read_csv("./data/solar_daily.csv")
    weather_station = pd.read_csv("./data/weather_station.csv")
    form_data = pd.read_csv("data/station_unit_transform.csv")
    dn = ['台南鹽田光電', '南投大彎光電', '金門鵲山光電', '金門塔山光電',
          '高雄保寧光電', '馬祖珠山光電', '蘭嶼貯存場光電', '蘭嶼電廠光電']
    dn2 = ['台中電廠建物光電', '台中電廠GIS廠房光電', '高雄E\\S停車棚光電',
           '大湳淨水場光電', '平鎮淨水場光電', '東興淨水場光電', '龍潭淨水場光電']
    dn3 = ['龜山加壓站光電', '淡水配水場光電', '鳳山水庫光電', '澎湖尖山小再光電',
           '台南七股II光電', '義竹工作站光電', '台南鹽田電氣室光電']

    data = dn3
    for row in range(0, len(data)):
        folder_path = './new2_weather_data'
        file_name = data[row]+".csv"
        print(file_name)
        if is_file_in_folder(folder_path, file_name):
            continue
        df = solar_daily.iloc[:, [row, -1]]
        current_station = df.columns.tolist()[0]
        fileName = current_station.replace("/", "\\")
        print(data[row])

        try:
            station_weather = weather.preprocess_data_weather(
                current_station+"站")

            # # 合併發電站度數和天氣觀測站的天氣資訊
            station_weather['date'] = station_weather['date'].astype(str)
            df['date'] = df["date"].astype(str)

            merged_df = pd.merge(station_weather, df, on="date", how="inner")
            merged_df.rename(columns={current_station: "degree"}, inplace=True)

            # 合併 merge_df 和紫外線資料 放到 UVI max 這格內

            merged_df["station"] = [current_station]*merged_df.shape[0]
            merged_df["capacity"] = [form_data[form_data['name'].astype(
                str).str.contains("{}".format(current_station))]['capacity'].values[0]]*merged_df.shape[0]
            merged_df = merged_df[merged_df['degree'] > 0]
            merged_df = merged_df.round(2)

            try:
                merged_df.to_csv(
                    "./new2_weather_data/{}.csv".format(data[row]))
            except Exception as e:
                print("{} Error: {}".format(data[row], e.args))
                with open("Exception_file.txt", 'w') as f:
                    f.write("{}\n".format(data[row]))
        except Exception as e:
            print("{} Error: {}".format(data[row], e.args[0]))
            with open("Exception_file.txt", 'w') as f:
                f.write("{}\n".format(data[row]))
