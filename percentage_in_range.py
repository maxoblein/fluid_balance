import csv
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from adjust_data import *
import sys


def stay_data(balances,targets,id):
    #collect all data for one stay in one place
    stay_balances = balances.loc[balances['encounterId'] == id]
    stay_targets = targets.loc[targets['encounterId'] == id]
    return stay_balances, stay_targets


def patient_bal_tar_plot(id,plot=False):
    balances = pd.read_csv('data/anonymised_total_balances.csv')
    targets = pd.read_csv('data/anonymised_targets.csv')

    new_balances, new_targets = reduce_data(balances, targets)

    if len(id) > 0:
        patientId = int(id[0])
    else:
        patientId = 17771 # Default patientId, can adjust this manually if no command line input

    stay_balances, stay_targets = stay_data(new_balances,new_targets,patientId)


    stay_balances.to_csv(str(patientId) + '_balances.csv')
    stay_targets.to_csv(str(patientId) + '_targets.csv')


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

    if plot == True:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(fluid_min, fluid_cum)
        ax.scatter(target_min, target_low, linewidth=2, c='r')
        ax.scatter(target_min, target_high, linewidth=2, c='g')
        plt.show()




if __name__ == "__main__":
    patient_bal_tar_plot(sys.argv[1:],plot = True)
