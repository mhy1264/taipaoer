import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import urllib.parse
import pandas as pd
import json
from calendar import isleap
import uva


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
        # if (df['UV'] == -1).all():
        #     UVinfo = uva.get_data_by_month(int(year), int(month), UVStation)[
        #         "UVI Max"].to_list()
        #     df['UV'] = UVinfo
        #     df['HaveEmpty'] = [True]*len(UVinfo)
        return df
    else:
        raise ValueError("mata Count = 0")


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
