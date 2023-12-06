import pandas as pd
import requests
import requests
import json
import pandas as pd


df = pd.read_csv("./station_place.csv")

# 取得太陽能的資料
df = df[df["能源別/Energy Type"] == "太陽能/Solar"]

df = df[["發電站名稱/Station Name", "地址/Address"]]

storeaddress = df["地址/Address"].to_list()
stat = df["發電站名稱/Station Name"].to_list()
geo = []
api_key = ""

for i in range(len(storeaddress)):
    address = storeaddress[i]
    station = stat[i]
    uri = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(
        address, api_key
    )
    res = requests.get(uri)
    obj = json.loads(res.text)
    lat, lon = 0, 0
    if obj["status"] == "OK":
        print("{} --> ok".format(address))
        lat = obj["results"][0]["geometry"]["location"]["lat"]
        lon = obj["results"][0]["geometry"]["location"]["lng"]
    else:
        print("{} --> fail".format(address))
    temp = [station, address, lon, lat]
    geo.append(temp)


print(geo)

result = pd.DataFrame(geo, columns=["Station", "Addr", "lng", "lat"])

print(result.head())

df = result.drop_duplicates(subset=result.columns, keep="first")
print(df.shape)
df.to_csv("./station.csv")
