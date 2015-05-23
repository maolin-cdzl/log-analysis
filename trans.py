#!/usr/bin/python

import sys
import re
import IP

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

rLogin = r"INFO\s%s\s\"(LOGIN|RELOGIN)\s%s\s%s\s%s\s%s\s%s\s%s\s%s\"" % (rDateTime,rUid,rIP,rVersion,rPlatform,rDevice,rPayload,rExt)
LoginPatten = re.compile(rLogin)
ContextPattern = re.compile(rContext)

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
        print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (time,uid,ip,country,proivnce,city,ctx,platform,device,date))
        return True
    return False

for line in sys.stdin:
    try:
        parseLogin(line)
    except:
        print('ERROR: %s' % line)
        pass

