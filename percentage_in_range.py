import csv
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from adjust_data import *
import sys


def stay_data(balances, targets, id):
    # Collect all data for one stay in one place
    stay_balances = balances.loc[balances['encounterId'] == id]
    stay_targets = targets.loc[targets['encounterId'] == id]

    # Sort timeline for linear timeflow
    stay_balances = stay_balances.sort_values(by=['minutes since admission'])
    stay_targets = stay_targets.sort_values(by=['minutes since admission'])

    return stay_balances, stay_targets


def patient_bal_tar_plot(id, plot=False, outcsv=False):
    balances = pd.read_csv('data/anonymised_total_balances.csv')
    targets = pd.read_csv('data/anonymised_targets.csv')

    new_balances, new_targets = reduce_data(balances, targets)

    # Check commandline
    if len(id) > 0:
        patientId = int(id[0])
    else:
        # Default patientId, can adjust this manually if no command line input
        patientId = 17771

    # Extract data for one patientId
    stay_balances, stay_targets = stay_data(new_balances, new_targets, patientId)

    if outcsv == True:
        stay_balances.to_csv(str(patientId) + '_balances.csv')
        stay_targets.to_csv(str(patientId) + '_targets.csv')


    # Extract fluid info
    fluid_stay = stay_balances.loc[stay_balances['longLabel'] == 'Net Body Balance (24hr)']
    fluid_cum = fluid_stay['cumTotal'].values
    fluid_min = fluid_stay['minutes since admission'].values

    # Extract target info
    target_stay = stay_targets['NumTargets'].values
    target_low = np.zeros(len(target_stay))
    target_high = np.zeros(len(target_stay))
    for i in range(len(target_stay)):
        target_low[i] = target_stay[i][0]
        target_high[i] = target_stay[i][1]
    target_min = stay_targets['minutes since admission'].values

    # Collect info for plot in one matrix
    plotMat = np.zeros((len(fluid_min), 4))
    plotMat[:,0] = fluid_min[:]
    plotMat[:,1] = fluid_cum[:]
    # Set targets using timeline
    for i in range(len(target_min)):
        for j in range(len(fluid_min)):
            if target_min[i] < plotMat[j][0]:
                plotMat[j][2] = target_low[i]
                plotMat[j][3] = target_high[i]


    if plot == True:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(plotMat[:,0], plotMat[:,1], c='b', label='Fluid cumTotal')
        ax.plot(plotMat[:,0], plotMat[:,2], c='r', label='Target lower bound')
        ax.plot(plotMat[:,0], plotMat[:,3], c='g', label='Target upper bound')
        ax.legend()
        plt.show()




if __name__ == "__main__":
    patient_bal_tar_plot(sys.argv[1:], plot=True, outcsv=True)
