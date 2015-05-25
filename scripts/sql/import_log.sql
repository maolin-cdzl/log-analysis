create external table if not exists login_daily (time string,uid int,relogin int,ip string,country string,proivncy string,city string,context string,platform string,device string) partitioned by (day string) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

create external table if not exists logout_daily (time string,uid int) partitioned by(day string) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

create external table if not exists onlines_daily (uid int,login string,logout string,seconds int)  partitioned by(day string) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

create external table if not exists speaks_daily (gid int,uid int,start string,stop string,micseconds int) partitioned by(day string) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';


create external table if not exists join_group_daily (time string,uid int,gid int)  partitioned by(day string) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

create external table if not exists leave_group_daily (time string,uid int,gid int) partitioned by(day string) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';


create external table if not exists call_daily (time string,uid int,targets int,called int) partitioned by(day string) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

