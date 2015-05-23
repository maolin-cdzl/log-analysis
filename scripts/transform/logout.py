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
rExt = r"(?P<extend>.*)"

rPattern = r"INFO\s%s\s\"LOGOUT(\sBROKEN)?\s%s\s%s\"" % (rDateTime,rUid,rExt)
Pattern = re.compile(rPattern)


def parse(logline):
    matchs = Pattern.match(logline)
    if matchs is not None:
        date = matchs.group("date")
        time = matchs.group("time")
        uid = matchs.group("uid")
        print("%s\t%s\t%s" % (time,uid,date))


for line in sys.stdin:
    try:
        parse(line)
    except:
        pass
