# taipower 

# description
一個可以藉由經緯度去預測太陽能發電量的程式

# data sources
* CBA open date
* CBA 天氣觀測網

# Depencies
```
scikit-learn
autoKeras
pandas
numpy
openpyxl
requests
lxml
bs4
```

# file Description
```
./data
├── dist.csv                         --> 每個觀測站對於發電站的距離
├── gen_obv_dist.csv                 --> 發電站和觀測站的距離
├── gen_obv_mini_dist_with_uv.csv    --> 發電站和觀測站的最短距離
├── gen_station.csv                  --> 發電站列表
├── solar_daily.csv                  --> 每日發電量報表（日期格式為dateTime）
├── uva_station.csv                  --> 發電站列表
└── weather_station.csv              --> 觀測站列表

```


# code Description
```
├── find_distance.py         --> 取得觀測站到發電站的距離
├── find_min_distance.py     --> 取得離發電站最近的天氣觀測站
├── find_uv_distance.py      --> 取得離發電站最近的紫外線觀測站
├── newWeather.py            --> 利用新版網站取得氣象資訊
├── paritial_train.py        --> 訓練單一的發電站
├── place_to_lat.py          --> 取得發電站的經緯度
├── preprocess.py            --> 合併天氣資料、紫外線資料、發電資料
├── split_data.py            --> 把訓練料分割
├── train.py                 --> 訓練檔案
├── uva.py                   --> 取得某個紫外線觀測站的數值
└── weather.py               --> 取得天氣資料

```