import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import plotly
import plotly.graph_objs as go
import re,datetime


def secs(d0):
  d     = datetime.datetime(*map(int, re.split('[^\d]', d0)[:-1]))
  epoch = datetime.datetime.utcfromtimestamp(0)
  delta = d - epoch
  return delta.total_seconds()


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

def per_day_norm_com(info, max_days):
    day_list = range(max_days + 1)
    day_list_jr = []
    for day in day_list:
        count = 0
        for inf in info:
            if inf[1] == day:
                count += 1
        day_list_jr.append(count)
    daddy_day = max(day_list_jr)
    day_list_jr = [x/daddy_day for x in daddy_day]
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

def pie_sectioner(info):
    ppl = list(set([inf[0] for inf in info]))
    count = [0] * len(ppl)
    for x in ppl:
        for y in info:
            if x == y[0]: count[ppl.index(x)] += 1
    return count, [ 'User '+ str(ppl.index(x)) for x in ppl]


def annon(x): return ['o','p','h'].index(x)

#=(A2 - MIN(A$2:A$1000)) / (MAX(A$2:A$1000) - MIN(A$2:A$1000))
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
    ax.set_ylabel('Normalized Cumulative Number of Commits to Project Completion')
    ax.set_xlabel('Normalized Time to Project Completion')
    ax.legend()
    ax.legend(loc='lower right')
    plt.show()


def per_day_line():
    fig  = plt.figure()
    ax = fig.add_subplot(111)
    for x, c in zip(['o','p','h'], ['r', 'b', 'g']):
        with open('team'+x+'_commit_norm.csv') as csvfile:
            print x
            reader = csv.DictReader(csvfile)
            info = []
            info2 = []
            for row in reader:
                info.append([row['author'], str(int(math.floor(float(row['date'])))/60/60/24), row['message'], row['commit number'], row['normalized commit number'], row['normalized date'], row['author']])
                first_date = info[-1][1]

            for inf in info:
                info2.append([inf[0], int(inf[1]) - int(first_date), inf[2], inf[3], inf[4], inf[5], inf[6]])

            max_days = int(info2[0][1])
            per_day_list = per_day(info2, max_days)

            ax.plot(per_day_list, color=c, label=str('group ' + str(annon(x))))

    ax.set_title('Number of Commits per Day')
    ax.set_ylabel('Number of Commits')
    ax.set_xlabel('Days since Initial Commit')
    ax.legend()
    plt.show()

def heatmap():
    fig  = plt.figure()
    ax = fig.add_subplot(111)
    groups = []
    for x, c in zip(['o','p','h'], ['r', 'b', 'g']):
        with open('team'+x+'_commit_norm.csv') as csvfile:
            print x
            reader = csv.DictReader(csvfile)
            info = []
            info2 = []
            for row in reader:
                info.append([row['author'], str(int(math.floor(float(row['date'])))/60/60/24), row['message'], row['commit number'], row['normalized commit number'], row['normalized date'], row['author']])
                first_date = info[-1][1]

            for inf in info:
                info2.append([inf[0], int(inf[1]) - int(first_date), inf[2], inf[3], inf[4], inf[5], inf[6]])

            max_days = int(info2[0][1])
            per_day_list = per_day(info2, max_days)
            while len(per_day_list) < 91:
                per_day_list.append(0)
            groups.append([7 if x > 7 else x for x in per_day_list])
    layout = go.Layout(
        title='Heatmap of Commits Per Day',
        xaxis=dict(
            title='Days Since Inital Commit',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#000000'
            )
        ),
        yaxis=dict(
            title='Group Number',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#000000'
            )
        )
    )
    trace = go.Heatmap(z=groups[::-1], y=['Group 2','Group 1','Group 0'])
    data = [trace]
    plotly.offline.plot(go.Figure(data=data, layout=layout), filename='basic-heatmap')

    ax.set_title('Number of Commits per Day')
    ax.set_ylabel('Number of Commits')
    ax.set_xlabel('Days since Initial Commit')
    ax.legend()
    plt.show()

