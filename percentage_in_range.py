import csv
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from reduce_script import *

balances = pd.read_csv('data/anonymised_total_balances.csv')
targets = pd.read_csv('data/anonymised_targets.csv')

new_balances, new_targets = reduce(balances, targets)

def stay_data(balances,targets,id):

    #collect all data for one stay in one place

    stay_balances = balances.loc[balances['encounterId'] == id]
    stay_targets = targets.loc[targets['encounterId'] == id]

    return stay_balances, stay_targets

patientId = 17936
	
stay_balances, stay_targets = stay_data(new_balances,new_targets,patientId)

#stay_balances.to_csv('_balances.csv')
#stay_targets.to_csv('_targets.csv')


fluid_stay = stay_balances.loc[stay_balances['longLabel'] == 'Net Body Balance (24hr)']
fluid_cum = fluid_stay['cumTotal'].values
fluid_min = fluid_stay['minutes since admission'].values
target_stay = stay_targets['NumTargets'].values
target_low = np.zeros(len(target_stay))
target_high = np.zeros(len(target_stay))
for i in range(len(target_stay)):
	target_low[i] = target_stay[i][0]
	target_high[i] = target_stay[i][1]
target_min = stay_targets['minutes since admission'].values



fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(fluid_min,fluid_cum)
ax.scatter(target_min, target_low, s=10, c='r')
ax.scatter(target_min, target_high, s=10, c='g')
plt.show()
