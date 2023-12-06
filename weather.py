import pandas as pd
import numpy as np
import requests
import json
from calendar import isleap
from count_area import three_points_weather
from util import cal_dis

def get_obv_station(gen_station: str):
    obv_station = pd.read_csv("./data/gen_obv_min_dist_with_uv.csv")
    df = obv_station[obv_station['gen_station'].astype(
        str).str.contains("{}".format(gen_station))]
    # print(df)
    try:
        res = df[['obv_station1', 'uv_station']].values.tolist()[0]
        return res[0], res[1]
    except:
        return None, None
    

def get_weater_location(weather_station: str):
    df = pd.read_csv("./data/weather_station.csv")
    
    df = df[df['StationName'] == weather_station] 
    res = df.values.tolist()[0]
    return [res[7], res[8]]


def get_station_info(name: str) -> list:
    df = pd.read_csv("./data/weather_station.csv")
    fliter = (df["StationName"] == name)
    info = df[fliter].iloc[0]
    station_type = "cwb"
    return [info['StationID'], station_type]


def get_month_data(station: list, year: int, month: int, UVStation: str):

    month = '0{}'.format(month) if month < 10 else "{}".format(month)

    ds = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (isleap(year)):
        ds[2] = 29
    data = {
        "date": "2017-02-01T00:00:00.000+08:00",
        "type": "table_month",
        "stn_ID": station[0],
        "stn_type": station[1],
        "start": "{}-{}-01T00:00:00".format(year, month),
        "end": "{}-{}-{}T00:00:00".format(year, month, ds[int(month)])
    }

    res = requests.post(
        "https://codis.cwa.gov.tw/api/station?", data=data)

    with open("{}.csv".format(station[1]), 'w', encoding=res.encoding) as f:
        f.write(res.text)

    jsonObj = json.loads(res.text)
    if jsonObj['metadata']['count'] != 0:
        daily_data = json.loads(res.text)['data'][0]['dts']

        Datas = []
        print(year, month)
        for i in daily_data:
            temp = [np.nan]*6
            temp[0] = i['DataDate'][0:10]
            temp[1] = i['AirTemperature']['Mean']
            temp[2] = i['UVIndex']['Maximum'] if (
                'UVIndex' in i and 'Maximum' in i['UVIndex']) else -1
            temp[3] = i['SunshineDuration']['Total'] if (
                "SunshineDuration" in i and "Total" in i['SunshineDuration']) else -1
            temp[4] = i['GlobalSolarRadiation']['Accumulation'] if (
                'GlobalSolarRadiation' in i and 'Accumulation' in i['GlobalSolarRadiation']) else -1
            temp[5] = False
            Datas.append(temp)
        Datas.sort()

        df = pd.DataFrame(
            Datas, columns=['date', 'Temp', 'UV', 'SunShineHour', 'GlobalRad', "HaveEmpty"])
        

        if (df['UV'].to_list() == [None]*df.shape[0]):
            df['UV'] = 0
        return df
    else:
        print("mata Count = 0")
        return None


def get_data(station: str, UVStation) -> pd.DataFrame:
    col = ['Date', 'Temp', 'UV', 'SunShineHour', 'GlobalRad']
    temp = pd.DataFrame(columns=col)
    station = get_station_info(station)
    print(station, UVStation)
    for year in range(2017, 2023):
        for month in range(1, 13):
            df = get_month_data(station, year, month, UVStation)
            temp = pd.concat([temp, df])
        print("\n")

    for month in range(1, 7):
        df = get_month_data(station, 2023, month, UVStation)
        temp = pd.concat([temp, df])

    return temp


def preprocess_data_weather(station_name: str):
    gen_station = pd.read_csv("./data/gen_station.csv")

    item = gen_station[gen_station['Station'] == station_name]
    sts = three_points_weather(item.iloc[0]['Lng'], item.iloc[0]['Lat'])
    # print(item['Station'], sts)
        
    w1 = get_data(sts[0], "")
    w2 = get_data(sts[1], "")
    w3 = get_data(sts[2], "")

    col = ['Temp', 'SunShineHour', 'GlobalRad']

    # 先處理 ['Temp', 'SunShineHour', 'GlobalRad']

    print(w1)
    print(w2)
    print(w3)
    df = pd.concat([w1[col]/3+w2[col]/3+w3[col]/3],axis=1)


    # 後處理 ['UV']
    data = {
        'date' : w1['date'].to_list(),
        'UV1' : w1['UV'].to_list(),
        'UV2' : w2['UV'].to_list(),
        'UV3' : w3['UV'].to_list(),
    }

    UV = pd.DataFrame(data)

    print(UV)

    return df


if __name__ == "__main__":
    df = preprocess_data_weather('竹工E/S光電站')
    print(df)


    