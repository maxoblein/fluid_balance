import csv
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from adjust_data import *
import sys
from matplotlib.ticker import PercentFormatter
import scipy.stats as stats
from labellines import *


def calc_distances(distances_df,dist_type,plot_type,individual_patient):
    
    if individual_patient:
        distances_df = distances_df.loc[distances_df['ID'] == individual_patient] 
        plot_type = 'all'

    ##################################################

    if plot_type == 'all':
        distances = distances_df['DistFromTar'].values

    elif type(plot_type) == int:
        distances_df = distances_df.loc[distances_df['Time'] == plot_type]   
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

def plot_hist(fig,ax,distance_range,distances,title,bars=True,line=True,label=None,density=True):

    if bars:
        n,x,_ = ax.hist(distances,distance_range,histtype=u'step',density=density)
    else:
        n,x = np.histogram(distances,distance_range,density=density)
    if line:
        density = stats.gaussian_kde(distances)
        # print(density._compute_covariance())
        plt.plot(x, density(x),label=label)
    if title:
        ax.set_title(title)
    ax.set_xlabel('Distance from Target Range')
    if density:
        ax.set_ylabel('Density Function')
    else:
        ax.set_ylabel('Proportion of Values Within Range')
    # plt.gca().yaxis.set_major_formatter(PercentFormatter(len(distances)))
    plt.gca().xaxis.set_major_formatter(PercentFormatter(500))

    return n,x


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

        fig1 = plt.figure(figsize = [6,5])
        ax1 = fig1.add_subplot(1,1,1)
        plot_hist(fig1,ax1,distance_range,distances,None,bars=True,line=True)
        fig1.tight_layout()
        plt.show()

    return distances

def plot_4_hist(distances_df,plot=True):

    all_distances = plot_distances(euc_distances,dist_type='euclid',plot_type='all',plot=False,zero_distances=True,individual_patient=None)
    average_distances = plot_distances(euc_distances,dist_type='euclid',plot_type='average',plot=False,zero_distances=True,individual_patient=None)
    furthest_distances = plot_distances(euc_distances,dist_type='euclid',plot_type='furthest',plot=False,zero_distances=True,individual_patient=None)
    midnight_distances = plot_distances(euc_distances,dist_type='euclid',plot_type=0,plot=False,zero_distances=True,individual_patient=None)

    distance_range = np.arange(-5025,5025,50)

    fig1 = plt.figure(figsize = [14,12])
    ax1 = fig1.add_subplot(2,2,1)
    plot_hist(fig1,ax1,distance_range,all_distances,"All Distances",bars=True,line=False)
    ax2 = fig1.add_subplot(2,2,2)
    plot_hist(fig1,ax2,distance_range,average_distances,"Average Patient Distances",bars=True,line=False)
    ax3 = fig1.add_subplot(2,2,3)
    plot_hist(fig1,ax3,distance_range,furthest_distances,"Furthest Patient Distances",bars=True,line=False)
    ax4 = fig1.add_subplot(2,2,4)
    plot_hist(fig1,ax4,distance_range,midnight_distances,"Midnight Distances",bars=True,line=False)

    # plt.subplots_adjust(top=5,bottom=0.98)
    fig1.tight_layout()

    if plot == True:
        plt.show()

    return None

def plot_multiple_densities(distances_df,plot=True):

    # 0_distances = plot_distances(euc_distances,dist_type='euclid',plot_type=0,plot=False,zero_distances=True,individual_patient=None)
    
    distance_range = np.arange(-5025,5025,50) # Range of x on histogram

    if plot == True:

        fig1 = plt.figure(figsize = [12,10])
        ax1 = fig1.add_subplot(1,1,1)
        for i in range(24):
            distances = plot_distances(euc_distances,dist_type='euclid',plot_type=i,plot=False,zero_distances=False,individual_patient=None)
            plot_hist(fig1,ax1,distance_range,distances,None,bars=False,line=True,label=str(i))
        # labelLines(plt.gca().get_lines())#,zorder=2.5)
        fig1.tight_layout()
        plt.legend()
        plt.show()

    return 

if __name__ == '__main__':

    euc_distances = pd.read_csv('distHourly.csv')
     
    # # Generates percentage distances fron distHourly file
    # plot_distances(euc_distances, 
    #                dist_type='euclid',
    #                plot_type='average', 
    #                plot=True,
    #                zero_distances=False,
    #                individual_patient=None)

    # # Plots the 4 bar charts on one figure
    # plot_4_hist(euc_distances,plot=True)

    # # Plotting multiple lines on same graph
    # plot_multiple_densities(euc_distances)





