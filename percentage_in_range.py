import csv
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

balances = pd.read_csv('new_balances.csv')
targets = pd.read_csv('new_targets.csv')


def stay_data(balances,targets,id):

    #collect all data for one stay in one place

    stay_balances = balances.loc[balances['encounterId'] == id]
    stay_targets = targets.loc[targets['encounterId'] == id]

    return stay_balances, stay_targets


stay_balances, stay_targets = stay_data(balances,targets,17014)

stay_balances.to_csv('17014_balances.csv')
stay_targets.to_csv('17014_targets.csv')

fluid_stay = stay_balances.loc[stay_balances['longLabel'] == 'Net Body Balance (LOS)']
