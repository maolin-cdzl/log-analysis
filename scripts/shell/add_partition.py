#coding:utf-8
#!/usr/bin/python

from __future__ import print_function
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')
import os

def get_sorted_partitions(path):
    partitions=[]
    for dirpath,dirs,files in os.walk(path):
        for d in dirs:
            partitions.append(d)

    partitions.sort()
    return partitions 

def generate_sql(root,table,subdir):
    path = ("%s/%s" %(root,subdir))
    partitions = get_sorted_partitions(path)
    for p in partitions:
        print("alter table %s add partition (day=\'%s\') location \'/echat/log/%s/%s\'" % (table,p,subdir,p))

ROOT='/media/FUN/echat/log'
LOGDIRS=[ ('login_daily','login'),('logout_daily','logout'),('onlines_daily','onlines'),('speaks_daily','speaks'),('join_group_daily','joingroup'),('leave_group_daily','leavegroup'),('call_daily','call')]

if __name__ == '__main__':
    for it in LOGDIRS:
        generate_sql(ROOT,it[0],it[1])
