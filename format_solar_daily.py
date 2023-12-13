import pandas as pd

if __name__ == "__main__":
    data = pd.read_csv("data/太陽光電.csv")

    old_column = data.columns
    print(old_column)
    new_colun = []

    for i in range(len(old_column)):
        temp_name = old_column[i].split("/")
        print(len(temp_name))
        if (len(temp_name) == 2):
            new_colun.append(temp_name[0])
        if (len(temp_name) == 4):
            new_colun.append(temp_name[0]+"/"+temp_name[1])

    for i in range(0, len(new_colun)):
        data.rename(columns={old_column[i]: new_colun[i]}, inplace=True)

    date = []
    for i in range(data.shape[0]):
        date.append(
            '{}-{}-{}'.format(data.iloc[i, 0], "0{}".format(data.iloc[i, 1]) if data.iloc[i, 1] < 10 else "{}".format(data.iloc[i, 1]), "0{}".format(data.iloc[i, 2]) if data.iloc[i, 2] < 10 else "{}".format(data.iloc[i, 2])))

    data["date"] = date
    print(data.columns)

    data.drop(["年度", "月份", "日期"], axis=1, inplace=True)

    print(data.head())
    data.to_csv("data/solar_daily.csv", index=False)
