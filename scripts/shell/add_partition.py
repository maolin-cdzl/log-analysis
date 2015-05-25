#coding:utf-8
#!/usr/bin/python

import sys
reload(sys) 
sys.setdefaultencoding('utf-8')
import os
from datetime import datetime,timedelta

def get_sorted_partitions(start,stop):
    oneday = timedelta(days=1)
    day = datetime.strptime(start,"%Y-%m-%d").date()
    stopday = datetime.strptime(stop,"%Y-%m-%d").date()
    partitions=[]

    while day <= stopday:
        partitions.append( day.strftime('%Y-%m-%d') )
        day = day + oneday
    return partitions 

def generate_sql(table,path,partitions):
    for p in partitions:
        print("alter table %s add partition (day=\'%s\') location \'%s/%s\'" % (table,p,path,p))

TABLES =[ 
        ('login_daily','/echat/log/login'),
        ('logout_daily','/echat/log/logout'),
        ('onlines_daily','/echat/log/onlines'),
        ('speaks_daily','/echat/log/speaks'),
        ('join_group_daily','/echat/log/joingroup'),
        ('leave_group_daily','/echat/log/leavegroup'),
        ('call_daily','/echat/log/call')]

if __name__ == '__main__':
    partitions = get_sorted_partitions(sys.argv[1],sys.argv[2])
    for it in TABLES:
        generate_sql(it[0],it[1],partitions)
