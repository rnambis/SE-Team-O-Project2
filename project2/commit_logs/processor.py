import csv
import math
import matplotlib.pyplot as plt
import numpy as np

def per_day(info, max_days):
    day_list = range(max_days + 1)
    day_list_jr = []

    for day in day_list:
        count = 0
        for inf in info:
	    if inf[1] == day:
                count += 1
        day_list_jr.append(count)
    return day_list_jr

def rate(info):
    dayno = []
    date = []

    for inf in info:
        dayno.append(float(inf[3]))
	date.append(float(inf[1]))
    return dayno, date

with open('teamp_commit.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    info = []
    info2 = []
    for row in reader:
        info.append([row['author'], str(int(math.floor(float(row['date'])))/60/60/24), row['message'], row['']])
        first_date = info[-1][1]

    for inf in info:
        info2.append([inf[0], int(inf[1]) - int(first_date), inf[2], inf[3]])

    max_days = int(info2[0][1])
    per_day_list = per_day(info2, max_days)

    plt.figure()
    plt.boxplot(per_day_list, 0, 'rs', 0)
    plt.show()

    dayno, date = rate(info2)
    dayno = dayno[::-1]
    plt.plot(date, dayno)
    plt.show()

        
