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
├── data
│   ├── dist.csv             --> 每個觀測站對於發電站的距離
│   ├── mini_dist2.csv       --> 距離某個發電站最近的觀測站
│   ├── solar_daily.csv      --> 每日發電量報表（日期格式為dateTime）
│   ├── solar_day.csv        --> 每日發電量報表（日期格式為三個 Row 分別為年、月、日）
│   ├── station.csv          --> 發電站資訊
│   └── weather_station.csv  --> 觀測站資訊
```


# code Description
```
├── filter_station.py        --> 濾掉沒有紫外線的氣象站
├── find_distance.py         --> 取得觀測站到發電站的距離
├── find_min_distance.py     --> 取得離觀測站最近的發電站
├── find_uv_distance.py      --> 
├── newWeather.py            --> 利用新版網站取得氣象資訊
├── paritial_train.py        --> 訓練單一的發電站
├── place_to_lat.py          --> 取得發電站的經緯度
├── preprocess.py            -->
├── split_data.py            --> 把訓練料分割
├── train.py                 -->
├── uva.py                   --> 取得某個紫外線觀測站的數值
└── weather.py               -->
```