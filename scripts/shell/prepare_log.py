#-*-coding:utf-8-*-

from __future__ import print_function
import os
import sys
import getopt
import re
import time
from datetime import datetime

global ROOT
global PREFIX
PREFIX = 'echat.log.'
ROOT = '.'


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


rLogin = r"%s\s%s\s%s\s%s\s%s\s%s\s%s\"" % (rUid,rIP,rVersion,rPlatform,rDevice,rPayload,rExt)
rLogout = r"%s\s%s\"" % (rUid,rExt)
rGetMic = r"%s\s%s\"" % (rUid,rGid)
rLostMic = r"%s\s%s\"" % (rUid,rGid)

rAction = r"(?P<action>[A-Z\s]+)"
rContent = r"(?P<content>.*)"
rPattern = r"INFO\s%s\s\"%s\s%s\"" % (rDateTime,rAction,rContent)

UidPattern = re.compile(rUid)
GidPattern = re.compile(rGid)

Pattern = re.compile(rPattern)


def usage():
    print('usage:')
    print("\t")

onlines = {}
speaking = {}

global fonlines,fspeaks

def login(dt,uid):
    if not onlines.has_key(uid):
        onlines[uid] = dt


def logout(dt,uid):
    if onlines.has_key(uid):
        t0 = datetime.strptime(onlines[uid],'%Y-%m-%d %H:%M:%S.%f')
        t1 = datetime.strptime(dt,'%Y-%m-%d %H:%M:%S.%f')
        if t1 >= t0:
            print(('%s\t%s\t%s\t%d' % (uid,onlines[uid],dt,(t1 - t0).total_seconds())),file=fonlines)
        else:
            print('ERROR LOGOUT %s\t%s\t%s' % (uid,onlines[uid],dt))
        del onlines[uid]

def getmic(dt,gid,uid):
    key = (gid,uid)
    if not speaking.has_key(key):
        speaking[key] = dt

def lostmic(dt,gid,uid):
    key = (gid,uid)
    if speaking.has_key(key):
        t0 = datetime.strptime(speaking[key],'%Y-%m-%d %H:%M:%S.%f')
        t1 = datetime.strptime(dt,'%Y-%m-%d %H:%M:%S.%f')
        if t1 >= t0:
            print(('%s\t%s\t%s\t%s\t%d' % (gid,uid,speaking[key],dt,(t1 - t0).total_seconds())),file=fspeaks)
        else:
            print('ERROR SPEAK: %s\t%s\t%s\t%s' % (gid,uid,speaking[key],dt))
        del speaking[key]

def parse(line):
    m = Pattern.match(line)
    if m is not None:
        dt = m.group("dt")
        action = m.group("action")
        content = m.group("content")
        return dt,action,content
    else:
        return None

def analysis(dt,action,content):
    if action.endswith('LOGIN'):
        uid = UidPattern.search(content).group('uid')
        login(dt,uid)
    elif action.startswith('LOGOUT'):
        uid = UidPattern.search(content).group('uid')
        logout(dt,uid)
    elif action.startswith('GET'):
        uid = UidPattern.search(content).group('uid')
        gid = GidPattern.search(content).group('gid')
        getmic(dt,gid,uid)
    elif action.startswith('LOSTMIC'):
        uid = UidPattern.search(content).group('uid')
        gid = GidPattern.search(content).group('gid')
        lostmic(dt,gid,uid)
       
        
        

def proc(filepath):
    f = open(filepath)
    while 1:
        lines = f.readlines(10000)
        if not lines:
            break
        for line in lines:
            dt,action,content = parse(line)
            if action:
                analysis(dt,action,content)

if __name__ == '__main__':
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hr:p:",["help","root=","prefix="])
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

    logfiles=[]
    for dirpath,dirs,files in os.walk(ROOT):
        for f in files:
            if f.startswith(PREFIX):
                logfiles.append(os.path.join(dirpath,f))

    logfiles.sort()
    
    fonlines = open('onlines.log','w')
    fspeaks = open('speaks.log','w')
    proc(logfiles[0])
    fonlines.close()
    fspeaks.close()
    