def per_day_line_milestone():
    fig  = plt.figure()
    ax = fig.add_subplot(111)
    for x, c in zip(['o','p','h'], ['r', 'b', 'g']):
    #for x, c in zip(['h'], ['g']):
        with open('team'+x+'_commit_norm.csv') as csvfile:
            print x
            reader = csv.DictReader(csvfile)
            info = []
            info2 = []
            for row in reader:
                info.append([row['author'], str(int(math.floor(float(row['date'])))/60/60/24), row['message'], row['commit number'], row['normalized commit number'], row['normalized date'], row['author']])
            first_date = info[-1][1]

            for inf in info:
                info2.append([inf[0], int(inf[1]) - int(first_date), inf[2], inf[3], inf[4], inf[5], inf[6]])

            max_days = int(info2[0][1])
            per_day_list = per_day(info2, max_days)

            ax.bar(range(len(per_day_list)), per_day_list, color=c, label=str('group ' + str(annon(x))))
            #ax.plot(per_day_list, color=c, label=str('group ' + str(annon(x))))

            import json
            from pprint import pprint

            with open('../milestone_json/' + x + 'mile.txt') as data_file:
                data = json.load(data_file)

            for gob in data:
                try:
                    lineos = (int(math.floor(float(secs(gob['due_on']))))/60/60/24 - int(first_date)) + 1
                    ax.plot((lineos, lineos), (0, 40), color=c)
                except:
                    pass

    ax.set_title('Number of Commits per Day')
    ax.set_ylabel('Number of Commits')
    ax.set_xlabel('Days since Initial Commit')
    ax.set_ylim([0, 40])
    ax.set_xlim([0, 90])
    ax.legend(loc='lower right')
    plt.show()

def milestone_timeline():
    fig  = plt.figure()
    ax = fig.add_subplot(111)

    #for x, c in zip(['o','p','h'], ['r', 'b', 'g']):
    for x, c in zip(['o'], ['r']):
        import json
        from pprint import pprint

        with open('../milestone_json/' + x + 'mile.txt') as data_file:
            data = json.load(data_file)

        days_over = []
        for gob in data:
            try:
                cl = (int(math.floor(float(secs(gob['closed_at']))))/60/60/24) - 17180
                du = (int(math.floor(float(secs(gob['due_on']))))/60/60/24) - 17180
                days = cl - du
                days_over.append(days)
            except:
                print x
                print 'no work'
        ax.bar(range(len(days_over)), sorted(days_over), color=c)

    ax.set_title('Milestone Due Date vs Close Date for Group '+str(annon(x)))
    ax.set_ylabel('Number of Days Milestone Closed Past Due Date')
    ax.set_xlabel('Milestone Number')
    ax.legend(loc='lower right')
    plt.show()

