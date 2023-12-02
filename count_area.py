import sys
import pandas as pd 
import numpy as np
from haversine import haversine
import math

INF = math.inf

#計算經緯度間距離
def cal_dis(s_Lng, s_Lat, uv_Lng, uv_Lat) -> float:
    d1 = (s_Lat, s_Lng)
    d2 = (uv_Lat, uv_Lng)
    dis = haversine(d1, d2) * 1000
    result = "%.7f" % dis
    return result

#找出目前暫存的最大值
def find_max(sta1, sta2, sta3):
    sta = [sta1, sta2, sta3]
    max_val = max(sta)
    return sta.index(max_val) if max_val in sta else False


def three_points_solar(Lng: float, Lat: float):
    solar = pd.read_csv("./data/gen_station.csv")[["Station", "Lng", "Lat"]]  # 光電站
    temp = [['0',INF],['0',INF],['0',INF]]

    for i in range(len(solar)):
        dis = cal_dis(Lng, Lat, solar["Lng"][i], solar["Lat"][i])
        dis = float(dis)
        if (dis < temp[0][1]) | (dis < temp[1][1]) | (dis < temp[2][1]):
            index = find_max(temp[0][1], temp[1][1], temp[2][1])
            temp[index - 1][0] = solar["Station"][i]
            temp[index - 1][1] = dis
    
    return [temp[0][0], temp[1][0], temp[2][0]]
    
def three_points_weather(Lng: float, Lat: float):
    weather = pd.read_csv(
    "./data/weather_station.csv")[["StationName", "StationLongitude", "StationLatitude"]]  # 氣象站
        
    temp = [['0',INF],['0',INF],['0',INF]]

    for i in range(len(weather)):
        dis = cal_dis(Lng, Lat, weather["StationLongitude"][i], weather["StationLatitude"][i])
        dis = float(dis)
        if (dis < temp[0][1]) | (dis < temp[1][1]) | (dis < temp[2][1]):
            index = find_max(temp[0][1], temp[1][1], temp[2][1])
            temp[index - 1][0] = weather["StationName"][i]
            temp[index - 1][1] = dis

    return [temp[0][0], temp[1][0], temp[2][0]]
    
def three_points_uva(Lng: float, Lat: float):

    uva = pd.read_csv(
        "./data/uva_station.csv")[["sitename", "twd97lon", "twd97lat"]]  #紫外線站

    temp = [['0',INF],['0',INF],['0',INF]]

    for i in range(len(uva)):
        dis = cal_dis(Lng, Lat, uva["twd97lon"][i], uva["twd97lat"][i])
        dis = float(dis)
        if (dis < temp[0][1]) | (dis < temp[1][1]) | (dis < temp[2][1]):
            index = find_max(temp[0][1], temp[1][1], temp[2][1])
            temp[index - 1][0] = uva["sitename"][i]
            temp[index - 1][1] = dis

    return [temp[0][0], temp[1][0], temp[2][0]]

if __name__ == "__main__":

    s = three_points_solar(120.9876, 23.83876)
    w = three_points_weather(120.9876, 23.83876)
    u = three_points_uva(120.9876, 23.8387)

    # print(s)
    print(w)
    # print(u)
