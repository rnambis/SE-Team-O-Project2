from __future__ import print_function
import urllib2
import json
import re,datetime
import sys
import pandas as pd
import json

df=pd.DataFrame()
rowsList = []
final = dict()
class L():
  "Anonymous container"
  def __init__(i,**fields) : 
    i.override(fields)
  def override(i,d): i.__dict__.update(d); return i
  def __repr__(i):
    d = i.__dict__
    name = i.__class__.__name__
    return name+'{'+' '.join([':%s %s' % (k,pretty(d[k])) 
                     for k in i.show()])+ '}'
  def show(i):
    lst = [str(k)+" : "+str(v) for k,v in i.__dict__.iteritems() if v != None]
    return ',\t'.join(map(str,lst))

  
def secs(d0):
  d     = datetime.datetime(*map(int, re.split('[^\d]', d0)[:-1]))
  epoch = datetime.datetime.utcfromtimestamp(0)
  delta = d - epoch
  return delta.total_seconds()
 
def dump1(u,issues):
  token = "ad4686af68d7cf97680d0f402f3e6bdb44716dba" # <===
  request = urllib2.Request(u, headers={"Authorization" : "token "+token})
  v = urllib2.urlopen(request).read()
  w = json.loads(v)

  d={}
  # with open('teamo.json', 'w') as outfile:
  #   json.dumps(w, outfile)
  
  
  if not w: return False

  k=0
  for event in w:
    k +=1
    print(k)

    issue_id = event['issue']['number']
    created_at = secs(event['created_at'])
    action = event['event']
    user = event['actor']['login']
    milestone = event['issue']['milestone']

    labels= event['issue']['labels']
    labels_name=[]
    labels_color=[]
    for label in labels:
      labels_name.append(label['name'])
      labels_color.append(label['color'])


    
    comments = event['issue']['comments']
    #print(event[])
    if event['issue']['assignee'] is not None:
      assignee = event['issue']['assignee']['login']
    else:
      assignee=[]
    
    assignees_name=[]
    
    assignees = event['issue']['assignees']
    for each in assignees:
      assignees_name.append(each['login'])
    closed_at = secs(event['issue']['closed_at'])
    #body = event['issue']['body']
    title = event['issue']['title']
    

    if milestone != None : milestone = milestone['title']

    eventObj = L(when=created_at,
                 action = action,
                 user = user,
                 milestone = milestone,
                 comments=comments,
                 assignee = assignee,
                 assignees_name = assignees_name,
                 closed_at = closed_at,
                 labels_name = labels_name,
                 labels_color = labels_color,

                 #body=body,
                 title=title
                 )
  

    d['when']=created_at
    d['action']=action
    d['user']=user
    d['milestone']=milestone
    d['comments']=comments
    d['assignee']=assignee
    d['assignees_name']=assignees_name
    d['closed_at']=closed_at
    d['labels_name']=labels_name
    d['labels_color']=labels_color
    d['title']=title

    #print(d['title'])

    all_events = issues.get(issue_id)
    if not all_events: 
      all_events = []
      
    all_events.append(eventObj)
    rowsList.append(d)
    d={}
    final[issue_id]=rowsList
    issues[issue_id] = all_events
  return True

def dump(u,issues):
  return dump1(u, issues)

def launchDump():
  page = 1
  issues = dict()
  while(True):
    doNext = dump('https://api.github.com/repos/SE17GroupH/Zap/issues/events?page=' + str(page), issues)
    print("page "+ str(page))
    page += 1
    if not doNext : break

  count = 0
  # for issue, events in issues.iteritems():
  #   print("ISSUE " + str(issue))
  #   for event in events: 
  #     print(event.show())
  #     count +=1
  #   print('')

  #print(count)




 
  # with open('result.json', 'w') as fp:
  #   json.dump(issues, fp)
    
launchDump()
print(type(rowsList))

for each in rowsList:
  print(each['title'])
  print("\n")

df=pd.DataFrame(rowsList)
df.to_csv('teamh.csv',sep=',')

