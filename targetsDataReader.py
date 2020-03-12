import csv
from matplotlib import pyplot as plt
import numpy as np
from statistics import mean
from datetime import datetime

line_count = 0

minutesSinceAdmission = []
encounterId = []
valueString = []
recordDay = []
timeOfDay = [] 

filename = "data/anonymised_targets.csv"
with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        if line_count != 0:
            minutesSinceAdmission.append(float(row[1]))
            encounterId.append(int(row[2]))
            valueString.append(row[3])
            recordDay.append(int(row[4]))
            timeOfDay.append(row[5])
            # timeOfDay.append(datetime.strptime(row[5], '%H:%M:%S')) # if we want it in the date and time format
        line_count += 1

# Change the target strings into integers 
targets = []
for i in range(len(valueString)):
    valueString[i] = valueString[i].replace(" ", "")

    if valueString[i] == '0ml':
        targets.append(0)

    elif valueString[i][0] == '0' or valueString[i][0] == '+' or valueString[i][0] == '-':
        valueString[i] = valueString[i].replace("ml", "")
        valueString[i] = valueString[i].replace("to", ",")
        index = valueString[i].index(',')
        targets.append([float(valueString[i][:index]),float(valueString[i][(1+index):])])

    elif valueString[i] == 'Notapplicable':
        targets.append(0) # DON'T KNOW WHAT TO DO WITH THESE ONES
  
