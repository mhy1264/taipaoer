import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import urllib.parse
import datetime


def transformat(string: str) -> str:
    string = urllib.parse.quote(string)
    string = "%25".join(string.split("%"))
    return string


def get_station_info(name: str) -> list:
    df = pd.read_csv("./data/weather_station.csv")
    fliter = (df["站名"] == name)
    info = df[fliter].iloc[0]
    return [info['站號'], info['海拔高度(m)']]


def seperate(df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    col = df.columns.to_list()
    new_col = []

    for i in col:
        new_col.append(i[2])

    new_col[0] = "date"
    temp_list = []

    for i in range(df.shape[0]):
        data = df.iloc[i].tolist()
        data[0] = datetime.date(int(year), int(month), int(data[0]))
        temp_list.append(data)

    new_df = pd.DataFrame(temp_list, columns=new_col)
    new_df = new_df.drop(['StnPresMax', 'StnPresMaxTime', 'StnPresMin', 'StnPresMinTime', 'T Max', 'T Max Time', 'T Min', 'T Min Time', 'RHMin', 
                          'RHMinTime', 'WSGust', 'WDGust', 'WGustTime', 'PrecpHour', 'PrecpMax10', 'PrecpMax10Time', 'PrecpMax60', 'PrecpMax60Time', 'UVI Max Time'], axis=1)
    new_df = new_df.replace('...', np.nan)
    new_df = new_df.replace('T', 0.1)
    new_df = new_df.replace('x', np.nan)
    new_df = new_df.replace('V', np.nan)

    return new_df


def get_month_data(name: str, year: int, month: int) -> pd.DataFrame:
    if month < 10:
        month = "0{}".format(month)
    else:
        month = str(month)
    info = get_station_info(name)

    URL = "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station={}&stname={}&datepicker={}-{}&altitude={}m#".format(
        info[0], transformat(name), year, month, info[1]
    )
    try:
        print(URL)
        web = requests.get(URL)
        soup = bs(web.text, "lxml")

        table = soup.find_all("table", {"id": "MyTable"})

        df = pd.read_html(str(table[0]))[0]
        df = seperate(df, year, month)
        return df
    except:
        raise ValueError("未找到站名 || 資訊取得錯誤")


def get_day_data(name: str, date : datetime.date) -> pd.DataFrame:
    df = get_month_data(name, year=date.year, month=date.month)
    return df.iloc[date.day-1:date.day]

def get_data(station: str) -> pd.DataFrame:
    col = [('Unnamed: 0_level_0', '觀測時間 (day)', 'ObsTime'), ('press', '測站氣壓 (hPa)', 'StnPres'), ('press', '海平面氣壓 (hPa)', 'SeaPres'), ('press', '測站最高氣壓 (hPa)', 'StnPresMax'), ('press', '測站最高氣壓時間 (LST)', 'StnPresMaxTime'), ('press', '測站最低氣壓 (hPa)', 'StnPresMin'), ('press', '測站最低氣壓時間 (LST)', 'StnPresMinTime'), ('temperature', '氣溫 (℃)', 'Temperature'), ('temperature', '最高氣溫 (℃)', 'T Max'), ('temperature', '最高氣溫時間 (LST)', 'T Max Time'), ('temperature', '最低氣溫 (℃)', 'T Min'), ('temperature', '最低氣溫時間 (LST)', 'T Min Time'), ('Dew Point', '露點溫度 (℃)', 'Td dew point'), ('RH', '相對溼度 (%)', 'RH'), ('RH', '最小相對溼度 (%)', 'RHMin'), ('RH', '最小相對溼度時間 (LST)', 'RHMinTime'), ('WS/WD', '風速 (m/s)', 'WS'), ('WS/WD', '風向 (360degree)', 'WD'), ('WS/WD', '最大瞬間風 (m/s)', 'WSGust'), ('WS/WD', '最大瞬間風風向 (360degree)', 'WDGust'), ('WS/WD', '最大瞬間風風速時間 (LST)', 'WGustTime'), ('Precp', '降水量 (mm)', 'Precp'), ('Precp', '降水時數 (hour)', 'PrecpHour'), ('Precp', '最大十分鐘降水量 (mm)', 'PrecpMax10'), ('Precp', '最大十分鐘降水量起始時間 (LST)', 'PrecpMax10Time'), ('Precp', '最大六十分鐘降水量 (mm)', 'PrecpMax60'), ('Precp', '最大六十分鐘降水量起始時間 (LST)', 'PrecpMax60Time'), ('SunShine', '日照時數 (hour)', 'SunShine'), ('SunShine', '日照率 (%)', 'SunShineRate'), ('SunShine', '全天空日射量 (MJ/㎡)', 'GloblRad'), ('visibility', '能見度 (km)', 'VisbMean'), ('Evaperation', 'A型蒸發量 (mm)', 'EvapA'), ('UVI', '日最高紫外線指數', 'UVI Max'), ('UVI', '日最高紫外線指數時間 (LST)', 'UVI Max Time'), ('Cloud', '總雲量 (0~10)', 'Cloud Amount')]
    new_col = ['date']
    for i in col:
        new_col.append(i[2])
    temp = pd.DataFrame(columns=new_col)

    for year in range(2017, 2024):
        for month in range(1, 13):
            df = get_month_data(station, year, month)
            temp = pd.concat([temp, df])

    for month in range(1, 7):
        df = get_month_data(station, 2023, month)
        temp = pd.concat([temp, df])

    return temp


if __name__ == "__main__":
    print(get_month_data('金沙', 2017, 1))