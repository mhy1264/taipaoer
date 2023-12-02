import pandas as pd
from util import cal_dis


if __name__ == "__main__":
    df1 = pd.read_csv(
        "./data/uva_station.csv")[["sitename", "twd97lon", "twd97lat"]]  # 紫外線站資料
    df2 = pd.read_csv("./data/gen_obv_min_dist.csv", index_col=False)
    dataframe = pd.DataFrame(df2)

    df2.drop(['Unnamed: 0'], axis=1)
    uv = df1["sitename"].to_list()
    uv_Lng = df1["twd97lon"].to_list()
    uv_Lat = df1["twd97lat"].to_list()

    solar_Lng = df2["gen_lng"].to_list()
    solar_Lat = df2["gen_lat"].to_list()

    inf = float('Inf')
    temp_sta = []
    temp_Lng = []
    temp_Lat = []

    for i in range(len(solar_Lng)):
        min = inf
        for k in range(len(uv)):
            dis = cal_dis(solar_Lng[i], solar_Lat[i], uv_Lng[k], uv_Lat[k])
            dis = float(dis)
            if dis < min:
                min = dis
                index = k
        temp_sta.append(uv[index])
        temp_Lng.append(uv_Lng[index])
        temp_Lat.append(uv_Lat[index])

    dataframe['uv_station'] = temp_sta
    dataframe['uv_lng'] = temp_Lng
    dataframe['uv_lat'] = temp_Lat
    dataframe.round(2).to_csv(
        "./data/gen_obv_min_dist_with_uv.csv", index=False)
