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


def main(argv):
    balances = pd.read_csv('data/anonymised_total_balances.csv')
    targets = pd.read_csv('data/anonymised_targets.csv')

    new_balances, new_targets = reduce_data(balances, targets)

    if len(argv) > 0:
        patientId = int(argv[0])
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
    
    target_av = []
    for i in range(0,len(target_low)):
        target_av.append(int((target_low[i]+target_high[i])/2))
        
    target_min = np.int_(target_min)
    #print(type(target_min))
    #rounded_target_min = []
    #for i in range(0,len(target_min)):
    #    rounded_target_min.append(round(target_min,0)) # hoping rounding will give some overlapping values
    # doesn't work because nd.arrays don't like round
    
    rounded_fluid_min = []
    for i in range(0,len(fluid_min)):
        rounded_fluid_min.append(np.round(fluid_min,0))
        
    

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(fluid_min, fluid_cum)
    #ax.plot(target_min, target_low, linewidth=2, c='r')
    #ax.plot(target_min, target_high, linewidth=2, c='g')
    ax.plot(target_min, target_av, linewidth=3, c = 'y')
    plt.show()
    
    #print(bool(set(target_min) & set(rounded_fluid_min)))
    
   
    fluid_cum = np.int_(fluid_cum)
    
    overlaps = list(set(fluid_min) & set(target_min))
    print(overlaps)
    first_shared_time = overlaps[0]
    first_shared_time_pos = fluid_min.index(first_shared_time)
    
    new_fluid_min = fluid_min[first_shared_time_pos:len(fluid_min)]
    new_fluid_cum = fluid_cum[first_shared_time_pos:len(fluid_cum)] # reduce fluid_cum to same range
    
    
    # can now compare fluid_cum and target_av as their i indexes should be at same / similar time
    Euc_dist_list = []
    for i in range(0,len(target_av)):
        Euc_dist_list.append(abs((int(new_fluid_cum[i]) - target_av[i])^2))
    print("total Euclidean distance:")
    print(np.sqrt(sum(Euc_dist_list)))
    
    
        
    

if __name__ == "__main__":
    main(sys.argv[1:])