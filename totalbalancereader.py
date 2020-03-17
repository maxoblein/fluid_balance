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
patients = [2,3,4]
fig = plt.figure()
ax = fig.add_subplot(111)
for i in patients:
	patient1 = data.loc[data['encounterId']==822]
	patient1 = patient1.loc[patient1['record day'] == i]

	patient1in = patient1.loc[patient1['longLabel']=='Total In (24hr)']


	patient1out = patient1.loc[patient1['longLabel']=='Total Out (24hr)']

	intotal = patient1in['cumTotal']
	intotal = intotal.values

	outtotal = patient1out['cumTotal']
	outtotal = outtotal.values



	balance = intotal + outtotal


	darray = np.vstack((patient1in['time of day'].values,balance))
	darray = darray.T


	sortedarray = darray[darray[:,0].argsort()]



	
	ax.scatter(sortedarray[:,0],sortedarray[:,1])

plt.show()
