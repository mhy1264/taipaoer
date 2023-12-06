from weather import preprocess_data_weather
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import tensorflow as tf
import autokeras as ak
import argparse as arg


if __name__ == "__main__":
    gen_data = pd.read_csv("./data/solar_daily.csv")

    epoch = 500
    max_trial = 100

    station = '金門金沙光電'

    weather = preprocess_data_weather(station+"站")
    
    gen_daily = pd.DataFrame()

    try:
        gen_daily = gen_data[station]
    except:
        raise KeyError("not found station")
    
    print(gen_daily)