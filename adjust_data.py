import csv
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import re
import warnings
warnings.filterwarnings("ignore")


def parseNumber(value, as_int=False):
    try:
        number = float(re.sub('[^.\-\d]', '', value))
        if as_int:
            return int(number + 0.5)
        else:
            return number
    except ValueError:
        return float('nan')  # or None if you wish


def add_day_of_week(data):

    record_days = data['record day'].values
    day_of_week = (record_days % 7)
    data['day of week'] = day_of_week
    return data

def fix_targets(targets):
    target_strings = np.copy(targets['valueString'].values)
    target_strings_keep = np.copy(targets['valueString'].values)
    for i in range(len(target_strings)):
        target_strings[i] = target_strings[i].replace("ml", "")
        target_strings[i] = target_strings[i].replace(" to ", ",")
        target_strings[i] = target_strings[i].replace(" ", "")
        if ',' in target_strings[i]:
            trange = target_strings[i].split(',')
            for j in range(len(trange)):
                trange[j] = parseNumber(trange[j])
            target_strings[i] = np.array([float(trange[0]),float(trange[1])])
        else:
            target_strings[i] = np.array([0.0,0.0])

    targets['valueString'] = target_strings_keep
    targets['NumTargets'] = target_strings
    return targets
