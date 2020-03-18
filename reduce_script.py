import csv
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from adjust_data import *

balances = pd.read_csv('data/anonymised_total_balances.csv')
targets = pd.read_csv('data/anonymised_targets.csv')
balances = balances.drop(balances.columns[0],axis=1)
targets = targets.drop(targets.columns[0],axis=1)

new_balances = remove_negatives(balances, 'minutes since admission')
new_targets = remove_negatives(targets, 'minutes since admission')

targetids = set(new_targets.encounterId.unique())
sharedids = targetids.intersection(set(new_balances.encounterId.unique()))

new_balances = new_balances[new_balances['encounterId'].isin(sharedids)]
new_balances = add_day_of_week(new_balances)
new_balances.to_csv('new_balances.csv')

new_targets = new_targets[new_targets['encounterId'].isin(sharedids)]
new_targets = add_day_of_week(new_targets)
new_targets = fix_targets(new_targets)
new_targets.to_csv('new_targets.csv')
