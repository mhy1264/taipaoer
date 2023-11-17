import requests
import json
import pandas

if __name__ == "__main__":
    # session = requests.session()
    # payload = {
    #     "authorization": "CWA-824CFA50-E9D9-482B-93A5-8B63E3BC4E9A",
    #     "format": "JSON",
    #     "status": "%E7%8F%BE%E5%AD%98%E6%B8%AC%E7%AB%99"
    # }
    # res = session.get(
    #     "https://opendata.cwa.gov.tw/api/v1/rest/datastore/C-B0074-001?Authorization=CWA-824CFA50-E9D9-482B-93A5-8B63E3BC4E9A&format=JSON&status=%E7%8F%BE%E5%AD%98%E6%B8%AC%E7%AB%99")
    # obj = json.loads(res.text)
    # # print(obj["records"]['data']['stationStatus']['station'][0])

    # df = pandas.DataFrame.from_dict(obj["records"]['data']
    #                                 ['stationStatus']['station'])
    # df.to_csv("./data/weather_station1.csv")

    # res2 = session.get(
    #     "https://opendata.cwa.gov.tw/api/v1/rest/datastore/C-B0074-002?Authorization=CWA-824CFA50-E9D9-482B-93A5-8B63E3BC4E9A&status=%E7%8F%BE%E5%AD%98%E6%B8%AC%E7%AB%99")

    # obj = json.loads(res2.text)
    # # print(obj["records"]['data']['stationStatus']['station'][0])

    # df2 = pandas.DataFrame.from_dict(obj["records"]['data']
    #                                  ['stationStatus']['station'])

    # df2.to_csv("./data/weather_station2.csv")

    df = pandas.read_csv("./data/weather_station.csv")

    df = df[~df['StationID'].str.contains("C1")]

    df.to_csv("./data/weather_station.csv")
