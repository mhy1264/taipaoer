import csv
import pandas as pd

if __name__ == "__main__":
    index_cols1 = ["sitename","twd97lon","twd97lat"]
    index_cols2 = ["gen_lng","gen_lat"]

    df1 = pd.read_csv("./data/UV_rays.csv", usecols=index_cols1) #紫外線站資料
    df2 = pd.read_csv("./data/mini_dist2.csv", usecols=index_cols2)

    uv = df1["sitename"].to_list()
    uv_Lng = df1["twd97lon"].to_list()
    uv_Lat = df1["twd97lat"].to_list()

    solar_Lng = df2["gen_lng"].to_list()
    solar_Lat = df2["gen_lat"].to_list()

    inf = float('Inf')

    for i in range(len(solar_Lng)):
        min = inf

    # dataframe=[]

    # print(df2)