import csv
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from adjust_data import *
import sys
from matplotlib.ticker import PercentFormatter


def calc_distances(distances_df,dist_type,plot_type,individual_patient):
    
    if individual_patient:
        distances_df = distances_df.loc[distances_df['ID'] == individual_patient] 
        plot_type = 'all'

    ##################################################

    if plot_type == 'all':
        distances = distances_df['DistFromTar'].values

    elif plot_type == 'midnight':
        distances_df = distances_df.loc[distances_df['Time'] == 0]   
        distances = distances_df['DistFromTar'].values

    elif plot_type == 'furthest': 
        distances = []
        unique_patients = np.unique(distances_df['ID'].values)

        for patient in unique_patients:
            patient_distances_df = distances_df.loc[distances_df['ID'] == patient]
            patient_distances = patient_distances_df['DistFromTar'].values
            distances.append(max(patient_distances.min(), patient_distances.max(), key=abs))

    elif plot_type == 'average':
        distances = []
        unique_patients = np.unique(distances_df['ID'].values)

        for patient in unique_patients:
            patient_distances_df = distances_df.loc[distances_df['ID'] == patient]
            patient_distances = patient_distances_df['DistFromTar'].values
            distances.append(np.mean(patient_distances))

    ##################################################

    if dist_type == 'euclid':  
        None

    elif dist_type == 'percent':
        patients = distances_df['ID'].values
        patient_summaries = patient_summary()
        for i in range(len(distances)):
            distances[i] = (distances[i]/patient_summaries[patients[i]][2])*100 

    return distances

def plot_distances(distances_df, 
                   dist_type='euclid',
                   plot_type='all',
                   plot=False,
                   zero_distances=False,
                   individual_patient=False):

    # dist_type = 'euclid' or 'percent' or 'percent_csv' depending on data input
    # plot_type = 'all', 'furthest', 'midnight' or 'average'

    distances = calc_distances(distances_df,dist_type,plot_type,individual_patient)    

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

def plot_4_hist(distances_df,plot=True):

    all_distances = plot_distances(euc_distances, 
                   dist_type='euclid',
                   plot_type='all', 
                   plot=False,
                   zero_distances=True,
                   individual_patient=None)

    average_distances = plot_distances(euc_distances, 
                   dist_type='euclid',
                   plot_type='average', 
                   plot=False,
                   zero_distances=True,
                   individual_patient=None)

    furthest_distances = plot_distances(euc_distances, 
                   dist_type='euclid',
                   plot_type='furthest', 
                   plot=False,
                   zero_distances=True,
                   individual_patient=None)

    midnight_distances = plot_distances(euc_distances, 
                   dist_type='euclid',
                   plot_type='midnight', 
                   plot=False,
                   zero_distances=True,
                   individual_patient=None)

    distance_range = np.arange(-5025,5025,50)

    fig1 = plt.figure(figsize = [14,12])
    ax1 = fig1.add_subplot(2,2,1)
    ax1.hist(all_distances,distance_range)
    ax1.set_title("All Distances")
    ax1.set_xlabel('Distance from Target Range')
    ax1.set_ylabel('Proportion of Values Within Range')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(len(all_distances)))
    plt.gca().xaxis.set_major_formatter(PercentFormatter(500))

    ax2 = fig1.add_subplot(2,2,2)
    ax2.hist(average_distances,distance_range)
    ax2.set_title("Average Patient Distances")
    ax2.set_xlabel('Distance from Target Range')
    ax2.set_ylabel('Proportion of Values Within Range')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(len(average_distances)))
    plt.gca().xaxis.set_major_formatter(PercentFormatter(500))

    ax3 = fig1.add_subplot(2,2,3)
    ax3.hist(furthest_distances,distance_range)
    ax3.set_title("Furthest Patient Distances")
    ax3.set_xlabel('Distance from Target Range')
    ax3.set_ylabel('Proportion of Values Within Range')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(len(furthest_distances)))
    plt.gca().xaxis.set_major_formatter(PercentFormatter(500))

    ax4 = fig1.add_subplot(2,2,4)
    ax4.hist(midnight_distances,distance_range)
    ax4.set_title("Midnight Patient Distances")
    ax4.set_xlabel('Distance from Target Range')
    ax4.set_ylabel('Proportion of Values Within Range')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(len(midnight_distances)))
    plt.gca().xaxis.set_major_formatter(PercentFormatter(500))

    # plt.subplots_adjust(top=5,bottom=0.98)
    fig1.tight_layout()

    if plot == True:
        plt.show()

    return None

if __name__ == '__main__':

    euc_distances = pd.read_csv('distHourly.csv')
     
    # # Generates percentage distances fron distHourly file
    # plot_distances(euc_distances, 
    #              dist_type='euclid',
    #              plot_type='average', 
    #              plot=True,
    #              zero_distances=False,
    #              individual_patient=None)

    # plot_4_hist(euc_distances,plot=True)





