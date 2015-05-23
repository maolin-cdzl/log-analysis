#-*-coding:utf-8-*-

import os
import sys
import getopt
import re
import IP


global ROOT
global PREFIX
PREFIX = 'echat.log.'
ROOT = '.'

rYear = r"(?P<year>\d\d\d\d)"
rMon = r"(?P<month>\d\d)"
rDay = r"(?P<day>\d\d)"
rHour = r"(?P<hour>\d\d)"
rMinute = r"(?P<minute>\d\d)"
rSecond = r"(?P<second>\d\d)"

rDate = r"(?P<date>\d\d\d\d-\d\d-\d\d)"
rTime = r"(?P<time>\d\d:\d\d:\d\d\.\d\d\d):\d+"
rDateTime = r"%s\s%s" % (rDate,rTime)

rUid = r"uid=\((?P<uid>\d+)\)"
rIP = r"address=\((?P<ip>[\d.]*):\d+\)"
rVersion = r"version=\((?P<version>\d+)\)"
rPlatform = r"platform=\((?P<platform>\w+)\)"
rDevice = r"device=\((?P<device>[\d\s\w]+)\)"
rPayload = r"expect_payload=\((?P<payload>\d+)\)"
rExt = r"(?P<extend>.*)"
rContext = r"context=\((?P<ctx>[\w\d]+)\)"


logline = "INFO 2015-02-01 00:00:10.887:139680061839104 \"LOGIN uid=(1000589) address=(14.16.134.85:31388) version=(0) platform=(brew) device=(ZTE G180) expect_payload=(103) system=(NONE) card=(NONE)\""
logline = "INFO 2015-02-01 00:00:13.119:139680040859392 \"LOGIN uid=(1007984) address=(27.128.2.148:48419) version=(0) platform=(brew) device=(ZTE G180) expect_payload=(103) os=(BREW) esn=() meid=(a0000038411785) context=(rel) card=(NONE)\""
#logline = "INFO 2015-02-01 00:01:15.366:139680061839104 \"LOGIN uid=(1003328) address=(1.28.90.9:52997) version=(0) platform=(unknown) device=(unknown) expect_payload=(103) os=(4.2.2) imei=(864300028910544) context=(std)  imsi=(460006061220587)\""

rLogin = r"INFO\s%s\s\"LOGIN\s%s\s%s\s%s\s%s\s%s\s%s\s%s\"" % (rDateTime,rUid,rIP,rVersion,rPlatform,rDevice,rPayload,rExt)
LoginPatten = re.compile(rLogin)
ContextPattern = re.compile(rContext)

def usage():
    print('usage:')
    print("\t")

def find_address(ip):
    country = "unknown"
    proivnce = "unknown"
    city = "unknown"
    address = IP.find(ip)

    if address:
        details = address.split("\t")
        if len(details) > 0:
            country = details[0]
            if len(details) > 1:
                proivnce = details[1]
                if len(details) > 2:
                    city = details[2]

    return country,proivnce,city
    
def parseLogin(logline):
    matchs = LoginPatten.match(logline)
    if matchs is not None:
        date = matchs.group("date")
        time = matchs.group("time")
        uid = matchs.group("uid")
        ip = matchs.group("ip")
        platform = matchs.group("platform")
        device = matchs.group("device")
        extend = matchs.group("extend")
        ctx = "unkown"
        ctxmatch = ContextPattern.search(extend)
        if ctxmatch is not None:
            ctx = ctxmatch.group("ctx")

        country,proivnce,city = find_address(ip)
        print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (date,time,uid,ip,country,proivnce,city,ctx,platform,device))
        return True
    return False

def import_file(filepath):
    f = open(filepath)
    while 1:
        lines = f.readlines(10000)
        if not lines:
            break
        for line in lines:
            parseLogin(line)

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
    
    import_file(logfiles[0])
    



