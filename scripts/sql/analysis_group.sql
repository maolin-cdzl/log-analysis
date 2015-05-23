set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonstict;
create table if not exists speaks_daily (gid int,uid int,start string,stop string,seconds int) partitioned by (day string);

insert overwrite table speaks_daily partition(day) select B.gid, B.uid, from_unixtime(A.start) as start,from_unixtime(min(B.stop)) as stop,(min(B.stop) - A.start) as seconds,A.day from (select gid,uid,unix_timestamp(concat(day,' ',time)) as start,day from get_mic_daily) A,(select gid,uid,unix_timestamp(concat(day,' ',time)) as stop from lost_mic_daily) B where A.gid = B.gid and A.uid = B.uid and B.stop > A.start group by B.gid,B.uid,A.day,A.start;

create table if not exists speaks_count_daily (day string,int speak_count);
insert overwrite speaks_count_daily select day,count(1) as speak_count,sum(seconds) as total_seconds)  from speaks_daily group by day;

create table if not exists speaks_valid_count_daily (day string,int speak_count,total_seconds bigint);
insert overwrite speaks_valid_count_daily select day,count(1) as speak_count,sum(seconds) as total_seconds from speaks_daily where seconds > 0 group by day;


create table if not exists speak_group_daily(day string,gid int,speak_count int,seconds bigint);
select day,gid,count(1) as speak_count,sum(seconds) as seconds from speaks_daily where seconds > 0 group by day,gid;

create table speak_group_stat as select day,max(seconds) as max_seconds,average(seconds) as average_seconds from speak_group_daily group by day;

create table speak_max_group as select * from (select day,gid,speak_count,seconds from  speak_group_daily A where seconds = (select max(seconds) from speak_group_daily B where B.day = A.day) C group by day;


create table if not exists speak_user_daily(day string,uid int,speak_count int,seconds bigint);
select day,uid,count(1) as speak_count,sum(seconds) as seconds from speaks_daily where seconds >0 group by day,uid;

create table speak_user_stat as select day,max(seconds) as max_seconds,average(seconds) as average_seconds from speak_user_daily group by day;
