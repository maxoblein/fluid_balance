import csv
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from adjust_data import *
import sys

def timeofday(distHour):
    #using the hourly distances can we decide
    #if doctors miss targets at certain times of Day
    print(distHour.head())
    print(max(distHour['DistFromTar'].values))
    minutes = distHour['Minute'].values
    hour_of_day = np.round(minutes/60)%24
    hour_of_dayuni = np.unique(hour_of_day)
    distHour['hour of day'] = hour_of_day
    hourvalues = []
    for i in hour_of_dayuni:
        hourindex = np.argwhere(hour_of_day == i)
        arr = []
        for j in hourindex:
            arr.append(list(distHour['DistFromTar'].values[j])[-1])
        hourvalues.append(arr)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.boxplot(hourvalues)
    ax.set_title('Target missing based on hour of day')
    ax.set_xlabel('hour of day')
    ax.set_ylabel('amount target missed by')
    plt.show()

def dayofweek(distDaily):
    print(distDay.head())
    day = distDay['Day'].values
    weekday = day%7
    distDay['day of week'] = weekday
    weekdayuni = np.unique(weekday)
    dayvalues = []


    for i in weekdayuni:
        dayindex = np.argwhere(weekday == i)
        arr = []
        for j in dayindex:
            arr.append(list(distDay['TotalDayDist'].values[j])[-1])
        dayvalues.append(arr)


    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.boxplot(dayvalues)
    ax.set_title('Target missing based on days of week')
    ax.set_xlabel('day of week')
    ax.set_ylabel('amount target missed by')
    plt.show()



if __name__ == '__main__':

    distHour = pd.read_csv('distHourly.csv')
    distDay = pd.read_csv('distDaily.csv')
    timeofday(distHour)
    #dayofweek(distDay)
