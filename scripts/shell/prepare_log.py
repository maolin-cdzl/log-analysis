#coding:utf-8
#!/usr/bin/python

from __future__ import print_function
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')
import os,errno
import getopt
import re
import time
from datetime import datetime
import IP

global ROOT
global PREFIX
SITE_NAME = "0001"
PREFIX = 'echat.log.'
ROOT = '.'
OUTDIR = 'echat/logs'
START = None

rDate = r"(?P<date>\d\d\d\d-\d\d-\d\d)"
rDateTime = r"(?P<dt>\d\d\d\d-\d\d-\d\d\s\d\d:\d\d:\d\d\.\d\d\d):\d+"

rUid = r"uid=\((?P<uid>\d+)\)"
rGid = r"gid=\((?P<gid>\d+)\)"
rIP = r"address=\((?P<ip>[\d.]*):\d+\)"
rVersion = r"version=\((?P<version>\d+)\)"
rPlatform = r"platform=\((?P<platform>\w+)\)"
rDevice = r"device=\((?P<device>[\d\s\w]+)\)"
rPayload = r"expect_payload=\((?P<payload>\d+)\)"
rExt = r"(?P<extend>.*)"
rContext = r"context=\((?P<ctx>[\w\d]+)\)"
rTargets = r"targets=\((?P<targets>(\d+,)+)\)"
rCalled = r"call(l)?ed=\((?P<called>(\d+,)+)\)"


rLogin = r"%s\s%s\s%s\s%s\s%s\s%s\s%s" % (rUid,rIP,rVersion,rPlatform,rDevice,rPayload,rExt)
rLogout = r"%s\s%s" % (rUid,rExt)
rGetMic = r"%s\s%s" % (rUid,rGid)
rLostMic = r"%s\s%s" % (rUid,rGid)
rJoinGroup = r"%s\s%s" % (rUid,rGid)
rLeaveGroup = r"%s\s%s" % (rUid,rGid)
rCall = r"%s\s%s\s%s" % (rUid,rTargets,rCalled)

rAction = r"(?P<action>[A-Z\s]+)"
rContent = r"(?P<content>.*)"
rPattern = r"^INFO\s%s\s\"%s\s%s\"$" % (rDateTime,rAction,rContent)

DatePattern = re.compile(rDate)
LinePattern = re.compile(rPattern)
LoginPattern = re.compile(rLogin)
LogoutPattern = re.compile(rLogout)
GetMicPattern = re.compile(rGetMic)
LostMicPattern = re.compile(rLostMic)
JoinGroupPattern = re.compile(rJoinGroup)
LeaveGroupPattern = re.compile(rLeaveGroup)
CallPattern = re.compile(rCall)
ContextPattern = re.compile(rContext)

class DailyPartitionFile:
    def __init__(self,path,name):
        self.path = path
        self.name = name
        self.today = None
        self.file_today = None
        self.file_old = {}

    def passday(self,day):
        assert(self.today is not None)
        assert(self.file_today is not None)
        print("%s update partition to %s" % (self.path,day.isoformat()))

        days = self.file_old.keys()
        if len(days) > 10:
            for day in days:
                if (self.today - day).days > 8:
                    self.file_old[day].close()
                    del self.file_old[day]
        
        self.file_old[self.today] = self.file_today
        self.today = None
        self.file_today = None
        self.setday(day)

    def setday(self,day):
        assert( self.today is None )
        assert( self.file_today is None)
        self.today = day
        mkdir_p( "%s/%s" % ( self.path,day.isoformat()) )
        self.file_today = open( ("%s/%s/%s" % ( self.path,day.isoformat(),self.name)), "w")


    def write(self,day,line):
        if self.today is None:
            self.setday(day)
            f = self.file_today
        elif day == self.today:
            f = self.file_today
        elif day > self.today:
            self.passday(day)
            f = self.file_today
        else:
            f = self.file_old.get(day)
        
        if f is not None:
            print(line,file=f)
        else:
            print("%s out of date,today is %s,target day is %s" % (self.path,self.today.isoformat(),day.isoformat()))
    
    def close(self):
        if self.file_today:
            self.file_today.close()
            self.file_today = None
        self.today = None
        days = self.file_old.keys()
        for day in days:
            self.file_old[day].close()
        self.file_old.clear()



