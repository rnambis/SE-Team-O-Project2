from __future__ import print_function
import urllib2
import json
import re,datetime
import sys
 
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
  token = "f8faf2b87e761ed90a574d7db6810a8f34846bcc" # <===
  request = urllib2.Request(u, headers={"Authorization" : "token "+token})
  v = urllib2.urlopen(request).read()
  w = json.loads(v)
  if not w: return False
  for event in w:
    issue_id = event['issue']['number']
    created_at = secs(event['created_at'])
    action = event['event']
    user = event['actor']['login']
    milestone = event['issue']['milestone']
    if milestone != None : milestone = milestone['title']
    eventObj = L(when=created_at,
                 action = action,
                 user = user,
                 milestone = milestone)
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
    doNext = dump('https://api.github.com/repos/opensciences/opensciences.github.io/issues/events?page=' + str(page), issues)
    print("page "+ str(page))
    page += 1
    if not doNext : break
  for issue, events in issues.iteritems():
    print("ISSUE " + str(issue))
    for event in events: print(event.show())
    print('')
    
launchDump()
