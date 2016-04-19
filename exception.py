#coding:utf-8
#!/usr/bin/python

import sys
reload(sys) 
sys.setdefaultencoding('utf-8')
import re
import uuid

rDate = r"(?P<date>\d\d\d\d-\d\d-\d\d)"
rTime = r"(?P<time>\d\d:\d\d:\d\d\.\d\d\d):\d+"
rDateTime = r"%s\s%s" % (rDate,rTime)

rUid = r"uid=\((?P<uid>\d+)\)"
rGid = r"gid=\((?P<gid>\d+)\)"
rExt = r"(?P<extend>.*)"

rPattern = r"INFO\s%s\s\"LOSTMIC(\sAUTO)?\s%s\s%s\"" % (rDateTime,rUid,rGid)
Pattern = re.compile(rPattern)



class Session:
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.uid = 0
        self.ip = ''
        self.address = ''
        self.platform = ''
        self.device = ''
        self.start_time = None
        self.end_time = None
        self.exists_time = 0
        self.broke_count = 0

class Speaking:
    def __init__(self):
        self.uid = 0
        self.gid = 0
        self.session = None
        self.start_time = None
        self.end_time = None
        self.end_type = 0       # 0: user release
                                # 1: end with no audio
                                # 2: end in exception

history_sessions = {}
alive_sessions = {}

def parse(logline):
    matchs = Pattern.match(logline)
    if matchs is not None:
        date = matchs.group("date")
        time = matchs.group("time")
        uid = matchs.group("uid")
        gid = matchs.group("gid")
        print("%s\t%s\t%s\t%s" % (time,uid,gid,date))


if __name__ == '__main__':
    for line in sys.stdin:
        try:
            parse(line)
        except:
            pass

