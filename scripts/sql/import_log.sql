create external table if not exists raw_logs (line string) location '/echat/log';

set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonstict;
add file /home/hadoop/scripts/format/login.py;

create table if not exists login_daily (time string,uid int,relogin int,ip string,country string,proivncy string,city string,context string,platform string,device string) partitioned by (day string);
insert overwrite table login_daily(day) select transform(t.i) using 'python login.py' as (t,u,re,ip,c,p,city,ctx,plat,dev,day) from (select line as i from raw_logs where line like '%LOGIN%') t;

create table if not exists logout_daily (time string,uid int) partitioned by(day string);
insert overwrite table logout_daily(day) select transform(t.i) using 'python logout.py' as (t,u,day) from (select line as i from raw_logs where line like '%LOGOUT%') t;

create table if not exists get_mic_daily (time string,uid int,gid int) partitioned by(day string);
insert overwrite table get_mic_daily(day) select transform(t.i) using 'python get_mic.py' as (t,u,g,day) from (select line as i from raw_logs where line like '%GET MIC%') t;

create table if not exists lost_mic_daily (time string,uid int,gid int) partitioned by(day string);
insert overwrite table lost_mic_daily(day) select transform(t.i) using 'python lost_mic.py' as (t,u,g,day) from (select line as i from raw_logs where line like '%LOSTMIC%') t;

create table if not exists join_group_daily (time string,uid int,gid int) partitioned by(day string);
insert overwrite table join_group_daily(day) select transform(t.i) using 'python join_group.py' as (t,u,g,day) from (select line as i from raw_logs where line like '%JOIN%') t; 

create table if not exists leave_group_daily (time string,uid int,gid int) partitioned by(day string);
insert overwrite table leave_group_daily(day) select transform(t.i) using 'python leave_group.py' as (t,u,g,day) from (select line as i from raw_logs where line like '%LEAVE%') t; 


create table if not exists call_daily (time string,uid int,targets int,called int) partitioned by(day string);
insert overwrite table call_daily(day) select transform(t.i) using 'python call.py' as (t,u,tars,called,day) from (select line as i from raw_logs where line like '%CALL%') t; 

#每日新增用户
create table distinct_login_daily_tmp as select uid,day from login_daily group by uid,day; 
create table login_first_day_tmp as select uid,min(day) as day from distinct_login_daily_tmp group by uid;

create table if not exists user_inc_daily(day string,inc_count int);
insert overwrite table user_inc_daily select day,count(uid) as inc_count from login_first_day_tmp group by day;

create table if not exists user_inc_week(week int,inc_count int);
insert overwrite table user_inc_week select week,sum(inc_count) as inc_count from (select weekofyear(day) as week,inc_count from user_inc_daily) a group by week;

