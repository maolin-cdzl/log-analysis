
create table if not exists speaks_count_daily (day string,speak_count int,seconds int);
insert overwrite table speaks_count_daily select day,count(1) as speak_count,sum(micseconds) / 1000 as seconds  from speaks_daily group by day;

create table if not exists speaks_valid_count_daily (day string,speak_count int);
insert overwrite table speaks_valid_count_daily select day,count(1) as speak_count from speaks_daily where micseconds > 400 group by day;


create table if not exists speak_group_daily(day string,gid int,speak_count int,total_seconds int,average_ms int);
select day,gid,count(1) as speak_count,sum(micseconds) / 1000 as total_seconds, average(micseconds) as average_ms from speaks_daily where micseconds > 400 group by day,gid;


create table speak_max_group as select * from (select day,gid,speak_count,seconds from  speak_group_daily A where seconds = (select max(seconds) from speak_group_daily B where B.day = A.day) C group by day;


create table if not exists speak_user_daily(day string,uid int,speak_count int,seconds bigint);
select day,uid,count(1) as speak_count,sum(seconds) as seconds from speaks_daily where seconds >0 group by day,uid;

create table speak_user_stat as select day,max(seconds) as max_seconds,average(seconds) as average_seconds from speak_user_daily group by day;
