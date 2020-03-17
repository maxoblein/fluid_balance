import csv
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

balances = pd.read_csv('data/anonymised_total_balances.csv')
targets = pd.read_csv('data/anonymised_targets.csv')

targetids = set(targets.encounterId.unique())
sharedids = targetids.intersection(set(balances.encounterId.unique()))

new_balances = balances[balances['encounterId'].isin(sharedids)]
new_balances.to_csv('new_balances.csv')

new_targets = targets[targets['encounterId'].isin(sharedids)]
new_targets.to_csv('new_targets.csv')