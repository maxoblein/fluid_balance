import csv
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


def add_day_of_week(data):

    record_days = data['record day'].values
    day_of_week = (record_days % 7)
    print(day_of_week)
    data['day of week'] = day_of_week
    return data

balances = pd.read_csv('new_balances.csv')

add_day_of_week(balances)
