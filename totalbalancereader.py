import csv
from matplotlib import pyplot as plt
import numpy as np
from statistics import mean
from datetime import datetime
import pandas as pd

data = pd.read_csv("data/anonymised_total_balances.csv",nrows=10000)
data = data.drop(data.columns[0],axis=1)
print(data.head())
print(data.dtypes)

patient1 = data.loc[data['encounterId']==822]
print(patient1.head())

patient1in = patient1.loc[patient1['longLabel']=='Total In (24hr)']
print(patient1in.head())

patient1out = patient1.loc[patient1['longLabel']=='Total Out (24hr)']
print(patient1in.head())

patient1diff = patient1in.loc[patient1in['cumTotal']]