
create external table if not exists login_daily (time string,uid int,relogin int,ip string,country string,proivncy string,city string,context string,platform string,device string) partitioned by (day string) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' location '/echat/log/login';


create external table if not exists logout_daily (time string,uid int) partitioned by(day string) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' location '/echat/log/logout';

create external table if not exists onlines_daily (uid int,login string,logout string,seconds int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' location '/echat/log/onlines';

create external table if not exists speaks_daily (gid int,uid int,start string,stop string,micseconds int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' partitioned by(day string) location '/echat/log/speaks';


create external table if not exists join_group_daily (time string,uid int,gid int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' partitioned by(day string) location '/echat/log/joingroup';

create external table if not exists leave_group_daily (time string,uid int,gid int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' partitioned by(day string) location '/echat/log/leavegroup';


create external table if not exists call_daily (time string,uid int,targets int,called int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' partitioned by(day string) location '/echat/log/call';

