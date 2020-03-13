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
patient1 = patient1.loc[patient1['record day'] == 2]
print(patient1.head())

patient1in = patient1.loc[patient1['longLabel']=='Total In (24hr)']
print(patient1in.head())

patient1out = patient1.loc[patient1['longLabel']=='Total Out (24hr)']
print(patient1in.head())

intotal = patient1in['cumTotal']
intotal = intotal.values

outtotal = patient1out['cumTotal']
outtotal = outtotal.values

print(len(intotal))


balance = intotal + outtotal
print(balance)

darray = np.vstack((patient1in['minutes since admission'].values,balance))
darray = darray.T
print(darray)

sortedarray = np.sort(darray,axis = 0)
print(sortedarray)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(sortedarray[:,0],sortedarray[:,1])
plt.show()