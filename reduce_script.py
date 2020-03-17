import csv
from matplotlib import pyplot as plt
import numpy as np
from statistics import mean
from datetime import datetime
import pandas as pd

data = pd.read_csv("data/anonymised_total_balances.csv")

reduced_data = data.loc[data['encounterId']>=17544]

reduced_data.to_csv("reduced_total_balances.csv")