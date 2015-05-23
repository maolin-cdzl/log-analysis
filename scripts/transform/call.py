#coding:utf-8
#!/usr/bin/python

import sys
reload(sys) 
sys.setdefaultencoding('utf-8')
import re


rDate = r"(?P<date>\d\d\d\d-\d\d-\d\d)"
rTime = r"(?P<time>\d\d:\d\d:\d\d\.\d\d\d):\d+"
rDateTime = r"%s\s%s" % (rDate,rTime)

rUid = r"uid=\((?P<uid>\d+)\)"
rTargets = r"targets=\((?P<targets>(\d+,)+)\)"
rCalled = r"call(l)?ed=\((?P<called>(\d+,)+)\)"
rExt = r"(?P<extend>.*)"

rPattern = r"INFO\s%s\s\"CALL\s%s\s%s\s%s\"" % (rDateTime,rUid,rTargets,rCalled)
Pattern = re.compile(rPattern)


def parse(logline):
    matchs = Pattern.match(logline)
    if matchs is not None:
        date = matchs.group("date")
        time = matchs.group("time")
        uid = matchs.group("uid")
        targets = matchs.group("targets")
        called = matchs.group("called")
        
        print("%s\t%s\t%d\t%d\t%s" % (time,uid,len(targets.split(",")) - 1,len(called.split(",")) - 1,date))


for line in sys.stdin:
    m = re.search(rTargets,line)
    if m is not None:
        print(m.groups())

    try:
        parse(line)
    except:
        pass



