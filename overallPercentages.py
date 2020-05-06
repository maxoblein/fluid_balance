import csv
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from adjust_data import *
import sys
from matplotlib.ticker import PercentFormatter

def gen_distances(balances, targets):

    # Don't think you actually need this function any more it's just and adaptation of
    # percentage_in_range for percentage balances.

    patient_summaries = patient_summary()

    # Sort timeline for linear timeflow
    balances = balances.sort_values(by=['encounterId','minutes since admission'])
    targets_df = targets.sort_values(by=['encounterId','minutes since admission'])
    targets_df = fix_targets(targets_df)

    fluid_balances_df = balances.loc[balances['longLabel'] == 'Net Body Balance (24hr)']
    fluid_balances = fluid_balances_df['cumTotal'].values
    fluid_min = fluid_balances_df['minutes since admission'].values
    patients_fluid = fluid_balances_df['encounterId'].values

    percent_balances = np.zeros(len(fluid_balances))
    for i in range(len(fluid_balances)):
        percent_balances[i] = (fluid_balances[i]/patient_summaries[patients_fluid[i]][2])*100

    # Extract target info
    targets = targets_df['NumTargets'].values
    target_low = np.zeros(len(targets))
    target_high = np.zeros(len(targets))
    patients_targets = targets_df['encounterId'].values
    for i in range(len(targets)):
        target_low[i] = (targets[i][0]/patient_summaries[patients_targets[i]][2])*100
        target_high[i] = (targets[i][1]/patient_summaries[patients_targets[i]][2])*100
    target_min = targets_df['minutes since admission'].values

    # Collect info for plot in one matrix
    plotMat = np.zeros((len(fluid_min), 8))
    plotMat[:,0] = fluid_min
    plotMat[:,1] = percent_balances
    plotMat[:,6] = patients_fluid
    plotMat[:,7] = np.zeros(len(fluid_min))
    # Set targets using timeline
    for i in range(len(target_min)):
        completion = 100*((i+1)/len(target_min-1))
        sys.stdout.write("\rGenerating Percentage Distances: %.0f%% Complete"%(completion))
        sys.stdout.flush()
        # print("\r%.1f/%.1f"%(i+1,len(target_min-1)))
        for j in range(len(fluid_min)):
            if plotMat[j][0] >= target_min[i] and patients_fluid[j] == patients_targets[i]:
                plotMat[j][2] = target_low[i]
                plotMat[j][3] = target_high[i]
                plotMat[j][7] = 1
    plotMat[:,4] = fluid_balances_df['record day'].values
    plotMat[:,5] = fluid_balances_df['time of day'].replace('[^\d.]', '', regex=True).astype(float)/10000
    print('\n')
    # Extract only rows with targets
    compareMat = plotMat#[plotMat[:,0] >= target_min[0]]
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
    # distMat = np.delete(distMat, [2, 3], 1)

    dist_df = pd.DataFrame(data=distMat, columns=['Minute','DistFromTar','','','Day', 'Time','ID','Useable'])
    dist_df.to_csv('dist_percent_weight.csv', index=False)

    return

def plot_distances(distances_df, dist_type='euclid',plot=False,zero_distances=False):

    # dist_type = 'euclid' or 'percent' or 'percent_csv' depending on data input

    if dist_type == 'euclid':
        distances = distances_df['DistFromTar'].values

    elif dist_type == 'percent':
        distances = distances_df['DistFromTar'].values
        patients = distances_df['ID'].values
        patient_summaries = patient_summary()
        for i in range(len(distances)):
            distances[i] = (distances[i]/patient_summaries[patients[i]][2])*100

    elif dist_type == 'percent_csv':
            distances_df = distances_df.loc[distances_df['Useable'] == 1]
            distances = distances_df['DistFromTar'].values
            patients = distances_df['ID'].values
            useable = distances_df['Useable'].values
            useable_distances = []
            for i in range(len(distances)):
                if distances[i] == np.inf or distances[i] == -np.inf or distances[i] == np.nan:
                    useable[i] = 0
                if useable[i] == 1:
                    useable_distances.append(distances[i])
            distances = useable_distances

    if zero_distances == False:
        distances = np.setdiff1d(distances,np.asarray(0)) # Removes distances of zero

    distance_range = np.arange(-5025,5025,50) # Range of x on histogram

    if plot == True:
        plt.hist(distances,distance_range)
        plt.xlabel('Distance from Target Range')
        plt.ylabel('Proportion of Values Within Range')
        plt.gca().yaxis.set_major_formatter(PercentFormatter(len(distances)))
        plt.gca().xaxis.set_major_formatter(PercentFormatter(500))
        plt.tight_layout()
        plt.show()

    return distances

if __name__ == '__main__':

    euc_distances = pd.read_csv('distHourly.csv')
    # Plots Euclidean
    plot_distances(euc_distances, dist_type='euclid',plot=True,zero_distances=False)
    # # Generates percentage distances fron distHourly file
    # plot_distances(euc_distances, dist_type='percent',plot=False,zero_distances=False)

    # # Generates percentage distances from scratch
    # # You don't really need to use this
    # new_balances = pd.read_csv('data/new_balances.csv')
    # new_targets = pd.read_csv('data/new_targets.csv')
    # # Generating the CSV file of distances using the percentage weight method
    # # gen_distances(new_balances, new_targets)
    # percent_distances = pd.read_csv('dist_percent_weight.csv')
    # plot_distances(percent_distances, dist_type='percent_csv',plot=False,zero_distances=False)
