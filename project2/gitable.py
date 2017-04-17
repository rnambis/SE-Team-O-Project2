from __future__ import print_function
import urllib2
import json
import re,datetime
import sys
import pandas as pd
import json
 
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
  token = "f3c77463acafb95306bc93aa012cddb67ecc0a42" # <===
  request = urllib2.Request(u, headers={"Authorization" : "token "+token})
  v = urllib2.urlopen(request).read()
  w = json.loads(v)

  with open('teamo.json', 'w') as outfile:
    json.dump(w, outfile)
  
  
  if not w: return False
  for event in w:
    issue_id = event['issue']['number']
    created_at = secs(event['created_at'])
    action = event['event']
    user = event['actor']['login']
    milestone = event['issue']['milestone']

    labels = event['issue']['labels']
    comments = event['issue']['comments']
    asignee = event['issue']['assignee']
    asignees = event['issue']['assignees']
    closed_at = secs(event['issue']['closed_at'])
    body = event['issue']['body']
    title = event['issue']['title']

    if milestone != None : milestone = milestone['title']

    eventObj = L(when=created_at,
                 action = action,
                 user = user,
                 milestone = milestone,
                 labels=labels,
                 comments=comments,
                 asignee = asignee,
                 asignees = asignees,
                 closed_at = closed_at,
                 body=body,
                 title=title
                 )
    all_events = issues.get(issue_id)
    if not all_events: all_events = []
    all_events.append(eventObj)
    issues[issue_id] = all_events
  return True

def dump(u,issues):
  return dump1(u, issues)

def launchDump():
  page = 1
  issues = dict()
  while(True):
    doNext = dump('https://api.github.com/repos/rnambis/SE17-group-O/issues/events?page=' + str(page), issues)
    print("page "+ str(page))
    page += 1
    if not doNext : break
  for issue, events in issues.iteritems():
    print("ISSUE " + str(issue))
    for event in events: print(event.show())
    print('')
    
launchDump()
