import sys
import pandas as pd 
import numpy as np
from haversine import haversine

#計算經緯度間距離
def cal_dis(s_Lng, s_Lat, uv_Lng, uv_Lat) -> float:
    d1 = (s_Lat, s_Lng)
    d2 = (uv_Lat, uv_Lng)
    dis = haversine(d1, d2) * 1000
    result = "%.7f" % dis
    return result

#計算兩點直線距離
def cal_str_dis(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

#判斷是否為三角形
def is_triangle(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    
    side1 = cal_str_dis(p1, p2)
    side2 = cal_str_dis(p2, p3)
    side3 = cal_str_dis(p1, p3)
    
    if(((side1 + side2) <= side3) | ((side2 + side3) <= side1) | ((side1 + side3) <= side2)):
        return False

    return (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) != 0

#找出目前暫存的最大值
def find_max(sta1, sta2, sta3):
    if ((sta1 >= sta2) & (sta1 >= sta3)):
        return 1
    elif ((sta2 >= sta1) & (sta2 >= sta3)):
        return 2
    elif ((sta3 >= sta1) & (sta3 >= sta2)):
        return 3
    else: 
        return False
    
def three_points_solar(Lng: float, Lat: float):
    stations = ['0']*3
    temp = [['0',inf],['0',inf],['0',inf]]

    for i in range(len(solar)):
        dis = cal_dis(Lng, Lat, solar_Lng[i], solar_Lat[i])
        dis = float(dis)
        if (dis < temp[0][1]) | (dis < temp[1][1]) | (dis < temp[2][1]):
            index = find_max(temp[0][1], temp[1][1], temp[2][1])
            temp[index - 1][0] = weather[i]
            temp[index - 1][1] = dis

    stations[0] = temp[0][0]
    stations[1] = temp[1][0]
    stations[2] = temp[2][0]
    
    return stations
    
def three_points_weather(Lng: float, Lat: float):
    stations = ['0']*3
    temp = [['0',inf],['0',inf],['0',inf]]

    for i in range(len(weather)):
        dis = cal_dis(Lng, Lat, weather_Lng[i], weather_Lat[i])
        dis = float(dis)
        if (dis < temp[0][1]) | (dis < temp[1][1]) | (dis < temp[2][1]):
            index = find_max(temp[0][1], temp[1][1], temp[2][1])
            temp[index - 1][0] = weather[i]
            temp[index - 1][1] = dis

    stations[0] = temp[0][0]
    stations[1] = temp[1][0]
    stations[2] = temp[2][0]
    
    return stations
    
def three_points_uva(Lng: float, Lat: float):
    stations = ['0']*3
    temp = [['0',inf],['0',inf],['0',inf]]

    for i in range(len(uv)):
        dis = cal_dis(Lng, Lat, uv_Lng[i], uv_Lat[i])
        dis = float(dis)
        if (dis < temp[0][1]) | (dis < temp[1][1]) | (dis < temp[2][1]):
            index = find_max(temp[0][1], temp[1][1], temp[2][1])
            temp[index - 1][0] = uv[i]
            temp[index - 1][1] = dis

    stations[0] = temp[0][0]
    stations[1] = temp[1][0]
    stations[2] = temp[2][0]

    return stations

if __name__ == "__main__":

    inf = float('Inf')

    df_gen = pd.read_csv(
    "./data/gen_station.csv")[["Station", "Lng", "Lat"]]  # 光電站
    df_weather = pd.read_csv(
    "./data/weather_station.csv")[["StationName", "StationLongitude", "StationLatitude"]]  # 氣象站
    df_uva = pd.read_csv(
        "./data/uva_station.csv")[["sitename", "twd97lon", "twd97lat"]]  #紫外線站
    
    solar = df_gen["Station"].to_list()
    solar_Lng = df_gen["Lng"].to_list()
    solar_Lat = df_gen["Lat"].to_list()

    weather = df_weather["StationName"].to_list()
    weather_Lng = df_weather["StationLongitude"].to_list()
    weather_Lat = df_weather["StationLatitude"].to_list()

    uv = df_uva["sitename"].to_list()
    uv_Lng = df_uva["twd97lon"].to_list()
    uv_Lat = df_uva["twd97lat"].to_list()

    #     lng = float(sys.argv[1])
    #     lat = float(sys.argv[2])
    s = three_points_solar(121.6,24.9)
    w = three_points_weather(121.6,24.9)
    u = three_points_uva(121.6,24.9)

    print(s)
    print(w)
    print(u)
