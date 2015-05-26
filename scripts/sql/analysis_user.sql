create table if not exists distinct_login_daily(day string,uid int,org int,agent int);
insert overwrite table distinct_login_daily select a.day,a.uid,b.org,b.agent from (select day,uid from login_daily where platform <> 'python' group by day,uid) a left outer join tb_user b on a.uid = b.uid; 

create table if not exists login_first_day (uid int,day string);
insert overwrite table login_first_day select uid,min(day) as day from distinct_login_daily group by uid;

create table if not exists login_last_day (uid int,day string);
insert overwrite table login_last_day select uid,max(day) as day from distinct_login_daily group by uid;

create table if not exists user_inc_daily(day string,inc_count int);
insert overwrite table user_inc_daily select day,count(uid) as inc_count from login_first_day group by day;

create table if not exists user_inc_month(mon string,inc_count int);
insert overwrite table user_inc_month select mon,sum(inc_count) as inc_count from (select from_unixtime(unix_timestamp(day,'yyyy-MM-dd'),'yyyy-MM') as mon,inc_count from user_inc_daily) a group by mon;


create table if not exists user_lost_daily(day string,lost_count int);
insert overwrite table user_lost_daily select day,count(uid) as lost_count from login_last_day group by day;

create table if not exists user_lost_month(mon string,lost_count int);
insert overwrite table user_lost_month select mon,sum(lost_count) as lost_count from (select from_unixtime(unix_timestamp(day,'yyyy-MM-dd'),'yyyy-MM') as mon,lost_count from user_lost_daily) a group by mon;


create table if not exists recent_onlineuser_of_agent(agent_name string,user_count int);
insert overwrite table recent_onlineuser_of_agent select b.name as agent_name,a.user_count from (select agent,count(distinct uid) as user_count from distinct_login_daily where day >= '2015-04-01' and day < '2015-05-01' group by agent) a left outer join tb_agent b on a.agent = b.agent order by a.user_count desc;

create table if not exists area_login_daily(day string,country string,proivncy string,city string,user_count int);
insert overwrite table area_login_daily select day,country,proivncy,city,count(distinct uid) as user_count from login_daily group by day,country,proivncy,city;


create table if not exists proivncy_alive(proivncy string,user_count int);
insert overwrite table proivncy_alive select proivncy,count(distinct uid) as user_count from login_daily where day >= '2015-01-01' group by proivncy order by user_count desc;




