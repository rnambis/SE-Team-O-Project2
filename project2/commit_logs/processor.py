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

def line_graph_info(info):
    dayno = []
    date = []

    for inf in info:
        dayno.append(float(inf[4]))
        date.append(float(inf[5]))
    return dayno, date

def annon(x): return ['o','p','h'].index(x)

def line_graph():
    fig  = plt.figure()
    ax = fig.add_subplot(111)
    for x, c in zip(['o','p','h'], ['r', 'b', 'g']):
        with open('team'+x+'_commit_norm.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            info = []
            info2 = []
            for row in reader:
                info.append([row['author'], str(int(math.floor(float(row['date'])))/60/60/24), row['message'], row['commit number'], row['normalized commit number'], row['normalized date']])
                first_date = info[-1][1]

            for inf in info:
                info2.append([inf[0], int(inf[1]) - int(first_date), inf[2], inf[3], inf[4], inf[5]])


            dayno, date = line_graph_info(info2)
            ax.plot(date, dayno, color=c, label=str('group ' + str(annon(x))))

    ax.set_title('Normalized Number of Commits vs Time')
    ax.set_ylabel('Normalized number of commits to Project Completion')
    ax.set_xlabel('Normalized date to Project Completion')
    ax.legend()
    plt.show()

def histogram():
    f, (p1, p2, p3) = plt.subplots(3, sharex=True)
    p1.set_title('Number of Commits Per Day')
    for x, c, p in zip(['o','p','h'], ['r', 'b', 'g'], [p1, p2, p3]):
        with open('team'+x+'_commit_norm.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            info = []
            info2 = []
            for row in reader:
                info.append([row['author'], str(int(math.floor(float(row['date'])))/60/60/24), row['message'], row['commit number'], row['normalized commit number'], row['normalized date']])
                first_date = info[-1][1]

            for inf in info:
                info2.append([inf[0], int(inf[1]) - int(first_date), inf[2], inf[3], inf[4], inf[5]])

            max_days = int(info2[0][1])
            per_day_list = per_day(info2, max_days)

            p.boxplot(per_day_list, 0, c, 0)
            p.set_ylabel('group ' + str(annon(x)))
            print annon(x)
    plt.show()

line_graph()
#histogram()
