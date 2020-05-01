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
            target_strings[i] = np.array([-250.0,250.0])

    targets['valueString'] = target_strings_keep
    targets['NumTargets'] = target_strings
    return targets


def remove_negatives(dataframe, colheading):
    indexName = dataframe[dataframe[colheading] < 0].index
    dataframe.drop(indexName, inplace=True)
    return dataframe


def reduce_data(balances, targets):
    balances = balances.drop(balances.columns[0],axis=1)
    targets = targets.drop(targets.columns[0],axis=1)

    new_balances = remove_negatives(balances, 'minutes since admission')
    new_targets = remove_negatives(targets, 'minutes since admission')

    targetids = set(new_targets.encounterId.unique())
    sharedids = targetids.intersection(set(new_balances.encounterId.unique()))

    new_balances = new_balances[new_balances['encounterId'].isin(sharedids)]
    new_balances = add_day_of_week(new_balances)

    new_targets = new_targets[new_targets['encounterId'].isin(sharedids)]
    new_targets = add_day_of_week(new_targets)
    new_targets = fix_targets(new_targets)
    return new_balances, new_targets


def patient_summary():

    summaries = pd.read_csv('data/anonymised_patient_summary.csv')
    patient_summaries_reduced = {}
    patient_summaries_full = {}

    patient_summaries_full['Key'] = ['Age','Gender','Weight','Height', 'Length of Stay']

    patients = summaries['encounterId'].values
    age = summaries['age'].values    
    gender = summaries['gender'].values
    weight = summaries['weight'].values
    height = summaries['height'].values
    lengthOfStay = summaries['lengthOfStay (mins)'].values

    for i in range(len(patients)):
        patient_summaries_full[patients[i]] = [age[i],gender[i],weight[i],height[i],lengthOfStay[i]]
       
    return patient_summaries_full


