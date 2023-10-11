# import brotli
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

def getAreaCode(station_name):
    N = "基隆 彭佳嶼 鞍部 臺北 陽明山 板橋 淡水 新屋 桃園 新竹 苗栗".split(' ')
    S = ["臺南", "永康", "新營", "高雄" ,"橋頭", "恆春","屏東"]
    I = ["東吉島","澎湖", "金門", "馬祖"]
    E = "宜蘭 花蓮 大武 成功 蘭嶼 臺東".split(' ')
    C = "臺中 沙鹿 田中 彰化 玉山 日月潭 南投 斗六 嘉義 朴子 塔塔加 阿里山".split(' ')
    
    if station_name in N:
        return "N"
    elif station_name in S:
        return "S"
    elif station_name in I:
        return "I"
    elif station_name in E:
        return "E"
    elif station_name in C:
        return "C"
    else:
        raise ValueError("Not Found")

def format_month(date = str)-> str:
    date = date.split('/')
    return '-'.join(date)

def get_data_by_month(year: int, month: int, station_name: str):
    area_code = getAreaCode(station_name)

    if month < 10:
        m = "{}{}".format(0, month)
    else:
        m = month
    url = "https://www.cwa.gov.tw/V8/C/D/MOD/UVIHistory/{}{}_{}.html".format(year,m, area_code)
    session = requests.session()
    web = session.get(url)
    cont = "{}{}{}".format("<table>", web.text, "</table>")
    table = bs(cont, features='lxml').find('table')
    print(table)
    df = pd.read_html(str(table))[0]
    date = df['日期'].tolist()
    val = df[station_name].tolist()
    new_df = pd.DataFrame({"date":date, "UVI max": val})
    new_df['date'] = new_df['date'].apply(lambda x: format_month(x))
    return new_df

def get_data(station_name: str):
    temp = pd.DataFrame(columns=['date', 'UVI max'])

    for year in range(2017, 2023):
        for month in range(1, 13):
            df = get_data_by_month(year, month, station_name)
            temp = pd.concat([temp, df])

    for month in range(1, 7):
        df = get_data_by_month(2023, month, station_name)
        temp = pd.concat([temp, df])

    return temp


if __name__ == "__main__":
    df = get_data_by_month(2023,2,'桃園')
    print(df)