import pandas as pd
import numpy as np
import requests
import json
from calendar import isleap
from count_area import three_points_weather
from util import cal_dis
import datetime


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


def get_data_from_cwb(station: str, start: datetime.date, finish: datetime.date):

    # TODO
    '''
    1. change the date format
    '''
    station_info = get_station_info(station)

    data = {
        "date":  "{}-{}-{}T00:00:00".format(start.year, start.month if start.month >= 10 else "0{}".format(start.month), start.day if start.day > 0 else "0{}".format(start.day)),
        "type": "table_month",
        "stn_ID": station_info[0],
        "stn_type": station_info[1],
        "start": "{}-{}-{}T00:00:00".format(start.year, start.month if start.month >= 10 else "0{}".format(start.month), start.day if start.day > 0 else "0{}".format(start.day)),
        "end": "{}-{}-{}T00:00:00".format(finish.year, finish.month if finish.month >= 10 else "0{}".format(finish.month), finish.day if finish.day > 0 else "0{}".format(finish.day))
    }

    res = requests.post(
        "https://codis.cwa.gov.tw/api/station?", data=data)

    jsonObj = json.loads(res.text)
    with open("./data/{}.json".format(station), "w") as f:
        json.dump(jsonObj, f)

    ndata = jsonObj['metadata']['count']

    df = pd.DataFrame(columns=['date', 'Temp', 'UV',
                      'SunShineHour', 'GlobalRad', "notNull"])

    if (ndata != 0):
        daily_data = json.loads(res.text)['data'][0]['dts']
        Datas = []

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
            temp[5] = True
            Datas.append(temp)
        Datas.sort()

        df = pd.concat([df, pd.DataFrame(Datas, columns=['date', 'Temp',
                                                         'UV', 'SunShineHour', 'GlobalRad', "notNull"])])

    date_pool = pd.date_range(start=start, end=finish)
    date_pool = date_pool.strftime("%Y-%m-%d").to_list()

    nulldate = list(set(date_pool) - set(df['date'].to_list()))
    nulldate.sort()

    Datas = []

    for i in nulldate:
        temp = [np.nan]*6
        temp[0] = i
        temp[5] = False
        Datas.append(temp)

    df = pd.concat([df, pd.DataFrame(Datas, columns=['date', 'Temp',
                                                     'UV', 'SunShineHour', 'GlobalRad', "notNull"])])

    return df


def get_data(station: str) -> pd.DataFrame:
    col = ['Date', 'Temp', 'UV', 'SunShineHour', 'GlobalRad']
    temp = pd.DataFrame(columns=col)

    ds = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    print(station)
    for year in range(2017, 2023):
        if isleap(year):
            ds[2] = 29
        else:
            ds[2] = 28

        for month in range(1, 13):
            df = get_data_from_cwb(station, datetime.date(
                year, month, 1), datetime.date(year, month, ds[month]))
            temp = pd.concat([temp, df])

    for month in range(1, 7):
        df = get_data_from_cwb(station, datetime.date(
            2023, month, 1), datetime.date(2023, month, ds[month]))
        temp = pd.concat([temp, df])
    return temp


def combine(w1: pd.DataFrame, w2: pd.DataFrame, w3: pd.DataFrame):
    col = ['Temp', 'SunShineHour', 'GlobalRad', 'UV']

    # 先處理 ['Temp', 'SShineHour', 'GlobalRad']
    df = pd.concat([w1[col]+w2[col]+w3[col]], axis=1)

    vaild = {
        'Vaild1': w1['notNull'].to_list(),
        'Vaild2': w2['notNull'].to_list(),
        'Vaild3': w3['notNull'].to_list(),
    }

    vaild = pd.DataFrame(vaild)
    nVaild = pd.DataFrame({"vaild": vaild.sum(axis=1).to_list()})
    print(nVaild.shape, len(w1['notNull'].to_list()),
          len(w2['notNull'].to_list()), len(w3['notNull'].to_list()))

    df = df.fillna(0)

    avedf = pd.DataFrame({
        "date": w1['date'].to_list(),
        "Temp": pd.DataFrame(df['Temp'] / nVaild['vaild']).dropna()[0].to_list(),
        "SunShineHour": pd.DataFrame(df['SunShineHour'] / nVaild['vaild']).dropna()[0].to_list(),
        "GlobalRad": pd.DataFrame(df['GlobalRad'] / nVaild['vaild']).dropna()[0].to_list(),
        "UV": pd.DataFrame(df['UV'] / nVaild['vaild']).dropna()[0].to_list(),
    })
    avedf = avedf.round(2)
    return avedf


def preprocess_data_weather(station_name: str):
    gen_station = pd.read_csv("./data/gen_station.csv")

    item = gen_station[gen_station['Station'] == station_name]
    sts = three_points_weather(item.iloc[0]['Lng'], item.iloc[0]['Lat'])
    # print(item['Station'], sts)

    w1 = get_data(sts[0]).fillna(0)
    w2 = get_data(sts[1]).fillna(0)
    w3 = get_data(sts[2]).fillna(0)

    return combine(w1, w2, w3)


def get_history_data(station_name: list, offset: int):

    finish = datetime.datetime.today() - datetime.timedelta(days=1)
    start = finish - datetime.timedelta(days=offset)

    data = []
    for station in station_name:
        temp = get_data_from_cwb(station, start, finish)
        data.append(temp)

    print(data[0].shape, data[1].shape, data[2].shape)

    df = combine(data[0], data[1], data[2])
    return df


if __name__ == "__main__":

    df = get_history_data(["臺北", "台中", '高雄'], datetime.date.today(), 30)