def per_day_line_universal_due_date():
    fig  = plt.figure()
    #ax = fig.add_subplot(111)
    f, (p1, p2, p3) = plt.subplots(3, sharex=True)
    p1.set_title('Number of Commits Per Day w/ Class Due Date Markers')
    for x, c, p in zip(['o','p','h'], ['r', 'b', 'g'], [p1, p2, p3]):
    #for x, c in zip(['o','p','h'], ['r', 'b', 'g']):
        with open('team'+x+'_commit_norm.csv') as csvfile:
            print x
            reader = csv.DictReader(csvfile)
            info = []
            info2 = []
            for row in reader:
                info.append([row['author'], str(int(math.floor(float(row['date'])))/60/60/24), row['message'], row['commit number'], row['normalized commit number'], row['normalized date'], row['author']])
            first_date = info[-1][1]

            for inf in info:
                info2.append([inf[0], int(inf[1]) - int(first_date), inf[2], inf[3], inf[4], inf[5], inf[6]])

            max_days = int(info2[0][1])
            per_day_list = per_day(info2, max_days)

            p.bar(range(len(per_day_list)), per_day_list, color=c, label=str('group ' + str(annon(x))))
            #ax.bar(range(len(per_day_list)), per_day_list, color=c, label=str('group ' + str(annon(x))))
            #ax.plot(per_day_list, color=c, label=str('group ' + str(annon(x))))


            import json
            from pprint import pprint

            with open('../milestone_json/' + x + 'mile.txt') as data_file:
                data = json.load(data_file)

            for gob in data:
                try:
                    lineos = (int(math.floor(float(secs(gob['due_on']))))/60/60/24 - int(first_date)) + 1
                    p.plot((lineos, lineos), (0, 40), color=c)
                except:
                    pass
            '''
            for day in [17, 45, 76]:
                try:
                    day += 1
                    #ax.plot((day, day), (0, 40), 'k')
                    p.plot((day, day), (0, 40), 'k')
                except:
                    pass'''

        p.set_ylabel('Number of Commits')
        #p.set_xlabel('Days since Initial Commit')
        p.set_ylim([0, 35])
        p.set_xlim([0, 91])
    '''ax.set_title('Number of Commits per Day')
    ax.set_ylabel('Number of Commits')
    ax.set_xlabel('Days since Initial Commit')
    ax.set_ylim([0, 40])
    ax.set_xlim([0, 90])
    ax.legend()'''
    p3.set_xlabel('Days since Initial Commit')
    plt.show()

def box_whisker():
    f, (p1, p2, p3) = plt.subplots(3, sharex=True)
    p1.set_title('Number of Commits Per Day')
    for x, c, p in zip(['o','p','h'], ['r', 'b', 'g'], [p1, p2, p3]):
        with open('team'+x+'_commit_norm.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            info = []
            info2 = []
            for row in reader:
                info.append([row['author'], str(int(math.floor(float(row['date'])))/60/60/24), row['message'], row['commit number'], row['normalized commit number'], row['normalized date'], row['author']])
                first_date = info[-1][1]

            for inf in info:
                info2.append([inf[0], int(inf[1]) - int(first_date), inf[2], inf[3], inf[4], inf[5], inf[6]])

            max_days = int(info2[0][1])
            per_day_list = per_day(info2, max_days)
            print c+'o'
            p.boxplot(per_day_list, 0, c+'o', 0)
            p.set_ylabel('group ' + str(annon(x)))
    plt.show()

def box_whisker_comments():
    f, (p1, p2, p3) = plt.subplots(3, sharex=True)
    p1.set_title('Box Whisker Plot of Comments Per Issue')
    for x, data,maxD, c, p in zip(['o','p','h'],[[
        1,1,1,1,1,1,1,1,1,1,1,1
    ],[
        7,2,2,7,3,11,5,2,2,6,2,2,1,6,4,4,5,1
    ],[
        3,2,1,1,6,11,1,1,1,4,1,15,3,6,7,5,15,5,5,8,1,1,1,1,1,1,2,3,2,1,1,2,3,5,1,1,6,1,11,1,1,2,1,3,3,1,5
    ]], [26,32,88], ['r', 'b', 'g'], [p1, p2, p3]):
        print data
        while len(data) < maxD: data.append(0)
        p.boxplot(data, 0, c+'o', 0)
        p.set_ylabel('Group ' + str(annon(x)))
    p3.set_xlabel('Number of Comments')
    plt.show()

def pie():
    f, (p1, p2, p3) = plt.subplots(3)
    #p1.set_title('Number of Commits Per Day')
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

            sizes, labels = pie_sectioner(info2)
            p.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            p.set_title('group ' + str(annon(x)))
    plt.show()

per_day_line_milestone()
per_day_line_universal_due_date()
line_graph()
box_whisker()
pie()
milestone_timeline()
heatmap()
box_whisker_comments()
