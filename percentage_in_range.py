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


def patient_bal_tar_plot(balances, targets, id=17771, plot=False, outcsv=False):
    # Extract data for one patientId
    stay_balances, stay_targets = stay_data(balances, targets, id)

    if outcsv == True:
        stay_balances.to_csv(str(id) + '_balances.csv')
        stay_targets.to_csv(str(id) + '_targets.csv')


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
    plotMat = np.zeros((len(fluid_min), 6))
    plotMat[:,0] = fluid_min
    plotMat[:,1] = fluid_cum
    # Set targets using timeline
    for i in range(len(target_min)):
        for j in range(len(fluid_min)):
            if plotMat[j][0] >= target_min[i]:
                plotMat[j][2] = target_low[i]
                plotMat[j][3] = target_high[i]
    plotMat[:,4] = fluid_stay['record day'].values
    plotMat[:,5] = fluid_stay['time of day'].replace('[^\d.]', '', regex=True).astype(float)/10000

    # Extract only rows with targets
    compareMat = plotMat[plotMat[:,0] >= target_min[0]]
    # Find distance to target boundary
    distMat = compareMat
    for i in range(len(compareMat)):
        if compareMat[i,1] < compareMat[i,2]:
            distMat[i,1] = compareMat[i,1] - compareMat[i,2]
        elif compareMat[i,1] > compareMat[i,3]:
            distMat[i,1] = compareMat[i,1] - compareMat[i,3]
        else:
            distMat[i,1] = 0.0
    # Delete targets
    distMat = np.delete(distMat, [2, 3], 1)
    # Add ID in first col
    distMat = np.hstack((np.full((len(distMat), 1), id), distMat))


    if plot == True:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(plotMat[:,0], plotMat[:,1], c='b', label='Fluid cumTotal')
        ax.plot(plotMat[:,0], plotMat[:,2], c='r', label='Target lower bound')
        ax.plot(plotMat[:,0], plotMat[:,3], c='g', label='Target upper bound')
        ax.legend()
        ax.set_title('Fluids plot for ID ' + str(id))
        ax.set_xlabel('Minutes since admission')
        ax.set_ylabel('Fluids balance [ml]')
        plt.show()

    return distMat


def dist_csvs(balances, targets):
    ids = np.unique(targets['encounterId'].values)
    print(len(ids), 'unique IDs')
    distTotal = np.array([])
    distDaily = np.array([])
    distHourly = np.array([])
    for i in range(len(ids)):
        distMat = patient_bal_tar_plot(balances, targets, id=ids[i])

        # Check for empty matrix, happens when target is set after length of stay
        if distMat.size:
            pass
        else:
            continue

        Euc_dist = np.sqrt(sum(distMat[:,2]**2))
        mean_dist = np.mean(abs(distMat[:,2]))
        dummyarr = np.array([ids[i], Euc_dist, mean_dist])
        distTotal = np.vstack((distTotal, dummyarr)) if distTotal.size else dummyarr

        for day in np.unique(distMat[:,3]):
            distDay = abs(np.where(distMat[:,3]==day, distMat[:,2], 0)).sum()
            dummyarr = np.array([ids[i], day, distDay])
            distDaily = np.vstack((distDaily, dummyarr)) if distDaily.size else dummyarr

        distHourly = np.vstack((distHourly, distMat)) if distHourly.size else distMat

    # Use pandas for headers
    distTotaldf = pd.DataFrame(data=distTotal, columns=['ID','EucDist','MeanDist'])
    distTotaldf.to_csv('distTotal.csv', index=False)
    distDailydf = pd.DataFrame(data=distDaily, columns=['ID','Day','TotalDayDist'])
    distDailydf.to_csv('distDaily.csv', index=False)
    distHourlydf = pd.DataFrame(data=distHourly, columns=['ID','Minute','DistFromTar','Day', 'Time'])
    distHourlydf.to_csv('distHourly.csv', index=False)

    # Use these for raw data no header
    #np.savetxt('distTotal.csv', distTotal, delimiter=',')
    #np.savetxt('distDaily.csv', distDaily, delimiter=',')
    #np.savetxt('distHourly.csv', distHourly, delimiter=',')

    return


def init():
    balances = pd.read_csv('data/anonymised_total_balances.csv')
    targets = pd.read_csv('data/anonymised_targets.csv')
    new_balances, new_targets = reduce_data(balances, targets)

    return new_balances, new_targets


if __name__ == "__main__":
    new_balances, new_targets = init()
    if len(sys.argv[1:]) == 0:
        dist_csvs(new_balances, new_targets)
    else:
        patient_bal_tar_plot(new_balances, new_targets, id=int(sys.argv[1]), plot=True, outcsv=True)
