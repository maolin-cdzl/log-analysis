create external table if not exists raw_logs (line string) location '/echat/log';

set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonstict;
add files transform/login.py transform/logout.py transform/join_group.py transform/leave_group.py transform/get_mic.py transform/lost_mic.py transform/call.py;

create table if not exists login_daily (time string,uid int,relogin int,ip string,country string,proivncy string,city string,context string,platform string,device string) partitioned by (day string);
insert overwrite table login_daily partition (day) select transform(t.i) using 'python login.py' as (t,u,re,ip,c,p,city,ctx,plat,dev,day) from (select line as i from raw_logs where line like '%LOGIN%') t;

create table if not exists logout_daily (time string,uid int) partitioned by(day string);
insert overwrite table logout_daily partition (day) select transform(t.i) using 'python logout.py' as (t,u,day) from (select line as i from raw_logs where line like '%LOGOUT%') t;

create table if not exists get_mic_daily (time string,uid int,gid int) partitioned by(day string);
insert overwrite table get_mic_daily partition (day) select transform(t.i) using 'python get_mic.py' as (t,u,g,day) from (select line as i from raw_logs where line like '%GET%') t;

create table if not exists lost_mic_daily (time string,uid int,gid int) partitioned by(day string);
insert overwrite table lost_mic_daily partition (day) select transform(t.i) using 'python lost_mic.py' as (t,u,g,day) from (select line as i from raw_logs where line like '%LOSTMIC%') t;

create table if not exists join_group_daily (time string,uid int,gid int) partitioned by(day string);
insert overwrite table join_group_daily partition (day) select transform(t.i) using 'python join_group.py' as (t,u,g,day) from (select line as i from raw_logs where line like '%JOIN%') t; 

create table if not exists leave_group_daily (time string,uid int,gid int) partitioned by(day string);
insert overwrite table leave_group_daily partition (day) select transform(t.i) using 'python leave_group.py' as (t,u,g,day) from (select line as i from raw_logs where line like '%LEAVE%') t; 


create table if not exists call_daily (time string,uid int,targets int,called int) partitioned by(day string);
insert overwrite table call_daily partition (day) select transform(t.i) using 'python call.py' as (t,u,tars,called,day) from (select line as i from raw_logs where line like '%CALL%') t; 