def usage():
    print('usage:')
    print("\t")

def mkdir_p(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise 

def find_address(ip):
    country = "unknown"
    proivnce = "unknown"
    city = "unknown"

    try:
        address = IP.find(ip)

        if address:
            details = address.split("\t")
            if len(details) > 0:
                country = details[0]
                if len(details) > 1:
                    proivnce = details[1]
                    if len(details) > 2:
                        city = details[2]
    except:
        pass

    return country,proivnce,city
onlines = {}
speaking = {}

global fonlines,fspeaks,flogin,flogout,fjoin,fleave,fcall

def login(dt,action,content):
    matchs = LoginPattern.match(content)
    if matchs is not None:
        uid = matchs.group("uid")
        ip = matchs.group("ip")
        platform = matchs.group("platform")
        device = matchs.group("device")
        extend = matchs.group("extend")
        ctx = "unkown"
        isre = 0
        if action.startswith("RELOGIN"):
            isre = 1
        ctxmatch = ContextPattern.search(extend)
        if ctxmatch is not None:
            ctx = ctxmatch.group("ctx")

        country,proivnce,city = find_address(ip)
        flogin.write(dt.date(),("%s\t%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (dt.time().isoformat(),uid,isre,ip,country,proivnce,city,ctx,platform,device)))

        if not onlines.has_key(uid):
            onlines[uid] = dt


def logout(dt,action,content):
    matchs = LogoutPattern.match(content)
    if matchs is not None:
        uid = matchs.group("uid")
        flogout.write(dt.date(),("%s\t%s" % (dt.time().isoformat(),uid)))

        if onlines.has_key(uid):
            t0 = onlines[uid]
            if dt > t0:
                fonlines.write(t0.date(),('%s\t%s\t%s\t%d' % (uid,t0.isoformat(),dt.isoformat(),(dt - t0).total_seconds())))
            else:
                print('ERROR LOGOUT %s\t%s\t%s' % (uid,t0.isoformat(),dt.isoformat()))
            del onlines[uid]


def getmic(dt,action,content):
    matchs = GetMicPattern.match(content)
    if matchs is not None:
        uid = matchs.group("uid")
        gid = matchs.group("gid")
        key = (gid,uid)
        if not speaking.has_key(key):
            speaking[key] = dt

def lostmic(dt,action,content):
    matchs = LostMicPattern.match(content)
    if matchs is not None:
        uid = matchs.group("uid")
        gid = matchs.group("gid")
        key = (gid,uid)
        if speaking.has_key(key):
            t0 = speaking[key]
            if dt >= t0:
                fspeaks.write(t0.date(),('%s\t%s\t%s\t%s\t%d' % (gid,uid,t0.isoformat(),dt.isoformat(),(dt - t0).total_seconds() * 1000)))
            else:
                print('ERROR speak time: %s\t%s\t%s\t%s' % (gid,uid,t0.isoformat(),dt.isoformat()))
            del speaking[key]

def joingroup(dt,action,content):
    matchs = JoinGroupPattern.match(content)
    if matchs is not None:
        uid = matchs.group("uid")
        gid = matchs.group("gid")
        fjoin.write(dt.date(),("%s\t%s\t%s" % (dt.time().isoformat(),uid,gid)))

def leavegroup(dt,action,content):
    matchs = LeaveGroupPattern.match(content)
    if matchs is not None:
        uid = matchs.group("uid")
        gid = matchs.group("gid")
        fleave.write(dt.date(),("%s\t%s\t%s" % (dt.time().isoformat(),uid,gid)))

def call(dt,action,content):
    matchs = CallPattern.match(content)
    if matchs is not None:
        uid = matchs.group("uid")
        targets = matchs.group("targets")
        called = matchs.group("called")
        
        fcall.write(dt.date(),("%s\t%s\t%d\t%d" % (dt.time().isoformat(),uid,len(targets.split(",")) - 1,len(called.split(",")) - 1)))

def parse(line):
    m = LinePattern.match(line)
    if m is not None:
        sdt = m.group("dt")
        action = m.group("action")
        content = m.group("content")
        
        if sdt and action and content:
            dt = datetime.strptime(sdt,'%Y-%m-%d %H:%M:%S.%f')
            return dt,action,content
    return None

def analysis(dt,action,content):
    if action.endswith('LOGIN'):
        login(dt,action,content)
    elif action.startswith('LOGOUT'):
        logout(dt,action,content)
    elif action.startswith('GET'):
        getmic(dt,action,content)
    elif action.startswith('LOSTMIC'):
        lostmic(dt,action,content)
    elif action.startswith('JOIN'):
        joingroup(dt,action,content)
    elif action.startswith('LEAVE'):
        leavegroup(dt,action,content)
    elif action.startswith('CALL'):
        call(dt,action,content)
       
        
        

def proc(filepath):
    while open(filepath,'r') as f:
        lines = f.readlines(10000)
        if not lines:
            break
        for line in lines:
            try:
                dt,action,content = parse(line)
                if action:
                    analysis(dt,action,content)
            except:
                print('Error when line: %s' % line)

def get_date_of_file(f):
    m = DatePattern.search(f)
    if m:
        return m.group("date")
    return None


def get_sorted_logfiles():
    logfiles=[]
    for dirpath,dirs,files in os.walk(ROOT):
        for f in files:
            if f.startswith(PREFIX):
                if START is not None:
                    date = get_date_of_file(f)
                    if date and date >= START:
                        logfiles.append(os.path.join(dirpath,f))
                else:
                    logfiles.append(os.path.join(dirpath,f))

    logfiles.sort(key=get_date_of_file)
    return logfiles

if __name__ == '__main__':
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hr:p:s:o:",["help","root=","prefix=","start=","output="])
    except:
        usage()
        sys.exit(2)

    for opt,arg in opts:
        if opt in ("-h","--help"):
            usage()
            sys.exit()
        elif opt in ("-r","--root"):
            ROOT = arg
        elif opt in ("-p","--prefix"):
            PREFIX = arg
        elif opt in ("-s","--start"):
            START = arg
        elif opt in ("-o","--output"):
            OUTDIR = arg

    OUTDIR = os.path.abspath(OUTDIR)
    mkdir_p(OUTDIR)

    fonlines = DailyPartitionFile(("%s/%s" % (OUTDIR,"onlines")),SITE_NAME) 
    fspeaks = DailyPartitionFile(("%s/%s" % (OUTDIR,"speaks")),SITE_NAME) 
    flogin = DailyPartitionFile(("%s/%s" % (OUTDIR,"login")),SITE_NAME) 
    flogout = DailyPartitionFile(("%s/%s" % (OUTDIR,"logout")),SITE_NAME) 
    fjoin = DailyPartitionFile(("%s/%s" % (OUTDIR,"joingroup")),SITE_NAME) 
    fleave = DailyPartitionFile(("%s/%s" % (OUTDIR,"leavegroup")),SITE_NAME) 
    fcall = DailyPartitionFile(("%s/%s" % (OUTDIR,"call")),SITE_NAME) 

    logfiles = get_sorted_logfiles()
    for f in logfiles:
        print('Process file: %s' % f)
        proc(f)

    fonlines.close()
    fspeaks.close()
    flogin.close()
    flogout.close()
    fjoin.close()
    fleave.close()
    fcall.close()
    



